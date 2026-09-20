# -*- coding: utf-8 -*-
"""
概述补全器
===========
为缺少 overview/summary 的实体生成说明性概述。

设计原则：
  1. 只使用该实体**已有的字段**组合成句，不引入任何新设定。
  2. 按类型采用不同句法，避免所有条目读起来一个腔调。
  3. 纯函数：不修改输入，由 build 管线在生成产物前调用。
  4. 已有 overview/summary 的实体一律不动。

用法（build.py 中）：
    import overview_filler as OF
    OF.fill(D)          # 就地补齐所有分组的缺概述条目
"""
import re

CN_NUM = "一二三四五六七八九十"


def _clean(s):
    """去掉字段值里的 markdown 强调与多余空白。"""
    if s is None:
        return ""
    s = str(s)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _join(parts, sep="。"):
    """把若干短句合成段落，自动去重、去空、补句号。"""
    out = []
    seen = set()
    for p in parts:
        p = _clean(p)
        if not p:
            continue
        if p[-1] not in "。！？；":
            p += "。"
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
    return "".join(out)


def _shrink(items, n=6, sep="、"):
    """截断过长列表，保持概述简短。"""
    if not isinstance(items, list):
        return _clean(items)
    vals = [_clean(x) for x in items if _clean(x)]
    if len(vals) > n:
        return sep.join(vals[:n]) + f"，等 {len(vals)} 项"
    return sep.join(vals)


# ---------------------------------------------------------------- 分类型生成
def ov_country(x):
    nm = x.get("name_zh", "")
    s = []
    if x.get("time_span"):
        s.append(f"{nm}存续期为 {_clean(x['time_span'])}")
    if x.get("polity"):
        s.append(f"政体为{_clean(x['polity'])}")
    if x.get("dynasty"):
        s.append(f"统治王朝为{_clean(x['dynasty'])}")
    if x.get("religion"):
        s.append(f"宗教上以{_clean(x['religion'])}为主")
    if x.get("capital") or x.get("capital_note"):
        cap = _clean(x.get("capital")) or _clean(x.get("capital_note"))
        s.append(f"首都为{cap}")
    if x.get("territory"):
        s.append(f"领土涵盖{_clean(x['territory'])}")
    if x.get("language"):
        s.append(f"语言为{_clean(x['language'])}")
    if x.get("peoples"):
        s.append(f"主要民族包括{_shrink(x['peoples'], 5)}")
    if x.get("key_traits"):
        s.append(f"其关键特征为{_shrink(x['key_traits'], 6)}")
    if x.get("religions_detail"):
        s.append(_clean(x["religions_detail"]))
    return _join(s)


def ov_dynasty(x):
    nm = x.get("name_zh", "")
    s = []
    if x.get("type"):
        s.append(f"{nm}属于{_clean(x['type'])}")
    if x.get("origin"):
        s.append(f"起源于{_clean(x['origin'])}")
    span = []
    if x.get("founded"):
        span.append(f"建立于 {_clean(x['founded'])}")
    if x.get("ends"):
        span.append(f"终结于 {_clean(x['ends'])}")
    if span:
        s.append("，".join(span))
    if x.get("polity"):
        ids = [i for i in x["polity"] if isinstance(i, str)]
        if ids:
            s.append(f"统治或关联的政治体包括 {_shrink(ids, 6)}")
    if x.get("religion"):
        s.append(f"信仰{_clean(x['religion'])}")
    if x.get("capital"):
        s.append(f"以{_clean(x['capital'])}为中心")
    if x.get("holdings"):
        s.append(f"领有{_shrink(x['holdings'], 6)}")
    if x.get("key_dates"):
        s.append(f"关键节点：{_shrink(x['key_dates'], 5)}")
    if x.get("members"):
        s.append(f"家族成员包括 {_shrink(x['members'], 8)}")
    return _join(s)


def ov_person(x):
    full = _clean(x.get("name_full_zh"))
    nm = full or _clean(x.get("name_zh"))
    s = []
    if x.get("title"):
        s.append(f"{nm}的身份是{_clean(x['title'])}")
    elif nm:
        s.append(nm)
    life = []
    if x.get("birth") and _clean(x["birth"]) != "文档未载":
        life.append(f"生于 {_clean(x['birth'])}")
    if x.get("death") and _clean(x["death"]) != "文档未载":
        life.append(f"卒于 {_clean(x['death'])}")
    if life:
        s.append("，".join(life))
    if x.get("reign") and "文档未载" not in _clean(x["reign"]):
        s.append(f"在位或活跃期为 {_clean(x['reign'])}")
    if x.get("dynasty"):
        s.append(f"属{_clean(x['dynasty'])}")
    if x.get("positions"):
        s.append(f"担任{_shrink(x['positions'], 4)}")
    if x.get("deeds"):
        s.append(f"主要事迹：{_shrink(x['deeds'], 4)}")
    if x.get("context"):
        s.append(_clean(x["context"]))
    return _join(s)


