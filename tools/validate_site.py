# -*- coding: utf-8 -*-
"""
HTML 站点校验器
================
运行： python tools/validate_site.py

校验项：
  W1  页面清单与实体数一致
  W2  每页 HTML 结构完整（DOCTYPE / html / head / body 闭合）
  W3  内嵌 JSON 可解析
  W4  站内链接全部可达（无死链）
  W5  wiki 页与实体一一对应，无孤儿页
  W6  索引页含 S5 标记与整合记录
  W7  时间轴页数据量与事件表一致
"""
import html
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
WIKI = os.path.join(DOCS, "wiki")

errors, warns, infos = [], [], []


def E(c, m):
    errors.append((c, m))


def W(c, m):
    warns.append((c, m))


def I(m):
    infos.append(m)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


ENT = load(os.path.join(DATA, "entities.json"))
TBL = load(os.path.join(DATA, "tables.json"))


def slug(eid):
    return eid.lower().replace("_", "-")


def route_to_path(route, from_dir):
    """把站内链接解析为磁盘路径"""
    route = route.split("#")[0].split("?")[0]
    if not route:
        return None
    if route.startswith(("http:", "https:", "mailto:", "javascript:", "data:")):
        return None
    p = os.path.normpath(os.path.join(from_dir, route))
    return p


# ------------------------------------------------------------------ W1/W5
expected = {f"{slug(e['id'])}.html" for e in ENT["entities"]}
try:
    import kb_documents as KD
    _mods = [KD]
    for _mn in ("kb_documents2", "kb_documents3"):
        try:
            _mods.append(__import__(_mn))
        except ImportError:
            pass
    doc_ids = [d["id"] for m in _mods
               for attr in ("DOCUMENTS", "DIARIES", "LETTERS", "SPEECHES")
               for d in getattr(m, attr, [])]
    doc_pages = {f'{i.lower().replace("_", "-")}.html' for i in doc_ids}
except ImportError:
    KD, doc_ids, doc_pages = None, [], set()
SPECIAL = {"index.html"}          # 文献总索引页
# docs/ 根目录下的顶层页面
TOP_PAGES = {"home.html", "index.html", "timeline.html"}
# 由 Markdown 转换而来的文档页 + 文档中心
try:
    import md_to_html as MD
    md_pages = {o for _g, _m, o, _t, _i, _d, _gg in MD.MD_PAGES}
    md_special = {"docs-index.html"}
except ImportError:
    MD, md_pages, md_special = None, set(), set()
# 分类型清单页（list-<group>.html）
try:
    import build_site as _BS
    list_pages = {f"list-{k}.html" for k, _l, _i, _d in _BS.LISTING_TYPES}
except ImportError:
    list_pages = set()
expected |= doc_pages | SPECIAL | md_pages | md_special | list_pages
actual = {f for f in os.listdir(WIKI) if f.endswith(".html")} if os.path.isdir(WIKI) else set()
if not actual:
    E("W1", "wiki/ 目录不存在或为空")
else:
    missing = expected - actual
    orphan = actual - expected
    if missing:
        E("W1", f"缺少 {len(missing)} 个词条页：{sorted(missing)[:10]}")
    if orphan:
        W("W5", f"存在 {len(orphan)} 个孤儿页：{sorted(orphan)[:10]}")
    ent_pages = {f"{slug(e['id'])}.html" for e in ENT["entities"]}
    if not missing and not orphan:
        I(f"W1/W5 词条页与实体一一对应：{len(ent_pages)} 实体页 + {len(doc_pages)} 文献页 "
          f"+ 1 文献索引 = {len(actual)} 页，无孤儿")
    I(f"W5b 仿真文献：{len(doc_pages)} 篇" + (
        "（" + " / ".join(
            f"{gl} {sum(len(getattr(m, a, [])) for m in _mods)}"
            for gl, a in (("文献", "DOCUMENTS"), ("日记", "DIARIES"),
                          ("书信", "LETTERS"), ("演讲", "SPEECHES"))) + "）"
        if KD else ""))

# W1b 顶层页面存在性
for _tp in sorted(TOP_PAGES):
    _p = os.path.join(DOCS, _tp)
    if not os.path.exists(_p):
        E("W1b", f"缺少顶层页面 docs/{_tp}")
    else:
        I(f"W1b 顶层页面 docs/{_tp} 存在（{os.path.getsize(_p)//1024} KB）")

