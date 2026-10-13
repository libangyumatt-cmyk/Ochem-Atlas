"""English editorial text for the reaction records; ordered flows follow each pathway."""
FLOWS = {
'proton-transfer': ['The cyanide carbon lone pair abstracts the carboxylic-acid proton; the acid O–H bond pair returns to oxygen, yielding acetate and HCN.'],
'lewis': ['The nitrogen lone pair donates to electron-deficient boron, forming the N–B bond and the zwitterionic formal-charge representation.'],
'sn2': ['The hydroxide oxygen lone pair attacks methyl carbon from behind; the C–Br bond pair departs with bromide in the same event.'],
'williamson': ['The methoxide oxygen lone pair attacks the carbon bearing bromine; the C–Br bond pair leaves with bromide in the same event.'],
'sn1-core': ['The C–X bond pair goes to X, producing X⁻ and a carbocation.', 'The nucleophile lone pair attacks the carbocation carbon and forms the new C–Nu σ bond.'],
'sn1-water': ['The C–Br bond pair goes to bromine, producing Br⁻ and tert-butyl cation.', 'Water donates an oxygen lone pair to the carbocation, giving a protonated alcohol (oxonium).', 'A second water molecule removes a proton from oxonium; its O–H bond pair returns to the alcohol oxygen, yielding tert-butanol and H₃O⁺.'],
'hbr': ['The alkene π pair bonds to H while the H–Br bond pair goes to bromide, placing the cation at the more substituted carbon.', 'Bromide donates a lone pair to the secondary carbocation to form C–Br.'],
'hydration': ['The alkene π pair takes H from H₃O⁺; the acid O–H pair returns to water, forming the secondary carbocation.', 'A water oxygen lone pair attacks the carbocation, producing protonated 2-propanol.', 'Water removes the oxonium proton; its O–H pair returns to the alcohol oxygen and H₃O⁺ is regenerated.'],
'e2': ['Ethoxide abstracts a β-H; the C–H pair forms C=C while the C–Br pair goes to Br⁻, all in one concerted event.'],
'e1': ['The C–Cl pair goes to chloride, forming tert-butyl cation.', 'Water removes a β-H; the C–H pair forms the neighboring C=C π bond and H₃O⁺ is produced.'],
'carbonyl-add': ['The nucleophile pair attacks carbonyl carbon while the C=O π pair moves to oxygen, giving tetrahedral alkoxide.'],
'hydride': ['The carbonyl oxygen lone pair coordinates to Al, preorganizing the carbonyl and an Al–H bond.', 'The Al–H bond pair transfers hydride character to carbonyl carbon; the C=O π pair shifts to O and an aluminum alkoxide forms.', 'Water protonates the alkoxide oxygen; hydrolysis breaks the Al–O contact and releases the alcohol.'],
'grignard': ['The aldehyde oxygen coordinates to Mg in the ether-solvated reagent complex.', 'The C–Mg bond pair forms a new C–C bond at carbonyl carbon; the C=O π pair moves to oxygen and a magnesium alkoxide forms.', 'During acidic work-up, alkoxide oxygen takes a proton from H₃O⁺ and the Mg–O contact dissociates, releasing the secondary alcohol.'],
'cyanohydrin': ['The carbon end of CN⁻ attacks carbonyl carbon; the C=O π pair shifts to oxygen, producing the cyano alkoxide.', 'Alkoxide oxygen removes H from HCN; the H–C bond pair returns to carbon to regenerate CN⁻ and form cyanohydrin.'],
'acyl': ['Alkoxide attacks the acyl carbon; the C=O π pair shifts to oxygen, forming a tetrahedral intermediate.', 'The oxyanion lone pair restores C=O while the C–Cl pair leaves with chloride, producing the ester.'],
'epoxide': ['Alkoxide attacks an epoxide carbon from behind; that ring C–O bond pair goes to the epoxide oxygen as the ring opens.', 'The resulting alkoxide takes a proton from water or another specified donor; the donor O–H pair returns to its oxygen.'],
'aldol': ['Base removes an α-H; the C–H electrons enter the delocalized enolate system rather than making a separate intermediate for each resonance form.', 'The enolate α-carbon forms C–C with a second aldehyde carbonyl carbon; its C=O π pair shifts to oxygen.', 'The aldolate oxygen abstracts H from water; the donor O–H pair returns to oxygen, forming β-hydroxy aldehyde and regenerating base.'],
'radical-add': ['One electron from the radical and one alkene π electron form a new σ bond; the other π electron remains at the other alkene carbon as a radical.'],
'radical-combine': ['Each radical center contributes one electron to a new C–C σ bond; this coupling terminates the radical pair.'],
'radical-chain': ['A chlorine radical takes H: its unpaired electron and one C–H electron form H–Cl while the other C–H electron stays at carbon.', 'The carbon radical bonds to one chlorine atom using one electron from Cl–Cl; the other Cl–Cl electron leaves on a new Cl radical.'],
'diels-alder': ['Three electron pairs move around a six-center cyclic path, creating two C–C σ bonds and shifting the remaining π bond within the six-membered ring.'],
'claisen': ['Across a six-center array, the O–allyl σ bond breaks, two π bonds shift, and a new C–C σ bond forms in one [3,3] rearrangement.'],
'electrocyclic': ['The conjugated 4π electrons redistribute as the terminal carbons form a new σ bond under thermal conrotatory motion.'],
'e1cb-dehydration': ['Hydroxide removes the carbonyl α-H; the C–H pair enters the conjugated enolate, also represented by an oxygen-anion resonance contributor.', 'The enolate α-carbon pair forms Cα=Cβ; the β-C–O pair goes to oxygen and HO⁻ leaves in this second event.'],
'alkene-bromination': ['The alkene π pair attacks one Br of Br₂, the Br–Br pair goes to the other Br, and a lone pair on the attached Br bridges the second alkene carbon to form bromonium.', 'Br⁻ attacks a bromonium carbon from behind; that C–Br bridge pair returns to the bridging bromine, opening the ring with anti addition.'],
'halohydrin': ['The alkene π pair attacks Br₂, the Br–Br pair leaves on Br⁻, and attached bromine bridges the second carbon with a lone pair.', 'Water attacks the more substituted bromonium carbon from behind; the broken bridge C–Br pair returns to Br, forming oxonium with anti C–O/C–Br attachment.', 'A second water molecule removes the oxonium proton; the O–H bond pair returns to product oxygen to give the neutral halohydrin.'],
'nitration-benzene': ['A nitric-acid oxygen lone pair takes H from sulfuric acid; the acid O–H pair returns to sulfate.', 'Protonated nitric acid loses water: the N–OH₂ bond breaks and the remaining oxygens form linear NO₂⁺.', 'A benzene π pair attacks nitronium nitrogen to form C–N and an arenium (σ) complex; its resonance contributors are one intermediate.', 'HSO₄⁻ removes H from the substituted ring carbon; the C–H pair restores aromatic π bonding and regenerates H₂SO₄.'],
'fischer-esterification': ['The carbonyl oxygen takes H from acid; the acid X–H bond pair returns to its conjugate base.', 'Ethanol oxygen attacks the activated acyl carbon; the C=O π pair shifts to the original carbonyl oxygen, giving tetrahedral oxonium.', 'Solvent-mediated proton transfers neutralize the ethoxy oxygen and turn one OH group into an H₂O leaving group.', 'The other oxygen lone pair reforms C=O while the C–OH₂ pair leaves with water, producing protonated ester.', 'Water removes the remaining carbonyl-oxygen proton; its O–H pair returns to ester oxygen and acid is regenerated.'],
'imine-formation': ['Acid protonates carbonyl oxygen, increasing electrophilicity; too much acid would suppress amine nucleophilicity.', 'Methylamine nitrogen attacks carbonyl carbon; the C=O π pair goes to oxygen, giving carbinolammonium.', 'Water removes a proton from nitrogen to form neutral carbinolamine.', 'Acid protonates the hydroxyl oxygen so it can leave as water.', 'The nitrogen lone pair makes C=N as the C–OH₂ bond pair leaves with water, forming an iminium ion.', 'Water removes the final N–H proton; the N–H pair returns to nitrogen to form neutral imine and regenerate acid.'],
'aldol-condensation': ['Base removes an acetone α-H, sending the C–H pair into the delocalized enolate system.', 'Enolate α-carbon bonds to a second acetone carbonyl carbon; its C=O π pair moves to oxygen.', 'Alkoxide takes H from water, forming diacetone alcohol and regenerating hydroxide.', 'Base removes another α-H to make the enolate precursor of dehydration.', 'Enolate α-carbon electrons form Cα=Cβ as the β-C–O bond pair leaves with HO⁻, giving conjugated mesityl oxide.'],
'acid-epoxide': ['Epoxide oxygen takes a proton from acid, activating ring C–O bonds for opening.', 'Cl⁻ attacks the more substituted carbon from behind; that ring C–O pair goes to oxygen and the ring opens with inversion at the attacked carbon.', 'Water removes the oxonium proton; its O–H pair returns to product oxygen to give neutral chlorohydrin and regenerate acid.'],
}

