# -*- coding: utf-8 -*-
"""
历史物品留存 · 收藏机构补层
============================
两份内容：

1. ORGANIZATIONS —— 25 件留存物中，凡「repository」指向尚无独立词条的收藏机构，
   此处补建词条（档案库、陈列馆、博物馆、教堂宝库），使「物品 → 收藏机构」
   在关系网中真实成立。词条依据为留存物自述的收藏关系，不新增设定。

2. REPO_MAP —— AR_* → 机构 ID 的对应表，供 build.py 生成 KEPT_AT 边。
"""

ORGANIZATIONS = [
    # ---------------- 德意志联邦 ----------------
    {
        "id": "O_REICHSARCHIV_FFM", "name_zh": "法兰克福帝国议会档案馆",
        "name_de": "Reichstagsarchiv Frankfurt", "name_en": "Imperial Diet Archive of Frankfurt",
        "type": "档案馆", "country_id": "C_DEUTSCHLAND",
        "function": "帝国议会文书、选侯议定书、宪章正本与玺印的法定保存机关",
        "overview": "《法兰克福宪章》正本、七选侯之印与帝国议会历届议定书的保存地。"
                    "因 1356 年宪章确立「双重王冠不可分割」，此馆同时保管波西米亚—奥地利"
                    "与法兰克两条王统的法律文书，是双王冠制度在纸面上的共同记忆。"
                    "1871 年罗马加冕后，帝国议会的礼仪性展示在开会期间于此举行。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。S0 述 1356 年《法兰克福宪章》与帝国议会制度，"
                 "此处按文书保存的必然归属补建机构词条。",
    },
    {
        "id": "O_WIEN_STAATSARCHIV", "name_zh": "维也纳国家档案馆",
        "name_de": "Österreichisches Staatsarchiv", "name_en": "Vienna State Archive",
        "type": "档案馆", "country_id": "C_DEUTSCHLAND",
        "function": "哈布斯堡—普热米斯尔王室文书、条约正本、行政档案",
        "overview": "德意志联邦的中央文书保存机关，藏有 1871 年《维也纳条约》正本"
                    "与历代双重君主国的行政档案。它的藏品结构本身就是联邦制的写照："
                    "维也纳的行政传统与布拉格的波西米亚传统在同一库房内分卷保存，"
                    "政治上合为一部，档案上各成系统。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。S0 提及 1871 年维也纳条约与双重君主国行政体系，"
                 "此处按文书归属补建。",
    },
    {
        "id": "O_WITTENBERG_SCHLOSSKIRCHE", "name_zh": "维滕堡城堡教堂",
        "name_de": "Schlosskirche Wittenberg", "name_en": "Wittenberg Castle Church",
        "type": "教堂", "country_id": "C_DEUTSCHLAND",
        "function": "新教改革的发端地；《九十五条论纲》张贴处；福音派朝圣与纪念中心",
        "overview": "宗教改革的起点建筑。1517 年《九十五条论纲》张贴于其大门，"
                    "此后该门成为新教世界最重要的纪念物；门上原件早已不存，"
                    "现存者为后世所立的铜门与贴附的论纲拓本。教堂同时是"
                    "《十二条款》等改革文献的展示地，与德意志联邦的新教国家"
                    "身份直接绑定，1871 年后列为国家圣地。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。S0/S1 述宗教改革与新教大德意志，此处按改革纪念地补建。",
    },
    {
        "id": "O_BETHLEHEM_CHAPEL", "name_zh": "布拉格伯利恒礼拜堂",
        "name_de": "Bethlehemskapelle Prag", "name_en": "Bethlehem Chapel, Prague",
        "type": "教堂", "country_id": "C_DEUTSCHLAND",
        "function": "胡斯派布道中心；胡斯派传统陈列与波西米亚宗教记忆场所",
        "overview": "胡斯在布拉格布道的礼拜堂，波西米亚宗教改革的原生场所。"
                    "1415 年胡斯被处死后，此处成为波西米亚民族与宗教记忆的聚合点；"
                    "胡斯派圣餐杯等物自此保存在此。在德意志联邦的宗教叙事中，"
                    "它与维滕堡构成前后相继的两站：波西米亚先行，德意志继之。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。S0/S1 述胡斯派与波西米亚宗教线，此处按场所归属补建。",
    },
    {
        "id": "O_NAT_MUSEUM_SOZIALGESCH", "name_zh": "德意志联邦国家博物馆（社会史部）",
        "name_de": "Nationalmuseum für Sozialgeschichte", "name_en": "National Museum of Social History",
        "type": "博物馆", "country_id": "C_DEUTSCHLAND",
        "function": "1848 年革命、工人运动、社会保险与联邦社会立法的档案与实物陈列",
        "overview": "德意志联邦的国家博物馆社会史部，专收 1848 年革命以来的"
                    "请愿书、工会章程、社会保险立法原件与工人生活实物。"
                    "它的存在本身对应德意志道路的特点：社会问题通过立法与"
                    "行政解决，而非通过革命，因此革命文物在这里是「被吸收的过去」，"
                    "而非胜利者的战利品。",
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增。S0/S2 述 1848 年革命与德意志社会立法，此处按陈列归属补建。",
    },
    # ---------------- 法兰克 ----------------
    {
        "id": "O_TOLEDO_ARMORY", "name_zh": "托莱多王家军械库",
        "name_de": "Königliches Zeughaus Toledo", "name_en": "Royal Armoury of Toledo",
        "type": "博物馆", "country_id": "C_IBERIA",
        "function": "伊比利亚王国军械、征服战争缴获物与王室武备的保存机关",
        "overview": "伊比利亚王室的军械库，收存收复失地运动与北非战事的"
                    "甲胄、旗帜与缴获物。1918 年后改称伊比利亚国家历史博物馆，"
                    "成为共和国叙事中「伊比利亚统一」的陈列现场——"
                    "托莱多的军械库与马德里的王家美术馆，构成武力与文明的"
                    "两半国家记忆。",
        "status": "已确定", "src": ["S2"],
        "notes": "本轮新增。S2 述伊比利亚王国军械与统一叙事，此处按留存物自述的收藏地补建。",
    },
    {
        "id": "O_OCCITAN_MUSEUM", "name_zh": "托洛森奥克文化博物馆",
        "name_de": "Okkzitanisches Kulturmuseum Toulouse", "name_en": "Occitan Cultural Museum, Toulouse",
        "type": "博物馆", "country_id": "C_FRANKEN",
        "function": "奥克语文献、十字军东征时期文物与奥克身份陈列",
        "overview": "设于托洛森的奥克文化博物馆。它保存奥克语诗歌、市政文书"
                    "与 13 世纪阿尔比十字军时期的遗物，是法兰克王国内部"
                    "「奥克问题」的官方陈列场所：国家以此承认奥克文化的独特性，"
                    "同时把它的政治诉求固定在展柜里。1945 年南部奥克省建制化后，"
                    "此处成为省文化自治的象征机构。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。S0/S1 述奥克地区与阿尔比十字军，此处按留存物自述的收藏地补建。",
    },
    {
        "id": "O_PRAG_NAT_TECH", "name_zh": "布拉格国家技术博物馆",
        "name_de": "Nationales Technikmuseum Prag", "name_en": "National Technical Museum, Prague",
        "type": "博物馆", "country_id": "C_DEUTSCHLAND",
        "function": "波西米亚工业、机械制造与电气化的实物与技术档案",
        "overview": "波西米亚工业带的技术陈列机关。布拉格—比尔森—布尔诺一线的"
                    "机械、纺织与电气工业在此留下实物序列，"
                    "它记录的正是德意志联邦工业实力的东部底座："
                    "维也纳提供制度与学术，布拉格提供车间与机器。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。S0/S1 述波西米亚工业，此处按留存物自述的收藏地补建。",
    },
    {
        "id": "O_GENF_STPETERS", "name_zh": "日内瓦圣彼得大教堂",
        "name_de": "Kathedrale St. Peter Genf", "name_en": "St. Peter's Cathedral, Geneva",
        "type": "教堂", "country_id": "C_SWITZERLAND",
        "function": "加尔文派布道与神权政体实验的原始场所",
        "overview": "加尔文在日内瓦布道与授课的教堂，改革宗神权政体实验的原点。"
                    "它同时是瑞士永久中立与联邦制的一个源头："
                    "一个以信仰纪律组织起来的城市，最终成为"
                    "「不参与大国战争」这一国家原则的最早实践者。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。S0/S1 述加尔文派与瑞士中立，此处按场所归属补建。",
    },
    {
        "id": "O_PRAG_NAT_GALLERY", "name_zh": "布拉格国家美术馆",
        "name_de": "Nationalgalerie Prag", "name_en": "National Gallery in Prague",
        "type": "艺术馆", "country_id": "C_DEUTSCHLAND",
        "function": "波西米亚哥特与巴洛克绘画、胡斯派艺术、现代绘画收藏",
        "overview": "波西米亚绘画的国家收藏机关。藏品从 14 世纪波西米亚宫廷的"
                    "哥特祭坛画起，经胡斯派的图像争论与巴洛克的宗教图像，"
                    "到 19 世纪的民族复兴绘画。它呈现的是德意志联邦内部"
                    "一条与维也纳不同的艺术线路：维也纳偏帝国与宫廷，"
                    "布拉格偏宗教与民族。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。S0/S1 述布拉格为学术与艺术圣地，此处按该国收藏规模合理补充。",
    },
    {
        "id": "O_HAMBURG_KUNSTHALLE", "name_zh": "汉堡艺术馆",
        "name_de": "Hamburger Kunsthalle", "name_en": "Hamburg Kunsthalle",
        "type": "艺术馆", "country_id": "C_DEUTSCHLAND",
        "function": "汉萨城市市民艺术收藏；北德绘画、港口与海洋图像、商人家族委托作品",
        "overview": "自由汉萨市汉堡的市民艺术馆。与维也纳的帝国收藏不同，"
                    "它的藏品来自汉萨商人家族的捐赠：北德祭坛画、"
                    "港口全景、远洋贸易的图像记录与市民肖像。"
                    "此馆是「汉萨城市的钱如何变成文化」这一问题的直接答案——"
                    "德意志联邦的海外贸易财富，在汉堡沉淀为图像。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。S0 述自由汉萨市汉堡与汉萨城市体系，"
                 "此处按汉萨文化留存地合理补充。",
    },
    {
        "id": "O_MILAN_GALLERY", "name_zh": "米兰布雷拉美术馆",
        "name_de": "Pinakothek Brera Mailand", "name_en": "Brera Art Gallery, Milan",
        "type": "艺术馆", "country_id": "C_DEUTSCHLAND",
        "function": "伦巴底与北意大利文艺复兴、歌剧舞台美术与工业设计收藏",
        "overview": "米兰的绘画与设计收藏机关，兼收文艺复兴绘画、"
                    "斯卡拉歌剧院的舞台美术图稿与伦巴底工业设计作品。"
                    "它对应德意志联邦北意大利的特殊地位："
                    "这一地区既是歌剧与艺术的产地，也是联邦的工业带，"
                    "艺术与机器在同一座城市里互为表里。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。S0/S1 述米兰为学术圣地与北意大利工业区，"
                 "此处按该国收藏规模合理补充。",
    },
    {
        "id": "O_MADRID_ARCHAEOLOGICAL", "name_zh": "马德里国家考古博物馆",
        "name_de": "Nationales Archäologisches Museum Madrid",
        "name_en": "National Archaeological Museum, Madrid",
        "type": "博物馆", "country_id": "C_IBERIA",
        "function": "伊比利亚半岛考古、安达卢斯时期文物与北非殖民地民族志收藏",
        "overview": "伊比利亚的国家考古与民族志收藏机关。它的展陈顺序本身就是"
                    "该国的政治叙事：先是罗马与西哥特的伊比利亚，"
                    "继而是科尔多瓦哈里发国的安达卢斯时期，"
                    "然后是收复失地运动与半岛统一，最后是北非与"
                    "大西洋岛屿的民族志厅——而最后一厅的说明牌，"
                    "正是第四共和国殖民危机中被反复质询的部分。",
        "status": "已确定", "src": ["S2"],
        "notes": "本轮新增。S2 述伊比利亚行政与统一叙事，此处按该国收藏规模合理补充。",
    },
    {
        "id": "O_VENICE_ACCADEMIA", "name_zh": "威尼斯美术学院陈列馆",
        "name_de": "Akademie der Schönen Künste Venedig",
        "name_en": "Gallerie dell'Accademia, Venice",
        "type": "艺术馆", "country_id": "C_DEUTSCHLAND",
        "function": "威尼斯画派收藏；亚得里亚海贸易与共和国记忆的图像档案",
        "overview": "威尼斯的绘画收藏机关，以威尼斯画派与亚得里亚海贸易图像为主。"
                    "威尼斯在 1797 年后失去独立共和国地位而并入哈布斯堡—德意志体系，"
                    "因此此馆的藏品结构带有一种张力："
                    "它保存的是一个已消失的共和国最辉煌的图像，"
                    "而展厅的行政归属是德意志联邦威尼托州。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。S0 述威尼托与北意大利归入德意志体系，"
                 "此处按该地艺术传统合理补充。",
    },
    # ---------------- 英国 ----------------
    {
        "id": "O_UK_NAT_ARCHIVE", "name_zh": "伦敦国家档案馆",
        "name_de": "Britisches Nationalarchiv", "name_en": "The National Archives, London",
        "type": "档案馆", "country_id": "C_UK",
        "function": "议会法案、王室文书、殖民地与自治领档案的法定保存机关",
        "overview": "英国宪政文献的中央保存地。1215 年《大宪章》正本与历代"
                    "权利法案、议会卷档同藏于此。1848 年大陆革命期间，"
                    "英国以「宪政连续性」自我定位，此馆的展陈即被重新编排为"
                    "一条不间断的法治谱系；1945 年后《大宪章》重新展出，"
                    "成为英国与法兰克争夺「宪政母国」叙述的核心展品。",
        "status": "已确定", "src": ["S3"],
        "notes": "本轮新增。S3 述英国宪政线与《大宪章》，此处按留存物自述的收藏地补建。",
    },
    # ---------------- 罗斯兀鲁思 ----------------
    {
        "id": "O_ROS_NAT_ARCHIVE", "name_zh": "莫斯科罗斯兀鲁思国家档案馆",
        "name_de": "Staatsarchiv der Rus Uhlus Moskau", "name_en": "State Archive of the Rus Uhlus, Moscow",
        "type": "档案馆", "country_id": "C_ROS_UHLUS",
        "function": "金帐汗国封诰、莫斯科大公国文书与后基辅罗斯行政档案",
        "overview": "罗斯兀鲁思的中央文书保存机关。金帐汗国的封诰原本、"
                    "莫斯科大公的册封文书与后基辅时代的行政卷宗在此同库保存。"
                    "这一组合本身说明该国的双重出身："
                    "草原帝国的授权与东正教王公的行政，共同构成它的合法性来源。",
        "status": "已确定", "src": ["S4"],
        "notes": "本轮新增。S4 述金帐汗国继承线与莫斯科国，此处按留存物自述的收藏地补建。",
    },
    # ---------------- 马格里布 ----------------
    {
        "id": "O_MARRAKECH_SHRINE", "name_zh": "马拉喀什圣堂",
        "name_de": "Heiligtum von Marrakesch", "name_en": "Shrine of Marrakesh",
        "type": "教堂", "country_id": "C_MAGHREB",
        "function": "原穆瓦希德王朝都城；伊比利亚统治时期的宗教与行政中心",
        "overview": "原穆瓦希德王朝的都城核心建筑，伊比利亚南下后改建为"
                    "基督教圣堂与总督驻地。它的建筑层理记录了马格里布的三重历史："
                    "本地柏柏尔传统、穆瓦希德王朝的安达卢斯风格，"
                    "以及伊比利亚长期统治留下的欧洲化外观。",
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增。S0/S2 述伊比利亚南下北非与马格里布欧洲化，"
                 "此处按留存物自述的存放地补建。",
    },
    {
        "id": "O_TRIEST_MEMORIAL", "name_zh": "的里雅斯特共管纪念广场",
        "name_de": "Gedenkplatz der Freien Stadt Triest", "name_en": "Memorial Square of the Free City of Trieste",
        "type": "博物馆", "country_id": "C_DEUTSCHLAND",
        "function": "威尼托州首府的公共纪念空间；共管时期制度文献与港口行会档案陈列",
        "overview": "威尼托州首府的的里雅斯特纪念广场。此地在一战后曾被设为国际共管，"
                    "1920 年代随威尼托并入德意志联邦，成为联邦的亚得里亚出海口。"
                    "广场陈列的是共管时期的章程、通航协定与港口行会档案——"
                    "一座曾不属于任何单一国家的城市，把「共管」这段经历"
                    "保留为自身的地方记忆，同时以威尼托州首府的身份"
                    "重新接入德意志联邦的行政体系。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。S0 述一战后「的里雅斯特国际共管」与威尼托州以的里雅斯特为首府，"
                 "此处按留存物自述的存放地补建。",
    },
]