def ov_event(x):
    s = []
    if x.get("summary"):
        return _clean(x["summary"])
    nm = x.get("name_zh", "")
    s.append(f"{_clean(x.get('year_text') or x.get('year'))}，{nm}")
    if x.get("region"):
        s.append(f"发生于{_clean(x['region'])}")
    if x.get("outcome"):
        s.append(f"结果为{_clean(x['outcome'])}")
    if x.get("significance"):
        s.append(f"其意义在于{_clean(x['significance'])}")
    return _join(s)


def ov_war(x):
    s = []
    a = (x.get("side_a") or {}).get("name")
    b = (x.get("side_b") or {}).get("name")
    s.append(f"{x.get('name_zh','')}发生于 {_clean(x.get('time_text') or x.get('year_text'))}")
    if a and b:
        s.append(f"交战双方为{a}与{b}")
    if x.get("causes_text"):
        s.append(f"起因包括：{_shrink(x['causes_text'], 4)}")
    if x.get("result"):
        s.append(f"结果是{_clean(x['result'])}")
    if x.get("consequence"):
        s.append(f"后果：{_shrink(x['consequence'], 4)}")
    return _join(s)


def ov_treaty(x):
    s = []
    s.append(f"{x.get('name_zh','')}签订于 {_clean(x.get('time') or x.get('year_text'))}")
    if x.get("place"):
        s.append(f"签订地为{_clean(x['place'])}")
    if x.get("parties"):
        s.append(f"参与方包括{_shrink(x['parties'], 5)}")
    if x.get("background"):
        s.append(_clean(x["background"]))
    if x.get("significance"):
        s.append(f"其意义为{_shrink(x['significance'], 3)}")
    return _join(s)


def ov_religion(x):
    s = []
    if x.get("type"):
        s.append(f"{x.get('name_zh','')}属于{_clean(x['type'])}")
    if x.get("followers_regions"):
        s.append(f"主要信众分布于{_shrink(x['followers_regions'], 6)}")
    if x.get("doctrine"):
        s.append(f"教义要点：{_clean(x['doctrine'])}")
    if x.get("political_role"):
        s.append(f"政治角色：{_clean(x['political_role'])}")
    if x.get("culture"):
        s.append(f"文化表现：{_clean(x['culture'])}")
    return _join(s)


def ov_language(x):
    s = []
    if x.get("family"):
        s.append(f"{x.get('name_zh','')}属{_clean(x['family'])}")
    if isinstance(x.get("base"), str) and x["base"]:
        s.append(f"语言基础：{_clean(x['base'])}")
    if x.get("regions"):
        s.append(f"通行于{_shrink(x['regions'], 6)}")
    if x.get("principles"):
        s.append(f"规范原则：{_shrink(x['principles'], 5)}")
    if x.get("institution"):
        s.append(f"规范机构：{_clean(x['institution'])}")
    if x.get("sociolinguistics"):
        s.append(_clean(x["sociolinguistics"]))
    return _join(s)


def ov_place(x):
    s = []
    nm = x.get("zh", "")
    t = _clean(x.get("type"))
    note = _clean(x.get("note"))

    def real_ok(v):
        v = _clean(v)
        return bool(v) and v not in ("—", "-", nm, "（未指定，字面义“港口”）") and not v.startswith("（未指定")

    if t == "首都" and note:
        s.append(f"{nm}为{note}")
    elif note:
        s.append(f"{nm}（{t}）：{note}" if t else f"{nm}：{note}")
    elif t:
        s.append(f"{nm}是{t}")
    ext = []
    if x.get("de") and _clean(x["de"]) != nm:
        ext.append(f"德文 {_clean(x['de'])}")
    if x.get("en") and _clean(x["en"]) not in ("—", "-", nm):
        ext.append(f"英文 {_clean(x['en'])}")
    if real_ok(x.get("real")):
        ext.append(f"现实对应 {_clean(x['real'])}")
    if ext:
        s.append("；".join(ext))
    if x.get("zh_alias"):
        s.append(f"中文别名：{_shrink(x['zh_alias'], 4)}")
    return _join(s)


