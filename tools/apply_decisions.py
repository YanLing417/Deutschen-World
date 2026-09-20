# -*- coding: utf-8 -*-
"""
应用用户裁定结果（2026 轮）
============================
运行： python tools/apply_decisions.py   （幂等，可重复运行）

  A. 把裁定写回 kb_pending.PENDING 的 user_choice 字段
  B. 按裁定修改 kb_data.py / kb_extra.py 的正典内容
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kb_decisions as DEC  # noqa: E402

DATA_PY = os.path.join(HERE, "kb_data.py")
EXTRA_PY = os.path.join(HERE, "kb_extra.py")
PEND_PY = os.path.join(HERE, "kb_pending.py")
REPORT = []


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


def sub(s, old, new, tag):
    """替换；未命中时记为跳过（幂等：已替换过的自然未命中）。"""
    n = s.count(old)
    if n == 0:
        REPORT.append(("跳过", tag, old.replace("\n", "\\n")[:60]))
        return s
    REPORT.append(("已改", tag, f"{n}×"))
    return s.replace(old, new)


# ==================================================================
# A. 写回 user_choice
# ==================================================================
def apply_choices():
    s = read(PEND_PY)
    n = 0
    for pid, d in DEC.DECISIONS.items():
        m = re.search(r'(    \{\n        "id": "%s",.*?\n    \},\n)' % re.escape(pid), s, re.S)
        if not m:
            REPORT.append(("缺条目", f"A-{pid}", "kb_pending 中找不到"))
            continue
        blk = m.group(1)
        if '"user_choice": None' not in blk:
            REPORT.append(("跳过", f"A-{pid}", "已填过"))
            continue
        extra = ""
        if d.get("extra"):
            extra = ',\n        "user_choice_note": %s' % json.dumps(d["extra"], ensure_ascii=False)
        if d.get("merged_into"):
            extra += ',\n        "merged_into": "%s"' % d["merged_into"]
        newblk = blk.replace(
            '"user_choice": None',
            '"user_choice": %s' % json.dumps(d["choice"], ensure_ascii=False)
            + ',\n        "user_choice_type": "%s"' % d["type"] + extra,
            1)
        s = s.replace(blk, newblk, 1)
        n += 1
    write(PEND_PY, s)
    REPORT.append(("汇总", "A-写回裁定", f"{n} 条"))


# ==================================================================
# B. 正典修改
# ==================================================================
def apply_canon():
    s = read(DATA_PY)
    x = read(EXTRA_PY)

    # ---------------- P5：波斯分裂为「伊朗」与「佛教-西域波斯残余」（kb_extra） ----------------
    x = sub(x,
        '"id": "C_PERSIA", "name_zh": "波斯伊斯兰政权（伊朗）", "name_short": "波斯",',
        '"id": "C_PERSIA", "name_zh": "伊朗（伊斯兰什叶派波斯）", "name_short": "伊朗",',
        "P5-改名为伊朗")

    x = sub(x,
        '"overview": "伊朗高原上的伊斯兰政权序列。本世界线中波斯逐步形成什叶派国家传统，'
        '是伊斯兰文明内部与逊尼派阿拉伯—安纳托利亚体系并立的第二极。其东侧与中亚西部穆斯林地区接壤，'
        '而更东的西域则保持佛教——这正是 S1 所定的“伊斯兰文明东部边界”。",',
        '"overview": "「波斯」概念在本世界线中被撕裂为两支：一支是伊斯兰化的什叶派波斯，'
        '即本条目「伊朗」；另一支是退守河中及以东、保持佛教的「西域-波斯残余」'
        '（见 C_PERSIA_BUDDHIST）。波斯曾抵御伊斯兰入侵，后因内乱而退守河中及以东，'
        '伊朗遂成为伊斯兰文明东端的什叶派国家，与逊尼派的阿拉伯—安纳托利亚体系长期并立。",',
        "P5-概述改写")

    x = sub(x,
        '"key_traits": ["什叶派国家传统", "波斯语高文化", "与逊尼派阿拉伯—安纳托利亚体系并立", '
        '"东邻伊斯兰中亚西部，再东即西域佛教带"],',
        '"key_traits": ["什叶派国家传统（伊斯兰化的波斯）", "波斯语高文化", '
        '"与逊尼派阿拉伯—安纳托利亚体系并立", "其东侧紧邻退守河中的佛教-西域波斯残余"],',
        "P5-关键特征")

    x = sub(x,
        '"notes": "本轮新增（补全方向已定，具体王朝名待定）。S1 明列“伊朗：伊斯兰”为区域主导文明，'
        '并指出“中亚西部仍有较强伊斯兰影响”。",',
        '"notes": "S1 明列“伊朗：伊斯兰”为区域主导文明。用户本轮裁定（P5）：'
        '波斯曾抵御伊斯兰入侵，后因内乱退守河中及以东；「波斯」概念撕裂为'
        '伊斯兰什叶派波斯（即本条目「伊朗」）与佛教-西域波斯残余。",',
        "P5-备注")

    x = sub(x,
        '"allies": [], "enemies": ["C_ANATOLIAN_TURKS", "C_ABBASID"],',
        '"allies": [], "enemies": ["C_ANATOLIAN_TURKS", "C_ABBASID", "C_PERSIA_BUDDHIST"],',
        "P5-敌对关系")

    # ---------------- P6：安纳托利亚突厥帝国 → 奥斯曼 ----------------
    x = sub(x,
        '"id": "C_ANATOLIAN_TURKS", "name_zh": "安纳托利亚突厥帝国", "name_short": "安纳托利亚突厥",',
        '"id": "C_ANATOLIAN_TURKS", "name_zh": "奥斯曼帝国（安纳托利亚突厥帝国）", "name_short": "奥斯曼帝国",',
        "P6-国名")

    x = sub(x,
        '"name_de": "Anatolisches Türkenreich", "name_local": "Anadolu Türk İmparatorluğu",',
        '"name_de": "Osmanisches Reich", "name_local": "Osmanlı İmparatorluğu",',
        "P6-王朝名")

    x = sub(x,
        '"status": "已确定", "src": ["S1"],\n'
        '        "notes": "本轮新增（S1 方向已定，王朝名与建国细节待定）。S1《君士坦丁堡问题》',
        '"status": "已确定", "src": ["S1"],\n'
        '        "notes": "用户本轮裁定（P6）：采用「奥斯曼」（德语 Osmanen）。S1《君士坦丁堡问题》',
        "P6-备注")

    # ---------------- P11：奥克正常化 1972—1978 ----------------
    s = sub(s, '"year_text": "约1975年以后"',
            '"year_text": "1972—1978（1975 为关键节点）"', "P11-年份")
    s = sub(s, '"summary": "约1975年以后，帕里斯推动“奥克正常化”',
            '"summary": "1972—1978 年（1975 为关键节点），帕里斯推动“奥克正常化”', "P11-摘要")
    s = sub(s, '"name_zh": "奥克省废除与“奥克正常化”"',
            '"name_zh": "奥克省废除与“奥克正常化”（1972—1978）"', "P11-事件名")
    s = sub(s, '"abolition": "约1975年以后，帕里斯推动“奥克正常化”',
            '"abolition": "1972—1978 年（1975 为关键节点），帕里斯推动“奥克正常化”', "P11-废除说明")
    s = sub(s, '"notes": "S2 将“奥克正常化法案的确切年份”列为 🟡 待定（此处取“约1975年”）。",',
            '"notes": "S2 将“奥克正常化法案的确切年份”列为 🟡 待定；'
            '用户本轮裁定（P11）定为 1972—1978 年的渐进过程，1975 为地图节点。",', "P11-备注")

    # ---------------- P17：法兰克州名统一为德语读音译名 ----------------
    for a, b, tag in [
        ('"name_zh": "加来-皮卡第州"', '"name_zh": "卡莱斯-皮卡迪恩州"', "卡来-皮卡第"),
        ('"name_zh": "布列塔尼州（布里滕兰/布雷塔尼恩）"', '"name_zh": "布里滕兰州（布雷塔尼恩）"', "布列塔尼"),
        ('"name_zh": "勃艮第-弗朗什孔泰州（勃艮第-自由伯领）"', '"name_zh": "勃艮第-自由伯领州"', "勃艮第-自由伯领"),
        ('"name_zh": "卢瓦尔-奥尔良州（利格-奥尔伦）"', '"name_zh": "利格-奥尔伦州"', "利格-奥尔伦"),
        ('"name_zh": "卢瓦尔-曼恩州（利格-迈恩兰）"', '"name_zh": "利格-迈恩兰州"', "利格-迈恩兰"),
        ('"name_zh": "罗讷-阿尔卑斯州（罗登-阿尔卑斯）"', '"name_zh": "罗登-阿尔卑斯州"', "罗登-阿尔卑斯"),
        ('"name_zh": "香槟-阿登州"', '"name_zh": "尚帕尼恩-阿登州"', "尚帕尼恩-阿登"),
        ('"name_zh": "法兰西岛州（弗兰肯岛/弗兰肯兰）"', '"name_zh": "弗兰肯兰州（弗兰肯岛）"', "弗兰肯兰"),
        ('"name_zh": "弗兰德斯州（弗兰登）"', '"name_zh": "弗兰登州"', "弗兰登"),
        ('"name_zh": "诺曼底州（诺德曼兰）"', '"name_zh": "诺德曼兰州"', "诺德曼兰"),
    ]:
        s = sub(s, a, b, f"P17-{tag}")

    s = sub(s, '"name_zh": "法兰克立宪君主国行政区划"',
            '"name_zh": "法兰克立宪君主国行政区划（11 本土州；1975 年后含奥克五州共 16 州）"',
            "P7-州数标题")

    # ---------------- P22：基辅王国—白罗斯联邦 ----------------
    s = sub(s,
        '"polity": "缓冲国家（待定：是否与基辅王国组成联邦）",\n'
        '        "polity_en": "Buffer state (federation with Kyiv pending)",',
        '"polity": "与基辅王国组成联邦（基辅王国—白罗斯联邦的成员邦）",\n'
        '        "polity_en": "Member state of the Kyiv-White Rus federation",',
        "P22-政体")

    s = sub(s,
        '"overview": "位于基辅王国、莫斯科国与波罗的海世界之间的重要缓冲国家。'
        '合理方案为二战后与基辅王国同时脱离莫斯科国，并与基辅王国组成联邦，'
        '形成德意志/欧洲 → 基辅王国-白罗斯 → 罗斯兀鲁思 → 蒙古-西伯利亚文化圈的文明梯度。",\n'
        '        "key_traits": ["文明梯度缓冲国", "不应自动归入基辅王国"],',
        '"overview": "二战后与基辅王国同时脱离罗斯兀鲁思，并与基辅王国组成「基辅王国—白罗斯联邦」，'
        '成为德意志/欧洲 → 基辅王国-白罗斯 → 罗斯兀鲁思 → 蒙古-西伯利亚文化圈这一文明梯度的中间环。",\n'
        '        "key_traits": ["文明梯度缓冲国", "基辅王国—白罗斯联邦成员邦"],',
        "P22-概述")

    s = sub(s,
        '"status": "待定", "src": ["S4"],\n'
        '        "notes": "S4明示“最好不要简单把白罗斯自动归入基辅王国”，联邦方案属“一种合理方案”。",',
        '"status": "已确定", "src": ["S4"],\n'
        '        "notes": "用户本轮裁定（P22）：采用 S4 提出的联邦方案，成立基辅王国—白罗斯联邦。",',
        "P22-状态")

    # ---------------- P31：君士坦丁堡海峡政治体 ----------------
    s = sub(s,
        '"id": "C_BYZANTIUM", "name_zh": "拜占庭 / 君士坦丁堡海峡政治体", "name_short": "拜占庭",',
        '"id": "C_BYZANTIUM", "name_zh": "君士坦丁堡（海峡政治体，通称拜占庭）", "name_short": "君士坦丁堡",',
        "P31-国名")

    s = sub(s,
        '"polity": "待定：不恢复完整拜占庭帝国，而是保留一个具有战略意义的基督教君士坦丁堡/海峡政治体",\n'
        '        "polity_en": "Pending: a strategically significant Christian Constantinople/Straits polity '
        'rather than a restored full Byzantine Empire",',
        '"polity": "希腊人主导的基督教城邦—海峡政治体；以控制海峡通行权立国，'
        '靠海峡通行税与贸易维生",\n'
        '        "polity_en": "Greek-led Christian city-state controlling the Straits; '
        'sustained by transit tolls and trade",',
        "P31-政体")

    s = sub(s,
        '"status": "待定", "src": ["S1", "S4"],\n'
        '        "notes": "S1标注为【待进一步确定】；S4据此推断“东正教教会显然不会向莫斯科转移”。",',
        '"status": "已确定", "src": ["S1", "S4"],\n'
        '        "notes": "S1 标注为【待进一步确定】；用户本轮裁定（P31）采用方案A：'
        '希腊人主导的基督教城邦—海峡政治体，控制海峡通行权，被称为「君士坦丁堡」或「拜占庭」。'
        'S4 据此推断「东正教教会显然不会向莫斯科转移」。",',
        "P31-状态")

    # ---------------- P33：罗曼正统之争 → 正统错位 ----------------
    s = sub(s,
        '"status": "待定", "src": ["S3"],\n'
        '        "notes": "S3 将“罗曼正统之争”作为可深挖的接口提出，尚未正式敲定。",',
        '"status": "修正", "src": ["S3"],\n'
        '        "notes": "用户本轮裁定（P33/P21）：并非「双方争夺罗曼正统」，而是两者对自身身份的正相反认定'
        '——帕里斯不认为自己有罗曼正统，而自认是日耳曼世界的延伸；伦敦则放弃了日耳曼身份、'
        '更倾向于罗曼身份（但对大陆领土不做要求）。S3 原提法「伦敦与帕里斯之间的罗曼正统之争」'
        '据此修正为「正统错位（Orthodoxie-Verschiebung）」。",',
        "P33-裁定")

    s = sub(s,
        '"summary": "1272年鲁道夫击败诺曼底公爵后，英格兰被逐出大陆，英-法兰克竞争长期化。'
        '战后演变为伦敦与帕里斯之间的“罗曼正统之争”：法兰克是罗曼-法兰西领土上的日耳曼继承者，'
        '不列颠是罗曼高文化的实际保存者，两者的语言-文化竞赛（谁的正字法、谁的古典典范算正统）'
        '成为继“奥克问题”之后的第二条文化张力线。",',
        '"summary": "1272年鲁道夫击败诺曼底公爵后，英格兰被逐出大陆，英-法兰克竞争长期化。'
        '战后演变为一种「正统错位」：帕里斯自认是日耳曼世界的延伸（不主张罗曼正统），'
        '伦敦则放弃日耳曼身份、更倾向罗曼身份（但对大陆领土不做要求）。'
        '两者的语言-文化竞争成为继“奥克问题”之后的第二条文化张力线。",',
        "P33-事件摘要")

    s = sub(s,
        '"outcome": "长期文化张力线（文档称为“可以继续深挖的接口”）。",',
        '"outcome": "长期文化张力线；经用户本轮裁定（P33）明确为「正统错位」而非「双方争夺正统」。",',
        "P33-事件结果")

    write(DATA_PY, s)
    write(EXTRA_PY, x)


if __name__ == "__main__":
    print("== A. 写回 user_choice ==")
    apply_choices()
    print("== B. 应用正典修改 ==")
    apply_canon()
    print()
    for st, tag, msg in REPORT:
        if st != "跳过":
            print(f"  [{st}] {tag}: {msg}")
    skip = [r for r in REPORT if r[0] == "跳过"]
    print(f"\n跳过 {len(skip)} 处（多为已应用过）")
