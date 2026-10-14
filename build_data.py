import json
from english_content import apply_english, finish_english
from quantum_literature import attach_literature
from qc_review import apply_review
import build_figures
import v028_figures
from v028_content import apply_v028
from v029_content import apply_v029
from pathlib import Path

ROOT=Path(__file__).parent
BASE='https://openstax.org/books/organic-chemistry/pages/'
sources={
 'acid':('2.9 · Acid–base equilibria','2-9-predicting-acid-base-reactions-from-pka-values'),
 'lewis':('2.11 · Lewis acids and bases','2-11-acids-and-bases-the-lewis-definition'),
 'sn2':('11.2 · The SN2 reaction','11-2-the-sn2-reaction'),
 'sn2scope':('11.3 · SN2 scope and stereochemistry','11-3-characteristics-of-the-sn2-reaction'),
 'sn1':('11.4 · The SN1 reaction','11-4-the-sn1-reaction'),
 'e2':('11.8 · E2 and kinetic isotope effects','11-8-the-e2-reaction-and-the-deuterium-isotope-effect'),
 'e1':('11.10 · E1 and E1cB','11-10-the-e1-and-e1cb-reactions'),
 'alkene':('7.7 · Electrophilic addition','7-7-electrophilic-addition-reactions-of-alkenes'),
 'hydration':('8.4 · Alkene hydration','8-4-hydration-of-alkenes-addition-of-h2o-by-oxymercuration'),
 'ether':('18.2 · Williamson ether synthesis','18-2-preparing-ethers'),
 'epoxide':('18.5 · Epoxide ring opening','18-5-reactions-of-epoxides-ring-opening'),
 'carbonyl':('19.4 · Nucleophilic carbonyl addition','19-4-nucleophilic-addition-reactions-of-aldehydes-and-ketones'),
 'hydride':('19.7 · Hydride and Grignard addition','19-7-nucleophilic-addition-of-hydride-and-grignard-reagents-alcohol-formation'),
 'cyanohydrin':('19.6 · Cyanohydrin formation','19-6-nucleophilic-addition-of-hcn-cyanohydrin-formation'),
 'acyl':('21.2 · Nucleophilic acyl substitution','21-2-nucleophilic-acyl-substitution-reactions'),
 'aldol':('23.1 · Aldol addition','23-1-carbonyl-condensations-the-aldol-reaction'),
 'radical':('6.6 · Radical reactions','6-6-radical-reactions'),
 'da':('14.4 · Diels–Alder cycloaddition','14-4-the-diels-alder-cycloaddition-reaction'),
 'dastereo':('14.5 · Diels–Alder stereochemistry','14-5-characteristics-of-the-diels-alder-reaction'),
 'claisen':('30.8 · Sigmatropic rearrangements','30-8-some-examples-of-sigmatropic-rearrangements'),
 'electro':('30.3 · Thermal electrocyclic stereochemistry','30-3-stereochemistry-of-thermal-electrocyclic-reactions'),
 'e1cb':('11.10 · E1 and E1cB','11-10-the-e1-and-e1cb-reactions'),
 'bromination':('8.1 · Addition of halogens to alkenes','8-1-addition-of-halogens-to-alkenes'),
 'halohydrin':('8.3 · Halohydrins from alkenes','8-3-halohydrins-from-alkenes-addition-of-ho-x'),
 'nitration':('16.2 · Electrophilic aromatic substitution','16-2-other-aromatic-substitutions'),
 'esterification':('21.3 · Reactions of carboxylic acids','21-3-reactions-of-carboxylic-acids'),
 'imine':('19.8 · Imine and enamine formation','19-8-nucleophilic-addition-of-amines-imine-and-enamine-formation'),
 'aldolcond':('23.3 · Dehydration of aldol products','23-3-dehydration-of-aldol-products-synthesis-of-enones'),
 'epoxideacid':('18.5 · Epoxide ring opening','18-5-reactions-of-epoxides-ring-opening'),
}
sources={k:{'title':v[0],'url':BASE+v[1],'publisher':'John McMurry / OpenStax','checked':'2026-10-12'} for k,v in sources.items()}
sources['tst']={'title':'IUPAC Gold Book · Transition state theory','url':'https://goldbook.iupac.org/terms/view/T06470','publisher':'IUPAC','checked':'2026-10-12'}
sources.update({
 'e1cb':{'title':'LibreTexts · E1 and E1cB mechanisms','url':'https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_(Morsch_et_al.)/11%3A_Reactions_of_Alkyl_Halides-_Nucleophilic_Substitutions_and_Eliminations/11.10%3A_The_E1_and_E1cB_Reactions','publisher':'Chemistry LibreTexts','checked':'2026-10-12'},
 'bromination':{'title':'OpenStax · Addition of halogens to alkenes','url':'https://openstax.org/books/organic-chemistry/pages/8-2-addition-of-halogens-to-alkenes','publisher':'John McMurry / OpenStax','checked':'2026-10-12'},
 'halohydrin':{'title':'OpenStax · Halohydrins from alkenes','url':'https://openstax.org/books/organic-chemistry/pages/8-3-halohydrins-from-alkenes-addition-of-ho-x','publisher':'John McMurry / OpenStax','checked':'2026-10-12'},
 'nitration':{'title':'OpenStax · Electrophilic aromatic substitution','url':'https://openstax.org/books/organic-chemistry/pages/16-2-other-aromatic-substitutions','publisher':'John McMurry / OpenStax','checked':'2026-10-12'},
 'esterification':{'title':'OpenStax · Fischer esterification','url':'https://openstax.org/books/organic-chemistry/pages/21-3-reactions-of-carboxylic-acids','publisher':'John McMurry / OpenStax','checked':'2026-10-12'},
 'imine':{'title':'Chemistry LibreTexts · Imine and enamine formation','url':'https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_(Morsch_et_al.)/19%3A_Aldehydes_and_Ketones-_Nucleophilic_Addition_Reactions/19.08%3A_Nucleophilic_Addition_of_Amines_-_Imine_and_Enamine_Formation','publisher':'Chemistry LibreTexts','checked':'2026-10-12'},
 'aldolcond':{'title':'Chemistry LibreTexts · Dehydration of aldol products','url':'https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_(OpenStax)/23%3A_Carbonyl_Condensation_Reactions/23.03%3A_Dehydration_of_Aldol_Products_-_Synthesis_of_Enones','publisher':'Chemistry LibreTexts','checked':'2026-10-12'},
 'epoxideacid':{'title':'OpenStax · Acid-catalyzed epoxide ring opening','url':'https://openstax.org/books/organic-chemistry/pages/18-5-reactions-of-epoxides-ring-opening','publisher':'John McMurry / OpenStax','checked':'2026-10-12'},
})
sources['qc_sn2']={'title':'Kubelka & Bickelhaupt · Activation Strain Analysis of SN2 Reactions at C, N, O, and F Centers','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC5330660/','publisher':'Journal of Physical Chemistry A (2017), 121, 885–891 · doi:10.1021/acs.jpca.6b12240','checked':'2026-10-13'}
sources['qc_coupling_method']={'title':'Cave & Newton · Generalized Mulliken–Hush electronic coupling','url':'https://doi.org/10.1016/0009-2614(95)01310-5','publisher':'Chemical Physics Letters (1996), 249, 15–19','checked':'2026-10-13'}
sources['qc_da_ion']={'title':'Vermeeren et al. · How Ionization Catalyzes Diels–Alder Reactions','url':'https://doi.org/10.1002/chem.202200987','publisher':'Chemistry – A European Journal (2022) · doi:10.1002/chem.202200987','checked':'2026-10-13'}
sources['qc_competition']={'title':'Wu, Bickelhaupt & Xie · Solvent-induced dual nucleophiles and the α-effect in SN2 versus E2 competition','url':'https://doi.org/10.1039/D4CP00671B','publisher':'Physical Chemistry Chemical Physics (2024) · doi:10.1039/D4CP00671B','checked':'2026-10-13'}
sources['qc_borderline']={'title':'Exploring borderline SN1–SN2 mechanisms: explicit solvation of isopropyl chloride','url':'https://doi.org/10.1039/D4RA00066H','publisher':'RSC Advances (2024) · doi:10.1039/D4RA00066H','checked':'2026-10-13'}
sources['qc_attack_angle']={'title':'Unraveling the Bürgi–Dunitz Angle with Precision: A Two-Dimensional Energy Decomposition Analysis','url':'https://doi.org/10.1021/acs.jctc.3c00907','publisher':'Journal of Chemical Theory and Computation (2023) · doi:10.1021/acs.jctc.3c00907','checked':'2026-10-13'}
sources['qc_claisen_elf']={'title':'A bonding evolution analysis for the thermal Claisen rearrangement','url':'https://doi.org/10.1039/C7CP07557J','publisher':'Physical Chemistry Chemical Physics (2018) · doi:10.1039/C7CP07557J','checked':'2026-10-13'}
sources['qc_nitration_solvent']={'title':'Nakatani et al. · Solvation in nitration of benzene and the valence electronic structure of the Wheland intermediate','url':'https://doi.org/10.1039/D2CP01699K','publisher':'Physical Chemistry Chemical Physics (2022) · doi:10.1039/D2CP01699K','checked':'2026-10-13'}

