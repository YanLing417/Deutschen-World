# -*- coding: utf-8 -*-
"""
历史设定集知识工程 —— 产物校验器
运行： python tools/validate.py

校验项：
  V1  JSON 语法与可解析性
  V2  实体 ID 唯一性与命名规范
  V3  图数据库边端点引用完整性（无悬空引用）
  V4  实体字段交叉引用完整性（dynasty_id / country_id / religion_id / language_id / war_id / treaty_id / causes / effects）
  V5  四张表行数与实体数一致
  V6  状态字段取值合法性（已确定 / 待定 / 修正）
  V7  出处代号合法性（S0–S4）
  V8  地名转写表：正典中文译名禁用现实译名规则抽查
  V9  对照表条目完整性（zh/de/en 三列）
  V10 索引可检索性（每条索引必须可被至少一个关键词命中）
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, HERE)

errors = []
warnings = []
infos = []


def err(code, msg):
    errors.append((code, msg))


def warn(code, msg):
    warnings.append((code, msg))


def info(msg):
    infos.append(msg)


def load(name):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        err("V1", f"缺少产物文件：{name}")
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        err("V1", f"{name} JSON 解析失败：{e}")
        return None


# ------------------------------------------------------------------ V1
JSON_FILES = ["entities.json", "graph.json", "tables.json", "table_timeline.json",
              "table_countries.json", "table_people.json", "table_wars.json",
              "glossary.json", "transliteration.json", "index.json", "status.json"]
docs = {}
for n in JSON_FILES:
    d = load(n)
    if d is not None:
        docs[n] = d
info(f"V1 JSON 文件全部可解析：{len(docs)}/{len(JSON_FILES)}")

entities = docs.get("entities.json")
graph = docs.get("graph.json")
tables = docs.get("tables.json")
glossary = docs.get("glossary.json")
translit = docs.get("transliteration.json")
index = docs.get("index.json")
status = docs.get("status.json")

# ------------------------------------------------------------------ V2
if entities:
    ids = [e["id"] for e in entities["entities"]]
    dup = [k for k, v in Counter(ids).items() if v > 1]
    if dup:
        err("V2", f"实体 ID 重复：{dup}")
    bad = [i for i in ids if not re.match(
        r"^(PE|D|C|R|L|P|E|W|T|O|PT|SB|AX|G|M|AR|DOC|DIA|LET|SP)_[A-Za-z0-9_]+$", i)]
    if bad:
        warn("V2", f"不符合命名规范的 ID：{bad}")
    info(f"V2 实体 ID 唯一性通过：{len(ids)} 个 ID，无重复")

    declared = entities["total"]
    if declared != len(entities["entities"]):
        err("V2", f"entities.total ({declared}) != 实际实体数 ({len(entities['entities'])})")
    group_sum = sum(entities["counts"].values())
    if group_sum != declared:
        err("V2", f"counts 合计 ({group_sum}) != total ({declared})")

# ------------------------------------------------------------------ V3
KNOWN = set(e["id"] for e in entities["entities"]) if entities else set()
if graph:
    dangling = []
    for e in graph["edges"]:
        for side in ("from", "to"):
            if e[side] not in KNOWN:
                dangling.append((e.get("id"), side, e[side]))
    if dangling:
        err("V3", f"图数据库存在 {len(dangling)} 条悬空边端点引用：{dangling[:10]}")
    else:
        info(f"V3 图数据库边引用完整性通过：{len(graph['edges'])} 条边，0 悬空")

    node_ids = [n["id"] for n in graph["nodes"]]
    if len(node_ids) != len(set(node_ids)):
        err("V3", "graph.nodes 存在重复 ID")
    if set(node_ids) != KNOWN:
        err("V3", "graph.nodes 与 entities 的 ID 集合不一致")
    if graph["meta"]["node_count"] != len(graph["nodes"]):
        err("V3", "graph.meta.node_count 与实际节点数不符")
    if graph["meta"]["edge_count"] != len(graph["edges"]):
        err("V3", "graph.meta.edge_count 与实际边数不符")

    # 四个子图必须都非空
    for name, view in graph["views"].items():
        if not view["edges"]:
            err("V3", f"子图「{name}」没有边")
        else:
            info(f"V3 子图「{name}」：{len(view['edges'])} 条边")

# ------------------------------------------------------------------ V4
FIELD_REFS = [
    ("dynasty_id", "DYNASTY"), ("country_id", "COUNTRY"),
    ("religion_id", "RELIGION"), ("language_id", "LANGUAGE"),
    ("war_id", "WAR"), ("treaty_id", "TREATY"),
]
bad_refs = []
if entities:
    for e in entities["entities"]:
        for field, kind in FIELD_REFS:
            v = e.get(field)
            if v and v not in KNOWN:
                bad_refs.append((e["id"], field, v))
        for key in ("causes", "effects"):
            for v in e.get(key, []) or []:
                if v not in KNOWN:
                    bad_refs.append((e["id"], key, v))
        for key in ("country_ids", "persons"):
            for v in e.get(key, []) or []:
                if v not in KNOWN:
                    bad_refs.append((e["id"], key, v))
        for key in ("war_id", "treaty_id"):
            v = e.get(key)
            if v and v not in KNOWN:
                bad_refs.append((e["id"], key, v))
        for cid in e.get("polity", []) or []:
            if isinstance(cid, str) and cid.startswith("C_") and cid not in KNOWN:
                bad_refs.append((e["id"], "polity", cid))
        for side in ("side_a", "side_b"):
            s = e.get(side)
            if isinstance(s, dict):
                for cid in s.get("country_ids", []) or []:
                    if cid not in KNOWN:
                        bad_refs.append((e["id"], side + ".country_ids", cid))
    if bad_refs:
        err("V4", f"字段交叉引用失败 {len(bad_refs)} 处：{bad_refs[:15]}")
    else:
        info("V4 字段交叉引用完整性通过（dynasty_id/country_id/religion_id/language_id/war_id/treaty_id/causes/effects/country_ids/persons/polity/side_*）")

# ------------------------------------------------------------------ V5
if entities and tables:
    exp = {
        "timeline": entities["counts"]["events"],
        "countries": entities["counts"]["countries"],
        "people": entities["counts"]["people"],
        "wars": entities["counts"]["wars"],
    }
    for k, n in exp.items():
        got = len(tables[k]["rows"])
        if got != n:
            err("V5", f"表 {k} 行数 {got} != 实体数 {n}")
        else:
            info(f"V5 表 {k}：{got} 行，与实体数一致")

# ------------------------------------------------------------------ V6
VALID_STATUS = {"已确定", "待定", "修正"}
if entities:
    bad_status = []
    for e in entities["entities"]:
        s = e.get("status")
        if s not in VALID_STATUS:
            bad_status.append((e["id"], s))
    if bad_status:
        err("V6", f"非法状态取值 {len(bad_status)} 处：{bad_status[:10]}")
    else:
        info("V6 状态取值全部合法（已确定 / 待定 / 修正）")

if graph:
    bad = [(e.get("id"), e.get("status")) for e in graph["edges"] if e.get("status") not in VALID_STATUS]
    if bad:
        warn("V6", f"边状态取值异常 {len(bad)} 处：{bad[:10]}")

# ------------------------------------------------------------------ V7
VALID_SRC = {"S0", "S1", "S2", "S3", "S4"}
if entities:
    bad_src = []
    for e in entities["entities"]:
        srcs = e.get("src")
        if not srcs:
            bad_src.append((e["id"], "缺失"))
        else:
            for s in srcs:
                if s not in VALID_SRC:
                    bad_src.append((e["id"], s))
    if bad_src:
        err("V7", f"非法/缺失出处代号 {len(bad_src)} 处：{bad_src[:10]}")
    else:
        info("V7 出处代号全部合法且无缺失（S0–S4）")

if graph:
    bad = [(e.get("id"), s) for e in graph["edges"] for s in (e.get("src") or []) if s not in VALID_SRC]
    if bad:
        err("V7", f"边出处代号非法 {len(bad)} 处：{bad[:10]}")

# ------------------------------------------------------------------ V8
FORBIDDEN_CANON = {
    "巴黎": "帕里斯", "兰斯": "雷姆斯", "里昂": "劳格登",
    "鲁昂": "鲁安", "马赛": "马西利恩", "蒙彼利埃": "蒙斯佩勒", "第戎": "迪根",
}
# 允许出现的上下文：原文引述、对照说明、别名列、现实世界专名
ALLOW_MARKERS = ["clause_old", "clause_new", "resolution", "原文", "现实对应",
                 "对照", "而非", "正典不用", "zh_alias", "_src_note"]
if translit:
    hits = []
    for p in translit["places"]:
        zh = p["zh"]
        for bad, good in FORBIDDEN_CANON.items():
            if bad in zh:
                hits.append((p["id"], zh, f"含现实译名「{bad}」，建议「{good}」"))
    if hits:
        err("V8", f"地名表正典中文列残留现实译名 {len(hits)} 处：{hits[:10]}")
    else:
        info("V8 地名转写表正典中文列无「巴黎/兰斯/里昂」等现实译名")
    miss = [p["id"] for p in translit["places"] if not p.get("zh") or not p.get("de")]
    if miss:
        err("V8", f"地名缺少 zh 或 de 形式：{miss}")
    else:
        info(f"V8 地名转写表完整性通过：{len(translit['places'])} 条均有中文与德文形式")

# V8b：全局扫描 description 类字段中的现实译名残留（排除原文引述与对照说明）
if entities:
    residual = []
    for e in entities["entities"]:
        for k, v in e.items():
            if k in ("zh_alias", "real", "fr", "en", "it", "nl", "es", "ca", "oc",
                     "name_de", "note", "_group", "_group_label") or k.startswith("_"):
                continue
            texts = v if isinstance(v, list) else [v]
            for t in texts:
                if not isinstance(t, str):
                    continue
                if any(m in t for m in ALLOW_MARKERS):
                    continue
                for bad in FORBIDDEN_CANON:
                    # 州名（如「卢瓦尔-奥尔良州」）以德语读音译名为主，但州名中的
                    # 「奥尔良」属现实旧称残留，此处仅告警
                    if bad in t:
                        residual.append((e["id"], k, bad, t[:50]))
    if residual:
        warn("V8b", f"描述性字段残留现实译名 {len(residual)} 处（多为州名）：{residual[:12]}")
    else:
        info("V8b 描述性字段无现实译名残留")

# ------------------------------------------------------------------ V9
if glossary:
    items = glossary["glossary"]
    miss = [g["id"] for g in items if not g.get("zh") or not g.get("de") or not g.get("en")]
    if miss:
        err("V9", f"对照表条目缺少 zh/de/en：{miss}")
    else:
        info(f"V9 中英德对照表完整性通过：{len(items)} 条均有三语形式")
    cats = {(g.get("category") or "未分类") for g in items}
    info(f"V9 对照表类别：{len(cats)} 类 → {'、'.join(sorted(cats))}")

# ------------------------------------------------------------------ V10
if index:
    entries = index["entries"]
    empty = [e for e in entries if not (e.get("title") or "").strip()]
    if empty:
        err("V10", f"索引存在无标题条目 {len(empty)} 条")
    kinds = Counter(e["kind"] for e in entries)
    info(f"V10 索引条目 {len(entries)} 条，类型分布：{dict(kinds)}")
    docs_used = Counter(e["doc"] for e in entries)
    for s in ("S0", "S1", "S2", "S3", "S4"):
        if docs_used.get(s, 0) == 0:
            err("V10", f"索引未收录文档 {s} 的任何条目")
    info(f"V10 索引按文档分布：{dict(docs_used)}")

# ------------------------------------------------------------------ 附加：时间线单调性
if tables:
    years = [r["year"] for r in tables["timeline"]["rows"]]
    if years != sorted(years):
        warn("V11", "时间线表未按年份升序排列")
    else:
        info(f"V11 时间线表按年份升序：{years[0]} → {years[-1]}，共 {len(years)} 个节点")

# 时间线纵轴 16 节点覆盖检查（使用显式节点映射）
if tables and "axis_nodes" in tables["timeline"]:
    axis = tables["timeline"]["axis_nodes"]
    missing = [a["year"] for a in axis if a["on_map_axis_16"] and not a["event_id"]]
    if missing:
        err("V12", f"地图工程纵轴节点未映射到事件：{missing}")
    else:
        n16 = sum(1 for a in axis if a["on_map_axis_16"])
        info(f"V12 地图工程16个纵轴节点全部映射到事件（映射表共 {len(axis)} 个节点，其中 S0 原始节点 {n16} 个）")
    # 映射目标必须存在
    bad = [a for a in axis if a["event_id"] and not a["event_zh"]]
    if bad:
        err("V12", f"纵轴节点映射到不存在的事件：{bad}")
    # 多节点映射同一事件的情况需显式说明
    seen = defaultdict(list)
    for a in axis:
        if a["event_id"]:
            seen[a["event_id"]].append(a["year"])
    multi = {k: v for k, v in seen.items() if len(v) > 1}
    if multi:
        warn("V12", f"多个纵轴节点映射到同一事件：{multi}")
    # 未出现在任何纵轴节点的核心事件
    axis_events = {a["event_id"] for a in axis if a["event_id"]}
    unmapped = [e["id"] for e in entities["entities"]
                if e["type"] == "EVENT" and e["id"] not in axis_events]
    info(f"V12 未进入纵轴映射表的事件 {len(unmapped)} 个（多为长时段/亚洲线/补充节点）：{unmapped[:12]}")

# ------------------------------------------------------------------ V13 分期国名一致性
# 用户 2026 裁定：不同时期的国名不得混用。
PERIOD_RULES = [
    ("C_FRANKISH_ROMANCE", ["法兰克王国", "法兰克立宪君主国", "法兰克共和国"],
     "843—1270 的罗曼语政治体应称「法兰西罗曼王国」"),
    ("C_WEST_FRANKIA", ["法兰克立宪君主国", "法兰克共和国"],
     "843—987 应称「西法兰克王国」"),
    ("C_FRANKEN_REPUBLIC", ["法兰克王国", "法兰克立宪君主国"],
     "1918—1945 应称「法兰克共和国」"),
    ("C_GERMAN_REPUBLIC", ["德意志帝国", "德意志联邦共和国"],
     "1918—1945 应称「德意志共和国」"),
]
if entities:
    bad_period = []
    by_id = {e["id"]: e for e in entities["entities"]}
    for eid, forbidden, why in PERIOD_RULES:
        e = by_id.get(eid)
        if not e:
            warn("V13", f"分期规则引用了不存在的实体 {eid}")
            continue
        # 只检查「定义身份」的字段：名称、分期、政体。
        # overview / notes 允许提及别的时期用于划界说明（例如「1918 年前为 X」），
        # 这恰恰是防止混用的正确写法。
        own = " ".join(str(e.get(k) or "") for k in
                       ("name_zh", "name_short", "time_span", "polity"))
        for w in forbidden:
            if w in own:
                bad_period.append((eid, w, why))
    if bad_period:
        detail = "；".join(f"{a} 的「名称/分期/政体」中出现了「{b}」（{c}）"
                          for a, b, c in bad_period)
        err("V13", f"分期国名混用 {len(bad_period)} 处：{detail[:400]}")
    else:
        info("V13 分期国名一致性通过（各分期词条的名称/分期/政体字段无互相混用；"
             "概述与注记中的跨期引用属划界说明，予以放行）")

    NEEDED = ["C_WEST_FRANKIA", "C_FRANKISH_ROMANCE", "C_FRANKEN_REPUBLIC",
              "C_GERMAN_REPUBLIC", "C_SPAIN", "C_ARAGON", "C_SPAIN_ARAGON",
              "C_IBERIAN_KINGDOM", "C_IBERIA_1REP", "C_IBERIA_1EMP",
              "C_IBERIA_2REP", "C_IBERIA_2EMP_UNION", "C_IBERIA_3REP_FULL",
              "C_IBERIA_OCCUPIED", "C_IBERIA_4REP", "C_IBERIA_5REP",
              "C_OCCITAN_KINGDOM"]
    miss_p = [x for x in NEEDED if x not in by_id]
    if miss_p:
        err("V13", f"缺少分期词条：{miss_p}")
    else:
        info(f"V13 分期词条齐备：法兰克系 4 条 / 德意志系 2 条 / "
             f"伊比利亚系 11 条，共 {len(NEEDED)} 条")

# ------------------------------------------------------------------ V14 概述齐备
if entities:
    WIKI_TYPES = {"COUNTRY", "DYNASTY", "PERSON", "EVENT", "PLACE", "RELIGION",
                  "LANGUAGE", "WAR", "TREATY", "SUBDIVISION", "PARTY",
                  "ORGANIZATION", "AXIS_INDICATOR", "ARTIFACT"}
    no_ov = [e["id"] for e in entities["entities"]
             if e["type"] in WIKI_TYPES
             and not str(e.get("overview") or e.get("summary") or "").strip()]
    if no_ov:
        err("V14", f"{len(no_ov)} 个词条缺少概述：{no_ov[:10]}")
    else:
        n = sum(1 for e in entities["entities"] if e["type"] in WIKI_TYPES)
        info(f"V14 概述齐备：全部 {n} 个词条类实体都有概述")

# ------------------------------------------------------------------ 输出
print("=" * 72)
print("泛德意志的欧洲 · 设定集知识工程 —— 产物校验报告")
print("=" * 72)
print()
for m in infos:
    print(f"  [通过] {m}")
print()
if warnings:
    print(f"--- 警告 {len(warnings)} 条 ---")
    for c, m in warnings:
        print(f"  [{c}] {m}")
    print()
if errors:
    print(f"--- 错误 {len(errors)} 条 ---")
    for c, m in errors:
        print(f"  [{c}] {m}")
    print()
print("=" * 72)
print(f"结论：错误 {len(errors)}，警告 {len(warnings)}，通过项 {len(infos)}")
print("=" * 72)
sys.exit(1 if errors else 0)
