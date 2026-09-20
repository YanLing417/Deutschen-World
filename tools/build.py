# -*- coding: utf-8 -*-
"""
历史设定集知识工程 —— 产物生成器
运行： python tools/build.py
输出：
  data/*.json        机器可读产物（实体总表 / 图数据库 / 四表 / 对照表 / 转写表 / 索引 / 三态清单）
  docs/*.md          人读产物（与 JSON 同源）
  docs/index.html    离线可检索的设定集索引
"""
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, HERE)

import kb_data as D  # noqa: E402

# ---------------------------------------------------------------- 合并补全层
# kb_extra.py 承载「一致性检查与补全」任务新增的内容（伊比利亚线、伊斯兰世界线、
# 未具名/新增人物）。此处合并进主数据层，使所有下游逻辑无需区分来源。
try:
    import kb_extra as X  # noqa: E402
except ImportError:
    X = None

try:
    import kb_decisions_content as DC  # noqa: E402
except ImportError:
    DC = None

# 分期政治体层：把同一地区不同时期的国名拆成独立词条（用户 2026 裁定）
try:
    import kb_periods as PER  # noqa: E402
except ImportError:
    PER = None

try:
    import kb_artifacts as AR  # noqa: E402
except ImportError:
    AR = None

if X is not None:
    _MERGE = [
        ("COUNTRIES", "COUNTRIES"), ("DYNASTIES", "DYNASTIES"), ("PEOPLE", "PEOPLE"),
        ("EVENTS", "EVENTS"), ("WARS", "WARS"), ("PLACES", "PLACES"),
        ("RELATIONS", "RELATIONS"),
    ]
    for dst, src in _MERGE:
        extra = getattr(X, src, None)
        if extra:
            getattr(D, dst).extend(extra)

# 分期政治体（伊比利亚系 / 法兰克系 / 德意志系）
if PER is not None:
    D.COUNTRIES.extend(PER.COUNTRIES)
    D.COUNTRIES.extend(PER.FRANKISH_COUNTRIES)
    D.DYNASTIES.extend(PER.DYNASTIES)
    D.PLACES.extend(PER.PLACES)
    D.RELATIONS.extend(PER.RELATIONS)

# 伊比利亚共和序列细分（第三/第四/第五共和国 + 第二帝国 + 被占领期）
try:
    import kb_iberia_rep as IBR  # noqa: E402
except ImportError:
    IBR = None
if IBR is not None:
    D.COUNTRIES.extend(IBR.IBERIAN_REPUBLICS)
    D.COUNTRIES.extend(IBR.IBERIAN_2EMP)
    D.EVENTS.extend(IBR.EVENTS)
    D.RELATIONS.extend(IBR.REPUBLIC_RELATIONS)

# 全球机构与建筑群
try:
    import kb_institutions as INS  # noqa: E402
except ImportError:
    INS = None
if INS is not None:
    D.ORGANIZATIONS.extend(INS.ORGANIZATIONS)
    D.PLACES.extend(INS.PLACES)

# 历史物品留存
if AR is not None:
    D.ARTIFACTS = list(getattr(D, 'ARTIFACTS', [])) + list(AR.ARTIFACTS)

# 留存物收藏机构（补建 + AR_* → 机构 ID 对应）
try:
    import kb_artifacts_repo as ARR  # noqa: E402
except ImportError:
    ARR = None
if ARR is not None:
    D.ORGANIZATIONS.extend(ARR.ORGANIZATIONS)
    for _a in getattr(D, 'ARTIFACTS', []) or []:
        _rid = ARR.REPO_MAP.get(_a["id"])
        if _rid:
            _a["repo_id"] = _rid

# 裁定驱动的新增内容（2026 轮）
if DC is not None:
    D.COUNTRIES.extend(DC.COUNTRIES)
    D.COUNTRIES.extend(DC.NEAR_EAST_20C)
    D.PEOPLE.extend(DC.MOUNTFORT_MONARCHS)
    D.PLACES.extend(DC.PLACES)

    # P10：伊比利亚八大区改以山系/水系命名
    for _sb in D.SUBDIVISIONS:
        if _sb["id"] != "SB_IBERIA":
            continue
        _sb["units"] = [
            {"name_zh": r["name_zh"], "name_de": r["name_de"],
             "capital": r["capital"], "note": r["note"]}
            for r in DC.IBERIAN_REGIONS
        ]
        _sb["level_system"] = (
            "高度中央集权的单一制：大区很大、数量少，共八个；省份才承载传统民族/历史地区"
            "（Galicia、Catalonia、Portugal、Andalusia 等下沉为省/次级行政区）。"
            "八大区以山系/水系命名——这从语义上切断了与民族身份的关联，"
            "彻底实现 S2「不能形成加泰罗尼亚邦、葡萄牙邦、摩洛哥邦」的设计意图。"
            "北非与伊比利亚半岛在法律上属于同一个国家行政体系，不设特殊宪制地位。"
        )
        _sb["naming_basis"] = "用户本轮裁定（P10）：保留八区框架但以山系/水系重新命名"
        _sb["status"] = "已确定"

    # P13：英联邦成员名单
    for _o in D.ORGANIZATIONS:
        if _o["id"] == "O_COMMONWEALTH":
            _o["members"] = [m["name_zh"] for m in DC.COMMONWEALTH_MEMBERS]
            _o["function"] = (
                "语言、文化与商业共同体；明确**无共同防务条款**。"
                "成员为若干移民自治领与少数岛屿领地，远不如现实庞大。"
                "不列颠的六极地位依靠工业、金融、海军残余与语言文化网络，而非领土规模。"
            )
            _o["status"] = "已确定"
            _o["notes"] = "用户本轮裁定（P13）：列 5—8 个具名成员，明确「无共同防务条款」。"
            break

    # P37：美国社会主义党的两阶段名称
    for _p in D.PARTIES:
        if _p["id"] == "PT_ASOC":
            _p["name_zh"] = "美国社会民主党（前身为美国社会党）"
            _p["name_en"] = "Social Democratic Party of America (SDPA)"
            _p["name_de"] = "Sozialdemokratische Partei Amerikas (SDPA)"
            _p["name_history"] = DC.US_PARTY_STAGES
            _p["status"] = "已确定"
            _p["notes"] = (
                "用户本轮裁定（P37）：分两阶段——早期称 Socialist Party of America（美国社会党），"
                "1930 年代后改组为 Social Democratic Party of America（美国社会民主党）。"
                "名称演变本身即 S2 所记「社会党吸收了大量原本可能支持共产主义/社会主义运动的选民」"
                "这一过程的结果。与不列颠 SDP、德意志 DSP、法兰克 FSP、伊比利亚 PSI 同构（S3）。"
            )
            break

