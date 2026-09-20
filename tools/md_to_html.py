# -*- coding: utf-8 -*-
r"""
Markdown → HTML 渲染器
========================
把 tools/build.py 生成的 Markdown 文档转成统一样式的 HTML 页面。

支持范围（覆盖本项目生成的全部 md 结构）：
  # / ## / ### / #### 标题
  | a | b | 表格（含 \| 转义、<br> 保留）
  - / 1. 列表（含缩进）
  - **粗体**、`代码`、[文本](链接)
  > 引用
  --- 分隔线
  空行分段
"""
import html
import os
import re

BT = chr(96)


def _inline(s):
    """行内标记 → HTML。先转义，再处理标记。"""
    out = html.escape(s, quote=False)
    # 代码
    out = re.sub(BT + r"([^" + BT + r"]+)" + BT,
                 lambda m: f'<code>{m.group(1)}</code>', out)
    # 粗体
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    # 斜体（避免误伤 ** ）
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", out)
    # 链接：仅允许相对路径与 http(s)
    def _link(m):
        txt, href = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return f'<a href="{href}">{txt}</a>'
        # 相对链接：/ 路径保持
        return f'<a href="{href}">{txt}</a>'
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _link, out)
    return out


def _split_row(line):
    """拆分表格行，尊重 \\| 转义。"""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    parts, cur, i = [], "", 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if c == "|":
            parts.append(cur)
            cur = ""
            i += 1
            continue
        cur += c
        i += 1
    parts.append(cur)
    return [p.strip() for p in parts]


def _is_sep(line):
    return bool(re.match(r"^\|?[\s:|-]+\|[\s:|-]*$", line)) and "-" in line


def convert(md):
    """Markdown 文本 → HTML 片段。"""
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    n = len(lines)
    in_ul = in_ol = False
    in_quote = False

    def close_lists():
        nonlocal in_ul, in_ol, in_quote
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False
        if in_quote:
            out.append("</blockquote>")
            in_quote = False

    while i < n:
        line = lines[i]
        s = line.strip()

        # 空行
        if not s:
            close_lists()
            i += 1
            continue

        # 表格
        if s.startswith("|"):
            if i + 1 < n and _is_sep(lines[i + 1].strip()):
                close_lists()
                head = _split_row(s)
                i += 2
                rows = []
                while i < n and lines[i].strip().startswith("|"):
                    rows.append(_split_row(lines[i].strip()))
                    i += 1
                out.append('<div class="tw"><table>')
                out.append("<thead><tr>" +
                           "".join(f"<th>{_inline(c)}</th>" for c in head) + "</tr></thead><tbody>")
                for r in rows:
                    cells = "".join(f"<td>{_inline(c)}</td>" for c in r)
                    out.append(f"<tr>{cells}</tr>")
                out.append("</tbody></table></div>")
                continue

        # 分隔线
        if re.match(r"^-{3,}$", s):
            close_lists()
            out.append('<hr class="mdhr">')
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            close_lists()
            lvl = min(len(m.group(1)), 4)
            txt = _inline(m.group(2))
            anchor = re.sub(r"[^\w\u4e00-\u9fff]+", "-", m.group(2))[:40].strip("-")
            out.append(f'<h{lvl} id="{html.escape(anchor)}">{txt}</h{lvl}>')
            i += 1
            continue

        # 引用
        if s.startswith(">"):
            if not in_quote:
                close_lists()
                out.append('<blockquote class="mdq">')
                in_quote = True
            out.append(f"<p>{_inline(s.lstrip('>').strip())}</p>")
            i += 1
            continue
        else:
            if in_quote:
                out.append("</blockquote>")
                in_quote = False

        # 有序列表
        m = re.match(r"^(\d+)\.\s+(.*)$", s)
        if m:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{_inline(m.group(2))}</li>")
            i += 1
            continue
        else:
            if in_ol:
                out.append("</ol>")
                in_ol = False

        # 无序列表
        if re.match(r"^[-*]\s+", s):
            if not in_ul:
                out.append('<ul class="mdul">')
                in_ul = True
            out.append(f"<li>{_inline(re.sub(r'^[-*]\\s+', '', s))}</li>")
            i += 1
            continue
        else:
            if in_ul:
                out.append("</ul>")
                in_ul = False

        # 缩进列表项（形如 "  - xxx"）
        if re.match(r"^\s+[-*]\s+", line) and in_ul:
            out.append(f"<li>{_inline(s.lstrip('-* ').strip())}</li>")
            i += 1
            continue

        # 普通段落
        out.append(f"<p>{_inline(s)}</p>")
        i += 1

    close_lists()
    return "\n".join(out)