SUMMARIES = {
'proton-transfer':'Proton transfer replaces an O–H bond with C–H bonding; it shares a broad 1122 code with SN2.', 'lewis':'A nitrogen lone pair forms one donor–acceptor N–B bond without displacement.',
'sn2':'C–O formation and C–Br cleavage occur together in one backside displacement.', 'williamson':'A preformed alkoxide replaces bromide through a backside SN2 event.',
'sn1-core':'Ionization and nucleophilic capture are distinct events that happen to share the inherited 1111 code.', 'sn1-water':'Ionization, water capture, and oxonium deprotonation produce neutral alcohol.',
'hbr':'Alkene protonation forms a carbocation, then bromide captures it.', 'hydration':'Protonation, water capture, and deprotonation form alcohol and regenerate acid.',
'e2':'Three electron-pair movements couple in a single anti-favored elimination event.', 'e1':'Ionization creates a carbocation shared with SN1; β-deprotonation forms alkene.',
'carbonyl-add':'Nucleophilic attack and C=O π-bond opening produce a tetrahedral alkoxide.', 'hydride':'Carbonyl–aluminum coordination, hydride transfer, and aqueous release yield an alcohol.',
'grignard':'Carbonyl–magnesium association precedes C–C formation and acidic release of alcohol.', 'cyanohydrin':'Cyanide attack gives an alkoxide; protonation from HCN regenerates CN⁻.',
'acyl':'Acyl substitution proceeds through addition and collapse of a tetrahedral intermediate.', 'epoxide':'Backside ring opening makes an alkoxide; protonation completes the alcohol product.',
'aldol':'Enolate formation, carbonyl attack, and protonation yield a β-hydroxy aldehyde.', 'radical-add':'Radical addition makes a σ bond while relocating the unpaired electron.',
'radical-combine':'Two singly occupied centers pair in a σ bond and end a radical chain.', 'radical-chain':'Two atom-transfer propagation events consume and regenerate Cl•.',
'diels-alder':'A concerted six-electron event makes a six-membered ring and a new π bond.', 'claisen':'A six-center [3,3] shift changes one σ bond and two π bonds together.',
'electrocyclic':'Thermal 4π conrotatory closure forms a terminal σ bond.', 'e1cb-dehydration':'A stabilized enolate forms first; hydroxide leaves in a separate elimination event.',
'alkene-bromination':'Bromonium formation followed by backside bromide opening gives anti dibromide.', 'halohydrin':'Bromonium formation, water attack, and deprotonation give an anti halohydrin.',
'nitration-benzene':'Nitronium generation, aromatic attack, and deprotonation restore the aromatic ring.', 'fischer-esterification':'Acid activation, alcohol addition, proton transfers, water loss, and catalyst regeneration form ester.',
'imine-formation':'Amine addition to activated carbonyl, proton transfers, dehydration, and deprotonation form imine.',
'aldol-condensation':'Aldol addition followed by E1cB dehydration gives a conjugated enone.', 'acid-epoxide':'Epoxide protonation, backside chloride opening, and deprotonation give chlorohydrin.'
}

