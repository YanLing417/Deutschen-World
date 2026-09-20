# -*- coding: utf-8 -*-
"""
裁定驱动的新增/改写内容（2026 轮）
====================================
本模块承载用户裁定后需要新增或改写的实体，由 tools/build.py 合并进主数据层。

覆盖条目：P5 / P6 / P10 / P13 / P14 / P16 / P27 / P37
"""

# ============================================================
# P5：佛教-西域波斯残余（「波斯」概念的另一半）
# ============================================================
COUNTRIES = [
    {
        "id": "C_PERSIA_BUDDHIST", "name_zh": "西域-波斯（佛教波斯残余）", "name_short": "西域-波斯",
        "name_de": "Westland-Persien (buddhistisches Persien)", "name_local": "پارس بودایی",
        "name_en": "Western-Persia (Buddhist Persia)", "name_en_short": "Buddhist Persia",
        "polity": "波斯遗民的佛教政权；据河中及以东，与西域佛教文明带连为一体",
        "polity_en": "Buddhist polity of the Persian remnant, holding Transoxiana and eastward",
        "dynasty": None, "dynasty_id": None,
        "religion": "佛教（兼存波斯传统宗教与摩尼教、祆教残余）", "religion_id": "R_BUDDHISM",
        "capital": "撒马尔罕（推定）", "capital_id": "P_SAMARKAND",
        "capital_note": "文档未指定首都；撒马尔罕为河中地区中心的推定",
        "territory": "河中地区（阿姆河—锡尔河之间）、呼罗珊东部；东与西域佛教文明带相连",
        "territory_axis": "中亚西部—中亚东部之间；伊斯兰文明与西域佛教带的过渡地带",
        "language": "波斯语（佛教与行政语域）；兼用西域诸语", "language_id": None,
        "peoples": ["波斯遗民", "粟特人", "河中诸族"],
        "founded": "波斯抵御伊斯兰入侵失败后，因内乱退守河中及以东（具体年份待定）",
        "time_span": "8世纪后 — 至今",
        "overview": "「波斯」概念在本世界线中被撕裂为两支之一。波斯曾抵御伊斯兰入侵，"
                    "但最终因内乱而退守河中及以东地区，其遗民在此保持佛教，成为「西域-波斯」。"
                    "它把河中地区纳入佛教文明圈，从而与东侧的西域佛教文明带连成一片，"
                    "构成伊斯兰文明与东洲佛教世界之间的过渡地带。这正是用户裁定（P5）确立的结构。",
        "key_traits": ["「波斯」概念的另一半", "据河中及以东，与西域佛教带连为一体",
                       "伊斯兰文明与西域佛教之间的过渡地带", "波斯语高文化在佛教语境中延续"],
        "religions_detail": "佛教为主；波斯传统宗教（祆教、摩尼教）残余并存",
        "allies": ["C_WESTERN_REGIONS"],
        "enemies": ["C_PERSIA", "C_ABBASID", "C_ANATOLIAN_TURKS"],
        "wars": ["W_MONGOL_EXPANSION"],
        "treaties": [],
        "policies": [],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S1"],
        "notes": "本轮新增（用户裁定 P5）。S1 只记「中亚西部仍有较强伊斯兰影响」与「天山以东：佛教强」；"
                 "用户裁定把伊斯兰化边界定在波斯本体，波斯遗民退守河中并保持佛教，"
                 "本条目即该裁定的正典化。",
    },
]

PLACES = [
    {"id": "P_SAMARKAND", "type": "推定都城", "zh": "撒马尔罕", "real": "Samarkand",
     "de": "Samarkand", "en": "Samarkand", "fa": "سمرقند", "note": "河中地区中心（推定）",
     "country_id": "C_PERSIA_BUDDHIST", "src": ["S1"]},
    {"id": "P_BUCHARA", "type": "区域中心", "zh": "布哈拉", "real": "Bukhara",
     "de": "Buchara", "en": "Bukhara", "fa": "بخارا", "note": "河中地区中心",
     "country_id": "C_PERSIA_BUDDHIST", "src": ["S1"]},
    {"id": "P_KHORASAN", "type": "地区", "zh": "呼罗珊", "real": "Khorasan",
     "de": "Chorasan", "en": "Khorasan", "fa": "خراسان",
     "note": "波斯东部地区；本世界线中为佛教波斯残余的东翼",
     "country_id": "C_PERSIA_BUDDHIST", "src": ["S1"]},
]

