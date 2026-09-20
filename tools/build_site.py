# -*- coding: utf-8 -*-
"""
HTML 站点生成器
================
运行： python tools/build_site.py

产出：
  docs/index.html        设定集索引（S0–S4 重复条目整合为 S5，单条保留）
  docs/wiki/*.html       维基式百科词条（每个国家/王朝/人物/事件/…各一页）
  docs/timeline.html     交互式时间轴（HTML + JavaScript）
"""
import json
import os
import re
import sys
from collections import defaultdict, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
WIKI = os.path.join(DOCS, "wiki")
sys.path.insert(0, HERE)

import html_common as H  # noqa: E402
import md_to_html as MD  # noqa: E402
import listing_types as _LT  # noqa: E402
import kb_data as D  # noqa: E402
try:
    import kb_decisions as DEC
except ImportError:
    DEC = None

os.makedirs(DOCS, exist_ok=True)
os.makedirs(WIKI, exist_ok=True)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


ENT = load("entities.json")
GRAPH = load("graph.json")
IDX = load("index.json")
TBL = load("tables.json")
PEND = load("pending_decisions.json")
CONS = load("consistency.json")

ENTITIES = {x["id"]: x for x in ENT["entities"]}
NODES = {n["id"]: n for n in GRAPH["nodes"]}
EDGES = GRAPH["edges"]

TYPE_LABEL = {
    "COUNTRY": "国家与政治实体", "DYNASTY": "王朝与家族", "PERSON": "人物",
    "EVENT": "事件", "PLACE": "地点", "RELIGION": "宗教", "LANGUAGE": "语言",
    "WAR": "战争", "TREATY": "条约与宪章", "SUBDIVISION": "行政区划",
    "PARTY": "政党", "ORGANIZATION": "机构与组织", "AXIS_INDICATOR": "横轴指标",
    "ARTIFACT": "历史物品留存",
}
TYPE_GROUP = {
    "COUNTRY": "countries", "DYNASTY": "dynasties", "PERSON": "people",
    "EVENT": "events", "PLACE": "places", "RELIGION": "religions",
    "LANGUAGE": "languages", "WAR": "wars", "TREATY": "treaties",
    "SUBDIVISION": "subdivisions", "PARTY": "parties",
    "ORGANIZATION": "organizations", "AXIS_INDICATOR": "axis_indicators",
    "ARTIFACT": "artifacts",
}
GROUP_LABEL = {
    "countries": "国家与政治实体", "dynasties": "王朝与家族", "people": "人物",
    "events": "事件", "places": "地点", "religions": "宗教", "languages": "语言",
    "wars": "战争", "treaties": "条约与宪章", "subdivisions": "行政区划",
    "parties": "政党", "organizations": "机构与组织", "axis_indicators": "横轴指标",
    "artifacts": "历史物品留存",
}
GROUP_ORDER = list(GROUP_LABEL.keys())


def slug(eid):
    return eid.lower().replace("_", "-")


def disp_name(ent):
    """实体的显示名：大部分用 name_zh，地点与横轴指标用各自字段。"""
    return (ent.get("name_zh") or ent.get("zh") or ent.get("name")
            or ent.get("name_de") or ent.get("id") or "—")


def wiki_href(eid):
    """词条链接：页面都在 docs/wiki/ 内，故一律用裸文件名（同目录相对链接）。"""
    return f"{slug(eid)}.html"


def link(eid, text=None):
    if eid not in NODES:
        return H.esc(text or eid)
    t = text or disp_name(NODES[eid])
    return f'<a href="{wiki_href(eid)}">{H.esc(t)}</a>'


def status_tag(st, src=None):
    return H.status_tags(st, src)


# ==================================================================
# 关系索引
# ==================================================================
OUT = defaultdict(list)
IN = defaultdict(list)
for ed in EDGES:
    OUT[ed["from"]].append(ed)
    IN[ed["to"]].append(ed)


def rel_rows(eid, limit=None):
    rows = []
    for ed in OUT.get(eid, []):
        f = NODES.get(ed["from"], {}).get("name_zh", ed["from"])
        t = NODES.get(ed["to"], {}).get("name_zh", ed["to"])
        rows.append((ed["kind"], "→", f, ed["to"], t, ed.get("label") or "", ed.get("time") or "", ed.get("status") or ""))
    for ed in IN.get(eid, []):
        f = NODES.get(ed["from"], {}).get("name_zh", ed["from"])
        t = NODES.get(ed["to"], {}).get("name_zh", ed["to"])
        rows.append((ed["kind"], "←", f, ed["from"], t, ed.get("label") or "", ed.get("time") or "", ed.get("status") or ""))
    return rows[:limit] if limit else rows