axes=[
 {'key':'S','name':'电子态','en':'Electronic state','question':'以什么电子态参与？','values':{'1':'闭壳层 / 成对电子','2':'开壳层 / 自由基','3':'激发态 / 态变换'},'note':'这里按反应事件涉及的电子态标记；S2 不表示产物一定仍是自由基。S3 与 S1/S2 可能重叠。'},
 {'key':'O','name':'轨道相互作用','en':'Orbital interaction','question':'主要的电子相互作用是什么？','values':{'1':'供体—受体','2':'单占轨道参与','3':'协同环状相互作用','4':'电子转移耦合'},'note':'取主要教学描述，不声称唯一轨道分解。O2 与 O4 存在交叉；所有反应都涉及轨道，O3 特指周环式协同。'},
 {'key':'R','name':'键联系变化','en':'Bond reorganization','question':'主要改变了什么联系？','values':{'1':'主要成键 / 断键','2':'联系替换','3':'多键重分布','4':'电子转移'},'note':'记录主要变化，不是完整键变化清单；R1 允许伴随局部 π 键级变化。详细成断键仍需看机理。'},
 {'key':'G','name':'几何变化','en':'Nuclear geometry','question':'原子怎样接近与重排？','values':{'1':'单一接近 / 分离','2':'接近—离去交换','3':'集体几何重排'},'note':'按显著的核几何变化粗分。G3 也可用于羰基平面→四面体的教学描述；这类边界标为候选。'}
]

# The codebook is a project convention, not a claim that a cited textbook uses SORG.
codebook={
 '1111':{'status':'inherited','label':'成键或断键','why':['主要采用闭壳层描述','用供受体或极性键电子对描述','以一项成键 / 断键为主','以接近或分离为主'],'boundary':'SN1 电离沿用原约定：O1 是极性电子对记账，不表示离去时一定存在新的供受体成键。烯烃质子化也沿用原分类，伴随的 π 键变化需另看机理。'},
 '1122':{'status':'inherited','label':'极性联系替换','why':['电子对参与','占据轨道向受体轨道作用','一个联系被另一个取代','接近与离去在同一步耦合'],'boundary':'SN2 与直接质子转移可以同码；编码不区分反应中心是 C 还是 H。'},
 '2211':{'status':'inherited','label':'自由基成键','why':['至少一个开壳层参与者','单占轨道参与','主要形成一项新联系','以反应中心接近为主'],'boundary':'自由基加成可伴随 π 键变为 σ 键；自由基复合最终可得到闭壳层产物。'},
 '1333':{'status':'inherited','label':'周环协同重排','why':['热反应的闭壳层基态模型','环状轨道相互作用','多个键协同重分布','多个反应中心集体变化'],'boundary':'协同不等于同步；相同四位码不能区分环加成、电环化和 σ 迁移，需同时保留反应名称。'},
 '1113':{'status':'candidate','label':'羰基加成 / 消除','why':['闭壳层电子对模型','n 或 σ → π*；逆向过程为羰基恢复','以亲核成键或离去断键为主','羰基中心平面与四面体之间重排'],'boundary':'沿用早期候选值，尚未成为 v0.1 的固定分配。若强调 π 键级变化，R3 也是可讨论的边界。'},
 '1133':{'status':'candidate','label':'极性多键重排','why':['成对电子参与','碱 / 底物的供受体相互作用','C–H、C–X 与 C=C 等联系耦合改变','多个中心需协同调整或形成平面 π 系统'],'boundary':'本站新增的候选编码，用于 E2 及 E1 的烯烃形成步。E2 的协同并不自动意味着 O3 周环反应。'},
 '2222':{'status':'candidate','label':'自由基原子转移','why':['自由基参与','单占轨道与 σ 键相互作用','原子从一个中心转移至另一个中心','接近与离去相耦合'],'boundary':'本站候选，用于 H / 卤原子转移；不是已完成量子化学验证的分类。'}
}

def step(title,code,equation,flow,orbital,geometry,diagram):
 return dict(title=title,code=code,equation=equation,flow=flow,orbital=orbital,geometry=geometry,diagram=diagram)
def pt(eq,flow='碱的孤对电子指向 H；原 H–A 键电子对返回 A。'):
 return step('Proton transfer','1122',eq,flow,'n(base) → σ*(H–A)','接近 H 的同时，原 H–A 联系减弱。','proton')
def ion(eq):
 return step('Heterolytic ionization','1111',eq,'C–X 键的两个电子都归离去基团 X。','σ(C–X) 的电子对随异裂保留在 X','C 与 X 分离，碳正离子中心趋于平面。','ion')
def capture(eq):
 return step('Carbocation capture','1111',eq,'亲核体孤对电子指向带正电的碳，形成新 σ 键。','n(Nu) → p(C⁺)','亲核体接近平面碳正离子的一个面。','capture')
def carbonyl(eq,donor='n(Nu)',flow='亲核体的电子对指向羰基碳，同时 C=O 的 π 电子对移至氧。'):
 return step('Nucleophilic carbonyl addition','1113',eq,flow,donor+' → π*(C=O)','羰基中心由近似平面变为四面体。','carbonyl')
def alkene(eq):
 return step('Alkene protonation','1111',eq,'C=C 的 π 电子对与 H 成键；H–A 键电子对移向 A。','π(C=C) → σ*(H–A)','先形成一条 C–H 键，另一碳成为碳正离子。','alkene')
def eliminate(eq):
 return step('Alkene formation','1133',eq,'碱孤对电子指向 β-H；C–H 键电子对形成邻位 C=C。','n(base) 与 σ(C–H) / p(C⁺) 耦合','形成 π 键的两个碳趋于共平面。','e1')

reactions=[]
def add(id,name,zh,family,equation,conditions,summary,steps,refs,facts,scope,level='基础',note=''):
 reactions.append(dict(id=id,name=name,zh=zh,family=family,equation=equation,conditions=conditions,summary=summary,steps=steps,sources=refs,facts=facts,scope=scope,level=level,note=note,
   mechanismComplete=True,
   mechanismNote='完整路径按此条列明的底物、试剂与工作条件展开；每张卡片给出该步反应式、电子对/单电子移动及生成的中间体。不同条件可能改变机理，边界见范围说明。'))

