
# ============================================================
# 四、伊比利亚共和序列的细分（用户 2026 补充裁定）
# ============================================================
IBERIAN_REPUBLICS = [
    {
        "id": "C_IBERIA_3REP_FULL", "name_zh": "伊比利亚第三共和国（1871—1940）",
        "name_short": "伊比利亚第三共和国",
        "name_de": "Dritte Iberische Republik", "name_local": "Tercera República Ibérica",
        "name_en": "Third Iberian Republic", "name_en_short": "Third Republic",
        "polity": "共和政体；中央集权，但尚未形成后来的强总统制",
        "polity_en": "Centralised republic, not yet the later strong-presidency system",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教（压制国内新教徒）", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO",
        "capital_note": "文档未指定首都",
        "territory": "伊比利亚半岛、北非西部、奥克地区",
        "territory_axis": "西南欧 + 西地中海 + 西马格里布",
        "language": "伊比利亚-奥克语", "language_id": "L_OCCITAN",
        "peoples": ["伊比利亚人", "奥克人", "马格里布基督教化居民"],
        "founded": "1871（伊比利亚第二帝国被德意志帝国击败后成立）",
        "time_span": "1871 — 1940（被法兰克与德意志击败）",
        "overview": "伊比利亚第二帝国于 1871 年被新成立的德意志帝国击败后，伊比利亚转入第三共和国。"
                    "它是本世界线中存续最久、出场最频繁的伊比利亚政权：一战中加入协约方"
                    "（与英帝国、俄罗斯、美国同侧）对中欧作战；二战中再度站到协约国一侧，"
                    "结果于 **1940 年被法兰克与德意志击败**，第三共和国就此终结。"
                    "其在奥克地区的势力也在此期间被法兰克逐出。",
        "key_traits": ["1871 年第二帝国战败后成立", "一战、二战均属协约方",
                       "1940 年被法兰克与德意志击败", "奥克地区的伊比利亚势力在此期终结"],
        "religions_detail": "天主教；压制国内新教徒（内政天主教），外交上则可加入反哈布斯堡阵营",
        "allies": ["C_UK", "C_ROS_UHLUS", "C_USA"],
        "enemies": ["C_FRANKEN", "C_DEUTSCHLAND"],
        "wars": ["W_WW1", "W_WW2"], "treaties": [],
        "policies": ["中央集权", "对奥克的同化政策", "北非一体行政"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S1", "S2"],
        "notes": "本轮新增（用户补充裁定）。**分期提示：本词条覆盖 1871—1940；"
                 "1940 年被击败后进入被占领/过渡期（1940—1945），1945 年建立第四共和国。**",
    },
    {
        "id": "C_IBERIA_OCCUPIED", "name_zh": "伊比利亚被占领与过渡期（1940—1945）",
        "name_short": "伊比利亚过渡期",
        "name_de": "Besetztes und Übergangs-Iberien", "name_local": "Iberia ocupada",
        "name_en": "Occupied and Transitional Iberia", "name_en_short": "Occupied Iberia",
        "polity": "战败后被占领并由过渡政权管理的时期",
        "polity_en": "Defeated, occupied, administered by a transitional regime",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO", "capital_note": None,
        "territory": "伊比利亚半岛、北非西部（1945 年失去奥克地区）",
        "territory_axis": "西南欧 + 西马格里布",
        "language": "伊比利亚-奥克语", "language_id": "L_OCCITAN",
        "peoples": ["伊比利亚人", "奥克人", "马格里布基督教化居民"],
        "founded": "1940（第三共和国被法兰克与德意志击败）",
        "time_span": "1940 — 1945（战后建立第四共和国）",
        "overview": "第三共和国于 1940 年战败后，伊比利亚进入被占领与过渡管理期，"
                    "直至 1945 年二战结束。这五年是伊比利亚政治体制的断点："
                    "旧共和国的中央集权与殖民体系在此期间崩解，"
                    "为战后高度议会化的第四共和国铺路。"
                    "1945 年，胜利方（德意志等）推动伊比利亚民主化，第四共和国由此建立。",
        "key_traits": ["1940 年战败后的占领与过渡", "旧共和体制的断点",
                       "1945 年由胜利方推动民主化"],
        "religions_detail": "天主教",
        "allies": [], "enemies": ["C_FRANKEN", "C_DEUTSCHLAND"],
        "wars": ["W_WW2"], "treaties": [],
        "policies": ["被占领状态", "战后由胜利方监督民主化"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增（用户补充裁定推出的分期）。用户裁定「第三共和国延续至 1940 年被击败」"
                 "与「第四共和国自 1945 年建立」，两者之间需有 1940—1945 的被占领/过渡期；"
                 "本条目即该时期的占位条目，具体占领形式与过渡机构为推定，可调整。",
    },
    {
        "id": "C_IBERIA_4REP", "name_zh": "伊比利亚第四共和国（1945—1954）",
        "name_short": "伊比利亚第四共和国",
        "name_de": "Vierte Iberische Republik", "name_local": "Cuarta República Ibérica",
        "name_en": "Fourth Iberian Republic", "name_en_short": "Fourth Republic",
        "polity": "高度议会化的共和国；**总统权力受限**，实权在议会与内阁",
        "polity_en": "Highly parliamentary republic with a weakened presidency",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教；战后推动民主化与文化保护", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO", "capital_note": None,
        "territory": "伊比利亚半岛、北非西部（已失去奥克地区）",
        "territory_axis": "西南欧 + 西马格里布",
        "language": "伊比利亚-奥克语", "language_id": "L_OCCITAN",
        "peoples": ["伊比利亚人", "马格里布基督教化居民", "西北伊比利亚群体"],
        "founded": "1945（二战结束，由胜利方推动民主化）",
        "time_span": "1945 — 1954（因非洲殖民地危机覆灭）",
        "overview": "战后由胜利方推动建立的议会制共和国，是伊比利亚政治史上**总统权力最弱**的阶段："
                    "国家高度议会化，总统权力受限。它面临的核心难题是"
                    "**非洲殖民地危机**——北非西部在法律上属伊比利亚本土行政体系，"
                    "但战后的民族主义浪潮使这一体制难以为继。1954 年前后危机爆发，第四共和国覆灭。",
        "key_traits": ["高度议会化", "总统权力受限", "1954 年前后非洲殖民地危机",
                       "危机导致共和国覆灭"],
        "religions_detail": "天主教；战后推行民主化与文化保护（但不联邦化）",
        "allies": ["C_DEUTSCHLAND"], "enemies": [],
        "wars": [], "treaties": [],
        "policies": ["高度议会制", "少数文化保护但不联邦化",
                     "北非同化与本土一体行政"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S2"],
        "notes": "本轮新增（用户补充裁定）。**非洲殖民地危机**是本期的关键："
                 "S2 明确北非西部「与半岛同属一个国家行政体系、无特殊宪制地位」，"
                 "故该危机不是一般意义上的殖民地独立问题，而是本土行政体系内部的撕裂。",
    },
    {
        "id": "C_IBERIA_5REP", "name_zh": "伊比利亚第五共和国（1960— ）",
        "name_short": "伊比利亚第五共和国",
        "name_de": "Fünfte Iberische Republik", "name_local": "Quinta República Ibérica",
        "name_en": "Fifth Iberian Republic", "name_en_short": "Fifth Republic",
        "polity": "**总统权力重新加强**的共和国；即现行伊比利亚共和国体制",
        "polity_en": "Republic with a re-strengthened presidency; the current Iberian system",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教（长期压制国内新教徒）", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO", "capital_note": None,
        "territory": "伊比利亚半岛、北非西部（本土一体行政）",
        "territory_axis": "西南欧 + 西马格里布；文明地理上属欧洲",
        "language": "伊比利亚-奥克语", "language_id": "L_OCCITAN",
        "peoples": ["伊比利亚人", "马格里布基督教化居民"],
        "founded": "1960",
        "time_span": "1960 — 至今",
        "overview": "第四共和国因非洲殖民地危机覆灭后，伊比利亚于 1960 年重建为第五共和国。"
                    "与第四共和国相反，本期**总统权力重新加强**，中央集权传统回归，"
                    "同时保留战后确立的民主化框架——这正是 S2 所概括的"
                    "「国家可以很强，但权力必须民主化」。"
                    "本词条即现行「伊比利亚共和国」的正式分期名称。",
        "key_traits": ["总统权力重新加强", "「强国家 + 民主化」的体制",
                       "大区很大而少、省份承载传统地区", "北非为本土一部分", "六极之一"],
        "religions_detail": "天主教；压制新教徒，但推行文化保护",
        "allies": ["C_UK"], "enemies": ["C_FRANKEN"],
        "wars": [], "treaties": [],
        "policies": ["大型大区制（大区很大、数量少；以大区命名山系/水系）",
                     "北非不设特殊行政层级", "民主化 + 文化保护，但不联邦化",
                     "二战后 PNI 被拆解，PSI 成为第一大党"],
        "subdivisions": ["SB_IBERIA"], "parties": ["PT_PNI", "PT_PSI", "PT_PLI", "PT_PCI"],
        "orgs": [],
        "status": "已确定", "src": ["S0", "S1", "S2"],
        "notes": "本轮新增（用户补充裁定）。**s1 母表所记 1960 年伊比利亚为「区域强国」，"
                 "与第五共和国自 1960 年建立完全吻合**——1960 年既是伊比利亚的政体重建年，"
                 "也是多极均势格局的成局年。",
    },
]

# ---------------------------------------------------------------- 新增事件
EVENTS = [
    {
        "id": "E_1871_IBERIA_2EMP_FALL", "year": 1871, "year_text": "1871",
        "epoch": "19世纪：小德意志统一与伊比利亚转折",
        "name_zh": "伊比利亚第二帝国被德意志帝国击败，第三共和国成立",
        "name_de": "Sieg über das Zweite Iberische Kaiserreich",
        "name_en": "Defeat of the Second Iberian Empire",
        "region": "中欧、南欧、那不勒斯与罗马",
        "country_ids": ["C_IBERIA_2REP", "C_DEUTSCHLAND", "C_IBERIA_3REP_FULL"],
        "persons": [],
        "summary": "普热米斯尔攻入受伊比利亚第二帝国长臂管辖的那不勒斯与罗马，"
                   "在罗马加冕成立德意志帝国；伊比利亚第二帝国同时被击败，"
                   "自此转入第三共和国。",
        "outcome": "南意大利与罗马被从伊比利亚势力范围中夺出；伊比利亚第二帝国终结，"
                   "第三共和国成立并延续至 1940 年。",
        "causes": ["E_1866_WAR"], "effects": ["E_1871_EMPIRE", "E_WW1"],
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增（用户补充裁定）。与 1871 年罗马加冕为同一转折的两面："
                 "德意志帝国成立之日，即伊比利亚第二帝国终结之时。",
    },
    {
        "id": "E_1940_IBERIA_DEFEAT", "year": 1940, "year_text": "1940",
        "epoch": "20世纪：第二次世界大战",
        "name_zh": "伊比利亚第三共和国被法兰克与德意志击败",
        "name_de": "Niederlage der Dritten Iberischen Republik",
        "name_en": "Defeat of the Third Iberian Republic",
        "region": "伊比利亚半岛、奥克地区、西地中海",
        "country_ids": ["C_IBERIA_3REP_FULL", "C_FRANKEN", "C_DEUTSCHLAND",
                        "C_GERMAN_REPUBLIC", "C_IBERIA_OCCUPIED"],
        "persons": [],
        "summary": "二战中伊比利亚第三共和国再度站到协约国一侧；1940 年，"
                   "法兰克与德意志将其击败，第三共和国终结，伊比利亚进入被占领与过渡期。",
        "outcome": "第三共和国终结；1940—1945 为被占领与过渡期；"
                   "伊比利亚在奥克地区的势力就此终结，1945 年失去奥克地区。",
        "causes": ["E_1939_WW2"], "effects": ["E_1945_IBERIA_4REP"],
        "war_id": "W_WW2",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增（用户补充裁定）。",
    },
    {
        "id": "E_1945_IBERIA_4REP", "year": 1945, "year_text": "1945",
        "epoch": "20世纪：战后秩序",
        "name_zh": "伊比利亚第四共和国成立",
        "name_de": "Gründung der Vierten Iberischen Republik",
        "name_en": "Founding of the Fourth Iberian Republic",
        "region": "伊比利亚半岛",
        "country_ids": ["C_IBERIA_4REP", "C_IBERIA", "C_DEUTSCHLAND", "C_FRANKEN"],
        "persons": [],
        "summary": "二战结束后，由胜利方（德意志等）推动民主化，伊比利亚建立高度议会化的第四共和国，"
                   "总统权力受限，实权归于议会与内阁。",
        "outcome": "伊比利亚进入总统权力最弱的阶段；同时失去奥克地区。",
        "causes": ["E_1940_IBERIA_DEFEAT", "E_1939_WW2"],
        "effects": ["E_1954_IBERIA_COLONIAL"],
        "status": "已确定", "src": ["S2"],
        "notes": "本轮新增（用户补充裁定）。与不列颠 1945 年被监督民主化同构——"
                 "S2/S3 均记「民主化由胜利者推动」。",
    },
    {
        "id": "E_1954_IBERIA_COLONIAL", "year": 1954,
        "year_text": "1954年前后", "epoch": "20世纪：战后秩序",
        "name_zh": "非洲殖民地危机与第四共和国覆灭",
        "name_de": "Afrikanische Kolonialkrise",
        "name_en": "African colonial crisis",
        "region": "北非西部（马格里布）、伊比利亚半岛",
        "country_ids": ["C_IBERIA_4REP", "C_MAGHREB", "C_IBERIA_5REP"],
        "persons": [],
        "summary": "第四共和国高度议会化、总统权力受限，难以应对**非洲殖民地危机**。"
                   "1954 年前后危机爆发，第四共和国覆灭。",
        "outcome": "第四共和国终结；1960 年重建为总统权力加强的第五共和国。",
        "causes": ["E_1945_IBERIA_4REP", "E_MAGHREB_CHRISTIANISATION"],
        "effects": ["E_1960_IBERIA_5REP"],
        "status": "已确定", "src": ["S2"],
        "notes": "本轮新增（用户补充裁定）。因 S2 明确北非西部属伊比利亚本土行政体系，"
                 "此危机的性质更接近「本土一体化体制的撕裂」而非一般殖民地独立。",
    },
    {
        "id": "E_1960_IBERIA_5REP", "year": 1960, "year_text": "1960",
        "epoch": "20世纪后期：多极均势",
        "name_zh": "伊比利亚第五共和国建立",
        "name_de": "Gründung der Fünften Iberischen Republik",
        "name_en": "Founding of the Fifth Iberian Republic",
        "region": "伊比利亚半岛、北非西部",
        "country_ids": ["C_IBERIA_5REP", "C_IBERIA", "C_DEUTSCHLAND", "C_FRANKEN"],
        "persons": [],
        "summary": "第四共和国覆灭后，伊比利亚于 1960 年重建为第五共和国，"
                   "总统权力重新加强，形成「强国家 + 民主化」的现行体制。",
        "outcome": "现行伊比利亚共和国体制确立；同年多极均势格局成局。",
        "causes": ["E_1954_IBERIA_COLONIAL"],
        "effects": ["E_1960_MULTIPOLAR"],
        "status": "已确定", "src": ["S0", "S1", "S2"],
        "notes": "本轮新增（用户补充裁定）。S1 母表记 1960 年伊比利亚为「区域强国」，"
                 "与第五共和国建立年重合。",
    },
]

# ---------------------------------------------------------------- 新增关系
REPUBLIC_RELATIONS = [
    {"id": "REL540", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIA_2REP", "from_type": "COUNTRY", "to": "C_IBERIA_2EMP_UNION",
     "to_type": "COUNTRY", "label": "第二共和国后转入第二帝国",
     "status": "已确定", "src": ["S0"]},
    {"id": "REL541", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIA_2EMP_UNION", "from_type": "COUNTRY", "to": "C_IBERIA_3REP_FULL",
     "to_type": "COUNTRY",
     "label": "1871 年伊比利亚第二帝国被德意志帝国击败，转入第三共和国",
     "time": "1871", "status": "已确定", "src": ["S0", "S1"]},
    {"id": "REL542", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIA_3REP_FULL", "from_type": "COUNTRY", "to": "C_IBERIA_OCCUPIED",
     "to_type": "COUNTRY",
     "label": "1940 年第三共和国被法兰克与德意志击败，进入被占领与过渡期",
     "time": "1940", "status": "已确定", "src": ["S0"]},
    {"id": "REL543", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIA_OCCUPIED", "from_type": "COUNTRY", "to": "C_IBERIA_4REP",
     "to_type": "COUNTRY",
     "label": "1945 年战后由胜利方推动民主化，建立高度议会化的第四共和国",
     "time": "1945", "status": "已确定", "src": ["S2"]},
    {"id": "REL544", "domain": "国家关系网", "kind": "SUCCEEDED_BY",
     "from": "C_IBERIA_4REP", "from_type": "COUNTRY", "to": "C_IBERIA_5REP",
     "to_type": "COUNTRY",
     "label": "1954 年前后非洲殖民地危机导致第四共和国覆灭，1960 年重建为第五共和国",
     "time": "1954 / 1960", "status": "已确定", "src": ["S2"]},
    {"id": "REL545", "domain": "国家关系网", "kind": "SAME_AS",
     "from": "C_IBERIA_5REP", "from_type": "COUNTRY", "to": "C_IBERIA",
     "to_type": "COUNTRY",
     "label": "现行「伊比利亚共和国」即第五共和国体制；C_IBERIA 为其通称条目",
     "status": "已确定", "src": ["S0", "S2"]},
    {"id": "REL546", "domain": "国家关系网", "kind": "ENEMY_OF",
     "from": "C_IBERIA_3REP_FULL", "from_type": "COUNTRY", "to": "C_DEUTSCHLAND",
     "to_type": "COUNTRY",
     "label": "一战与二战均与中欧为敌；1940 年被法兰克与德意志击败",
     "time": "1914—1918 / 1939—1940", "status": "已确定", "src": ["S0"]},
    {"id": "REL547", "domain": "国家关系网", "kind": "TERRITORY_TRANSFER",
     "from": "C_IBERIA_4REP", "from_type": "COUNTRY", "to": "C_FRANKEN",
     "to_type": "COUNTRY",
     "label": "1945 年伊比利亚失去奥克地区，法兰克获取并设南部奥克省",
     "time": "1945", "status": "已确定", "src": ["S0", "S2"]},
]

# 第二帝国的占位条目（原数据只列名称，此处补齐为可拆分的一环）
IBERIAN_2EMP = [
    {
        "id": "C_IBERIA_2EMP_UNION", "name_zh": "伊比利亚第二帝国",
        "name_short": "第二帝国",
        "name_de": "Zweites Iberisches Kaiserreich",
        "name_local": "Segundo Imperio Ibérico",
        "name_en": "Second Iberian Empire", "name_en_short": "Second Empire",
        "polity": "帝制政体（第二共和国之后）",
        "polity_en": "Empire following the Second Republic",
        "dynasty": None, "dynasty_id": None,
        "religion": "天主教", "religion_id": "R_CATHOLIC",
        "capital": "托莱多（推定）", "capital_id": "P_TOLEDO", "capital_note": None,
        "territory": "伊比利亚半岛、北非西部、奥克地区；长臂管辖伸至南意大利那不勒斯与罗马",
        "territory_axis": "西南欧 + 西地中海 + 西马格里布",
        "language": "伊比利亚-奥克语", "language_id": "L_OCCITAN",
        "peoples": ["伊比利亚人", "奥克人"],
        "founded": "19世纪中叶（第二共和国转为帝制）",
        "time_span": "19世纪中叶 — 1871（被德意志帝国击败）",
        "overview": "第二共和国之后的帝制阶段。它的势力范围一度覆盖那不勒斯与罗马，"
                    "1871 年普热米斯尔攻入这两地并在罗马加冕，第二帝国同时被击败——"
                    "**德意志帝国成立之日，即伊比利亚第二帝国终结之时**。",
        "key_traits": ["长臂管辖伸至南意大利", "1871 年被德意志帝国击败",
                       "其终结与德意志帝国成立同年"],
        "religions_detail": "天主教",
        "allies": [], "enemies": ["C_DEUTSCHLAND", "C_FRANKEN"],
        "wars": ["W_1866"], "treaties": [],
        "policies": ["帝制", "对南意大利的长臂管辖"],
        "subdivisions": [], "parties": [], "orgs": [],
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增（分期拆分）。S0 记「伊比利亚第二帝国长臂管辖那不勒斯和罗马」，"
                 "原库中只有名称而未立条目，此处补齐。",
    },
]
