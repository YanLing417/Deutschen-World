# -*- coding: utf-8 -*-
"""
文献扩充层（第三批）
======================
把仿真文献从 86 篇补足到 100 篇（本文件提供 14 篇）。
"""
DOCUMENTS = [
    {
        "id": "DOC_WIENER_ZEITUNG_1918", "kind": "文献·报刊", "year": 1918,
        "year_text": "1918年11月", "place": "维也纳", "place_id": "P_VIENNA",
        "title": "《维也纳日报》停战号",
        "title_orig": "Wiener Zeitung, Waffenstillstandsnummer",
        "author": "维也纳日报编辑部", "lang": "共同体德语",
        "context": "一战中欧战败，奥地利德意志君主政体瓦解，建立维也纳德意志共和国；"
                   "双方两败俱伤。",
        "body": """<p class="doc-preamble">维也纳日报。号外。</p>

<h4>停战</h4>
<p>前线司令部今日公告：停战协议已签字。战事终止。</p>

<h4>皇帝退位</h4>
<p>普热米斯尔王朝今日结束。维也纳成立德意志共和国，临时政府已接管各机关。</p>

<h4>和约条件（传闻）</h4>
<p>据本埠消息：波兰地区须释放；北意大利须设非军事区；的里雅斯特或由国际共管；军队限额；赔款待议。以上未获官方证实。</p>

<h4>本报社论</h4>
<p>本埠各校今日照常上课。维也纳大学、卡尔大学、米兰理工、阿姆斯特丹自由大学均未停课。本社以为，此事的义比停战更大。</p>

<p class="doc-seal">〔维也纳日报编辑部〕</p>""",
        "significance": "以一战后当日报纸的形态同时报道停战、王朝终结与和约条件，"
                        "并在社论中点出「学校照常上课，此事意义比停战更大」这一韧性命题。",
        "src": ["S0", "S1"],
    },
    {
        "id": "DOC_RAILWAY_DIRECTIVE", "kind": "文献·交通指令", "year": 1900,
        "year_text": "1900年前后", "place": "维也纳", "place_id": "P_VIENNA",
        "title": "《帝国铁路联运指令》",
        "title_orig": "Weisung über den gemeinsamen Eisenbahnverkehr",
        "author": "德意志帝国交通部", "lang": "共同体德语",
        "context": "S0 横轴指标「交通基础设施」与地图工程「汉萨贸易铁路」；"
                   "德意志世界拥有三个巨型工业带。",
        "body": """<p class="doc-preamble">德意志帝国交通部指令。</p>

<h4>第一条　三带联运</h4>
<p>莱茵-低地、多瑙-波西米亚、波河-阿尔卑斯三工业带之间，实行统一时刻与统一运价。</p>

<h4>第二条　口岸衔接</h4>
<p>汉堡、不来梅、阿姆斯特丹三港与内地各站，实行直通货运。货至口岸不再换单。</p>

<h4>第三条　跨境</h4>
<p>与法兰克、瑞士之铁路，依各自协定衔接。在边境站换轨不换车。</p>

<h4>第四条　同制之由</h4>
<p>三国共一标准语，故单据、标识、时刻表皆用共同体德语，无须另译。此为本帝国铁路之独有便利。</p>

<p class="doc-seal">〔钤印：德意志帝国交通部〕</p>""",
        "significance": "把「三国共一标准语」这一语言设定的**实用后果**（单据无需翻译）"
                        "落实为交通指令，并呈现三大工业带的物理连接。",
        "src": ["S0"],
    },
    {
        "id": "DOC_UNIVERSITY_CHARTER", "kind": "文献·特许状", "year": 1600,
        "year_text": "17世纪（推定）", "place": "维也纳", "place_id": "P_VIENNA",
        "title": "《维也纳大学特许状（新教时期重颁）》",
        "title_orig": "Neuausgestellte Stiftungsurkunde der Universität Wien",
        "author": "普热米斯尔皇帝", "lang": "高地德语",
        "context": "S0：维也纳大学为学术圣地，涵盖神学、法学、医学、哲学、经济学、工程科学；"
                   "南德意志阿尔卑斯福音派保留主教制，主教由牧师与信徒代表共同选举。",
        "body": """<p class="doc-preamble">奉上帝恩典，普热米斯尔皇帝重颁维也纳大学特许状。</p>

<h4>一　学部</h4>
<p>设神学、法学、医学、哲学四部，另设经济学与工程科学二部。工程学部与工坊相连，学生得入厂实习。</p>

<h4>二　神学</h4>
<p>神学部依阿尔卑斯福音派之信条授课。本院不设拉丁弥撒之必修，然保留教会史与教堂艺术之课程。</p>

<h4>三　主教之选</h4>
<p>本邦主教由牧师与信徒代表共同选举，不由朝廷任命。大学神学部为选举之预备教育机构。</p>

<h4>四　自治</h4>
<p>大学自选校长、自定课程、自管学位。朝廷只验其年课，不干预其教法。</p>

<p class="doc-seal">〔钤印：皇帝御玺、维也纳大学评议会〕</p>""",
        "significance": "把「南德新教保留主教制、但主教由牧师与信徒代表共同选举」"
                        "与大学的学部结构写入特许状，说明南德新教体制的组织原则。",
        "src": ["S0", "S1"],
    },
    {
        "id": "DOC_MAGHREB_ANNEX", "kind": "文献·行政敕令", "year": 1560,
        "year_text": "16世纪", "place": "马拉喀什", "place_id": "P_MARRAKECH",
        "title": "《马格里布行政一体敕令》",
        "title_orig": "Erlass über die Verwaltungseinheit des Maghreb",
        "author": "伊比利亚王国", "lang": "伊比利亚-奥克语",
        "context": "S0：伊比利亚统治北非西部，长期基督教化与欧洲化；"
                   "S2：北非西部「没有特殊宪制地位」，与半岛同属一个国家行政体系；"
                   "撒哈拉以北西部划入欧洲。",
        "body": """<p class="doc-preamble">伊比利亚王国敕令。</p>

<h4>第一条</h4>
<p>马格里布诸地，自本令施行之日起，与半岛同属一国行政体系。不设总督府，不设特殊宪制地位。</p>

<h4>第二条</h4>
<p>诸地分为若干省，与半岛诸省同级。省官由中央任命，任期与半岛同。</p>

<h4>第三条</h4>
<p>诸地居民为本国臣民，非属地之民。得入本国学校、任本国官职。</p>

<h4>第四条</h4>
<p>教会于此设堂区，行基督教化之教。旧有清真寺或改为主教座堂，或拆除另建。</p>

<h4>第五条</h4>
<p>撒哈拉以南之地，不在本令范围。此地为界，非为殖民地之界，乃文明之分界。</p>

<p class="doc-seal">〔钤印：伊比利亚王国御玺〕</p>""",
        "significance": "把 S2「北非与半岛同属一个国家行政体系、无特殊宪制地位」"
                        "与「撒哈拉承担文明分界功能」写成行政敕令，"
                        "并明确这不是殖民地体制。",
        "src": ["S0", "S2"],
    },
    {
        "id": "DOC_NORDSTADT_RAILWAY", "kind": "文献·工程纪要", "year": 1840,
        "year_text": "19世纪", "place": "约克", "place_id": "P_YORK",
        "title": "《北方铁路工程纪要》",
        "title_orig": "Report on the Northern Railway Works",
        "author": "不列颠北方铁路公司", "lang": "英语",
        "context": "S3：不列颠为海洋商业帝国，依靠工业、金融、海军残余与语言文化网络；"
                   "北方州首府约克。",
        "body": """<p class="doc-preamble">Report to the Directors, Northern Railway Company.</p>

<h4>I. Purpose</h4>
<p>The line connects the coalfields of the north with the port of Hull and the yards at Newcastle. Its object is the carriage of coal and iron to the sea.</p>

<h4>II. Labour</h4>
<p>Navvies are engaged from the northern counties. Wages are paid weekly. The company notes that the men have no combination, and that any such combination would be unlawful.</p>

<h4>III. Land</h4>
<p>All wayleave was obtained by Act. No compensation was resisted. The landed interest was consulted at every stage, being represented in the Lords.</p>

<h4>IV. Remark</h4>
<p>The company observes that the same works upon the Continent are executed under the direction of boards answerable to ministers, whereas here they answer to proprietors. This the directors regard as an advantage.</p>

<p class="doc-seal">〔Seal: Northern Railway Company〕</p>""",
        "significance": "呈现战前不列颠「土地利益在议会、资本在业主」的运行方式，"
                        "并让纪要自己指出与大陆的制度差异（董事会 vs 部会），"
                        "反衬 S3「跨阶层议价集团无法形成」这一判断的另一面。",
        "src": ["S3"],
    },
    {
        "id": "DOC_FRANKEN_ORIENTAL_INSTITUTE", "kind": "文献·章程", "year": 1750,
        "year_text": "18世纪", "place": "劳格登", "place_id": "P_LAUGDEN",
        "title": "《劳格登东方语言与商路研究所章程》",
        "title_orig": "Statut des Laugdener Instituts für orientalische Sprachen und Handelswege",
        "author": "劳格登大学与马西利恩商会合办", "lang": "法兰克语（学术语域）",
        "context": "S0：劳格登大学以医学、药学、地理学、东西方贸易、东方语言著称；"
                   "S1：法兰克拥有地中海传统、北非与黎凡特传统影响、帕里斯的东方学传统。",
        "body": """<p class="doc-preamble">劳格登。大学与商会合办之研究所。</p>

<h4>第一条　宗旨</h4>
<p>本院研究东方之语言、商路、货品与律例，以供本国商民之用。</p>

<h4>第二条　语种</h4>
<p>设阿拉伯语、波斯语、突厥语、叙利亚诸语四席。学生须择二种，习满五年。</p>

<h4>第三条　档案</h4>
<p>本院汇集商路文书、领事记录、传教档案三类。凡商民携回之契、账、图、札，本院愿以副本交换原件之保存。</p>

<h4>第四条　派出</h4>
<p>每年派学生二人，随商队赴黎凡特或北非，居留不少于一年，习语兼习俗。</p>

<h4>第五条　与帕里斯</h4>
<p>本院与帕里斯王家学院分工：彼治神学、教会法与史，本院治语言、商路与地。</p>

<p class="doc-seal">〔钤记：劳格登大学、马西利恩商会〕</p>""",
        "significance": "把法兰克东方学的**制度形态**（语种、档案、选派、与帕里斯的分工）写成章程，"
                        "落实 S1 所称「法兰克成为欧洲研究东方世界的重要文明」。",
        "src": ["S0", "S1"],
    },
    {
        "id": "DOC_BRITAIN_EXILES_1789", "kind": "文献·回忆录", "year": 1795,
        "year_text": "1795年", "place": "伦敦", "place_id": "P_LONDON",
        "title": "《一位诺曼流亡者的回忆》",
        "title_orig": "Memoirs of a Norman Exile", "author": "法兰克流亡文人（架空人物）",
        "author_id": None, "lang": "盎格鲁-法兰西语（宫廷语域）",
        "context": "S3：1272 年诺曼-法兰西精英退回不列颠；此后叠加 1648 维也纳和约后、"
                   "1789 伊比利亚革命后两次流亡波次，英伦作为罗曼-法兰西高文化"
                   "唯一活体保存地的地位不断加固。",
        "body": """<p class="doc-preamble">London, my third winter here.</p>

<p>My grandfather came to this island in the troubles that followed the fall of the Capetians — or so our family says. He spoke the old tongue of the court at Paris; his children spoke it in this island's courts; I write it to you now.</p>

<p>Twice since then our people have come over: after the peace of Vienna, and now, after the Iberian revolution.</p>

<p>What I marvel at is this: at Paris the tongue is dead, and on the Continent there is no one left who speaks it as we do. We are the only ones who keep it. My son will write it better than he speaks it, and his son after him will write only.</p>

<p>So we are not exiles returning. We are the place where a language went when its own country was taken from it.</p>

<p class="doc-seal">〔无钤印，私稿〕</p>""",
        "significance": "以流亡者回忆录的形式把 S3 所述三次流亡波次串成一条线，"
                        "并给出关键判断：「我们不是归来的流亡者，我们是语言被夺走国家之后所去的地方。」",
        "src": ["S3"],
    },
    {
        "id": "DOC_SIBERIA_SHAMAN", "kind": "文献·口述记录", "year": 1700,
        "year_text": "17—18世纪", "place": "西伯利亚（未具名）", "place_id": None,
        "title": "《西伯利亚萨满口述记录》",
        "title_orig": "Aufzeichnung sibirischer Schamanenüberlieferung",
        "author": "罗斯兀鲁思边地录事官", "lang": "东斯拉夫语（兼录通古斯语词）",
        "context": "S1：西伯利亚形成「萨满传统 + 长生天传统」；"
                   "欧亚文明梯度为：蒙古高原 → 西伯利亚 → 中亚佛教 → 金帐 → 罗斯兀鲁思 → 东欧边缘。",
        "body": """<p class="doc-preamble">录事官记录。受录者：██部落萨满。</p>

<p>问：你们拜什么？</p>
<p>答：拜山、拜河、拜祖先。天在上，最大。</p>

<p>问：你们也拜佛？</p>
<p>答：南边的部族拜佛，他们的僧人住大帐。我们这里没有和尚，但长者说佛也是天的一种说法。</p>

<p>问：莫斯科来的官要你们改信？</p>
<p>答：他们不管。他们只收皮子，问路，修驿站。他们的神父也来过一次，后来不来了——太远。</p>

<p>问：你们与南边的蒙古人通婚吗？</p>
<p>答：通。南边来的商人说蒙古话，我们有些人会说。往西去，说的话越来越像莫斯科。</p>

<p class="doc-seal">〔钤记：边地录事官〕</p>""",
        "significance": "以口述记录形式呈现西伯利亚「萨满 + 长生天」的宗教结构，"
                        "以及罗斯兀鲁思向东扩张采取「只收皮子、修驿站、不问信仰」的实际策略——"
                        "这正是蒙古遗产的延续方式。",
        "src": ["S1", "S4"],
    },
    {
        "id": "DOC_VENICE_AIX_1820", "kind": "文献·旅行记", "year": 1820,
        "year_text": "19世纪", "place": "普罗旺斯", "place_id": "P_MASSILIEN",
        "title": "《南法兰克旅行记》",
        "title_orig": "Reise durch das südliche Franken", "author": "德意志旅行者（架空人物）",
        "author_id": None, "lang": "共同体德语",
        "context": "S0/S2：南部奥克省；奥克语与伊比利亚半岛语言共享词汇语法；"
                   "奥克人认同「北伊比利亚人」或「奥克-伊比利亚人」；"
                   "马西利恩为法兰克—德意志文化支点。",
        "body": """<p class="doc-preamble">旅行记。马西利恩。</p>

<p>从劳格登南下，地势渐宽，日光渐强。此地居民的话，与北方大不相同：同是日耳曼语的骨架，却多了许多罗曼语的音与词。他们管这叫奥克语。</p>

<p>奇怪的是，往西越过山口，那边伊比利亚人说的话，与此地的奥克语几乎可以相通。而向北，帕里斯的宫廷语言他们听得懂，却说得生硬。</p>

<p>城里有人对我说：我们是北伊比利亚人。也有人说：我们是奥克-伊比利亚人。</p>

<p>马西利恩港口的商人与北意大利来往甚密。教堂是天主教的，与德意志那边的新教村庄相邻而不同。</p>

<p>我走的时候想：这块地不属于任何一方。它是一条河的南岸。</p>""",
        "significance": "以旅行者视角印证 S0 所记「奥克语与伊比利亚半岛语言共享词汇语法」"
                        "与「奥克人认同北伊比利亚人或奥克-伊比利亚人」，"
                        "并呼应 S1「奥克地区不是铁板一块」的修正。",
        "src": ["S0", "S1", "S2"],
    },
    {
        "id": "DOC_SPANISH_MISSION", "kind": "文献·传教报告", "year": 1540,
        "year_text": "16世纪", "place": "托莱多（推定）", "place_id": "P_TOLEDO",
        "title": "《北非传教年度报告》",
        "title_orig": "Jahresbericht der afrikanischen Mission",
        "author": "伊比利亚天主教传教会", "lang": "伊比利亚-奥克语",
        "context": "S0：伊比利亚南下北非驱逐穆斯林，长期统治并基督教化、欧洲化该地区；"
                   "S2：该地无特殊宪制地位，与半岛同属一个国家行政体系。",
        "body": """<p class="doc-preamble">呈伊比利亚王国宗教会议。</p>

<h4>一　本年度堂区</h4>
<p>新设堂区十四处，改建清真寺为主教座堂三处，另建五处。</p>

<h4>二　语言</h4>
<p>本地居民习用柏柏尔语与阿拉伯语。本会以本国语言传教，兼用土语。第二代已多能通本国语言。</p>

<h4>三　学校</h4>
<p>设堂区学校九所，教读、写、算与教理。学生中本地居民之子占七成。</p>

<h4>四　关于身份</h4>
<p>本会提请宗教会议留意一事：本地居民不是属地之民，乃本国臣民。故传教之法宜与本国同，不宜另立一套「殖民地教规」。此举于教理为当，于国策亦为当。</p>

<p class="doc-seal">〔钤记：伊比利亚天主教传教会〕</p>""",
        "significance": "以传教报告落实「北非为本土而非殖民地」这一设定的**宗教行政层面**，"
                        "并说明基督教化如何在两代人之内改变语言使用。",
        "src": ["S0", "S2"],
    },
    {
        "id": "DOC_ALPINE_SANCTUARY", "kind": "文献·寺院章程", "year": 1400,
        "year_text": "14—15世纪", "place": "布伦纳", "place_id": "P_BRENNER",
        "title": "《布伦纳山口接待章程》",
        "title_orig": "Herbergsordnung der Brennerklause",
        "author": "山口修道院", "lang": "高地德语（兼用拉丁语）",
        "context": "S0：阿尔卑斯山口修道院与山间礼拜堂列为「跨宗教」圣地。",
        "body": """<p class="doc-preamble">布伦纳山口之修道院，订接待章程。</p>

<h4>一</h4>
<p>凡过关者，无论其为天主教、路德宗、加尔文宗，皆得投宿。不问其教，不问其国。</p>

<h4>二</h4>
<p>礼拜堂分时用之。晨为旧礼，午后为新礼，各不相扰。</p>

<h4>三</h4>
<p>雪封之时，救济不问教派。冻毙于道者，无论何教，皆葬于本院之侧。</p>

<h4>四</h4>
<p>本院不藏兵，不休兵，不留逃兵。过客携械者，寄于门房。</p>

<p class="doc-seal">〔钤记：布伦纳山口修道院〕</p>""",
        "significance": "把「山口为跨宗教圣地」这一设定写成具体的接待章程，"
                        "呈现宗教分裂时代里中立空间的实际运作方式。",
        "src": ["S0"],
    },
    {
        "id": "DOC_MILAN_DESIGN", "kind": "文献·教学纲要", "year": 1900,
        "year_text": "1900年前后", "place": "米兰", "place_id": "P_MAILAND",
        "title": "《米兰理工机械美学课程纲要》",
        "title_orig": "Lehrplan der mechanischen Ästhetik am Polytechnikum Mailand",
        "author": "米兰理工大学与伦巴底美学院", "lang": "共同体德语与意大利语并行",
        "context": "S0：米兰理工大学与伦巴底美学院，涵盖建筑工程、机械美学、工业设计、"
                   "歌剧音乐理论；波河-阿尔卑斯工业带以纺织、金融、精密仪器为主。",
        "body": """<p class="doc-preamble">米兰。两校合设课程。</p>

<h4>第一年　材料之性</h4>
<p>钢、铜、木、石之受力与外观。以本带旧织机为范本，拆解测绘。</p>

<h4>第二年　机与饰</h4>
<p>机械之功能与装饰之关系。论点：饰非多余，饰为机械之自述——它说明此机为何物、属何人。</p>

<h4>第三年　声与器</h4>
<p>歌剧音乐理论。以斯卡拉歌剧院之乐池与机关为实例。德意志南部的歌剧取材圣经或德意志历史，故舞台机械之设计与剧情相连。</p>

<h4>第四年　厂与城</h4>
<p>厂房、工人住宅与城市之关系。以本带三城（米兰、都灵、威尼斯）为例。</p>

<p class="doc-seal">〔钤记：米兰理工大学、伦巴底美学院〕</p>""",
        "significance": "把 S0 所记「机械美学」这一概念落实为可授的课程结构，"
                        "并说明南德新教「歌剧取材圣经或德意志历史」如何影响舞台设计。",
        "src": ["S0"],
    },
]