# ============================================================
# P10：伊比利亚八大区（以山系/水系命名）
# ============================================================
IBERIAN_REGIONS = [
    {"name_zh": "杜罗大区", "name_de": "Duero-Region", "capital": "巴利亚多利德",
     "geometry": "杜罗河流域", "note": "卡斯蒂利亚北部核心"},
    {"name_zh": "埃布罗大区", "name_de": "Ebro-Region", "capital": "萨拉戈萨",
     "geometry": "埃布罗河流域", "note": "阿拉贡核心"},
    {"name_zh": "塔霍大区", "name_de": "Tajo-Region", "capital": "托莱多",
     "geometry": "塔霍河流域", "note": "半岛地理中心；伊比利亚王国故都所在"},
    {"name_zh": "瓜达尔基维尔大区", "name_de": "Guadalquivir-Region", "capital": "塞维利亚",
     "geometry": "瓜达尔基维尔河流域", "note": "安达卢斯核心；收复失地运动的终点区"},
    {"name_zh": "比利牛斯-北大区", "name_de": "Pyrenäen-Nordregion", "capital": "圣地亚哥-德孔波斯特拉",
     "geometry": "比利牛斯山脉与坎塔布连山脉以北", "note": "含加利西亚、巴斯克、纳瓦拉"},
    {"name_zh": "地中海大区", "name_de": "Mittelmeer-Region", "capital": "巴塞罗那",
     "geometry": "地中海沿岸", "note": "含加泰罗尼亚、瓦伦西亚"},
    {"name_zh": "海峡大区", "name_de": "Straßen-Region", "capital": "直布罗陀",
     "geometry": "直布罗陀海峡两岸", "note": "本土与北非的衔接点"},
    {"name_zh": "阿特拉斯大区", "name_de": "Atlas-Region", "capital": "马拉喀什",
     "geometry": "阿特拉斯山脉及马格里布西部", "note": "北非西部；与半岛同属一个国家行政体系"},
]