def ov_subdivision(x):
    s = []
    s.append(_clean(x.get("level_system")))
    units = x.get("units") or []
    if units:
        names = [_clean(u.get("name_zh")) for u in units if isinstance(u, dict)]
        s.append(f"下辖 {len(units)} 个单位：{_shrink(names, 6)}")
    if x.get("oct_province"):
        s.append("另设南部奥克省这一特殊建制（详见页内「南部奥克省」一节）")
    if x.get("constitution"):
        s.append(f"宪制安排：{_clean(x['constitution'])}")
    if x.get("issues"):
        s.append(f"相关问题：{_shrink(x['issues'], 4)}")
    return _join(s)


def ov_party(x):
    s = []
    if x.get("spectrum"):
        s.append(f"{x.get('name_zh','')}在政治光谱上属{_clean(x['spectrum'])}")
    if x.get("base"):
        s.append(f"社会基础与主张：{_shrink(x['base'], 7)}")
    if x.get("note"):
        s.append(_clean(x["note"]))
    return _join(s)


def ov_org(x):
    s = []
    if x.get("type"):
        s.append(f"{x.get('name_zh','')}属{_clean(x['type'])}")
    if x.get("function"):
        s.append(f"职能：{_clean(x['function'])}")
    if x.get("members"):
        s.append(f"成员或相关方：{_shrink(x['members'], 6)}")
    return _join(s)


def ov_artifact(x):
    s = []
    nm = x.get("name_zh", "")
    if x.get("kind"):
        s.append(f"{nm}属{x.get('kind')}类实物遗存")
    else:
        s.append(nm)
    if x.get("period"):
        s.append(f"年代：{_clean(x['period'])}")
    if x.get("material"):
        s.append(f"材质：{_clean(x['material'])}")
    if x.get("repository"):
        s.append(f"现藏：{_clean(x['repository'])}")
    if x.get("significance"):
        s.append(f"意义：{_clean(x['significance'])}")
    return _join(s)


def ov_axis(x):
    s = []
    s.append(f"「{x.get('name_zh','')}」是设定集《地图工程》横轴 12 项指标之一")
    if x.get("name_en"):
        s.append(f"英文作 {_clean(x['name_en'])}")
    s.append("每一项指标与纵轴的时间节点相乘，构成基础地图矩阵的一格")
    return _join(s)


FILLERS = {
    "COUNTRY": ov_country, "DYNASTY": ov_dynasty, "PERSON": ov_person,
    "EVENT": ov_event, "WAR": ov_war, "TREATY": ov_treaty,
    "RELIGION": ov_religion, "LANGUAGE": ov_language, "PLACE": ov_place,
    "SUBDIVISION": ov_subdivision, "PARTY": ov_party,
    "ORGANIZATION": ov_org, "AXIS_INDICATOR": ov_axis,
    "ARTIFACT": ov_artifact,
}

# 需要处理的实体分组（与 build.py 的 Entity 分组一致）
GROUPS = [
    ("COUNTRIES", "COUNTRY"), ("DYNASTIES", "DYNASTY"), ("PEOPLE", "PERSON"),
    ("EVENTS", "EVENT"), ("WARS", "WAR"), ("TREATIES", "TREATY"),
    ("RELIGIONS", "RELIGION"), ("LANGUAGES", "LANGUAGE"), ("PLACES", "PLACE"),
    ("SUBDIVISIONS", "SUBDIVISION"), ("PARTIES", "PARTY"),
    ("ORGANIZATIONS", "ORGANIZATION"), ("AXIS_INDICATORS", "AXIS_INDICATOR"),
    ("ARTIFACTS", "ARTIFACT"),
]

STATS = {}


def fill(D):
    """就地补齐 D 各分组中缺少 overview/summary 的条目，返回统计。"""
    STATS.clear()
    for attr, typ in GROUPS:
        items = getattr(D, attr, None)
        if not items:
            continue
        fn = FILLERS.get(typ)
        if not fn:
            continue
        done = 0
        for x in items:
            if not isinstance(x, dict):
                continue
            if _clean(x.get("overview")) or _clean(x.get("summary")):
                continue
            text = fn(x)
            if text:
                # 统一写入 overview；EVENT 用 summary 字段以兼容既有渲染
                if typ == "EVENT":
                    x["summary"] = text
                else:
                    x["overview"] = text
                x.setdefault("_overview_source", "auto")
                done += 1
        if done:
            STATS[typ] = done
    return STATS