DIARIES = [
    {
        "id": "DIA_JOURNALIST_1960", "kind": "日记", "year": 1960,
        "year_text": "1960年", "place": "维也纳", "place_id": "P_VIENNA",
        "title": "维也纳记者日记·多极世界的第一年",
        "author": "维也纳记者（架空人物）", "author_id": None,
        "lang": "共同体德语",
        "context": "1960 年前后多极均势格局成局；S1 母表称 1960 年德意志为超级强国、"
                   "法兰克与伊比利亚为区域强国、英美为强国。",
        "body": """<p class="doc-preamble">维也纳。编辑部。</p>

<p>总编今日定了新栏目：六极。德意志、法兰克、伊比利亚、罗斯兀鲁思、英美、以及英联邦。</p>

<p>我写第一篇时卡住了。因为「极」这个词是用不上的。我们不是两极，也不是一超多强——我们是六个各自有自己账本的国家，互相牵制，谁也不能把谁怎么样。</p>

<p>没有阵营，没有铁幕，没有谁在等着谁垮台。这在记者看来是坏消息：没有大新闻。在公民看来是好消息。</p>

<p>今天伊比利亚宣布第五共和国成立。同一周，非洲那边还有事没完。我把它写在第三版——不是因为它不重要，是因为我们这边已经习惯了：远处的事，慢慢地也就成了邻家的事。</p>""",
        "significance": "以记者视角呈现「无冷战、多极均势」这一核心设定，"
                        "并点出这一格局对新闻业与公民生活的不同含义。",
        "src": ["S0", "S1"],
    },
    {
        "id": "DIA_MUSEUM_CURATOR", "kind": "日记", "year": 1990,
        "year_text": "1990年前后", "place": "法兰克福", "place_id": "P_FRANKFURT",
        "title": "博物馆策展人日记·双冠旗的展陈",
        "author": "法兰克福帝国议会档案馆策展人（架空人物）", "author_id": None,
        "lang": "共同体德语",
        "context": "双王冠旗（1356—1871）现存法兰克福帝国议会档案馆与帕里斯王家武库两幅；"
                   "1871 年双王冠分离后废止。",
        "body": """<p class="doc-preamble">法兰克福。档案馆展陈室。</p>

<p>今日挂旗。这面双冠旗一米八见方，左半深蓝底金鹰，右半酒红底银狮，中缝一只帝国之鹰统摄二者。一百三十五年间，它挂在帝国议会正中。</p>

<p>我把它挂在两个展柜之间：左边是《法兰克福宪章》的御玺，右边是 1871 年罗马加冕的诏书。中间是这面旗。</p>

<p>观众走过来，看到的是：一个制度，运行了五百多年，然后停了。</p>

<p>有个中学生问我：这算成功还是失败？我答：它让两个民族共戴一个皇帝五百年而没有互相吞并。这在这个大陆上，算是成功。它最后还是没有变成一个国家。这算是失败。两句话都对。</p>""",
        "significance": "以展陈设计呈现「双王冠制度运行五百年后停止」这一历史判断，"
                        "并用「两句话都对」给出不简化的评价。",
        "src": ["S0", "S1"],
    },
]