add('proton-transfer','Proton transfer','直接质子转移','酸碱反应','CH₃CO₂H + CN⁻ ⇌ CH₃CO₂⁻ + HCN','同一溶剂、同一 pKa 标度下讨论平衡。','H 改变连接对象：与 SN2 共享“联系替换”的编码。',[pt('CH₃CO₂H + CN⁻ ⇌ CH₃CO₂⁻ + HCN')],['acid'],[['pKa(CH₃CO₂H)','4.76 · 教材近似值'],['pKa(HCN)','9.31 · 教材近似值'],['K 的模型','10^(9.31 − 4.76) ≈ 3.55 × 10⁴；由两项 pKa 推算，并非实测 K。']], 'pKa 随溶剂、温度与标准态而变；这里用于教材同标度比较。真实溶液可能存在溶剂介导的质子接力。','acid')
add('lewis','Lewis acid–base association','Lewis 酸碱加合','酸碱反应','NH₃ + BF₃ ⇌ H₃N⁺–BF₃⁻','Lewis donor + electron-deficient acceptor','只需形成一个新的供受体联系，不伴随离去基团。',[step('Donor–acceptor bond formation','1111','NH₃ + BF₃ ⇌ H₃N⁺–BF₃⁻','N 的孤对电子指向缺电子的 B。','n(N) → empty p(B)','N 接近 B；B 的配位几何随加合改变。','lewis')],['lewis'],[['Electron accounting','N 提供一对电子；B 接受。'],['Formal charge','形成普通键表示后 N 为 +1、B 为 −1；总电荷仍为 0。']],'G1 是原教学约定中的“主导接近”，并不否认 B 的局部几何改变。')
add('sn2','SN2 substitution','双分子亲核取代','取代反应','HO⁻ + CH₃Br → CH₃OH + Br⁻','以甲基底物示意；溶剂影响亲核性。','成键和断键在同一个 elementary event 中完成。',[step('Backside displacement','1122','HO⁻ + CH₃Br → CH₃OH + Br⁻','O 的孤对电子指向甲基碳；C–Br 键电子对指向 Br。','n(O) → σ*(C–Br)','Nu–C–Br 近似共线，背面进攻。','sn2')],['sn2','sn2scope'],[['Orbital interaction','n(O) donation into σ*(C–Br)'],['Stereochemistry','在手性反应中心发生构型反转；不保证 R 标签一定变成 S。']],'甲基例子本身不手性。空间位阻改变 SN2 与消除两条路径的相对可及性。')
add('williamson','Williamson ether synthesis','Williamson 醚合成','取代反应','CH₃O⁻ + CH₃CH₂Br → CH₃OCH₂CH₃ + Br⁻','预先形成的 alkoxide + primary alkyl halide','换一种亲核体，仍然沿用 SN2 的电子与几何模式。',[step('Alkoxide displacement','1122','CH₃O⁻ + CH₃CH₂Br → CH₃OCH₂CH₃ + Br⁻','烷氧负离子 O 进攻连 Br 的碳，C–Br 键电子对移向 Br。','n(O) → σ*(C–Br)','从离去基团背面接近。','sn2')],['ether'],[['Reaction center','亲核氧形成新的 C–O σ 键。'],['Substrate choice','甲基或较少受阻的一级底物有利于取代。']],'条目从预制烷氧负离子开始；若从醇开始，还须加入生成 alkoxide 的步骤。')
add('sn1-core','SN1: ionization & capture','SN1 核心两步','取代反应','R₃C–X + Nu⁻ → R₃C–Nu + X⁻','能够形成较稳定碳正离子的底物；条件须使电离可行。','以阴离子亲核体作形式模型，展示真正的两步编码。',[ion('R₃C–X → R₃C⁺ + X⁻'),capture('R₃C⁺ + Nu⁻ → R₃C–Nu')],['sn1'],[['Two events','1111 → 1111；同码不意味着同一步。'],['Electronic structure','C–X heterolysis forms a p-like carbocation acceptor orbital.']],'这是核心机理模型，不保证任意 R₃C–X / Nu⁻ 组合都走 SN1；强碱可能引发 E2。',note='若 Nu 是 H₂O 或 ROH，形成 oxonium 后通常还有去质子化。见 SN1 solvolysis 条目。')
add('sn1-water','SN1 solvolysis','SN1 水解完整路径','取代反应','(CH₃)₃CBr + 2 H₂O → (CH₃)₃COH + H₃O⁺ + Br⁻','water / polar protic medium','水进攻后仍须去质子化，不能把氧鎓离子当作中性醇。',[ion('(CH₃)₃CBr → (CH₃)₃C⁺ + Br⁻'),capture('(CH₃)₃C⁺ + H₂O → (CH₃)₃COH₂⁺'),pt('(CH₃)₃COH₂⁺ + H₂O → (CH₃)₃COH + H₃O⁺')],['sn1','e1'],[['Intermediates','Carbocation → oxonium → alcohol。'],['Electronic structure','Nucleophile donation occurs into the vacant p-like orbital; ion pairing can alter the electronic structure.']],'可与 E1 竞争。一般手性 SN1 底物常得到部分消旋，离子对会影响两面的进攻。')
add('hbr','Electrophilic HBr addition','HBr 亲电加成','烯烃反应','CH₃CH=CH₂ + HBr → CH₃CHBrCH₃','极性加成路径；无自由基引发条件。','先生成碳正离子，再由溴离子捕获。',[alkene('CH₃CH=CH₂ + HBr → (CH₃)₂CH⁺ + Br⁻'),capture('(CH₃)₂CH⁺ + Br⁻ → CH₃CHBrCH₃')],['alkene'],[['Regiochemistry','此例主路径给 Markovnikov 加成产物。'],['Key intermediate','Secondary carbocation。']],'不把该机理用于自由基 HBr 加成；在其他底物上碳正离子还可能重排。')
add('hydration','Acid-catalyzed hydration','酸催化烯烃水合','烯烃反应','CH₃CH=CH₂ + H₂O ⇌ (CH₃)₂CHOH','aqueous acid；H₃O⁺ 是催化剂。','三步循环中酸被消耗后再生。',[alkene('CH₃CH=CH₂ + H₃O⁺ → (CH₃)₂CH⁺ + H₂O'),capture('(CH₃)₂CH⁺ + H₂O → (CH₃)₂CHOH₂⁺'),pt('(CH₃)₂CHOH₂⁺ + H₂O → (CH₃)₂CHOH + H₃O⁺')],['hydration'],[['Catalyst balance','H₃O⁺ 在最后一步再生。'],['Regiochemistry','在该底物上形成 2-propanol。']],'过程可逆；该机理与 oxymercuration、hydroboration 不同。不能由四位码直接判断平衡位置。')
add('e2','E2 elimination','双分子消除','消除反应','CH₃CHBrCH₃ + EtO⁻ → CH₂=CHCH₃ + EtOH + Br⁻','strong base；可达到 anti-periplanar 构象。','三个电子对移动相耦合，但按极性消除编码，不归入周环 O3。',[step('Concerted β-elimination','1133','CH₃CHBrCH₃ + EtO⁻ → CH₂=CHCH₃ + EtOH + Br⁻','碱进攻 β-H；C–H 电子对形成 C=C；C–Br 电子对移向 Br。','n(base) → σ*(C–H)，σ(C–H) 与 σ*(C–Br) 耦合','通常偏好 H–C–C–Br anti-periplanar。','e2')],['e2'],[['Orbital interaction','Base lone-pair donation into σ*(C–H) is coupled with σ(C–H) donation into σ*(C–Br).'],['Geometry','The anti-periplanar arrangement aligns the breaking and forming interactions.']],'1133 是本站候选编码。anti 通常更有利，但并非所有底物都绝对禁止 syn 消除。')
add('e1','E1 elimination','单分子消除','消除反应','(CH₃)₃CCl + H₂O → (CH₃)₂C=CH₂ + H₃O⁺ + Cl⁻','polar protic solvent；可与 SN1 竞争。','与 SN1 共用电离步，之后通过脱质子形成 π 键。',[ion('(CH₃)₃CCl → (CH₃)₃C⁺ + Cl⁻'),eliminate('(CH₃)₃C⁺ + H₂O → (CH₃)₂C=CH₂ + H₃O⁺')],['e1'],[['Shared intermediate','E1 and SN1 pathways share the carbocation formed by C–Cl heterolysis.'],['Electronic structure','The β-C–H σ bond donates into the carbocation p orbital as the π bond forms.']],'第二步 1133 为候选。自由碳正离子模型不表示离子对、溶剂笼效应或重排可以忽略。')
add('carbonyl-add','Carbonyl nucleophilic addition','羰基亲核加成事件','羰基反应','R₂C=O + Nu⁻ → R₂C(O⁻)Nu','从亲核体与羰基的反应事件开始。','用同一局部模式理解许多醛、酮反应。',[carbonyl('R₂C=O + Nu⁻ → R₂C(O⁻)Nu')],['carbonyl'],[['Geometry','Trigonal planar → tetrahedral。'],['Electronic change','形成 C–Nu；C=O 的 π 电子对移至氧。']],'1113 是早期候选，不是已定稿的 v0.1 分配。反应最终产物常还需质子化。')
add('hydride','Lithium aluminum hydride reduction','LiAlH₄ 还原酮','羰基反应','(CH₃)₂C=O + LiAlH₄ → (CH₃)₂CHOH (aqueous workup)','LiAlH₄ in dry ether, followed by H₂O work-up.','列出羰基氧配位、Al–H 向羰基碳转移，以及水解释放醇的步骤。',[
 step('Carbonyl coordination to aluminum','1111','(CH₃)₂C=O + AlH₄⁻ ⇌ (CH₃)₂C=O→AlH₄⁻','羰基氧孤对电子配位到缺电子的 Al，为同一铝氢化物上的氢转移预组织反应物。','n(O) → acceptor orbital on Al','O 接近 Al；配位使羰基碳的受体轨道与 Al–H 键取向耦合。','lewis'),
 step('Intracomplex hydride transfer','1113','(CH₃)₂C=O→AlH₄⁻ → [(CH₃)₂CH–O–AlH₃]⁻','Al–H σ 键电子对以氢化物等效体形式转移至羰基碳；C=O π 电子对移至氧并保留 O–Al 联系。','σ(Al–H) → π*(C=O); n(O) → Al','羰基碳由平面 sp² 型转为四面体；形成 C–H 与 O–Al 联系。','carbonyl'),
 step('Aqueous work-up releases the alcohol','1122','[(CH₃)₂CH–O–AlH₃]⁻ + H₂O → (CH₃)₂CHOH + [AlH₃OH]⁻','水向烷氧氧提供质子；水的 O–H 键电子保留在氧上形成 Al–OH，Al–O(alkoxide) 联系断裂并释放醇。','n(O-alkoxide) → σ*(O–H); σ(Al–O) cleavage','质子化与 Al–O 键水解完成工作后处理。','proton')],['hydride'],[['Reagent model','LiAlH₄; the displayed donor is AlH₄⁻.'],['Conditions','Anhydrous ether during reduction; water is introduced only in the work-up.'],['Species','The aluminate is a stoichiometric intermediate, not free H⁻ in solution.']],'此条明确展示单羰基/单氢转移的反应物配合物模型和一个水解后处理事件；LiAlH₄ 实际可连续转移多个氢化物并形成更复杂铝酸盐，需按具体计量与后处理展开。')

add('grignard','Grignard addition to an aldehyde','格氏试剂对醛加成','羰基反应','PhCHO + CH₃MgBr → PhCH(OH)CH₃ (after H₃O⁺ work-up)','CH₃MgBr in dry diethyl ether; H₃O⁺ only after addition.','依次展示醚溶剂中的羰基配位、C–C 成键/O–Mg 键形成，以及酸性后处理。',[
 step('Carbonyl coordination to magnesium','1111','PhCHO + CH₃MgBr ⇌ PhCH=O→MgBrCH₃','羰基氧孤对电子配位至有机镁试剂中的 Mg；乙醚溶剂稳定并配位 Mg 中心。','n(O) → acceptor orbital on Mg','配位使羰基碳受体轨道与 C–Mg 键取向耦合。','lewis'),
 step('Intracomplex carbon transfer','1113','PhCH=O→MgBrCH₃ → PhCH(O–MgBr)CH₃','C–Mg 键电子对转移形成新的 C–C 键；C=O π 电子对移至氧并与 MgBr 结合为镁烷氧化物。','σ(C–Mg) → π*(C=O); n(O) → Mg','醛羰基碳由平面变为四面体；C–C 成键与 O–Mg 配位协同发生。','carbonyl'),
 step('Acidic work-up protonates the magnesium alkoxide','1122','PhCH(O–MgBr)CH₃ + H₃O⁺ → PhCH(OH)CH₃ + MgBr⁺ + H₂O','烷氧氧接受 H₃O⁺ 的质子；O–H 键电子留在水氧，Mg–O 联系解离，释放二级醇。','n(O-alkoxide) → σ*(O–H); σ(Mg–O) cleavage','酸性水处理在 C–C 成键后进行；手性醛可能从两面进攻并形成对映体。','proton')],['hydride'],[['Order of operations','Carbonyl coordination and C–C bond formation precede aqueous acid work-up.'],['Intermediate','The addition product before work-up is a magnesium alkoxide.'],['Stereochemistry','An achiral Grignard reagent attacking planar benzaldehyde gives racemic product in the idealized model.']],'按单体接触配合物与乙醚溶剂描述教材机理；真实格氏试剂可聚集并与醚溶剂配位，具体聚集平衡依浓度、溶剂和温度变化。此记录完整呈现所选接触配合物反应路径，不把后处理提前到 C–C 成键之前。')

