# -*- coding: utf-8 -*-
"""
文献扩充层（第二批）
======================
把仿真文献从 41 篇扩充到 100 篇（本文件提供 59 篇）。
全部锚定 S0–S4 已确立的设定，形制符合各国语文。
"""
from collections import OrderedDict

# ============================================================
# A. 历史文献仿真（诏令 / 条约 / 纪要 / 章程 / 报告）
# ============================================================
DOCUMENTS = [
    {
        "id": "DOC_FRANKFURT_OVERTURE", "kind": "文献·会议纪要", "year": 1356,
        "year_text": "1356年（会议首月）", "place": "法兰克福", "place_id": "P_FRANKFURT",
        "title": "《法兰克福会议开幕纪要》",
        "title_orig": "Eröffnungsprotokoll des Frankfurter Konvents",
        "author": "帝国议会书记处", "lang": "拉丁语与高地德语并行",
        "context": "阿尔布雷希特二世年老无嗣，仅有一女。法兰克贵族要求女婿继承法兰克王位，"
                   "德意志选侯坚持选举德意志诸侯为皇帝。会议历时八个月。",
        "body": """<p class="doc-preamble">会议首月纪要。书记：███。</p>

<h4>出席者</h4>
<p>法兰克贵族十七人、德意志选侯代表六人（波西米亚国王亲至）、教皇使节一人、瑞士联邦代表二人。</p>

<h4>第一日</h4>
<p>皇帝陛下亲临，言其年老无嗣，仅有一女。法兰克贵族即席请求：请以陛下之婿承继法兰克王位。选侯代表当即异议：德意志人之国王，须由选侯于法兰克福选举而生。</p>

<h4>第七日</h4>
<p>教皇使节发言。其意不在裁定二者之是非，而在保住圣座对皇帝之加冕权。使节言：若两冠合一而无圣座之认可，则皇帝之称将失其教义根基。</p>

<h4>第十九日</h4>
<p>瑞士代表请求确认其自治地位。皇帝允诺列入条款。</p>

<p class="doc-seal">〔钤记：帝国议会书记处〕</p>""",
        "significance": "呈现《法兰克福宪章》八个月谈判的开局格局：三方的诉求与教皇的介入动机。",
        "src": ["S0", "S1"],
    },
    {
        "id": "DOC_OCCITAN_PROCLAMATION", "kind": "文献·公告", "year": 1972,
        "year_text": "1972年", "place": "帕里斯", "place_id": "P_PARIS",
        "title": "《奥克正常化公告》",
        "title_orig": "Bekanntmachung zur Okzitanischen Normalisierung",
        "author": "法兰克中央政府", "lang": "法兰克语",
        "context": "1945 年法兰克获取奥克地区并设南部奥克省（临时性省级中间管理层）。"
                   "1972—1978 年帕里斯推动「奥克正常化」，1975 为关键节点。",
        "body": """<p class="doc-preamble">法兰克中央政府公告。</p>

<p>自本法施行之日起，南部奥克省之临时建制将分阶段废止。朗格多克、普罗旺斯、多菲内、奥克海岸、罗讷河口诸州，一律升为普通联邦州，与本土诸州同权。</p>

<p>奥克语得为州级官方语言。州内实行双语教育。奥克文化机构由国家支持。</p>

<p>惟法兰克语仍为联邦层面唯一之官方语言。外交、国防、货币、海关与最高司法，仍由帕里斯掌握。</p>

<p>本法所予者，为文化之承认与普通联邦州之地位，非民族自治领之地位。此点务使各地周知。</p>

<p class="doc-seal">〔钤印：法兰克中央政府〕</p>""",
        "significance": "把「先控制、再正常化」的整合策略写成阶段性的公开公告，"
                        "明确政策的边界：文化承认而非民族自治。",
        "src": ["S2"],
    },
    {
        "id": "DOC_LOWLAND_INDEPENDENCE", "kind": "文献·独立宣言", "year": 1625,
        "year_text": "1625年", "place": "阿姆斯特丹", "place_id": "P_AMSTERDAM",
        "title": "《低地联合省独立宣言》",
        "title_orig": "Plakkaat van Verlatinghe der Verenigde Provinciën",
        "author": "低地联合省议会", "lang": "低地德语（荷兰语域）",
        "context": "宗教战争丹麦-低地阶段（1625—1629）：低地加尔文宗城市介入，"
                   "低地联合省宣布独立；皇帝联合法兰克镇压，低地城市凭海军和金融坚持抵抗。",
        "body": """<p class="doc-preamble">Wy, Staten der Verenigde Provinciën, doen kondt allen luden.</p>

<p>De keyser unde de koninc der Franken willen unsen gelove nemen unde unsen handel breken. Wy en willen des nicht.</p>

<p>Onse stede liggen an der see. Onse schepe varen to allen landen. Onse banken lenen den vorsten, de uns nu bekriegen wille. Darumme: wy bliven by unsem gelove unde by unser vrijheit.</p>

<p>Wy verklaren: de Vereenigde Provinciën sünd ene vrije republike, na dem rechte der naturen unde der reden.</p>

<p class="doc-seal">〔钤印：低地联合省议会〕</p>""",
        "significance": "以低地德语（荷兰语域）写成，落实 S0「荷兰语被视为低地德语一部分」的设定；"
                        "并说明低地独立的财政与海军基础。",
        "src": ["S0"],
    },
    {
        "id": "DOC_SWISS_CHARTER", "kind": "文献·自治确认书", "year": 1356,
        "year_text": "1356年", "place": "苏黎世", "place_id": "P_ZUERICH",
        "title": "《瑞士自治确认书》",
        "title_orig": "Bestaetigung der eidgenössischen Freiheiten",
        "author": "瑞士联邦各州代表", "lang": "高地德语（瑞士方言色彩）",
        "context": "《法兰克福宪章》确认瑞士为帝国内「特殊自治体」，不承担帝国税和兵役；"
                   "各州可保留共和制度，但对外不得与帝国敌人结盟；哈布斯堡放弃对瑞士祖地的宗主权要求。",
        "body": """<p class="doc-preamble">Wir, die eidgenossen, tuon kund allen, die disen brief ansehent.</p>

<p>Wir sin des riches besunder lüte, unde doch niht des riches knehte. Wir gebent dem riche keinen zins unde dienent im mit keinem hervart.</p>

<p>Wir behaltent unsere frien stette unde unsere lantgerichte unde unsere ratthuser.</p>

<p>Aber wir verbindent uns: wir enwellent uns mit des riches vienden verbinden, noch trost noch geleite geben.</p>

<p>Und der herzoge von Oesterrich verzichet aller ansprüche an unsere alte lant.</p>

<p class="doc-seal">〔钤记：瑞士联邦各州印信〕</p>""",
        "significance": "以瑞士德语方言写成，呈现「特殊自治体」这一制度安排的双向约束："
                        "免帝国税与兵役，但不得与帝国敌人结盟。",
        "src": ["S0"],
    },
    {
        "id": "DOC_HANSA_PRIVILEGE", "kind": "文献·特许状", "year": 1356,
        "year_text": "1356年后", "place": "汉堡", "place_id": "P_HAMBURG",
        "title": "《自由汉萨城市特许状》",
        "title_orig": "Privilegium der freien Hansestädte",
        "author": "哈布斯堡皇帝", "lang": "低地德语",
        "context": "《法兰克福宪章》设立帝国议会，由法兰克贵族、德意志诸侯、自由汉萨城市代表组成。"
                   "自由汉萨城市在德意志联邦中为城市州。",
        "body": """<p class="doc-preamble">Wy, keyser, don kondt.</p>

<p>Den steden Hamborch, Bremen unde Amsterdam, unde allen anderen steden der Hanse, geven wy wet unde macht unde enen sit in deme rikes rade, nebene den vorsten unde nebene deme adelrikke.</p>

<p>Se moghen selven setten ere tollen, ere munte, ere rechtes unde ere schepe mit eren segelen.</p>

<p>Und se draghen tosamene en gemeinsam seghel, dar mede se ere vedernisse bezegelen.</p>

<p class="doc-seal">〔钤印：皇帝御玺、汉萨三城联合印记〕</p>""",
        "significance": "落实「自由汉萨城市代表进入帝国议会」与三城城市州地位的法律来源。",
        "src": ["S0"],
    },
    {
        "id": "DOC_STANDARD_ORTHOGRAPHY", "kind": "文献·规范", "year": 1700,
        "year_text": "18世纪（推定）", "place": "法兰克福", "place_id": "P_FRANKFURT",
        "title": "《共同正字法条文》",
        "title_orig": "Satzung der gemeindeutschen Rechtschreibung",
        "author": "泛德意志语言会议", "lang": "共同体德语",
        "context": "三国推行统一正字法，将高地德语（含瑞士）、法兰克德语、低地德语（含荷兰）融合。",
        "body": """<p class="doc-preamble">泛德意志语言会议议定条文。</p>

<h4>第一条　词源优先</h4>
<p>拼写依词源，不依当下之音。凡词形之古者可考者，存其古形。</p>

<h4>第二条　跨方言折中</h4>
<p>高地、法兰克、低地三者，择其可通者。动词与名词之屈折，取三者共有之式。</p>

<h4>第三条　词汇层融合</h4>
<p>三系词汇并举。凡一物而有二名者，视其义明者取之，义晦者列于注。</p>

<h4>第四条　语法保守</h4>
<p>存古之格、性、数。凡方言已失而文书可考者，复之。</p>

<h4>第五条　拼写标注发音</h4>
<p>正字与读音并存，不强求一致。方言仍存于家庭与乡里，不入废止之列。</p>

<p class="doc-seal">〔钤记：泛德意志语言会议〕</p>""",
        "significance": "把《共同体德语》的五条原则写成正式条文，可供各邦学校直接援引。",
        "src": ["S0"],
    },
    {
        "id": "DOC_TRIEST_STATUTE", "kind": "文献·共管章程", "year": 1919,
        "year_text": "1919年（推定）", "place": "的里雅斯特", "place_id": "P_TRIEST",
        "title": "《的里雅斯特国际共管章程》",
        "title_orig": "Statut der internationalen Verwaltung von Triest",
        "author": "战胜方各国代表", "lang": "共同体德语、伊比利亚-奥克语、英语并行",
        "context": "一战后奥地利德意志被迫接受的里雅斯特国际共管；北意大利设非军事区。",
        "body": """<p class="doc-preamble">兹以战胜各国之名义，订立的里雅斯特共管章程。</p>

<h4>第一条</h4>
<p>的里雅斯特及其港区，设国际共管，由签约各国派员组成共管委员会。</p>

<h4>第二条</h4>
<p>港口对各国商船开放，通行税统一，不因船旗国而异。</p>

<h4>第三条</h4>
<p>北意大利地区设非军事区，双方军队不得进入。</p>

<h4>第四条</h4>
<p>奥地利德意志在波兰地区之占领，须即行释放。</p>

<p class="doc-seal">〔钤印：共管委员会、战胜各国全权代表〕</p>""",
        "significance": "把 S0 所列一战对奥地利德意志的三项处罚（释放波兰、北意非军事化、的里雅斯特共管）"
                        "整合为一份可援引的章程。",
        "src": ["S0", "S1"],
    },
    {
        "id": "DOC_VERSAILLES_SYSTEM", "kind": "文献·和约体系", "year": 1919,
        "year_text": "1919年", "place": "（未具名）", "place_id": None,
        "title": "《战后和约体系要纲》",
        "title_orig": "Grundzüge des Nachkriegsvertragssystems",
        "author": "战胜方各国", "lang": "共同体德语译本",
        "context": "S0 地图工程列有「1919凡尔赛体系」节点。一战后中欧战败，"
                   "奥地利德意志受更严厉处罚，法兰克建立不完善的共和国。",
        "body": """<p class="doc-preamble">战后和约体系要纲。中欧译本。</p>

<h4>甲、对奥地利德意志</h4>
<p>释放所占领之波兰地区。北意大利设非军事区。的里雅斯特国际共管。军队限额。赔款待议。君主政体废止，改为共和国。</p>

<h4>乙、对法兰克</h4>
<p>哈布斯堡失去统治地位。法兰克改为共和国——然其贵族仍居政府与军队之要职。</p>

<h4>丙、通用条款</h4>
<p>本体系不设超国家执行机构。签约各国各自担保，无共同防务条款。</p>

<p class="doc-seal">〔钤印：战胜各国全权代表〕</p>""",
        "significance": "把一战后的中欧处置与「无共同防务条款」这一结构性缺陷并列写出，"
                        "为二十年后二战的重启埋下伏笔。",
        "src": ["S0", "S1"],
    },
    {
        "id": "DOC_GERMAN_FEDERAL_ACT", "kind": "文献·联邦法", "year": 1945,
        "year_text": "1945年", "place": "维也纳", "place_id": "P_VIENNA",
        "title": "《德意志联邦重建法》",
        "title_orig": "Gesetz über den Wiederaufbau des deutschen Bundes",
        "author": "德意志联邦共和国制宪会议", "lang": "共同体德语",
        "context": "二战后德意志取消所有不平等条约、收复波兰、建立统一联邦制民主共和国；"
                   "低地与北意大利重新并入。",
        "body": """<p class="doc-preamble">德意志联邦共和国制宪会议制定。</p>

<h4>第一条　国体</h4>
<p>本邦为联邦制民主共和国。主权在民，行使之权分属联邦与各邦。</p>

<h4>第二条　各邦之权</h4>
<p>各邦有宪法、议会、政府、法院。教育、文化、地方治安与州内交通归各邦。</p>

<h4>第三条　条约之地位</h4>
<p>一战以来强加于本国之一切不平等条约，自本法施行之日起失效。</p>

<h4>第四条　疆域</h4>
<p>波兰地区收复。低地与北意大利重新并入本联邦，为其邦。</p>

<h4>第五条　政教</h4>
<p>联邦不设国教。四大福音派教会并存，各邦得自行安排教会事务。</p>

<p class="doc-seal">〔钤印：德意志联邦共和国制宪会议〕</p>""",
        "significance": "把二战后德意志的条约取消、领土收复与联邦化重建整合为一部联邦法，"
                        "并明确「联邦不设国教」以对应四大派别并存。",
        "src": ["S0", "S1", "S2"],
    },
    {
        "id": "DOC_FRANKEN_RESTORATION", "kind": "文献·复辟诏书", "year": 1945,
        "year_text": "1945年", "place": "帕里斯", "place_id": "P_PARIS",
        "title": "《法兰克王政复辟诏书》",
        "title_orig": "Thronerhebungsurkunde der fränkischen Restauration",
        "author": "哈布斯堡王室与法兰克贵族院", "lang": "法兰克语",
        "context": "二战中哈布斯堡复辟，建立法兰克君主立宪共和国，统治奥克以外法兰克地区；"
                   "国王彻底成为礼仪性国家元首。",
        "body": """<p class="doc-preamble">哈布斯堡王室与法兰克贵族院共同颁行。</p>

<h4>第一条</h4>
<p>法兰克恢复君主政体，是为法兰克君主立宪共和国。国王为国家元首。</p>

<h4>第二条</h4>
<p>国王签署法律、任命最高法院法官、宣布特赦，于特殊时期得解散州议院。</p>

<h4>第三条</h4>
<p>国王不得否决联邦预算，不得单独宣战，不得任命或罢免总理。</p>

<h4>第四条</h4>
<p>国王不加入任何政党。王室保持政治中立。惟广义哈布斯堡家族之成员，得各依其志加入不同政党——王室与家族，自此分为二者。</p>

<h4>第五条</h4>
<p>1918 年至 1945 年之共和时期，载入国史，不为讳。</p>

<p class="doc-seal">〔钤印：国王御玺、法兰克贵族院〕</p>""",
        "significance": "把 S2 所记的宪制安排与「哈布斯堡王室 ≠ 整个哈布斯堡家族」这一关键区分"
                        "写成复辟诏书，并让第五条主动承认共和时期的存在。",
        "src": ["S0", "S1", "S2"],
    },
    {
        "id": "DOC_IBERIA_5REP_CONSTITUTION", "kind": "文献·宪法要纲", "year": 1960,
        "year_text": "1960年", "place": "托莱多（推定）", "place_id": "P_TOLEDO",
        "title": "《伊比利亚第五共和国宪法要纲》",
        "title_orig": "Grundzüge der Verfassung der Fünften Iberischen Republik",
        "author": "伊比利亚制宪议会", "lang": "伊比利亚-奥克语",
        "context": "第四共和国因 1954 年前后非洲殖民地危机覆灭；1960 年重建为第五共和国，"
                   "总统权力重新加强，形成「强国家 + 民主化」体制。",
        "body": """<p class="doc-preamble">伊比利亚制宪议会制定。</p>

<h4>第一条</h4>
<p>伊比利亚为不可分割之共和国。主权在民。</p>

<h4>第二条　总统</h4>
<p>总统由普选产生，任期七年。总统任命总理，主持内阁会议，得于紧急状态时行使特别权力，得解散议会。</p>

<h4>第三条　大区</h4>
<p>全国分为八个大区。大区之幅须大，其数须少。大区不得以传统民族或历史省份为界，其名以山系水系定之。</p>

<h4>第四条　省份</h4>
<p>传统地区（加利西亚、加泰罗尼亚、葡萄牙、安达卢西亚等）为省或次级行政区，承载历史与语言之保护，不构成政治主体。</p>

<h4>第五条　北非</h4>
<p>北非西部与半岛同属一国行政体系，不设特殊之宪制地位，不列为殖民地或自治领。</p>

<h4>第六条　语言</h4>
<p>地方语言得于学校与地方行政中使用。国家不承认任何民族邦。不得设立独立军队与自主外交。</p>

<p class="doc-seal">〔钤印：伊比利亚制宪议会〕</p>""",
        "significance": "把 S2 的伊比利亚原则（大而少的大区、省份承载传统地区、北非为本土、"
                        "民主化但不联邦化）与 P10 裁定（山系水系命名）整合为一部宪法要纲。",
        "src": ["S0", "S2"],
    },
    {
        "id": "DOC_IBERIA_4REP_FALL", "kind": "文献·调查报告", "year": 1954,
        "year_text": "1954年", "place": "托莱多（推定）", "place_id": "P_TOLEDO",
        "title": "《非洲殖民地危机调查委员会报告》",
        "title_orig": "Bericht des Untersuchungsausschusses zur afrikanischen Krise",
        "author": "伊比利亚第四共和国议会调查委员会", "lang": "伊比利亚-奥克语",
        "context": "第四共和国高度议会化、总统权力受限；1954 年前后非洲殖民地危机爆发，"
                   "第四共和国覆灭。北非西部在法律上属伊比利亚本土行政体系。",
        "body": """<p class="doc-preamble">呈第四共和国议会。委员会主席███。</p>

<h4>一、危机之性质</h4>
<p>本委员会须先纠正一常见之误解：北非西部非殖民地。依本国法律，该地与半岛同属一国行政体系，无特殊宪制地位。故本次危机非殖民地独立之争，而是本国行政体系内部之撕裂。</p>

<h4>二、制度之失能</h4>
<p>第四共和国之议会制，使行政权分散于内阁与各委员会。总统无权。危机起时，内阁三度更迭，无人能作决断。</p>

<h4>三、结论</h4>
<p>若欲维持国家之统一与北非之属地，则须有能决断之行政权。现行宪法之议会至上原则，与本国之地缘现实不相容。</p>

<p class="doc-seal">〔钤记：议会调查委员会〕</p>""",
        "significance": "为「第四共和国覆灭 → 第五共和国总统权力加强」提供制度逻辑，"
                        "并强调北非为本土而非殖民地这一关键设定。",
        "src": ["S2"],
    },
    {
        "id": "DOC_UK_CENTRAL_LOCAL", "kind": "文献·法案", "year": 1947,
        "year_text": "1947年", "place": "伦敦", "place_id": "P_LONDON",
        "title": "《中央与地方权限划分法》",
        "title_orig": "Act on the Division of Powers between Centre and Regions",
        "author": "不列颠联邦共和国议会", "lang": "英语",
        "context": "S3：民主化后强制联邦化分权；一级联邦单位拥有自己的议会、政府与法院，"
                   "但不设民族邦主权、不设独立军队与外交，法律体系统一。",
        "body": """<p class="doc-preamble">An Act to divide the powers of government.</p>

<h4>1. Regional competence</h4>
<p>Each federal unit shall have its own legislature, executive and courts, with competence over education, culture, local policing and internal transport.</p>

<h4>2. Reserved matters</h4>
<p>Defence, foreign affairs, currency, customs and the highest appellate jurisdiction are reserved to the Republic. No federal unit shall raise armed forces of its own or conduct its own foreign relations.</p>

<h4>3. Uniform law</h4>
<p>The legal system of the Republic shall remain uniform. No unit shall possess a separate legal tradition of its own.</p>

<h4>4. Language and culture</h4>
<p>Units may provide for regional cultural councils and bilingual education. Such provision is cultural, not sovereign; it shall not found a claim to nationhood.</p>

<p class="doc-seal">〔Seal: Parliament of the Federal Republic of Britain〕</p>""",
        "significance": "把 S3 的关键限定（有联邦单位之权、无民族邦主权）写成成文法条文，"
                        "明确「文化自治 ≠ 民族主权」。",
        "src": ["S3"],
    },
    {
        "id": "DOC_COMMONWEALTH_CHARTER", "kind": "文献·章程", "year": 1955,
        "year_text": "1955年前后", "place": "伦敦", "place_id": "P_LONDON",
        "title": "《英联邦章程》",
        "title_orig": "Charter of the Commonwealth", "author": "英联邦成员代表",
        "lang": "英语",
        "context": "S3：英联邦存在但远不如现实庞大；性质是语言、文化与商业共同体，"
                   "而非政治军事帝国。裁定 P13：列 5—8 个具名成员，明确「无共同防务条款」。",
        "body": """<p class="doc-preamble">Agreed by the members of the Commonwealth.</p>

<h4>1. Nature</h4>
<p>The Commonwealth is a community of language, culture and commerce. It is not a political or military empire.</p>

<h4>2. No common defence</h4>
<p>There shall be no common defence clause. No member is bound to assist another in war. Each retains full sovereignty in foreign affairs and defence.</p>

<h4>3. Members</h4>
<p>Canada, Australia, New Zealand, South Africa, Newfoundland, Malta and Ceylon, together with such other dominions and island territories as may accede.</p>

<h4>4. No territory</h4>
<p>The Commonwealth holds no territory of its own. The standing of Britain in the world rests not upon the extent of the Commonwealth but upon her industry, finance, the remnant of her navy, and the network of her language and culture.</p>

<p class="doc-seal">〔Seal: the Commonwealth Secretariat〕</p>""",
        "significance": "把 P13 裁定「无共同防务条款」与 S3「依靠工业、金融、海军残余与语言文化网络，"
                        "而非领土规模」写成章程，并列出七名成员。",
        "src": ["S3"],
    },
    {
        "id": "DOC_ROS_UHLUS_CHARTER", "kind": "文献·国家章程", "year": 1550,
        "year_text": "16世纪", "place": "莫斯科", "place_id": "P_MOSCOW",
        "title": "《罗斯兀鲁思国家章程》",
        "title_orig": "Устав Рос-Улуса", "author": "莫斯科蒙古王朝",
        "lang": "东斯拉夫语（兼录蒙古语制度词汇）",
        "context": "罗斯兀鲁思的国家正统：古罗斯诸国 → 蒙古征服 → 金帐秩序 → 罗斯兀鲁思；"
                   "国家认同是「继承了蒙古-罗斯的北方帝国」。文化四层：东斯拉夫+蒙古+突厥+佛教/萨满。",
        "body": """<p class="doc-preamble">奉长生天之命，莫斯科之大汗敕定。</p>

<h4>第一　政统</h4>
<p>吾国政统，上承金帐秩序。古罗斯诸国为吾国史之早段，然非政统之本。金帐汗国为吾国现代国家制度之直接祖。</p>

<h4>第二　官制</h4>
<p>存金帐之制：驿道（站赤）、税籍、贵族等级、诸公继承之裁决，皆仍旧章。</p>

<h4>第三　宗教</h4>
<p>东正教为斯拉夫人口之信仰，官府保护之，不干预之。宫廷奉长生天，崇佛教。萨满之礼，存于氏族与乡里。</p>

<h4>第四　语言</h4>
<p>文书用东斯拉夫语，兼录蒙古语制度词汇。西里尔字母并用于蒙古语之转写。</p>

<h4>第五　正统</h4>
<p>吾国不自称「最正统之罗斯人」，而自称「蒙古帝国—金帐汗国政治秩序在北方之合法继承者」。</p>

<p class="doc-seal">〔钤印：莫斯科大汗之玺〕</p>""",
        "significance": "把 S4 的国家正统、官制沿袭、复合宗教结构与「后基辅罗斯国家」的自我定位"
                        "整合为一部国家章程。",
        "src": ["S4"],
    },
    {
        "id": "DOC_KIEV_EUROPE_CHARTER", "kind": "文献·国家章程", "year": 1946,
        "year_text": "1946年", "place": "基辅", "place_id": "P_KYIV",
        "title": "《基辅王国国家章程》",
        "title_orig": "Статут Королівства Київ", "author": "基辅王国议会",
        "lang": "东斯拉夫语（乌克兰语域）",
        "context": "S4：基辅王国自认古罗斯传统的真正继承者，强调基辅、东斯拉夫传统、"
                   "东欧基督教、欧洲政治文化、古罗斯法律传统，与中欧、德意志、波罗的海的联系，"
                   "越来越靠近欧洲文明。P22：与白罗斯组成联邦。",
        "body": """<p class="doc-preamble">基辅王国议会制定。</p>

<h4>第一条　正统</h4>
<p>本国为古罗斯传统之真正继承者。基辅为古罗斯之母城，其法律与信仰传统由本国承续。</p>

<h4>第二条　文明归属</h4>
<p>本国属欧洲东部。本国之文明来源为东欧基督教、古罗斯法律、欧洲政治文化。</p>

<h4>第三条　联邦</h4>
<p>本国与白罗斯共组联邦，两国同为联邦之构成主体。</p>

<h4>第四条　邻邦</h4>
<p>本国与中欧、德意志、波罗的海诸国维持密切之文化与商业联系，以驿道与第聂伯河之舟楫相通。</p>

<h4>第五条</h4>
<p>本国与罗斯兀鲁思为两个主权国家。古罗斯世界已永久分裂，此事实载于国史，不为讳。</p>

<p class="doc-seal">〔钤印：基辅王国议会〕</p>""",
        "significance": "把 S4 的「罗斯向欧洲发展」道路与 P22 的白罗斯联邦裁定写成国家章程，"
                        "并与罗斯兀鲁思的章程形成对照文本。",
        "src": ["S4"],
    },
    {
        "id": "DOC_MONGOL_RELIGION_EDICT", "kind": "文献·敕令", "year": 1280,
        "year_text": "13世纪", "place": "哈拉和林（推定）", "place_id": None,
        "title": "《宗教免赋敕令》",
        "title_orig": "ᠳᠠᠯᠠᠯᠭ᠎ᠠ ᠶᠢᠨ ᠵᠠᠷᠯᠢᠭ",
        "author": "蒙古大汗", "lang": "蒙古语（德译本）",
        "context": "S1：蒙古帝国保持「长生天 + 佛教 + 萨满」三层宗教结构，"
                   "统治者长期保持对不同宗教的宽容。宗教多元是蒙古社会结构的一部分。",
        "body": """<p class="doc-preamble">大汗敕令。德译本。</p>

<h4>一</h4>
<p>佛僧、道士、回回阿訇、也里可温教士，及各氏族之萨满，皆免赋税，免兵役。</p>

<h4>二</h4>
<p>各以其法祈天，为汗祈寿。天必听之，不问其法之名。</p>

<h4>三</h4>
<p>不得以官力改人之信仰。刀能改人，不能改心；心不改，则地不稳。</p>

<h4>四</h4>
<p>天山以东诸佛国，河中杂处之地，皆依此令。</p>

<p class="doc-seal">〔钤印：大汗之玺〕</p>""",
        "significance": "把 S1 的宗教宽容原则写成可援引的敕令，"
                        "并直接给出「不得以官力改人之信仰」这一西域佛教带得以长期存在的制度原因。",
        "src": ["S1"],
    },
    {
        "id": "DOC_ANATOLIAN_CAPITULATION", "kind": "文献·通商条约", "year": 1535,
        "year_text": "16世纪", "place": "君士坦丁堡", "place_id": "P_CONSTANTINOPLE",
        "title": "《海峡通行与通商条约》",
        "title_orig": "Handels- und Durchfahrtsvertrag der Straße",
        "author": "君士坦丁堡议会与安纳托利亚突厥帝国", "lang": "希腊语、奥斯曼突厥语并行",
        "context": "S1：海峡是文明边界，而不是文明墙。P31：君士坦丁堡为希腊人主导的"
                   "基督教城邦—海峡政治体，控制海峡通行权，靠通行税与贸易维生；"
                   "与安纳托利亚突厥帝国长期对峙共处。",
        "body": """<p class="doc-preamble">君士坦丁堡议会与安纳托利亚突厥帝国御前会议共订。</p>

<h4>第一条</h4>
<p>海峡通行之权，归君士坦丁堡。凡过海峡之舟，无论其旗为十字、为新月、为鹰、为狮，皆纳通行之税。</p>

<h4>第二条</h4>
<p>税则一律，不因教派而异。穆斯林商人之税，与基督徒商人之税同。</p>

<h4>第三条</h4>
<p>双方商民得于对岸设栈、置货、雇工、立契。契约依所在之法。</p>

<h4>第四条</h4>
<p>安纳托利亚之军不入本城，君士坦丁堡之军不入安纳托利亚。此两岸之约，世代守之。</p>

<p class="doc-seal">〔钤印：君士坦丁堡议会、突厥帝国御前会议〕</p>""",
        "significance": "把「海峡是文明边界，而不是文明墙」这一 S1 核心表述，"
                        "落实为一份双向通商条约及其军事互不进入条款。",
        "src": ["S1"],
    },
]