CONDITIONS = {
'proton-transfer':'Compare equilibrium in the same solvent and pKa scale.', 'sn2':'Methyl substrate; nucleophilicity depends on solvent.',
'williamson':'Preformed alkoxide and a primary alkyl bromide.', 'sn1-core':'A substrate and medium that permit carbocation formation; illustrative formal anionic nucleophile.',
'hbr':'Polar addition without radical initiators.', 'hydration':'Aqueous acid; H₃O⁺ is catalytic.', 'e2':'Strong base and access to an anti-periplanar conformation.',
'e1':'Polar protic solvent; SN1 may compete.', 'carbonyl-add':'The entry begins with the nucleophile–carbonyl addition event.', 'cyanohydrin':'Textbook CN⁻-catalyzed pathway with HCN as proton donor.',
'epoxide':'Alkoxide attack followed by protonation.', 'aldol':'Base-catalyzed addition ending at the β-hydroxy aldehyde.',
'radical-add':'An open-shell radical participates in one chain propagation event.', 'radical-combine':'Two radicals meet in a spin-compatible configuration.',
'radical-chain':'Begins with an existing Cl• in the chain propagation phase.', 'diels-alder':'Thermal [4+2] cycloaddition; minimal structural example.',
'e1cb-dehydration':'Base-promoted dehydration of diacetone alcohol to mesityl oxide.'
}