# ------------------------------------------------------------------ 逐页校验
all_pages = []
for d, files in ((DOCS, [f for f in os.listdir(DOCS) if f.endswith(".html")]),
                 (WIKI, sorted(actual))):
    for f in files:
        all_pages.append(os.path.join(d, f))

dead = []
struct_bad = []
json_bad = []
back_bad = []
madeby_bad = []
for p in all_pages:
    try:
        s = open(p, encoding="utf-8").read()
    except Exception as ex:
        E("W2", f"{p} 读取失败：{ex}")
        continue
    # W2 结构（注意用 [ >] 界定，避免把 <header> 误认为 <head>）
    for tag in ("html", "head", "body"):
        if len(re.findall(rf"<{tag}[ >]", s)) != s.count(f"</{tag}>"):
            struct_bad.append((os.path.relpath(p, ROOT), tag))
    if not s.lstrip().startswith("<!DOCTYPE html>"):
        struct_bad.append((os.path.relpath(p, ROOT), "DOCTYPE"))
    # W3 内嵌 JSON
    for m in re.finditer(r"const (?:DATA|D|FILTERS)\s*=\s*(\[.*?\]|\{.*?\});\s*\n", s, re.S):
        try:
            json.loads(m.group(1))
        except Exception as ex:
            json_bad.append((os.path.relpath(p, ROOT), str(ex)[:60]))
    # W4 站内链接
    base = os.path.dirname(p)
    for m in re.finditer(r'(?:href|src)="([^"]+)"', s):
        tgt = m.group(1)
        if tgt.startswith(("#", "http", "mailto:", "javascript:", "data:")):
            continue
        # 跳过 JS 模板拼接（如 "'+r.href+'"），它们由运行时生成
        if "'" in tgt or "+" in tgt or "${" in tgt:
            continue
        tp = route_to_path(tgt, base)
        if tp and not os.path.exists(tp):
            dead.append((os.path.relpath(p, ROOT), tgt))

    # W10 子页面返回导航（主页除外）
    rel = os.path.relpath(p, DOCS).replace("\\", "/")
    is_home = rel == "home.html"
    has_home_link = 'class="bkn"' in s and "回到主页" in s
    has_prev = 'id="bkPrev"' in s and "返回上一页" in s
    if is_home:
        if has_home_link or has_prev:
            back_bad.append((rel, "主页不应显示返回按钮"))
    else:
        if not has_home_link:
            back_bad.append((rel, "缺少「回到主页」"))
        if not has_prev:
            back_bad.append((rel, "缺少「返回上一页」"))

    # W11 页脚署名
    if 'class="madeby"' not in s or "DeepSeek Harness" not in s:
        madeby_bad.append(rel)

if struct_bad:
    E("W2", f"HTML 结构异常 {len(struct_bad)} 处：{struct_bad[:8]}")
else:
    I(f"W2 全部 {len(all_pages)} 个页面的 HTML 结构完整")
if json_bad:
    E("W3", f"内嵌 JSON 解析失败 {len(json_bad)} 处：{json_bad[:5]}")
else:
    I(f"W3 内嵌 JSON 全部可解析")
if dead:
    E("W4", f"死链 {len(dead)} 处：{dead[:10]}")
else:
    I(f"W4 站内链接全部可达（{len(all_pages)} 页）")

# W4b 锚标签嵌套检查（实体名自动链接可能误伤已有标签）
nested = []
for p in all_pages:
    s = open(p, encoding="utf-8").read()
    depth = 0
    for m in re.finditer(r"<a\b|</a>", s):
        if m.group() == "</a>":
            depth -= 1
            if depth < 0:
                nested.append((os.path.relpath(p, ROOT), "多余的 </a>"))
                break
        else:
            depth += 1
            if depth > 1:
                nested.append((os.path.relpath(p, ROOT), "锚标签嵌套"))
                break
if nested:
    E("W4b", f"锚标签结构异常 {len(nested)} 处：{nested[:8]}")
else:
    I(f"W4b 锚标签结构正常（{len(all_pages)} 页，无嵌套、无多余闭合）")