# ============================================================
# B. 日记（第二批）
# ============================================================
DIARIES = [
    {
        "id": "DIA_HABSBURG_MONK_1450", "kind": "日记", "year": 1450,
        "year_text": "1450年前后", "place": "维也纳", "place_id": "P_VIENNA",
        "title": "维也纳宫廷书记官日记·双元君主国的日常",
        "author": "普热米斯尔宫廷书记官（架空人物）", "author_id": "D_PREMISLID",
        "lang": "高地德语（波西米亚德语色彩）",
        "context": "14世纪后期哈布斯堡取得皇帝位，形成双元君主国：法兰克王冠为实际权力核心，"
                   "德意志王冠为帝国法理基础，皇帝冠冕需三重加冕。",
        "body": """<p class="doc-preamble">维也纳。宫廷文书房。</p>

<p>今日抄录皇帝敕令三道。第一道寄法兰克福，第二道寄帕里斯，第三道寄罗马。三处用三种不同的头衔，须一一核对，错一字则礼部驳回。</p>

<p>法兰克那头衔是「法兰克人的国王」，世袭，由雷姆斯加冕。德意志那头衔是「德意志人的国王」，由七侯在法兰克福选出。两者合于一身，才得称「罗马人的皇帝」。</p>

<p>同一个人，三顶冠，两族的君主。这制度怪，但它已经运行了一百年。</p>

<p>我常想：若有一天两族不再要同一个皇帝，这套文书该怎么办。那时大概要先改称谓的格式——而格式，是政治最先变动的地方。</p>""",
        "significance": "从文书官的角度呈现「同一个帝国皇帝，同时是两个政治民族的国王」这一制度矛盾，"
                        "并点出「格式是政治最先变动的地方」。",
        "src": ["S0", "S1"],
    },
    {
        "id": "DIA_LOWLAND_MERCHANT", "kind": "日记", "year": 1645,
        "year_text": "1645年", "place": "阿姆斯特丹", "place_id": "P_AMSTERDAM",
        "title": "阿姆斯特丹商人日记·战争中的生意",
        "author": "低地加尔文宗商人（架空人物）", "author_id": None,
        "lang": "低地德语（荷兰语域）",
        "context": "宗教战争丹麦-低地阶段（1625—1629）与伊比利亚-法兰克阶段（1635—1648）："
                   "低地凭海军和金融坚持抵抗；1648 年低地联合省正式独立，成为加尔文宗共和国。",
        "body": """<p class="doc-preamble">阿姆斯特丹。账房。</p>

<p>今日又向交战双方各贷一笔。法兰克的贵族要买船，皇帝要发饷，我两边的息都收。</p>

<p>有人说这不义。我说：若我不贷，自有人贷；海上的货总要有人运。而且两国打仗，货价涨，我的仓里正有货。</p>

<p>长老今日讲道，说预定论：得救者早已注定，不因善行。我听了安心。生意场上没有定数，神那里有定数，这样最好。</p>

<p>荷兰语与低地北部的德语，在我耳朵里是一种话的两个说法。南边的人听得懂我，我听得懂他们。既然如此，我们为什么要归他们管？海峡这一道水，便是一切。</p>""",
        "significance": "呈现加尔文宗商业伦理与低地独立的实际动机（海军与金融），"
                        "并落实「荷兰语被视为低地德语一部分」这一语言设定。",
        "src": ["S0"],
    },
    {
        "id": "DIA_OTTOMAN_SCHOLAR", "kind": "日记", "year": 1517,
        "year_text": "1517年", "place": "开罗", "place_id": "P_CAIRO",
        "title": "开罗学者日记·马穆鲁克终局",
        "author": "开罗学者（架空人物）", "author_id": None,
        "lang": "阿拉伯语（德译本）",
        "context": "1517 年安纳托利亚突厥帝国取代马穆鲁克王朝，取得汉志两圣地宗主权；"
                   "近东整合为单一逊尼派伊斯兰帝国，与波斯什叶派体系长期并立。",
        "body": """<p class="doc-preamble">开罗。爱资哈尔学院。</p>

<p>苏丹的军队已入城。马穆鲁克之贵族，或死或逃。爱资哈尔照常开课——学院不属任何王朝，此事在数百年间屡经变乱而未改。</p>

<p>新来的统治者是突厥人。他们自安纳托利亚来，说突厥语，读阿拉伯经，也读波斯诗。他们取得两圣地之宗主权，从此哈里发之名在他们庇护之下。</p>

<p>我在课上对学生说：近东已合为一。东边的波斯是什叶，我们是逊尼，中间隔着两河与高原。这条线，此后数百年不会变。</p>

<p>学生问：那我们还算埃及吗？我说：算。统治者换了，学院没换，尼罗河没换。</p>""",
        "significance": "从伊斯兰一方呈现 1517 年近东整合，并解释逊尼派阿拉伯—安纳托利亚体系"
                        "与什叶派波斯体系的双极并立格局。",
        "src": ["S1"],
    },
    {
        "id": "DIA_PERSIA_SCHOLAR", "kind": "日记", "year": 1000,
        "year_text": "11世纪", "place": "布哈拉", "place_id": "P_BUCHARA",
        "title": "布哈拉僧人日记·经的两种字母",
        "author": "西域-波斯佛僧（架空人物）", "author_id": None,
        "lang": "波斯语（兼录粟特语）",
        "context": "P5 裁定：波斯曾抵御伊斯兰入侵，后因内乱退守河中及以东；"
                   "「波斯」概念撕裂为伊斯兰什叶派波斯（伊朗）与佛教-西域波斯残余。",
        "body": """<p class="doc-preamble">布哈拉。寺院的抄经房。</p>

<p>今日抄《般若》一卷，用波斯文。两日路程之外，有人用同样的字母写另一种经。</p>

<p>长老说：文字是一样的，路是两条。这句话我抄在卷末。</p>

<p>西边的那半波斯，如今叫伊朗——那是地理的名字。他们忘了我们是同一族人。其实我们没有变，变的是他们：他们在内乱之中丢掉了自己的佛，捡起了别人的经。</p>

<p>我把这一卷另抄一份，托商队带往敦煌。纸比城墙耐久，长老常说这句。</p>""",
        "significance": "以抄经僧的视角呈现 P5 裁定的「波斯撕裂」，"
                        "并重申「纸比城墙耐久」——西域-波斯文献得以跨时代保存的理由。",
        "src": ["S1"],
    },
    {
        "id": "DIA_KIEV_STUDENT", "kind": "日记", "year": 1960,
        "year_text": "1960年前后", "place": "基辅", "place_id": "P_KYIV",
        "title": "基辅大学生日记·两个罗斯",
        "author": "基辅大学生（架空人物）", "author_id": None,
        "lang": "东斯拉夫语（乌克兰语域）",
        "context": "S4：基辅王国与罗斯兀鲁思的文明分流——基辅向欧洲，罗斯兀鲁思向蒙古-北亚。"
                   "二战后国际秩序承认两国为不同主权国家。",
        "body": """<p class="doc-preamble">基辅。大学宿舍。</p>

<p>放假时我随考察队去东边。过了边界，火车上的告示牌换了字，教堂的顶还是金的，但宫廷里的仪典有蒙古的样式：驿道的站、贵族的等、汗的名。</p>

<p>那里的人也读古罗斯的编年史，但他们把它放在「古罗斯时代」一章里，后面接的是「蒙古—金帐时代」。他们说蒙古帝国是「我们的帝国时代之一」。</p>

<p>我们这里的历史课本不是这样写的。我们的第二王朝就是古罗斯本身。</p>

<p>一个民族，两条路。老师说这是一次文明分流，不是谁对谁错。我信。但我仍觉得，我们和他们之间那条边界，是欧洲与亚洲之间最短的一条线。</p>""",
        "significance": "从年轻人的日常体验呈现 S4 的「文明分流」，"
                        "并落实「基辅王国是罗斯向欧洲发展的道路，罗斯兀鲁思是罗斯向蒙古-北亚发展的道路」。",
        "src": ["S4"],
    },
    {
        "id": "DIA_OCCITAN_TEACHER", "kind": "日记", "year": 1980,
        "year_text": "1980年前后", "place": "托洛森", "place_id": "P_THOLOSEN",
        "title": "奥克双语教师日记·正常化之后",
        "author": "奥克语双语教师（架空人物）", "author_id": None,
        "lang": "伊比利亚-奥克语（奥克语域） / 法兰克语",
        "context": "1972—1978 年奥克正常化：南部奥克省废除，奥克各州升为普通联邦州；"
                   "奥克语可作州级官方语言、实行双语教育，但法兰克语仍是联邦唯一官方语言。",
        "body": """<p class="doc-preamble">托洛森。州立中学。</p>

<p>今天开学。我用奥克语点名，用奥克语讲第一课。孩子们听得懂——他们的祖父母在家里说这个话，父母只说一半，他们现在在学校里重新学全。</p>

<p>一九七五年之前，这所学校里说奥克语是要罚的。省署说那是「不合规范」。后来省署撤了，我们成了普通的州。普通人有了不普通的权利：说自己的话，在课堂上。</p>

<p>但我不能骗孩子。联邦的法律、公文、法院，还是用法兰克语。他们若想走出这个州，还是要会那一种。双语不是两条平齐的路，是一条宽一条窄。</p>

<p>我告诉他们：宽的那条通往帕里斯，窄的那条通往你自己的家。两条都值得走。</p>""",
        "significance": "从教师视角呈现「奥克正常化」的实际效果与限度："
                        "文化承认＋普通联邦州地位，但法兰克语仍是联邦唯一官方语言。",
        "src": ["S2"],
    },
    {
        "id": "DIA_IRELAND_TEACHER", "kind": "日记", "year": 1960,
        "year_text": "1960年前后", "place": "都柏林", "place_id": "P_DUBLIN",
        "title": "爱尔兰教师日记·西部的凯尔特语",
        "author": "爱尔兰教师（架空人物）", "author_id": None,
        "lang": "爱尔兰英语（罗曼化程度最低的一支） / 凯尔特语",
        "context": "S3：爱尔兰 1945 年全岛独立为共和国；长期文化殖民使本土凯尔特语言文化"
                   "大幅减弱，未出现现实式的盖尔语复兴。用户 P14/P35 裁定："
                   "凯尔特语为全国官方语言，与爱尔兰保留的弱罗曼化英语并列为官方语言。",
        "body": """<p class="doc-preamble">都柏林，后转康诺特。</p>

<p>我在西部支教两年。这里的老人家说凯尔特语，说得慢，词很旧。他们说这种话的时候，会停下来想，因为有些东西没有别的说法。</p>

<p>课本上是官方语言——共和国的两种官方语言之一。但街上说英语，议会说英语，连我上课也多半说英语，只是用英语解释凯尔特语的语法。孩子问我：既然它不用，为什么它是官方语言？</p>

<p>我说：因为它是我们的。这句话有点软弱，但它是真的。语言不因为有用才留下，有时候只是因为有人在它里面出生。</p>

<p>我们这里说的英语也与伦敦的不一样。它离宫廷的腔调远得多，里面的日耳曼成分更重——因为几百年来，宫廷的舌头从来没有伸到这里。</p>""",
        "significance": "落实 P14/P35 的凯尔特语官方地位裁定，同时呈现 S3 所记"
                        "「未出现现实式的盖尔语复兴」这一事实，并印证「爱尔兰英语是罗曼化程度最低的一支」。",
        "src": ["S3"],
    },
    {
        "id": "DIA_BRITAIN_WORKER", "kind": "日记", "year": 1946,
        "year_text": "1946年", "place": "伦敦", "place_id": "P_LONDON",
        "title": "伦敦码头工人日记·被监督的第一年",
        "author": "伦敦码头工人（架空人物）", "author_id": None,
        "lang": "英语",
        "context": "1945 年不列颠战败后，经制宪会议决议并辅以全民公决废除王位；"
                   "1945—约1955 年为监督过渡期，设监督委员会与制宪会议；"
                   "强制实行多党制与联邦化分权。",
        "body": """<p class="doc-preamble">伦敦。东区码头。</p>

<p>去年这个时候，我们的国王还在。今年，共和国。变化来得比换一块招牌快。</p>

<p>码头上现在有委员会的人——从维也纳和帕里斯来的。他们在街上走过，穿的不是制服，说话很客气，但所有人都知道他们说了算。他们让我们成立政党。我头一回填那种表：我选哪一边。</p>

<p>我父亲那一辈没有这种事。他说他祖父也没见过。这个国家的议会，上一次开门是十四世纪。所以他填表的时候手是抖的。</p>

<p>外国人来教我们怎么投票。这事说出去不好听。但我想，难堪一阵，总好过再来一次。</p>""",
        "significance": "从底层视角呈现 S3 的核心机制「民主化不是自发生长，而是在胜利方监督下被强制推行」，"
                        "并以「上一次开门是十四世纪」呼应「宪政不是中世纪遗产」。",
        "src": ["S3"],
    },
    {
        "id": "DIA_ROS_PRIEST", "kind": "日记", "year": 1900,
        "year_text": "1900年前后", "place": "莫斯科", "place_id": "P_MOSCOW",
        "title": "东正教神父日记·宫廷里的两种经",
        "author": "罗斯兀鲁思东正教神父（架空人物）", "author_id": None,
        "lang": "东斯拉夫语", "context": "S4：莫斯科国的文化结构为东斯拉夫+蒙古+突厥+佛教/萨满四层，"
                                         "形成「东正教斯拉夫人口 + 蒙古佛教王朝」的复合国家。",
        "body": """<p class="doc-preamble">莫斯科。克里姆林宫内。</p>

<p>今日为大汗祈福。仪典之先是长生天的祝辞，由萨满长老诵；次为佛僧诵经；末为我的祈祷。三者在同一厅堂，各据一隅。</p>

<p>我起初不适。后来想通了：我们的教在百姓中间，不在这个厅堂。东边与南边的教堂与佛寺并存，乡村里的人们既来我的堂，也去萨满那里求雨。这不是信仰的混乱，是这片地的规矩。</p>

<p>有年轻的修士问：为何我们不劝朝廷归正？我说：劝过，几百年了。而且教会的中枢不在这里——在君士坦丁堡。那边尚在，我们这边的教会便不必争名分。</p>""",
        "significance": "呈现 S4 所记「东正教斯拉夫人口 + 蒙古佛教王朝」的复合结构，"
                        "并点明「东正教教会不向莫斯科转移，因拜占庭仍然存在」这一推论。",
        "src": ["S4"],
    },
]