# ==================================================================
# 1. 索引（S0–S4 → S5 去重合并）
# ==================================================================
def build_index():
    entries = IDX["entries"]

    # --- 1a. 实体索引：按 ref_id 合并，整合为 S5 ---
    ent_entries = [x for x in entries if x["kind"] not in ("章节", "CONFIRMED", "PENDING")
                   and x["ref_id"]]
    merged = OrderedDict()
    for x in ent_entries:
        k = x["ref_id"]
        if k not in merged:
            merged[k] = {
                "ref_id": k, "kind": x["kind"], "title": x["title"],
                "summary": x.get("summary") or "", "sections": [], "docs": [],
            }
        m = merged[k]
        m["docs"].append(x["doc"])
        m["sections"].append((x["doc"], x["section"], x.get("subsection")))
        if x.get("summary") and len(x["summary"]) > len(m["summary"]):
            m["summary"] = x["summary"]
        if x["kind"] not in m["kind"]:
            m["kind"] = x["kind"]

    for m in merged.values():
        docs = list(dict.fromkeys(m["docs"]))
        m["merged_from"] = docs
        # 用户要求：S0–S4 的重复条目在整合后保留一条，并标记为 S5。
        # 因此凡经整合（无论原出自几份文档）一律标记为 S5 条目。
        m["doc"] = "S5"
        m["doc_count"] = len(docs)

    # --- 1b. 章节索引：按 (section, subsection) 合并 ---
    sec_entries = [x for x in entries if x["kind"] == "章节"]
    sec_merged = OrderedDict()
    for x in sec_entries:
        k = (x["doc"], x["section"], x.get("subsection"))
        if k not in sec_merged:
            sec_merged[k] = dict(x)
    sec_seen = defaultdict(list)
    for x in sec_entries:
        sec_seen[(x["section"], x.get("subsection"))].append(x["doc"])
    for k, v in sec_merged.items():
        v["merged_from"] = list(dict.fromkeys(sec_seen[(v["section"], v.get("subsection"))]))

    # --- 1c. 章节骨架（按文档） ---
    sections = IDX["sections"]

    # --- 1d. S5 整合记录 ---
    s5 = DEC.S5_MERGES if DEC else []

    # 统计
    stats = {
        "entities": len(merged),
        "sections": len(sec_merged),
        "s5_merges": len(s5),
        "raw_entries": len(entries),
        "dedup_saved": len(entries) - (len(merged) + len(sec_merged)),
    }

    # ---------------- 生成 HTML ----------------
    payload = {
        "entities": [
            {"id": m["ref_id"], "type": m["kind"], "group": TYPE_GROUP.get(m["kind"], "other"),
             "title": m["title"], "summary": m["summary"][:400], "doc": "S5",
             "docs": ["S5"] + m["merged_from"], "n_from": len(m["merged_from"]),
             "sec": (m["sections"][0][1] if m["sections"] else ""),
             "sub": (m["sections"][0][2] or "") if m["sections"] else "",
             "sections": [f'{d}｜{s}' + (f' → {sb}' if sb else "")
                          for d, s, sb in dict.fromkeys(m["sections"])],
             "href": ("wiki/" + wiki_href(m["ref_id"])) if m["ref_id"] in NODES else ""}
            for m in merged.values()
        ],
        "sections": [
            {"doc": v["doc"], "section": v["section"], "sub": v.get("subsection") or "",
             "title": v["title"], "summary": v.get("summary") or "",
             "docs": v["merged_from"], "group": "__sec"}
            for v in sec_merged.values()
        ],
        "s5": [
            {"id": x["id"], "topic": x["topic"], "statement": x["s5_statement"],
             "merged_from": x["merged_from"], "basis": x["basis"], "group": "__s5"}
            for x in s5
        ],
    }

    filters = [{"k": "*", "label": "全部"}] + [
        {"k": g, "label": GROUP_LABEL[g]} for g in GROUP_ORDER
        if any(x["group"] == g for x in payload["entities"])
    ] + [{"k": "__sec", "label": "章节"}, {"k": "__s5", "label": "S5 整合记录"}]

    doc_groups = OrderedDict()
    for g in GROUP_ORDER:
        items = [x for x in payload["entities"] if x["group"] == g]
        if items:
            doc_groups[GROUP_LABEL[g]] = items

    body = [f"""
<header><div class="hdr">
<h1>泛德意志的欧洲 · <span style="color:var(--accent)">设定集索引</span>
<span class="sub">S0–S4 重复条目已整合为 S5，单条保留 · 共 {stats['entities']} 个实体条目</span></h1>
<nav class="crumbs">
<a href="home.html">← 主页</a> ／ <a href="index.html">索引</a> ／ <a href="timeline.html">交互式时间轴</a> ／
<a href="#wiki">百科词条</a> ／ <a href="#s5">S5 整合层</a> ／ <a href="#sources">出处</a>
</nav></div></header>
<main>
<div class="card">
<b>S5 整合说明</b><br>
原索引对同一实体的不同文档记载分列多条（如「法兰克立宪君主国」在 S0/S1/S2/S3 各一条）。
本次已把这些条目<b>按实体 ID 整合为一条</b>，整合结果标记为 <span class="tag s5">S5</span>，
并在词条页的「出处」中列出被合并的全部原文档。
原始条目 {stats['raw_entries']} 条 → 去重后 {stats['entities']} 个实体 + {stats['sections']} 个章节
（减少 {stats['dedup_saved']} 条冗余）。
</div>

<div class="q">
<input id="q" type="search" placeholder="检索：奥克、普热米斯尔、蒙福尔、罗斯兀鲁思、维也纳和约、待定、S5……" autocomplete="off">
<div class="chips" id="chips"></div>
</div>
<div class="count" id="count"></div>
<div id="list"></div>

<h2 id="wiki">百科词条（按类型）</h2>
"""]

    # 历史文献仿真入口
    try:
        import kb_documents as _KD
        _nd = len(_KD.DOCUMENTS) + len(_KD.DIARIES) + len(_KD.LETTERS) + len(_KD.SPEECHES)
        body.append(f"""
<h2 id="docs">历史文献仿真（{_nd} 篇）</h2>
<div class="card">
<span class="kindbadge">S* 仿真文献层</span>
基于 S0–S5 的既有设定<b>生成</b>的历史文献、人物日记、书信与演讲。
文献形制符合世界线（法兰克用德语并保留罗曼语地名、教廷用拉丁语、伊斯兰世界用阿拉伯／波斯语、
罗斯兀鲁思带蒙古制度词汇），内容只呈现已有设定，<b>不新增设定</b>。<br><br>
<b>历史文献 {len(_KD.DOCUMENTS)}</b>　宪章、和约、加冕诏书、敕令、教会决议、语言规划议定书、实录、官修史书序、学术论著、通商敕令、正常化法案、议会记录、废止文书<br>
<b>人物日记 {len(_KD.DIARIES)}</b>　鲁道夫、奥托卡二世、阿尔布雷希特二世、黎塞留、蒙福尔四世、约翰娜·冯·阿尔孔、战地士兵、安纳托利亚官员、波斯遗民僧人<br>
<b>书信 {len(_KD.LETTERS)}</b>　鲁道夫致爱德华一世、普热米斯尔致哈布斯堡、斯特拉斯堡致马格德堡、蒙福尔一世致法兰克宫廷、伊比利亚首相致州督、罗斯兀鲁思致基辅王国、路德致诸侯、马西利恩商会致帕里斯<br>
<b>演讲 {len(_KD.SPEECHES)}</b>　1848 大德意志议会、1871 罗马加冕、1945 不列颠制宪、1789 伊比利亚革命、1920 维也纳共和国成立、1945 德意志联邦重建、西域-波斯长老会议、忽里勒台谕示<br><br>
<a href="wiki/index.html"><b>→ 进入历史文献仿真总索引</b></a>
</div>
""")
    except ImportError:
        pass

    for label, items in doc_groups.items():
        body.append(f'<h3>{H.esc(label)}（{len(items)}）</h3><div class="chips">')
        for it in items:
            body.append(f'<a class="chip" href="{it["href"]}">{H.esc(it["title"])}</a>')
        body.append("</div>")

    body.append('<h2 id="s5">S5 整合层 · 重复条目合并记录</h2>')
    body.append('<div class="legend">S0–S4 中对同一主题的重复记载，整合后的单一表述如下。</div>')
    for x in payload["s5"]:
        mf = "".join(f'<li>{H.esc(m)}</li>' for m in x["merged_from"])
        body.append(f"""<div class="card">
<h3>{H.esc(x['topic'])}<span class="rid">{H.esc(x['id'])}</span></h3>
<p><b>S5 整合表述：</b>{H.esc(x['statement'])}</p>
<details><summary class="legend">被合并的原条目（{len(x['merged_from'])} 条）</summary><ul>{mf}</ul></details>
<p class="legend">整合依据：{H.esc(x['basis'])}</p>
</div>""")

    body.append('<h2 id="sources">文档清单与出处</h2>')
    body.append(H.src_legend_html())
    body.append('<h3>各文档章节骨架</h3>')
    for sid in ("S0", "S1", "S2", "S3", "S4"):
        if sid not in sections:
            continue
        meta = next((s for s in D.META["source_documents"] if s["id"] == sid), {})
        body.append(f'<div class="card"><h4><code>{sid}</code>　{H.esc(meta.get("title",""))}</h4>'
                    f'<div class="legend">{H.esc(meta.get("role",""))}</div><ul>')
        for sec in sections[sid]:
            section, sub, summary = sec[0], sec[1], sec[2]
            body.append(f'<li><b>{H.esc(section)}</b>' + (f' → {H.esc(sub)}' if sub else "")
                        + (f'<br><span class="legend">{H.esc(summary)}</span>' if summary else "") + '</li>')
        body.append('</ul></div>')

    body.append("</main>")

    js = f"""
<script>
const DATA = {json.dumps(payload['entities'] + payload['sections'] + payload['s5'], ensure_ascii=False)};
const FILTERS = {json.dumps(filters, ensure_ascii=False)};
const active = new Set();
const chipsEl = document.getElementById('chips');
FILTERS.forEach(f => {{
  const c = document.createElement('div');
  c.className='chip'; c.textContent=f.label; c.dataset.k=f.k;
  if(f.k==='*') c.classList.add('on');
  c.onclick=()=>{{
    if(f.k==='*') {{ active.clear(); }}
    else {{ active.has(f.k)?active.delete(f.k):active.add(f.k);
            chipsEl.querySelector('[data-k="*"]').classList.toggle('on', active.size===0); }}
    document.querySelectorAll('.chip[data-k]').forEach(x=>{{
      if(x.dataset.k!=='*') x.classList.toggle('on', active.has(x.dataset.k));
    }});
    render();
  }};
  chipsEl.appendChild(c);
}});
const q=document.getElementById('q'); q.addEventListener('input',render);
function esc(s){{return (s==null?'':String(s)).replace(/[&<>"]/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[m]));}}
// 设定集原文用 **…** 标重点：先按 ** 切分原文 → 逐段转义 → 偶数段包 <strong>，
// 最后才做 <mark> 检索高亮（否则高亮会把两个星号拆开而无法配对）。
function hl(s,t){{
  const parts=String(s==null?'':s).split('**');
  let o=parts.map((p,i)=>(i%2)?'<strong>'+esc(p)+'</strong>':esc(p)).join('');
  if(!t) return o;
  const safe=t.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&');
  try{{return o.replace(new RegExp('('+safe+')','gi'),'<mark>$1</mark>');}}catch(e){{return o;}}}}
function render(){{
  const term=q.value.trim(), t=term.toLowerCase();
  let rows=DATA;
  if(active.size) rows=rows.filter(r=>active.has(r.group));
  if(t) rows=rows.filter(r=>((r.title||'')+' '+(r.summary||'')+' '+(r.id||'')+' '+(r.sec||'')+' '
        +(r.sub||'')+' '+((r.docs||[]).join(' '))+' '+((r.sections||[]).join(' '))).toLowerCase().includes(t));
  document.getElementById('count').textContent='命中 '+rows.length+' / '+DATA.length+' 条';
  const list=document.getElementById('list');
  if(!rows.length){{list.innerHTML='<div class="empty">没有匹配的索引条目。</div>';return;}}
  list.innerHTML=rows.slice(0,400).map(r=>{{
    const ttl=r.href?('<a href="'+r.href+'">'+hl(r.title,term)+'</a>'):hl(r.title,term);
    let docs='';
    if(r.group==='__sec') docs=(r.docs||[]).map(d=>'<span class="tag'+(d==='S5'?' s5':'')+'">'+esc(d)+'</span>').join('');
    else if(r.group==='__s5') docs='<span class="tag s5">S5</span>';
    else {{
      docs='<span class="tag s5">S5</span>';
      if((r.docs||[]).length>1) docs+='<span class="legend"> 整合自 '+
        (r.docs.filter(d=>d!=='S5').map(esc).join('、'))+'</span>';
    }}
    const secs=(r.group==='__s5')?'':(r.sec?' ｜ '+esc(r.sec):'')+(r.sub?' → '+esc(r.sub):'');
    return '<div class="item"><h3>'+ttl+(r.id?'<span class="rid">'+esc(r.id)+'</span>':'')+'</h3>'
      +'<div class="meta">'+docs+secs+'</div>'
      +(r.summary?'<div class="sm">'+hl(r.summary,term)+'</div>':'')+'</div>';
  }}).join('')+(rows.length>400?'<div class="empty">仅显示前 400 条，请细化检索词。</div>':'');
}}
render();
</script>
"""
    html_out = H.page("泛德意志的欧洲 · 设定集索引", "\n".join(body), extra_js=js, active="index")
    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html_out)
    print(f"  index.html：{stats['entities']} 实体 + {stats['sections']} 章节 + {stats['s5_merges']} 条 S5 整合记录"
          f"（原 {stats['raw_entries']} 条，减少 {stats['dedup_saved']}）")
    return payload