# ---------------------------------------------------------------- 文档清单
# id -> (md 文件名, HTML 文件名, 标题, 图标, 说明, 分组)
MD_PAGES = [
    ("tables", "table_timeline.md", "table-timeline.html", "时间线表", "📅",
     "年份 · 事件 · 国家 · 结果（53 个事件节点，含地图工程纵轴映射）", "tables"),
    ("tables", "table_countries.md", "table-countries.html", "国家表", "🏛",
     "国名 · 政体 · 宗教 · 首都 · 领土（46 个国家与政治实体）", "tables"),
    ("tables", "table_people.md", "table-people.html", "人物表", "🧑",
     "姓名 · 王朝 · 生卒 · 职位 · 事迹（41 条）", "tables"),
    ("tables", "table_wars.md", "table-wars.html", "战争表", "⚔",
     "时间 · 双方 · 结果 · 条约（11 场武装冲突）", "tables"),
    ("refs", "glossary_zh_en_de.md", "glossary.html", "专有名词中英德对照表", "🔤",
     "107 条，按 8 个类别分组", "refs"),
    ("refs", "transliteration.md", "transliteration.html", "地名转写表", "📍",
     "113 条地名，中／德／英／法／意／荷／俄／奥克等多语形式", "refs"),
    ("refs", "index.md", "index-text.html", "设定集索引（文本版）", "🗂",
     "文档骨架 → 章节 → 实体 → 主题检索表", "refs"),
    ("analysis", "consistency_report.md", "consistency.html", "一致性检查报告", "✅",
     "日期／地理／宗教／数量／时间线自洽／命名，共 74 条发现", "analysis"),
    ("analysis", "pending_decisions.md", "pending.html", "待定项决策报告", "🗳",
     "34 条待定项，按 P0–P3 分级，逐条给出方案、利弊与推荐", "analysis"),
    ("analysis", "pending_checklist.md", "checklist.html", "待定项裁定清单", "☑",
     "勾选式清单；裁定结果已全部写回正典", "analysis"),
    ("analysis", "status_confirmed_pending_revisions.md", "status.html", "三态清单", "📌",
     "已确定 36 ／ 待定 34 ／ 修正 15", "analysis"),
    ("analysis", "graph_relations.md", "graph.html", "关系网总览", "🕸",
     "1025 条边全表 + 五张 ASCII 谱系图", "analysis"),
]

GROUP_LABEL = {
    "tables": ("四张表", "设定集的结构化输出"),
    "refs": ("对照表与索引", "专有名词、地名转写与检索入口"),
    "analysis": ("一致性与决策", "检查报告、待定项方案与关系网"),
}


def build_md_pages(docs_dir, wiki_dir, html_common):
    """把 MD_PAGES 里的 md 转成 HTML，返回生成清单。"""
    H = html_common
    made = []
    for gid, md_name, out_name, title, ico, desc, grp in MD_PAGES:
        src = os.path.join(docs_dir, md_name)
        if not os.path.exists(src):
            continue
        with open(src, encoding="utf-8") as f:
            md = f.read()
        body_html = convert(md)

        # 同组导航
        sib = [(t, o, i) for g, m, o, t, i, d, gg in MD_PAGES if gg == grp and o != out_name]
        chips = "".join(f'<a class="chip" href="{o}">{i} {H.esc(t)}</a>' for t, o, i in sib)

        # 页面内目录（h2 锚点）
        toc = []
        for m in re.finditer(r"^##\s+(.+)$", md, re.M):
            t = m.group(1).strip()
            a = re.sub(r"[^\w\u4e00-\u9fff]+", "-", t)[:40].strip("-")
            toc.append(f'<a class="pill" href="#{html.escape(a)}">{H.esc(t[:34])}</a>')
        toc_html = ('<div class="card"><div class="legend">本页目录</div>'
                    '<div class="pill-row">' + "".join(toc[:40]) + '</div></div>') if toc else ""

        parts = [f"""
<header><div class="hdr">
<h1>{ico} {H.esc(title)}<span class="sub">{H.esc(desc)}</span></h1>
<nav class="crumbs"><a href="../home.html">主页</a> ／ <a href="../index.html">索引</a> ／
<a href="index.html">文档</a> ／ {H.esc(GROUP_LABEL[grp][0])}</nav></div></header>
<main>
<div class="card">
<span class="kindbadge">{H.esc(GROUP_LABEL[grp][0])}</span>
本页由 <code>docs/{H.esc(md_name)}</code> 自动转换生成，
数据源为 <code>tools/kb_data.py</code> 等设定数据层；源 Markdown 保留在 <code>docs/</code> 下。
{'<div class="pill-row" style="margin-top:10px">' + chips + '</div>' if chips else ''}
</div>
{toc_html}
<div class="mdbody">
{body_html}
</div>
</main>
"""]
        page = H.page(f"{title} · 泛德意志的欧洲", "".join(parts), base="../", active=("tables" if grp == "tables" else "docs"))
        with open(os.path.join(wiki_dir, out_name), "w", encoding="utf-8", newline="\n") as f:
            f.write(page)
        made.append((gid, out_name, title, ico, desc, grp))
    return made


def build_md_index(docs_dir, wiki_dir, made, html_common):
    """文档总索引页 docs/wiki/docs-index.html"""
    H = html_common
    parts = ["""
<header><div class="hdr">
<h1>📄 文档中心<span class="sub">设定集的结构化输出：四张表、对照表、检查报告与决策记录</span></h1>
<nav class="crumbs"><a href="../home.html">主页</a> ／ <a href="../index.html">索引</a> ／
<a href="../timeline.html">时间轴</a></nav></div></header><main>
<div class="card"><div class="legend">
本页汇集由 <code>tools/build.py</code> 与 <code>tools/build_pending.py</code> 生成的 Markdown 文档，
已全部转为 HTML 并接入站点导航。源 Markdown 仍保留在 <code>docs/</code> 下，可直接编辑或外发。
</div></div>
"""]
    for grp, (glabel, gdesc) in GROUP_LABEL.items():
        items = [x for x in made if x[5] == grp]
        if not items:
            continue
        parts.append(f'<h2>{H.esc(glabel)}</h2><div class="legend">{H.esc(gdesc)}</div>'
                     '<div class="entries">')
        for gid, out_name, title, ico, desc, g in items:
            parts.append(f'<a class="entry" href="{out_name}"><span class="ico">{ico}</span>'
                         f'<h3>{H.esc(title)}</h3><p>{H.esc(desc)}</p></a>')
        parts.append('</div>')
    parts.append('</main>')
    page = H.page("文档中心 · 泛德意志的欧洲", "".join(parts), base="../")
    with open(os.path.join(wiki_dir, "docs-index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    return "docs-index.html"
