# -*- coding: utf-8 -*-
"""
历史物品留存层
================
设定中的实物遗存：加冕礼器、文书正本、徽记、建筑构件、宗教法器、
工业遗产、科学仪器、货币、旗帜等。

每条都锚定 S0–S4 已确立的设定，说明其形制、来历、保存地与象征意义。
不新增与正典冲突的史实。
"""

ARTIFACTS = [
    # ---------------- 加冕与王权礼器 ----------------
    {
        "id": "AR_STEPHAN_CROWN", "name_zh": "圣斯特凡王冠（波西米亚—奥地利王冠）",
        "name_de": "Stephanskrone", "name_en": "Crown of St. Stephen",
        "kind": "加冕礼器", "period": "中世纪 — 至今",
        "holder": "C_DEUTSCHLAND", "place_id": "P_VIENNA",
        "repository": "维也纳霍夫堡王室宝库",
        "overview": "普热米斯尔家族的加冕王冠，波西米亚—奥地利王统的象征。"
                    "1871 年罗马加冕成立德意志帝国后，它成为帝国皇权在行政首都的实体依托——"
                    "行政在维也纳，圣事在罗马，而这顶王冠居于两者之间。"
                    "1918 年王朝结束后移交共和国，现为联邦国家博物馆的首要藏品。",
        "material": "黄金、珐琅、波西米亚石榴石、珍珠",
        "significance": "普热米斯尔王统的连续性象征；1871—1918 年德意志皇权的核心礼器",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_REIMS_AMPULLA", "name_zh": "雷姆斯圣油瓶",
        "name_de": "Heilige Ampulle von Reims", "name_en": "Holy Ampulla of Reims",
        "kind": "加冕礼器", "period": "中世纪 — 至今",
        "holder": "C_FRANKEN", "place_id": "P_REIMS",
        "repository": "雷姆斯圣母大教堂宝库",
        "overview": "法兰克国王加冕所用的圣油容器，存于雷姆斯圣母大教堂。"
                    "按 1356 年《法兰克福宪章》所定，法兰克国王须由雷姆斯大主教在雷姆斯加冕，"
                    "此瓶即该仪式的核心法器。它是法兰克王权合法性最古老的实物凭证，"
                    "也是「天主教法兰克民族意识」的象征物。",
        "material": "黄金、宝石",
        "significance": "法兰克王冠合法性的核心法器；三重加冕礼第一重的必备之物",
        "status": "已确定", "src": ["S0"],
    },
    {
        "id": "AR_IMPERIAL_SEAL_1356", "name_zh": "《法兰克福宪章》御玺",
        "name_de": "Kaisersiegel der Frankfurter Verfassung",
        "name_en": "Imperial Seal of the Charter of Frankfurt",
        "kind": "文书正本与玺印", "period": "1356",
        "holder": "C_DEUTSCHLAND", "place_id": "P_FRANKFURT",
        "repository": "法兰克福帝国议会档案馆",
        "overview": "1356 年《法兰克福宪章》正本所钤之玺，连同七位选侯之印与教皇使节之印。"
                    "该宪章确立双重王冠不可分割、选举与继承双轨制与三重加冕，"
                    "本玺即这套制度矛盾的法律凭证。宪章正本与玺印现存法兰克福帝国议会档案馆，"
                    "是帝国议会开会时的礼仪性展示物。",
        "material": "蜜蜡、丝绦、羊皮纸",
        "significance": "双王冠制度的法律凭证；帝国议会合法性展示物",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_SEVEN_ELECTORS_STAFF", "name_zh": "七选侯权杖",
        "name_de": "Kurfürstenstäbe der Sieben",
        "name_en": "Staves of the Seven Electors",
        "kind": "礼制器物", "period": "1356 — 至今",
        "holder": "C_DEUTSCHLAND", "place_id": "P_FRANKFURT",
        "repository": "法兰克福帝国议会档案馆",
        "overview": "七位选侯各持一杖：美因茨、科隆、特里尔三大主教，以及波西米亚国王、"
                    "莱茵普法尔茨伯爵、萨克森公爵、勃兰登堡藩侯。"
                    "德意志国王由七侯于法兰克福选举，选举时七杖并列，"
                    "杖身刻有各家的纹章与「法兰克福宪章」条文首句。",
        "material": "乌木、镀金、银、珐琅纹章",
        "significance": "选举制度的实物化；普热米斯尔持杖权在其家族存续期内从未旁落",
        "status": "已确定", "src": ["S0"],
    },
    # ---------------- 宗教法器 ----------------
    {
        "id": "AR_HUSSITE_CHALICE", "name_zh": "胡斯派圣杯",
        "name_de": "Hussitenkelch", "name_en": "Hussite Chalice",
        "kind": "宗教法器", "period": "15世纪 — 至今",
        "holder": "C_DEUTSCHLAND", "place_id": "P_PRAG",
        "repository": "布拉格伯利恒礼拜堂旧址（胡斯派传统陈列）",
        "overview": "波西米亚胡斯派的核心法器。胡斯派坚持平信徒领圣餐（杯与饼同领），"
                    "圣杯因之成为该派标志。此杯为胡斯派传统中最受尊崇的一件，"
                    "16 世纪胡斯派与路德宗融合后仍保留圣杯传统，"
                    "普热米斯尔家族以教会保护者身份保管之。",
        "material": "镀银铜、波西米亚水晶",
        "significance": "胡斯派-路德宗混合教会的核心象征；普热米斯尔宗教合法性的实物",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_WITTENBERG_DOOR", "name_zh": "维滕堡城堡教堂大门（九十五条论纲之门）",
        "name_de": "Thesentür der Schlosskirche Wittenberg",
        "name_en": "Theses Door of Wittenberg Castle Church",
        "kind": "建筑构件", "period": "1517 — 至今",
        "holder": "C_DEUTSCHLAND", "place_id": "P_WITTENBERG",
        "repository": "维滕堡城堡教堂（新教母教会）",
        "overview": "马丁·路德张贴《九十五条论纲》之门，新教母教会的标志性实物。"
                    "原门于战火中损毁后，以青铜重铸，门面铸有论纲拉丁原文。"
                    "每年宗教改革纪念日，全德意志福音教会会议在此门前列队。",
        "material": "青铜（重铸件）",
        "significance": "新教母教会的标志物；德意志新教世界的精神原点",
        "status": "已确定", "src": ["S0"],
    },
    {
        "id": "AR_ALPINE_ALTAR", "name_zh": "阿尔卑斯福音派巴洛克祭坛（圣斯特凡）",
        "name_de": "Barockaltar der Alpenländischen Evangelischen Kirche",
        "name_en": "Baroque Altar of the Alpine Evangelical Church",
        "kind": "教堂陈设", "period": "17世纪 — 至今",
        "holder": "C_DEUTSCHLAND", "place_id": "P_VIENNA",
        "repository": "维也纳圣斯特凡大教堂",
        "overview": "圣斯特凡大教堂改为新教主教座堂后**保留**的巴洛克祭坛。"
                    "它是「阿尔卑斯福音派」神学立场的物证：该派认为美、音乐与食馔皆是"
                    "上帝创造之恩典，故不弃教堂艺术。祭坛旁的镀金讲坛与管风琴同属此列。"
                    "此物与新教母教会维滕堡的素朴风格形成鲜明对照。",
        "material": "镀金木雕、大理石",
        "significance": "「十字架下的喜悦」的物证；南德新教与北德新教文化分野的实物标志",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_CALVIN_PULPIT", "name_zh": "加尔文讲坛（日内瓦圣彼得大教堂）",
        "name_de": "Calvin-Kanzel im Genfer Petersdom",
        "name_en": "Calvin's Pulpit, St. Peter's Geneva",
        "kind": "教堂陈设", "period": "16世纪 — 至今",
        "holder": "C_SWITZERLAND", "place_id": "P_GENF",
        "repository": "日内瓦圣彼得大教堂",
        "overview": "加尔文在日内瓦布道所用讲坛，改革宗传统的核心实物。"
                    "讲坛位于堂内视觉中心，而祭坛被移于侧位——这一空间安排本身"
                    "即改革宗神学的表述：圣言高于圣事。"
                    "日内瓦学院以此坛为国际改革宗神学教育的象征。",
        "material": "橡木",
        "significance": "改革宗「圣言中心」神学的空间化实物；日内瓦国际神学传统象征",
        "status": "已确定", "src": ["S0"],
    },
    # ---------------- 文书与档案 ----------------
    {
        "id": "AR_VIENNA_TREATY_ORIGINAL", "name_zh": "《维也纳和约》正本",
        "name_de": "Original des Wiener Friedens",
        "name_en": "Original of the Peace of Vienna",
        "kind": "文书正本", "period": "1648",
        "holder": "C_DEUTSCHLAND", "place_id": "P_VIENNA",
        "repository": "维也纳国家档案馆",
        "overview": "1648 年结束三十年宗教战争的条约正本，拉丁文本，附高地德语、法兰克语、"
                    "低地德语与伊比利亚-奥克语四种副本。正本列九条：宗教自选、低地独立、"
                    "瑞士中立确认、波西米亚恢复胡斯派-路德宗混合教会、阿尔卑斯福音派获承认、"
                    "北意大利归属、奥克占领后撤、西里西亚与摩拉维亚归普热米斯尔、帝国进一步分权。",
        "material": "羊皮纸、蜜蜡玺印、丝绦",
        "significance": "「政治边界 ≠ 宗教边界 ≠ 文化边界」这一文明结构的法律源头",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_TWELVE_ARTICLES", "name_zh": "《十二条款》农民战争传单",
        "name_de": "Flugblatt der Zwölf Artikel",
        "name_en": "Broadside of the Twelve Articles",
        "kind": "文书与印刷品", "period": "1524—1525",
        "holder": "C_DEUTSCHLAND", "place_id": "P_WITTENBERG",
        "repository": "德意志联邦国家博物馆（社会史部）",
        "overview": "农民战争期间起义者纲领的印刷传单，要求自由选举牧师、废除农奴制、"
                    "恢复公地权利、降低赋税劳役、限制贵族司法权、宗教自由；"
                    "南德意志版本另增「保留教堂艺术与音乐、农民子弟受教育、建立农民自治社区」三项。"
                    "传单在德意志、莱茵兰、波西米亚与北意大利广泛翻印。",
        "material": "纸质印刷、木刻插图",
        "significance": "农民战争的纲领物证；南北德意志新教文化分野的早期文本证据",
        "status": "已确定", "src": ["S0"],
    },
    {
        "id": "AR_RIGHTS_CHARTER", "name_zh": "不列颠《权利宪章》1945/1947 正本",
        "name_de": "Urkunde der britischen Charta der Rechte",
        "name_en": "Original of the British Charter of Rights",
        "kind": "文书正本", "period": "1945/1947",
        "holder": "C_UK", "place_id": "P_LONDON",
        "repository": "伦敦制宪会议大厦（原枢密院法庭旧址）",
        "overview": "不列颠战败后被监督民主化的产物：成文宪法，确立人民主权与司法独立，"
                    "下议院普选为政府来源，上议院仅保留延搁权，新设宪法法院，"
                    "废除枢密院法庭与出版审查，实行政教分离。"
                    "正本陈列于原枢密院法庭（星室式法庭）旧址——该法庭恰于 1945 年被废除。",
        "material": "犊皮纸、蜡印",
        "significance": "不列颠由绝对君主制转为共和国的法律凭证；「被监督强制的民主化」的物证",
        "status": "已确定", "src": ["S3"],
    },
    {
        "id": "AR_GOLDEN_HORDE_YARLIK", "name_zh": "金帐汗国册封诏书（雅尔里克）",
        "name_de": "Jarlyk der Goldenen Horde", "name_en": "Yarlik of the Golden Horde",
        "kind": "文书正本", "period": "14世纪",
        "holder": "C_ROS_UHLUS", "place_id": "P_MOSCOW",
        "repository": "莫斯科罗斯兀鲁思国家档案馆",
        "overview": "金帐汗国册封莫斯科大公的诏书（雅尔里克），以蒙古文与察合台文书写，"
                    "附东斯拉夫语译本。此件是罗斯兀鲁思国家正统的核心物证："
                    "该国自认历史序列为「古罗斯诸国 → 蒙古征服 → 金帐秩序 → 罗斯兀鲁思」，"
                    "并视金帐汗国为自己的前身王朝，而非外国占领政权。"
                    "诏书上敕封者之印与莫斯科大公之印并列——这一并列本身即该国"
                    "「东斯拉夫人口 + 蒙古王朝」复合性质的象征。",
        "material": "纸质（桑皮纸）、朱印",
        "significance": "罗斯兀鲁思国家正统的核心物证；否定「鞑靼枷锁」叙事的实物",
        "status": "已确定", "src": ["S4"],
    },
    {
        "id": "AR_MAGNA_CARTA_MORTUA_DOC", "name_zh": "《贵族宪章废止令》原件",
        "name_de": "Annullierungsurkunde der Baronencharta",
        "name_en": "Writ of Annulment of the Baronial Charter",
        "kind": "文书正本", "period": "14世纪初",
        "holder": "C_UK", "place_id": "P_LONDON",
        "repository": "伦敦国家档案馆（1945 年后重新展出）",
        "overview": "不列颠国王会同枢密院废止 1215 年式贵族宪章的文书。"
                    "签署该宪章的男爵正是主张大陆路线而失败的一派。"
                    "此后等级会议自 14 世纪后基本停开，此令成为**死掉的先例**，"
                    "直到 1945 年战败后被民主派重新挖掘为宪法传统的起点，"
                    "并与《权利宪章》并列展出。",
        "material": "羊皮纸、御玺",
        "significance": "不列颠「宪政不是中世纪遗产」这一论断的关键物证；1945 年后被重新诠释",
        "status": "已确定", "src": ["S3"],
    },
    # ---------------- 徽记与旗帜 ----------------
    {
        "id": "AR_DOUBLE_CROWN_BANNER", "name_zh": "双王冠旗",
        "name_de": "Doppelkronenbanner", "name_en": "Dual Crown Banner",
        "kind": "旗帜与徽记", "period": "1356 — 1871",
        "holder": "C_FRANKEN", "place_id": "P_FRANKFURT",
        "repository": "法兰克福帝国议会档案馆（与帕里斯王家武库分藏两幅）",
        "overview": "法兰克王冠与德意志王冠并置于一旗的帝国旗，1356 年《法兰克福宪章》后启用，"
                    "1871 年双王冠分离后废止。旗面左半为哈布斯堡法兰克的深蓝底金鹰，"
                    "右半为普热米斯尔的酒红底银狮，中缝以帝国之鹰统摄二者。"
                    "帝国议会开幕时悬于会场正中，是「同一皇帝、两个政治民族」这一制度矛盾的视觉化。",
        "material": "丝织、金线绣",
        "significance": "双王冠制度的旗帜化；1871 年后成为历史陈列品",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_ALPINE_EAGLE_STANDARD", "name_zh": "阿尔卑斯福音派军旗",
        "name_de": "Feldzeichen der Alpenländischen Evangelischen",
        "name_en": "Standard of the Alpine Evangelical Church",
        "kind": "旗帜与徽记", "period": "17世纪 — 至今",
        "holder": "C_DEUTSCHLAND", "place_id": "P_MUENCHEN",
        "repository": "慕尼黑巴伐利亚国家博物馆",
        "overview": "三十年宗教战争期间南德意志新教军队的军旗。旗面以酒红为地，"
                    "绣银狮与圣经经文，四角饰以啤酒花与葡萄藤纹——"
                    "这正是「阿尔卑斯福音派」的神学表态：喜乐与丰饶亦属恩典。"
                    "北德意志路德宗的军旗则是纯黑底白十字，无任何装饰。两面旗并列展出，"
                    "直观呈现南德与北德新教的文化分野。",
        "material": "羊毛织物、丝线绣",
        "significance": "南德新教文化立场的实物；与北德路德宗军旗形成对照展品",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_OCCITAN_CROSS", "name_zh": "奥克十字旗",
        "name_de": "Okzitanisches Kreuzbanner", "name_en": "Occitan Cross Banner",
        "kind": "旗帜与徽记", "period": "中世纪 — 至今",
        "holder": "C_FRANKEN", "place_id": "P_THOLOSEN",
        "repository": "托洛森奥克文化博物馆",
        "overview": "奥克语地区的传统徽记，十二尖十字。1789 年伊比利亚-奥克大革命时被起义者"
                    "用作旗帜；1945 年法兰克设南部奥克省后一度被禁，"
                    "1972—1978 年奥克正常化后恢复为**文化标志**（非政治标志），"
                    "现于州级文化机构与双语学校悬挂。其法律地位的变化，"
                    "本身即法兰克奥克政策「先控制、再正常化」的实物记录。",
        "material": "织物、印染",
        "significance": "奥克文化承认的实物标志；其法律地位的变迁记录法兰克奥克政策",
        "status": "已确定", "src": ["S0", "S2"],
    },
    # ---------------- 工业与科学 ----------------
    {
        "id": "AR_BOHEMIA_DYNAMO", "name_zh": "布拉格首台工业发电机",
        "name_de": "Erster Industrieller Dynamo Prags",
        "name_en": "Prague's First Industrial Dynamo",
        "kind": "工业遗产", "period": "19世纪后期",
        "holder": "C_DEUTSCHLAND", "place_id": "P_PRAG",
        "repository": "布拉格国家技术博物馆",
        "overview": "多瑙河-波西米亚工业带的首批发电设备之一，标志该工业带以"
                    "「电气、汽车、军火」为核心的产业特征。"
                    "此机与维也纳、布雷斯劳的同类设备同属一个技术谱系，"
                    "是德意志世界「不是单一工业核心、而是多个历史工业区叠加」的实物证据——"
                    "也正是这一结构使中欧在输掉一战后仍能恢复。",
        "material": "铸铁、铜绕组、大理石基座",
        "significance": "多瑙河-波西米亚工业带的起点物证；「一战战败仍能恢复」的结构性资产之一",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_MILAN_LOOM", "name_zh": "米兰精密织机（波河-阿尔卑斯工业带）",
        "name_de": "Präzisionswebstuhl aus Mailand",
        "name_en": "Precision Loom from Milan",
        "kind": "工业遗产", "period": "19世纪后期",
        "holder": "C_DEUTSCHLAND", "place_id": "P_MAILAND",
        "repository": "米兰理工大学机械美学陈列馆",
        "overview": "波河-阿尔卑斯工业带（伦巴底、皮埃蒙特、威尼托）的代表性设备，"
                    "体现该带「纺织、金融、精密仪器」的产业特征。"
                    "机身上的雕饰并非装饰多余，而是该带「机械美学」传统的体现——"
                    "米兰理工大学与伦巴底美学院共设的工业设计课程以此机为教学范本。",
        "material": "钢、黄铜、胡桃木",
        "significance": "波河-阿尔卑斯工业带的物证；「机械美学」教学范本",
        "status": "已确定", "src": ["S0"],
    },
    {
        "id": "AR_GOTTINGEN_SEXTANT", "name_zh": "哥廷根天文台六分仪",
        "name_de": "Göttinger Sextant", "name_en": "Göttingen Sextant",
        "kind": "科学仪器", "period": "18—19世纪",
        "holder": "C_DEUTSCHLAND", "place_id": "P_GOETTINGEN",
        "repository": "哥廷根大学天文台（数学与天文学部）",
        "overview": "哥廷根大学天文台使用的大型六分仪。哥廷根大学以数学、天文学、"
                    "实验物理、东方学与统计学著称，此仪即其天文传统的实物。"
                    "一战后的知识分子流散中，哥廷根的学者多留在中欧参与重建，"
                    "该天文台的观测序列因此未中断——这与迁往美国、瑞士的学者形成对照。",
        "material": "黄铜、乌木、望远镜镜片",
        "significance": "哥廷根学术传统的物证；「人才留在中欧」这一设定的实物印证",
        "status": "已确定", "src": ["S0", "S1"],
    },
    # ---------------- 货币与经济 ----------------
    {
        "id": "AR_HANSA_GUILDER", "name_zh": "汉萨三城联合印记",
        "name_de": "Verbundsiegel der drei Hansestädte",
        "name_en": "Joint Seal of the Three Hanseatic Cities",
        "kind": "商业印信", "period": "中世纪 — 至今",
        "holder": "C_DEUTSCHLAND", "place_id": "P_HAMBURG",
        "repository": "汉堡汉萨博物馆（阿姆斯特丹与不来梅各存一副印）",
        "overview": "汉堡、不来梅、阿姆斯特丹三城的联合印记，用于共同签署贸易协定与"
                    "担保跨城债务。三城在德意志联邦中均为**城市州**，保留商业自治传统。"
                    "此印按 1356 年《法兰克福宪章》授予自由汉萨城市的议会代表权而立，"
                    "是「城市自治进入帝国制度」的实物凭证。",
        "material": "青铜印模、火漆",
        "significance": "自由汉萨城市议会代表权的实物凭证；三城城市州地位的历史依据",
        "status": "已确定", "src": ["S0"],
    },
    {
        "id": "AR_STANDARD_GERMAN_SAMPLE", "name_zh": "《共同体德语正字法》标准字样本",
        "name_de": "Normblatt der Gemeindeutschen Rechtschreibung",
        "name_en": "Specimen Sheet of Common German Orthography",
        "kind": "文献与样本", "period": "18世纪（推定）",
        "holder": "C_DEUTSCHLAND", "place_id": "P_FRANKFURT",
        "repository": "法兰克福泛德意志语言会议档案馆",
        "overview": "泛德意志语言会议颁行的标准字样本，列示统一正字法的五条原则"
                    "（词源优先、跨方言折中、词汇层融合、语法保守、拼写标注发音）"
                    "与示范词条，如「machen/maken 统一为 machen」「Nation → Volkheit」"
                    "「Religion → Glaubenslehre」。样本由德意志各州教育部长、"
                    "法兰克王家学院院士、苏黎世联邦理工学院与巴塞尔大学学者、"
                    "三大新教教会与天主教法兰克教会代表共同签署。",
        "material": "纸质印刷、手写签署页",
        "significance": "三国统一正字法的原始样本；德意志、法兰克、瑞士语言共同体的物证",
        "status": "已确定", "src": ["S0"],
    },
    # ---------------- 战争纪念 ----------------
    {
        "id": "AR_TRIEST_ANCHOR", "name_zh": "的里雅斯特共管锚",
        "name_de": "Anker von Triest", "name_en": "Anchor of Trieste",
        "kind": "战争纪念物", "period": "1918年后",
        "holder": "C_DEUTSCHLAND", "place_id": "P_TRIEST",
        "repository": "的里雅斯特国际共管区纪念广场",
        "overview": "一战战败后，奥地利德意志被迫接受的里雅斯特国际共管；"
                    "此锚为共管体制建立时的纪念物，锚身刻有共管四方的标记与年份。"
                    "它是德意志世界一战战败的直接物证——"
                    "而这正是 S1 所论的「韧性测试」：失去领土与国家形式，"
                    "但维也纳、布拉格、米兰、阿姆斯特丹的学院与工厂仍在。",
        "material": "铸铁、青铜铭牌",
        "significance": "一战战败与的里雅斯特共管的物证；「韧性测试」命题的实物注脚",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_NORMANDY_SHIELD", "name_zh": "诺曼底公爵之盾（1272 年决战遗物）",
        "name_de": "Schild des Herzogs der Normandie",
        "name_en": "Shield of the Duke of Normandy",
        "kind": "战争遗物", "period": "1272",
        "holder": "C_FRANKEN", "place_id": "P_PARIS",
        "repository": "帕里斯王家武库（后为法兰克国家军事博物馆）",
        "overview": "1272 年决战中诺曼底公爵所遗之盾。此役中鲁道夫击败诺曼底公爵，"
                    "夺取法兰西岛与香槟，英格兰-诺曼底被逐出大陆。"
                    "盾面凹陷处即当日所受重击。此物与「鲁道夫加冕诏书」并列陈列，"
                    "构成法兰克建国的双件套——加冕的合法性，与被逐者的失败。",
        "material": "橡木、铁箍、皮革",
        "significance": "法兰克建国的物证之一；英-法兰克竞争长期化的起点实物",
        "status": "已确定", "src": ["S0", "S1"],
    },
    {
        "id": "AR_RECONQUISTA_KEY", "name_zh": "格拉纳达城门钥匙",
        "name_de": "Schlüssel von Granada", "name_en": "Key of Granada",
        "kind": "战争遗物", "period": "15世纪末",
        "holder": "C_IBERIAN_KINGDOM", "place_id": "P_GRANADA",
        "repository": "托莱多伊比利亚王国军械库（后为伊比利亚国家历史博物馆）",
        "overview": "收复失地运动终局时，安达卢斯最后据点格拉纳达的城门钥匙。"
                    "此物象征伊比利亚各基督教王国完成半岛统一，并由此转向南下北非、"
                    "驱逐穆斯林、长期基督教化与欧洲化马格里布。"
                    "在伊比利亚的政治象征体系中，它与「共同基督教/伊比利亚身份」直接绑定——"
                    "而这正是该国「中央集权从未真正逆转」的合法性来源。",
        "material": "铁、镀银铭牌",
        "significance": "收复失地运动终局的物证；伊比利亚国家合法性的核心象征物之一",
        "status": "已确定", "src": ["S0", "S2"],
    },
    {
        "id": "AR_MAGHREB_BELL", "name_zh": "马格里布基督教化纪念钟",
        "name_de": "Glocke der Christianisierung des Maghreb",
        "name_en": "Bell of the Christianisation of the Maghreb",
        "kind": "宗教纪念物", "period": "16世纪后",
        "holder": "C_MAGHREB", "place_id": "P_MARRAKECH",
        "repository": "马拉喀什圣堂（原穆瓦希德王朝都城）",
        "overview": "伊比利亚南下北非、驱逐穆斯林之后，在马格里布铸造的纪念钟。"
                    "钟身铭文记伊比利亚对北非西部的长期统治与基督教化。"
                    "此物是 S2「北非西部与半岛同属一个国家行政体系、无特殊宪制地位」"
                    "这一设定的实物记录——它不是殖民地的纪念物，而是**本土**的纪念物。",
        "material": "青铜",
        "significance": "马格里布基督教化与欧洲化的物证；「北非为本土一部分」的实物说明",
        "status": "已确定", "src": ["S0", "S2"],
    },
]