# ============================================================
# P16：蒙福尔王朝谱系（3—5 代具名君主）
#   命名规则（S3 已定）：法兰西贵族姓氏 + 英语化拼写
# ============================================================
MOUNTFORT_MONARCHS = [
    {
        "id": "PE_MOUNTFORT_I", "name_zh": "蒙福尔一世", "name_de": "Mountfort I.",
        "name_en": "Mountfort I", "title": "不列颠国王（蒙福尔王朝开国君主）",
        "title_de": "König von Britannien", "dynasty": "蒙福尔", "dynasty_id": "D_MOUNTFORT",
        "country_id": "C_UK",        "birth": "推定 1755 年", "death": "推定 1823 年（本轮新增，可调整）",
        "reign": "推定 1795 — 1823",
        "positions": ["不列颠国王"],
        "deeds": [
            "约1789—1815 政治动荡中，以「恢复秩序、对外抗击伊比利亚」为旗号上位",
            "加入反伊比利亚同盟，绝对主义渡过革命浪潮",
            "镇压曾短暂出现的共和派与议会派要求",
            "以诺曼-罗曼式「王在国中即皇帝」的主权观重建权威",
        ],
        "family": {"dynasty": "蒙福尔"},
        "context": "蒙福尔王朝开国君主。其家族源自法兰西贵族蒙福尔（Montfort，祖地帕里斯西侧），"
                   "姓名的英语化拼写为 Mountfort。",
        "status": "待定", "src": ["S3"],
        "notes": "本轮新增（用户裁定 P16）。姓名、生卒年与在位年为推定，可按需调整。",
    },
    {
        "id": "PE_MOUNTFORT_II", "name_zh": "蒙福尔二世", "name_de": "Mountfort II.",
        "name_en": "Mountfort II", "title": "不列颠国王",
        "title_de": "König von Britannien", "dynasty": "蒙福尔", "dynasty_id": "D_MOUNTFORT",
        "country_id": "C_UK",
        "birth": "推定 1786 年", "death": "推定 1851 年（本轮新增，可调整）",
        "reign": "推定 1823 — 1851",
        "positions": ["不列颠国王"],
        "deeds": [
            "1815 年后的反革命时代中进一步加固绝对主义",
            "1848 年大陆大德意志方案失败之际，镇压本土自由派，旧制度未动",
            "维持宫廷古典主义与盎格鲁语歌剧的高文化",
        ],
        "family": {"dynasty": "蒙福尔", "predecessor": "PE_MOUNTFORT_I"},
        "context": "蒙福尔王朝第二代。承接 1815 年后的反革命时代。",
        "status": "待定", "src": ["S3"],
        "notes": "本轮新增（用户裁定 P16），推定。",
    },
    {
        "id": "PE_MOUNTFORT_III", "name_zh": "蒙福尔三世", "name_de": "Mountfort III.",
        "name_en": "Mountfort III", "title": "不列颠国王",
        "title_de": "König von Britannien", "dynasty": "蒙福尔", "dynasty_id": "D_MOUNTFORT",
        "country_id": "C_UK",
        "birth": "推定 1820 年", "death": "推定 1893 年（本轮新增，可调整）",
        "reign": "推定 1851 — 1893",
        "positions": ["不列颠国王"],
        "deeds": [
            "绝对主义鼎盛期：宫廷古典主义、沙龙、海外殖民",
            "与伊比利亚、德意志争夺海权",
            "维持「海洋帝国天命」作为绝对主义的意识形态燃料",
        ],
        "family": {"dynasty": "蒙福尔", "predecessor": "PE_MOUNTFORT_II"},
        "context": "蒙福尔王朝第三代，绝对主义鼎盛期的君主。",
        "status": "待定", "src": ["S3"],
        "notes": "本轮新增（用户裁定 P16），推定。",
    },
    {
        "id": "PE_MOUNTFORT_IV", "name_zh": "蒙福尔四世", "name_de": "Mountfort IV.",
        "name_en": "Mountfort IV", "title": "不列颠国王",
        "title_de": "König von Britannien", "dynasty": "蒙福尔", "dynasty_id": "D_MOUNTFORT",
        "country_id": "C_UK",
        "birth": "推定 1862 年", "death": "推定 1943 年（本轮新增，可调整）",
        "reign": "推定 1893 — 1943",
        "positions": ["不列颠国王", "教会最高元首"],
        "deeds": [
            "1914—1918 一战中作为协约国成员获胜，战功增强王权合法性",
            "战时经济扩大国家能力，胜利固化旧制度",
            "战间期帝国鼎盛，绝对主义成为欧洲孤例",
            "1939—1945 二战中作为协约国成员参战并战败",
        ],
        "family": {"dynasty": "蒙福尔", "predecessor": "PE_MOUNTFORT_III",
                   "successor": "PE_MOUNTFORT_V"},
        "context": "蒙福尔王朝第四代。经历了「一战获胜固化旧制度 → 二战战败」的完整转折。",
        "status": "待定", "src": ["S3"],
        "notes": "本轮新增（用户裁定 P16），推定。S3 原文：「一战获胜使不列颠免于中欧那样的王朝终结；"
                 "直到二战落败，绝对主义才失去最后的正当性来源。」",
    },
    {
        "id": "PE_MOUNTFORT_V", "name_zh": "蒙福尔五世", "name_de": "Mountfort V.",
        "name_en": "Mountfort V", "title": "不列颠末代国王",
        "title_de": "letzter König von Britannien", "dynasty": "蒙福尔", "dynasty_id": "D_MOUNTFORT",
        "country_id": "C_UK",
        "birth": "推定 1901 年", "death": "推定 1968 年（本轮新增，可调整）",
        "reign": "推定 1943 — 1945（王位于 1945 年废除）",
        "positions": ["不列颠国王（末代）"],
        "deeds": [
            "1943 年继承王位，两年后即逢二战战败",
            "1945 年王权合法性崩溃，经制宪会议决议并辅以全民公决被正式废除王位",
            "退位后不列颠进入 1945—1955 年的监督过渡期",
        ],
        "family": {"dynasty": "蒙福尔", "predecessor": "PE_MOUNTFORT_IV"},
        "context": "蒙福尔王朝末代君主，也是不列颠历史上最后一位国王。",
        "status": "待定", "src": ["S3"],
        "notes": "本轮新增（用户裁定 P16），推定。其退位对应 S3「1945 年经制宪会议决议并辅以全民公决，"
                 "正式废除王位」。",
    },
]

# ============================================================
# P13 / P14：英联邦成员 + 爱尔兰语言与地位
# ============================================================
COMMONWEALTH_MEMBERS = [
    {"name_zh": "加拿大自治领", "name_de": "Kanadische Dominion", "note": "移民自治领"},
    {"name_zh": "澳大利亚自治领", "name_de": "Australische Dominion", "note": "移民自治领"},
    {"name_zh": "新西兰自治领", "name_de": "Neuseeländische Dominion", "note": "移民自治领"},
    {"name_zh": "南非自治领", "name_de": "Südafrikanische Dominion", "note": "移民自治领，含布尔人问题"},
    {"name_zh": "纽芬兰", "name_de": "Neufundland", "note": "岛屿领地"},
    {"name_zh": "马耳他", "name_de": "Malta", "note": "岛屿领地，地中海据点"},
    {"name_zh": "锡兰", "name_de": "Ceylon", "note": "岛屿领地，印度洋据点"},
]