# ==================================================================
# 2. 维基式词条
# ==================================================================
FIELD_ORDER = {
    "COUNTRY": ["name_de", "name_local", "name_en", "polity", "dynasty", "religion",
                "capital", "territory", "language", "founded", "time_span", "peoples",
                "key_traits", "allies", "enemies", "wars", "treaties", "policies",
                "subdivisions", "parties", "orgs"],
    "DYNASTY": ["name_de", "name_en", "name_local", "type", "origin", "founded", "ends",
                "religion", "capital", "key_dates", "holdings", "members"],
    "PERSON": ["name_de", "name_en", "name_local", "title", "dynasty", "country_id",
               "birth", "death", "reign", "positions", "deeds", "family"],
    "EVENT": ["year_text", "epoch", "region", "event_de", "event_en", "country_ids",
              "persons", "causes", "effects", "war_id", "treaty_id", "significance"],
    "WAR": ["name_de", "name_en", "time_text", "epoch", "side_a", "side_b",
            "other_claimants", "causes_text", "phases", "key_battles", "result",
            "consequence", "treaty"],
    "TREATY": ["name_de", "name_en", "time", "place", "parties", "background",
               "clauses", "seven_electors", "significance"],
    "RELIGION": ["name_de", "name_en", "type", "doctrine", "culture", "political_role",
                 "followers_regions"],
    "LANGUAGE": ["name_de", "name_en", "family", "base", "regions", "principles",
                 "examples", "institution", "sociolinguistics"],
    "PLACE": ["type", "de", "en", "real", "note"],
    "SUBDIVISION": ["name_de", "level_system", "units", "oct_province", "southern_hubs",
                    "constitution", "issues"],
    "ARTIFACT": ["kind", "period", "material", "holder", "place_id", "repository",
                 "repo_id", "significance"],
    "PARTY": ["name_de", "name_en", "spectrum", "base", "note"],
    "ORGANIZATION": ["name_de", "name_en", "type", "members", "function"],
}
FIELD_LABEL = {
    "name_de": "德文", "name_local": "本地语", "name_en": "英文", "polity": "政体",
    "dynasty": "王朝", "religion": "宗教", "capital": "首都", "territory": "领土",
    "language": "语言", "founded": "建立", "time_span": "存续", "peoples": "民族",
    "key_traits": "关键特征", "allies": "同盟", "enemies": "敌对", "wars": "参与战争",
    "treaties": "相关条约", "policies": "政策", "subdivisions": "行政区划",
    "parties": "政党", "orgs": "相关机构", "type": "类型", "origin": "起源",
    "ends": "终结", "key_dates": "关键年份", "holdings": "领有", "members": "成员",
    "title": "头衔", "birth": "生", "death": "卒", "reign": "在位", "positions": "职位",
    "deeds": "事迹", "family": "家族", "year_text": "年份", "epoch": "时代",
    "region": "地域", "country_ids": "涉及国家", "persons": "涉及人物",
    "causes": "前因", "effects": "后果", "war_id": "关联战争", "treaty_id": "关联条约",
    "significance": "意义", "time_text": "时间", "side_a": "A 方", "side_b": "B 方",
    "other_claimants": "其他主张者", "causes_text": "起因", "phases": "阶段",
    "key_battles": "关键战斗", "result": "结果", "consequence": "后果",
    "treaty": "条约", "time": "时间", "place": "地点", "parties_": "缔约方",
    "background": "背景", "clauses": "条款", "seven_electors": "七位选侯",
    "doctrine": "教义", "culture": "文化", "political_role": "政治角色",
    "followers_regions": "信众分布", "family_": "语系", "base": "基础", "regions": "分布",
    "principles": "原则", "examples": "示例", "institution": "机构",
    "sociolinguistics": "社会语言学", "de": "德文", "en": "英文", "real": "现实对应",
    "note": "备注", "level_system": "层级体系", "units": "下级单位",
    "oct_province": "南部奥克省", "southern_hubs": "南方枢纽",
    "constitution": "宪制", "issues": "问题", "spectrum": "政治光谱",
    "kind": "类别", "period": "年代", "material": "材质", "repository": "现藏",
    "repo_id": "收藏机构", "holder": "现存持有方", "place_id": "存放地",
    "event_de": "德文", "event_en": "英文", "parties": "缔约方",
}


def render_value(k, v):
    if k in ("country_ids", "persons", "causes", "effects", "war_id", "treaty_id",
             "subdivisions", "parties", "orgs", "members", "allies", "enemies", "wars",
             "treaties"):
        if isinstance(v, list):
            return "、".join(link(x) if x in NODES else H.esc(x) for x in v)
        if isinstance(v, str) and v in NODES:
            return link(v)
    if k == "country_id" and isinstance(v, str) and v in NODES:
        return link(v)
    if k in ("holder", "place_id", "repo_id") and isinstance(v, str) and v in NODES:
        return link(v)
    if k == "dynasty_id" and isinstance(v, str) and v in NODES:
        return link(v)
    if k in ("war_id", "treaty_id") and isinstance(v, str) and v in NODES:
        return link(v)
    if k in ("side_a", "side_b") and isinstance(v, dict):
        s = H.esc(v.get("name", ""))
        mem = v.get("members") or []
        cids = v.get("country_ids") or []
        if cids:
            s += "（" + "、".join(link(c) for c in cids) + "）"
        if mem:
            s += "<br><span class='legend'>" + "；".join(H.esc(m) for m in mem) + "</span>"
        return s
    return H.e(v)


