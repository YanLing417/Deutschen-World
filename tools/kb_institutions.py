# -*- coding: utf-8 -*-
"""
全球机构与建筑群层
====================
补充世界各国的大学、博物馆、艺术馆、宫殿与教堂，加入 ORGANIZATION / PLACE 词条。

原则：
  · 优先补 S0–S4 已提及但未单列的地点（如沙特尔、圣迪奥尼修斯、维滕堡、马格德堡、阿维尼翁）。
  · 其余机构按该国的文明定位合理推设，并在 notes 中注明「本轮新增」，不冒称文档原文。
  · 类型字段 type 用中文，区分：大学 / 博物馆 / 艺术馆 / 宫殿 / 教堂 / 图书馆 / 学会。
"""

ORGANIZATIONS = [
    # ================= 德意志联邦 =================
    {
        "id": "O_TUEBINGEN_UNI", "name_zh": "蒂宾根大学", "name_de": "Universität Tübingen",
        "name_en": "University of Tübingen", "type": "大学",
        "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "新教神学、古文字学、考古学、法学；阿尔卑斯福音派神学教育中心之一",
        "overview": "德意志联邦南部的老牌大学，以新教神学与古文字学著称。"
                    "它对碑铭与纸草文献的整理，是泛德意志东方学传统的重要一支："
                    "法兰克有帕里斯的东方学，德意志则有靠文献学支撑的古代研究。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。S0 只列维也纳、布拉格、莱比锡、哥廷根、阿姆斯特丹、米兰六处为学术圣地，"
                 "此处按德意志联邦的教育规模合理补充。",
    },
    {
        "id": "O_BERLIN_UNI", "name_zh": "柏林大学", "name_de": "Universität Berlin",
        "name_en": "University of Berlin", "type": "大学",
        "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "哲学、历史学、国家学、自然科学；北德意志路德宗学术中心",
        "overview": "勃兰登堡州首府的大学，北德意志路德宗世界的学术中心。"
                    "与南德意志的维也纳、布拉格不同，此处学风素朴严肃——"
                    "与北德路德宗「反对宗教艺术和华丽礼仪」的文化立场一致。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_KUNSTHIST_MUSEUM", "name_zh": "维也纳艺术史博物馆",
        "name_de": "Kunsthistorisches Museum Wien", "name_en": "Vienna Art History Museum",
        "type": "博物馆", "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "哈布斯堡—普热米斯尔宫廷收藏、巴洛克绘画、德意志与意大利文艺复兴、"
                    "教堂艺术与管风琴藏品",
        "overview": "德意志联邦最重要的艺术收藏机构，藏有普热米斯尔家族数世纪的宫廷收藏。"
                    "它与圣斯特凡大教堂的巴洛克祭坛构成一组对照："
                    "一个说明「南德新教不弃教堂艺术」，一个展示这些艺术的历史纵深。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_BAYERN_NAT_MUSEUM", "name_zh": "巴伐利亚国家博物馆",
        "name_de": "Bayerisches Nationalmuseum", "name_en": "Bavarian National Museum",
        "type": "博物馆", "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "巴伐利亚乡村新教教堂艺术（木雕、壁画、彩绘长椅）、"
                    "啤酒节民俗、阿尔卑斯福音派军旗",
        "overview": "慕尼黑的民俗与艺术博物馆，收藏巴伐利亚乡村新教教堂的木雕、壁画与彩绘长椅。"
                    "这些藏品是南德新教文化最直观的证据：乡村教堂未被清空，"
                    "反而成为地方教会美学自由的展示场。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_HOFBURG", "name_zh": "维也纳霍夫堡宫", "name_de": "Hofburg zu Wien",
        "name_en": "Hofburg Palace, Vienna", "type": "宫殿",
        "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "普热米斯尔王朝冬宫；1871—1918 年为德意志帝国皇宫；"
                    "1918 年后为联邦国家礼仪场所与王室宝库",
        "overview": "维也纳的王朝宫殿，普热米斯尔家族的权力中枢。"
                    "1871 年罗马加冕后成为德意志皇帝的行政居所——"
                    "帝国的「行政在维也纳、圣事在罗马」这一双重结构，"
                    "在建筑上就体现为霍夫堡与罗马加冕圣城的分离。"
                    "1918 年王朝结束后移交共和国，现为国家礼仪场所，藏有圣斯特凡王冠。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_SCHOENBRUNN", "name_zh": "美泉宫", "name_de": "Schloss Schönbrunn",
        "name_en": "Schönbrunn Palace", "type": "宫殿",
        "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "普热米斯尔王朝夏宫；宫廷音乐与歌剧演出场所",
        "overview": "维也纳郊外的夏宫。其镜厅与花园剧场是德语康塔塔、清唱剧与管弦乐"
                    "宫廷演出的主要场所——南德新教「音乐属于恩典」的神学立场，"
                    "在这里获得了最宏大的空间形式。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_STEPHANSDOM", "name_zh": "圣斯特凡大教堂", "name_de": "Stephansdom",
        "name_en": "St. Stephen's Cathedral", "type": "教堂",
        "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "新教主教座堂；全德意志福音教会会议与联邦重大国事的举行地；"
                    "保留巴洛克祭坛、镀金讲坛与管风琴",
        "overview": "维也纳的地标教堂，改为新教主教座堂后**完整保留**了原有的巴洛克祭坛、"
                    "镀金讲坛与管风琴。它是「阿尔卑斯福音派」神学最有力的实物宣言："
                    "新教不等于清除美物，美、音乐与食馔皆属上帝创造之恩典。",
        "status": "已确定", "src": ["S0", "S1"],
        "notes": "文档原有条目，此处补全为机构词条。",
    },
    {
        "id": "O_MAGDEBURG_DOM", "name_zh": "马格德堡大教堂", "name_de": "Dom zu Magdeburg",
        "name_en": "Magdeburg Cathedral", "type": "教堂",
        "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "福音殉道者纪念堂；北德意志路德宗圣地",
        "overview": "萨克森-安哈尔特州首府的教堂，被列为福音殉道者纪念堂。"
                    "与南德的圣斯特凡形成对照：此处没有镀金祭坛，只有铭碑与素壁——"
                    "两座教堂并列，即南德与北德新教文化的分野。",
        "status": "已确定", "src": ["S0"],
        "notes": "文档原有条目，此处补全为机构词条。",
    },
    {
        "id": "O_AMS_NIEUWEKERK", "name_zh": "阿姆斯特丹新教堂与西教堂",
        "name_de": "Nieuwe Kerk und Westerkerk Amsterdam",
        "name_en": "Nieuwe Kerk and Westerkerk, Amsterdam", "type": "教堂",
        "country_id": "C_DEUTSCHLAND",
        "members": [],
        "function": "加尔文宗礼拜与市政仪典场所；低地改革宗传统的代表性建筑",
        "overview": "阿姆斯特丹的两座改革宗教堂，低地加尔文宗传统的建筑代表。"
                    "堂内空间素净，讲坛居中而祭坛移侧——与日内瓦圣彼得大教堂同一逻辑："
                    "圣言高于圣事。",
        "status": "已确定", "src": ["S0"],
        "notes": "文档原有条目，此处补全为机构词条。",
    },
    # ================= 法兰克 =================
    {
        "id": "O_NOTRE_DAME_PARIS", "name_zh": "帕里斯圣母大教堂",
        "name_de": "Kathedrale Notre-Dame zu Paris",
        "name_en": "Notre-Dame de Paris", "type": "教堂",
        "country_id": "C_FRANKEN",
        "members": [],
        "function": "天主教法兰克教会的主教座堂之一；哥特式建筑典范",
        "overview": "帕里斯的主教座堂，法兰克天主教的建筑象征。"
                    "在德意志化的法兰克，它承担着一项特殊功能："
                    "以罗曼-法兰西的建筑语言，表达日耳曼政治体的天主教信仰——"
                    "法兰克「属于德意志文明却未成为德国人」的双重性，"
                    "在这座建筑上体现得最直观。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_REIMS_CATHEDRAL", "name_zh": "雷姆斯圣母大教堂",
        "name_de": "Kathedrale Notre-Dame de Reims",
        "name_en": "Reims Cathedral", "type": "教堂",
        "country_id": "C_FRANKEN",
        "members": [],
        "function": "法兰克国王加冕地；藏雷姆斯圣油瓶",
        "overview": "法兰克国王的加冕教堂，三重加冕礼第一重的举行地。"
                    "按 1356 年《法兰克福宪章》，法兰克国王须由雷姆斯大主教在此加冕；"
                    "堂内所藏圣油瓶是法兰克王权最古老的实物凭证。",
        "status": "已确定", "src": ["S0"],
        "notes": "文档原有条目，此处补全为机构词条。",
    },
    {
        "id": "O_ST_DENIS", "name_zh": "圣迪奥尼修斯王家修道院",
        "name_de": "Königliche Abtei St. Dionysius",
        "name_en": "Royal Abbey of St. Denis", "type": "教堂",
        "country_id": "C_FRANKEN",
        "members": [],
        "function": "法兰克王室陵墓；王家丧葬与加冕礼的辅助场所",
        "overview": "法兰克王室的陵墓修道院。国王加冕在雷姆斯，安葬在此——"
                    "一头是圣油与合法性，一头是石棺与记忆。"
                    "两处相距不远，构成法兰克王权从开端到终结的完整空间序列。",
        "status": "已确定", "src": ["S0"],
        "notes": "文档原有条目，此处补全为机构词条。",
    },
    {
        "id": "O_CHARTRES", "name_zh": "沙特尔圣母大教堂",
        "name_de": "Kathedrale Notre-Dame zu Chartres",
        "name_en": "Chartres Cathedral", "type": "教堂",
        "country_id": "C_FRANKEN",
        "members": [],
        "function": "藏圣母面纱；法兰克天主教朝圣地",
        "overview": "法兰克最重要的朝圣教堂之一，以所藏圣母面纱著称。"
                    "在法兰克与伊比利亚长期对立的历史中，它同时是南方法兰克人心目中的"
                    "「正统天主教法兰克」象征——与更靠近奥克地区的妥协地带形成对比。",
        "status": "已确定", "src": ["S0"],
        "notes": "文档原有条目，此处补全为机构词条。",
    },
    {
        "id": "O_CLUNY", "name_zh": "克吕尼修道院旧址与普利姆修道院",
        "name_de": "Cluny und Prüm", "name_en": "Cluny and Prüm",
        "type": "教堂", "country_id": "C_FRANKEN",
        "members": [],
        "function": "本笃会精神的两处纪念地；法兰克修道制度的历史源头",
        "overview": "克吕尼与普利姆两处修道院遗址，代表法兰克的天主教修道传统。"
                    "国王加冕的圣油、王家陵墓的石棺、朝圣地的圣母面纱、"
                    "以及这两处本笃会旧址——合起来构成法兰克天主教的完整实物谱系。",
        "status": "已确定", "src": ["S0"],
        "notes": "文档原有条目，此处补全为机构词条。",
    },
    {
        "id": "O_ST_VICTOR", "name_zh": "圣维克多修道院",
        "name_de": "Abtei St. Victor", "name_en": "Abbey of St. Victor",
        "type": "教堂", "country_id": "C_FRANKEN",
        "members": [],
        "function": "经院神学与神秘主义研究中心；帕里斯王家学院的前身机构之一",
        "overview": "帕里斯的修道院学校，以经院神学与神秘主义著称。"
                    "它是帕里斯成为西欧神学与学术中心的关键环节之一，"
                    "也是后来帕里斯王家学院「神学、教会法、古典语文学、历史编纂学」"
                    "这一学科组合的直接前身。",
        "status": "已确定", "src": ["S0"],
        "notes": "文档原有条目，此处补全为机构词条。",
    },
    {
        "id": "O_LOUVRE", "name_zh": "帕里斯王家美术馆（卢浮宫）",
        "name_de": "Königliche Kunstsammlung zu Paris (Louvre)",
        "name_en": "Royal Art Collection of Paris (Louvre)", "type": "艺术馆",
        "country_id": "C_FRANKEN",
        "members": [],
        "function": "王家绘画与雕塑收藏；1945 年后转为国家美术馆",
        "overview": "帕里斯的王宫与王家收藏。法兰克是「连接西欧、地中海、黎凡特与"
                    "德意志世界的文明边界国家」，其收藏因此带有明显的地中海与近东成分："
                    "黎凡特出土物、北非织物、意大利文艺复兴绘画与本地哥特雕塑同处一馆。",
        "status": "已确定", "src": ["S1"],
        "notes": "本轮新增。S1 记法兰克「拥有地中海传统、北非与黎凡特传统影响」"
                 "与「帕里斯有神学、历史、东方学传统」，故其国家收藏必含近东成分。",
    },
    {
        "id": "O_AVIGNON_PALACE", "name_zh": "阿文根教皇宫",
        "name_de": "Papstpalast zu Avingen", "name_en": "Palace of the Popes, Avignon",
        "type": "宫殿", "country_id": "C_FRANKEN",
        "members": [],
        "function": "教廷在法兰克的驻节地；法兰克与罗马教廷关系的实物见证",
        "overview": "奥克地区阿文根的教皇宫。按 1356 年《法兰克福宪章》，"
                    "教皇承认皇帝对法兰克教会的提名权——"
                    "这座宫殿即那一安排的空间形式：教廷在法兰克境内有驻节之地，"
                    "而法兰克国王的加冕仍需罗马或帝国主教团的认可。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。阿文根（Avingen）已在文档的地名清单中。",
    },
    # ================= 不列颠 =================
    {
        "id": "O_OXFORD", "name_zh": "牛津大学", "name_de": "Universität Oxford",
        "name_en": "University of Oxford", "type": "大学",
        "country_id": "C_UK",
        "members": [],
        "function": "古典学、法务语域训练、宫廷文书官养成；盎格鲁-法兰西语的高等语域中心",
        "overview": "不列颠最古老的大学，宫廷-法务语域的训练场。"
                    "在绝对君主制下，大学不培养自治的市民阶层，而培养王权所需的"
                    "法学家、文书官与教士——这与德意志、法兰克大学承担的"
                    "市民与教会双重职能明显不同。1945 年后转为普通国立大学。",
        "status": "已确定", "src": ["S3"],
        "notes": "本轮新增。S3 记不列颠「宫廷-法务语域」为其语言最高层，此处补出承担该语域训练的机构。",
    },
    {
        "id": "O_CAMBRIDGE", "name_zh": "剑桥大学", "name_de": "Universität Cambridge",
        "name_en": "University of Cambridge", "type": "大学",
        "country_id": "C_UK",
        "members": [],
        "function": "数学、天文学、自然哲学、医学",
        "overview": "不列颠第二所老牌大学，以数学与自然哲学见长。"
                    "与牛津的法务—文书取向互补：一个供给王权的官僚，"
                    "一个供给海军与殖民所需的测算与医学人才。",
        "status": "已确定", "src": ["S3"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_BRITISH_MUSEUM", "name_zh": "不列颠博物馆",
        "name_de": "Britisches Museum", "name_en": "British Museum",
        "type": "博物馆", "country_id": "C_UK",
        "members": [],
        "function": "殖民时代的世界收藏；1945 年后部分藏品归还，馆体改为国立博物馆",
        "overview": "伦敦的殖民时代世界收藏馆。其藏品结构记录了不列颠海洋帝国的范围，"
                    "也记录了 1945 年的断裂——战败后殖民地纷纷瓦解独立，"
                    "部分藏品随之归还或移交。它是「战败不等于解体、但帝国确实缩回」"
                    "这一过程最直观的实物档案。",
        "status": "已确定", "src": ["S3"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_NATIONAL_GALLERY_UK", "name_zh": "不列颠国家美术馆",
        "name_de": "Nationale Kunstgalerie Britanniens",
        "name_en": "National Gallery of Britain", "type": "艺术馆",
        "country_id": "C_UK",
        "members": [],
        "function": "罗曼-法兰西绘画与宫廷古典主义收藏；大陆流亡波次带来的藏品",
        "overview": "伦敦的国家美术馆。不列颠是罗曼-法兰西高文化的实际保存者，"
                    "其收藏因此不同于法兰克：法兰克的罗曼遗产已被日耳曼化，"
                    "而不列颠保存的是「大陆所弃而吾岛所存」的那一支。"
                    "1648 与 1789 两次流亡波次带来的藏品，构成该馆的核心。",
        "status": "已确定", "src": ["S3"],
        "notes": "本轮新增。对应 S3 所述「大陆的法兰克被日耳曼化，旧的法兰西世俗文明"
                 "反在不列颠存活得更纯」。",
    },
    {
        "id": "O_WESTMINSTER", "name_zh": "威斯敏斯特宫廷礼拜堂",
        "name_de": "Hofkapelle Westminster", "name_en": "Westminster Court Chapel",
        "type": "教堂", "country_id": "C_UK",
        "members": [],
        "function": "战前王室新教礼拜场所；国王为教会最高元首的仪式空间",
        "overview": "不列颠王室的礼拜堂。战前国王兼任教会最高元首，主教由王任命；"
                    "此堂即「教会从制衡者变为王权官僚」这一过程的仪式现场。"
                    "1945 年废王、政教分离后，改为自治教会堂，并划归国立博物馆体系。",
        "status": "已确定", "src": ["S3"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_BUCKINGHAM", "name_zh": "白金汉宫",
        "name_de": "Buckingham-Palast", "name_en": "Buckingham Palace",
        "type": "宫殿", "country_id": "C_UK",
        "members": [],
        "function": "蒙福尔王朝王宫；1945 年后改为共和国总统府",
        "overview": "伦敦的王宫，蒙福尔王朝的居所。S3 记蒙福尔四世在此写下 1918 年胜利日记；"
                    "1945 年废王后改为共和国总统府——同一座建筑，"
                    "由「胜利巩固绝对主义」的空间转变为「被监督民主化」的空间。",
        "status": "已确定", "src": ["S3"],
        "notes": "本轮新增。",
    },
    # ================= 伊比利亚 =================
    {
        "id": "O_SALAMANCA", "name_zh": "萨拉曼卡大学", "name_de": "Universität Salamanca",
        "name_en": "University of Salamanca", "type": "大学",
        "country_id": "C_IBERIA",
        "members": [],
        "function": "法学、神学、殖民行政训练；伊比利亚中央集权的官僚来源",
        "overview": "伊比利亚最古老的大学之一，长期为中央集权的国家机器培养法学家与行政官。"
                    "与德意志、法兰克的大学不同，它极少承担市政或教会的自治职能——"
                    "这与 S2 所记伊比利亚「中央集权从未真正逆转」相互印证。",
        "status": "已确定", "src": ["S2"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_PRADO", "name_zh": "伊比利亚王家美术馆（普拉多）",
        "name_de": "Königliche Kunstsammlung Iberiens (Prado)",
        "name_en": "Royal Art Collection of Iberia (Prado)", "type": "艺术馆",
        "country_id": "C_IBERIA",
        "members": [],
        "function": "王家绘画收藏；天主教宗教画与宫廷肖像为主",
        "overview": "伊比利亚的王家美术馆，以天主教宗教画与宫廷肖像为主。"
                    "其藏品中有相当部分来自北非与南意大利——"
                    "这些是伊比利亚「南下北非、长臂管辖那不勒斯」的历史痕迹，"
                    "也是该国作为秩序挑战者的文化自信来源。",
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_ESCORIAL", "name_zh": "埃斯科里亚尔宫",
        "name_de": "Palast Escorial", "name_en": "Escorial Palace",
        "type": "宫殿", "country_id": "C_IBERIA",
        "members": [],
        "function": "伊比利亚王国宫殿与王家陵墓；兼修道院",
        "overview": "伊比利亚王国的宫殿兼修道院，王权与国教的合一空间。"
                    "收复失地运动确立的「共同基督教/伊比利亚身份」在此获得建筑形式："
                    "宫殿、教堂与陵墓同处一体，政治与宗教没有分界。",
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_TOLEDO_CATHEDRAL", "name_zh": "托莱多大教堂",
        "name_de": "Kathedrale von Toledo", "name_en": "Toledo Cathedral",
        "type": "教堂", "country_id": "C_IBERIAN_KINGDOM",
        "members": [],
        "function": "伊比利亚王国首席主教座堂；王国与帝国的加冕、加封礼场所",
        "overview": "托莱多的首席主教座堂，伊比利亚王国的宗教中心。"
                    "该城同时是王国首都——政教合一的格局在空间上极为紧凑。",
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_CORDOBA_MEZQUITA", "name_zh": "科尔多瓦大清真寺（后改主教座堂）",
        "name_de": "Große Moschee von Córdoba",
        "name_en": "Great Mosque of Córdoba", "type": "教堂",
        "country_id": "C_IBERIA",
        "members": [],
        "function": "原科尔多瓦哈里发国大清真寺；收复失地后改为主教座堂",
        "overview": "科尔多瓦哈里发国的大清真寺，收复失地运动后改为主教座堂。"
                    "这一改建本身即伊比利亚历史的核心叙事："
                    "伊斯兰政权被逐出半岛，其最宏大的建筑被转为基督教的礼拜场所——"
                    "而北非西部的基督教化，是同一逻辑在半岛之外的延续。",
        "status": "已确定", "src": ["S0", "S2"],
        "notes": "本轮新增。",
    },
    # ================= 瑞士 =================
    {
        "id": "O_GROSSMUENSTER", "name_zh": "苏黎世大教堂", "name_de": "Grossmünster Zürich",
        "name_en": "Grossmünster, Zurich", "type": "教堂",
        "country_id": "C_SWITZERLAND",
        "members": [],
        "function": "瑞士德语区改革宗发源地之一；改革宗讲道与市政仪典场所",
        "overview": "苏黎世的改革宗大教堂，瑞士德语区宗教改革的起点之一。"
                    "它与日内瓦圣彼得大教堂、巴塞尔诸堂共同构成瑞士改革宗的建筑谱系，"
                    "也是泛德意志语言共同体中「高地德语（含瑞士）」这一支的宗教载体。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。S0 已记苏黎世大教堂，此处补全为机构词条。",
    },
    {
        "id": "O_ST_GOTTHARD_HOSPICE", "name_zh": "圣哥达山口修道院与山间礼拜堂",
        "name_de": "Gotthardkloster und Bergkapellen",
        "name_en": "St. Gotthard Hospice and Mountain Chapels", "type": "教堂",
        "country_id": "C_SWITZERLAND",
        "members": [],
        "function": "阿尔卑斯山口修道院；旅人与朝圣者的庇护所",
        "overview": "阿尔卑斯山口的修道院与山间礼拜堂。S0 将其列为「跨宗教」圣地——"
                    "意即在宗教分裂的欧洲，山口是各方共用的通道，"
                    "不同教派的旅人同在此处投宿。它是「政治边界 ≠ 宗教边界」"
                    "这一文明结构在地形上的体现。",
        "status": "已确定", "src": ["S0"],
        "notes": "本轮新增。S0 已列阿尔卑斯山口修道院与山间礼拜堂为跨宗教圣地。",
    },
    # ================= 近东与伊斯兰世界 =================
    {
        "id": "O_AL_AZHAR", "name_zh": "爱资哈尔学院", "name_de": "Al-Azhar-Hochschule",
        "name_en": "Al-Azhar", "type": "大学", "country_id": "C_EGYPT_REGION",
        "members": [],
        "function": "逊尼派伊斯兰最高学府；法蒂玛王朝创建，后转为逊尼派学术中心",
        "overview": "开罗的伊斯兰最高学府，由法蒂玛王朝创建，后在阿尤布王朝时期转为逊尼派学术中心。"
                    "它在什叶派与逊尼派交替的埃及史上存活下来——"
                    "这一连续性正是埃及作为东地中海与印度洋贸易中转之学术后盾的证明。",
        "status": "已确定", "src": ["S1"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_HAGIA_SOPHIA", "name_zh": "圣索菲亚大教堂",
        "name_de": "Hagia Sophia", "name_en": "Hagia Sophia", "type": "教堂",
        "country_id": "C_BYZANTIUM",
        "members": [],
        "function": "君士坦丁堡海峡政治体的首要教堂；东正教文明核心象征",
        "overview": "君士坦丁堡的大教堂，基督教海峡政治体的宗教中心。"
                    "本世界线中该城未被安纳托利亚突厥帝国吞并，故此堂仍为基督教礼拜场所——"
                    "S4 由此推论「东正教教会显然不会向莫斯科转移」。"
                    "一座建筑的存在，决定了一条教会的去向。",
        "status": "已确定", "src": ["S1", "S4"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_ISFAHAN_MOSQUE", "name_zh": "伊斯法罕王家清真寺",
        "name_de": "Königliche Moschee zu Isfahan",
        "name_en": "Royal Mosque of Isfahan", "type": "教堂",
        "country_id": "C_PERSIA",
        "members": [],
        "function": "什叶派国教的王家清真寺；波斯伊斯兰建筑与瓷砖艺术的顶点",
        "overview": "伊斯法罕的王家清真寺，什叶派国教的建筑象征。"
                    "「波斯」概念撕裂为两支后，此处是伊斯兰什叶派波斯（伊朗）的宗教中心；"
                    "而退守河中及以东的佛教波斯残余，则另有其佛寺系统。",
        "status": "已确定", "src": ["S1"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_SAMARKAND_VIHARA", "name_zh": "撒马尔罕佛寺群",
        "name_de": "Buddhistische Tempel von Samarkand",
        "name_en": "Buddhist Temples of Samarkand", "type": "教堂",
        "country_id": "C_PERSIA_BUDDHIST",
        "members": [],
        "function": "西域-波斯佛教残余的核心寺院；波斯语佛教文献的抄写与保存中心",
        "overview": "河中的佛寺群，佛教波斯残余的宗教中心。"
                    "此处僧人以波斯语诵读、以波斯文抄经——与两日路程外"
                    "用同样的字母写着另一种经的邻邦形成镜像。"
                    "寺院另向敦煌与天山之南分送抄本，构成西域佛教带的知识网络。",
        "status": "已确定", "src": ["S1"],
        "notes": "本轮新增。对应 P5 裁定「波斯概念撕裂为伊朗与佛教-西域波斯残余」。",
    },
    {
        "id": "O_MOSCOW_KREML", "name_zh": "莫斯科克里姆林宫",
        "name_de": "Moskauer Kreml", "name_en": "Moscow Kremlin", "type": "宫殿",
        "country_id": "C_ROS_UHLUS",
        "members": [],
        "function": "罗斯兀鲁思大汗宫廷；藏金帐汗国册封诏书（雅尔里克）",
        "overview": "莫斯科的宫廷城堡，罗斯兀鲁思的统治中心。"
                    "宫内并存东正教教堂与蒙古式仪典厅堂——"
                    "这一空间上的并列，即该国「东正教斯拉夫人口 + 蒙古佛教王朝」"
                    "复合性质的直接呈现。册封诏书（雅尔里克）即藏于此。",
        "status": "已确定", "src": ["S4"],
        "notes": "本轮新增。",
    },
    # ================= 东亚与南亚 =================
    {
        "id": "O_DUNHUANG_CAVES", "name_zh": "敦煌石窟群", "name_de": "Höhlen von Dunhuang",
        "name_en": "Dunhuang Caves", "type": "教堂", "country_id": "C_CHINA",
        "members": [],
        "function": "东方佛教门户；写经与壁画的保存中心；东西交通的宗教节点",
        "overview": "敦煌的石窟群，东方佛教的门户。S1 明确其「继续作为东方佛教门户」，"
                    "在西域佛教文明带长期存在的世界线中，它的地位比现实更重——"
                    "此处是印度佛教 → 犍陀罗 → 西域 → 中亚 → 中国这条链条的关键一环。",
        "status": "已确定", "src": ["S1"],
        "notes": "本轮新增。",
    },
    {
        "id": "O_KUCHA_CAVES", "name_zh": "龟兹石窟群", "name_de": "Höhlen von Kutscha",
        "name_en": "Kucha Caves", "type": "教堂", "country_id": "C_WESTERN_REGIONS",
        "members": [],
        "function": "西域佛教文明带的中心寺院群；吐火罗语佛典中心",
        "overview": "龟兹的石窟寺院群，西域佛教文明带的核心。"
                    "现实中龟兹约在 12 世纪前后结束佛教时代，本世界线改变这一节点——"
                    "伊斯兰化止步于更西侧，龟兹的佛教延续至今。",
        "status": "已确定", "src": ["S1"],
        "notes": "本轮新增。",
    },
    # ================= 新大洲与西欧跨区 =================
    {
        "id": "O_EUROPA_ACADEMY", "name_zh": "欧洲学院（欧盟共同高等教育机构）",
        "name_de": "Europäische Akademie", "name_en": "European Academy",
        "type": "大学", "country_id": "C_EUROPE_CONTINENT",
        "members": ["C_DEUTSCHLAND", "C_FRANKEN", "C_IBERIA", "C_UK", "C_SWITZERLAND", "C_KIEV"],
        "function": "欧盟框架下的共同高等教育与比较法研究；「多层政治传统的现代民主化延续」的教育载体",
        "overview": "欧盟框架下设立的共同高等教育机构，由德意志、法兰克、伊比利亚、"
                    "不列颠、瑞士与基辅王国联合办学。其课程以比较宪法与多层治理为核心——"
                    "这正是 S2 所论「把欧盟理解为古老欧洲多层政治传统的现代民主化延续」"
                    "在教育制度上的落地。",
        "status": "已确定", "src": ["S2"],
        "notes": "本轮新增。",
    },
]

# ---------------------------------------------------------------- 相关地点
PLACES = [
    {"id": "P_ISFAHAN_MOSQUE", "type": "宗教圣地", "zh": "伊斯法罕王家清真寺",
     "real": "Shah Mosque, Isfahan", "de": "Königliche Moschee Isfahan",
     "en": "Royal Mosque of Isfahan", "fa": "مسجد شاه",
     "note": "什叶派国教的王家清真寺", "country_id": "C_PERSIA", "src": ["S1"]},
    {"id": "P_SAMARKAND_TEMPLE", "type": "宗教圣地", "zh": "撒马尔罕佛寺群",
     "real": "（推定）", "de": "Buddhistische Tempel Samarkand",
     "en": "Buddhist Temples, Samarkand",
     "note": "西域-波斯佛教残余的核心寺院", "country_id": "C_PERSIA_BUDDHIST", "src": ["S1"]},
    {"id": "P_KREML", "type": "宫殿", "zh": "莫斯科克里姆林宫", "real": "Moscow Kremlin",
     "de": "Moskauer Kreml", "en": "Moscow Kremlin", "ru": "Московский Кремль",
     "note": "罗斯兀鲁思大汗宫廷", "country_id": "C_ROS_UHLUS", "src": ["S4"]},
    {"id": "P_DUNHUANG_CAVES", "type": "宗教圣地", "zh": "敦煌石窟群",
     "real": "Mogao Caves", "de": "Höhlen von Dunhuang", "en": "Dunhuang Caves",
     "note": "东方佛教门户", "country_id": "C_CHINA", "src": ["S1"]},
    {"id": "P_KUCHA_CAVES", "type": "宗教圣地", "zh": "龟兹石窟群",
     "real": "Kizil Caves", "de": "Höhlen von Kutscha", "en": "Kucha Caves",
     "note": "西域佛教文明带中心", "country_id": "C_WESTERN_REGIONS", "src": ["S1"]},
]
