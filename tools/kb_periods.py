# -*- coding: utf-8 -*-
"""
分期政治体层
==============
把「同一地区在不同时期的不同国名」拆成**独立而相互关联**的词条，
避免在其它页面混用（例如把 1918 年后的法兰克仍称作「法兰克王国」）。

命名口径（用户 2026 裁定）：
  · 分期年份按设定集 S0：一战 1914—1918，1918 年德意志帝国瓦解、
    成立维也纳德意志共和国、法兰克共和化 → 故政体分界取 **1918**。
  · 法兰西的罗曼时期定名「法兰西罗曼王国」，覆盖 **843—1270**
    （西法兰克王国 → 法兰西罗曼王国 → 卡佩绝嗣）。

本模块只新增/澄清国名与继承关系，不新增与 S0–S4 冲突的史实。
"""

# ============================================================
# 一、伊比利亚系
# ============================================================
COUNTRIES = [
    {
        "id": "C_SPAIN", "name_zh": "西班牙王国", "name_short": "西班牙",
        "name_de": "Königreich Spanien", "name_local": "Reino de España",
        "name_en": "Kingdom of Spain", "name_en_short": "Spain",
        "polity": "中央集权君主国（卡斯蒂利亚—莱昂王统）",
        "polity_en": "Centralising monarchy of the Castilian-Leonese line",
        "dynasty": "特拉斯塔马拉系（推定）", "dynasty_id": None,
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO",
        "capital_note": "后与阿拉贡合并，首都地位延续至伊比利亚王国时期",
        "territory": "卡斯蒂利亚、莱昂、加利西亚、安达卢斯北部",
        "territory_axis": "伊比利亚半岛中部与西北部",
        "language": "伊比利亚-奥克语（卡斯蒂利亚语域）", "language_id": "L_OCCITAN",
        "peoples": ["卡斯蒂利亚人", "莱昂人", "加利西亚人"],
        "founded": "卡斯蒂利亚与莱昂合并后形成",
        "time_span": "15世纪 — 16世纪初（并入西班牙-阿拉贡及奥克王国）",
        "overview": "伊比利亚半岛中部的中央集权君主国，是伊比利亚统一进程的两大起点之一。"
                    "它在收复失地运动中扩张最快，推动天主教共同身份的形成，并最终与阿拉贡合并。"
                    "其首都托莱多后来成为伊比利亚王国的首都。",
        "key_traits": ["伊比利亚统一的两个起点之一", "收复失地运动的主力", "中央集权传统的源头"],
        "religions_detail": "天主教；以宗教统一为立国原则之一",
        "allies": ["C_ARAGON"], "enemies": ["C_CORDOBA", "C_ALMOHAD"],
        "wars": ["W_RECONQUISTA"], "treaties": [],
        "policies": ["驱逐穆斯林", "同化地方势力"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增（分期拆分）。S0/S2 只记「西班牙-阿拉贡」为其前身；"
                 "此处把「西班牙」与「阿拉贡」拆为独立词条，便于区分不同时期的国名。",
    },
    {
        "id": "C_ARAGON", "name_zh": "阿拉贡王国", "name_short": "阿拉贡",
        "name_de": "Königreich Aragon", "name_local": "Reino de Aragón",
        "name_en": "Kingdom of Aragon", "name_en_short": "Aragon",
        "polity": "君主国（联姻与地中海扩张型）",
        "polity_en": "Monarchy expanding through marriage and the Mediterranean",
        "dynasty": "巴塞罗那系（推定）", "dynasty_id": None,
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "萨拉戈萨（推定）", "capital_id": "P_ZARAGOZA",
        "capital_note": None,
        "territory": "阿拉贡、加泰罗尼亚、瓦伦西亚；地中海属地",
        "territory_axis": "伊比利亚半岛东北部与西地中海",
        "language": "伊比利亚-奥克语（加泰罗尼亚语域）", "language_id": "L_OCCITAN",
        "peoples": ["阿拉贡人", "加泰罗尼亚人", "瓦伦西亚人"],
        "founded": "阿拉贡与巴塞罗那伯国联合后形成",
        "time_span": "12世纪 — 16世纪初（并入西班牙-阿拉贡及奥克王国）",
        "overview": "伊比利亚半岛东北部的君主国，伊比利亚统一进程的另一起点。"
                    "与卡斯蒂利亚方向不同，阿拉贡的扩张重心在地中海与南法，"
                    "因此与奥克语地区关系密切，是奥克最终卷入伊比利亚轨道的关键。",
        "key_traits": ["伊比利亚统一的两个起点之一", "地中海扩张型君主国",
                       "与奥克语地区的联系枢纽"],
        "religions_detail": "天主教",
        "allies": ["C_SPAIN", "C_OCCITAN_KINGDOM"], "enemies": ["C_ALMOHAD"],
        "wars": ["W_RECONQUISTA"], "treaties": [],
        "policies": ["地中海扩张", "与南法诸侯联姻"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增（分期拆分）。阿拉贡与奥克语地区的关系，解释了 S0 所记"
                 "「奥克语与伊比利亚半岛语言共享词汇语法」以及奥克王国为何并入伊比利亚。",
    },
    {
        "id": "C_IBERIA_1REP", "name_zh": "伊比利亚第一共和国", "name_short": "第一共和国",
        "name_de": "Erste Iberische Republik", "name_local": "Primera República Ibérica",
        "name_en": "First Iberian Republic", "name_en_short": "First Republic",
        "polity": "革命共和政体（1789 年大革命推翻伊比利亚王国后建立）",
        "polity_en": "Revolutionary republic established after 1789",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教（革命期一度推行国家教会化）", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO",
        "capital_note": "文档未指定；沿伊比利亚王国旧都",
        "territory": "伊比利亚半岛、北非西部；革命期曾占领奥克地区并攻入南意大利",
        "territory_axis": "西南欧 + 西地中海 + 西马格里布",
        "language": "伊比利亚-奥克语", "language_id": "L_OCCITAN",
        "peoples": ["伊比利亚人", "奥克人"],
        "founded": "1789（大革命推翻伊比利亚王国）",
        "time_span": "1789 — 约1804（转为伊比利亚第一帝国）",
        "overview": "伊比利亚大革命推翻王国后建立的第一个共和政体，是「伊比利亚共和国—帝国反复更替」"
                    "序列的起点。革命军自伊比利亚与奥克出发席卷南欧，攻入那不勒斯，"
                    "迫使神圣罗马帝国解散。该政体后由第一帝国取代。",
        "key_traits": ["伊比利亚革命政体的开端", "革命军远征南欧的发起点",
                       "民族主义、立宪主义、共和主义由此深入人心"],
        "religions_detail": "天主教为主；革命期推行教会财产国有化",
        "allies": [], "enemies": ["C_FRANKEN", "C_DEUTSCHLAND", "C_UK", "C_ROS_UHLUS"],
        "wars": ["W_REV_IBERIA"], "treaties": [],
        "policies": ["教会财产国有化", "对外革命输出"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增（分期拆分）。S0 记「伊比利亚第一共和国 → 第一帝国 → 第二共和国 → "
                 "第二帝国 → 第三/四/五共和国」，此处把每一阶段拆为独立词条。",
    },
    {
        "id": "C_IBERIA_1EMP", "name_zh": "伊比利亚第一帝国", "name_short": "第一帝国",
        "name_de": "Erstes Iberisches Kaiserreich", "name_local": "Primer Imperio Ibérico",
        "name_en": "First Iberian Empire", "name_en_short": "First Empire",
        "polity": "革命帝国（共和政体转向帝制）",
        "polity_en": "Revolutionary empire",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO", "capital_note": None,
        "territory": "伊比利亚半岛、北非西部、奥克地区；曾远征俄罗斯",
        "territory_axis": "西南欧 + 西地中海；一度伸入中欧与东欧",
        "language": "伊比利亚-奥克语", "language_id": "L_OCCITAN",
        "peoples": ["伊比利亚人", "奥克人"],
        "founded": "约1804（第一共和国转为帝制）",
        "time_span": "约1804 — 1815（被反伊比利亚同盟击败）",
        "overview": "伊比利亚革命政权的帝国阶段，也是其扩张的顶点。"
                    "它把大革命推向全欧，但其**远征俄罗斯最终失败**——"
                    "这与现实史中拿破仑远征的失败同构，是伊比利亚由盛转衰的转折。"
                    "1815 年被法兰克、普热米斯尔、英国、俄罗斯组成的反伊比利亚同盟击败。",
        "key_traits": ["伊比利亚扩张的顶点", "远征俄罗斯失败", "1815 年被反伊比利亚同盟击败"],
        "religions_detail": "天主教",
        "allies": [], "enemies": ["C_FRANKEN", "C_DEUTSCHLAND", "C_UK", "C_ROS_UHLUS"],
        "wars": ["W_REV_IBERIA"], "treaties": [],
        "policies": ["大陆封锁式经济政策", "革命输出的军事化"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增（分期拆分）。S0 明记「第一帝国大革命远征俄罗斯最终失败」。",
    },
    {
        "id": "C_IBERIA_2REP", "name_zh": "伊比利亚第二共和国", "name_short": "第二共和国",
        "name_de": "Zweite Iberische Republik", "name_local": "Segunda República Ibérica",
        "name_en": "Second Iberian Republic", "name_en_short": "Second Republic",
        "polity": "共和政体（拿破仑战争后重建）",
        "polity_en": "Republic restored after the Napoleonic wars",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教（压制国内新教徒）", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO", "capital_note": None,
        "territory": "伊比利亚半岛、北非西部",
        "territory_axis": "西南欧 + 西马格里布",
        "language": "伊比利亚-奥克语", "language_id": "L_OCCITAN",
        "peoples": ["伊比利亚人"],
        "founded": "1815（反伊比利亚战争结束、帝国倾覆后）",
        "time_span": "1815 — 19世纪中叶（转为伊比利亚第二帝国）",
        "overview": "拿破仑战争后重建的共和政体。它接过革命留下的民族主义、立宪主义与共和主义遗产，"
                    "但中央集权并未松动——S2 所记「中央集权从未真正逆转」正由此延续。"
                    "其长臂管辖一度伸至南意大利那不勒斯与罗马。",
        "key_traits": ["革命遗产的承接者", "中央集权延续", "长臂管辖伸至南意大利"],
        "religions_detail": "天主教；继续压制新教徒",
        "allies": [], "enemies": ["C_FRANKEN", "C_DEUTSCHLAND"],
        "wars": ["W_1866"], "treaties": [],
        "policies": ["中央集权", "对南意大利的长臂管辖"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增（分期拆分）。S0 记 1871 年普热米斯尔「攻入受伊比利亚第二帝国长臂管辖的"
                 "那不勒斯和罗马」，本条目即该长臂管辖的主体。",
    },
]

DYNASTIES = [
    {
        "id": "D_TRASTAMARA", "name_zh": "特拉斯塔马拉系（西班牙）",
        "name_de": "Haus Trastámara", "name_en": "House of Trastámara",
        "name_local": "Casa de Trastámara",
        "type": "王朝", "polity": ["C_SPAIN", "C_ARAGON", "C_IBERIAN_KINGDOM"],
        "origin": "卡斯蒂利亚王室的支系",
        "founded": "14世纪", "ends": "16世纪初（让位于伊比利亚王朝）",
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO",
        "key_dates": ["15世纪 卡斯蒂利亚与阿拉贡联姻", "15世纪末 完成半岛主要部分的统一",
                      "16世纪 南下北非"],
        "overview": "卡斯蒂利亚与阿拉贡两支王统，通过联姻把伊比利亚两大政治体合为一体，"
                    "是伊比利亚统一进程的直接执行者。其王统后来延续为伊比利亚王朝。",
        "holdings": ["卡斯蒂利亚", "莱昂", "阿拉贡", "加泰罗尼亚", "瓦伦西亚"],
        "members": ["PE_ISABELLA_VON_KASTILIEN"],
        "status": "已确定", "src": ["S2"],
        "notes": "本轮新增（分期拆分）。名字取自伊比利亚史上实际存在的王朝，属「以现实史为改编参考」"
                 "的补全；S2 只记「高度中央集权的非哈布斯堡王朝」，未给王朝名。",
    },
]

PLACES = [
    {"id": "P_ZARAGOZA", "type": "王国都城（推定）", "zh": "萨拉戈萨", "real": "Zaragoza",
     "de": "Saragossa", "en": "Zaragoza", "es": "Zaragoza",
     "note": "阿拉贡王国都城（推定）；另有埃布罗大区首府之设定",
     "country_id": "C_ARAGON", "src": ["S0"]},
]

# ============================================================
# 二、法兰克系（澄清不同时期的国名）
# ============================================================
FRANKISH_COUNTRIES = [
    {
        "id": "C_WEST_FRANKIA", "name_zh": "西法兰克王国", "name_short": "西法兰克",
        "name_de": "Westfrankenreich", "name_local": "Francia occidentalis",
        "name_en": "West Francia", "name_en_short": "West Francia",
        "polity": "加洛林系君主国",
        "polity_en": "Carolingian monarchy",
        "dynasty": "加洛林（Karolinger）", "dynasty_id": None,
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "帕里斯（推定）", "capital_id": "P_PARIS", "capital_note": None,
        "territory": "塞根河、利格河、加伦河流域及勃艮第、阿基坦",
        "territory_axis": "西欧；罗曼语政治体的第一阶段",
        "language": "罗曼语（langue d'oïl 的前身）", "language_id": None,
        "peoples": ["西法兰克人", "罗曼语居民"],
        "founded": "843（凡尔登分家后）",
        "time_span": "843 — 987（卡佩家族取代加洛林）",
        "overview": "大陆北部罗曼语政治体序列的第一阶段，也是后来「法兰西罗曼王国」的前身。"
                    "本世界线中，这一支罗曼语政治体最终在 1270 年卡佩绝嗣后终结，"
                    "其语言与宫廷文化则转移到不列颠（见「罗曼正统错位」）。",
        "key_traits": ["罗曼语政治体的第一阶段", "langue d'oïl 的政治母体",
                       "其文化后被不列颠承接"],
        "religions_detail": "天主教",
        "allies": [], "enemies": [], "wars": [], "treaties": [], "policies": [],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S3"],
        "notes": "本轮新增（分期拆分）。S0/S3 只记「大陆北部的罗曼语政治民族不存在」"
                 "与「1270 年之前是罗曼语政治体」，未给出具体国名；此处按用户裁定补出。",
    },
    {
        "id": "C_FRANKISH_ROMANCE", "name_zh": "法兰西罗曼王国", "name_short": "法兰西罗曼",
        "name_de": "Romanisch-fränkisches Königreich", "name_local": "Royaume romano-franc",
        "name_en": "Romano-Frankish Kingdom", "name_en_short": "Romano-Frankish Kingdom",
        "polity": "罗曼语君主国（卡佩王统）",
        "polity_en": "Romance-speaking monarchy of the Capetian line",
        "dynasty": "卡佩（Kapetinger）", "dynasty_id": "D_CAPET",
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "帕里斯", "capital_id": "P_PARIS", "capital_note": None,
        "territory": "法兰西岛、香槟、勃艮第、诺曼底、阿基坦、朗格多克北部",
        "territory_axis": "西欧；罗曼语政治体；1270 年终结",
        "language": "langue d'oïl（罗曼语）", "language_id": None,
        "peoples": ["罗曼语居民"],
        "founded": "987（卡佩家族即位）",
        "time_span": "987 — 1270（卡佩直系绝嗣）",
        "overview": "**大陆北部的罗曼语政治体**，本世界线中十字军东征的发动者，"
                    "也是「法兰西」这一政治名称的最后载体。1270 年前后卡佩直系绝嗣后，"
                    "它被哈布斯堡的法兰克所取代——此后大陆北部说日耳曼语，"
                    "而它的语言与宫廷文化转入不列颠。",
        "key_traits": ["十字军东征的发动者", "罗曼语政治体的最后阶段",
                       "1270 年卡佩绝嗣后终结", "其文化转入不列颠"],
        "religions_detail": "天主教；教廷与王权的紧密同盟",
        "allies": ["C_PAPAL"], "enemies": ["C_CORDOBA", "C_AYYUBID", "C_FATIMID", "C_SYRIA"],
        "wars": ["W_CRUSADES", "W_RECONQUISTA"], "treaties": [],
        "policies": ["十字军东征", "王权扩张"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S1", "S3"],
        "notes": "本轮新增（用户裁定）。**凡提到 1270 年以前大陆北部的十字军东征、"
                 "罗曼语宫廷文化、「法兰西」这一政治体时，一律应称「法兰西罗曼王国」，"
                 "不得称「法兰克」**——法兰克是 1272 年鲁道夫入主之后的日耳曼政治体。",
    },
    {
        "id": "C_FRANKEN_REPUBLIC", "name_zh": "法兰克共和国", "name_short": "法兰克共和国",
        "name_de": "Fränkische Republik", "name_local": "République franque",
        "name_en": "Frankish Republic", "name_en_short": "Frankish Republic",
        "polity": "共和政体（不完善；哈布斯堡贵族仍渗透政府与军队）",
        "polity_en": "Imperfect republic; Habsburg nobility still permeated state and army",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "帕里斯", "capital_id": "P_PARIS", "capital_note": None,
        "territory": "原法兰克王领（法兰西岛、香槟、勃艮第、洛林、弗兰登等），不含南部奥克省",
        "territory_axis": "西欧；1918 年后由君主国转为共和国",
        "language": "法兰克语（Fränkisch）", "language_id": "L_FRANKISH",
        "peoples": ["法兰克人"],
        "founded": "1918（一战战败、哈布斯堡失去统治地位）",
        "time_span": "1918 — 1945（二战中哈布斯堡复辟）",
        "overview": "一战战败后，哈布斯堡失去对法兰克的实际统治，法兰克由君主国立宪政体转为共和国。"
                    "但这一共和国是**不完善的**：哈布斯堡贵族仍然渗透政府与军队。"
                    "1945 年二战中哈布斯堡复辟，此共和国时期结束。",
        "key_traits": ["不完善的共和国", "哈布斯堡贵族仍渗透政府与军队",
                       "1945 年被复辟取代"],
        "religions_detail": "天主教",
        "allies": ["C_DEUTSCHLAND"], "enemies": ["C_IBERIA", "C_UK", "C_ROS_UHLUS", "C_USA"],
        "wars": ["W_WW2"], "treaties": [],
        "policies": ["共和化但不彻底", "贵族网络延续"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S1", "S2"],
        "notes": "本轮新增（用户裁定）。**凡提及 1918—1945 年的法兰克，应称「法兰克共和国」，"
                 "不得称「法兰克王国」或「法兰克立宪君主国」**——后者指 1945 年复辟后的政体。",
    },
    {
        "id": "C_GERMAN_REPUBLIC", "name_zh": "德意志共和国（1918—1945）",
        "name_short": "德意志共和国",
        "name_de": "Deutsche Republik", "name_local": "Deutsche Republik",
        "name_en": "German Republic", "name_en_short": "German Republic",
        "polity": "共和政体；1930 年代重建为统一联邦制民主共和国",
        "polity_en": "Republic founded 1918; rebuilt as a federal democratic republic",
        "dynasty": None, "dynasty_id": None,
        "religion": "新教（阿尔卑斯福音派为主流）", "religion_id": "R_ALPEN",
        "capital": "维也纳", "capital_id": "P_VIENNA", "capital_note": None,
        "territory": "波西米亚、摩拉维亚、奥地利、施蒂利亚、卡林西亚、蒂罗尔、低地全境、北意大利及部分波兰地区（一战后被迫释放波兰地区）",
        "territory_axis": "中欧；1918 年由帝国转为共和国",
        "language": "共同体德语", "language_id": "L_STANDARD",
        "peoples": ["德意志人", "波西米亚人", "低地人", "北意大利人", "克罗地亚-斯洛文尼亚人"],
        "founded": "1918（德意志帝国瓦解，普热米斯尔王朝结束）",
        "time_span": "1918 — 1945（二战中取消不平等条约、收复波兰，其后重建联邦政体）",
        "overview": "一战战败后普热米斯尔王朝结束，德意志由帝国转为共和政体。"
                    "它在两次大战之间**保住了学院、工厂、乐团与咖啡馆**，"
                    "却没有保住国家的能力——直到二战中取消不平等条约、收复波兰，"
                    "并最终重建为统一联邦制民主共和国。",
        "key_traits": ["普热米斯尔王朝结束后的共和政体", "一战后的领土与军事限制",
                       "1930 年代重建为联邦制民主共和国"],
        "religions_detail": "四大新教派别并存",
        "allies": ["C_FRANKEN_REPUBLIC"], "enemies": ["C_IBERIA", "C_UK", "C_ROS_UHLUS", "C_USA"],
        "wars": ["W_WW2"], "treaties": [],
        "policies": ["取消战后不平等条约", "收复波兰地区", "联邦化重建"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S1", "S2"],
        "notes": "本轮新增（用户裁定）。**1918—1945 年的德意志应称「德意志共和国」**，"
                 "1945 年后为「德意志联邦共和国」；1871—1918 年为「德意志帝国」。"
                 "S0 另记 1918 年成立「维也纳德意志共和国」，本条目为该政体的通称。",
    },
]

# ============================================================
# 三、分期继承关系
# ============================================================
RELATIONS = [
    # ---- 伊比利亚系 ----
    {"id": "REL501", "domain": "国家关系网", "kind": "SPLIT_FROM",
     "from": "C_SPAIN_ARAGON", "from_type": "COUNTRY", "to": "C_SPAIN", "to_type": "COUNTRY",
     "label": "西班牙-阿拉贡及奥克王国由西班牙王国与阿拉贡王国合并而成（含奥克王国）",
     "time": "15世纪末 — 16世纪初", "status": "已确定", "src": ["S0", "S2"]},
    {"id": "REL502", "domain": "国家关系网", "kind": "SPLIT_FROM",
     "from": "C_SPAIN_ARAGON", "from_type": "COUNTRY", "to": "C_ARAGON", "to_type": "COUNTRY",
     "label": "阿拉贡王国是西班牙-阿拉贡及奥克王国的两个构成主体之一",
     "time": "15世纪末 — 16世纪初", "status": "已确定", "src": ["S0", "S2"]},
    {"id": "REL503", "domain": "国家关系网", "kind": "ALLY_OF",
     "from": "C_SPAIN", "from_type": "COUNTRY", "to": "C_ARAGON", "to_type": "COUNTRY",
     "label": "卡斯蒂利亚方向与阿拉贡方向通过王朝联姻合为一体，共同推进伊比利亚统一",
     "time": "15世纪", "status": "已确定", "src": ["S2"]},
    {"id": "REL504", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_SPAIN_ARAGON", "from_type": "COUNTRY", "to": "C_IBERIAN_KINGDOM",
     "to_type": "COUNTRY",
     "label": "西班牙-阿拉贡及奥克王国完成伊比利亚各基督教王国的统一，建立伊比利亚王国",
     "time": "16世纪", "status": "已确定", "src": ["S0", "S2"]},
    {"id": "REL505", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIAN_KINGDOM", "from_type": "COUNTRY", "to": "C_IBERIA_1REP",
     "to_type": "COUNTRY", "label": "1789 年伊比利亚-奥克大革命推翻伊比利亚王国，建立第一共和国",
     "time": "1789", "status": "已确定", "src": ["S0", "S1"]},
    {"id": "REL506", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIA_1REP", "from_type": "COUNTRY", "to": "C_IBERIA_1EMP",
     "to_type": "COUNTRY", "label": "第一共和国转为伊比利亚第一帝国",
     "time": "约1804", "status": "已确定", "src": ["S0"]},
    {"id": "REL507", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIA_1EMP", "from_type": "COUNTRY", "to": "C_IBERIA_2REP",
     "to_type": "COUNTRY", "label": "第一帝国被反伊比利亚同盟击败；1815 年后重建为第二共和国",
     "time": "1815", "status": "已确定", "src": ["S0", "S1"]},
    {"id": "REL508", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIA_2EMP_UNION", "from_type": "COUNTRY", "to": "C_IBERIA_3REP_FULL",
     "to_type": "COUNTRY",
     "label": "第二共和国后转入第二帝国，继而第三、第四、第五共和国反复更替",
     "status": "已确定", "src": ["S0"]},
    {"id": "REL509", "domain": "国家关系网", "kind": "DYNASTY_RULES",
     "from": "D_TRASTAMARA", "from_type": "DYNASTY", "to": "C_SPAIN", "to_type": "COUNTRY",
     "label": "特拉斯塔马拉系为卡斯蒂利亚—莱昂方向的王统", "status": "已确定", "src": ["S2"]},
    {"id": "REL510", "domain": "国家关系网", "kind": "DYNASTY_RULES",
     "from": "D_TRASTAMARA", "from_type": "DYNASTY", "to": "C_ARAGON", "to_type": "COUNTRY",
     "label": "特拉斯塔马拉系另一支为阿拉贡方向的王统", "status": "已确定", "src": ["S2"]},
    {"id": "REL511", "domain": "国家关系网", "kind": "SPLIT_FROM",
     "from": "D_IBERIA_DYNASTY", "from_type": "DYNASTY", "to": "D_TRASTAMARA",
     "to_type": "DYNASTY", "label": "伊比利亚王朝由西班牙与阿拉贡两支王统合并而成",
     "status": "已确定", "src": ["S2"]},
    {"id": "REL512", "domain": "国家关系网", "kind": "BORDER_TENSION",
     "from": "C_ARAGON", "from_type": "COUNTRY", "to": "C_OCCITAN_KINGDOM", "to_type": "COUNTRY",
     "label": "阿拉贡的地中海与南法扩张，是奥克语地区最终卷入伊比利亚轨道的关键",
     "status": "已确定", "src": ["S0", "S2"]},
    {"id": "REL513", "domain": "国家关系网", "kind": "TERRITORY_TRANSFER",
     "from": "C_OCCITAN_KINGDOM", "from_type": "COUNTRY", "to": "C_SPAIN_ARAGON",
     "to_type": "COUNTRY", "label": "奥克王国并入西班牙-阿拉贡及奥克王国",
     "time": "16世纪初", "status": "已确定", "src": ["S2"]},

    # ---- 法兰克 / 德意志分期 ----
    {"id": "REL520", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_WEST_FRANKIA", "from_type": "COUNTRY", "to": "C_FRANKISH_ROMANCE",
     "to_type": "COUNTRY", "label": "加洛林西法兰克王国由卡佩家族接续，成为法兰西罗曼王国",
     "time": "987", "status": "已确定", "src": ["S0", "S3"]},
    {"id": "REL521", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_FRANKISH_ROMANCE", "from_type": "COUNTRY", "to": "C_FRANKEN",
     "to_type": "COUNTRY",
     "label": "1270 年卡佩直系绝嗣；1272 年哈布斯堡的鲁道夫入主，罗曼语政治体被日耳曼的法兰克取代",
     "time": "1270 / 1272", "status": "已确定", "src": ["S0", "S1"]},
    {"id": "REL522", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_FRANKEN", "from_type": "COUNTRY", "to": "C_FRANKEN_REPUBLIC",
     "to_type": "COUNTRY",
     "label": "一战战败后哈布斯堡失去统治地位，法兰克立宪君主国转为法兰克共和国",
     "time": "1918", "status": "已确定", "src": ["S0", "S1"]},
    {"id": "REL523", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_FRANKEN_REPUBLIC", "from_type": "COUNTRY", "to": "C_FRANKEN",
     "to_type": "COUNTRY",
     "label": "二战中哈布斯堡复辟，法兰克共和国回到君主立宪政体（国王彻底礼仪化）",
     "time": "1945", "status": "已确定", "src": ["S0", "S1", "S2"]},
    {"id": "REL524", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_DEUTSCHLAND", "from_type": "COUNTRY", "to": "C_GERMAN_REPUBLIC",
     "to_type": "COUNTRY",
     "label": "一战战败后德意志帝国瓦解、普热米斯尔王朝结束，转为德意志共和国",
     "time": "1918", "status": "已确定", "src": ["S0", "S1"]},
    {"id": "REL525", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_GERMAN_REPUBLIC", "from_type": "COUNTRY", "to": "C_DEUTSCHLAND",
     "to_type": "COUNTRY",
     "label": "二战后重建为统一联邦制民主共和国（德意志联邦共和国）",
     "time": "1945", "status": "已确定", "src": ["S0", "S1", "S2"]},
    {"id": "REL526", "domain": "国家关系网", "kind": "CULTURAL_HEGEMONY",
     "from": "C_FRANKISH_ROMANCE", "from_type": "COUNTRY", "to": "C_UK", "to_type": "COUNTRY",
     "label": "1270 年后法兰西罗曼王国的宫廷、文书与语言文化转入不列颠；"
              "此即「正统错位」的历史来源",
     "time": "1272 后", "status": "已确定", "src": ["S3"]},
    {"id": "REL527", "domain": "国家关系网", "kind": "ENEMY_OF",
     "from": "C_FRANKISH_ROMANCE", "from_type": "COUNTRY", "to": "C_AYYUBID",
     "to_type": "COUNTRY", "label": "十字军东征时期，大陆北部的罗曼语政治体（法兰西罗曼王国）"
                                       "是远征的发动者",
     "time": "11—13世纪", "status": "已确定", "src": ["S1"]},
    {"id": "REL528", "domain": "国家关系网", "kind": "ALLY_OF",
     "from": "C_FRANKISH_ROMANCE", "from_type": "COUNTRY", "to": "C_PAPAL",
     "to_type": "COUNTRY", "label": "十字军东征中与教皇国同阵营（1270 年之前）",
     "time": "11—13世纪", "status": "已确定", "src": ["S1"]},
    {"id": "REL530", "domain": "国家关系网", "kind": "ALLY_OF",
     "from": "C_FRANKEN_REPUBLIC", "from_type": "COUNTRY", "to": "C_GERMAN_REPUBLIC",
     "to_type": "COUNTRY", "label": "二战中欧协定：法兰克共和国与德意志共和国同阵营",
     "time": "1939—1945", "status": "已确定", "src": ["S0"]},
]