add('cyanohydrin','Cyanohydrin formation','氰醇形成','羰基反应','PhCHO + HCN ⇌ PhCH(OH)CN','CN⁻ 催化的教材机理模型。','亲核加成后从 HCN 取质子，同时再生 CN⁻。',[carbonyl('PhCHO + CN⁻ → PhCH(O⁻)CN','n(C of CN⁻)'),pt('PhCH(O⁻)CN + HCN → PhCH(OH)CN + CN⁻')],['cyanohydrin'],[['Catalyst balance','CN⁻ 在加成步消耗，在质子转移步再生。'],['Reversibility','Cyanohydrin formation 是可逆过程。']],'羰基加成 1113 为候选；亲核反应端是 CN⁻ 的碳。非手性环境中此例形成外消旋产物。')
add('acyl','Nucleophilic acyl substitution','亲核酰基取代','羰基反应','CH₃COCl + CH₃O⁻ → CH₃CO₂CH₃ + Cl⁻','acid chloride + alkoxide','总反应是取代，但关键路径是“加成—消除”，与单步 SN2 不同。',[carbonyl('CH₃COCl + CH₃O⁻ → CH₃C(O⁻)(OCH₃)Cl'),step('Tetrahedral intermediate collapse','1113','CH₃C(O⁻)(OCH₃)Cl → CH₃CO₂CH₃ + Cl⁻','O⁻ 的孤对电子恢复 C=O；C–Cl 键电子对移向 Cl。','n(O) 恢复 π(C=O)，与 C–Cl 断裂耦合','四面体中心恢复羰基平面。','collapse')],['acyl'],[['Path','Addition → tetrahedral intermediate → elimination。'],['Coding','1113 → 1113，两个方向不同的事件可同码。']],'两步是常见教学模型；某些底物 / 条件可出现更协同的酰基取代。不能仅凭产物判断 SN2。')
add('epoxide','Basic epoxide opening','碱性条件下环氧开环','取代反应','ethylene oxide + CH₃O⁻ → CH₃OCH₂CH₂O⁻ → CH₃OCH₂CH₂OH','alkoxide attack，随后质子化。','环张力释放伴随局部 SN2 型联系替换。',[step('Ring-opening displacement','1122','ethylene oxide + CH₃O⁻ → CH₃OCH₂CH₂O⁻','亲核 O 进攻环氧碳；该 C–O 环键电子对移到环氧 O。','n(Nu) → σ*(C–O)','背面进攻，环打开。','sn2'),pt('CH₃OCH₂CH₂O⁻ + H₃O⁺ → CH₃OCH₂CH₂OH + H₂O')],['epoxide'],[['Site selectivity','不对称环氧化物在碱性条件下通常于较少受阻的碳被进攻。'],['Stereochemistry','进攻位点发生反转。']],'乙烯氧化物本身对称；酸催化开环的区域选择性不能直接套用此条。')
add('aldol','Aldol addition','羟醛加成','羰基反应','2 CH₃CHO ⇌ CH₃CH(OH)CH₂CHO','base-catalyzed；本条止于 β-hydroxy aldehyde。','先产生 enolate，再形成 C–C 键，最后质子化。',[pt('CH₃CHO + HO⁻ ⇌ enolate + H₂O','碱取走 α-H，C–H 电子留在与羰基共轭的体系中；负电荷由 enolate 离域稳定。'),carbonyl('enolate + CH₃CHO → CH₃CH(O⁻)CH₂CHO','occupied enolate orbital','enolate 的 α-C 形成新 C–C 键；受体羰基的 π 电子移到 O。'),pt('CH₃CH(O⁻)CH₂CHO + H₂O ⇌ CH₃CH(OH)CH₂CHO + HO⁻')],['aldol'],[['Catalyst balance','HO⁻ 在最后一步再生。'],['Addition ≠ condensation','后续脱水会增加新的事件，不能包含在本条三步编码里。']],'enolate 的共振式不算额外反应步骤。第一步的 1122 只记主要质子转移，不涵盖全部离域细节。')
add('radical-add','Radical alkene addition','自由基烯烃加成事件','自由基反应','CH₃• + CH₂=CH₂ → CH₃CH₂CH₂•','开壳层自由基参与。','形成新 σ 键，同时自由基中心转移到烯烃另一端。',[step('Radical addition','2211','CH₃• + CH₂=CH₂ → CH₃CH₂CH₂•','自由基单电子与 π 键中的一个电子形成新键；另一个 π 电子留在另一碳。','SOMO 与 alkene π / π* 相互作用','自由基接近双键的一端。','radical')],['radical'],[['Electron accounting','使用 fishhook arrows 表示单电子移动。'],['Spin','总体系仍为开壳层；不是生成一个游离碳正离子。']],'这里仅为一个链增长事件，不包括引发与终止；半箭头与双电子箭头不能混用。')
add('radical-combine','Radical recombination','自由基复合','自由基反应','CH₃• + •CH₃ → CH₃CH₃','两个相遇且自旋匹配的自由基。','两个单占轨道形成一个电子对，终止自由基链。',[step('Radical coupling','2211','CH₃• + •CH₃ → CH₃CH₃','两个自由基各贡献一个电子，形成新的 C–C σ 键。','SOMO + SOMO → bonding pair','两个反应中心接近。','recombine')],['radical'],[['Event type','Chain termination。'],['S2 meaning','指事件涉及开壳层，不意味着乙烷产物也为开壳层。']],'实际复合受自旋、扩散及溶剂笼影响；不从四位码推导定量物理量。')
add('radical-chain','Radical chlorination: propagation','自由基氯化链传播','自由基反应','CH₄ + Cl₂ → CH₃Cl + HCl','从已有 Cl• 的链传播阶段开始。','两次原子转移构成传播循环，Cl• 在第二步再生。',[step('Hydrogen atom abstraction','2222','Cl• + CH₄ → HCl + CH₃•','Cl 的单电子与 C–H 键的一个电子形成 H–Cl；剩余电子留在 C。','SOMO(Cl) 与 σ(C–H)','Cl 接近 H，C–H 断裂。','hat'),step('Chlorine atom transfer','2222','CH₃• + Cl₂ → CH₃Cl + Cl•','碳自由基与 Cl–Cl 键的一个电子成键；另一个电子留给离去的 Cl。','SOMO(C) 与 σ(Cl–Cl)','碳接近 Cl，Cl–Cl 同时断裂。','hat')],['radical'],[['Cycle','消去两侧 Cl• / CH₃• 后得到净反应。'],['Scope of two codes','只编码传播循环，不声称完整反应只有两步。']],'2222 是候选。引发可涉及光激发与解离，需另标 S3；本版本不强行给其唯一编码。')
add('diels-alder','Diels–Alder cycloaddition','Diels–Alder 环加成','周环反应','1,3-butadiene + ethene → cyclohexene','thermal [4+2] cycloaddition；这是最简结构示例。','一个协同事件重排三个 π 联系，产生六元环。',[step('[4+2] cycloaddition','1333','CH₂=CH–CH=CH₂ + CH₂=CH₂ → cyclohexene','三个电子对绕六中心环状路径重排；形成两条新 C–C σ 键和一条新的 π 键。','diene / dienophile frontier orbitals，六电子环状相互作用','diene 需能取 s-cis；两个端点共同靠近 dienophile。','da')],['da','dastereo'],[['Bond bookkeeping','3 π → 1 π + 2 σ。'],['Stereochemistry','典型热反应为 suprafacial / suprafacial。']],'最简乙烯例子不表示易反应。endo 偏好取决于底物与条件，协同也不保证两个新键完全同步形成。')
add('claisen','Claisen rearrangement','Claisen 重排','周环反应','CH₂=CH–O–CH₂–CH=CH₂ → OHC–CH₂–CH₂–CH=CH₂','thermal [3,3]-sigmatropic rearrangement','断开一条 σ 键、形成另一条 σ 键，π 联系同时移动。',[step('[3,3]-Sigmatropic rearrangement','1333','allyl vinyl ether → pent-4-enal','通过六中心路径：O–allyl σ 键断裂，两个 π 键迁移并形成新 C–C 联系。','六电子环状 orbital overlap','常用 chair-like transition structure 理解构象选择。','cyclic')],['claisen'],[['Product','Allyl vinyl ether gives a γ,δ-unsaturated carbonyl。'],['Shared code','与 Diels–Alder 同为 1333，但成断键拓扑不同。']],'Claisen rearrangement 与 Claisen condensation 不是同一反应。chair-like 是常见模型，不是所有底物的唯一构象。')
add('electrocyclic','Thermal electrocyclic closure','热电环化','周环反应','1,3-butadiene ⇌ cyclobutene','thermal 4π electrocyclic event','共轭体系两个末端成键，π 键数改变。',[step('4π electrocyclic closure','1333','1,3-butadiene ⇌ cyclobutene','共轭 π 电子重排，末端之间形成新的 σ 键。','4π frontier-orbital symmetry','热 4π 体系采用 conrotatory 模式。','electro')],['electro'],[['Selection rule','Thermal 4π: conrotatory；thermal 6π: disrotatory。'],['Orbital symmetry','Thermal 4π: conrotatory; thermal 6π: disrotatory.']],'本条仅热反应；光化学激发可能改变规则，需要 S3，并超出首版固定编码。')

