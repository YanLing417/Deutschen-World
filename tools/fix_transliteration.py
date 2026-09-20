# -*- coding: utf-8 -*-
"""
一次性数据规范化：把“描述性正典文本”中的法兰克地名统一为德语读音译名。
依据：S0 第四节「中文译名采用德语发音，如帕里斯而非巴黎，劳格登而非里昂」+
      S3「大陆法兰克地名沿用既定的德语读音译名」。
保留不动的部分：
  - 原文引述（CONFLICTS 的 clause_old / S3_R1-R7 原文 / X12 的对照说明）
  - 转写表中的 zh_alias「现实对应名」
  - 现实世界专名（法兰西岛、法国北方贵族等）
运行： python tools/fix_transliteration.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "kb_data.py")

REPS = [
    # 法兰克首都/王家城市
    ('"capital": "帕里斯（巴黎）"', '"capital": "帕里斯"'),
    ("加冕地为雷姆斯（Rems）；王家城市巴黎、兰斯、里昂由皇帝/国王直接管辖",
     "加冕地为雷姆斯（Rems）；王家城市帕里斯、雷姆斯、劳格登由皇帝/国王直接管辖"),
    ('"巴黎为时尚、外交、奢侈品、金融中心"', '"帕里斯为时尚、外交、奢侈品、金融中心"'),
    # 1272 加冕叙述
    ("法兰克人的国王（1272年在兰斯由兰斯大主教加冕）",
     "法兰克人的国王（1272年在雷姆斯由雷姆斯大主教加冕）"),
    ("1272年在兰斯大主教主持下加冕", "1272年在雷姆斯大主教主持下加冕"),
    ("定都巴黎", "定都帕里斯"),
    ("被兰斯大主教加冕", "被雷姆斯大主教加冕"),
    # 1356 宪章条款
    ("法兰克国王由兰斯大主教在雷姆斯加冕", "法兰克国王由雷姆斯大主教在雷姆斯加冕"),
    ("但巴黎、兰斯、里昂等王家城市仍由皇帝直接管辖",
     "但帕里斯、雷姆斯、劳格登等王家城市仍由皇帝直接管辖"),
    # 行政区划表：首府名
    ('"capital": "鲁昂（Ruan / Rodom）"', '"capital": "鲁安（Ruan / Rodom）"'),
    ('"capital": "兰斯（Rems）"', '"capital": "雷姆斯（Rems）"'),
    ('"capital": "南特（Nanten / Nant）"', '"capital": "南滕（Nanten / Nant）"'),
    ('"capital": "第戎（Digen / Divion）"', '"capital": "迪根（Digen / Divion）"'),
    ('"capital": "奥尔良（Orlen）"', '"capital": "奥尔伦（Orlen）"'),
    ('"capital": "里昂（Laugden / Luden）"', '"capital": "劳格登（Laugden / Luden）"'),
    ('"capital": "马赛（Massilien / Massel）"', '"capital": "马西利恩（Massilien / Massel）"'),
    ('"capital": "蒙彼利埃（Monspeler）"', '"capital": "蒙斯佩勒（Monspeler）"'),
    # 南部奥克省
    ('"note": "省总督由巴黎直接任命；1975年前后废除，原奥克各州升为普通联邦州"',
     '"note": "省总督由帕里斯直接任命；1975年前后废除，原奥克各州升为普通联邦州"'),
    ('"governor": "省长由巴黎任命"', '"governor": "省长由帕里斯任命"'),
    ("约1975年以后，巴黎推动“奥克正常化”", "约1975年以后，帕里斯推动“奥克正常化”"),
    ('"外交、国防、货币、海关、最高司法仍由巴黎掌握"',
     '"外交、国防、货币、海关、最高司法仍由帕里斯掌握"'),
    ('{"name_zh": "普罗旺斯（马赛）"', '{"name_zh": "普罗旺斯（马西利恩）"'),
    # 事件文本
    ('"region": "欧洲西部（雷姆斯/兰斯）"', '"region": "欧洲西部（雷姆斯）"'),
    ("兰斯大主教在部分贵族见证下为鲁道夫加冕", "雷姆斯大主教在部分贵族见证下为鲁道夫加冕"),
    ("巴黎中央政府 ↓ 法兰克本土各州，同时巴黎中央政府 ↓ 南部奥克省 ↓ 奥克各州",
     "帕里斯中央政府 ↓ 法兰克本土各州，同时帕里斯中央政府 ↓ 南部奥克省 ↓ 奥克各州"),
    ("核心矛盾不是“巴黎 vs 整个奥克地区”", "核心矛盾不是“帕里斯 vs 整个奥克地区”"),
    # 六极定位
    ('"traits": ["天主教", "哈布斯堡", "巴黎", "地中海", "奥克", "北非", "黎凡特", "西日耳曼语言"]',
     '"traits": ["天主教", "哈布斯堡", "帕里斯", "地中海", "奥克", "北非", "黎凡特", "西日耳曼语言"]'),
    # 城市平面图清单（S0 原文用现实英文名 Paris，此条不改）
]

# 州名中的现实译名（州名本身以德语读音译名为主，此处仅统一括号内首府）
EXTRA = [
    ('"capital": "鲁昂（Ruan / Rodom）"', '"capital": "鲁安（Ruan / Rodom）"'),
]

src = open(PATH, encoding="utf-8").read()
orig = src
report = []
for old, new in REPS:
    if old == new:
        continue
    n = src.count(old)
    if n == 0:
        report.append(("未命中", old[:60]))
        continue
    src = src.replace(old, new)
    report.append(("已替换", f"{n}× {old[:60]}"))

if src == orig:
    print("没有发生变化。")
else:
    open(PATH, "w", encoding="utf-8", newline="\n").write(src)
    print(f"已写回 {PATH}")

for status, msg in report:
    print(f"  [{status}] {msg}")