# ============================================================
# C. 书信（第二批）
# ============================================================
LETTERS = [
    {
        "id": "LET_ALBRECHT_DAUGHTER", "kind": "书信", "year": 1356, "year_text": "1356年",
        "place": "法兰克福", "place_id": "P_FRANKFURT",
        "title": "阿尔布雷希特二世致其女书",
        "author": "皇帝阿尔布雷希特二世", "author_id": "PE_ALBRECHT_II",
        "recipient": "阿尔布雷希特二世之女", "recipient_id": "PE_ALBRECHT_II_DAUGHTER",
        "lang": "高地德语（皇帝私函）",
        "context": "阿尔布雷希特二世年老无嗣，仅有一女。法兰克贵族要求女婿继承法兰克王位，"
                   "德意志选侯坚持选举德意志诸侯为皇帝。",
        "body": """<p class="doc-preamble">法兰克福，会议之第四月。致吾女。</p>

<p>汝之婚事，原是家务；如今成了国事。</p>

<p>法兰克之贵族愿汝之夫承继王位，德意志之选侯不愿。二者相持不下，已历四月。我老矣，不能久待。</p>

<p>我已想定一策：王冠不分，然继承之法可两立。法兰克之冠归我族，由汝之夫承之；德意志之冠由七侯另选。二者合于一人之身，各依其法。</p>

<p>如此，汝将为一国之母，而那顶德意志的冠，可能落在别家头上。这不是我所愿，但是我能留下的最稳的安排。</p>

<p>若后人问起，你告诉他们：我不要一个统一的王冠，我要一个能存续的秩序。</p>""",
        "significance": "把《法兰克福宪章》双轨制的设计动机写成父亲给女儿的私信，"
                        "呈现「要一个能存续的秩序」这一政治判断。",
        "src": ["S0"],
    },
    {
        "id": "LET_GUTENBERG_LEIPZIG", "kind": "书信", "year": 1550,
        "year_text": "16世纪", "place": "莱比锡", "place_id": "P_LEIPZIG",
        "title": "莱比锡书商致维滕堡教会书",
        "author": "莱比锡书商（架空人物）", "author_id": None,
        "recipient": "维滕堡教会", "recipient_id": "O_WITTENBERG_CHURCH",
        "lang": "高地德语",
        "context": "莱比锡大学以图书出版著称；维滕堡城堡教堂为新教母教会。",
        "body": """<p class="doc-preamble">莱比锡致维滕堡之弟兄。</p>

<p>《十二条款》之传单已印第三版，行销南德意志、莱茵兰与波西米亚。另附南德版本一种，多列三条，曰教堂艺术、农民子弟受教育、自治社区。</p>

<p>北方各邦已下令禁售。然禁令之效，不过使书价涨三成。</p>

<p>有一事请弟兄们留意：南方与北方读同一部圣经，却读出了不同的教会。北方的堂里撤去图像，南方的堂里留下巴洛克祭坛。同一种印刷术，印出两种信。</p>

<p>我不评断孰是。我只作生意——而生意教我一件事：思想一旦可以大量复制，就再也收不回去了。</p>""",
        "significance": "以出版业者视角呈现印刷术对宗教改革与南北新教文化分野的放大作用。",
        "src": ["S0", "S1"],
    },
    {
        "id": "LET_IBERIA_LOWLAND", "kind": "书信", "year": 1636, "year_text": "1636年",
        "place": "托莱多（推定）", "place_id": "P_TOLEDO",
        "title": "伊比利亚第三共和国致低地联合省书",
        "author": "伊比利亚国务秘书处", "author_id": "C_IBERIA",
        "recipient": "低地联合省议会", "recipient_id": "C_LOWLANDS",
        "lang": "伊比利亚-奥克语",
        "context": "S0/S1：西班牙-阿拉贡（与伊比利亚）虽在国内压制新教徒，"
                   "但出于反哈布斯堡法兰克地缘利益，后期加入新教联盟，"
                   "形成「外交新教、内政天主教」矛盾立场。",
        "body": """<p class="doc-preamble">托莱多致阿姆斯特丹。</p>

<p>贵省之信仰，本国不予承认，此点无须讳言。本国境内之新教徒，仍依本国法律处置。</p>

<p>然哈布斯堡之法兰克，其势日张。若法兰克并吞奥克，则地中海西岸尽归其手，贵省之航运与本国之港口同受其困。</p>

<p>故本国愿与贵省结盟，共击法兰克。盟约内不涉宗教条款。</p>

<p>此中矛盾，本国知之，贵省亦知之。有人称之为伪善。本国称之为地缘。</p>

<p class="doc-seal">〔钤印：伊比利亚国务秘书处〕</p>""",
        "significance": "把「外交新教、内政天主教」这一 S1 称为「关键变量」的矛盾立场"
                        "写成一份坦率承认自身矛盾的结盟函。",
        "src": ["S0", "S1"],
    },
    {
        "id": "LET_ROME_WITTENBERG", "kind": "书信", "year": 1540,
        "year_text": "16世纪", "place": "罗马", "place_id": "P_ROME",
        "title": "教廷致维滕堡书·论法兰克教会之提名权",
        "author": "教廷国务枢机", "author_id": "C_PAPAL",
        "recipient": "维滕堡教会", "recipient_id": "O_WITTENBERG_CHURCH",
        "lang": "拉丁语",
        "context": "1356 年《法兰克福宪章》第五条：教皇承认皇帝对法兰克教会的提名权；"
                   "德意志教会由各诸侯自行管理；帝国境内教会财产受法律保护，"
                   "但新教诸侯可自行决定教产归属。",
        "body": """<p class="doc-preamble">Romae, ad Wittenbergam.</p>

<p>圣座承认：皇帝对法兰克教会享有提名之权。此权载于一千三百五十六年之宪章，圣座未曾撤回。</p>

<p>然请注意条约之分界：德意志之教会，由各诸侯自行管理。圣座不承认此安排为正当，然亦不否认其存在。此即宪章第五条之实情——它把一件教义上不可分割之事，在地理上切成了两块。</p>

<p>至于教产：帝国法律保护教会财产，然新教诸侯得自行决定其归属。此条自颁行之日起即为争议之源，圣座预计它将在某一日引发战争。</p>

<p class="doc-seal">〔钤印：教廷国务枢机〕</p>""",
        "significance": "把《法兰克福宪章》第五条的宗教模糊性以教廷视角写明，"
                        "并预告它将引发战争——即 S0 所记「《法兰克福条约》宗教模糊性是宗教战争起因之一」。",
        "src": ["S0"],
    },
    {
        "id": "LET_ALPINE_NORDIC", "kind": "书信", "year": 1570,
        "year_text": "16世纪后期", "place": "慕尼黑", "place_id": "P_MUENCHEN",
        "title": "慕尼黑教会致马格德堡教会书·论音乐",
        "author": "巴伐利亚阿尔卑斯福音派教会", "author_id": "O_BAYERN_NAT_MUSEUM",
        "recipient": "马格德堡教会", "recipient_id": "O_MAGDEBURG_DOM",
        "lang": "高地德语",
        "context": "北德意志路德宗「反对宗教艺术和华丽礼仪」；"
                   "南德意志阿尔卑斯福音派「保留教堂艺术和音乐，认为美、音乐、美食和社交"
                   "是上帝创造的恩典」。",
        "body": """<p class="doc-preamble">慕尼黑致马格德堡。</p>

<p>弟兄来信问：贵处教堂为何仍设管弦乐、仍绘壁画、仍在节期设宴。</p>

<p>我答以一句：我们不认为信主须以愁苦为凭。</p>

<p>贵处之堂，素壁铭碑，庄严肃穆，我们敬重。但我们这里的人，坐在彩绘长椅上，听德语康塔塔，散会后去喝咖啡——他们若被告知这一切都当除去，他们不会留下。</p>

<p>所以我们的神学是这样：十字架下有喜乐，喜乐当有节制，但不可无。</p>

<p>这不是妥协，这是此处的地方教会美学自由。</p>""",
        "significance": "把南北德意志新教的美学分歧写成两地的通信，"
                        "并给出「十字架下的喜悦」这一核心观念的完整表述。",
        "src": ["S0", "S1"],
    },
    {
        "id": "LET_HABSBURG_PRETENDER", "kind": "书信", "year": 1921,
        "year_text": "1921年", "place": "帕里斯", "place_id": "P_PARIS",
        "title": "哈布斯堡家族成员致法兰克共和国总理书",
        "author": "哈布斯堡家族成员（架空人物）", "author_id": "D_HABSBURG",
        "recipient": "法兰克共和国总理", "recipient_id": "C_FRANKEN_REPUBLIC",
        "lang": "法兰克语",
        "context": "S2：哈布斯堡王室保持政治中立；广义哈布斯堡家族仍是庞大的贵族、商业、军事、"
                   "外交、法律/学术、政治社会网络，不同成员可加入不同政党。"
                   "1918 年法兰克建立不完善的共和国，哈布斯堡贵族仍渗透政府与军队。",
        "body": """<p class="doc-preamble">帕里斯，致共和国总理。</p>

<p>舍弟已加入社会民主党。我从政于中间派。我们的从兄在银行，另有一位在军中任职。王室本支已声明政治中立，然家族不是王室。</p>

<p>总理先生或许觉得这很怪：一个家族的人分属不同政党。我告诉您，这不是分裂，这就是法兰克。</p>

<p>我们在此地已六百年。王朝可以结束，家族不能一夜消失。若您要把我们完全赶出政府与军队，您需要另建一整套官僚系统——而那要二十年的钱与十年的太平。</p>

<p>所以我请您区分两件事：王冠，与家族。前者已经交出去了。后者还在做事。</p>""",
        "significance": "落实 S2 的关键区分「哈布斯堡王室 ≠ 整个哈布斯堡家族」，"
                        "并解释为何 1918 年后的法兰克共和国是「不完善的」。",
        "src": ["S2"],
    },
    {
        "id": "LET_MONTFORT_1945", "kind": "书信", "year": 1945,
        "year_text": "1945年", "place": "伦敦", "place_id": "P_LONDON",
        "title": "蒙福尔五世致不列颠制宪会议书",
        "author": "不列颠末代国王蒙福尔五世", "author_id": "PE_MOUNTFORT_V",
        "recipient": "不列颠制宪会议", "recipient_id": None,
        "lang": "英语（宫廷语域）",
        "context": "1945 年二战战败，王权合法性崩溃，经制宪会议决议并辅以全民公决废除王位。",
        "body": """<p class="doc-preamble">To the Constitutional Convention.</p>

<p>I will not obstruct you. The crown is yours to end, and I shall sign the instrument if you require a signature.</p>

<p>But let the record be complete. Our house came to this throne in the disorder of the Iberian wars, restored order, and held it. What sustained it was not consent — there were no parties to consent. It was victory in 1918, and before that, two centuries of the fleet and the counting-house.</p>

<p>In 1945 the victory is gone. That is all. Do not write that the nation rose against us. Write that we lost a war, and that a lost war is the only thing that could have ended us.</p>

<p class="doc-seal">〔Signed: Mountfort V〕</p>""",
        "significance": "让末代国王亲自写明「合法性只剩战功一条支柱」，"
                        "与蒙福尔四世 1918 年的胜利日记构成一头一尾的对照。",
        "src": ["S3"],
    },
    {
        "id": "LET_FRANKEN_UNI", "kind": "书信", "year": 1830,
        "year_text": "19世纪", "place": "帕里斯", "place_id": "P_PARIS",
        "title": "帕里斯王家学院致维也纳大学书·论正统之争",
        "author": "帕里斯王家学院", "author_id": "O_PARIS_AKADEMIE",
        "recipient": "维也纳大学", "recipient_id": "O_VIENNA_UNI",
        "lang": "法兰克语（学术语域） / 共同体德语",
        "context": "S0：法兰克语为罗曼-法兰西领土上的日耳曼语言；"
                   "P33 裁定：帕里斯自认是日耳曼世界的延伸，伦敦则放弃日耳曼身份、更倾向罗曼身份。",
        "body": """<p class="doc-preamble">帕里斯王家学院致维也纳大学。</p>

<p>贵校来函询问：法兰克是否为「罗曼正统」之继承者。本院答：不是，亦不想是。</p>

<p>我们不主张罗曼正统。我们说的是法兰克语，属西日耳曼语支；我们的宫廷用德语，我们的文书用德语，我们的教会奉罗马，我们的王朝出自哈布斯堡。我们是日耳曼世界向西的延伸。</p>

<p>罗曼语的高文化在别处。它不在我们这里，也不在伊比利亚——它在海峡对面。伦敦保存着 langue d'oïl 的最高语域，而他们现在更愿意称自己是罗曼人。</p>

<p>所以两国之间确有竞争，但那不是「谁更正统」的争执，而是两种自我认识的错位。我们向东看，他们向西看，中间隔着一条海峡与五百年。</p>""",
        "significance": "把「正统错位」这一 P33 裁定写成两所学院之间的学术通信，"
                        "明确法兰克自认日耳曼延伸、不主张罗曼正统。",
        "src": ["S3", "S0"],
    },
]