# Added core reactions. Every discrete proton transfer, bond-forming event, and
# leaving-group step is represented separately so the displayed path is complete.
add('e1cb-dehydration','E1cB dehydration','E1cB 型脱水','消除反应','CH₃COCH₂C(OH)(CH₃)₂ ⇌ CH₃COCH=C(CH₃)₂ + H₂O','以二丙酮醇在碱性条件下脱水生成 mesityl oxide 为结构模型。','先形成共振稳定的 enolate，再消除 β-OH；不把它画成一步 E2。',[
 step('α-Deprotonation to the enolate','1122','CH₃COCH₂C(OH)(CH₃)₂ + HO⁻ ⇌ CH₃COCH⁻C(OH)(CH₃)₂ + H₂O','HO⁻ 的孤对电子指向羰基 α-H；C–H 键电子对留在 α-C，并与 C=O 共轭，enolate 可由氧负离子共振式表示。','n(O) → σ*(C–H); σ(C–H) → π-system','先生成可离域稳定的共轭碱；这一步先于离去基团脱离。','e1'),
 step('E1cB elimination of hydroxide','1133','CH₃COCH⁻C(OH)(CH₃)₂ → CH₃COCH=C(CH₃)₂ + HO⁻','enolate 的 α-C 电子形成 Cα=Cβ；Cβ–O 键电子对移至氧，羟基以 HO⁻ 离去。','enolate HOMO → σ*(Cβ–O)','Cα 与 Cβ 建立 π 键，离去与成键在第二个独立事件中发生。','e1')],['e1cb','aldolcond'],[['Key distinction','E1cB = deprotonation first, leaving-group loss second.'],['Product','Mesityl oxide is the conjugated enone.']],'这是以二丙酮醇为底物的碱促 E1cB 模型；脱水路径随取代基、溶剂和碱而变化。OH⁻ 是差离去基团，先形成稳定共轭碱是该路径的关键。')

add('alkene-bromination','Bromination of an alkene','烯烃溴化','烯烃反应','CH₂=CH₂ + Br₂ → BrCH₂CH₂Br','Br₂ in an inert solvent; no water or alcohol as competing nucleophile.','先形成桥式溴鎓离子，再由 Br⁻ 从背面开环，得到 anti 加成产物。',[
 step('Bromonium-ion formation','1133','CH₂=CH₂ + Br₂ → [CH₂–Br⁺–CH₂] + Br⁻','烯烃 π 键进攻 Br₂ 的一个 Br；Br–Br 键电子对移向另一 Br；被进攻的 Br 的孤对电子同时与另一烯碳成键，得到三元环溴鎓离子。','π(C=C) → σ*(Br–Br), n(Br) → p(C)','两个 C–Br 联系桥接同一 Br；不是游离碳正离子。','alkene'),
 step('Backside bromide ring opening','1122','[CH₂–Br⁺–CH₂] + Br⁻ → BrCH₂CH₂Br','Br⁻ 从桥式 Br 的背面进攻一个碳；被进攻碳与桥式 Br 的 C–Br 键电子对回到 Br，打开三元环。','n(Br⁻) → σ*(C–Br)','背面开环使两个 Br 反面加入；环状中间体被解除。','sn2')],['bromination'],[['Intermediate','Cyclic bromonium ion, not a free carbocation.'],['Stereochemistry','Anti addition; a cyclic alkene gives trans vicinal dibromide.']],'乙烯模型用于显示完整电子步骤；环状、不对称或取代烯烃需额外标注构象、区域选择性及立体化学。第一步的编码为候选扩展。')

add('halohydrin','Halohydrin formation','卤代醇形成','烯烃反应','CH₃CH=CH₂ + Br₂ + H₂O → BrCH₂CH(OH)CH₃ + HBr','Br₂ in water; water is the competing nucleophile and solvent.','桥式溴鎓离子形成后，水优先从较取代端背面进攻；随后去质子化。',[
 step('Bromonium-ion formation','1133','CH₃CH=CH₂ + Br₂ → [CH₃CH–CH₂–Br]⁺ + Br⁻','C=C π 电子进攻 Br₂；Br–Br 键电子对给 Br⁻；桥式 Br 的孤对电子与第二个烯碳成键，得到溴鎓离子。','π(C=C) → σ*(Br–Br), n(Br) → p(C)','烯烃两个碳被桥式 Br 连结。','alkene'),
 step('Water opens the bromonium ion','1122','[CH₃CH–CH₂–Br]⁺ + H₂O → BrCH₂CH(OH₂⁺)CH₃','水的氧孤对电子从背面进攻较取代的碳；该碳与桥式 Br 的键电子对移至 Br，产生 oxonium。','n(O) → σ*(C–Br)','背面进攻与桥断裂同时发生；形成 anti 的 C–O 与 C–Br 关系。','sn2'),
 pt('BrCH₂CH(OH₂⁺)CH₃ + H₂O ⇌ BrCH₂CH(OH)CH₃ + H₃O⁺','另一分子水从 O–H 取质子，O–H 键电子留在产物氧；酸性介质中也可由 Br⁻ 接受该质子。')],['halohydrin'],[['Regioselectivity','Water attacks the more substituted bromonium carbon in the standard aqueous model.'],['Stereochemistry','Anti addition through backside opening.']],'产物为 1-bromopropan-2-ol；图示结构式按骨架方向书写，区域选择性与背面进攻是两条独立判断。以水为大量溶剂时，净计量式还可写成 HBr。')

add('nitration-benzene','Nitration of benzene','苯的硝化','芳香取代','C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O','concentrated HNO₃ / H₂SO₄; electrophile is NO₂⁺.','完整列出硝鎓离子生成、σ-complex 形成与去质子化恢复芳香性的步骤。',[
 pt('HNO₃ + H₂SO₄ ⇌ H₂NO₃⁺ + HSO₄⁻','硫酸向硝酸氧原子供质子；硝酸 O–H 键电子回到氧。'),
 step('Nitronium-ion formation','1111','H₂NO₃⁺ → NO₂⁺ + H₂O','质子化羟基上的 N–O 键电子对随水离去；形成线性 NO₂⁺ 电亲体。','σ(N–OH₂⁺) cleavage; nitronium π system forms','脱水产生的 NO₂⁺ 是芳香亲电取代的实际电亲试剂。','collapse'),
 step('Aromatic attack and σ-complex formation','1133','C₆H₆ + NO₂⁺ → [C₆H₆NO₂]⁺','苯环 π 电子对进攻 N，形成 C–N σ 键；芳香 π 系统转成可由多个环碳共振稳定的 arenium ion。','π(arene) → acceptor orbital of NO₂⁺','被进攻碳暂时转为 sp³；此中间体已失去芳香稳定。','carbonyl'),
 step('Deprotonation restores aromaticity','1133','[C₆H₆NO₂]⁺ + HSO₄⁻ → C₆H₅NO₂ + H₂SO₄','HSO₄⁻ 移走连硝基碳上的 H；C–H 键电子回到环中形成 π 键，恢复芳香性并再生 H₂SO₄。','n(HSO₄⁻) → σ*(C–H); σ(C–H) → aromatic π','恢复平面共轭芳香环。','e1')],['nitration'],[['Electrophile','Nitronium ion, NO₂⁺, generated by the acid mixture.'],['Aromaticity','Lost in the σ-complex step and restored by deprotonation.']],'此条是苯硝化的完整教材机理模型。取代苯会影响定位与反应路径；强酸生成电亲体的具体平衡依水含量而变。芳香进攻/去质子化的 SORG 值为候选。')

add('fischer-esterification','Fischer esterification','Fischer 酯化','羰基反应','CH₃CO₂H + CH₃CH₂OH ⇌ CH₃CO₂CH₂CH₃ + H₂O','acid-catalyzed; water removal or alcohol excess can shift the equilibrium.','完整经历羰基质子化、醇加成、质子转移、脱水与去质子化；不是一步“酸和醇结合”。',[
 pt('CH₃C(=O)OH + H₃O⁺ ⇌ CH₃C(=OH⁺)OH + H₂O','羰基氧接受质子，增强羰基碳的亲电性。'),
 carbonyl('CH₃C(=OH⁺)OH + HOCH₂CH₃ → CH₃C(OH)(OH)(O⁺HCH₂CH₃)','n(OEtOH)','乙醇氧孤对电子进攻羰基碳；C=O π 电子转移至原羰基氧，形成四面体 oxonium 中间体。'),
 pt('CH₃C(OH)(OH)(O⁺HCH₂CH₃) ⇌ CH₃C(OH)(OH₂⁺)(OCH₂CH₃)','溶剂介导质子转移，将一个 OH 转成较好的离去基团 H₂O，并使乙氧基氧中性。'),
 step('Collapse of the tetrahedral intermediate','1113','CH₃C(OH)(OH₂⁺)(OCH₂CH₃) → CH₃C(=OH⁺)OCH₂CH₃ + H₂O','另一羟基氧的孤对电子重建 C=O；C–OH₂⁺ 键电子对随水离去。','n(O) → π*(C–O); σ(C–OH₂⁺) cleavage','四面体中心恢复平面羰基结构，生成质子化酯。','collapse'),
 pt('CH₃C(=OH⁺)OCH₂CH₃ + H₂O ⇌ CH₃CO₂CH₂CH₃ + H₃O⁺','水夺取羰基氧上的质子，酸催化剂再生。')],['esterification'],[['Path type','Acid-catalyzed nucleophilic acyl substitution with a tetrahedral intermediate.'],['Equilibrium','The reaction is reversible; water removal or excess alcohol favors ester.']],'这里把溶剂参与的质子接力写成一个教学质子转移事件；微观上可能由多分子水/醇接力。氧交换与平衡同位素标记不在本站 SORG 主线中展开。')