# W10 子页面返回导航
if back_bad:
    E("W10", f"返回导航异常 {len(back_bad)} 处：{back_bad[:8]}")
else:
    I(f"W10 返回导航齐备：{len(all_pages)-1} 个子页面均有「回到主页」「返回上一页」，"
      f"主页 home.html 正确豁免")

# W11 页脚署名
if madeby_bad:
    E("W11", f"{len(madeby_bad)} 个页面缺少页脚署名：{madeby_bad[:8]}")
else:
    I(f"W11 页脚署名齐备：全部 {len(all_pages)} 页均含「本页面由 DeepSeek Harness 创作」")

# ------------------------------------------------------------------ W6 索引页
idx_p = os.path.join(DOCS, "index.html")
if os.path.exists(idx_p):
    s = open(idx_p, encoding="utf-8").read()
    if "S5" not in s:
        E("W6", "索引页未包含 S5 标记")
    elif "整合层" not in s:
        E("W6", "索引页未包含 S5 整合层说明")
    else:
        n = s.count('class="tag s5"')
        I(f"W6 索引页含 S5 标记，共 {n} 处；S5 整合记录 "
          f"{s.count('被合并的原条目')} 条")
else:
    E("W6", "docs/index.html 不存在")

# ------------------------------------------------------------------ W7 时间轴
tl_p = os.path.join(DOCS, "timeline.html")
if os.path.exists(tl_p):
    s = open(tl_p, encoding="utf-8").read()
    m = re.search(r"const D = (\{.*?\});\s*\n", s, re.S)
    if not m:
        E("W7", "时间轴页未找到内嵌数据")
    else:
        try:
            d = json.loads(m.group(1))
            ev_n = len(d["events"])
            exp = len(TBL["timeline"]["rows"])
            if ev_n != exp:
                E("W7", f"时间轴事件数 {ev_n} != 事件表 {exp}")
            else:
                I(f"W7 时间轴：{ev_n} 个事件节点，{len(d['causal'])} 条因果边，"
                  f"范围 {d['min']}—{d['max']}")
            if not d["causal"]:
                W("W7", "时间轴无因果边数据")
            # W8 关键修正：事件链接必须带 wiki/ 前缀（本页在 docs/，词条在 docs/wiki/）
            bad_href = [e["id"] for e in d["events"]
                        if not e.get("href", "").startswith("wiki/")]
            if bad_href:
                E("W8", f"时间轴有 {len(bad_href)} 个事件链接缺少 wiki/ 前缀，"
                        f"点击会「找不到文件」：{bad_href[:8]}")
            else:
                I(f"W8 时间轴全部 {len(d['events'])} 个「打开完整词条」链接均带 wiki/ 前缀，"
                  f"指向 docs/wiki/ 下真实存在的页面")
                # 逐条确认目标文件存在
                miss = [e["id"] for e in d["events"]
                        if not os.path.exists(os.path.join(DOCS, e["href"]))]
                if miss:
                    E("W8", f"时间轴链接指向不存在的文件：{miss[:8]}")
                else:
                    I("W8 逐条核对：所有词条目标文件均存在")
            # W9 纵轴视角
            if "RULES" not in s or "classify" not in s:
                E("W9", "时间轴缺少纵轴分类逻辑（region/religion/culture/polity/conflict）")
            else:
                modes = re.findall(r"value=\"(region|religion|culture|polity|conflict|epoch)\"", s)
                I(f"W9 时间轴纵轴视角：{len(modes)} 个 → {modes}")
        except Exception as ex:
            E("W7", f"时间轴数据解析失败：{ex}")
else:
    E("W7", "docs/timeline.html 不存在")

# ------------------------------------------------------------------ 输出
print("=" * 72)
print("HTML 站点校验报告")
print("=" * 72)
for m in infos:
    print(f"  [通过] {m}")
print()
if warns:
    print(f"--- 警告 {len(warns)} 条 ---")
    for c, m in warns:
        print(f"  [{c}] {m}")
    print()
if errors:
    print(f"--- 错误 {len(errors)} 条 ---")
    for c, m in errors:
        print(f"  [{c}] {m}")
    print()
print("=" * 72)
print(f"结论：错误 {len(errors)}，警告 {len(warns)}，通过项 {len(infos)}")
print("=" * 72)
sys.exit(1 if errors else 0)