# ============================================================
# D. 演讲（第二批）
# ============================================================
SPEECHES = [
    {
        "id": "SPEECH_1871_IBERIA", "kind": "演讲", "year": 1871,
        "year_text": "1871年", "place": "托莱多（推定）", "place_id": "P_TOLEDO",
        "title": "伊比利亚第三共和国成立演说",
        "author": "伊比利亚第三共和国临时政府首脑（架空人物）", "author_id": None,
        "lang": "伊比利亚-奥克语",
        "context": "1871 年伊比利亚第二帝国被德意志帝国击败，第三共和国成立，延续至 1940 年。",
        "body": """<p class="doc-preamble">托莱多。同胞们。</p>

<p>第二帝国今日终结。罗马与那不勒斯，我们已保不住。北意大利已归维也纳。</p>

<p>这不是我们第一次战败，也不是第一次改制。这个国家自大革命以来，王国、共和国、帝国，反复更迭。有人因此说我们没有定数。我说：正因如此，我们有一种别人没有的东西——我们知道政体可以更换，而国家不会。</p>

<p>第三共和国自今日始。它会有议会，会有宪法，会有选举。</p>

<p>但我请诸位记住一件事：这个国家的力量从来不在于它的政体，而在于它的中央集权。谁当政都一样——半岛是一个，北非是本土的一部分，奥克是我们的边界。这条底线不变。</p>""",
        "significance": "把 1871 年伊比利亚第二帝国战败后的转折写成建国演说，"
                        "并点出「政体可以更换，中央集权不改」这一贯穿伊比利亚史的主线。",
        "src": ["S0", "S1", "S2"],
    },
    {
        "id": "SPEECH_1960_IBERIA", "kind": "演讲", "year": 1960,
        "year_text": "1960年", "place": "托莱多（推定）", "place_id": "P_TOLEDO",
        "title": "伊比利亚第五共和国成立演说",
        "author": "伊比利亚第五共和国首任总统（架空人物）", "author_id": None,
        "lang": "伊比利亚-奥克语",
        "context": "第四共和国因 1954 年前后非洲殖民地危机覆灭；1960 年建立第五共和国，"
                   "总统权力重新加强。",
        "body": """<p class="doc-preamble">托莱多。同胞们。</p>

<p>六年前，第四共和国在危机中倒下。那一届议会很有教养，很守程序，也很无能为力。危机来的时候，内阁换了三次，没有人能作一个决断。</p>

<p>我们今天重建共和国，要做的是相反的事：让国家有决断的能力。</p>

<p>但请听清：这不是回到旧的专制。战后十五年，我们已经学会了普选、议会、法院与新闻。我们要保留这些，同时把行政权还给总统。</p>

<p>一句话：国家可以很强，但权力必须民主化。</p>

<p>还有一件事。北非不是我们的殖民地——它在法律上与半岛同属一国。那里发生的事，不是海外的事，是本国的事。我们这一代人若解决不了它，共和国还会再倒一次。</p>""",
        "significance": "把第四共和国的失败教训与第五共和国的制度选择写成演说，"
                        "并完整表述 S2 的核心命题「国家可以很强，但权力必须民主化」。",
        "src": ["S0", "S2"],
    },
    {
        "id": "SPEECH_HANSA_1789", "kind": "演讲", "year": 1789,
        "year_text": "1789年", "place": "汉堡", "place_id": "P_HAMBURG",
        "title": "汉萨三城议会演说·论为何不参战",
        "author": "汉堡商会代表（架空人物）", "author_id": "O_HANSA",
        "lang": "低地德语",
        "context": "1789 年伊比利亚-奥克大革命席卷南欧，法兰克、普热米斯尔、英国、俄罗斯"
                   "组成反伊比利亚同盟；汉萨城市为自由汉萨城市/城市州。",
        "body": """<p class="doc-preamble">汉堡，议会厅。</p>

<p>有人请本城加入反伊比利亚同盟。本席以为不可。</p>

<p>我们的船在南边有买卖。伊比利亚的港口、奥克的货栈、地中海的航线，都是我们的生计。若我们参战，那些港口会关，货栈会被没收。</p>

<p>有人说这不义——革命军在那边推翻国王。我说：他们的国王不是我们的国王。当年宪章给我们三城议会之席位，条件是对外不与帝国之敌结盟。伊比利亚不是帝国的敌人。</p>

<p>我们是商人，我们的城是自由汉萨城市。自由的意思是：可以自己算这笔账。</p>""",
        "significance": "以城市州视角呈现帝国体系中的商业自治逻辑，"
                        "并援引《法兰克福宪章》关于汉萨城市对外结盟的限制条款。",
        "src": ["S0"],
    },
    {
        "id": "SPEECH_SPRACHKONFERENZ_1700", "kind": "演讲", "year": 1700,
        "year_text": "18世纪（推定）", "place": "法兰克福", "place_id": "P_FRANKFURT",
        "title": "泛德意志语言会议开幕演说",
        "author": "会议主席（架空人物）", "author_id": "O_SPRACHKONFERENZ",
        "lang": "共同体德语",
        "context": "三国推行统一正字法，融合高地德语（含瑞士）、法兰克德语、低地德语（含荷兰），"
                   "成为德语通用语言。",
        "body": """<p class="doc-preamble">法兰克福。与会者：德意志各州教育部长、法兰克王家学院院士、
瑞士联邦理工学院与巴塞尔大学学者、三大新教教会与天主教法兰克教会代表。</p>

<p>我们今日要做的事，在别处没有先例：把三种写法合成一种，而不废掉任何一种说法。</p>

<p>高地的、法兰克的、低地的，本是同一条语言带上的三个段落。我们不是要选一个当正统——那会输。我们要造一个三者都能认的写法。</p>

<p>为此，我提五条：词源优先；跨方言折中；词汇层融合；语法保守；拼写标注发音。</p>

<p>我要特别说第四条。我们要存古的格、性、数，哪怕许多方言里已经没有了——因为那些形式是我们共同的旧账。一个共同语，需要一本共同的旧账。</p>

<p>至于方言：它们留在家里、留在乡里、留在地方文学里。我们不废它们。标准语是用来写的，方言是用来活的。</p>""",
        "significance": "把统一正字法的五条原则写成会议开幕辞，"
                        "并给出「标准语用来写、方言用来活」这一语言政策的基本立场。",
        "src": ["S0"],
    },
    {
        "id": "SPEECH_WW1_DEBATE", "kind": "演讲", "year": 1916,
        "year_text": "1916年", "place": "维也纳", "place_id": "P_VIENNA",
        "title": "维也纳战时议会演说·论为何而战",
        "author": "德意志帝国议员（架空人物）", "author_id": None,
        "lang": "共同体德语",
        "context": "一战中德意志帝国与法兰克携手对抗伊比利亚、英帝国、俄罗斯与美国。"
                   "S1：「一个拥有远超现实德国的工业、人口、学术和文化资产的德意志世界，"
                   "仍然输掉了第一次世界大战。」",
        "body": """<p class="doc-preamble">维也纳。议会。</p>

<p>有人问：我们为何而战？我要给一个不体面的答案——为出货的路，为进口的粮。</p>

<p>我们的工业带需要鲁尔的煤、洛林的铁、波河的棉。我们的港口需要北海与地中海的航线。若伊比利亚控制了西地中海，英帝国封了北海，我们的工厂会在半年内停。</p>

<p>所以这不是荣耀之战，是通路之战。</p>

<p>我也要提醒诸位一句不中听的话：我们即使输了这场战争，也不会亡国。因为我们的资产不在皇冠上——在布拉格的实验室、在米兰的工坊、在阿姆斯特丹的银行、在维也纳的音乐厅。这些搬不走。</p>

<p>打赢最好。打输，我们还在。</p>""",
        "significance": "把 S1「一战不是失败点而是韧性测试」这一核心命题，"
                        "写成战时的国会演说，并由当事人自己预言了最坏结果。",
        "src": ["S0", "S1"],
    },
    {
        "id": "SPEECH_EU_1990", "kind": "演讲", "year": 1990,
        "year_text": "1990年前后", "place": "（未具名欧洲城市）", "place_id": None,
        "title": "欧洲学院开学演说·论多层政治传统",
        "author": "欧洲学院院长（架空人物）", "author_id": "O_EUROPA_ACADEMY",
        "lang": "共同体德语（兼用英语与法兰克语）",
        "context": "S2：把欧盟理解为「古老欧洲多层政治传统的现代民主化延续」，"
                   "而不是简单地把欧盟写成「HRE 2.0」。",
        "body": """<p class="doc-preamble">欧洲学院，开学典礼。</p>

<p>诸位来自德意志、法兰克、伊比利亚、不列颠、瑞士与基辅王国。你们会在这里发现一件事：我们六国的民主制度，长得不一样。</p>

<p>德意志是联邦制，法兰克是宪政君主传统，伊比利亚是中央集权型民主，瑞士是永久联邦与永久中立，不列颠是战后才被强加的民主，基辅王国是欧洲东部的议会传统。</p>

<p>有人因此说欧盟是一个勉强凑起来的机构。我说相反：它是一条很长的制度河流的现代形态。</p>

<p>诸位若只读本国的宪法史，会以为自己的制度是唯一的正解。读了六国的，就会明白：多层、嵌套、共同决策，本来就是这片大陆的常态——只是从前由王朝和教会承担，如今由议会和法院承担。</p>

<p>所以请不要把欧盟写成帝国复辟。它是那些旧传统的民主化延续。</p>""",
        "significance": "把 S2「欧盟是古老欧洲多层政治传统的现代民主化延续，而非 HRE 2.0」"
                        "这一判断写成开学演说，并逐国点出六种不同的民主模式。",
        "src": ["S2"],
    },
    {
        "id": "SPEECH_ARTIFACT_MUSEUM", "kind": "演讲", "year": 1919,
        "year_text": "1919年", "place": "维也纳", "place_id": "P_VIENNA",
        "title": "维也纳国家博物馆开馆演说·论失去皇冠之后",
        "author": "维也纳艺术史博物馆馆长（架空人物）", "author_id": "O_KUNSTHIST_MUSEUM",
        "lang": "共同体德语",
        "context": "一战后普热米斯尔王朝结束，成立德意志共和国；霍夫堡移交共和国，"
                   "宫内藏品转入国家博物馆体系。",
        "body": """<p class="doc-preamble">维也纳。开馆之日。</p>

<p>诸位今日看到的是宫廷的收藏，成为国家的收藏。宝库的钥匙，由王室交到共和国手里。</p>

<p>有一个问题我要在这里回答：这些东西原本属于一个王朝，王朝没有了，它们属于谁？</p>

<p>我的回答是：属于制作它们的人，和后来看它们的人。祭坛属于雕刻它的人，管风琴属于弹奏它的人，王冠属于那个曾经戴它、后来交出去的时代。</p>

<p>我们今天把这些东西摆出来，不是为了怀念皇冠，是为了说明一件事——一个文明可以在失去国家形式之后，仍然保有它的实物。</p>

<p>请诸位进来看看。然后请记住：这些东西我们没有失去，也不会失去。</p>""",
        "significance": "把「一战战败但文明存续」这一命题放在博物馆的语境里说，"
                        "并以实物（王冠、祭坛、管风琴）为其证据——与历史物品留存层直接呼应。",
        "src": ["S0", "S1"],
    },
    {
        "id": "SPEECH_1940_IBERIA", "kind": "演讲", "year": 1940,
        "year_text": "1940年", "place": "托莱多（推定）", "place_id": "P_TOLEDO",
        "title": "伊比利亚第三共和国末代演说",
        "author": "伊比利亚第三共和国末任总统（架空人物）", "author_id": None,
        "lang": "伊比利亚-奥克语",
        "context": "1940 年伊比利亚第三共和国被法兰克与德意志击败，进入 1940—1945 被占领与过渡期。",
        "body": """<p class="doc-preamble">托莱多。广播。城市已被包围。</p>

<p>同胞们，我要作最后一篇报告。</p>

<p>法兰克与德意志的军队已入半岛。政府将停止行使职权。</p>

<p>有人会问：我们为何又站在失败的一边？因为两次大战里，我们选的都是海上的那一方。这个选择有其理由——海路是我们的命。只是这一次，海没有救我们。</p>

<p>我要留下三句话给后来的人。</p>

<p>第一：奥克已经保不住了，从今天起不必再谈它。</p>

<p>第二：无论谁在这片土地上重建政权，北非都必须与半岛同属一体。这不是殖民，这是本国。</p>

<p>第三：这个国家不会消失。它会以另一种政体回来——第四、第五、第六，随便叫什么。但中央集权会回来。</p>""",
        "significance": "把 1940 年战败与「政体会再回来但现在先停」写成末代演说，"
                        "并为第四共和国的议会化与第五共和国的总统制回归预设了历史对照。",
        "src": ["S0", "S2"],
    },
    {
        "id": "SPEECH_PERSIA_SPLIT_2", "kind": "演讲", "year": 1100,
        "year_text": "12世纪", "place": "撒马尔罕", "place_id": "P_SAMARKAND",
        "title": "西域-波斯僧团决议开示·论不退",
        "author": "撒马尔罕寺院长老（架空人物）", "author_id": "O_SAMARKAND_VIHARA",
        "lang": "波斯语",
        "context": "P5 裁定：波斯退守河中及以东；「波斯」概念撕裂为伊斯兰什叶派波斯（伊朗）"
                   "与佛教-西域波斯残余。S1：伊斯兰化止步于更西侧。",
        "body": """<p class="doc-preamble">撒马尔罕。僧团会议。</p>

<p>西边的商队带来消息：那边的波斯已经彻底改了经。他们现在自称伊朗。</p>

<p>有人问：我们是否也要改？我答：不必，也不能。</p>

<p>我们留在这里，是因为当年内乱之时，有人守住了这一段河。守住的人不多，但够了。从此阿姆河成了界线——以西是他们的，以东是我们的。</p>

<p>我要诸位做三件事。</p>

<p>一，把我们的经、诗、历、医，各抄三份：一份送敦煌，一份送天山之南，一份留在此处。</p>

<p>二，收留从西边逃来的僧人。他们带着那边的写法与说法，不要让这些东西断绝。</p>

<p>三，不与西边为敌。他们走的是另一条路，那条路是我们当年在内乱中让出来的。</p>""",
        "significance": "把 P5 裁定的「阿姆河为界」与西域-波斯的文化自保策略写成僧团决议，"
                        "并与《白史》所记蒙古宗教宽容形成前后呼应。",
        "src": ["S1"],
    },
]