add('imine-formation','Imine formation from a ketone','酮生成亚胺','羰基反应','(CH₃)₂C=O + CH₃NH₂ ⇌ (CH₃)₂C=NCH₃ + H₂O','mild acid catalysis; avoid strongly acidic conditions that fully protonate the amine.','羰基质子化后胺加成形成 carbinolamine，经质子转移、失水成 iminium，最后去质子化。',[
 pt('(CH₃)₂C=O + H₃O⁺ ⇌ (CH₃)₂C=OH⁺ + H₂O','酸活化羰基；过强酸会使胺失去亲核性。'),
 carbonyl('(CH₃)₂C=OH⁺ + CH₃NH₂ → (CH₃)₂C(OH)(NH₂CH₃)⁺','n(N)','甲胺 N 孤对电子进攻羰基碳，C=O π 电子移至氧，形成 carbinolammonium。'),
 pt('(CH₃)₂C(OH)(NH₂CH₃)⁺ + H₂O ⇌ (CH₃)₂C(OH)(NHCH₃) + H₃O⁺','水夺走氮上的质子，得到中性的 carbinolamine。'),
 pt('(CH₃)₂C(OH)(NHCH₃) + H₃O⁺ ⇌ (CH₃)₂C(OH₂⁺)(NHCH₃) + H₂O','羟基氧质子化为水离去基团。'),
 step('Dehydration to the iminium ion','1113','(CH₃)₂C(OH₂⁺)(NHCH₃) → (CH₃)₂C=NH⁺CH₃ + H₂O','氮孤对电子形成 C=N π 键，同时 C–OH₂⁺ 键断裂，水离去，生成 iminium ion。','n(N) → π*(C–N); σ(C–O) cleavage','C=N 双键形成；离去过程中正电荷保留在亚胺氮/π 系统。','collapse'),
 pt('(CH₃)₂C=NH⁺CH₃ + H₂O ⇌ (CH₃)₂C=NCH₃ + H₃O⁺','水从 N 移走最后一个 N–H 质子，得到中性亚胺并再生酸。')],['imine'],[['Intermediate','Carbinolamine (hemiaminal) → iminium ion → imine.'],['Condition window','Mild acid activates the carbonyl while leaving enough free amine nucleophile.']],'可逆反应；持续移水推动亚胺生成。这里的质子转移用溶剂介导净式表示，不能理解为质子在孤立分子间必然一步直达。',note='亚胺与烯胺形成是不同路径；只有仍有 α-H 的适当羰基底物才可能继续进入烯胺路径。')

add('aldol-condensation','Base-catalyzed aldol condensation','碱催化羟醛缩合','羰基反应','2 (CH₃)₂C=O ⇌ CH₃COCH=C(CH₃)₂ + H₂O','acetone under basic conditions; dehydration gives mesityl oxide.','先经羟醛加成形成 β-hydroxy ketone，再通过 E1cB 脱水；展示加成与缩合的全部五个教学事件。',[
 pt('(CH₃)₂CO + HO⁻ ⇌ CH₃COCH₂⁻ + H₂O','碱夺取 α-H；C–H 键电子进入 enolate 共振体系。'),
 carbonyl('CH₃COCH₂⁻ + (CH₃)₂CO → CH₃COCH₂C(O⁻)(CH₃)₂','occupied enolate orbital','enolate α-C 进攻第二分子丙酮羰基碳；受体 C=O π 电子移到氧。'),
 pt('CH₃COCH₂C(O⁻)(CH₃)₂ + H₂O ⇌ CH₃COCH₂C(OH)(CH₃)₂ + HO⁻','烷氧负离子从水取质子，生成二丙酮醇并再生碱。'),
 pt('CH₃COCH₂C(OH)(CH₃)₂ + HO⁻ ⇌ CH₃COCH⁻C(OH)(CH₃)₂ + H₂O','继续夺取 α-H，生成脱水前的 enolate。'),
 step('E1cB loss of hydroxide','1133','CH₃COCH⁻C(OH)(CH₃)₂ → CH₃COCH=C(CH₃)₂ + HO⁻','α-C 电子形成 Cα=Cβ；β-C–O 键电子移至氧，HO⁻ 离去，形成共轭 enone。','enolate HOMO → σ*(Cβ–O)','形成与羰基共轭的双键，碱在总体循环中再生。','e1')],['aldol','aldolcond'],[['Named intermediates','Enolate → β-hydroxy ketone (diacetone alcohol) → enone (mesityl oxide).'],['Condensation boundary','Dehydration is a distinct E1cB sequence after aldol addition.']],'醛/酮底物、温度和碱性决定停在加成物还是继续脱水；此条针对丙酮自羟醛缩合的标准碱促模型。')

add('acid-epoxide','Acid-catalyzed epoxide opening','酸催化环氧开环','取代反应','propylene oxide + HCl → CH₃CH(Cl)CH₂OH','aqueous acid; chloride is the nucleophile.','先质子化环氧氧，再由 Cl⁻ 背面进攻开环，最后去质子化得到醇。',[
 pt('propylene oxide + H₃O⁺ ⇌ protonated propylene oxide + H₂O','环氧氧接受质子，C–O 键变得更易断裂。'),
 step('Chloride opens the protonated epoxide','1122','protonated propylene oxide + Cl⁻ → CH₃CH(Cl)CH₂OH₂⁺','Cl⁻ 从背面进攻较取代的环氧碳；对应 C–O 环键电子对移至氧，生成 oxonium。','n(Cl⁻) → σ*(C–O); σ(C–O) → O','进攻碳发生反转；环开裂与 C–Cl 成键耦合，反面加成。','sn2'),
 pt('CH₃CH(Cl)CH₂OH₂⁺ + H₂O ⇌ CH₃CH(Cl)CH₂OH + H₃O⁺','水夺取 oxonium 上的质子，生成中性氯代醇并再生酸。')],['epoxideacid','epoxide'],[['Regioselectivity','Acidic opening commonly favors attack at the more substituted carbon; substrate effects matter.'],['Stereochemistry','Backside ring opening gives inversion at the attacked carbon and anti relationship.']],'这里用丙烯氧化物加 HCl 示意。酸性环氧开环带有 SN1-like regioselectivity 与 SN2-like backside stereochemistry；不能简单等同于游离碳正离子路径。')