LETTERS = [
    {
        "id": "LET_SALADIN_FRANKISH", "kind": "书信", "year": 1192,
        "year_text": "12世纪", "place": "大马士革", "place_id": "P_DAMASCUS",
        "title": "萨拉丁致法兰西罗曼王国书",
        "author": "萨拉丁", "author_id": "PE_SALADIN",
        "recipient": "法兰西罗曼王国宫廷", "recipient_id": "C_FRANKISH_ROMANCE",
        "lang": "阿拉伯语（拉丁语译本）",
        "context": "十字军东征（11—13 世纪）的发动者是法兰西罗曼王国（1270 年前大陆北部的"
                   "罗曼语政治体）；1187 年萨拉丁收复耶路撒冷。",
        "body": """<p class="doc-preamble">大马士革，致罗马语法兰克人的宫廷。</p>

<p>你们从海上来，说那座城是你们的圣城。我们知道它对你们是圣的。它对我们也一样。</p>

<p>我今日写这封信，不是求和，是说明一件事：你们若继续来，我们会继续挡。不是因为恨，是因为那座城在我们的土地上。</p>

<p>你们的国王们说，是上帝要他们来。我听过这个说法。我也听过你们的商人在阿卡与提尔的市场上跟我的人讲价，讲得很仔细。</p>

<p>所以我说：圣战与生意，你们自己分得清。我也分得清。</p>

<p>若你们愿意让朝圣者自由来往，我们可以谈。城不能给，路可以给。</p>

<p class="doc-seal">〔钤印：萨拉丁〕</p>""",
        "significance": "从穆斯林一方回应十字军东征，并把发动者准确称为「罗马语法兰克人」（法兰西罗曼王国），"
                        "同时区分「圣战与生意」——与法兰克后世的东方学传统形成呼应。",
        "src": ["S1"],
    },
    {
        "id": "LET_DUNHUANG_KUCHA", "kind": "书信", "year": 900,
        "year_text": "9—10世纪", "place": "敦煌", "place_id": "P_DUNHUANG",
        "title": "敦煌僧团致龟兹僧团书",
        "author": "敦煌僧团", "author_id": "O_DUNHUANG_CAVES",
        "recipient": "龟兹僧团", "recipient_id": "O_KUCHA_CAVES",
        "lang": "汉语（兼录吐火罗语词）",
        "context": "S1：西域佛教文明带长期存在；敦煌继续作为东方佛教门户；"
                   "印度佛教 → 犍陀罗 → 西域 → 中亚 → 中国这条链条比现实更强。",
        "body": """<p class="doc-preamble">敦煌致龟兹。</p>

<p>贵寺所寄经本三种已收到。其中《十诵》写本用吐火罗字，本寺已有汉译本，两本对校，得异文四十余处，谨录呈回。</p>

<p>西边来的商队说，河中那边的佛寺也还在，僧人用波斯文抄经。他们与我们说不同的字，读同一类经，走同一条路。</p>

<p>本寺以为，此事比任何一位王的胜负都要紧。诸国兴亡不过百年，经卷若散，千年不可复得。</p>

<p>故本寺请与贵寺约定：凡一方得经，抄副赠另一方；凡一方遇难，经卷先西送或东送，再论人。</p>

<p class="doc-seal">〔钤记：敦煌僧团〕</p>""",
        "significance": "以两地僧团的通信呈现西域佛教带的知识网络，"
                        "并落实「敦煌继续作为东方佛教门户」这一设定及其实际运作机制。",
        "src": ["S1"],
    },
    {
        "id": "LET_VOLTA_MILAN", "kind": "书信", "year": 1800,
        "year_text": "1800年前后", "place": "米兰", "place_id": "P_MAILAND",
        "title": "伦巴底学者致哥廷根学者书·论电",
        "author": "伦巴底自然哲学家（架空人物）", "author_id": None,
        "recipient": "哥廷根大学学者", "recipient_id": "O_GOETTINGEN_UNI",
        "lang": "共同体德语与意大利语并行",
        "context": "S0：哥廷根大学以数学、天文学、实验物理著称；"
                   "米兰理工大学以建筑工程、机械美学著称；波河-阿尔卑斯工业带以精密仪器为主。",
        "body": """<p class="doc-preamble">米兰致哥廷根。</p>

<p>先生所问之电堆实验，本处已重复三次。结论与先生同：电流之强弱与两金属之种类成一定之比。</p>

<p>本处之利在于工坊。此地做精密仪器者多，细丝、薄片、纯锌，皆可定制。先生若要实验，本处可为先生做一套器具，一月可成，托商队送阿尔卑斯以北。</p>

<p>本处之不利在于数学。此地学者长于机与工，短于算。故本处拟请先生推荐一名算学者来此讲席一年，本处则派一人赴哥廷根习天文测算。</p>

<p>此非私谊，是分工。我们这个大陆上的学问，本来就是这样一城补一城的。</p>""",
        "significance": "呈现德意志世界内部的学术分工（南方的工艺＋北方的数学），"
                        "并说明「人才留在中欧」这一设定在学术制度上的运作方式。",
        "src": ["S0", "S1"],
    },
]