# 「俄罗斯」已按 S4 要求废弃，统一替换为「罗斯兀鲁思」。
# 保留 S4 原文说明其在 source/ 中的废弃记录（见 CONFLICTS X07）。
def _deprecate_ru_name(obj):
    if isinstance(obj, str):
        return obj.replace("俄罗斯帝国", "罗斯兀鲁思").replace("俄罗斯", "罗斯兀鲁思")
    if isinstance(obj, list):
        return [_deprecate_ru_name(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _deprecate_ru_name(v) for k, v in obj.items()}
    return obj


for _attr in ("COUNTRIES", "DYNASTIES", "PEOPLE", "EVENTS", "WARS", "TREATIES",
              "RELIGIONS", "LANGUAGES", "SUBDIVISIONS", "PARTIES", "ORGANIZATIONS",
              "RELATIONS", "PLACES", "GLOSSARY"):
    _v = getattr(D, _attr, None)
    if isinstance(_v, list):
        setattr(D, _attr, _deprecate_ru_name(_v))

# 反向补全：国家声明的 religion_id 自动并入该宗教条目的 polity 列表，
# 避免「国家说自己是某教」而「该教没把国家列入」的单向漂移。
for _c in D.COUNTRIES:
    _rid = _c.get("religion_id")
    if not _rid:
        continue
    for _r in D.RELIGIONS:
        if _r["id"] != _rid:
            continue
        _pol = _r.setdefault("polity", [])
        if _c["id"] not in _pol:
            _pol.append(_c["id"])
        break

# 概述补全：为缺少 overview/summary 的实体生成说明性概述
try:
    import overview_filler as OF  # noqa: E402
    _of = OF.fill(D)
    if _of:
        print('   概述补全：%d 条 %s' % (sum(_of.values()), _of))
except ImportError:
    pass

# 地名与横轴指标在数据层使用紧凑写法，此处统一补齐 status / src 字段，
# 必须早于实体注册表构建（REG）。
for _p in D.PLACES:
    _p.setdefault("status", "已确定")
    _p.setdefault("src", ["S0"])
for _a in D.AXIS_INDICATORS:
    _a.setdefault("status", "已确定")
    _a.setdefault("src", ["S0"])

os.makedirs(DATA, exist_ok=True)
os.makedirs(DOCS, exist_ok=True)

ID_RE = re.compile(r"\b((?:PE|D|C|R|L|P|E|W|T|O|PT|SB|AX|G|REL|X|M)_[A-Z0-9_]+)\b")

STATUS_ORDER = ["已确定", "待定", "修正"]


# ---------------------------------------------------------------- 工具
def wjson(name, obj):
    p = os.path.join(DATA, name)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return p


def wtext(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        cells = []
        for c in r:
            s = "" if c is None else str(c)
            s = s.replace("|", "\\|").replace("\n", "<br>")
            cells.append(s)
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def j(v):
    """把 list/dict 压成可读字符串"""
    if v is None or v == [] or v == {}:
        return None
    if isinstance(v, list):
        parts = []
        for x in v:
            if isinstance(x, dict):
                parts.append("；".join(f"{k}:{vv}" for k, vv in x.items()))
            else:
                parts.append(str(x))
        return "；".join(parts)
    if isinstance(v, dict):
        return "；".join(f"{k}:{vv}" for k, vv in v.items())
    return str(v)


# ---------------------------------------------------------------- 实体注册表
def build_registry():
    reg = OrderedDict()

    def add(eid, etype, obj):
        if eid in reg:
            raise SystemExit(f"重复 ID: {eid}")
        reg[eid] = {
            "id": eid, "type": etype,
            "name_zh": (obj.get("name_zh") or obj.get("zh") or obj.get("name")
                        or obj.get("name_short") or eid),
            "name_de": obj.get("name_de") or obj.get("de"),
            "name_en": obj.get("name_en") or obj.get("en"),
            "status": obj.get("status"), "src": obj.get("src", []),
        }

    for c in D.COUNTRIES:
        add(c["id"], "COUNTRY", c)
    for c in D.DYNASTIES:
        add(c["id"], "DYNASTY", c)
    for c in D.PEOPLE:
        add(c["id"], "PERSON", c)
    for c in D.WARS:
        add(c["id"], "WAR", c)
    for c in D.TREATIES:
        add(c["id"], "TREATY", c)
    for c in D.RELIGIONS:
        add(c["id"], "RELIGION", c)
    for c in D.LANGUAGES:
        add(c["id"], "LANGUAGE", c)
    for c in D.SUBDIVISIONS:
        add(c["id"], "SUBDIVISION", c)
    for c in D.PARTIES:
        add(c["id"], "PARTY", c)
    for c in D.ORGANIZATIONS:
        add(c["id"], "ORGANIZATION", c)
    for c in D.EVENTS:
        add(c["id"], "EVENT", c)
    for c in D.PLACES:
        add(c["id"], "PLACE", c)
    for c in D.AXIS_INDICATORS:
        add(c["id"], "AXIS_INDICATOR", c)
    for c in getattr(D, "ARTIFACTS", []) or []:
        add(c["id"], "ARTIFACT", c)
    return reg


REG = build_registry()
KNOWN_IDS = set(REG)


def extract_ids(value):
    """从任意嵌套结构中提取实体 ID"""
    found = []

    def walk(v):
        if isinstance(v, str):
            found.extend(ID_RE.findall(v))
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)

    walk(value)
    return found


# ---------------------------------------------------------------- 1. 实体总表
def build_entities():
    groups = [
        ("countries", "国家与政治实体", D.COUNTRIES),
        ("dynasties", "王朝与家族", D.DYNASTIES),
        ("people", "人物", D.PEOPLE),
        ("events", "事件", D.EVENTS),
        ("places", "地点", D.PLACES),
        ("religions", "宗教", D.RELIGIONS),
        ("languages", "语言", D.LANGUAGES),
        ("wars", "战争", D.WARS),
        ("treaties", "条约与宪章", D.TREATIES),
        ("subdivisions", "行政区划", D.SUBDIVISIONS),
        ("parties", "政党", D.PARTIES),
        ("organizations", "机构与组织", D.ORGANIZATIONS),
        ("axis_indicators", "横轴指标", D.AXIS_INDICATORS),
        ("artifacts", "历史物品留存", getattr(D, "ARTIFACTS", [])),
    ]
    counts = {}
    status_counts = defaultdict(lambda: defaultdict(int))
    for key, _label, items in groups:
        counts[key] = len(items)
        for it in items:
            status_counts[key][it.get("status") or "（未标）"] += 1

    all_entities = []
    for key, label, items in groups:
        for it in items:
            rec = dict(it)
            rec["_group"] = key
            rec["_group_label"] = label
            rec["type"] = REG[it["id"]]["type"]
            all_entities.append(rec)

    doc = {
        "meta": D.META,
        "counts": counts,
        "total": sum(counts.values()),
        "status_matrix": {k: dict(v) for k, v in status_counts.items()},
        "entities": all_entities,
    }
    return doc


# ---------------------------------------------------------------- 2. 图数据库
def build_graph():
    nodes = []
    for eid, r in REG.items():
        nodes.append({
            "id": eid, "type": r["type"],
            "name_zh": r["name_zh"], "name_de": r["name_de"], "name_en": r["name_en"],
            "status": r["status"], "src": r["src"],
        })

    edges = []
    dangling = []
    for rel in D.RELATIONS:
        for side in ("from", "to"):
            t = rel[side]
            if t not in KNOWN_IDS:
                dangling.append({"relation": rel["id"], "side": side, "target": t})
        edges.append({
            "id": rel["id"], "domain": rel["domain"], "kind": rel["kind"],
            "from": rel["from"], "from_type": rel["from_type"],
            "to": rel["to"], "to_type": rel["to_type"],
            "label": rel["label"], "time": rel.get("time"),
            "status": rel["status"], "src": rel["src"],
        })

    # 由实体字段自动补边（家族成员、所属国、条约、战争等）
    auto = []

    def ae(kind, f, ft, t, tt, label, src, status):
        auto.append({
            "id": None, "domain": "自动补边", "kind": kind,
            "from": f, "from_type": ft, "to": t, "to_type": tt,
            "label": label, "time": None, "status": status, "src": src,
            "derived": True,
        })

    for c in D.COUNTRIES:
        for oid in c.get("orgs", []) or []:
            if oid in KNOWN_IDS:
                ae("HAS_INSTITUTION", c["id"], "COUNTRY", oid, "ORGANIZATION", "设有", c["src"], c["status"])
        for pid in c.get("parties", []) or []:
            if pid in KNOWN_IDS:
                ae("HAS_PARTY", c["id"], "COUNTRY", pid, "PARTY", "政党", c["src"], c["status"])
        for sid in c.get("subdivisions", []) or []:
            if sid in KNOWN_IDS:
                ae("HAS_SUBDIVISION", c["id"], "COUNTRY", sid, "SUBDIVISION", "行政区划", c["src"], c["status"])
        for wid in c.get("wars", []) or []:
            wid_clean = wid.split("（")[0].strip()
            if wid_clean in KNOWN_IDS:
                ae("PARTICIPATES_IN_WAR", c["id"], "COUNTRY", wid_clean, "WAR", "参战", c["src"], c["status"])
        for tid in c.get("treaties", []) or []:
            if tid in KNOWN_IDS:
                ae("SIGNED_TREATY", c["id"], "COUNTRY", tid, "TREATY", "缔约", c["src"], c["status"])
        if c.get("religion_id") in KNOWN_IDS:
            ae("RELIGIOUS_AFFILIATION", c["id"], "COUNTRY", c["religion_id"], "RELIGION", "国教/主流宗教", c["src"], c["status"])
        if c.get("language_id") in KNOWN_IDS:
            ae("OFFICIAL_LANGUAGE", c["id"], "COUNTRY", c["language_id"], "LANGUAGE", "官方/通用语言", c["src"], c["status"])
        if c.get("dynasty_id") and c["dynasty_id"] in KNOWN_IDS:
            ae("RULED_BY", c["id"], "COUNTRY", c["dynasty_id"], "DYNASTY", "统治王朝", c["src"], c["status"])

    for e in D.EVENTS:
        for cid in e.get("country_ids", []) or []:
            if cid in KNOWN_IDS:
                ae("EVENT_INVOLVES_COUNTRY", e["id"], "EVENT", cid, "COUNTRY", "涉及国家", e["src"], e["status"])
        for pid in e.get("persons", []) or []:
            if pid in KNOWN_IDS:
                ae("EVENT_INVOLVES_PERSON", e["id"], "EVENT", pid, "PERSON", "涉及人物", e["src"], e["status"])
        for key, kind in (("war_id", "EVENT_HAS_WAR"), ("treaty_id", "EVENT_HAS_TREATY")):
            tgt = e.get(key)
            if tgt and tgt in KNOWN_IDS:
                ae(kind, e["id"], "EVENT", tgt, "WAR" if key == "war_id" else "TREATY", "关联", e["src"], e["status"])
        for cid in e.get("causes", []) or []:
            if cid in KNOWN_IDS:
                ae("CAUSES", cid, "EVENT", e["id"], "EVENT", "前因", e["src"], e["status"])
        for cid in e.get("effects", []) or []:
            if cid in KNOWN_IDS:
                ae("RESULTS_IN", e["id"], "EVENT", cid, "EVENT", "后果", e["src"], e["status"])

    for w in D.WARS:
        for side_key, role in (("side_a", "A方"), ("side_b", "B方")):
            for cid in (w.get(side_key) or {}).get("country_ids", []) or []:
                if cid in KNOWN_IDS:
                    ae("WAR_INVOLVES", w["id"], "WAR", cid, "COUNTRY", role, w["src"], w["status"])
        if w.get("treaty_id") and w["treaty_id"] in KNOWN_IDS:
            ae("WAR_ENDS_WITH", w["id"], "WAR", w["treaty_id"], "TREATY", "结束条约", w["src"], w["status"])

    for p in D.PEOPLE:
        if p.get("dynasty_id") and p["dynasty_id"] in KNOWN_IDS:
            ae("DYNASTY_MEMBER", p["id"], "PERSON", p["dynasty_id"], "DYNASTY", "所属王朝", p["src"], p["status"])
        if p.get("country_id") and p["country_id"] in KNOWN_IDS:
            ae("SUBJECT_OF", p["id"], "PERSON", p["country_id"], "COUNTRY", "所属国家", p["src"], p["status"])

    for t in D.TREATIES:
        for p in t.get("parties", []) or []:
            for cid in ID_RE.findall(p):
                if cid in KNOWN_IDS:
                    ae("TREATY_PARTY", t["id"], "TREATY", cid, "COUNTRY", "缔约方", t["src"], t["status"])

    for d in D.DYNASTIES:
        for cid in d.get("polity", []) or []:
            if cid in KNOWN_IDS:
                ae("DYNASTY_RULES", d["id"], "DYNASTY", cid, "COUNTRY", "统治", d["src"], d["status"])
        for pid in d.get("members", []) or []:
            if pid in KNOWN_IDS:
                ae("DYNASTY_MEMBER", pid, "PERSON", d["id"], "DYNASTY", "家族成员", d["src"], d["status"])

    for r in D.RELIGIONS:
        for cid in r.get("polity", []) or []:
            if cid in KNOWN_IDS:
                ae("RELIGION_IN", r["id"], "RELIGION", cid, "COUNTRY", "信众所在", r["src"], r["status"])

    for o in D.ORGANIZATIONS:
        if o.get("country_id") and o["country_id"] in KNOWN_IDS:
            ae("LOCATED_IN", o["id"], "ORGANIZATION", o["country_id"], "COUNTRY", "所在国", o["src"], o["status"])

    for p in D.PARTIES:
        if p.get("country_id") and p["country_id"] in KNOWN_IDS:
            ae("PARTY_IN", p["id"], "PARTY", p["country_id"], "COUNTRY", "所在国", p["src"], p["status"])

    for s in D.SUBDIVISIONS:
        if s.get("country_id") and s["country_id"] in KNOWN_IDS:
            ae("SUBDIVISION_OF", s["id"], "SUBDIVISION", s["country_id"], "COUNTRY", "所属国", s["src"], s["status"])

    for pl in D.PLACES:
        if pl.get("country_id") and pl["country_id"] in KNOWN_IDS:
            ae("PLACE_IN", pl["id"], "PLACE", pl["country_id"], "COUNTRY", "所在地",
               pl.get("src", []), pl.get("status", "已确定"))

    # 历史物品留存：持有人 / 存放地 / 收藏机构
    for a in getattr(D, "ARTIFACTS", []) or []:
        a_src = a.get("src", [])
        a_st = a.get("status", "已确定")
        h = a.get("holder")
        if h in KNOWN_IDS:
            ae("HELD_BY", a["id"], "ARTIFACT", h, REG[h]["type"], "现存持有方",
               a_src, a_st)
        pid = a.get("place_id")
        if pid in KNOWN_IDS:
            ae("KEPT_IN", a["id"], "ARTIFACT", pid, REG[pid]["type"], "存放地",
               a_src, a_st)
        rid = a.get("repo_id")
        if rid in KNOWN_IDS:
            ae("KEPT_AT", a["id"], "ARTIFACT", rid, REG[rid]["type"], "收藏机构",
               a_src, a_st)

    # 全部边统一去重：同一 (kind, from, to) 只保留一条，人工定义的优先于自动补边；
    # 两条人工边重复时合并说明与出处。
    manual_seen = {}
    dedup_manual = []
    for e in edges:
        k = (e["kind"], e["from"], e["to"])
        if k in manual_seen:
            prev = manual_seen[k]
            if e["label"] and e["label"] not in prev["label"]:
                prev["label"] = prev["label"] + "；" + e["label"]
            for s in e["src"]:
                if s not in prev["src"]:
                    prev["src"].append(s)
            prev["merged_from"] = (prev.get("merged_from") or []) + [e["id"]]
            continue
        manual_seen[k] = e
        dedup_manual.append(e)
    edges = dedup_manual

    # 自动边去重（同 from/kind/to 只留一条），并跳过已有人工边的键
    seen = set(manual_seen.keys())
    dedup = []
    for e in auto:
        k = (e["kind"], e["from"], e["to"])
        if k in seen:
            continue
        seen.add(k)
        e["id"] = f"AUTO{len(dedup)+1:04d}"
        dedup.append(e)

    all_edges = edges + dedup

    # 分域视图
    def sub(kind_filter=None, domain_filter=None, exclude_domain=None):
        out = []
        for e in all_edges:
            if kind_filter and e["kind"] not in kind_filter:
                continue
            if domain_filter and e["domain"] != domain_filter:
                continue
            if exclude_domain and e["domain"] == exclude_domain:
                continue
            out.append(e)
        return out

    FAMILY_KINDS = {"PARENT_OF", "CHILD_OF", "SPOUSE_OF", "SIBLING_OF",
                    "DYNASTY_MEMBER", "SUCCEEDED_BY", "CLAIMANT_TO", "RIVAL_OF",
                    "DYNASTY_RULES", "RULED_BY", "DYNASTY_ENDS", "DYNASTY_RESTORED",
                    "OFFICE_HOLD"}
    COUNTRY_KINDS = {"ALLY_OF", "ENEMY_OF", "DYNASTIC_UNION", "PERSONAL_UNION",
                     "RELIGIOUS_AFFILIATION", "SHARED_LANGUAGE", "SPLIT_FROM",
                     "SUZERAIN_OF", "VASSAL_OF", "TERRITORY_TRANSFER", "TRADE_PARTNER",
                     "CULTURAL_HEGEMONY", "BORDER_TENSION", "WAR_INVOLVES",
                     "PARTICIPATES_IN_WAR", "SIGNED_TREATY", "TREATY_PARTY",
                     "OFFICIAL_LANGUAGE", "RELIGION_IN", "WAR_ENDS_WITH",
                     "HAS_SUBDIVISION", "SUBDIVISION_OF", "PLACE_IN", "SUBJECT_OF"}
    CAUSAL_KINDS = {"CAUSES", "RESULTS_IN", "PARTICIPATES_IN", "OCCURS_AT", "SIGNED",
                    "EVENT_INVOLVES_COUNTRY", "EVENT_INVOLVES_PERSON",
                    "EVENT_HAS_WAR", "EVENT_HAS_TREATY"}

    graph = {
        "meta": {
            **D.META,
            "graph_name": "泛德意志的欧洲 · 设定集知识图谱",
            "node_count": len(nodes),
            "edge_count": len(all_edges),
            "node_types": dict(sorted(defaultdict(int, {t: sum(1 for n in nodes if n["type"] == t) for t in {n["type"] for n in nodes}}).items())),
            "edge_kinds": dict(sorted(defaultdict(int, {k: sum(1 for e in all_edges if e["kind"] == k) for k in {e["kind"] for e in all_edges}}).items())),
            "domains": ["人物与家族关系网", "国家关系网", "事件因果关系链", "自动补边"],
            "dangling_references": dangling,
        },
        "nodes": nodes,
        "edges": all_edges,
        "views": {
            "人物与家族关系网": {
                "description": "人物之间的血缘、婚姻、王朝归属、继承与竞争关系",
                "node_types": ["PERSON", "DYNASTY", "COUNTRY", "TREATY"],
                "edge_kinds": sorted(FAMILY_KINDS),
                "edges": sub(kind_filter=FAMILY_KINDS),
            },
            "国家关系网": {
                "description": "国家之间的同盟、敌对、王朝联合、宗教归属、语言共同体、领土转移与边缘张力",
                "node_types": ["COUNTRY", "RELIGION", "LANGUAGE", "SUBDIVISION", "PLACE", "WAR", "TREATY", "DYNASTY"],
                "edge_kinds": sorted(COUNTRY_KINDS),
                "edges": sub(kind_filter=COUNTRY_KINDS),
            },
            "事件因果关系链": {
                "description": "事件之间的因果传导、事件与人物/国家/战争/条约的关联",
                "node_types": ["EVENT", "PERSON", "COUNTRY", "WAR", "TREATY", "PLACE"],
                "edge_kinds": sorted(CAUSAL_KINDS),
                "edges": sub(kind_filter=CAUSAL_KINDS),
            },
            "历史物品留存网": {
                "description": "留存物与其现存持有方、存放地与收藏机构的关系",
                "node_types": ["ARTIFACT", "COUNTRY", "PLACE", "ORGANIZATION", "EVENT"],
                "edge_kinds": ["HELD_BY", "KEPT_IN", "KEPT_AT"],
                "edges": sub(kind_filter={"HELD_BY", "KEPT_IN", "KEPT_AT"}),
            },
        },
    }
    return graph, dangling


# ---------------------------------------------------------------- 3. 四张表
def build_timeline_table():
    rows = []
    for e in sorted(D.EVENTS, key=lambda x: (x["year"], x["id"])):
        rows.append({
            "seq": len(rows) + 1,
            "id": e["id"],
            "year": e["year"],
            "year_text": e["year_text"],
            "epoch": e["epoch"],
            "event_zh": e["name_zh"],
            "event_de": e["name_de"],
            "event_en": e["name_en"],
            "region": e["region"],
            "countries": [REG[c]["name_zh"] for c in e.get("country_ids", []) if c in REG],
            "country_ids": [c for c in e.get("country_ids", []) if c in REG],
            "persons": [REG[p]["name_zh"] for p in e.get("persons", []) if p in REG],
            "result": e["outcome"],
            "causes": e.get("causes", []),
            "effects": e.get("effects", []),
            "war_id": e.get("war_id"),
            "treaty_id": e.get("treaty_id"),
            "significance": e.get("significance"),
            "status": e["status"],
            "src": e["src"],
        })

    # 纵轴节点映射（含地图工程16节点）
    map_keys = D.map_axis_node_keys()
    axis = []
    for n in D.TIMELINE_NODES:
        eid = n.get("event_id")
        axis.append({
            "year": n["year"],
            "label": n.get("label"),
            "event_id": eid,
            "event_zh": REG[eid]["name_zh"] if eid in REG else None,
            "on_map_axis_16": n["year"] in map_keys,
            "note": n.get("note"),
        })

    md = ["# 时间线表（年份 · 事件 · 国家 · 结果）", "",
          f"> 共 {len(rows)} 个事件节点。字段：序号、年份、事件、国家、结果。",
          "> 状态：已确定 / 待定 / 修正。出处代号见文末。", ""]
    md.append(md_table(
        ["#", "年份", "事件", "国家", "结果", "状态"],
        [[r["seq"], r["year_text"], r["event_zh"], "、".join(r["countries"]) or "—",
          r["result"], r["status"]] for r in rows]))
    md.append("")
    md.append(f"## 纵轴节点映射（{len(axis)} 个节点，其中 S0《地图工程》原始节点 16 个）")
    md.append("")
    md.append(md_table(["年份", "节点标签", "对应事件 ID", "对应事件", "属S0地图16节点"],
                       [[a["year"], a["label"] or "—",
                         (f"`{a['event_id']}`" if a["event_id"] else "—"),
                         a["event_zh"] or "—",
                         "是" if a["on_map_axis_16"] else "否（后续文档新增）"]
                        for a in axis]))
    md.append("")
    md.append("> 注：S0《地图工程》纵轴共16个节点（1270、1272、1300、1356、1450、1524—1527、1618、1648、"
              "1789、1815、1848、1866、1871、1918、1945、1960），与横轴12项指标构成 16×12=192 张基础图。"
              "1450 节点对应“哈布斯堡回归”，正文将其记于“14世纪后期”，本表以 1450 为地图节点。")
    md.append("")
    md.append("## 事件详表")
    for r in rows:
        md.append(f"### {r['seq']}. {r['year_text']}　{r['event_zh']}")
        md.append(f"- **ID**：`{r['id']}`　**时代**：{r['epoch']}　**状态**：{r['status']}")
        if r["event_de"]:
            md.append(f"- **德**：{r['event_de']}")
        if r["event_en"]:
            md.append(f"- **英**：{r['event_en']}")
        md.append(f"- **地域**：{r['region']}")
        md.append(f"- **国家**：{'、'.join(r['countries']) or '—'}")
        if r["persons"]:
            md.append(f"- **人物**：{'、'.join(r['persons'])}")
        if r["war_id"]:
            md.append(f"- **战争**：{REG[r['war_id']]['name_zh'] if r['war_id'] in REG else r['war_id']}")
        if r["treaty_id"]:
            md.append(f"- **条约**：{REG[r['treaty_id']]['name_zh'] if r['treaty_id'] in REG else r['treaty_id']}")
        if r["significance"]:
            md.append(f"- **意义**：{r['significance']}")
        md.append(f"- **结果**：{r['result']}")
        md.append(f"- **出处**：{'、'.join(r['src'])}")
        md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return {"table": "timeline", "rows": rows, "axis_nodes": axis}, "\n".join(md)


def build_country_table():
    rows = []
    for c in D.COUNTRIES:
        rows.append({
            "id": c["id"],
            "name_zh": c["name_zh"],
            "name_short": c.get("name_short"),
            "name_de": c.get("name_de"),
            "name_en": c.get("name_en"),
            "polity": c.get("polity"),
            "dynasty": c.get("dynasty"),
            "religion": c.get("religion"),
            "capital": c.get("capital"),
            "territory": c.get("territory"),
            "language": c.get("language"),
            "founded": c.get("founded"),
            "time_span": c.get("time_span"),
            "overview": c.get("overview"),
            "key_traits": c.get("key_traits"),
            "status": c["status"],
            "src": c["src"],
        })

    md = ["# 国家表（国名 · 政体 · 宗教 · 首都 · 领土）", "",
          f"> 共 {len(rows)} 个国家/政治实体。包含大洲文明体与区域文明体。", ""]
    md.append(md_table(
        ["国名", "政体", "宗教", "首都", "领土"],
        [[r["name_zh"], r["polity"], r["religion"] or "—", r["capital"] or "—", r["territory"]]
         for r in rows]))
    md.append("")
    md.append("## 国家详表")
    for r in rows:
        md.append(f"### {r['name_zh']}　`{r['id']}`")
        md.append(f"- **德**：{r['name_de'] or '—'}　**英**：{r['name_en'] or '—'}")
        md.append(f"- **政体**：{r['polity']}")
        md.append(f"- **王朝**：{r['dynasty'] or '—'}")
        md.append(f"- **宗教**：{r['religion'] or '—'}")
        md.append(f"- **首都**：{r['capital'] or '—'}")
        md.append(f"- **领土**：{r['territory']}")
        md.append(f"- **语言**：{r['language'] or '—'}")
        md.append(f"- **存续**：{r['time_span'] or '—'}")
        md.append(f"- **概述**：{r['overview']}")
        if r["key_traits"]:
            md.append(f"- **关键特征**：{j(r['key_traits'])}")
        md.append(f"- **状态**：{r['status']}　**出处**：{'、'.join(r['src'])}")
        md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return {"table": "countries", "rows": rows}, "\n".join(md)


def build_people_table():
    rows = []
    for p in sorted(D.PEOPLE, key=lambda x: (x.get("dynasty_id") or "", x["id"])):
        rows.append({
            "id": p["id"],
            "name_zh": p.get("name_full_zh") or p["name_zh"],
            "name_de": p.get("name_de"),
            "name_en": p.get("name_en"),
            "title": p.get("title"),
            "dynasty": p.get("dynasty"),
            "dynasty_id": p.get("dynasty_id"),
            "country": REG[p["country_id"]]["name_zh"] if p.get("country_id") in REG else None,
            "birth": p.get("birth"),
            "death": p.get("death"),
            "reign": p.get("reign"),
            "positions": p.get("positions"),
            "deeds": p.get("deeds"),
            "family": p.get("family"),
            "context": p.get("context"),
            "appendix": p.get("appendix", False),
            "status": p["status"],
            "src": p["src"],
        })

    md = ["# 人物表（姓名 · 王朝 · 生卒 · 职位 · 事迹）", "",
          f"> 共 {len(rows)} 条。**重要说明**：原设定集对人物的记载密度极低，多数人物仅一处提及，"
          "生卒年在文档中未载。本表严格留空为“文档未载”，不作任何推定填充。", ""]
    md.append(md_table(
        ["姓名", "王朝", "生", "卒", "职位", "事迹（摘要）"],
        [[r["name_zh"], r["dynasty"] or "—", r["birth"] or "—", r["death"] or "—",
          j(r["positions"]) or r["title"] or "—", j(r["deeds"])] for r in rows]))
    md.append("")
    md.append("## 人物详表")
    for r in rows:
        md.append(f"### {r['name_zh']}　`{r['id']}`")
        md.append(f"- **德**：{r['name_de'] or '—'}　**英**：{r['name_en'] or '—'}")
        md.append(f"- **头衔**：{r['title'] or '—'}")
        md.append(f"- **王朝**：{r['dynasty'] or '—'}　**所属国**：{r['country'] or '—'}")
        md.append(f"- **生**：{r['birth'] or '—'}　**卒**：{r['death'] or '—'}　**在位**：{r['reign'] or '—'}")
        if r["positions"]:
            md.append(f"- **职位**：{j(r['positions'])}")
        md.append(f"- **事迹**：{j(r['deeds'])}")
        if r["family"]:
            md.append(f"- **家族**：{j(r['family'])}")
        if r["context"]:
            md.append(f"- **备注**：{r['context']}")
        md.append(f"- **状态**：{r['status']}　**出处**：{'、'.join(r['src'])}")
        md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return {"table": "people", "rows": rows}, "\n".join(md)


def build_war_table():
    rows = []
    for w in sorted(D.WARS, key=lambda x: (int(x["time_start"]), x["id"])):
        rows.append({
            "id": w["id"],
            "name_zh": w["name_zh"],
            "name_de": w.get("name_de"),
            "name_en": w.get("name_en"),
            "time": w["time_text"],
            "time_start": w["time_start"],
            "time_end": w["time_end"],
            "epoch": w.get("epoch"),
            "side_a": w["side_a"]["name"],
            "side_a_members": w["side_a"].get("members"),
            "side_b": w["side_b"]["name"],
            "side_b_members": w["side_b"].get("members"),
            "causes": w.get("causes_text"),
            "phases": w.get("phases"),
            "key_battles": w.get("key_battles"),
            "result": w["result"],
            "consequence": w.get("consequence"),
            "treaty": w.get("treaty"),
            "treaty_id": w.get("treaty_id"),
            "status": w["status"],
            "src": w["src"],
        })

    md = ["# 战争表（时间 · 双方 · 结果 · 条约）", "",
          f"> 共 {len(rows)} 场武装冲突/战争。", ""]
    md.append(md_table(
        ["时间", "战争", "A方", "B方", "结果", "条约"],
        [[r["time"], r["name_zh"], r["side_a"], r["side_b"], r["result"], r["treaty"] or "—"]
         for r in rows]))
    md.append("")
    md.append("## 战争详表")
    for r in rows:
        md.append(f"### {r['name_zh']}　`{r['id']}`")
        md.append(f"- **德**：{r['name_de'] or '—'}　**英**：{r['name_en'] or '—'}")
        md.append(f"- **时间**：{r['time']}　**时代**：{r['epoch'] or '—'}")
        md.append(f"- **A方**：{r['side_a']}（{j(r['side_a_members'])}）")
        md.append(f"- **B方**：{r['side_b']}（{j(r['side_b_members'])}）")
        if r["causes"]:
            md.append(f"- **起因**：{j(r['causes'])}")
        if r["phases"]:
            md.append("- **阶段**：")
            for ph in r["phases"]:
                md.append(f"  - {ph['time']}　{ph['name']}：{ph['content']}")
        if r["key_battles"]:
            md.append(f"- **关键战斗/战况**：{j(r['key_battles'])}")
        md.append(f"- **结果**：{r['result']}")
        if r["consequence"]:
            md.append(f"- **后果**：{j(r['consequence'])}")
        if r["treaty"]:
            md.append(f"- **条约**：{r['treaty']} (`{r['treaty_id']}`)" if r["treaty_id"] else f"- **条约**：{r['treaty']}")
        md.append(f"- **状态**：{r['status']}　**出处**：{'、'.join(r['src'])}")
        md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return {"table": "wars", "rows": rows}, "\n".join(md)


# ---------------------------------------------------------------- 4. 对照表 / 转写表
def build_glossary():
    by_cat = OrderedDict()
    for g in D.GLOSSARY:
        by_cat.setdefault(g["category"], []).append(g)

    md = ["# 专有名词 中 — 英 — 德 对照表", "",
          f"> 共 {len(D.GLOSSARY)} 条，按类别分组。",
          "> 原则：中文为正典译名；德文取设定集原始拼写；英文为对照形式（设定集未给出英文形式者，按通行学术译法标注）。", ""]
    for cat, items in by_cat.items():
        md.append(f"## {cat}")
        md.append("")
        md.append(md_table(["中文", "Deutsch", "English", "备注"],
                           [[i["zh"], i["de"], i["en"], i.get("note") or ""] for i in items]))
        md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return {"glossary": D.GLOSSARY, "by_category": by_cat}, "\n".join(md)


GERMAN_TO_ENGLISH_FALLBACK = True


def build_transliteration():
    rows = []
    for p in D.PLACES:
        rows.append({
            "id": p["id"],
            "type": p["type"],
            "zh": p["zh"],
            "zh_alias": p.get("zh_alias", []),
            "real": p.get("real"),
            "de": p.get("de"),
            "en": p.get("en"),
            "fr": p.get("fr"),
            "it": p.get("it"),
            "nl": p.get("nl"),
            "ru": p.get("ru"),
            "uk": p.get("uk"),
            "oc": p.get("oc"),
            "pl": p.get("pl"),
            "cs": p.get("cs"),
            "hr": p.get("hr"),
            "es": p.get("es"),
            "ca": p.get("ca"),
            "el": p.get("el"),
            "tr": p.get("tr"),
            "hu": p.get("hu"),
            "cy": p.get("cy"),
            "ga": p.get("ga"),
            "country_id": p.get("country_id"),
            "note": p.get("note"),
            "src": p.get("src", []),
        })

    md = ["# 地名转写表", "",
          "> 规则（来自设定集）：**法兰克地名中文译名采用德语发音**（如帕里斯而非巴黎，劳格登而非里昂）；",
          "> 不列颠的英语国名与专名一律采用通行英语读音的中文译名。", "",
          "> 表格中 **「正典中文」** 为推荐用法；**「现实对应」** 仅供检索与理解，不作为正典。", ""]
    md.append("## 全部地名")
    md.append("")
    md.append(md_table(
        ["正典中文", "类型", "Deutsch", "English", "现实对应", "所在国", "备注"],
        [[r["zh"], r["type"], r["de"] or "—", r["en"] or "—", r["real"] or "—",
          REG[r["country_id"]]["name_zh"] if r["country_id"] in REG else "—",
          ((("别名：" + "、".join(r["zh_alias"])) if r["zh_alias"] else "") +
           (("；" + r["note"]) if r["note"] else "")).strip("；") or ""]
         for r in rows]))
    md.append("")

    # 按国分组
    md.append("## 按国家/地区分组")
    md.append("")
    groups = OrderedDict()
    for r in rows:
        key = REG[r["country_id"]]["name_zh"] if r["country_id"] in REG else "跨国/未归属"
        groups.setdefault(key, []).append(r)
    for country, items in groups.items():
        md.append(f"### {country}")
        md.append("")
        md.append(md_table(["正典中文", "类型", "Deutsch", "English", "现实对应"],
                           [[i["zh"], i["type"], i["de"] or "—", i["en"] or "—", i["real"] or "—"] for i in items]))
        md.append("")

    # 河流山脉
    md.append("## 河流与山脉")
    md.append("")
    md.append(md_table(["正典中文", "类型", "Deutsch", "English", "现实对应"],
                       [[r["zh"], r["type"], r["de"] or "—", r["en"] or "—", r["real"] or "—"]
                        for r in rows if r["type"] in ("河流", "山脉", "山口")]))
    md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return {"places": rows}, "\n".join(md)


# ---------------------------------------------------------------- 5. 索引
def build_index():
    """构建设定集索引：文档 → 章节 → 条目，并可全文检索"""
    entries = []

    def add(doc, section, subsection, kind, ref_id, title, summary):
        entries.append({
            "doc": doc, "section": section, "subsection": subsection,
            "kind": kind, "ref_id": ref_id, "title": title,
            "summary": summary or "",
        })

    # 源文档章节骨架
    DOC_SECTIONS = {
        "S0": [
            ("一、总纲", None, "世界线总述：13世纪卡佩绝嗣→哈布斯堡入主法兰克→双日耳曼政治体→多极格局"),
            ("二、时间纵轴", "（一）13世纪：双源发生", "卡佩绝嗣、鲁道夫加冕、奥托卡二世、鲁道夫坐稳法兰克"),
            ("二、时间纵轴", "（二）14世纪：法兰克福条约与双元帝国", "哈布斯堡回归帝国、1356法兰克福宪章、双元格局"),
            ("二、时间纵轴", "（三）15—16世纪：宗教改革与农民战争", "普热米斯尔新教化、新教四大派别、南德新教文化、1524—1527农民战争"),
            ("二、时间纵轴", "（四）17世纪：宗教战争与维也纳和约", "起因、阵营、四阶段、1648维也纳和约十二条结果"),
            ("二、时间纵轴", "（五）18世纪：双王冠融合与伊比利亚大革命", "双王冠准融合、1789伊比利亚-奥克大革命、反伊比利亚战争"),
            ("二、时间纵轴", "（六）19世纪：1848、1866、1871", "1848大德意志失败、1866奥法战争、1871罗马加冕"),
            ("二、时间纵轴", "（七）20世纪：一战、二战与战后秩序", "第二次工业革命、一战、二战、两套行政区划"),
            ("三、横轴指标", "（一）政治与王朝", "哈布斯堡、普热米斯尔、瑞士、伊比利亚、英格兰-诺曼底、低地、汉萨"),
            ("三、横轴指标", "（二）宗教", "天主教、路德宗、加尔文宗、胡斯派、阿尔卑斯福音派"),
            ("三、横轴指标", "（三）语言与正字法", "四种语言、统一正字法、泛德意志认同层次"),
            ("三、横轴指标", "（四）经济与工业", "四大工业带、汉萨城市、法兰克经济、第二次工业革命"),
            ("三、横轴指标", "（五）学术与宗教圣地", "德意志/法兰克/瑞士学术圣地、宗教圣地"),
            ("三、横轴指标", "（六）民族与边缘问题", "奥克、克罗地亚-斯洛文尼亚、布列塔尼、波兰西部、北意大利、波西米亚、低地"),
            ("三、横轴指标", "（七）国际体系", "六极均势、泛德意志合作、殖民地、一战二战阵营"),
            ("三、横轴指标", "（八）人才分布", "中欧科学人才、法兰西人才分割、一战知识分子流散、美国定位"),
            ("四、语言与地名系统", None, "国名与民族、州名、首府、其他城市、河流与山脉、译名原则"),
            ("五、地图工程", None, "16×12基础矩阵、24张专题、核心必绘48张、统一风格"),
            ("六、修正与注意", None, "八条关键修正：法语人口、宗教格局、王朝归属、南德文化、美国定位、无冷战、民族构建、正字法"),
        ],
        "S1": [
            ("一、世界观总纲", None, "把现实史的“奥地利问题”转移为“法兰克问题”"),
            ("二、纵轴：世界历史时间线", None, "1270→1960逐节点整理，标注【原设定】【本轮确定】【待定】"),
            ("二、纵轴", "亚洲宗教史：新的基本原则", "削弱伊斯兰教在亚洲中部东部的统治范围，重划伊斯兰文明东部边界"),
            ("二、纵轴", "公元前后—8世纪 / 8—12世纪：西域佛教", "西域佛教传统强化、伊斯兰化止步于更西侧"),
            ("二、纵轴", "1200—1300：蒙古帝国", "蒙古作为连接三大文明的枢纽"),
            ("二、纵轴", "蒙古宗教结构", "长生天（王权合法性）+ 佛教（知识体系）+ 萨满（基层传统）三层结构"),
            ("二、纵轴", "15—17世纪：蒙古佛教化", "佛教成为国家文化但未取代长生天与萨满"),
            ("二、纵轴", "16—19世纪：俄罗斯进入亚洲", "俄罗斯面对草原蒙古、西伯利亚萨满、佛教西域的梯度"),
            ("二、纵轴", "俄罗斯的新历史主题 / 中国的新历史角色", "欧亚双重身份；中国西向文明轴"),
            ("二、纵轴", "1960年前后：新的亚洲文明地图", "区域文明/宗教对照表"),
            ("二、纵轴", "君士坦丁堡问题", "【待进一步确定】保留基督教海峡政治体，海峡是文明边界而非文明墙"),
            ("二、纵轴", "法兰克与近东", "法兰克东方学传统与文明边界国家定位"),
            ("三、横轴：六大文明/政治力量", None, "德意志=文明核心、法兰克=文明边界、伊比利亚=秩序挑战者、俄罗斯=欧亚平衡者、英国=海洋平衡者、美国=海外工业强国"),
            ("四、文明结构", None, "六极结构 + 两条亚洲文明轴"),
            ("五、最终的纵横时间表", None, "世界史母表：时间 × 德意志/法兰克、伊比利亚、俄罗斯、英国/美国、亚洲"),
            ("六、最重要的一句话", None, "历史实验：更大的德意志文明仍会输掉一战，但能避免被彻底重构"),
        ],
        "S2": [
            ("一、总览", None, "四个层次：国家内部行政区划、中央—地方关系、政党政治、超国家/文明地理"),
            ("二、法兰克：联邦化单一制", None, "国家基本结构、中央与州权划分"),
            ("三、法兰克行政区划", None, "奥克省特殊建制最终走向废除"),
            ("四、奥克省1975年前后被取消", None, "奥克正常化政策"),
            ("五、法兰克州的最终结构", None, "原法兰克本土州 + 原奥克省地区；11 vs 12 数字矛盾"),
            ("六、两个南方枢纽州", None, "多菲内（格勒诺布尔）、普罗旺斯（马赛）"),
            ("七—十、法兰克政治发展", None, "否定王权专制→革命逻辑；最早的宪政君主制之一；宪政演化时间线；两个哈布斯堡必须严格区分"),
            ("十一、法兰克政党政治", None, "FVP / FSP / FKP，两大党竞争+小党"),
            ("十二—十六、德意志", None, "真正的联邦制、联邦州列表、央地关系、多党制、政治文化"),
            ("十七—二十三、伊比利亚", None, "高度中央集权总统制、历史政治逻辑、大型大区、央地关系、少数民族政策、政党政治"),
            ("二十四、英国", None, "本阶段不要过度补设定（后由S3全部敲定）"),
            ("二十五—二十八、美国", None, "共和制进一步“左移”、政党政治、行政区划尚未重新设计"),
            ("二十九、新增的“大洲划分”", None, "四洲：欧洲、亚洲、新大洲（未命名）、非洲；撒哈拉的文明分界功能"),
            ("三十、五国政治光谱", None, "五种不同的民主政治模式 + 欧盟作为共同框架"),
            ("三十一、状态标记", None, "🟢基本敲定清单 / 🟡已提出但细节未定清单"),
        ],
        "S3": [
            ("序：本册的任务", None, "处理S2中列为未定的全部英国条目；核心命题：罗曼世俗高文化转移到不列颠"),
            ("一、修订清单", None, "R1-R7 正式覆盖旧设定"),
            ("二、核心命题与机制", None, "法兰克问题/英格兰问题的一对镜像；罗曼文化流向英伦的三级因果；为什么是绝对主义而不是议会"),
            ("三、语言：英语即罗曼化的日耳曼语", None, "双言到合流的五阶段；罗曼化程度梯度"),
            ("四、王朝：金雀花与蒙福尔", None, "金雀花倾覆、蒙福尔上位、备选王朝名、王权法统"),
            ("五、政治史年表", None, "盎格鲁-撒克逊到1945转向"),
            ("六、战前：不列颠王国", None, "政体、中央机构、军政合一三级制、社会与文化"),
            ("七、1945：战败与被监督的民主化", None, "触发链条、核心特征、两项被强加的改造、过渡形态"),
            ("八、战后：不列颠联邦共和国", None, "政体与宪法、联邦化分权、政党政治、八个一级联邦单位"),
            ("九、苏格兰与威尔士", None, "无独立法统；特殊性是语言与文化的"),
            ("十、爱尔兰", None, "1945年全岛独立共和国，不分治"),
            ("十一、英联邦与帝国遗产", None, "海洋商业帝国、战后瓦解、语言文化商业共同体"),
            ("十二、国际定位", None, "海洋平衡者；与伊比利亚/法兰克/德意志的关系"),
            ("十三、法兰克与不列颠对偶表", None, "十个维度的对偶"),
            ("十四、状态标记", None, "已敲定 / 待定"),
            ("十五、六国政治模式总表", None, "德意志、法兰克、伊比利亚、美国、不列颠、瑞士"),
        ],
        "S4": [
            ("七、罗斯兀鲁思：蒙古王朝与后基辅罗斯国家传统", "一、问题的核心", "基辅罗斯→莫斯科公国→俄罗斯帝国链条被彻底改变"),
            ("七、罗斯兀鲁思", "二、蒙古对东斯拉夫世界的统治更加深入", "金帐汗国未迅速伊斯兰化；不只是“占领者”"),
            ("七、罗斯兀鲁思", "三、莫斯科王朝的蒙古化", "反向融合：不是莫斯科摆脱蒙古，而是成为蒙古政治体系的继承者"),
            ("七、罗斯兀鲁思", "四、蒙古王朝最终直接统治莫斯科", "联姻、继承、军事合作、贵族融合"),
            ("七、罗斯兀鲁思", "五、“金帐汗国灭亡”≠蒙古传统灭亡", "国家灭亡 ≠ 文明传统消失"),
            ("七、罗斯兀鲁思", "六、国家正统发生变化", "古罗斯诸国→蒙古征服→金帐秩序→罗斯兀鲁思"),
            ("七、罗斯兀鲁思", "七、莫斯科国的文化结构", "东斯拉夫 + 蒙古 + 突厥 + 佛教/萨满 四层"),
            ("七、罗斯兀鲁思", "八、与基辅王国的分道扬镳", "欧洲道路 vs 蒙古-北亚道路"),
            ("七、罗斯兀鲁思", "九、一战：重新夺取基辅王国", "试图恢复旧时代的东欧大陆体系"),
            ("七、罗斯兀鲁思", "十、二战后基辅王国再次脱离", "两次统一、两次分离的历史记忆"),
            ("七、罗斯兀鲁思", "十一、白罗斯的地位", "缓冲国家；合理方案为与基辅王国组成联邦"),
            ("七、罗斯兀鲁思", "十二、与欧洲的关系", "罗斯兀鲁思是亚洲北部国家；基辅王国属欧洲东部"),
            ("七、罗斯兀鲁思", "十三、与蒙古帝国的关系", "“蒙古帝国是我们的帝国时代之一”"),
            ("七、罗斯兀鲁思", "十四—十五、蒙古文明圈的西向影响 / 欧亚文明梯度", "从太平洋延伸到东欧森林地带"),
            ("七、罗斯兀鲁思", "十六、最重要的结果", "后基辅罗斯国家的国家认同"),
        ],
    }

    for doc, secs in DOC_SECTIONS.items():
        for section, sub, summary in secs:
            add(doc, section, sub, "章节", None, (f"{section}｜{sub}" if sub else section), summary)

    # 实体条目挂到文档
    def doc_of(entity):
        return entity.get("src", ["S0"])

    for c in D.COUNTRIES:
        for d in c["src"]:
            add(d, "实体：国家", None, "COUNTRY", c["id"], c["name_zh"], c.get("overview"))
    for c in D.DYNASTIES:
        for d in c["src"]:
            add(d, "实体：王朝", None, "DYNASTY", c["id"], c["name_zh"], c.get("overview"))
    for c in D.PEOPLE:
        for d in c["src"]:
            add(d, "实体：人物", None, "PERSON", c["id"], c["name_zh"], j(c.get("deeds")))
    for c in D.EVENTS:
        for d in c["src"]:
            add(d, "实体：事件", c.get("epoch"), "EVENT", c["id"], f"{c['year_text']}　{c['name_zh']}", c.get("summary"))
    for c in D.WARS:
        for d in c["src"]:
            add(d, "实体：战争", c.get("epoch"), "WAR", c["id"], c["name_zh"], c.get("result"))
    for c in D.TREATIES:
        for d in c["src"]:
            add(d, "实体：条约", c.get("time"), "TREATY", c["id"], c["name_zh"], c.get("background"))
    for c in D.RELIGIONS:
        for d in c["src"]:
            add(d, "实体：宗教", None, "RELIGION", c["id"], c["name_zh"], c.get("doctrine"))
    for c in D.LANGUAGES:
        for d in c["src"]:
            add(d, "实体：语言", None, "LANGUAGE", c["id"], c["name_zh"], c.get("sociolinguistics"))
    for c in D.PLACES:
        for d in c["src"]:
            add(d, "实体：地点", c.get("type"), "PLACE", c["id"], c["zh"], c.get("note"))
    for c in D.SUBDIVISIONS:
        for d in c["src"]:
            add(d, "实体：行政区划", None, "SUBDIVISION", c["id"], c["name_zh"], j(c.get("level_system")))
    for c in D.PARTIES:
        for d in c["src"]:
            add(d, "实体：政党", None, "PARTY", c["id"], c["name_zh"], j(c.get("base")))
    for c in D.ORGANIZATIONS:
        for d in c["src"]:
            add(d, "实体：机构", None, "ORGANIZATION", c["id"], c["name_zh"], c.get("function"))
    for c in D.CONFLICTS:
        for d in c["src"]:
            add(d, "冲突与修正", c["topic"], "CONFLICT", c["id"], c["topic"], c.get("resolution"))
    for c in D.REVISIONS:
        for d in c["src"]:
            add(d, "冲突与修正", c["topic"], "REVISION", c["id"], c["topic"], None)
    for p in D.PENDING:
        for d in p["src"]:
            add(d, "待定项", None, "PENDING", None, p["item"], p.get("resolved_by"))
    for p in D.CONFIRMED:
        add("S2", "已确定项", None, "CONFIRMED", None, p, None)

    doc = {
        "meta": {**D.META, "index_entry_count": len(entries)},
        "documents": [dict(s, sections=[s2[0] for s2 in secs] if False else None)
                      for s in D.META["source_documents"]],
        "sections": {k: v for k, v in DOC_SECTIONS.items()},
        "entries": entries,
    }
    return doc, entries, DOC_SECTIONS


def index_markdown(entries, DOC_SECTIONS):
    md = ["# 设定集索引", "",
          "> 用途：快速检索五份设定集文档中的任意主题。",
          "> 结构：文档骨架 → 章节索引 → 实体索引 → 待定/已确定/修正清单。",
          "> 交互式检索请打开 `docs/index.html`。", ""]

    md.append("## 文档清单与章节骨架")
    md.append("")
    for s in D.META["source_documents"]:
        md.append(f"### {s['id']}　{s['file']}")
        md.append(f"- **标题**：{s['title']}")
        md.append(f"- **职能**：{s['role']}")
        md.append("")
        for section, sub, summary in DOC_SECTIONS[s["id"]]:
            md.append(f"  - **{section}**" + (f" → {sub}" if sub else ""))
            if summary:
                md.append(f"    - {summary}")
        md.append("")

    # 按 kind 汇总
    md.append("## 实体索引（按类型）")
    md.append("")
    kinds = OrderedDict()
    for e in entries:
        if e["kind"] in ("章节", "已确定项", "待定项", "CONFLICT", "REVISION"):
            continue
        kinds.setdefault(e["kind"], []).append(e)
    for kind, items in kinds.items():
        md.append(f"### {kind}（{len(items)}）")
        md.append("")
        md.append(md_table(["名称", "ID", "出处"],
                           [[i["title"], (f"`{i['ref_id']}`" if i["ref_id"] else "—"), i["doc"]] for i in items]))
        md.append("")

    md.append("## 主题检索表（关键词 → 条目）")
    md.append("")
    kw = defaultdict(list)
    for e in entries:
        for token in re.findall(r"[\u4e00-\u9fff]{2,4}|[A-Za-z]{3,}", (e["title"] or "") + (e["summary"] or "")):
            kw[token].append(e)
    hot = sorted(((k, v) for k, v in kw.items() if len(v) >= 3), key=lambda x: (-len(x[1]), x[0]))[:200]
    md.append(md_table(["关键词", "命中数", "相关条目"],
                       [[k, len(v), "、".join(dict.fromkeys(i["title"] for i in v[:8]))] for k, v in hot]))
    md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return "\n".join(md)


INDEX_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>泛德意志的欧洲 · 设定集索引</title>
<style>
  :root { --bg:#14110d; --fg:#e8e2d4; --dim:#a89e8a; --accent:#c9a227; --line:#3a332a; --card:#1d1913; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--fg);
         font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif; }
  header { position:sticky; top:0; background:rgba(20,17,13,.96); border-bottom:1px solid var(--line);
           padding:14px 20px; backdrop-filter:blur(6px); z-index:10; }
  h1 { margin:0 0 8px; font-size:19px; letter-spacing:.04em; }
  h1 span { color:var(--accent); }
  .sub { color:var(--dim); font-size:12px; margin-bottom:10px; }
  #q { width:100%; padding:11px 13px; font-size:15px; border-radius:7px;
       border:1px solid var(--line); background:#0e0c09; color:var(--fg); }
  #q:focus { outline:none; border-color:var(--accent); }
  .filters { margin-top:10px; display:flex; flex-wrap:wrap; gap:6px; }
  .chip { font-size:12px; padding:3px 10px; border-radius:20px; border:1px solid var(--line);
          background:#0e0c09; color:var(--dim); cursor:pointer; user-select:none; }
  .chip:hover { border-color:var(--accent); color:var(--fg); }
  .chip.on { background:var(--accent); color:#14110d; border-color:var(--accent); font-weight:600; }
  main { padding:16px 20px 60px; max-width:1180px; margin:0 auto; }
  .count { color:var(--dim); font-size:12px; margin-bottom:12px; }
  .item { border:1px solid var(--line); border-radius:8px; background:var(--card);
          padding:11px 14px; margin-bottom:9px; }
  .item h3 { margin:0 0 5px; font-size:15px; font-weight:600; }
  .item h3 .rid { font-family:Consolas,monospace; font-size:11px; color:var(--accent);
                  border:1px solid var(--line); border-radius:4px; padding:1px 5px; margin-left:7px; }
  .item .meta { font-size:11.5px; color:var(--dim); margin-bottom:5px; }
  .item .meta b { color:#cfc6b2; font-weight:600; }
  .item .sm { font-size:13px; line-height:1.6; color:#d6cebc; }
  mark { background:var(--accent); color:#14110d; border-radius:2px; padding:0 1px; }
  .empty { color:var(--dim); padding:30px 0; text-align:center; }
  footer { color:var(--dim); font-size:11.5px; padding:0 20px 40px; max-width:1180px; margin:0 auto; }
  footer code { color:var(--accent); }
</style>
</head>
<body>
<header>
  <h1>泛德意志的欧洲 · <span>设定集索引</span></h1>
  <div class="sub">离线全文检索 · 共 __N__ 条索引 · 数据源：source/ 下五份设定集文档（S0–S4）</div>
  <input id="q" type="search" placeholder="输入关键词检索：奥克、普热米斯尔、蒙福尔、罗斯兀鲁思、维也纳和约、待定……" autocomplete="off">
  <div class="filters" id="filters"></div>
</header>
<main>
  <div class="count" id="count"></div>
  <div id="list"></div>
</main>
<footer>
  出处代号：<code>S0</code> 设定集.docx ｜ <code>S1</code> 设定集补充.docx ｜ <code>S2</code> 设定集补充2.docx ｜
  <code>S3</code> 设定集补充3.docx ｜ <code>S4</code> 设定集补充4.docx<br>
  本页由 tools/build.py 自动生成，可直接双击在浏览器打开（无需服务器）。
</footer>
<script>
const DATA = __DATA__;
const FILTERS = __FILTERS__;
let active = new Set();

const filtersEl = document.getElementById('filters');
FILTERS.forEach(f => {
  const c = document.createElement('div');
  c.className = 'chip'; c.textContent = f.label; c.dataset.k = f.kind;
  if (f.kind === '*') c.classList.add('on');
  c.onclick = () => {
    if (f.kind === '*') { active.clear(); }
    else {
      active.has(f.kind) ? active.delete(f.kind) : active.add(f.kind);
      filtersEl.querySelector('[data-k="*"]').classList.toggle('on', active.size === 0);
    }
    document.querySelectorAll('.chip').forEach(x => {
      if (x.dataset.k !== '*') x.classList.toggle('on', active.has(x.dataset.k));
    });
    render();
  };
  filtersEl.appendChild(c);
});

const q = document.getElementById('q');
q.addEventListener('input', render);

function esc(s) {
  return (s == null ? '' : String(s)).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));
}
function hl(s, term) {
  let out = esc(s);
  if (!term) return out;
  const safe = term.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
  try { return out.replace(new RegExp('(' + safe + ')', 'gi'), '<mark>$1</mark>'); } catch (e) { return out; }
}

function render() {
  const term = q.value.trim();
  const t = term.toLowerCase();
  let rows = DATA;
  if (active.size) rows = rows.filter(r => active.has(r.kind));
  if (t) rows = rows.filter(r => ((r.title||'') + ' ' + (r.summary||'') + ' ' + (r.ref_id||'') + ' ' +
                                  (r.section||'') + ' ' + (r.subsection||'') + ' ' + r.doc).toLowerCase().includes(t));
  document.getElementById('count').textContent = '命中 ' + rows.length + ' / ' + DATA.length + ' 条';
  const list = document.getElementById('list');
  if (!rows.length) { list.innerHTML = '<div class="empty">没有匹配的索引条目。</div>'; return; }
  list.innerHTML = rows.slice(0, 400).map(r => `
    <div class="item">
      <h3>${hl(r.title, term)}${r.ref_id ? '<span class="rid">' + esc(r.ref_id) + '</span>' : ''}</h3>
      <div class="meta"><b>${esc(r.doc)}</b> ｜ ${esc(r.section||'')}${r.subsection ? ' → ' + esc(r.subsection) : ''} ｜ ${esc(r.kind)}</div>
      ${r.summary ? '<div class="sm">' + hl(r.summary, term) + '</div>' : ''}
    </div>`).join('') + (rows.length > 400 ? '<div class="empty">仅显示前 400 条，请细化检索词。</div>' : '');
}
render();
</script>
</body>
</html>
"""


def build_index_html(entries):
    kinds = [k for k in dict.fromkeys(e["kind"] for e in entries)
             if k not in ("章节", "CONFIRMED")]
    order = ["COUNTRY", "DYNASTY", "PERSON", "EVENT", "WAR", "TREATY", "PLACE",
             "RELIGION", "LANGUAGE", "SUBDIVISION", "PARTY", "ORGANIZATION",
             "CONFLICT", "REVISION", "PENDING"]
    kinds = [k for k in order if k in kinds] + [k for k in kinds if k not in order]
    filters = [{"kind": "*", "label": "全部"}] + [{"kind": k, "label": k} for k in kinds]
    html = INDEX_HTML_TEMPLATE.replace("__DATA__", json.dumps(entries, ensure_ascii=False))
    html = html.replace("__FILTERS__", json.dumps(filters, ensure_ascii=False))
    html = html.replace("__N__", str(len(entries)))
    return html


# ---------------------------------------------------------------- 6. 三态清单
def build_status_doc():
    # 待定项：以 kb_pending.py 的 29 条（含优先级与方案）为唯一权威清单，
    # 并保留 kb_data.py 中的传统口径（S2 第三十一节 🟡 清单）。
    try:
        import kb_pending as PD
        detailed = PD.PENDING
        detailed_map = {p["topic"]: p for p in detailed}
    except ImportError:
        detailed, detailed_map = [], {}

    def _common_prefix(a, b):
        n = 0
        for x, y in zip(a, b):
            if x != y:
                break
            n += 1
        return n

    # 显式别名表：kb_data.PENDING 的旧措辞 → kb_pending.PENDING 的正式 topic。
    # 两张清单对同一件事的措辞差异过大，无法靠字面匹配，故显式列出。
    _ALIAS = {
        "美国具体州界及行政层级": "美国具体州界及行政层级",
        "英国现代行政区划": "不列颠一级单位是否最终定为八个 / 与爱尔兰的关系安排",
        "英国政治体系": "不列颠战后总统职权细节与政教分离的具体安排",
        "英国具体联邦/单一制结构": "不列颠一级单位是否最终定为八个 / 与爱尔兰的关系安排",
        "英国苏格兰、威尔士的最终制度（爱尔兰独立）":
            "爱尔兰凯尔特语官方地位、总统与总理职权、与英联邦的关系",
        "英联邦成员名单与共同防务条款": "英联邦成员名单与是否设共同防务条款",
        "不列颠政教分离的具体安排": "不列颠战后总统职权细节与政教分离的具体安排",
        "爱尔兰凯尔特语官方地位、总统与总理职权、与英联邦关系":
            "爱尔兰凯尔特语官方地位、总统与总理职权、与英联邦的关系",
        "不列颠一级单位是否最终定为八个":
            "爱尔兰是否最终采用八个一级联邦单位之外的安排 / 不列颠一级单位是否最终定为八个",
        "伦敦与帕里斯之间的“罗曼正统之争”（可继续深挖的接口）":
            "「伦敦与帕里斯之间的罗曼正统之争」是否正式立线",
        "君士坦丁堡/海峡政治体的具体形态": "君士坦丁堡 / 海峡政治体的具体形态",
        "“罗斯兀鲁思/莫斯科国”的正式别名（“俄罗斯”已废弃）":
            "「罗斯兀鲁思 / 莫斯科国」的正式别名（「俄罗斯」已按 S4 要求废弃）",
    }

    # 已被 S3/R4 明确敲定、不再属于待定的旧条目（保留记录，标为已解决）
    _RESOLVED = {
        "英国现代行政区划": "S3 已敲定八个一级联邦单位，各带首府",
        "英国政治体系": "S3 已敲定为联邦共和国（成文宪法、总统、下议院普选、宪法法院、多党制）",
        "英国具体联邦/单一制结构": "S3 已敲定为联邦共和国",
        "英国苏格兰、威尔士的最终制度（爱尔兰独立）":
            "S3 已敲定：无独立法统，特殊性为语言与文化；爱尔兰 1945 全岛独立",
    }

    def _match(item_text):
        """kb_pending 的 topic 与 kb_data 的 item 措辞略有差异。

        判定顺序：
          1) 显式别名表（措辞差异过大、无法靠字面匹配者）
          2) 完全相等
          3) 一方是另一方的子串
          4) 公共前缀 >= min(12, 较短串长度 * 0.7)
        宁可不匹配，也不误配——误配会让一个真待定项长出错误的优先级。
        """
        a = item_text.strip()
        if a in _ALIAS:
            return detailed_map.get(_ALIAS[a])
        if a in detailed_map:
            return detailed_map[a]
        best, best_score = None, 0
        for topic, d in detailed_map.items():
            b = topic.strip()
            if a in b or b in a:
                score = min(len(a), len(b)) * 2  # 子串关系视为最强
            else:
                cp = _common_prefix(a, b)
                need = min(12, int(min(len(a), len(b)) * 0.7))
                score = cp if cp >= need else 0
            if score > best_score:
                best, best_score = d, score
        return best

    pending = []
    matched = set()
    resolved = []
    for p in D.PENDING:
        item = dict(p)
        if p["item"] in _RESOLVED:
            item["priority"] = None
            item["resolved_by_later_doc"] = _RESOLVED[p["item"]]
            resolved.append(item)
            continue
        d = _match(p["item"])
        if d:
            item["priority"] = d["priority"]
            item["options_count"] = len(d["options"])
            item["recommend"] = d["recommend"]
            item["detail_ref"] = d["id"]
            item["status"] = d["status"]
            if d.get("adopted"):
                item["adopted"] = d["adopted"]
            matched.add(d["id"])
        else:
            item["priority"] = None
        pending.append(item)

    for d in detailed:
        if d["id"] in matched:
            continue
        pending.append({
            "item": d["topic"], "src": d["src"],
            "priority": d["priority"], "options_count": len(d["options"]),
            "recommend": d["recommend"], "detail_ref": d["id"],
            "status": d["status"], "adopted": d.get("adopted"),
            "new_in_phase2": True,
        })

    # 按优先级排序（P0 → P3 → 未分级）
    _pri = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    pending.sort(key=lambda x: (_pri.get(x.get("priority"), 9), x.get("detail_ref") or "zz"))

    doc = {
        "meta": {
            **D.META,
            "purpose": "已确定项 / 待定项 / 修正项 三态清单",
            "pending_sources": "kb_data.PENDING（S2 原清单）+ kb_pending.PENDING（阶段二扩充的 29 条权威清单）",
        },
        "confirmed": D.CONFIRMED,
        "pending": pending,
        "resolved_pending": resolved,
        "conflicts": D.CONFLICTS,
        "revisions": D.REVISIONS,
        "s3_revision_table": D.S3_REVISION_TABLE,
        "status_matrix_overview": {
            "已确定": "文档中明确写定，可直接当正典使用",
            "待定": "文档中明确标注为未定 / 待进一步确定 / 🟡 已提出但细节未定",
            "修正": "后续文档明确覆盖或改写了先前条款",
        },
    }

    md = ["# 设定集三态清单：已确定项 / 待定项 / 修正项", "",
          "> 三态定义：**已确定** = 可直接当正典使用；**待定** = 文档明确标注未定；"
          "**修正** = 后续文档明确覆盖/改写先前条款。", ""]

    md.append(f"## 一、已确定项（{len(D.CONFIRMED)} 条）")
    md.append("")
    md.append("来源以《设定集补充2》第三十一节 🟢 清单为主，并补入 S3、S4 明确敲定的条款。")
    md.append("")
    for i, c in enumerate(D.CONFIRMED, 1):
        md.append(f"{i}. {c}")
    md.append("")

    md.append(f"## 二、待定项（{len(pending)} 条）")
    md.append("")
    md.append("> 优先级与方案详见 `docs/pending_decisions.md`；勾选裁定见 `docs/pending_checklist.md`。")
    md.append("")
    md.append(md_table(["#", "优先级", "待定项", "出处", "方案数", "推荐方案 / 已被后续文档部分解决"],
                       [[i,
                         p.get("priority") or "—",
                         p["item"],
                         "、".join(p["src"]),
                         p.get("options_count") or "—",
                         (p.get("recommend") or p.get("resolved_by") or "—")]
                        for i, p in enumerate(pending, 1)]))
    md.append("")
    md.append("### 待定项按优先级分布")
    md.append("")
    pri_dist = defaultdict(list)
    for p in pending:
        pri_dist[p.get("priority") or "未分级"].append(p["item"])
    md.append(md_table(["优先级", "条数", "待定项"],
                       [[k, len(v), "；".join(x[:38] + ("…" if len(x) > 38 else "") for x in v)]
                        for k, v in sorted(pri_dist.items())]))
    md.append("")
    md.append("### 待定项按来源分布")
    md.append("")
    dist = defaultdict(list)
    for p in pending:
        for s in p["src"]:
            dist[s].append(p["item"])
    md.append(md_table(["来源", "条数", "待定项"],
                       [[k, len(v), "；".join(v)] for k, v in sorted(dist.items())]))
    md.append("")

    md.append(f"## 三、修正项与冲突记录（{len(D.CONFLICTS)} 条冲突 + {len(D.REVISIONS)} 条修订）")
    md.append("")
    md.append("### 3.1 条款冲突与覆盖")
    md.append("")
    for c in D.CONFLICTS:
        md.append(f"#### `{c['id']}`　{c['topic']}　（状态：{c['status']}）")
        md.append(f"- **原条款**：{c['clause_old']}")
        md.append(f"- **改后条款**：{c['clause_new']}")
        md.append(f"- **裁定**：{c['resolution']}")
        md.append(f"- **出处**：{'、'.join(c['src'])}")
        md.append("")
    md.append("### 3.2 修订条目汇总")
    md.append("")
    md.append(md_table(["编号", "修订对象", "出处"],
                       [[r["id"], r["topic"], "、".join(r["src"])] for r in D.REVISIONS]))
    md.append("")
    md.append("### 3.3 《设定集补充3》R1–R7 修订清单（原文照录）")
    md.append("")
    md.append(md_table(["编号", "覆盖对象", "原条款", "修订后"],
                       [[r["编号"], r["覆盖对象"], r["原条款"], r["修订后"]] for r in D.S3_REVISION_TABLE]))
    md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return doc, "\n".join(md)


def _src_legend():
    lines = ["## 出处代号", ""]
    for s in D.META["source_documents"]:
        lines.append(f"- **{s['id']}** = `{s['file']}`（{s['title']}）")
    return "\n".join(lines)


# ---------------------------------------------------------------- 7. 关系网文档
def build_relations_doc(graph):
    md = ["# 图数据库关系总览", "",
          f"> 节点 {graph['meta']['node_count']} 个，边 {graph['meta']['edge_count']} 条。",
          "> 四个子图：人物与家族关系网、国家关系网、事件因果关系链、历史物品留存网。", ""]

    for name, view in graph["views"].items():
        md.append(f"## {name}")
        md.append("")
        md.append(f"{view['description']}")
        md.append("")
        edges = view["edges"]
        md.append(f"边数：**{len(edges)}**")
        md.append("")
        rows = []
        for e in edges:
            f = REG.get(e["from"], {})
            t = REG.get(e["to"], {})
            rows.append([
                e.get("id") or "(auto)",
                e["kind"],
                f"{f.get('name_zh', e['from'])}",
                f"{t.get('name_zh', e['to'])}",
                e.get("label") or "",
                e.get("time") or "",
                e.get("status") or "",
            ])
        md.append(md_table(["边ID", "关系类型", "起点", "终点", "说明", "时期", "状态"], rows))
        md.append("")

    # 人物家族关系网 ASCII 树
    md.append("## 人物与家族关系网 · 结构化视图")
    md.append("")
    md.append("### 哈布斯堡 → 法兰克王统")
    md.append("")
    md.append("```")
    md.append("鲁道夫之母（卡佩旁系公主）")
    md.append("        │")
    md.append("        ▼")
    md.append("    鲁道夫 ──(妻)── 勃艮第伯爵之女")
    md.append("     │ 1272 加冕为法兰克人的国王")
    md.append("     ▼")
    md.append("  阿尔布雷希特 ──(妻)── 让娜（香槟女继承人）")
    md.append("     │  ⇒ 哈布斯堡合法吞并香槟")
    md.append("     ▼")
    md.append("  …（世系未载）…")
    md.append("     ▼")
    md.append("  阿尔布雷希特二世（皇帝，年老无嗣）")
    md.append("     │ 1356 召集法兰克福会议")
    md.append("     ├── 一女（未具名）──(婿，未具名)")
    md.append("     ▼")
    md.append("  1356《法兰克福宪章》⇒ 双重王冠 + 双轨继承 + 三重加冕")
    md.append("     ▼ 14世纪后期")
    md.append("  哈布斯堡取得皇帝位 ⇒ 双元君主国（至1871）")
    md.append("     ▼")
    md.append("  1871 法兰克与德意志王冠分离 ⇒ 法兰克立宪君主国")
    md.append("     ▼ 1918 失去统治 ⇒ 法兰克共和国 ⇒ 1945 复辟 ⇒ 礼仪性君主制")
    md.append("```")
    md.append("")
    md.append("### 卡佩绝嗣与继承争夺")
    md.append("")
    md.append("```")
    md.append("路易九世")
    md.append("   ▼")
    md.append("腓力三世（早逝）")
    md.append("   ├── 腓力四世（夭折或仅有女嗣）")
    md.append("   ├── 查理（夭折或仅有女嗣）")
    md.append("   └── 路易（夭折或仅有女嗣）")
    md.append("   ⇒ 萨利克法下卡佩直系断绝（1270）")
    md.append("")
    md.append("继承争夺者：")
    md.append("  瓦卢瓦的查理      ┐")
    md.append("  埃夫勒的腓力      │")
    md.append("  布列塔尼公爵      ├─→ 哈布斯堡的鲁道夫【胜】─→ 1272 法兰克人的国王")
    md.append("  英格兰爱德华一世  │      （母系卡佩血统 + 勃艮第联姻 + 阿尔萨斯/瑞士军事资源）")
    md.append("  哈布斯堡的鲁道夫  ┘")
    md.append("```")
    md.append("")
    md.append("### 普热米斯尔 → 德意志皇统")
    md.append("")
    md.append("```")
    md.append("奥托卡二世（波希米亚国王）")
    md.append("   │ 1273 成为德意志最强势候选人")
    md.append("   │ 掌波希米亚 + 奥地利 + 施蒂利亚")
    md.append("   ▼ 约1290 罗马加冕为神圣罗马帝国皇帝")
    md.append("普热米斯尔王朝")
    md.append("   │ 14—15世纪 波西米亚/奥地利德意志化")
    md.append("   │ 16世纪 皈依路德宗-胡斯派混合信条")
    md.append("   ▼ 17世纪 泛德意志新教世界最高世俗领袖")
    md.append("   │ 1866 奥法战争击败法兰克、夺取北意大利")
    md.append("   ▼ 1871 罗马加冕 ⇒ 德意志帝国（维也纳行政首都 / 罗马加冕圣城）")
    md.append("   ▼ 1918 王朝结束 ⇒ 维也纳德意志共和国 ⇒ 1945 联邦化")
    md.append("```")
    md.append("")
    md.append("### 金雀花 → 蒙福尔（不列颠王统）")
    md.append("")
    md.append("```")
    md.append("金雀花王朝（12—13世纪跨海帝国）")
    md.append("   │ 爱德华一世：卡佩继承争夺者之一")
    md.append("   ▼ 1272 败于鲁道夫、被逐出大陆")
    md.append("   │ ⇒ 诺曼-法兰西精英退回不列颠（逆向的诺曼征服）")
    md.append("   ▼ 13—15世纪 绝对主义奠基（废贵族宪章、停开等级会议）")
    md.append("   ▼ 16世纪 王室宗教改革：国王为教会最高元首")
    md.append("   ▼ 17—18世纪 绝对主义鼎盛（宫廷古典主义、海外殖民）")
    md.append("   ▼ 约1789—1815 金雀花倾覆")
    md.append("蒙福尔王朝（源自法兰西 Montfort-l'Amaury，英语化拼写 Mountfort）")
    md.append("   ▼ 1815后 反革命时代加固绝对主义")
    md.append("   ▼ 1914—1918 一战获胜 ⇒ 旧制度固化")
    md.append("   ▼ 1939—1945 二战战败 ⇒ 王权合法性崩溃")
    md.append("   ▼ 1945 制宪会议 + 全民公决 ⇒ 废除王位 ⇒ 不列颠联邦共和国")
    md.append("```")
    md.append("")
    md.append("### 蒙古 → 金帐汗国 → 罗斯兀鲁思")
    md.append("")
    md.append("```")
    md.append("蒙古帝国（长生天 + 佛教 + 萨满 三层结构）")
    md.append("   ▼ 13世纪西征")
    md.append("金帐汗国（14世纪未伊斯兰化）")
    md.append("   │ 制度化/官僚化/地方化：任命大公、税收、道路、驿站、贵族等级")
    md.append("   ▼ 莫斯科成为最重要的斯拉夫代理政权")
    md.append("莫斯科蒙古王朝（蒙古王族与莫斯科大公家族联姻融合）")
    md.append("   ▼ 金帐汗国政治覆灭（但文明传统被继承）")
    md.append("罗斯兀鲁思（后基辅罗斯国家）")
    md.append("   │ 一战：重新夺取基辅、白罗斯")
    md.append("   ▼ 二战：基辅王国 + 白罗斯再次脱离")
    md.append("   ⇒ 欧洲—亚洲政治文明边界之一")
    md.append("```")
    md.append("")
    md.append("---")
    md.append("")
    md.append(_src_legend())
    return "\n".join(md)


# ---------------------------------------------------------------- 主流程
def main():
    print("== 构建实体总表 ==")
    entities = build_entities()
    wjson("entities.json", entities)
    print(f"   实体 {entities['total']} 条：{entities['counts']}")

    print("== 构建图数据库 ==")
    graph, dangling = build_graph()
    wjson("graph.json", graph)
    print(f"   节点 {graph['meta']['node_count']}，边 {graph['meta']['edge_count']}")
    if dangling:
        print(f"   !! 悬空引用 {len(dangling)} 条")

    print("== 构建四张表 ==")
    tables = {}
    for fn, key in ((build_timeline_table, "timeline"),
                    (build_country_table, "countries"),
                    (build_people_table, "people"),
                    (build_war_table, "wars")):
        doc, md = fn()
        tables[key] = doc
        wjson(f"table_{key}.json", doc)
        wtext(os.path.join(DOCS, f"table_{key}.md"), md)
        print(f"   table_{key}: {len(doc['rows'])} 行")
    wjson("tables.json", {
        "meta": D.META,
        "timeline": tables["timeline"],
        "countries": tables["countries"],
        "people": tables["people"],
        "wars": tables["wars"],
    })

    print("== 构建对照表 ==")
    gl, gl_md = build_glossary()
    wjson("glossary.json", gl)
    wtext(os.path.join(DOCS, "glossary_zh_en_de.md"), gl_md)
    print(f"   对照条目 {len(D.GLOSSARY)}")

    print("== 构建地名转写表 ==")
    tl, tl_md = build_transliteration()
    wjson("transliteration.json", tl)
    wtext(os.path.join(DOCS, "transliteration.md"), tl_md)
    print(f"   地名 {len(tl['places'])}")

    print("== 构建索引 ==")
    idx, entries, sections = build_index()
    wjson("index.json", idx)
    wtext(os.path.join(DOCS, "index.md"), index_markdown(entries, sections))
    wtext(os.path.join(DOCS, "index.html"), build_index_html(entries))
    print(f"   索引条目 {len(entries)}")

    print("== 构建三态清单 ==")
    st, st_md = build_status_doc()
    wjson("status.json", st)
    wtext(os.path.join(DOCS, "status_confirmed_pending_revisions.md"), st_md)
    print(f"   已确定 {len(D.CONFIRMED)} / 待定 {len(D.PENDING)} / 冲突 {len(D.CONFLICTS)}")

    print("== 构建关系总览 ==")
    wtext(os.path.join(DOCS, "graph_relations.md"), build_relations_doc(graph))

    print("\n全部产物已生成。")
    return dangling


if __name__ == "__main__":
    d = main()
    if d:
        print("\n悬空引用：")
        for x in d:
            print("  ", x)
        sys.exit(2)