figures={
 'e1cb-dehydration':{'src':'https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/E1cb-mechanism.svg/1280px-E1cb-mechanism.svg.png','href':'https://commons.wikimedia.org/wiki/File:E1cb-mechanism.svg','alt':'E1cB elimination mechanism','credit':'Matthias M. · Wikimedia Commons · Public domain'},
 'alkene-bromination':{'src':'https://upload.wikimedia.org/wikipedia/commons/3/33/Alkene-bromine-addition-2D-skeletal.png','href':'https://commons.wikimedia.org/wiki/File:Alkene-bromine-addition-2D-skeletal.png','alt':'Bromonium-ion formation and anti opening in alkene bromination','credit':'Benjah-bmm27 · Wikimedia Commons · Public domain'},
 'halohydrin':{'src':'https://upload.wikimedia.org/wikipedia/commons/f/fe/NBS_Bromohydrin_Formation_Scheme.png','href':'https://commons.wikimedia.org/wiki/File:NBS_Bromohydrin_Formation_Scheme.png','alt':'Halohydrin formation scheme','credit':'~K · Wikimedia Commons · Public domain; NBS halohydrin scheme'},
 'nitration-benzene':{'src':'https://upload.wikimedia.org/wikipedia/commons/7/74/Nitration_of_benzene.svg','href':'https://commons.wikimedia.org/wiki/File:Nitration_of_benzene.svg','alt':'Benzene nitration mechanism','credit':'Yikrazuul · Wikimedia Commons · Public domain'},
 'fischer-esterification':{'src':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Fischer_esterification_mechanism.svg/1280px-Fischer_esterification_mechanism.svg.png','href':'https://commons.wikimedia.org/wiki/File:Fischer_esterification_mechanism.svg','alt':'Fischer esterification mechanism','credit':'V8rik · Wikimedia Commons · Public domain'},
 'imine-formation':{'src':'https://upload.wikimedia.org/wikipedia/commons/c/c8/Mechanism_imine_formation_general.svg','href':'https://commons.wikimedia.org/wiki/File:Mechanism_imine_formation_general.svg','alt':'General imine formation mechanism','credit':'Wikimedia Commons · CC BY-SA 4.0'},
 'aldol-condensation':{'src':'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/E1cB_aldol_condensation.svg/1280px-E1cB_aldol_condensation.svg.png','href':'https://commons.wikimedia.org/wiki/File:E1cB_aldol_condensation.svg','alt':'Aldol addition and E1cB dehydration','credit':'Wikimedia Commons · E1cB aldol-condensation scheme'},
}
for r in reactions:
 if r['id'] in figures:r['figure']=figures[r['id']]

# Reaction-specific mechanism illustrations. Images are embedded in the
# mechanism panel; each caption links to its original educational source.
additional_figures={
 'proton-transfer':{'src':'https://image3.slideserve.com/402313/conjugate-acids-bases7-l.jpg','href':'https://www.slideserve.com/wiley/organic-chemistry-powerpoint-ppt-presentation','alt':'Curved-arrow illustration of a Brønsted acid–base proton transfer','credit':'Brown, Foote & Iverson lecture slide · SlideServe (analogous proton-transfer example)'},
 'lewis':{'src':'https://image2.slideserve.com/4280814/acid-base-concepts-06-l.jpg','href':'https://www.slideserve.com/gittel/chapter-14','alt':'Lewis acid–base adduct formation between ammonia and boron trifluoride','credit':'Aqueous equilibria lecture slide · SlideServe'},
 'sn2':{'src':'https://kpu.pressbooks.pub/app/uploads/sites/139/2020/12/Sn2-mechanism-1024x480.png','href':'https://kpu.pressbooks.pub/organicchemistry/chapter/7-2/','alt':'Complete SN2 backside-attack mechanism with curved arrows','credit':'KPU Pressbooks · Organic Chemistry'},
 'williamson':{'src':'https://www.chemistrysteps.com/wp-content/uploads/2022/11/Williamson-Ether-Synthesis-some-examples.png','href':'https://www.chemistrysteps.com/williamson-ether-synthesis/','alt':'Williamson ether synthesis by an alkoxide SN2 displacement','credit':'Chemistry Steps · Williamson Ether Synthesis'},
 'sn1-core':{'src':'https://ncstate.pressbooks.pub/app/uploads/sites/52/2023/11/image30-11.jpeg','href':'https://ncstate.pressbooks.pub/organicchem/chapter/the-sn1-reaction/','alt':'SN1 ionization, carbocation capture by water, and oxonium deprotonation','credit':'OpenStax adaptation · NC State Pressbooks'},
 'sn1-water':{'src':'https://ncstate.pressbooks.pub/app/uploads/sites/52/2023/11/image30-11.jpeg','href':'https://ncstate.pressbooks.pub/organicchem/chapter/the-sn1-reaction/','alt':'Three-step SN1 solvolysis of tert-butyl bromide in water','credit':'OpenStax adaptation · NC State Pressbooks'},
 'hbr':{'src':'https://oss.linstitute.net/wechatimg/2022/07/3.2-Hydrocarbons-Electrophilic-Addition-HBr-1.png','href':'https://www.linstitute.net/','alt':'Electrophilic addition of HBr to an alkene through a carbocation','credit':'Organic chemistry teaching diagram · HBr addition'},
 'hydration':{'src':'https://d3nzlfkeryzt6j.cloudfront.net/fc3m8degkaatqcczbt0mk27e0n4k','href':'https://app.medify.co/a-level-chemistry-ocr/study-notes/articles/85-alkenes-4-1-3','alt':'Three-step acid-catalyzed hydration of propene to propan-2-ol','credit':'Medify · Alkene hydration mechanism'},
 'e2':{'src':'https://image4.slideserve.com/1012269/electron-rich-to-electron-poor-sites-and-e2-steps-l.jpg','href':'https://www.slideserve.com/caressa/chapter-7-alkyl-halides-and-nu-substitution','alt':'Concerted E2 beta-elimination with curved arrows','credit':'Organic chemistry lecture slide · SlideServe'},
 'e1':{'src':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/E1-mechanism.svg/1280px-E1-mechanism.svg.png','href':'https://commons.wikimedia.org/wiki/File:E1-mechanism.svg','alt':'Two-step E1 elimination: ionization followed by beta-deprotonation','credit':'Wikimedia Commons · E1-mechanism.svg'},
 'carbonyl-add':{'src':'https://www.chem.ucla.edu/~harding/IGOC/N/nucleophilic_addition01.png','href':'https://www.chem.ucla.edu/~harding/IGOC/N/nucleophilic_addition01.html','alt':'Nucleophilic addition to a carbonyl followed by protonation','credit':'UCLA Illustrated Glossary of Organic Chemistry'},
 'hydride':{'src':'https://image3.slideserve.com/6508687/reduction-of-carbonyls1-l.jpg','href':'https://www.slideserve.com/brooke-stafford/alcohols','alt':'Hydride addition to a carbonyl followed by aqueous protonation','credit':'Organic chemistry lecture slide · SlideServe'},
 'grignard':{'src':'https://ncstate.pressbooks.pub/app/uploads/sites/52/2023/11/image42-21.jpeg','href':'https://ncstate.pressbooks.pub/organicchem/chapter/nucleophilic-addition-of-hydride-and-grignard-reagents-alcohol-formation-3/','alt':'Grignard coordination, carbonyl addition, and aqueous work-up','credit':'OpenStax adaptation · NC State Pressbooks'},
 'cyanohydrin':{'src':'https://image1.slideserve.com/2870845/draw-the-mechanism-for-the-reaction-of-hydrogen-cyanide-and-ethanal-l.jpg','href':'https://www.slideserve.com/jalen/carbonyl-compounds','alt':'Cyanide addition to a carbonyl and proton transfer regenerating cyanide','credit':'Organic chemistry lecture slide · SlideServe'},
 'acyl':{'src':'https://ncstate.pressbooks.pub/app/uploads/sites/52/2023/11/image167-5.jpeg','href':'https://ncstate.pressbooks.pub/organicchem/chapter/21-2-nucleophilic-acyl-substitution-reactions/','alt':'Addition–elimination mechanism for nucleophilic acyl substitution','credit':'OpenStax adaptation · NC State Pressbooks'},
 'epoxide':{'src':'https://image1.slideserve.com/2027597/reactions-of-epoxides-base-catalyzed-ring-opening1-l.jpg','href':'https://www.slideserve.com/luyu/ethers','alt':'Base-promoted SN2 epoxide opening followed by protonation','credit':'Organic chemistry lecture slide · SlideServe'},
 'aldol':{'src':'https://images.squarespace-cdn.com/content/v1/62185f3b81809a6fd03ddbb5/134a326b-e67c-4496-afd6-a087e976360e/Ketone_aldol%2Bcopy.png','href':'https://www.makingmolecules.com/','alt':'Enolate formation, carbonyl addition, and proton transfer in an aldol addition','credit':'Making Molecules · Aldol addition mechanism'},
 'radical-add':{'src':'https://cf.ppt-online.org/files/slide/w/WV2FQO8BaH07nouxhEfp5Rt6SmLZezKCUrPTIJ/slide-5.jpg','href':'https://ppt-online.org/215280','alt':'Free-radical addition to an alkene during chain propagation','credit':'Edexcel organic reaction mechanisms slide · PPT Online'},
 'radical-combine':{'src':'https://image3.slideserve.com/6885036/slide9-l.jpg','href':'https://www.slideserve.com/armando-lopez/acids-and-bases','alt':'Fish-hook arrows illustrating radical recombination','credit':'Organic chemistry lecture slide · SlideServe'},
 'radical-chain':{'src':'https://image.slidesharecdn.com/halogenationofalkanes-180702090250/75/Halogenation-of-alkanes-5-2048.jpg','href':'https://www.slideshare.net/slideshow/halogenation-of-alkanes/103920966','alt':'Two propagation steps in radical chlorination with fish-hook arrows','credit':'Organic chemistry lecture slide · SlideShare'},
 'diels-alder':{'src':'https://www.chemistrylearner.com/wp-content/uploads/2020/01/Diels-Alder-Reaction-Mechanism.jpg','href':'https://www.chemistrylearner.com/diels-alder-reaction.html','alt':'Concerted six-electron Diels–Alder cycloaddition mechanism','credit':'Chemistry Learner · Diels–Alder reaction'},
 'claisen':{'src':'https://image.slideserve.com/392337/mechanism-4-claisen-rearrangement-l.jpg','href':'https://www.slideserve.com/asasia/ch-18-ethers-and-epoxides','alt':'Six-membered transition-state electron flow in the Claisen rearrangement','credit':'Organic chemistry lecture slide · SlideServe'},
 'electrocyclic':{'src':'https://www.stereoelectronics.org/webPR/images_PR/4042.png','href':'https://www.stereoelectronics.org/webPR/PR_04.html','alt':'Thermal conrotatory electrocyclic closure of a 4π diene','credit':'Stereoelectronics · Pericyclic reaction orbital symmetry'},
 'acid-epoxide':{'src':'https://www.chemistrysteps.com/wp-content/uploads/2024/11/Epoxide-Reactions-under-Acidic-and-Basic-Conditions-768x821.png','href':'https://www.chemistrysteps.com/reactions-of-epoxides-under-acidic-and-basic-conditions/','alt':'Acid-catalyzed epoxide protonation and chloride ring opening','credit':'Chemistry Steps · Epoxide ring-opening mechanisms'}
}
figures.update(additional_figures)
for r in reactions:
    if r['id'] in additional_figures:r['figure']=additional_figures[r['id']]

# Reaction-appropriate electronic-structure observables. These are analysis
# targets, not fabricated computed values. The SN2 literature case is a related
# benchmark with a different substrate/nucleophile from the teaching card.
qc_targets={
 '酸碱反应':['同一溶剂和构象下的电荷/电子密度变化','供体—受体轨道能量与 NBO 二阶相互作用（注明分区方案）'],
 '取代反应':['反应坐标上的 ΔE_strain / ΔE_interaction','EDA 的 Pauli、静电、轨道项及 σ*(C–LG) 能量'],
 '消除反应':['E2 反应坐标与 ΔE_strain / ΔE_interaction','σ(C–H) / σ*(C–LG) 轨道作用与几何扭转扫描'],
 '烯烃反应':['沿反应坐标的电荷转移与前线轨道能级','关键中间体/过渡态的电子密度与键级'],
 '羰基反应':['供体 HOMO—受体 LUMO 能隙及轨道作用能','羰基碳电荷、C–O/C–Nu 键级与反应坐标'],
 '周环反应':['前线轨道相位/系数与对称允许性','沿协同反应坐标的键级演化和轨道相互作用能'],
 '自由基反应':['自旋密度/自旋布居与 SOMO 系数','断键/成键坐标上的自旋态及键级变化'],
 '芳香取代':['芳香 π 轨道系数及亲电体—芳环相互作用','σ-complex 的电荷/自旋密度与芳香性指标'],
}
for r in reactions:
    r['quantumData']={'status':'not-yet-computed','descriptors':qc_targets.get(r['family'],['电子密度/电荷分布','轨道作用与键级沿反应坐标的变化']),
                      'note':'本站尚无此条具体底物与条件的量子化学计算值；此处列出适配的待测量，不是结果。'}
families_en={'酸碱反应':'Acid–base reactions','取代反应':'Substitution reactions','烯烃反应':'Alkene reactions','消除反应':'Elimination reactions','羰基反应':'Carbonyl reactions','自由基反应':'Radical reactions','周环反应':'Pericyclic reactions','芳香取代':'Aromatic substitution'}
axes_en=[
 {'key':'S','name':'Electronic state','en':'Electronic state','question':'Which electronic state participates?','values':{'1':'Closed shell / electron pairs','2':'Open shell / radicals','3':'Excited state / state change'},'note':'Codes describe the electronic state involved in an event; S2 does not imply that the product remains a radical. S3 may overlap with S1 or S2.'},
 {'key':'O','name':'Orbital interaction','en':'Orbital interaction','question':'What is the dominant electronic interaction?','values':{'1':'Donor–acceptor','2':'Singly occupied orbital participation','3':'Concerted cyclic interaction','4':'Electron-transfer coupling'},'note':'This is a teaching-level description, not a unique orbital decomposition. O2 and O4 can overlap; all reactions involve orbitals, while O3 specifically denotes pericyclic concerted interaction.'},
 {'key':'R','name':'Bond reorganization','en':'Bond reorganization','question':'What changes in bonding are most prominent?','values':{'1':'Principal bond formation / cleavage','2':'Bond replacement','3':'Multiple-bond reorganization','4':'Electron transfer'},'note':'This records the principal change, not a complete bond-change inventory. R1 can include local π-bond-order changes; consult the mechanism for detailed bond making and breaking.'},
 {'key':'G','name':'Nuclear geometry','en':'Nuclear geometry','question':'How do atoms approach and reorganize?','values':{'1':'Single approach / separation','2':'Approach–departure exchange','3':'Collective geometric reorganization'},'note':'A coarse grouping of prominent nuclear motion. G3 can also describe the planar-to-tetrahedral carbonyl change as a teaching model; such boundaries are candidates.'}
]
codebook_en={
 '1111':('Bond formation or cleavage',['Closed-shell description','Donor–acceptor or polar-bond electron-pair model','One principal bond formed or broken','Approach or separation dominates'],'For SN1 ionization, O1 follows the project convention for polar electron-pair bookkeeping; it does not claim a new donor–acceptor bond forms during departure. Alkene protonation follows the same inherited convention; inspect the mechanism for the accompanying π-bond change.'),
 '1122':('Polar bond replacement',['Electron pairs participate','Occupied orbital donates into an acceptor orbital','One bond is replaced by another','Approach and departure are coupled in one event'],'SN2 and direct proton transfer can share this code; the code does not distinguish a carbon from a hydrogen reaction center.'),
 '2211':('Radical bond formation',['At least one open-shell participant','Singly occupied orbitals participate','One principal new bond forms','Approach at the reaction center dominates'],'Radical addition can convert a π bond into a σ bond; radical recombination can ultimately yield a closed-shell product.'),
 '1333':('Concerted pericyclic reorganization',['Thermal closed-shell ground-state model','Cyclic orbital interaction','Several bonds reorganize together','Several reaction centers change collectively'],'Concerted does not mean synchronous. This code cannot distinguish cycloaddition, electrocyclization, and σ migration, so retain the reaction name.'),
 '1113':('Carbonyl addition / elimination',['Closed-shell electron-pair model','n or σ donation into π*; reverse process restores the carbonyl','Nucleophilic bond formation or leaving-group cleavage dominates','The carbonyl center changes between planar and tetrahedral geometry'],'This is an early candidate assignment, not a fixed v0.1 code. R3 is another possible boundary when π-bond-order change is emphasized.'),
 '1133':('Polar multiple-bond reorganization',['Electron pairs participate','Donor–acceptor interaction between base and substrate','C–H, C–X, and C=C bonding changes are coupled','Several centers adjust together or form a planar π system'],'A project candidate used for E2 and the alkene-forming E1 event. Concerted E2 chemistry is not automatically a pericyclic O3 reaction.'),
 '2222':('Radical atom transfer',['Radical participation','Singly occupied orbital interacts with a σ bond','An atom transfers between reaction centers','Approach and departure are coupled'],'A project candidate for H- or halogen-atom transfer; this is not a quantum-chemically validated classification.')
}
for i,a in enumerate(axes): axes[i]=axes_en[i]
for c,(label,why,boundary) in codebook_en.items(): codebook[c].update(label=label,why=why,boundary=boundary)
qc_en={
 '酸碱反应':['Charge and electron-density changes in a defined solvent and conformation','Donor–acceptor orbital energies and NBO second-order interactions (with partitioning specified)'],
 '取代反应':['Activation-strain profile (ΔEstrain / ΔEinteraction) along the reaction coordinate','EDA terms (Pauli, electrostatic, orbital) and σ*(C–LG) energy'],
 '消除反应':['E2 reaction coordinate and activation-strain profile','σ(C–H) / σ*(C–LG) interaction and torsional scan'],
 '烯烃反应':['Charge transfer and frontier-orbital energies along the reaction coordinate','Electron density and bond order for key intermediates and transition states'],
 '羰基反应':['Donor HOMO–acceptor LUMO gap and orbital interaction energy','Carbonyl-carbon charge, C–O/C–Nu bond orders, and reaction coordinate'],
 '周环反应':['Frontier-orbital phases/coefficients and symmetry allowance','Bond-order evolution and orbital interaction energy along the concerted coordinate'],
 '自由基反应':['Spin density/population and SOMO coefficients','Spin-state and bond-order changes along bond-breaking/forming coordinates'],
 '芳香取代':['Aromatic π-orbital coefficients and electrophile–arene interaction','Charge/spin density and aromaticity measures for the σ complex']}
for r in reactions:
    r.pop('zh',None)
    if 'level' in r: r['level']='Foundational'
    r['family']=families_en.get(r['family'],r['family'])
    apply_english(r)
    finish_english(r)
    r['mechanismNote']='Follow the specified substrate and conditions through every listed event. Electron arrows and intermediates are described below; solvent-mediated proton transfer may group several microscopic transfers.'
    for field in ('conditions','summary','scope','note'):
        assert not any('\u3400' <= ch <= '\u9fff' for ch in r.get(field,'')), (r['id'],field)
    for st in r['steps']:
        for field in ('flow','orbital','geometry'):
            assert not any('\u3400' <= ch <= '\u9fff' for ch in st[field]), (r['id'],st['title'],field,st[field])
    for fact in r['facts']:
        assert not any('\u3400' <= ch <= '\u9fff' for ch in ' '.join(fact)), (r['id'],fact)
    for j,d in enumerate(r['quantumData'].get('descriptors',[])):
        if any('\u3400' <= ch <= '\u9fff' for ch in d): r['quantumData']['descriptors'][j]=qc_en.get(next((k for k,v in families_en.items() if v==r['family']),''),['Electron density and charge distribution along a defined reaction coordinate','Orbital interaction and bond-order changes']) [min(j,1)]
    if any('\u3400' <= ch <= '\u9fff' for ch in r['quantumData'].get('note','')): r['quantumData']['note']='No reaction-specific quantum-chemical calculation is available for this substrate and condition set. The descriptors above are proposed observables, not calculated results.'
attach_literature(reactions)
apply_review(reactions, sources)
apply_v028(reactions)
apply_v029(reactions,codebook)
payload={'version':'0.3.3','updated':'2026-10-14','axes':axes,'codebook':codebook,'sources':sources,'reactions':reactions}
(ROOT/'dist'/'data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
(ROOT/'dist'/'data.js').write_text('window.SORG = '+json.dumps(payload,ensure_ascii=False)+';\n')
print(f'Created {len(reactions)} reaction records, {sum(len(r["steps"]) for r in reactions)} coded events.')