SPEECHES = [
    {
        "id": "SPEECH_MAGHREB_BISHOP", "kind": "演讲", "year": 1600,
        "year_text": "17世纪", "place": "马拉喀什", "place_id": "P_MARRAKECH",
        "title": "马格里布主教就职演说",
        "author": "马格里布首任主教（架空人物）", "author_id": None,
        "lang": "伊比利亚-奥克语",
        "context": "S0：伊比利亚南下北非驱逐穆斯林，长期统治并基督教化、欧洲化；"
                   "S2：北非西部无特殊宪制地位，与半岛同属一个国家行政体系。",
        "body": """<p class="doc-preamble">马拉喀什。主教座堂（原清真寺）。</p>

<p>诸位看到的这座建筑，去年还是另一群人的礼拜之所。我们把它改了过来。此事我不打算美化：这靠的是征服，不是辩论。</p>

<p>但我要说清我们此后要做什么。我们把这里当作本国的一省，不是当作属地。这里的居民是本国的臣民，不是被征服之民。他们进我们的学校，做我们的官，说我们的语言——到他们的孙辈，会说三种话：家里的话、城里的话、本国的话。</p>

<p>撒哈拉以南，我们不越界。那道沙，是文明的界线。我们在这里，是欧洲的南端，不是非洲的北端。</p>""",
        "significance": "以主教就职演说明确「北非为本土、撒哈拉为文明界线」这两条 S2 设定，"
                        "同时不回避基督教化的征服性质。",
        "src": ["S0", "S2"],
    },
    {
        "id": "SPEECH_SWISS_BRIDGE", "kind": "演讲", "year": 1955,
        "year_text": "1955年前后", "place": "苏黎世", "place_id": "P_ZUERICH",
        "title": "苏黎世联邦理工学院百年演说·论中立者能做之事",
        "author": "苏黎世联邦理工学院院长（架空人物）", "author_id": "O_ZURICH_ETH",
        "lang": "高地德语（瑞士方言色彩）",
        "context": "S0：瑞士为永久联邦、永久中立，在泛德意志语言共同体中发挥桥梁作用；"
                   "S0 另记一战流散知识分子迁往瑞士，日内瓦、苏黎世、巴塞尔成为流亡学术中心。",
        "body": """<p class="doc-preamble">苏黎世。联邦理工学院百年。</p>

<p>我们是永久中立国。有客人问：中立的意思是不是什么都不做？</p>

<p>我给一个具体的回答。三十年前，中欧战败，维也纳的物理学家、布拉格的语言学家、法兰克的法学家，都往这边来。我们没有参战，我们收留了他们。</p>

<p>再往前，宗教战争的时候，我们的山口让两边的人过。我们的出版社印两边的书。我们的学者用同一种标准语与法兰克、德意志通信——那是三国教育部长和学者一起定的正字法。</p>

<p>所以中立不是不做，是做得不一样。别人筑墙的时候我们开门，别人划线的时候我们通信。</p>

<p>这个世界有六极。六极之间需要一个能收信、能存稿、能让两边的人同时坐下来喝茶的地方。那是我们的位置。</p>""",
        "significance": "把 S0 所记瑞士「永久中立 + 语言共同体桥梁 + 流亡学术中心」三重角色"
                        "整合为一段自我说明，并给出「中立不是不做，是做得不一样」的定义。",
        "src": ["S0"],
    },
]