# ============================================================
# P27：20 世纪近东民族国家格局
# ============================================================
NEAR_EAST_20C = [
    {"id": "C_ARAB_KINGDOM", "name_zh": "阿拉伯王国", "name_short": "阿拉伯王国",
     "name_de": "Arabisches Königreich", "name_local": "المملكة العربية",
     "name_en": "Arab Kingdom", "polity": "汉志与阿拉伯半岛的谢里夫王朝国家",
     "dynasty": "哈希姆系（推定）", "religion": "伊斯兰教（逊尼派）", "religion_id": "R_ISLAM",
     "capital": "麦加（推定）", "capital_id": "P_MECCA",
     "territory": "汉志、阿拉伯半岛西部与内陆", "language": "阿拉伯语",
     "overview": "20 世纪近东民族国家格局中的阿拉伯国家。由汉志的谢里夫政权升格而来，"
                 "控制麦加、麦地那两圣地。其诞生背景是安纳托利亚突厥帝国在 20 世纪的多极格局中"
                 "逐步失去对阿拉伯半岛的直接统治。",
     "status": "待定", "src": ["S1"], "notes": "本轮新增（用户裁定 P27）。" },
    {"id": "C_SYRIAN_REPUBLIC", "name_zh": "叙利亚共和国", "name_short": "叙利亚共和国",
     "name_de": "Syrische Republik", "name_local": "الجمهورية السورية",
     "name_en": "Syrian Republic", "polity": "议会制共和国",
     "dynasty": None, "religion": "伊斯兰教（逊尼派为主，多教派并存）", "religion_id": "R_ISLAM",
     "capital": "大马士革", "capital_id": "P_DAMASCUS",
     "territory": "黎凡特（叙利亚、巴勒斯坦、黎巴嫩沿海）", "language": "阿拉伯语",
     "overview": "20 世纪近东民族国家格局中的叙利亚国家。是法兰克东方学传统在 20 世纪的直接接触对象。",
     "status": "待定", "src": ["S1"], "notes": "本轮新增（用户裁定 P27）。" },
    {"id": "C_EGYPT_KINGDOM", "name_zh": "埃及王国", "name_short": "埃及王国",
     "name_de": "Königreich Ägypten", "name_local": "المملكة المصرية",
     "name_en": "Kingdom of Egypt", "polity": "君主立宪国",
     "dynasty": None, "religion": "伊斯兰教（逊尼派）；科普特教会并存", "religion_id": "R_ISLAM",
     "capital": "开罗", "capital_id": "P_CAIRO",
     "territory": "尼罗河流域、苏伊士地峡", "language": "阿拉伯语",
     "overview": "20 世纪近东民族国家格局中的埃及国家，控制苏伊士地峡——"
                 "东地中海与印度洋之间的关键通道。",
     "status": "待定", "src": ["S1", "S2"], "notes": "本轮新增（用户裁定 P27）。" },
    {"id": "C_IRAQ_KINGDOM", "name_zh": "两河王国", "name_short": "两河王国",
     "name_de": "Königreich Mesopotamien", "name_local": "المملكة العراقية",
     "name_en": "Kingdom of Mesopotamia", "polity": "君主立宪国",
     "dynasty": None, "religion": "伊斯兰教（逊尼派与什叶派并存）", "religion_id": "R_ISLAM",
     "capital": "巴格达", "capital_id": "P_BAGHDAD",
     "territory": "两河流域", "language": "阿拉伯语",
     "overview": "20 世纪近东民族国家格局中的两河国家，以巴格达为都——"
                 "阿拔斯哈里发国的故地。",
     "status": "待定", "src": ["S1"], "notes": "本轮新增（用户裁定 P27）。" },
]

# ============================================================
# P37：美国社会主义党的两阶段名称
# ============================================================
US_PARTY_STAGES = [
    {"phase": "早期（19世纪末—1930年代）", "name_en": "Socialist Party of America",
     "name_zh": "美国社会党", "note": "S2 所记「American Socialist Party」的早期形态"},
    {"phase": "改组后（1930年代以后）", "name_en": "Social Democratic Party of America (SDPA)",
     "name_zh": "美国社会民主党",
     "note": "与不列颠 SDP、德意志 DSP、法兰克 FSP、伊比利亚 PSI 同构（S3）"},
]