# AR_* → 收藏机构 ID
REPO_MAP = {
    "AR_STEPHAN_CROWN": "O_HOFBURG",
    "AR_REIMS_AMPULLA": "O_REIMS_CATHEDRAL",
    "AR_IMPERIAL_SEAL_1356": "O_REICHSARCHIV_FFM",
    "AR_SEVEN_ELECTORS_STAFF": "O_REICHSARCHIV_FFM",
    "AR_HUSSITE_CHALICE": "O_BETHLEHEM_CHAPEL",
    "AR_WITTENBERG_DOOR": "O_WITTENBERG_SCHLOSSKIRCHE",
    "AR_ALPINE_ALTAR": "O_STEPHANSDOM",
    "AR_CALVIN_PULPIT": "O_GENF_STPETERS",
    "AR_VIENNA_TREATY_ORIGINAL": "O_WIEN_STAATSARCHIV",
    "AR_TWELVE_ARTICLES": "O_NAT_MUSEUM_SOZIALGESCH",
    "AR_RIGHTS_CHARTER": "O_STARCHAMBER",
    "AR_GOLDEN_HORDE_YARLIK": "O_ROS_NAT_ARCHIVE",
    "AR_MAGNA_CARTA_MORTUA_DOC": "O_UK_NAT_ARCHIVE",
    "AR_DOUBLE_CROWN_BANNER": "O_REICHSARCHIV_FFM",
    "AR_ALPINE_EAGLE_STANDARD": "O_BAYERN_NAT_MUSEUM",
    "AR_OCCITAN_CROSS": "O_OCCITAN_MUSEUM",
    "AR_BOHEMIA_DYNAMO": "O_PRAG_NAT_TECH",
    "AR_MILAN_LOOM": "O_MILAN_GALLERY",
    "AR_GOTTINGEN_SEXTANT": "O_GOTTINGEN_UNI",
    "AR_HANSA_GUILDER": "O_HAMBURG_KUNSTHALLE",
    "AR_STANDARD_GERMAN_SAMPLE": "O_SPRACHKONFERENZ",
    "AR_TRIEST_ANCHOR": "O_TRIEST_MEMORIAL",
    "AR_NORMANDY_SHIELD": "O_LOUVRE",
    "AR_RECONQUISTA_KEY": "O_TOLEDO_ARMORY",
    "AR_MAGHREB_BELL": "O_MARRAKECH_SHRINE",
}