def build_wiki():
    n = 0
    by_group = defaultdict(list)
    for eid, ent in ENTITIES.items():
        by_group[TYPE_GROUP.get(ent["type"], "other")].append(eid)

    for eid, ent in ENTITIES.items():
        t = ent["type"]
        title = disp_name(ent)
        node = NODES.get(eid, {})

        props = []
        for k in FIELD_ORDER.get(t, ["name_de", "name_en"]):
            if k in ent and ent[k] not in (None, [], {}):
                props.append((FIELD_LABEL.get(k, k), render_value(k, ent[k])))
        if t == "PLACE":
            for k in ("zh_alias",):
                if ent.get(k):
                    props.append(("中文别名", H.e(ent[k])))

        # 概述
        overview = ent.get("overview") or ent.get("summary")
        overview_html = H.inline_md(H.esc(overview)) if overview else ""
        extra = []
        for k in ("religions_detail", "context", "appendix"):
            pass
        if ent.get("religions_detail"):
            extra.append(("宗教详情", H.e(ent["religions_detail"])))
        if ent.get("context"):
            extra.append(("语境", H.e(ent["context"])))
        if ent.get("notes"):
            extra.append(("编纂注记", H.e(ent["notes"])))

        # 关系
        rels = rel_rows(eid)
        rel_html = ""
        if rels:
            trs = "".join(
                f'<tr><td><code>{H.esc(k)}</code></td><td>{ar}</td>'
                f'<td>{link(to) if to in NODES else H.esc(fn)}</td>'
                f'<td>{H.esc(lb)}</td><td>{H.esc(tm)}</td>'
                f'<td>{H.esc(st)}</td></tr>'
                for k, ar, fn, to, tn, lb, tm, st in rels)
            rel_html = (f'<h2>关系（{len(rels)}）</h2><table>'
                        '<tr><th>关系类型</th><th>方向</th><th>对方</th><th>说明</th>'
                        '<th>时期</th><th>状态</th></tr>' + trs + '</table>')

        # 出处（S5 整合）
        raw_srcs = ent.get("src") or node.get("src") or []
        src_html = (H.tag("S5", "s5") + " " +
                    "".join(H.tag(s) for s in raw_srcs))
        merged = (f'<p class="legend"><b>S5 整合条目</b>：本词条整合了 '
                  f'{"、".join(raw_srcs) if raw_srcs else "（文档未标）"} 的原记载，'
                  f'统一为单一表述。原始出处按下方标签列出。</p>')

        # 同组导航
        same = sorted(by_group[TYPE_GROUP.get(t, "other")],
                      key=lambda x: disp_name(NODES.get(x, {"id": x})))
        others = "".join(f'<a class="chip" href="{slug(o)}.html">{H.esc(disp_name(NODES[o]))}</a>'
                         for o in same if o != eid)

        parts = [
            f'<header><div class="hdr"><h1>{H.esc(title)}'
            f'<span class="sub">{H.esc(TYPE_LABEL.get(t, t))}　{status_tag(ent.get("status"), raw_srcs)}</span></h1>'
            f'<nav class="crumbs"><a href="../index.html">索引</a> ／ '
            f'<a href="../index.html#{TYPE_GROUP.get(t,"wiki")}">{H.esc(TYPE_LABEL.get(t, t))}</a> ／ '
            f'<a href="../timeline.html">时间轴</a></nav></div></header><main>',
            f'<div class="card"><div class="mono" style="color:var(--accent)">{H.esc(eid)}</div>',
            f'<p>{overview_html if overview else "（文档未载概述）"}</p>',
            merged,
            '</div>',
        ]
        if props:
            parts.append('<h2>属性</h2><dl class="kv">' + "".join(
                f'<dt>{H.esc(k)}</dt><dd>{v}</dd>' for k, v in props) + '</dl>')
        if extra:
            parts.append('<h2>补充</h2><dl class="kv">' + "".join(
                f'<dt>{H.esc(k)}</dt><dd>{v}</dd>' for k, v in extra) + '</dl>')
        if rel_html:
            parts.append(rel_html)
        parts.append('<h2>出处</h2>' + src_html)
        parts.append(f'<h2>同类型词条（{len(same)}）</h2><div class="chips">{others}</div>')
        parts.append('</main>')

        badge = ""
        page_html = H.page(f"{title} · 泛德意志的欧洲",
                           "\n".join(parts), extra_head=badge, base="../")
        with open(os.path.join(WIKI, f"{slug(eid)}.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(page_html)
        n += 1
    print(f"  wiki/：{n} 个词条页")
    return n


# ==================================================================
# 2b. 历史文献 / 日记 / 书信 / 演讲
# ==================================================================
def build_docs():
    try:
        import kb_documents as KD
    except ImportError:
        print("  （未找到 kb_documents.py，跳过文献页）")
        return 0

    def _merge(attr):
        out = list(getattr(KD, attr, []))
        for mn in ("kb_documents2", "kb_documents3"):
            try:
                mod = __import__(mn)
            except ImportError:
                continue
            out += list(getattr(mod, attr, []))
        return out

    GROUPS = [
        ("DOC", "历史文献仿真", "诏令、条约、宪章、敕令、实录、论著、法案", _merge("DOCUMENTS")),
        ("DIA", "人物日记", "以第一人称呈现当事人在关键年份的处境与抉择", _merge("DIARIES")),
        ("LET", "书信", "君主、首相、教会、商会、地方政府之间的往来书信", _merge("LETTERS")),
        ("SPEECH", "演讲", "议会、加冕、制宪、革命与立国演说", _merge("SPEECHES")),
    ]

    items = []
    for prefix, glabel, gdesc, coll in GROUPS:
        for d in coll:
            rec = dict(d)
            rec["_group"] = prefix
            rec["_glabel"] = glabel
            rec["_gdesc"] = gdesc
            rec["_slug"] = d["id"].lower().replace("_", "-")
            items.append(rec)

    for d in items:
        meta = []
        if d.get("author"):
            meta.append(("作者／发出方", H.esc(d["author"])))
        if d.get("recipient"):
            meta.append(("受信人", H.esc(d["recipient"])))
        if d.get("title_orig"):
            meta.append(("原文题名", f'<span class="mono">{H.esc(d["title_orig"])}</span>'))
        meta.append(("年代", H.esc(d.get("year_text") or d.get("year"))))
        if d.get("place"):
            pl = d.get("place_id")
            meta.append(("地点", link(pl) if pl and pl in NODES else H.esc(d["place"])))
        if d.get("lang"):
            meta.append(("语文", H.esc(d["lang"])))
        meta.append(("类别", H.esc(d["kind"])))

        body = d.get("body") or ""
        # 正文中的实体名标为交叉引用（span，不插 <a>，避免与正文自身链接嵌套），
        # 词条超链接统一放在文末「本文涉及的词条」区。
        refs = []
        for eid, nd in NODES.items():
            nm = disp_name(nd)
            if nm and len(nm) >= 3 and nm in body:
                body = body.replace(
                    nm, f'<span class="xr" title="词条：{H.esc(nm)}">{H.esc(nm)}</span>')
                refs.append((eid, nm))

        ctx = H.esc(d.get("context") or "")
        sig = H.esc(d.get("significance") or "")
        srcs = d.get("src") or []
        src_html = H.tag("S*", "sstar") + " " + "".join(H.tag(s) for s in srcs)

        same = [x for x in items if x["_group"] == d["_group"] and x["id"] != d["id"]]
        others = "".join(
            f'<a class="chip" href="{x["_slug"]}.html">{H.esc(x["title"])}</a>' for x in same)

        parts = [
            f'<header><div class="hdr"><h1>{H.esc(d["title"])}'
            f'<span class="sub">{H.esc(d["_glabel"])}　{src_html}</span></h1>'
            f'<nav class="crumbs"><a href="../index.html">索引</a> ／ '
            f'<a href="index.html">历史文献</a> ／ '
            f'<a href="../timeline.html">时间轴</a></nav></div></header><main>',
            '<div class="card"><div class="legend">'
            '<b>S* 仿真文献</b>：本文献基于 S0–S5 的既有设定仿真生成，'
            '用于呈现已确立的设定，不新增任何设定。年份、地点、人物、教派、政体与术语均锚定正典；'
            '若需作为正典引用，请先确认。</div></div>',
            f'<div class="doc"><h3>{H.esc(d["title"])}</h3>'
            f'<div class="dsub">{H.esc(d.get("title_orig") or "")}　·　'
            f'{H.esc(d.get("year_text") or d.get("year"))}　·　{H.esc(d.get("place") or "")}</div>'
            f'{body}</div>',
            '<h2>文献信息</h2><dl class="docmeta">' + "".join(
                f'<dt>{H.esc(k)}</dt><dd>{v}</dd>' for k, v in meta) + '</dl>',
        ]
        if ctx:
            parts.append(f'<h2>设定依据</h2><p>{ctx}</p>')
        if sig:
            parts.append(f'<h2>在设定中的作用</h2><p>{sig}</p>')
        if refs:
            seen_nm = set()
            chips = []
            for eid, nm in sorted(set(refs), key=lambda x: x[1]):
                if nm in seen_nm:
                    continue
                seen_nm.add(nm)
                chips.append(f'<a class="chip" href="{wiki_href(eid)}">{H.esc(nm)}</a>')
            parts.append(f'<h2>本文涉及的词条（{len(chips)}）</h2>'
                         f'<div class="chips">{"".join(chips)}</div>')
        parts.append('<h2>出处</h2>' + src_html)
        if others:
            parts.append(f'<h2>同类文献（{len(same)}）</h2><div class="chips">{others}</div>')
        parts.append('</main>')

        html_out = H.page(f'{d["title"]} · 历史文献 · 泛德意志的欧洲',
                          "\n".join(parts), base="../", active="docs")
        with open(os.path.join(WIKI, f'{d["_slug"]}.html'), "w", encoding="utf-8",
                  newline="\n") as f:
            f.write(html_out)

    # ---------------- 总索引页 ----------------
    parts = ["""
<header><div class="hdr">
<h1>泛德意志的欧洲 · <span style="color:var(--accent)">历史文献仿真</span>
<span class="sub">基于 S0–S5 设定生成的文献、日记、书信与演讲</span></h1>
<nav class="crumbs"><a href="../home.html">主页</a> ／ <a href="../index.html">索引</a> ／
<a href="../timeline.html">交互式时间轴</a></nav></div></header><main>
<div class="card"><div class="legend">
<b>S* 仿真文献层</b>并非设定集原文，而是<b>依据设定生成</b>的可读文本，用于呈现已确立的设定。
每条文献的年份、地点、人物、教派、政体与术语均锚定正典；文献形制亦符合世界线：
法兰克用德语并保留罗曼语地名（帕里斯、雷姆斯），教廷与部分正本用拉丁语，
伊斯兰世界用阿拉伯／波斯语，罗斯兀鲁思用东斯拉夫语并带蒙古制度词汇。<br>
<b>不新增设定</b>——文献只用来「演出」设定，不用来「扩充」设定。
</div></div>
"""]
    for prefix, glabel, gdesc, _c in GROUPS:
        sub = [x for x in items if x["_group"] == prefix]
        if not sub:
            continue
        parts.append(f'<h2>{H.esc(glabel)}（{len(sub)}）</h2>'
                     f'<div class="legend">{H.esc(gdesc)}</div><table>'
                     f'<tr><th>年代</th><th>题名</th><th>作者／发出方</th><th>地点</th><th>语文</th></tr>')
        for x in sorted(sub, key=lambda y: y["year"]):
            parts.append(
                f'<tr><td>{H.esc(x.get("year_text") or x["year"])}</td>'
                f'<td><a href="{x["_slug"]}.html">{H.esc(x["title"])}</a></td>'
                f'<td>{H.esc(x.get("author") or "—")}</td>'
                f'<td>{H.esc(x.get("place") or "—")}</td>'
                f'<td>{H.esc(x.get("lang") or "—")}</td></tr>')
        parts.append('</table>')
    parts.append('</main>')

    html_out = H.page("历史文献仿真 · 泛德意志的欧洲", "\n".join(parts), base="../", active="docs")
    with open(os.path.join(WIKI, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html_out)

    print(f"  wiki/：{len(items)} 篇仿真文献（"
          + " / ".join(f"{gl} {len(coll)}" for _, gl, _, coll in GROUPS)
          + "） + 文献总索引 1 页")
    return len(items)



# ==================================================================
# 2c. 主页
# ==================================================================
HOME_THEME_RULES = {
    "rel": ["天主教", "教皇", "教宗", "路德", "加尔文", "胡斯", "福音", "宗教", "信仰", "教会", "新教", "穆斯林", "伊斯兰", "佛教", "萨满", "长生天", "政教"],
    "cul": ["语言", "正字法", "大学", "学院", "学术", "科学", "音乐", "艺术", "教堂", "建筑", "咖啡馆", "文学", "出版", "编纂", "宪章", "和约", "条约", "条款"],
    "pol": ["王朝", "继承", "加冕", "革命", "战争", "条约", "共和", "帝国", "联邦", "独立", "统一", "议会", "宪", "同盟", "一战", "二战"],
}


def build_home():
    try:
        import kb_documents as KD
        docs_all = list(KD.DOCUMENTS + KD.DIARIES + KD.LETTERS + KD.SPEECHES)
    except ImportError:
        KD, docs_all = None, []
    # 第二批、第三批文献
    try:
        import kb_documents2 as KD2
        docs_all += list(KD2.DOCUMENTS + KD2.DIARIES + KD2.LETTERS + KD2.SPEECHES)
    except ImportError:
        KD2 = None
    try:
        import kb_documents3 as KD3
        docs_all += list(KD3.DOCUMENTS + KD3.DIARIES + KD3.LETTERS + KD3.SPEECHES)
    except ImportError:
        KD3 = None

    # ---------------- 统计 ----------------
    counts = ENT["counts"]
    n_edges = GRAPH["meta"]["edge_count"]
    n_nodes = GRAPH["meta"]["node_count"]
    n_docs = len(docs_all)
    years = [r["year"] for r in TBL["timeline"]["rows"]]
    n_pend = len(PEND["items"])
    n_conf = len(CONS["findings"])
    n_none = sum(1 for f in CONS["findings"] if f["severity"] == "高")

    # 索引去重统计
    raw_index = len(IDX["entries"])
    n_ent_index = len({x["ref_id"] for x in IDX["entries"] if x.get("ref_id")})
    n_s5 = len(DEC.S5_MERGES) if DEC else 0

    # 仿真文献分类计数（含第二、三批）—— 按 ID 前缀归类
    _n_doc = _n_dia = _n_let = _n_sp = 0
    for _d in docs_all:
        _i = _d.get("id", "")
        if _i.startswith("DIA_"):
            _n_dia += 1
        elif _i.startswith("LET_"):
            _n_let += 1
        elif _i.startswith("SPEECH_"):
            _n_sp += 1
        else:
            _n_doc += 1

    assert _n_doc + _n_dia + _n_let + _n_sp == len(docs_all), "文献分类计数与总数不符"

    # ---------------- 类型入口 ----------------
    # 与「分类型清单页」共用同一数据源，卡片数量即真实实体数
    GROUPS = [(key, label, ico, desc)
              for key, label, ico, desc in LISTING_TYPES
              if counts.get(key, 0)]

    # ---------------- 迷你时间轴 ----------------
    def theme(r):
        txt = (r["event_zh"] or "") + (r.get("region") or "") + (r.get("epoch") or "") \
              + (r.get("result") or "")
        for k in ("rel", "cul", "pol"):
            if any(w in txt for w in HOME_THEME_RULES[k]):
                return k
        return "pol"

    # 三个泳道：宗教 / 文化 / 制度·军事；用密度柱 + 关键锚点表现
    tm_rows = {"rel": [], "cul": [], "pol": []}
    for r in TBL["timeline"]["rows"]:
        tm_rows[theme(r)].append(r)
    y0, y1 = min(years), max(years)
    span = max(1, y1 - y0)
    LANES = [("rel", "宗教"), ("cul", "文化·文献"), ("pol", "制度·军事")]
    LANE_CLS = {"rel": "rel", "cul": "cul", "pol": "pol"}

    def px(y):
        return (y - y0) / span * 100

    # 每 20 年一个桶；柱高编码事件密度。柱必须落在自己的泳道内。
    BUCKET = 20
    lane_html = []
    for key, label in LANES:
        items = tm_rows[key]
        buckets = {}
        for r in items:
            b = int((r["year"] - y0) // BUCKET)
            buckets.setdefault(b, []).append(r)
        bars = []
        for b, group in sorted(buckets.items()):
            yr = y0 + b * BUCKET
            left = px(yr)
            n = len(group)
            h = 6 + min(1.0, n / 6.0) * 30
            ttl = "; ".join(f'{x["year_text"]} {x["event_zh"]}' for x in group)
            bars.append(
                f'<a class="bar {LANE_CLS[key]}" style="left:{left:.2f}%;height:{h:.1f}px" '
                f'href="wiki/{slug(group[0]["id"])}.html" '
                f'title="{H.esc(ttl)}"></a>')
        lane_html.append(
            f'<div class="tlmini-lane"><span>{label}</span>'
            f'<div class="tlmini-bars">{"".join(bars)}</div></div>')

    # 关键锚点
    ANCHORS = [1270, 1356, 1524, 1648, 1789, 1871, 1918, 1945, 1960]
    anchor_html = "".join(
        f'<div class="tlmini-anchor" style="left:{px(y):.2f}%"><i></i><b>{y}</b></div>'
        for y in ANCHORS if y0 <= y <= y1)

    mini = ('<div class="tl-mini">'
            '<div class="tlmini-grid">'
            + "".join(f'<div class="tlmini-line" style="left:{px(y):.2f}%"></div>'
                       for y in range(((y0 // 100) + 1) * 100, y1, 100))
            + '</div>'
            + "".join(lane_html)
            + anchor_html
            + '</div>'
            '<div class="tlmini-foot">'
            f'<span>柱高＝该 20 年内的事件数　·　'
            f'<b style="color:#c25b45">宗教</b>　'
            f'<b style="color:#7fa650">文化·文献</b>　'
            f'<b style="color:#8fb6d8">制度·军事</b></span>'
            f'<span>共 {len(years)} 个事件节点 · 范围 {y0}—{y1}</span>'
            '</div>')

    # ---------------- 精选 ----------------
    def pick(ids):
        return "".join(
            f'<a class="pill" href="wiki/{slug(i)}.html">{H.esc(disp_name(NODES[i]))}</a>'
            for i in ids if i in NODES)

    featured = [
        ("关键国家", ["C_FRANKEN", "C_DEUTSCHLAND", "C_UK", "C_IBERIA", "C_ROS_UHLUS",
                      "C_KIEV", "C_SWITZERLAND", "C_USA", "C_ANATOLIAN_TURKS",
                      "C_PERSIA", "C_PERSIA_BUDDHIST", "C_MAGHREB", "C_BYZANTIUM"]),
        ("核心王朝", ["D_HABSBURG", "D_PREMISLID", "D_PLANTAGENET", "D_MOUNTFORT",
                      "D_MONGOL", "D_MOSCOW_MONGOL", "D_MAMLUK", "D_PERSIAN_LINE"]),
        ("关键人物", ["PE_RUDOLF", "PE_OTTOKAR_II", "PE_ALBRECHT_II", "PE_EDWARD_I",
                      "PE_MARTIN_LUTHER", "PE_JOHANNA_VON_ARKON", "PE_KARDINAL_RICHELIEU",
                      "PE_SALADIN", "PE_BAIBARS", "PE_MOUNTFORT_IV"]),
        ("转折事件", ["E_1270_CAPET", "E_1272_RUDOLF", "E_1356_CHARTER", "E_1524_PEASANTS",
                      "E_1618_RELIGION", "E_1648_VIENNA", "E_1789_REVOLUTION",
                      "E_1848_REVOLUTION", "E_1866_WAR", "E_1871_EMPIRE",
                      "E_WW1", "E_1939_WW2", "E_1945_SETTLEMENT", "E_1960_MULTIPOLAR"]),
        ("关键条约", ["T_FRANKFURT_1356", "T_VIENNA_1648", "T_TWELVE_ARTICLES",
                      "T_RIGHTS_CHARTER"]),
        ("宗教与语言", ["R_CATHOLIC", "R_LUTHERAN", "R_CALVIN", "R_HUSSITE", "R_ALPEN",
                        "R_ISLAM", "R_BUDDHISM", "R_TENGRI",
                        "L_STANDARD", "L_FRANKISH", "L_OCCITAN", "L_ENGLISH"]),
    ]

    # ---------------- 文献精选 ----------------
    doc_pick = []
    if KD:
        for d in (KD.DOCUMENTS[:4] + KD.DIARIES[:3] + KD.LETTERS[:3] + KD.SPEECHES[:3]):
            doc_pick.append(d)
    doc_html = "".join(
        f'<a class="pill" href="wiki/{d["id"].lower().replace("_", "-")}.html">'
        f'{H.esc(d["year_text"] if d["year_text"] and len(d["year_text"]) < 14 else d["year"])}'
        f'　{H.esc(d["title"])}</a>'
        for d in doc_pick)

    # ---------------- 组装 ----------------
    body = [f"""
<div class="hero">
  <h1>泛德意志的欧洲 · <b>架空世界设定知识库</b></h1>
  <div class="tagline">
    一条从 1270 年卡佩绝嗣分叉出去的世界线：西部的<b>哈布斯堡法兰克</b>与东部的<b>普热米斯尔德意志</b>
    共享日耳曼语连续体，却因宗教、王朝与政治路径永久分裂；伊比利亚成为持续打破中欧平衡的第三极；
    罗斯兀鲁思继承了金帐汗国；不列颠保存了罗曼高文化却走上绝对主义。
  </div>
  <div class="realms">
    <span class="realm">德意志 <i>文明核心</i></span>
    <span class="realm">法兰克 <i>文明边界</i></span>
    <span class="realm">伊比利亚 <i>秩序挑战者</i></span>
    <span class="realm">罗斯兀鲁思 <i>欧亚平衡者</i></span>
    <span class="realm">不列颠 <i>海洋平衡者</i></span>
    <span class="realm">美国 <i>海外工业强国</i></span>
  </div>
  <svg class="fork" viewBox="0 0 900 208" role="img"
       aria-label="1270 年卡佩绝嗣后的历史分叉示意图">
    <defs>
      <linearGradient id="gA" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#4a4133"/><stop offset="1" stop-color="#4a76a8"/>
      </linearGradient>
      <linearGradient id="gB" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#4a4133"/><stop offset="1" stop-color="#a8485a"/>
      </linearGradient>
      <linearGradient id="gC" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#4a4133"/><stop offset="1" stop-color="#b09440"/>
      </linearGradient>
    </defs>

    <circle cx="72" cy="104" r="8" fill="#c9a227"/>
    <circle cx="72" cy="104" r="15" fill="none" stroke="#c9a227" stroke-width="1" opacity=".35"/>
    <text x="72" y="140" text-anchor="middle" class="fkl">1270</text>
    <text x="72" y="158" text-anchor="middle" class="fkl">卡佩绝嗣</text>

    <path d="M82 104 C 170 104, 190 44, 282 44" fill="none" stroke="url(#gA)" stroke-width="2.5"/>
    <path d="M82 104 C 170 104, 190 104, 282 104" fill="none" stroke="url(#gB)" stroke-width="2.5"/>
    <path d="M82 104 C 170 104, 190 164, 282 164" fill="none" stroke="url(#gC)"
          stroke-width="2.5" stroke-dasharray="6 5"/>

    <circle cx="286" cy="44" r="6" fill="#4a76a8"/>
    <text x="302" y="40" class="fkt">1272　鲁道夫加冕「法兰克人的国王」</text>
    <text x="302" y="59" class="fks">→ 哈布斯堡法兰克 · 天主教 · 帕里斯 · 西日耳曼语</text>

    <circle cx="286" cy="104" r="6" fill="#a8485a"/>
    <text x="302" y="100" class="fkt">1273　奥托卡二世崛起</text>
    <text x="302" y="119" class="fks">→ 普热米斯尔德意志 · 新教 · 维也纳</text>

    <circle cx="286" cy="164" r="6" fill="#b09440"/>
    <text x="302" y="160" class="fkt">同期　伊比利亚统一 · 蒙古遗产 · 英伦承接罗曼</text>
    <text x="302" y="179" class="fks">→ 秩序挑战者 ／ 欧亚平衡者 ／ 海洋平衡者</text>

    <line x1="636" y1="24" x2="636" y2="104" stroke="#3f382e" stroke-width="1"/>
    <text x="644" y="78" class="fkm">1356 双王冠</text>
    <line x1="762" y1="24" x2="762" y2="104" stroke="#3f382e" stroke-width="1"/>
    <text x="770" y="78" class="fkm">1871 罗马加冕</text>
    <text x="770" y="94" class="fkm">双冠分离</text>
  </svg>
  <div class="legend" style="margin-top:12px;max-width:820px;margin-left:auto;margin-right:auto">
    三条分叉对应本世界线的三重分裂：<b>日耳曼世界的宗教—王朝分裂</b>（法兰克 vs 德意志），
    以及<b>伊比利亚／罗斯兀鲁思／不列颠</b>三条平行的文明路径。
  </div>
</div>
<main>

<div class="stats">
  <div class="stat"><b>{counts['countries']}</b><span>国家与政治实体</span></div>
  <div class="stat"><b>{counts['dynasties']}</b><span>王朝与家族</span></div>
  <div class="stat"><b>{counts['people']}</b><span>人物</span></div>
  <div class="stat"><b>{counts['events']}</b><span>事件</span></div>
  <div class="stat"><b>{counts['places']}</b><span>地点</span></div>
  <div class="stat"><b>{n_nodes}</b><span>实体节点</span></div>
  <div class="stat"><b>{n_edges}</b><span>关系边</span></div>
  <div class="stat"><b>{n_docs}</b><span>仿真文献</span></div>
</div>

<h2>入口</h2>
<div class="entries">
  <a class="entry wide" href="index.html">
    <span class="ico">🔍</span><span class="n">S5 整合</span>
    <h3>设定集索引</h3>
    <p>S0–S4 的重复条目已按实体整合为单条并标记 S5；{n_ent_index} 个实体条目、81 个章节骨架、
    {n_s5} 条 S5 整合记录，支持全文检索与按类型筛选。</p>
  </a>
  <a class="entry" href="wiki/index.html">
    <span class="ico">📚</span><span class="n">{n_docs}</span>
    <h3>历史文献仿真</h3>
    <p>文献 {_n_doc} ／ 日记 {_n_dia} ／书信 {_n_let} ／ 演讲 {_n_sp}。
    羊皮纸样式，标注设定依据。</p>
  </a>
  <a class="entry" href="timeline.html">
    <span class="ico">🕰</span><span class="n">{len(years)}</span>
    <h3>交互式时间轴</h3>
    <p>横轴为时间；纵轴可在<b>地域／宗教／文化／制度／军事／时代</b>六个视角间切换，
    点击事件展开因果链。</p>
  </a>
  <a class="entry" href="wiki/c-franken.html">
    <span class="ico">🏛</span><span class="n">{counts['countries']}</span>
    <h3>百科词条</h3>
    <p>每个国家、王朝、人物、事件各一页；含属性表、关系网与出处标签，实体之间自动互链。</p>
  </a>
  <a class="entry" href="wiki/docs-index.html">
    <span class="ico">📊</span><span class="n">4</span>
    <h3>文档中心</h3>
    <p>时间线表、国家表、人物表、战争表；中英德专有名词对照表与地名转写表；
    20 张表格全部转为 HTML，支持横向滚动与页面内目录。</p>
  </a>
  <a class="entry" href="wiki/consistency.html">
    <span class="ico">✅</span><span class="n">{n_conf}</span>
    <h3>一致性与待定项</h3>
    <p>一致性检查 {n_conf} 条发现（真实矛盾 {n_none} 条）；{n_pend} 条待定项已按 P0–P3
    分级并逐条给出方案与利弊。</p>
  </a>
</div>

<h2>时间轴速览</h2>
<div class="legend">范围 {y0} — {y1} 年，共 {len(years)} 个事件节点。点击圆点直达词条，或
<a href="timeline.html">打开完整交互式时间轴</a>。</div>
{mini}

<h2>关键设定速览</h2>
<div class="twocol">
  <div class="card">
    <h4>法兰克问题</h4>
    <p>法兰克人属于德意志文明，却最终没有成为德国人。
    <a href="wiki/c-franken.html">法兰克立宪君主国</a>奉天主教、使用法兰克语（西日耳曼语支，
    保留古法兰克军事法律词汇与名词性数格残留），是最早的宪政君主制之一。</p>
    <div class="quote">
      现实历史：德意志世界 ←→ 奥地利问题<br>
      本世界：德意志世界 ←→ <b>法兰克问题</b>
      <cite>《设定集补充》总纲</cite>
    </div>
  </div>
  <div class="card">
    <h4>英格兰问题</h4>
    <p>罗曼语世界的对称另一半：英格兰人属于罗曼-法兰西文明，却最终没有成为法兰西人。
    <a href="wiki/c-uk.html">不列颠</a>保存了 langue d'oïl 的最高语域，却因语言断层而走上绝对主义，
    直到 1945 年战败才被监督强制民主化。</p>
    <div class="quote">
      帕里斯自认是日耳曼世界的延伸；伦敦则放弃了日耳曼身份、更倾向罗曼身份，
      但对大陆领土不做要求。
      <cite>用户裁定 P33（正统错位）</cite>
    </div>
  </div>
  <div class="card">
    <h4>韧性测试</h4>
    <p>一个文明资产远比现实德意志世界庞大的德国，即使输掉世界大战，仍然拥有足够的结构性资本
    保存自身核心文明——于是“一战战败、二战胜利”不再是胜负安排，而是结构性实验。</p>
    <div class="quote">
      德意志帝国在一战中战败，君主政体瓦解；但维也纳、布拉格、米兰、阿姆斯特丹、莱比锡、哥廷根、
      苏黎世的学术中心与工业体系没有被摧毁。这是二战能够重新崛起的结构原因。
      <cite>《设定集补充》本轮确定</cite>
    </div>
  </div>
  <div class="card">
    <h4>波斯撕裂与文明边界</h4>
    <p>波斯曾抵御伊斯兰入侵，后因内乱退守河中及以东。「波斯」概念因此撕裂为两支：
    <a href="wiki/c-persia.html">伊朗（伊斯兰什叶派波斯）</a>与
    <a href="wiki/c-persia-buddhist.html">西域-波斯（佛教波斯残余）</a>。</p>
    <div class="quote">
      一条带过渡带的边界，好过一堵墙：伊斯兰文明止于伊朗，河中为双影响过渡带，
      更东即西域佛教带。
      <cite>用户裁定 P1 + P5</cite>
    </div>
  </div>
</div>
"""]

    body.append('<h2>精选词条</h2>')
    for label, ids in featured:
        body.append(f'<h3>{H.esc(label)}</h3><div class="pill-row">{pick(ids)}</div>')

    if doc_html:
        body.append('<h2>精选文献</h2><div class="pill-row">' + doc_html +
                    '<a class="pill gold" href="wiki/index.html">全部文献 →</a></div>')

    body.append('<h2>按类型浏览</h2><div class="entries">')
    for key, label, ico, desc in GROUPS:
        n = counts.get(key, 0)
        body.append(
            f'<a class="entry" href="wiki/list-{key}.html"><span class="ico">{ico}</span>'
            f'<span class="n">{n}</span><h3>{H.esc(label)}</h3><p>{H.esc(desc)}</p></a>')
    body.append('</div>')

    body.append(f"""
<h2>关于本知识库</h2>
<div class="card">
<p>本库把五份散文体设定集（<code>S0</code>–<code>S4</code>）转成<b>可校验、可检索、可继续扩写</b>的
结构化知识库：{n_nodes} 个实体节点、{n_edges} 条关系边、{counts['events']} 个事件节点。</p>
<p>索引层把同一实体在不同文档中的重复记载整合为单条并标记 <code>S5</code>：
原始 {raw_index} 条索引去重为 {n_ent_index} 个实体条目 + 81 个章节。</p>
<p><code>S*</code> 是<b>仿真文献层</b>：依据设定生成的历史文献、日记、书信与演讲，
用于呈现已确立的设定，<b>不新增设定</b>。</p>
<p class="legend">导航：<a href="index.html">索引</a> ／
<a href="wiki/index.html">历史文献</a> ／ <a href="timeline.html">时间轴</a> ／
<a href="index.html#sources">出处代号</a></p>
</div>
</main>
""")

    html_out = H.page("泛德意志的欧洲 · 架空世界设定知识库", "".join(body), active="home")
    with open(os.path.join(DOCS, "home.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html_out)
    print(f"  home.html：主页（{len(GROUPS)} 个类型入口，{len(years)} 个时间轴节点，{len(doc_pick)} 篇文献精选）")



# ==================================================================
# 2d. Markdown 文档 → HTML
# ==================================================================
def build_docs_html():
    made = MD.build_md_pages(DOCS, WIKI, H)
    idx = MD.build_md_index(DOCS, WIKI, made, H)
    print(f"  wiki/：{len(made)} 个文档页 + 文档中心 1 页")
    return made



# ==================================================================
# 2e. 分类型清单页（替换主页「按类型浏览」的索引锚点）
# ==================================================================
LISTING_TYPES = _LT.LISTING_TYPES


def build_listings():
    """为每个实体类型生成独立清单页，供主页「按类型浏览」指向。"""
    made = []
    for key, label, ico, desc in LISTING_TYPES:
        items = [e for e in ENT["entities"] if e.get("_group") == key]
        if not items:
            continue
        items.sort(key=lambda x: (x.get("name_zh") or x.get("zh") or x.get("id")))

        cards = []
        for x in items:
            eid = x["id"]
            nm = x.get("name_zh") or x.get("zh") or eid
            ov = x.get("overview") or x.get("summary") or ""
            ov = re.sub(r"\s+", " ", str(ov)).strip()
            if len(ov) > 150:
                ov = ov[:150] + "…"
            st = x.get("status") or ""
            badges = H.tag(st, H.STATUS_CLASS.get(st, ""))
            if x.get("type") == "COUNTRY" and x.get("time_span"):
                badges += H.tag(re.sub(r"\s+", " ", str(x["time_span"]))[:34])
            cards.append(
                f'<a class="entry" href="{slug(eid)}.html">'
                f'<h3>{H.esc(nm)}</h3>'
                f'<div style="margin:4px 0 6px">{badges}</div>'
                f'<p>{H.inline_md(H.esc(ov)) if ov else "（尚无概述）"}</p></a>')

        others = "".join(
            f'<a class="chip{" on" if k2 == key else ""}" href="list-{k2}.html">{i2} {H.esc(l2)}</a>'
            for k2, l2, i2, _d in LISTING_TYPES)

        body = [f"""
<header><div class="hdr">
<h1>{ico} {H.esc(label)}<span class="sub">共 {len(items)} 条</span></h1>
<nav class="crumbs"><a href="../home.html">主页</a> ／ <a href="../index.html">索引</a> ／
<a href="docs-index.html">文档</a> ／ 分类清单</nav></div></header>
<main>
<div class="card">
<span class="kindbadge">分类型清单</span>{H.esc(desc)}
<div class="pill-row" style="margin-top:10px">{others}</div>
<div style="margin-top:8px"><a href="../index.html#{key}">→ 在设定集索引中检索本类</a></div>
</div>
<div class="entries">
{"".join(cards)}
</div>
</main>
"""]
        page = H.page(f"{label} · 分类清单 · 泛德意志的欧洲", "".join(body),
                      base="../", active="index")
        with open(os.path.join(WIKI, f"list-{key}.html"), "w", encoding="utf-8",
                  newline="\n") as f:
            f.write(page)
        made.append((key, label, ico, len(items)))

    print(f"  wiki/：{len(made)} 个分类清单页（" +
          "、".join(f"{l} {n}" for _k, l, _i, n in made) + "）")
    return made


# ==================================================================
# 3. 交互式时间轴
# ==================================================================
def build_timeline():
    ev = []
    for r in TBL["timeline"]["rows"]:
        ev.append({
            "id": r["id"], "year": r["year"], "year_text": r["year_text"],
            "title": r["event_zh"], "epoch": r.get("epoch", ""),
            "region": r.get("region", ""),
            "countries": r.get("countries") or [],
            "persons": r.get("persons") or [],
            "result": r.get("result") or "",
            "causes": r.get("causes") or [], "effects": r.get("effects") or [],
            "war": r.get("war_id"), "treaty": r.get("treaty_id"),
            "significance": r.get("significance") or "",
            "status": r["status"], "src": r["src"],
            # 关键修正：词条页位于 docs/wiki/，而本页位于 docs/，
            # 链接必须带 wiki/ 前缀，否则浏览器会去 docs/ 下找文件而报「找不到」。
            "href": "wiki/" + wiki_href(r["id"]),
        })
    causal = [{"from": e["from"], "to": e["to"], "kind": e["kind"], "label": e["label"]}
              for e in EDGES if e["kind"] in ("CAUSES", "RESULTS_IN")]
    epochs = list(dict.fromkeys(x["epoch"] for x in ev))
    axis = TBL["timeline"].get("axis_nodes", [])
    payload = {"events": ev, "causal": causal, "epochs": epochs, "axis": axis,
               "min": min(x["year"] for x in ev), "max": max(x["year"] for x in ev)}

    body = ["""
<header><div class="hdr">
<h1>泛德意志的欧洲 · <span style="color:var(--accent)">交互式时间轴</span>
<span class="sub">横轴＝时间　纵轴＝地域／宗教／文化／制度／军事</span></h1>
<nav class="crumbs"><a href="index.html">索引</a> ／ <a href="index.html#wiki">百科词条</a> ／
<a href="wiki/index.html">历史文献</a> ／ <a href="#acc">事件年表</a></nav></div></header>
<main>
<div class="card">
<div class="legend">
时间范围 <b id="rg"></b>　｜　事件 <b id="cnt"></b> 个　｜　当前视角
<b id="modev">地域</b>　｜　把鼠标移到方块上可看事件，点击展开因果链
</div>
<input class="scrub" id="from" type="range" min="700" max="2000" value="700">
<input class="scrub" id="to" type="range" min="700" max="2000" value="2000">
<div style="margin-top:12px">
<label class="legend" for="mode">纵轴视角：</label>
<select id="mode">
<option value="region">地域 · 西欧／中欧／东欧／南欧·地中海／不列颠／北欧／近东·北非／亚洲</option>
<option value="religion">宗教 · 天主教／路德宗／加尔文宗／胡斯派／阿尔卑斯福音派／东正教／伊斯兰／佛教·萨满·长生天</option>
<option value="culture">文化 · 语言正字法／学术教育／艺术音乐／文献编纂</option>
<option value="polity">制度 · 王朝更替／宪制条约／政体变革／国际体系</option>
<option value="conflict">军事 · 战争／革命起义／迫害流散</option>
<option value="epoch">时代 · 按设定集原有分期</option>
</select>
</div>
<div class="chips" id="kinds" style="margin-top:9px"></div>
<div class="chips" id="epochs" style="margin-top:4px"></div>
</div>
<div class="tl-wrap"><div class="tl-holder" id="chart"></div></div>
<h2 id="acc">事件年表</h2>
<div id="acc-list"></div>
<h2>因果链</h2>
<div id="causal" class="legend">点击上方任意事件方块或年表中的事件，即可展开其前因与后果。</div>
</main>
<div id="tip"></div>
"""]

    js = f"""
<script>
const D = {json.dumps(payload, ensure_ascii=False)};
const EV = {{}}; D.events.forEach(e => EV[e.id]=e);

/* ============ 分类规则：地域 / 宗教 / 文化 / 制度 / 军事 ============ */
const RULES = {{
  region: [
    ['不列颠',      ['不列颠','英格兰','伦敦','爱尔兰','苏格兰','威尔士','英联邦','蒙福尔','金雀花','盎格鲁']],
    ['近东·北非',   ['近东','黎凡特','叙利亚','埃及','阿拉伯','马格里布','北非','十字军','马穆鲁克','阿尤布','法蒂玛','奥斯曼','安纳托利亚','君士坦丁堡','海峡','波斯','伊朗','两河','巴格达','汉志','麦加','麦地那','科尔多瓦','穆瓦希德','收复失地']],
    ['亚洲',        ['亚洲','西域','蒙古','金帐','罗斯兀鲁思','基辅王国','白罗斯','中国','西藏','敦煌','龟兹','于阗','吐鲁番','东洲','长生天','萨满','撒马尔罕','布哈拉','呼罗珊']],
    ['南欧·地中海', ['意大利','罗马','伦巴底','威尼托','皮埃蒙特','那不勒斯','米兰','托斯卡纳','北意大利','教皇','地中海','西西里']],
    ['东欧',        ['波兰','波西米亚','摩拉维亚','西里西亚','克罗地亚','斯洛文尼亚','布拉格','维也纳','奥地利','施蒂利亚','蒂罗尔','卡林西亚','布雷斯劳','波森','但泽']],
    ['北欧',        ['丹麦','挪威','瑞典','北欧']],
    ['西欧',        ['法兰克','帕里斯','雷姆斯','香槟','勃艮第','洛林','诺曼底','布列塔尼','弗兰登','法兰西岛','奥克','图卢兹','普罗旺斯','多菲内','伊比利亚','卡斯蒂利亚','阿拉贡','葡萄牙','托莱多','鲁安','南滕']],
    ['中欧',        ['德意志','普鲁士','萨克森','巴伐利亚','勃兰登堡','汉萨','莱茵','威斯特法伦','美因茨','黑森','图林根','阿尔萨斯','瑞士','低地','尼德兰','阿姆斯特丹','汉诺威','汉堡','不来梅','法兰克福','斯特拉斯堡']],
  ],
  religion: [
    ['天主教',            ['天主教','教皇','教宗','圣母','修道院','本笃','克吕尼','神学院','枢机','黎塞留','封圣','雷姆斯圣母']],
    ['阿尔卑斯福音派',    ['阿尔卑斯福音','南德意志新教','十字架下的喜悦','有节制的喜乐','巴伐利亚','蒂罗尔','施蒂利亚','伦巴底新教']],
    ['胡斯派',            ['胡斯','波西米亚福音','伯利恒礼拜堂','布拉格']],
    ['加尔文宗',          ['加尔文','改革宗','长老制','日内瓦','苏黎世','低地','尼德兰','瑞士德语']],
    ['路德宗',            ['路德','路德宗','维滕堡','九十五条','北德意志','萨克森','勃兰登堡','丹麦','瑞典']],
    ['东正教',            ['东正教','正教','基辅','古罗斯','白罗斯','君士坦丁堡','拜占庭','东正']],
    ['伊斯兰',            ['伊斯兰','穆斯林','哈里发','苏丹','逊尼','什叶','科尔多瓦','穆瓦希德','法蒂玛','阿尤布','马穆鲁克','阿拔斯','奥斯曼','波斯','伊朗','阿拉伯','埃及','叙利亚','马格里布','安纳托利亚']],
    ['佛教·萨满·长生天', ['佛教','佛','萨满','长生天','腾格里','西域','敦煌','龟兹','于阗','吐鲁番','蒙古','西藏','东洲','犍陀罗']],
    ['宗教改革与战争',    ['宗教改革','宗教战争','三十年','维也纳和约','教产','信仰','新教联盟','天主教联盟','政教分离','教会','皈依']],
  ],
  culture: [
    ['语言·正字法',    ['语言','正字法','共同体德语','标准语','法兰克语','英语','奥克语','方言','宫廷语','语言会议','术语','称谓','译名','罗曼化','正统']],
    ['学术·教育',      ['大学','学院','学术','科学','物理','数学','化学','医学','法学','哲学','东方学','理工','出版','图书馆','知识分子','人才','学人','哥廷根','莱比锡']],
    ['艺术·音乐·建筑', ['艺术','音乐','歌剧','巴洛克','教堂','建筑','咖啡馆','甜点','啤酒节','斯卡拉','美学院','绘画','文学','宫廷古典主义','沙龙']],
    ['文献·编纂',      ['宪章','和约','条约','条款','法典','档案','文献','编纂','纪年','注记','敕令','诏书']],
  ],
  polity: [
    ['王朝更替',    ['王朝','世系','继承','绝嗣','登基','加冕','复辟','废王','谱系','联姻','王冠','君主','国王','皇帝','哈里发国','苏丹国']],
    ['宪制·条约',   ['宪章','和约','条约','宪法','权利宪章','宪政','议会','选举','选侯','帝国议会','法案','三重加冕','双王冠','双轨制']],
    ['政体变革',    ['共和','帝国','联邦','单一制','总统制','多党','政体','民主化','联邦化','革命','改革','集权','自治','正常化']],
    ['国际体系',    ['同盟','协约','中欧协定','均势','六极','多极','外交','中立','殖民地','国际','英联邦','欧盟']],
  ],
  conflict: [
    ['战争',      ['战争','大战','一战','二战','三十年','奥法','收复失地','十字军','蒙古西征','入侵','战役','会战','联军','出征']],
    ['革命·起义', ['革命','起义','农民战争','暴动','叛乱','独立','镇压','政变']],
    ['迫害·流散', ['屠杀','迫害','驱逐','迁移','压制','流散','流亡','迁往','赶去','禁止']],
  ],
}};
const CHRONO = ['13世纪','14世纪','15—16世纪','17世纪','18世纪','19世纪','20世纪','长时段','宗教史长时段','亚洲线'];
const MODES = {{
  region:  {{label:'地域', order:['西欧','中欧','东欧','南欧·地中海','不列颠','北欧','近东·北非','亚洲']}},
  religion:{{label:'宗教', order:['天主教','路德宗','加尔文宗','胡斯派','阿尔卑斯福音派','东正教','伊斯兰','佛教·萨满·长生天','宗教改革与战争']}},
  culture: {{label:'文化', order:['语言·正字法','学术·教育','艺术·音乐·建筑','文献·编纂']}},
  polity:  {{label:'制度', order:['王朝更替','宪制·条约','政体变革','国际体系']}},
  conflict:{{label:'军事', order:['战争','革命·起义','迫害·流散']}},
}};
function classify(e, mode) {{
  const text = e.title+' '+e.region+' '+e.epoch+' '+e.result+' '+(e.significance||'')+' '
             + e.countries.join(' ')+' '+e.persons.join(' ');
  const rules = RULES[mode] || [];
  for (let i=0;i<rules.length;i++) {{
    const lane=rules[i][0], kws=rules[i][1];
    for (let j=0;j<kws.length;j++) if (text.indexOf(kws[j]) >= 0) return lane;
  }}
  return '其他';
}}
function chronoLane(e) {{
  const ep = e.epoch||'';
  if (ep.indexOf('宗教史')>=0) return '宗教史长时段';
  if (ep.indexOf('亚洲')>=0 || ep.indexOf('蒙古')>=0) return '亚洲线';
  const y=e.year;
  if (y<1300) return '13世纪';
  if (y<1400) return '14世纪';
  if (y<1600) return '15—16世纪';
  if (y<1700) return '17世纪';
  if (y<1800) return '18世纪';
  if (y<1900) return '19世纪';
  if (y<2000) return '20世纪';
  return '长时段';
}}
function laneOf(e, mode) {{ return mode==='epoch' ? chronoLane(e) : classify(e, mode); }}
function laneOrder(mode) {{
  if (mode==='epoch') return CHRONO.slice();
  return ((MODES[mode]||{{order:[]}}).order).slice();
}}

const activeEpochs=new Set(), activeLanes=new Set();
const fromEl=document.getElementById('from'), toEl=document.getElementById('to');
let MODE='region';
function fmt(y){{ return y<0? (-y)+' BC' : y; }}
function visible(){{
  const f=+fromEl.value, t=+toEl.value;
  return D.events.filter(e=>e.year>=f && e.year<=t
     && (!activeEpochs.size || activeEpochs.has(e.epoch))
     && (!activeLanes.size || activeLanes.has(laneOf(e, MODE))));
}}
document.getElementById('mode').onchange=function(){{
  MODE=this.value;
  activeLanes.clear();
  document.getElementById('modev').textContent=(MODES[MODE]||{{label:'时代'}}).label;
  buildLaneChips(); draw();
}};
const epEl=document.getElementById('epochs');
D.epochs.forEach(function(ep){{
  const c=document.createElement('div'); c.className='chip'; c.textContent=ep;
  c.onclick=function(){{ activeEpochs.has(ep)?activeEpochs.delete(ep):activeEpochs.add(ep);
                        c.classList.toggle('on'); draw(); }};
  epEl.appendChild(c);
}});
const lnEl=document.getElementById('kinds');
function buildLaneChips(){{
  lnEl.innerHTML='';
  const order=laneOrder(MODE);
  const present={{}};
  D.events.forEach(function(e){{ present[laneOf(e,MODE)]=1; }});
  Object.keys(present).forEach(function(l){{ if(order.indexOf(l)<0) order.push(l); }});
  order.forEach(function(l){{
    if(!present[l]) return;
    const c=document.createElement('div'); c.className='chip'; c.textContent=l;
    c.onclick=function(){{ activeLanes.has(l)?activeLanes.delete(l):activeLanes.add(l);
                          c.classList.toggle('on'); draw(); }};
    lnEl.appendChild(c);
  }});
}}
fromEl.oninput=toEl.oninput=draw;

function draw(){{
  const f=+fromEl.value, t=+toEl.value;
  document.getElementById('rg').textContent=fmt(f)+' — '+fmt(t);
  const rows=visible();
  document.getElementById('cnt').textContent=rows.length;
  const span=Math.max(1,t-f);
  const chart=document.getElementById('chart');
  let html='<div class="tl-axis">';
  const step=Math.max(25, Math.round(span/10/25)*25);
  for(let y=Math.ceil(f/step)*step; y<=t; y+=step){{
    html+='<div class="tl-tick" style="left:'+((y-f)/span*100)+'%"><span>'+fmt(y)+'</span></div>';
  }}
  html+='</div>';
  const byLane={{}};
  rows.forEach(function(e){{ const l=laneOf(e,MODE); (byLane[l]=byLane[l]||[]).push(e); }});
  const order=laneOrder(MODE);
  Object.keys(byLane).forEach(function(l){{ if(order.indexOf(l)<0) order.push(l); }});
  order.forEach(function(l){{
    const list=byLane[l]; if(!list) return;
    list.sort(function(a,b){{return a.year-b.year;}});
    const clusters=[];
    const tol=Math.max(2, span*0.012);
    list.forEach(function(e){{
      const last=clusters[clusters.length-1];
      if(last && e.year-last.year<=tol) {{ last.items.push(e); last.year=(last.year+e.year)/2; }}
      else clusters.push({{year:e.year, items:[e]}});
    }});
    html+='<div class="tl-lane"><div class="tl-lane-label">'+l+'</div>';
    clusters.forEach(function(c){{
      const p=(c.year-f)/span*100;
      const w=Math.max(0.8, Math.min(26, 1600/span));
      const lbl = c.items.length>1 ? ('● '+c.items.length) : c.items[0].title;
      let tt='';
      c.items.forEach(function(x){{ tt += x.year_text+' '+x.title+' / '; }});
      html+='<div class="tl-ev" style="left:'+p+'%;width:'+w+'%" '
          + 'data-cluster="'+c.items.map(function(x){{return x.id;}}).join(',')+'" '
          + 'title="'+esc(tt)+'"><span>'+esc(lbl)+'</span></div>';
    }});
    html+='</div>';
  }});
  chart.innerHTML=html;
  const blocks=chart.querySelectorAll('.tl-ev');
  for(let i=0;i<blocks.length;i++){{
    blocks[i].onclick=function(){{
      const ids=(this.dataset.cluster||'').split(',').filter(Boolean);
      if(ids.length===1) show(ids[0], this); else showCluster(ids, this);
    }};
  }}
  document.getElementById('acc-list').innerHTML =
    '<table><tr><th>年份</th><th>事件</th><th>国家</th><th>结果</th><th>状态</th></tr>'
    + rows.slice().sort(function(a,b){{return a.year-b.year;}}).map(function(e){{
        return '<tr><td>'+esc(e.year_text)+'</td>'
        +'<td><a href="'+e.href+'">'+esc(e.title)+'</a></td>'
        +'<td>'+esc(e.countries.join('、'))+'</td>'
        +'<td>'+esc(e.result.slice(0,90))+(e.result.length>90?'…':'')+'</td>'
        +'<td>'+esc(e.status)+'</td></tr>';
      }}).join('')+'</table>';
}}
function esc(s){{return (s==null?'':String(s)).replace(/[&<>"]/g,function(m){{
  return ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[m];}});}}
function nm(id){{ return EV[id]? EV[id].title : id; }}
function place(el, w){{
  const tip=document.getElementById('tip');
  const r=el.getBoundingClientRect();
  tip.style.left=Math.min(window.innerWidth-(w||400), Math.max(10, r.left))+'px';
  tip.style.top=Math.min(window.innerHeight-300, r.bottom+8)+'px';
  tip.style.display='block';
}}
function show(id, el){{
  const e=EV[id]; if(!e) return;
  let causes='', effs='';
  (e.causes||[]).forEach(function(c){{ causes+='<li>'+esc(nm(c))+'</li>'; }});
  (e.effects||[]).forEach(function(c){{ effs+='<li>'+esc(nm(c))+'</li>'; }});
  document.getElementById('tip').innerHTML='<h4>'+esc(e.year_text)+'　'+esc(e.title)+'</h4>'
   +'<div class="legend">'+esc(e.epoch)+' ｜ '+esc(e.region)+' ｜ '+esc(e.status)+' ｜ '+esc(e.src.join('、'))+'</div>'
   +(e.countries.length?'<div><b>国家：</b>'+esc(e.countries.join('、'))+'</div>':'')
   +(e.persons.length?'<div><b>人物：</b>'+esc(e.persons.join('、'))+'</div>':'')
   +'<div><b>结果：</b>'+esc(e.result)+'</div>'
   +(causes?'<div><b>前因：</b><ul>'+causes+'</ul></div>':'')
   +(effs?'<div><b>后果：</b><ul>'+effs+'</ul></div>':'')
   +'<div style="margin-top:6px"><a href="'+e.href+'">打开完整词条 →</a></div>';
  place(el, 400);
}}
function showCluster(ids, el){{
  let items='';
  ids.forEach(function(id){{ const e=EV[id];
    items+='<li><a href="'+e.href+'">'+esc(e.year_text)+'　'+esc(e.title)+'</a></li>'; }});
  document.getElementById('tip').innerHTML='<h4>该处共 '+ids.length+' 个事件</h4><ul>'+items+'</ul>';
  place(el, 420);
}}
document.addEventListener('click', function(ev){{
  const tip=document.getElementById('tip');
  if(!tip.contains(ev.target) && !ev.target.closest('.tl-ev')) tip.style.display='none';
}});
buildLaneChips();
draw();
</script>
"""

    html_out = H.page("交互式时间轴 · 泛德意志的欧洲", "\n".join(body), extra_js=js, active="timeline")
    with open(os.path.join(DOCS, "timeline.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html_out)

    # 统计各视角的泳道覆盖，便于校验
    import html as _h
    n_modes = 5
    print(f"  timeline.html：{len(ev)} 个事件节点，{len(causal)} 条因果边，"
          f"{n_modes}+1 个纵轴视角（地域/宗教/文化/制度/军事/时代）")


if __name__ == "__main__":
    print("== 生成 HTML 站点 ==")
    build_index()
    build_wiki()
    build_docs()
    build_docs_html()
    build_listings()
    build_timeline()
    build_home()
    print("完成。")