SCOPES = {
'proton-transfer':'pKa depends on solvent, temperature, and standard state; solution proton transfer can involve solvent relays.',
'lewis':'G1 marks the dominant approach but does not exclude local rehybridization at boron.',
'sn2':'Methyl carbon is achiral; hindrance can alter the competition between substitution and elimination.',
'williamson':'This entry starts with preformed alkoxide; starting from alcohol requires a preceding deprotonation.',
'sn1-core':'A formal core model, not a guarantee for every R₃C–X/Nu⁻ pair; strong bases may favor E2.',
'sn1-water':'E1 can compete. Chiral SN1 substrates often partially racemize; ion pairs may bias attack from each face.',
'hbr':'Radical HBr addition follows another pathway; other carbocations can rearrange.',
'hydration':'Reversible and different from oxymercuration and hydroboration; a SORG code does not specify equilibrium position.',
'e2':'1133 is a candidate code. Anti geometry is usually favored, though syn elimination can occur in suitable systems.',
'e1':'The second event has a candidate code; ion pairing, solvent cages, and rearrangement may matter.',
'carbonyl-add':'1113 is a candidate code. Many isolated products require protonation after this local event.',
'hydride':'One carbonyl and one hydride transfer are modeled; LiAlH₄ can transfer further hydrides and form complex aluminates.',
'grignard':'A solvent-coordinated contact-complex model; aggregation depends on concentration, solvent, and temperature. Acid work-up follows C–C formation.',
'cyanohydrin':'The carbon of CN⁻ attacks. The 1113 addition code is a candidate; a prochiral carbonyl gives a racemate in an achiral medium.',
'acyl':'A common addition–elimination model; some substrates/conditions may favor a more concerted path.',
'epoxide':'Ethylene oxide is symmetric; do not transfer its regiochemical behavior directly to acid-catalyzed opening.',
'aldol':'Enolate resonance contributors are not separate reaction steps; the proton-transfer code does not capture all delocalization.',
'radical-add':'One propagation event only; initiation and termination are separate. Fishhook arrows represent single electrons.',
'radical-combine':'Spin, diffusion, and solvent cages matter; the code predicts no quantitative coupling value.',
'radical-chain':'2222 is a candidate. Photochemical initiation would need separate excited-state treatment.',
'diels-alder':'Unactivated ethylene is a minimal illustration, not an assertion of facile reaction; concerted new bonds need not form synchronously.',
'claisen':'Claisen rearrangement differs from Claisen condensation; chair-like geometry is a common model, not unique.',
'electrocyclic':'Thermal pathway only; photochemical rules can differ and require explicit excited-state treatment.',
'e1cb-dehydration':'Base-promoted diacetone-alcohol model; OH⁻ is a poor leaving group, so stabilized conjugate-base formation matters.',
'alkene-bromination':'Ethylene illustrates electron flow. Substituted and cyclic alkenes require additional regio- and stereochemical detail.',
'halohydrin':'Propene yields 1-bromopropan-2-ol; regioselectivity and backside anti addition are separate predictions.',
'nitration-benzene':'A textbook benzene model; substituents change orientation, and electrophile-generation equilibria depend on water content.',
'fischer-esterification':'Solvent-mediated proton relays are grouped as one teaching event; microscopic relays can involve multiple alcohol/water molecules.',
'imine-formation':'Reversible; removing water drives imine formation. Proton transfers can involve solvent relays.',
'aldol-condensation':'Substrate, temperature, and base decide whether addition product persists or dehydration follows.',
'acid-epoxide':'Propylene oxide and HCl illustrate an acid-promoted path with regioselectivity and backside stereochemistry; a free carbocation is not required.'
}

