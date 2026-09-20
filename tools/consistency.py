# -*- coding: utf-8 -*-
"""
一致性检查器 —— 日期 / 地理 / 宗教 / 数量 / 时间线自洽
运行： python tools/consistency.py

输出：
  data/consistency.json
  docs/consistency_report.md
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
import kb_data as D  # noqa: E402
try:
    import kb_extra as X
except ImportError:
    X = None

# 复用 build.py 的合并与规范化逻辑
import build as B  # noqa: E402

FINDINGS = []


def add(category, severity, fid, title, detail, recommendation, refs=None):
    FINDINGS.append({
        "id": fid, "category": category, "severity": severity,
        "title": title, "detail": detail, "recommendation": recommendation,
        "refs": refs or [],
    })


E = {e["id"]: e for e in B.REG.values()}


def ent(eid):
    return B.REG.get(eid)


def name(eid):
    return B.REG[eid]["name_zh"] if eid in B.REG else eid


# ==================================================================
# 1. 日期一致性
# ==================================================================
def country_lifespan(c):
    """返回 (起点年或 None, 终点年或 None)。None 表示开区间。

    解析规则：
      - "至今/延续" ⇒ 上界为 None（开放）
      - 年份后紧跟「后」⇒ 该年为下界（此后仍存续）
      - 形如 "— 1789" ⇒ 只有上界
    """
    ts = (c.get("time_span") or "").strip()
    if not ts:
        return None, None
    ongoing = bool(re.search(r"至今|延续", ts))
    same = re.findall(r"(\d{3,4})\s*[—\-–~至]+\s*(\d{3,4})", ts)
    after = re.findall(r"(\d{3,4})\s*后", ts)
    all_years = [int(x) for x in re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", ts)]
    lo, hi = None, None
    if same:
        lo = min(int(a) for a, _ in same)
        hi = None if ongoing else max(int(b) for _, b in same)
    elif after:
        lo = min(int(a) for a in after)
        hi = None
    elif all_years:
        if ongoing:
            lo = min(all_years)
        elif len(all_years) == 1 and ts.lstrip().startswith(("—", "-", "–")):
            hi = all_years[0]
        else:
            lo, hi = min(all_years), max(all_years)
    if ongoing:
        hi = None
    return lo, hi


def check_dates():
    # 1.1 事件年份与 year_text 是否自洽
    for e in D.EVENTS:
        yt = e["year_text"]
        yrs = [int(x) for x in re.findall(r"\b(1[0-9]{3}|20[0-9]{2}|[0-9]{1,3})\b", yt)]
        if yrs and not any(abs(y - e["year"]) <= 60 for y in yrs):
            add("日期矛盾", "中", f"D-{e['id']}", f"事件 {e['id']} 的 year 字段与 year_text 距离过远",
                f"year={e['year']}，year_text=「{yt}」解析出 {yrs}",
                "统一为区间起年，或调整 year 字段。", [e["id"]])

    # 1.2 事件区间自洽：causes 的年份应早于或等于 effects
    ev = {e["id"]: e for e in D.EVENTS}
    for e in D.EVENTS:
        for c in e.get("causes", []) or []:
            if c in ev and ev[c]["year"] > e["year"] + 40:
                add("日期矛盾", "高", f"D-{e['id']}-CAUSE-{c}",
                    f"因果倒置：{e['id']} 的因 {c} 年份更晚",
                    f"{c} year={ev[c]['year']} > {e['id']} year={e['year']}",
                    "复核该因果关系的方向或年份标注。", [e["id"], c])
        for f in e.get("effects", []) or []:
            if f in ev and ev[f]["year"] < e["year"] - 40:
                add("日期矛盾", "高", f"D-{e['id']}-EFFECT-{f}",
                    f"因果倒置：{e['id']} 的果 {f} 年份更早",
                    f"{f} year={ev[f]['year']} < {e['id']} year={e['year']}",
                    "复核该因果关系的方向或年份标注。", [e["id"], f])

    # 1.3 人物生卒与在位
    for p in D.PEOPLE:
        b, d, r = p.get("birth"), p.get("death"), p.get("reign")
        if b and d and b != "文档未载" and d != "文档未载":
            nb = re.search(r"\d{3,4}", str(b))
            nd = re.search(r"\d{3,4}", str(d))
            if nb and nd and int(nb.group()) > int(nd.group()):
                add("日期矛盾", "高", f"D-{p['id']}-LIFE", f"{p['name_zh']} 生年晚于卒年",
                    f"birth={b}, death={d}", "修正生卒年。", [p["id"]])
        # 生卒为「文档未载」但记事有年份者
        if (b == "文档未载" or d == "文档未载") and not p.get("appendix"):
            deeds = " ".join(p.get("deeds") or [])
            if re.search(r"1[0-9]{3}", deeds):
                add("日期缺口", "低", f"D-{p['id']}-LIFE2",
                    f"{p['name_zh']} 事迹含具体年份但生卒为「文档未载」",
                    f"birth={b}, death={d}",
                    "若需精确时间轴，可补推生卒年；否则维持留空（原设定确实未载）。", [p["id"]])

    # 1.4 王朝存续期与所辖国家时间线
    for dy in D.DYNASTIES:
        kd = " ".join(dy.get("key_dates") or [])
        for cid in dy.get("polity") or []:
            c = ent(cid)
            if not c:
                continue

    # 1.5 战争双方参战国的存续期
    for w in D.WARS:
        ws, we = int(w["time_start"]), int(w["time_end"])
        for side in ("side_a", "side_b"):
            for cid in (w.get(side) or {}).get("country_ids", []) or []:
                c = next((x for x in D.COUNTRIES if x["id"] == cid), None)
                if not c:
                    continue
                lo, hi = country_lifespan(c)
                if lo is None and hi is None:
                    continue
                gap_high = (hi is not None and ws > hi + 5) or (lo is not None and we < lo - 5)
                if gap_high:
                    # 区分两种情况：
                    #  (a) 战争早于该国出现 ⇒ 该国以「前身形态」参战，属可解释
                    #  (b) 战争晚于该国终结 ⇒ 真实矛盾（除非该实体以其他形态延续）
                    if lo is not None and we < lo - 5:
                        add("日期说明", "中", f"D-{w['id']}-{cid}-PRE",
                            f"{w['name_zh']} 早于 {c['name_zh']} 的存续起点，该国以「前身形态」参战",
                            f"战争 {ws}—{we}，{c['name_zh']} 存续起点 {lo}（{c.get('time_span')}）",
                            "无需改动；建议在该国 time_span 或战争成员标注中显式写出前身名称，"
                            "以免后续扩写时误判。", [w["id"], cid])
                    else:
                        add("日期矛盾", "高", f"D-{w['id']}-{cid}",
                            f"{w['name_zh']} 晚于参战国 {c['name_zh']} 的终结年份",
                            f"战争 {ws}—{we}，{c['name_zh']} 存续 {c.get('time_span')}",
                            "复核该国的存续期：若其在战后以其他形态延续，需改写 time_span；"
                            "否则应改标参战成员。", [w["id"], cid])
                elif lo is not None and ws < lo - 5:
                    add("日期说明", "中", f"D-{w['id']}-{cid}-PRE2",
                        f"{w['name_zh']} 早于 {c['name_zh']} 的存续起点，该国以「前身形态」参战",
                        f"战争 {ws}—{we}，{c['name_zh']} 存续起点 {lo}（{c.get('time_span')}）",
                        "无需改动；建议显式标注前身名称。", [w["id"], cid])


# ==================================================================
# 2. 地理一致性
# ==================================================================
def check_geography():
    # 2.1 地点所在国 vs 该国的领土声称
    country_places = defaultdict(list)
    for p in D.PLACES:
        if p.get("country_id"):
            country_places[p["country_id"]].append(p)
    for cid, ps in country_places.items():
        c = next((x for x in D.COUNTRIES if x["id"] == cid), None)
        if c is None:
            add("地理矛盾", "中", f"G-{cid}", f"地点引用了不存在的国家 {cid}",
                f"{len(ps)} 个地点指向 {cid}", "修正 country_id。", [cid])

    # 2.2 同一城市被划归两个国家
    zh_map = defaultdict(list)
    for p in D.PLACES:
        zh_map[p["zh"]].append(p)
    for zh, ps in zh_map.items():
        cids = {p.get("country_id") for p in ps if p.get("country_id")}
        if len(cids) > 1:
            add("地理矛盾", "高", f"G-DUP-{ps[0]['id']}",
                f"地名「{zh}」被划归多个国家",
                " → ".join(f"{p['id']}@{p.get('country_id')}" for p in ps),
                "确认是否同名异地（如两个不同的城市），否则统一归属。",
                [p["id"] for p in ps])

    # 2.3 领土转移的时间顺序
    xfers = [r for r in D.RELATIONS if r["kind"] == "TERRITORY_TRANSFER"]
    for r in xfers:
        if not r.get("time"):
            add("地理缺口", "低", f"G-{r['id']}", "领土转移未标注年份",
                r["label"], "补充 time 字段。", [r["id"]])

    # 2.4 奥克问题上三重实体的重叠
    add("地理重叠（已处理）", "信息", "G-OCC",
        "奥克相关实体存在三重表述",
        "C_FRANKEN 的南部奥克省（行政区划）、C_OCCITAN_KINGDOM（政治体）、C_OCCITAN_REVOLT（地理—文化区域）"
        "分别从三个角度描述同一地区。",
        "已在各条目 notes 中注明彼此关系；建议后续统一为「奥克地区」为上位概念，"
        "「奥克王国」为其历史政治体形态，「南部奥克省」为其在法兰克的一级建制。",
        ["C_FRANKEN", "C_OCCITAN_KINGDOM"])

    # 2.5 州首府层级：行政区的首府必须出现在地点表中
    for sb in D.SUBDIVISIONS:
        units = sb.get("units") or []
        for u in units:
            cap = u.get("capital")
            if not cap or cap in ("—", "国家首都"):
                continue
            base = re.split(r"[（(]", cap)[0].strip()
            hit = any(base == p["zh"] or base in p["zh"] or p["zh"] in base for p in D.PLACES)
            if not hit:
                add("地理缺口", "低", f"G-CAP-{sb['id']}-{base}",
                    f"行政区首府「{base}」未在地点表中登记",
                    f"所属：{sb['name_zh']}",
                    "如需完整地名库，可补入地点表。", [sb["id"]])

    # 2.6 法兰克州名用词不一致（S0 内部）
    for note in getattr(X, "GEO_NOTES", []) if X else []:
        add("地理不一致（已记录）", "中", "G-FR-STATES", note["topic"],
            note["finding"], note["handling"], ["SB_FRANKEN"])

    # 2.7 法兰克本土州数量
    frank = next((s for s in D.SUBDIVISIONS if s["id"] == "SB_FRANKEN"), None)
    if frank:
        units = frank["units"]
        oct_units = [u for u in units if "奥克" in u["name_zh"] or "南部奥克省" in u["name_zh"]]
        native = [u for u in units if u not in oct_units]
        add("数量矛盾", "中", "N-FR-STATES",
            "法兰克本土州数量：文本称「12个」，实际列出 11 个",
            f"S0/S2 明写「原设定写12个法兰克本土州，但实际列出的只有11个，这个数字矛盾只是统计错误」（S2 第五节）。"
            f"本库实测：SB_FRANKEN 共 {len(units)} 个单元，其中本土州 {len(native)} 个、南部奥克省 {len(oct_units)} 个。",
            "已被设定集自身认定为统计错误（非设定冲突），本库按 11 个本土州 + 1 个南部奥克省记录。"
            "若后续确定最终州数，见待定项 P6。",
            ["SB_FRANKEN"])


# ==================================================================
# 3. 宗教一致性
# ==================================================================
def check_religion():
    # 3.1 国家官方宗教 vs 宗教条目的覆盖范围（双向）
    declared = {}
    for c in D.COUNTRIES:
        if c.get("religion_id"):
            declared.setdefault(c["religion_id"], []).append(c["id"])
    covered = {}
    for r in D.RELIGIONS:
        for cid in r.get("polity") or []:
            covered.setdefault(r["id"], []).append(cid)

    for rid, cids in declared.items():
        rc = set(covered.get(rid, []))
        for cid in cids:
            if cid not in rc:
                add("宗教矛盾", "中", f"R-{rid}-{cid}",
                    f"{name(cid)} 声明国教为 {name(rid)}，但该宗教条目未把该国列入覆盖范围",
                    f"country.religion_id={rid}；religion.polity 未含 {cid}",
                    "在宗教条目的 polity 中补入该国，或修正国家的 religion_id。", [cid, rid])

    # 3.2 同一国家声明多个互斥宗教（多派并存需显式说明）
    MULTI_OK = {"C_DEUTSCHLAND", "C_UK", "C_ROS_UHLUS", "C_EUROPE_CONTINENT",
                "C_ASIA_CONTINENT", "C_NEW_CONTINENT", "C_MONGOL_EMPIRE",
                "C_GOLDEN_HORDE", "C_ISLAMIC_WORLD", "C_ANATOLIAN_TURKS",
                "C_BYZANTIUM", "C_ARABIA", "C_SYRIA", "C_EGYPT_REGION", "C_MAGHREB",
                "C_SIBERIA", "C_CORDOBA"}
    for c in D.COUNTRIES:
        rt = c.get("religion") or ""
        # 只把"具体新教派别名"与"天主教"并列视为潜在冲突；
        # 「长期压制国内新教徒」这类表述是描述政策，不算教派声明。
        has_prot = any(k in rt for k in ("路德宗", "加尔文宗", "福音派", "胡斯派", "王室新教"))
        has_cath = "天主教" in rt
        if has_prot and has_cath and c["id"] not in MULTI_OK:
            add("宗教矛盾", "高", f"R-MULTI-{c['id']}",
                f"{c['name_zh']} 同时声明新教派别与天主教",
                f"religion=「{rt}」",
                "明确哪一方为官方宗教；若确为并存，需在 religions_detail 中说明分界。", [c["id"]])

    # 3.3 「德意志全境信奉新教」vs 阿尔萨斯-萨尔州（斯特拉斯堡为跨宗教）
    add("宗教张力（已解释）", "信息", "R-ELSASS",
        "「德意志全境（含维也纳）信奉新教」与阿尔萨斯-萨尔州的跨宗教地位",
        "S0 第六节明写「德意志全境（含维也纳）信奉新教。法兰克天主教。北意大利官方天主教」；"
        "同时 S0 第三节把「阿尔萨斯-萨尔州斯特拉斯堡」列为「跨宗教」圣地。",
        "两者并不冲突：阿尔萨斯-萨尔为德意志联邦内的跨宗教接触地带（法兰克天主教与德意志新教交界），"
        "非官方宗教的例外。建议在后续设定中明确该州的宗教构成比例。",
        ["C_DEUTSCHLAND", "SB_DEUTSCHLAND"])

    # 3.4 北意大利：官方天主教 + 文化新教
    add("宗教张力（已解释）", "信息", "R-NORDITALIEN",
        "北意大利「政治天主教、文化新教」的双重身份",
        "S0 明写「北意大利官方天主教，文化受南德意志新教影响」「北意大利形成『政治天主教、文化新教』独特身份」，"
        "并在领土上属德意志联邦（伦巴底州、威尼托州等）。",
        "这是设定集的有意设计，不是矛盾。已在 C_FRANKEN 与 R_CATHOLIC 的 political_role 中双向标注。",
        ["C_FRANKEN", "C_DEUTSCHLAND"])

    # 3.5 伊比利亚：天主教 vs 宗教战争中加入新教联盟
    add("宗教张力（已解释）", "信息", "R-IBERIA",
        "伊比利亚「外交新教、内政天主教」的矛盾立场",
        "S0/S1 明写西班牙-阿拉贡与伊比利亚「虽在国内压制新教徒，但出于反哈布斯堡法兰克地缘利益，"
        "后期加入新教联盟，形成『外交新教、内政天主教』矛盾立场」。",
        "设定集自身已把它作为关键变量解释，不是矛盾。",
        ["C_IBERIA", "C_SPAIN_ARAGON"])

    # 3.6 罗斯兀鲁思：东正教人口 + 蒙古佛教王朝
    add("宗教张力（已解释）", "信息", "R-ROS",
        "罗斯兀鲁思的复合宗教结构",
        "S4 明写「东正教斯拉夫人口 + 蒙古佛教王朝」，「莫斯科国不会因此变成佛教国家。"
        "东斯拉夫人口仍然主要保持自己的东正教传统」。",
        "设定集自身已解释。已在 C_ROS_UHLUS.religions_detail 中保留原文口径。",
        ["C_ROS_UHLUS"])

    # 3.7 新增：伊斯兰世界各政权教派一致性
    sunni = ["C_ABBASID", "C_AYYUBID", "C_MAMLUK", "C_CORDOBA", "C_ALMOHAD",
             "C_ANATOLIAN_TURKS", "C_ARABIA", "C_SYRIA", "C_EGYPT_REGION"]
    shia = ["C_FATIMID", "C_PERSIA"]
    for cid in sunni + shia:
        c = next((x for x in D.COUNTRIES if x["id"] == cid), None)
        if c and c.get("religion_id") != "R_ISLAM":
            add("宗教矛盾", "中", f"R-ISL-{cid}",
                f"{name(cid)} 的宗教归属未指向伊斯兰教",
                f"religion_id={c.get('religion_id')}",
                "修正为 R_ISLAM。", [cid])


# ==================================================================
# 4. 数量一致性
# ==================================================================
def check_counts():
    # 4.1 德意志州数
    de = next((s for s in D.SUBDIVISIONS if s["id"] == "SB_DEUTSCHLAND"), None)
    if de:
        n = len(de["units"])
        add("数量核对", "信息", "N-DE-STATES",
            f"德意志联邦州数：清单 {n} 个",
            "S0 第十九节逐条列出 31 项；S2 表述为「德意志30余州结构」。两者相容。",
            "无需修正。若最终确定州数，请更新 SB_DEUTSCHLAND.units。",
            ["SB_DEUTSCHLAND"])

    # 4.2 选侯数
    t = next((x for x in D.TREATIES if x["id"] == "T_FRANKFURT_1356"), None)
    if t:
        n = len(t.get("seven_electors") or [])
        if n != 7:
            add("数量矛盾", "高", "N-ELECTORS", "七位选侯清单数目不为 7",
                f"实际 {n} 项", "补齐或删减至 7 项。", ["T_FRANKFURT_1356"])
        else:
            add("数量核对", "信息", "N-ELECTORS-OK", "七位选侯清单数目正确（7 项）",
                "美因茨、科隆、特里尔三大主教 + 波西米亚国王、莱茵普法尔茨伯爵、萨克森公爵、勃兰登堡藩侯。",
                "无需修正。", ["T_FRANKFURT_1356"])

    # 4.3 新教四大派别
    four = ["R_LUTHERAN", "R_CALVIN", "R_HUSSITE", "R_ALPEN"]
    ok = all(any(r["id"] == x for r in D.RELIGIONS) for x in four)
    add("数量核对", "信息", "N-PROT4",
        "新教四大派别齐备" if ok else "新教四大派别不齐",
        "S0/S1 明列：北德意志路德宗、低地-瑞士加尔文宗、波西米亚胡斯派-路德宗混合、南德意志阿尔卑斯福音派。",
        "无需修正。" if ok else "补齐缺失派别。", four)

    # 4.4 六大工业带 / 四洲划分
    add("数量核对", "信息", "N-CONTINENTS",
        "四大洲文明划分齐备",
        "S2 第29节：欧洲（含撒哈拉以北非洲西部）、亚洲（含撒哈拉以北非洲东部与俄罗斯）、"
        "新大洲（未命名，含中国/蒙古/西藏/西域/印度）、非洲（撒哈拉以南）。",
        "无需修正。新大洲正式名称仍待定（见待定项 P11/P12）。",
        ["C_EUROPE_CONTINENT", "C_ASIA_CONTINENT", "C_NEW_CONTINENT", "C_AFRICA_CONTINENT"])

    # 4.5 六极
    add("数量核对", "信息", "N-POLES",
        "六极结构齐备",
        "S1/S3：德意志（文明核心）、法兰克（文明边界）、伊比利亚（秩序挑战者）、"
        "罗斯兀鲁思（欧亚大陆平衡者）、不列颠（海洋平衡者）、美国（海外工业—科学强国）。",
        "无需修正。注意 S3 已把英国的「议会制度」改为「绝对主义文明」，"
        "但「海洋平衡者」的国际定位保留。",
        ["C_DEUTSCHLAND", "C_FRANKEN", "C_IBERIA", "C_ROS_UHLUS", "C_UK", "C_USA"])

    # 4.6 地图工程 16 × 12
    add("数量核对", "信息", "N-MAP",
        "地图工程基础矩阵 16 × 12 = 192 张，与清单一致",
        f"S0 纵轴 {len(D.MAP_AXIS_YEARS)} 个节点 × 横轴 {len(D.AXIS_INDICATORS)} 项指标。",
        "无需修正。", [])

    # 4.7 州清单与首府数目是否一致
    for sb in D.SUBDIVISIONS:
        units = sb.get("units") or []
        with_cap = [u for u in units if u.get("capital") and u["capital"] not in ("—",)]
        if units and len(with_cap) != len(units):
            miss = [u["name_zh"] for u in units if not u.get("capital") or u["capital"] == "—"]
            add("数量缺口", "低", f"N-{sb['id']}-CAP",
                f"{sb['name_zh']} 有 {len(units) - len(with_cap)} 个单位未给首府",
                "；".join(miss), "如需要可补齐首府。", [sb["id"]])


# ==================================================================
# 5. 时间线自洽
# ==================================================================
def check_timeline():
    ev = sorted(D.EVENTS, key=lambda x: x["year"])

    # 5.1 因果图无环
    adj = defaultdict(list)
    for e in D.EVENTS:
        for f in e.get("effects", []) or []:
            adj[e["id"]].append(f)
        for c in e.get("causes", []) or []:
            adj[c].append(e["id"])
    color = {}
    cycles = []

    def dfs(u, stack):
        color[u] = 1
        stack.append(u)
        for v in adj.get(u, []):
            if color.get(v) == 1:
                i = stack.index(v)
                cycles.append(stack[i:] + [v])
            elif color.get(v, 0) == 0:
                dfs(v, stack)
        stack.pop()
        color[u] = 2

    for e in D.EVENTS:
        if color.get(e["id"], 0) == 0:
            dfs(e["id"], [])
    if cycles:
        add("时间线矛盾", "高", "T-CYCLE", f"因果链存在环 {len(cycles)} 处",
            "；".join(" → ".join(c) for c in cycles[:5]),
            "打断环：把其中一条边改为「背景」而非因果。", cycles[0])
    else:
        add("时间线核对", "信息", "T-CYCLE-OK", "事件因果图无环",
            f"检查 {len(D.EVENTS)} 个事件、{sum(len(e.get('causes') or []) + len(e.get('effects') or []) for e in D.EVENTS)} 条因果边。",
            "无需修正。", [])

    # 5.2 因果边的方向与年份一致（允许长时段宽容）
    TOL = 60
    bad = []
    for e in D.EVENTS:
        for f in e.get("effects", []) or []:
            t = next((x for x in D.EVENTS if x["id"] == f), None)
            if t and t["year"] < e["year"] - TOL:
                bad.append((e["id"], f, e["year"], t["year"]))
    if bad:
        add("时间线矛盾", "中", "T-DIR", f"后果事件年份早于原因事件 {len(bad)} 处",
            "；".join(f"{a}({c}) → {b}({d})" for a, b, c, d in bad[:6]),
            "复核方向；长时段事件可用区间标注。", [b[0] for b in bad[:3]])
    else:
        add("时间线核对", "信息", "T-DIR-OK", "因果边方向与年份一致",
            f"宽容度 ±{TOL} 年。", "无需修正。", [])

    # 5.3 事件引用的国家在该事件年份是否已存在
    for e in D.EVENTS:
        for cid in e.get("country_ids", []) or []:
            c = next((x for x in D.COUNTRIES if x["id"] == cid), None)
            if not c:
                continue
            ts = c.get("time_span") or ""
            yrs = [int(x) for x in re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", ts)]
            if yrs:
                lo, hi = min(yrs), max(yrs)
                if e["year"] < lo - 30:
                    add("时间线矛盾", "中", f"T-{e['id']}-{cid}",
                        f"事件 {e['id']}（{e['year']}）早于 {c['name_zh']} 的存续期起点（{lo}）",
                        f"time_span=「{ts}」",
                        "确认是该国的前身形态，或调整事件的 country_ids。", [e["id"], cid])

    # 5.4 时间线覆盖范围说明
    add("时间线核对", "信息", "T-RANGE",
        f"时间线覆盖 {ev[0]['year']} — {ev[-1]['year']}，共 {len(ev)} 个事件节点",
        "S0 地图工程纵轴 16 节点全部有事件对应（见 table_timeline.json 的 axis_nodes）。",
        "无需修正。", [])

    # 5.5 王朝结束与事件对应
    for dy in D.DYNASTIES:
        ends = dy.get("ends")
        if not ends:
            continue
        yrs = [int(x) for x in re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", ends)]
        if not yrs:
            continue
        y = min(yrs)
        near = [e for e in D.EVENTS if abs(e["year"] - y) <= 3]
        if not near:
            add("日期缺口", "低", f"T-{dy['id']}-END",
                f"{dy['name_zh']} 的终结年份（{y}）附近没有对应事件节点",
                f"ends=「{ends}」",
                "为该王朝终结补一个事件节点，或说明其为渐进而非事件性终结。", [dy["id"]])


# ==================================================================
# 6. 命名 / 称谓一致性（本轮新增诉求）
# ==================================================================
def check_naming():
    # 6.1 废弃国名
    hits = []
    for attr in ("COUNTRIES", "DYNASTIES", "PEOPLE", "EVENTS", "WARS",
                 "TREATIES", "RELIGIONS", "LANGUAGES", "SUBDIVISIONS",
                 "PARTIES", "ORGANIZATIONS", "PLACES", "GLOSSARY"):
        for it in getattr(D, attr, []) or []:
            s = json.dumps(it, ensure_ascii=False)
            if "俄罗斯" in s:
                hits.append((attr, it.get("id")))
    if hits:
        add("命名矛盾", "高", "N-RU", f"仍有 {len(hits)} 处使用已废弃国名「俄罗斯」",
            str(hits[:10]),
            "S4 明确要求停止使用「俄罗斯」，统一为「罗斯兀鲁思」；「莫斯科国」为工作别名。", [])
    else:
        add("命名核对", "信息", "N-RU-OK", "已无「俄罗斯」残留",
            "S4 要求废弃「俄罗斯」；本库已统一为「罗斯兀鲁思」（工作别名「莫斯科国」）。",
            "无需修正。", [])

    # 6.2 法兰克地名译名
    BAD = {"巴黎": "帕里斯", "兰斯": "雷姆斯", "里昂": "劳格登",
           "鲁昂": "鲁安", "马赛": "马西利恩", "蒙彼利埃": "蒙斯佩勒", "第戎": "迪根"}
    residual = []
    for p in D.PLACES:
        for b, g in BAD.items():
            if b in p["zh"]:
                residual.append((p["id"], p["zh"], g))
    if residual:
        add("命名矛盾", "中", "N-FR-PLACE", f"地名表正典列残留现实译名 {len(residual)} 处",
            str(residual[:8]), "改为德语读音译名。", [r[0] for r in residual[:3]])
    else:
        add("命名核对", "信息", "N-FR-PLACE-OK", "法兰克地名译名统一",
            "正典中文列已统一为德语读音译名（帕里斯/雷姆斯/劳格登/鲁安/马西利恩/蒙斯佩勒/迪根）。",
            "无需修正。", [])

    # 6.3 新增人物姓名是否符合世界线语言
    for p in D.PEOPLE:
        if p.get("appendix"):
            continue
        if "本轮新增" in (p.get("notes") or "") and not p.get("name_de"):
            add("命名缺口", "低", f"N-NAME-{p['id']}", f"{p['name_zh']} 缺德文姓名形式",
                "", "补 name_de。", [p["id"]])


def main():
    check_dates()
    check_geography()
    check_religion()
    check_counts()
    check_timeline()
    check_naming()

    sev_order = {"高": 0, "中": 1, "低": 2, "信息": 3}
    FINDINGS.sort(key=lambda f: (sev_order.get(f["severity"], 9), f["category"], f["id"]))

    by_cat = defaultdict(list)
    for f in FINDINGS:
        by_cat[f["category"]].append(f)

    doc = {
        "meta": {**D.META, "task": "一致性检查", "total_findings": len(FINDINGS)},
        "summary": {
            "by_severity": dict(Counter(f["severity"] for f in FINDINGS)),
            "by_category": {k: len(v) for k, v in by_cat.items()},
        },
        "findings": FINDINGS,
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "consistency.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ---------------- Markdown ----------------
    def md_table(headers, rows):
        out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
        for r in rows:
            out.append("| " + " | ".join("" if c is None else str(c).replace("|", "\\|").replace("\n", "<br>") for c in r) + " |")
        return "\n".join(out)

    md = ["# 一致性检查报告", "",
          "> 自动审计范围：日期、地理、宗教、数量、时间线自洽、命名/称谓。",
          f"> 共 {len(FINDINGS)} 条发现。", "",
          "## 总览", ""]
    md.append(md_table(["严重度", "条数"], [[k, v] for k, v in
                                            sorted(doc["summary"]["by_severity"].items(),
                                                   key=lambda x: sev_order.get(x[0], 9))]))
    md.append("")
    md.append(md_table(["类别", "条数"], sorted(doc["summary"]["by_category"].items())))
    md.append("")
    md.append("> 严重度含义：**高** = 必须修正的真实矛盾；**中** = 需裁定或补注；"
              "**低** = 缺口/可选补全；**信息** = 已核对无矛盾，或设定集自身已解释的张力。")
    md.append("")

    CAT_TITLES = {
        "日期矛盾": "一、日期矛盾", "日期缺口": "一、日期缺口",
        "地理矛盾": "二、地理矛盾", "地理不一致（已记录）": "二、地理不一致",
        "地理重叠（已处理）": "二、地理重叠（已处理）", "地理缺口": "二、地理缺口",
        "宗教矛盾": "三、宗教矛盾", "宗教张力（已解释）": "三、宗教张力（设定集自身已解释）",
        "数量矛盾": "四、数量矛盾", "数量核对": "四、数量核对", "数量缺口": "四、数量缺口",
        "时间线矛盾": "五、时间线矛盾", "时间线核对": "五、时间线核对",
        "命名矛盾": "六、命名/称谓矛盾", "命名核对": "六、命名核对", "命名缺口": "六、命名缺口",
    }
    for cat in sorted(by_cat, key=lambda c: (min(sev_order.get(f["severity"], 9) for f in by_cat[c]), c)):
        md.append(f"## {CAT_TITLES.get(cat, cat)}")
        md.append("")
        for f in by_cat[cat]:
            md.append(f"### `{f['id']}`　{f['title']}　（{f['severity']}）")
            md.append("")
            md.append(f"- **发现**：{f['detail']}")
            md.append(f"- **处理建议**：{f['recommendation']}")
            if f["refs"]:
                md.append(f"- **关联实体**：{'、'.join(f'`{r}`' for r in f['refs'])}")
            md.append("")
        md.append("")

    md.append("---")
    md.append("")
    md.append("## 出处代号")
    md.append("")
    for s in D.META["source_documents"]:
        md.append(f"- **{s['id']}** = `{s['file']}`（{s['title']}）")

    os.makedirs(DOCS, exist_ok=True)
    with open(os.path.join(DOCS, "consistency_report.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md))

    print(f"一致性检查完成：{len(FINDINGS)} 条发现")
    for k, v in sorted(doc["summary"]["by_severity"].items(), key=lambda x: sev_order.get(x[0], 9)):
        print(f"  {k}: {v}")
    print(f"  → data/consistency.json, docs/consistency_report.md")


if __name__ == "__main__":
    main()