NOTES = {
'sn1-core':'If Nu is water or an alcohol, oxonium deprotonation is normally required; see SN1 solvolysis.',
}

GEOMETRY_BY_TITLE = {
'Proton transfer':'The base approaches H as the original donor–H contact weakens.',
'Heterolytic ionization':'C and leaving group separate; the carbocation center tends toward planar geometry.',
'Carbocation capture':'The nucleophile approaches one face of the approximately planar cation.',
'Nucleophilic carbonyl addition':'The carbonyl center changes from approximately trigonal planar to tetrahedral.',
'Alkene protonation':'One alkene carbon forms C–H while the other becomes a planarizing carbocation.',
'Alkene formation':'The adjacent carbon atoms align to form a planar π system.',
}

def apply_english(r):
    rid = r['id']
    assert len(FLOWS[rid]) == len(r['steps']), rid
    r['summary'] = SUMMARIES[rid]
    r['conditions'] = CONDITIONS.get(rid, r['conditions'])
    r['scope'] = SCOPES[rid]
    r['note'] = NOTES.get(rid, '')
    for st, flow in zip(r['steps'], FLOWS[rid]):
        st['flow'] = flow
        st['geometry'] = GEOMETRY_BY_TITLE.get(st['title'], st['geometry'])

ORBITAL_TRANSLATIONS = {
'σ(C–X) 的电子对随异裂保留在 X':'The σ(C–X) electron pair follows X during heterolysis; a vacant p-like orbital develops at carbon.',
'n(base) 与 σ(C–H) / p(C⁺) 耦合':'Base donation at β-H couples C–H σ electrons with the empty carbocation p orbital.',
'n(base) → σ*(C–H)，σ(C–H) 与 σ*(C–Br) 耦合':'n(base) → σ*(C–H), coupled with σ(C–H) → σ*(C–Br).',
'n(O) 恢复 π(C=O)，与 C–Cl 断裂耦合':'n(O) restores π(C=O) while C–Cl cleavage releases chloride.',
'SOMO 与 alkene π / π* 相互作用':'SOMO interaction with the alkene π/π* manifold.',
'六电子环状 orbital overlap':'Six-electron cyclic orbital overlap.',
'SOMO(Cl) 与 σ(C–H)':'SOMO(Cl) interacts with σ(C–H).',
'SOMO(C) 与 σ(Cl–Cl)':'SOMO(C) interacts with σ(Cl–Cl).',
'diene / dienophile frontier orbitals，六电子环状相互作用':'Diene and dienophile frontier orbitals in a cyclic six-electron interaction.',
'4π frontier-orbital symmetry':'4π frontier-orbital symmetry',
}
GEOMETRY_TRANSLATIONS = {
'N 接近 B；B 的配位几何随加合改变。':'N approaches B and boron changes its local coordination geometry.',
'Nu–C–Br 近似共线，背面进攻。':'Nu–C–Br approaches a near-linear backside alignment.',
'从离去基团背面接近。':'The nucleophile approaches opposite the leaving group.',
'通常偏好 H–C–C–Br anti-periplanar。':'An anti-periplanar H–C–C–Br alignment is generally favored.',
'O 接近 Al；配位使羰基碳的受体轨道与 Al–H 键取向耦合。':'O approaches Al, aligning carbonyl acceptance with an Al–H donor bond.',
'羰基碳由平面 sp² 型转为四面体；形成 C–H 与 O–Al 联系。':'Planar carbonyl carbon becomes tetrahedral as C–H and O–Al contacts form.',
'质子化与 Al–O 键水解完成工作后处理。':'Protonation and Al–O hydrolysis complete aqueous work-up.',
'配位使羰基碳受体轨道与 C–Mg 键取向耦合。':'Coordination aligns carbonyl acceptance with the C–Mg bond.',
'醛羰基碳由平面变为四面体；C–C 成键与 O–Mg 配位协同发生。':'The aldehyde carbon changes from planar to tetrahedral as C–C bonding and O–Mg coordination develop.',
'酸性水处理在 C–C 成键后进行；手性醛可能从两面进攻并形成对映体。':'Acid work-up follows C–C formation; two faces of a planar prochiral carbonyl can yield enantiomers.',
'四面体中心恢复羰基平面。':'The tetrahedral center returns to an approximately planar carbonyl.',
'背面进攻，环打开。':'Backside attack opens the epoxide ring.',
'自由基接近双键的一端。':'The radical approaches one end of the double bond.',
'两个反应中心接近。':'The two radical centers approach each other.',
'Cl 接近 H，C–H 断裂。':'Cl approaches H as the C–H bond breaks.',
'碳接近 Cl，Cl–Cl 同时断裂。':'Carbon approaches Cl while Cl–Cl breaks.',
'diene 需能取 s-cis；两个端点共同靠近 dienophile。':'The diene needs an accessible s-cis geometry; both termini approach the dienophile.',
'常用 chair-like transition structure 理解构象选择。':'A chair-like transition structure often explains conformational preference.',
'热 4π 体系采用 conrotatory 模式。':'A thermal 4π system closes conrotatorily.',
'先生成可离域稳定的共轭碱；这一步先于离去基团脱离。':'The delocalized conjugate base forms before the leaving group departs.',
'Cα 与 Cβ 建立 π 键，离去与成键在第二个独立事件中发生。':'Cα and Cβ form a π bond during the separate leaving-group event.',
'两个 C–Br 联系桥接同一 Br；不是游离碳正离子。':'One bromine bridges both carbons in a three-membered ion; no free carbocation is required.',
'背面开环使两个 Br 反面加入；环状中间体被解除。':'Backside opening places the two bromines anti and removes the bridge.',
'烯烃两个碳被桥式 Br 连结。':'A bromine bridge connects both alkene carbons.',
'背面进攻与桥断裂同时发生；形成 anti 的 C–O 与 C–Br 关系。':'Backside attack and bridge cleavage give anti C–O and C–Br contacts.',
'脱水产生的 NO₂⁺ 是芳香亲电取代的实际电亲试剂。':'Dehydration produces the near-linear NO₂⁺ electrophile.',
'被进攻碳暂时转为 sp³；此中间体已失去芳香稳定。':'The attacked carbon becomes approximately tetrahedral and the σ complex loses aromaticity.',
'恢复平面共轭芳香环。':'The conjugated aromatic ring becomes planar again.',
'四面体中心恢复平面羰基结构，生成质子化酯。':'The tetrahedral acyl center reforms a planar carbonyl in protonated ester.',
'C=N 双键形成；离去过程中正电荷保留在亚胺氮/π 系统。':'C=N forms while water departs, leaving an iminium center.',
'形成与羰基共轭的双键，碱在总体循环中再生。':'A C=C bond conjugated with carbonyl forms; base is regenerated over the cycle.',
'进攻碳发生反转；环开裂与 C–Cl 成键耦合，反面加成。':'The attacked carbon inverts as C–Cl forms and the ring opens from behind.',
}
FACTS = {
'proton-transfer': [['pKa(CH₃CO₂H)','4.76 (approximate textbook value)'],['pKa(HCN)','9.31 (approximate textbook value)'],['Illustrative equilibrium estimate','10^(9.31 − 4.76) ≈ 3.55 × 10⁴ from the two approximate pKa values on a shared scale; not a measured equilibrium constant.']],
'lewis':[['Electron accounting','N donates one electron pair; B accepts it.'],['Formal charge','A conventional covalent-bond depiction assigns N +1 and B −1; total charge remains zero.']],
'sn2':[['Orbital interaction','n(O) donation into σ*(C–Br)'],['Stereochemistry','A chiral reaction center inverts configuration, but the R/S descriptor does not necessarily flip.']],
'williamson':[['Reaction center','Nucleophilic oxygen forms a new C–O σ bond.'],['Substrate choice','Methyl and less hindered primary substrates favor substitution.']],
'sn1-core':[['Two events','1111 → 1111; the same code does not mean the same event.'],['Electronic structure','C–X heterolysis forms a p-like carbocation acceptor orbital.']],
'sn1-water':[['Intermediates','Carbocation → oxonium → alcohol.'],['Electronic structure','Lone-pair donation enters the vacant p-like orbital; ion pairing can alter the electronic structure.']],
'hbr':[['Regiochemistry','The principal polar pathway gives the Markovnikov product in this example.'],['Key intermediate','Secondary carbocation.']],
'hydration':[['Catalyst balance','H₃O⁺ is regenerated in the last event.'],['Regiochemistry','The example produces 2-propanol.']],
'carbonyl-add':[['Geometry','Trigonal planar → tetrahedral.'],['Electronic change','C–Nu forms while the C=O π pair shifts to oxygen.']],
'cyanohydrin':[['Catalyst balance','CN⁻ is consumed in addition and regenerated on protonation.'],['Reversibility','Cyanohydrin formation is reversible.']],
'acyl':[['Path','Addition → tetrahedral intermediate → elimination.'],['Coding','1113 → 1113; two events with opposite bond changes can share a code.']],
'epoxide':[['Site selectivity','Base-promoted opening of unsymmetrical epoxides usually attacks the less hindered carbon.'],['Stereochemistry','The attacked site undergoes inversion.']],
'aldol':[['Catalyst balance','HO⁻ is regenerated in the last event.'],['Addition ≠ condensation','Later dehydration adds separate events outside this three-step entry.']],
'radical-add':[['Electron accounting','Fishhook arrows denote single-electron movement.'],['Spin','The system remains open shell; no free carbocation is produced.']],
'radical-combine':[['Event type','Chain termination.'],['S2 meaning','The event involves radicals; ethane product is closed shell.']],
'radical-chain':[['Cycle','Canceling the propagating Cl• and CH₃• gives the net equation.'],['Scope of two codes','Only propagation is coded; initiation and termination are separate.']],
'diels-alder':[['Bond bookkeeping','3 π → 1 π + 2 σ.'],['Stereochemistry','A typical thermal event is suprafacial on both components.']],
'claisen':[['Product','Allyl vinyl ether produces a γ,δ-unsaturated carbonyl.'],['Shared code','The Diels–Alder event also has 1333 but a different bond-change topology.']],
'electrocyclic':[['Selection rule','Thermal 4π: conrotatory; thermal 6π: disrotatory.'],['Orbital symmetry','The thermal rotation mode follows the occupied-orbital symmetry.']],
}

# Retain records whose facts were already English.
def finish_english(r):
    rid = r['id']
    if rid in FACTS: r['facts'] = FACTS[rid]
    for st in r['steps']:
        st['orbital'] = ORBITAL_TRANSLATIONS.get(st['orbital'], st['orbital'])
        st['geometry'] = GEOMETRY_TRANSLATIONS.get(st['geometry'], st['geometry'])
