(function(root){
 'use strict';
 // Curated teaching metadata. These labels neither modify the reaction database nor imply calculated orbitals.
 const cases={
  sn2:{title:'SN2 · backside displacement',event:'sn2:0',intro:'Reason from HO⁻ + CH₃Br to CH₃OH + Br⁻. Methyl bromide cannot display stereochemical inversion at a stereogenic center.',
   questions:[
    ['Where does the attacking electron pair begin?',[
      ['The hydroxide oxygen lone pair','yes','O of HO⁻ donates a lone pair; carbon is the electrophilic reaction center.'],
      ['The C–Br σ bond','no','The C–Br pair leaves with bromide. It is not the pair that forms C–O.'],
      ['The bromine lone pair','no','Bromine is the departing group in this substitution, not the attacking nucleophile.']]],
    ['Which substrate acceptor is approached?',[
      ['σ*(C–Br), along the C–Br axis','yes','Backside donation into the C–Br antibonding region is the useful orbital picture.'],
      ['π*(C=O)','no','Methyl bromide has no carbonyl π bond. That acceptor belongs to carbonyl addition.'],
      ['An occupied C–Br σ orbital','no','Donation into an occupied bond is not the standard acceptor description; the relevant acceptor is σ*(C–Br).']]],
    ['What bond changes belong to this one event?',[
      ['C–O forms as C–Br cleaves','yes','The displacement couples formation and departure; Br⁻ carries the C–Br bonding pair.'],
      ['C–Br first ionizes to a free methyl cation','no','That is a stepwise SN1 model, not the specified concerted methyl substitution.'],
      ['A C=C bond forms after β-H loss','no','CH₃Br has no β-carbon or β-hydrogen for ordinary E2.']]],
    ['What approach geometry is favored?',[
      ['Near-linear O···C···Br backside approach','yes','This orientation aligns the oxygen donor with the C–Br antibonding direction. The drawn methyl example is achiral.'],
      ['Attack from the same side as Br','no','Frontside approach is not the characteristic backside SN2 geometry and gives poorer access to σ*(C–Br).'],
      ['A six-atom cyclic array','no','That is a pericyclic topology, not this local substitution.']]],
    ['Which inherited teaching code fits this event?',[
      ['1122 · closed-shell donor–acceptor bond replacement','yes','S1/O1/R2/G2 captures coupled substitution, but not the identity of O, C, or Br.'],
      ['1113 · local planar-to-tetrahedral carbonyl change','no','There is no carbonyl π bond or tetrahedral carbonyl intermediate here.'],
      ['1333 · concerted cyclic orbital organization','no','Concerted does not by itself mean pericyclic: this event is local backside displacement.']]]]},
  e2:{title:'E2 · anti elimination',event:'e2:0',intro:'Reason from CH₃CHBrCH₃ + EtO⁻ to propene, EtOH and Br⁻. The diagram depicts one anti-compatible conformer.',
   questions:[
    ['Which pair initiates the drawn elimination?',[
      ['An ethoxide oxygen lone pair abstracts a β-H','yes','The base takes a hydrogen on the carbon next to the C–Br center.'],
      ['A bromide lone pair attacks the α-carbon','no','Br⁻ is produced when the C–Br pair departs; it is not the base in this equation.'],
      ['The alkene π bond attacks ethoxide','no','The alkene is the product, not a reactant electron source.']]],
    ['Which coupled acceptor-and-donor sequence is useful?',[
      ['n(O)→σ*(Cβ–H); σ(Cβ–H)→π(Cα=Cβ) as σ(Cα–Br) departs','yes','This is a coupled three-arrow electron-pair description, not a measured orbital coupling constant.'],
      ['n(O)→π*(C=O)','no','No carbonyl appears in the substrate; E2 consumes β-C–H and C–Br bonds.'],
      ['π(diene)→π*(dienophile)','no','That describes a cycloaddition donor–acceptor view, not β-elimination.']]],
    ['Which bonds change in the concerted model?',[
      ['Cβ–H and Cα–Br break as Cα=Cβ forms','yes','All three bond changes belong to the same E2 event, though bonding changes need not be perfectly synchronous.'],
      ['C–Br breaks to a carbocation before deprotonation','no','That sequence is E1, not the specified E2 elementary event.'],
      ['Two C–C σ bonds form','no','That is a [4+2] cycloaddition pattern.']]],
    ['Why rotate into an anti-compatible conformation?',[
      ['β-C–H and C–Br align approximately antiperiplanar','yes','The aligned orbitals facilitate coupled C–H cleavage, π formation and leaving-group departure. Acyclic conformers can interconvert.'],
      ['It makes carbonyl carbon planar','no','This substrate has no carbonyl. The relevant coordinate is the H–Cβ–Cα–Br dihedral.'],
      ['It forces a cis diene','no','s-cis describes a conjugated diene for a Diels–Alder reaction.']]],
    ['Which provisional SORG assignment is retained?',[
      ['1133 · polar coupled multiple-bond reorganization','yes','S1/O1/R3/G3 is the current candidate convention; 1133 also groups chemically different events.'],
      ['1122 · only bond replacement at one center','no','The β-C–H, Cα–Br and C=C changes span a coupled two-carbon elimination.'],
      ['1333 · cyclic pericyclic overlap','no','Anti alignment does not turn E2 into a six-center pericyclic reaction.']]]]},
  'carbonyl-add':{title:'Carbonyl addition · alkoxide formation',event:'carbonyl-add:0',intro:'The card deliberately writes R₂C=O + Nu⁻ → R₂C(O⁻)Nu. It leaves the nucleophile and carbonyl substituents unspecified.',
   questions:[
    ['Which pair is the incoming donor in this model?',[
      ['A filled orbital/lone pair on Nu⁻','yes','The nucleophile supplies the pair forming the new C–Nu bond; its orbital identity depends on the actual Nu⁻.'],
      ['The carbonyl oxygen lone pair','no','Oxygen receives the C=O π pair in the product; it is not the incoming nucleophile.'],
      ['An unpaired radical electron','no','The written event is a closed-shell anionic addition, not a radical attack.']]],
    ['Which acceptor best explains attack at carbonyl carbon?',[
      ['π*(C=O), polarized toward carbon','yes','Occupied nucleophile donation into the carbonyl antibonding system is a qualitative FMO model.'],
      ['σ*(C–Br)','no','No C–Br bond is present in the generic carbonyl equation.'],
      ['A diene π HOMO','no','This is not a conjugated diene/dienophile pair.']]],
    ['How do bonding and charge change?',[
      ['C–Nu forms; C=O π pair moves to O⁻','yes','A tetrahedral alkoxide forms and net charge remains −1 in this idealized equation.'],
      ['O–H forms and C=O stays intact','no','There is no proton source in the written elementary equation; protonation would be another event.'],
      ['C–O σ bond cleaves to give a carbocation','no','Carbonyl addition weakens the π component, not the C–O σ bond.']]],
    ['What geometry is supported without claiming a universal angle?',[
      ['Out-of-plane approach to planar C=O; tetrahedralization follows','yes','The preferred trajectory depends on nucleophile and substituents. ≈111° belongs to published CN⁻ + acetone, not every R₂C=O + Nu⁻.'],
      ['Any approach must be exactly 111°','no','The cited ≈111° is a model-specific optimum for gas-phase CN⁻ + acetone, not a universal constraint.'],
      ['Antiperiplanar β-H and leaving group','no','That stereoelectronic requirement belongs to E2 elimination.']]],
    ['Which candidate code is used by the Atlas?',[
      ['1113 · polar local addition with planar-to-tetrahedral change','yes','The G3/R1 boundary is provisional: the code does not specify Nu identity or approach face.'],
      ['1122 · backside leaving-group replacement','no','The written product is an alkoxide from π-bond opening; no leaving group is expelled.'],
      ['1333 · cyclic six-electron reorganization','no','The event is local polar addition, not a pericyclic six-center topology.']]]]},
  'diels-alder':{title:'Diels–Alder · [4+2] cycloaddition',event:'diels-alder:0',intro:'The displayed reaction is neutral 1,3-butadiene + ethene → cyclohexene. The acrolein calculations below are related models, not this equation.',
   questions:[
    ['Where are the participating electron pairs?',[
      ['Three π pairs across diene and dienophile','yes','The six π electrons are reorganized around the cyclic [4+2] topology.'],
      ['A hydroxide lone pair and C–Br bond','no','That pair belongs to the SN2 teaching equation, not this hydrocarbon cycloaddition.'],
      ['One radical SOMO on ethene','no','The displayed neutral ethene/butadiene reaction is closed-shell; an ionized acrolein model is a separate pathway.']]],
    ['Which orbital organization is the useful symmetry model?',[
      ['Cyclic interaction of diene/dienophile π frontier orbitals','yes','A thermal suprafacial–suprafacial [4+2] model is symmetry allowed; the sketch is conceptual, not a calculated orbital plot.'],
      ['Donation into σ*(C–Br)','no','There is no alkyl bromide or localized leaving-group bond.'],
      ['Only a carbonyl π* at one carbon','no','Ethene has no carbonyl, and both diene termini participate in the cyclic organization.']]],
    ['What bonds change in the [4+2] event?',[
      ['Two terminal C–C σ bonds form; one ring π bond remains','yes','Three π bonds reorganize into two σ bonds and one π bond in cyclohexene.'],
      ['Only one C–C bond forms, then a carbocation waits','no','That is not the neutral concerted teaching model; the studied acrolein radical cation can follow a distinct stepwise path.'],
      ['A β-H and C–Br both break','no','That is the E2 bond-change pattern.']]],
    ['Which conformational/geometric constraint matters?',[
      ['The diene accesses s-cis and both termini meet the dienophile','yes','The s-cis diene geometry enables six-center overlap; the model does not specify a single synchronous bond length.'],
      ['The diene must stay s-trans','no','An s-trans diene cannot bring both ends into the usual six-membered cycloaddition geometry.'],
      ['One nucleophile approaches carbonyl carbon at exactly 111°','no','No carbonyl appears in this teaching reaction, and the angle is from another published model.']]],
    ['Which code and topology descriptor apply to the neutral event?',[
      ['1333 · concerted cyclic organization; cycloaddition','yes','The descriptor names the topology without adding a fifth digit. The code does not encode asynchronicity or substituent effects.'],
      ['1133 · polar E2-like elimination','no','Both events reorganize bonds, but the six-center cyclic orbital organization is O3 rather than O1.'],
      ['2211 · open-shell radical coupling','no','The displayed butadiene/ethene model is neutral closed shell.']]]]}
 };
 const groups={
  'polar-proton-transfer':{label:'Polar proton transfer',description:'An electron-pair donor forms a bond to H as the original H–donor bond changes; alkene protonation additionally reorganizes a π bond.',keys:['proton-transfer:0','hbr:0','hydration:0','sn1-water:2','cyanohydrin:1','fischer-esterification:0','imine-formation:0']},
  'backside-displacement':{label:'Backside substitution',description:'A donor approaches a carbon opposite a departing C–X or strained C–O bond; substrate and leaving group differ.',keys:['sn2:0','williamson:0','epoxide:0','alkene-bromination:1','acid-epoxide:1']},
  'carbonyl-addition':{label:'C=O addition',description:'C–Nu bond formation accompanies C=O π-pair displacement to oxygen; the entering species and activation state differ.',keys:['carbonyl-add:0','hydride:1','grignard:1','cyanohydrin:0','acyl:0','aldol:1','fischer-esterification:1','imine-formation:1','aldol-condensation:1']},
  'alkene-forming-elimination':{label:'Alkene-forming elimination',description:'A C=C bond forms with loss of a group, but E2, E1 and E1cB have different timing and intermediates.',keys:['e2:0','e1:1','e1cb-dehydration:1','aldol-condensation:4']},
  'bromonium-formation':{label:'Bromonium bridge',description:'Alkene π electrons participate in Br⁺ bridging; water versus bromide capture occurs later.',keys:['alkene-bromination:0','halohydrin:0']},
  'carbonyl-collapse':{label:'Tetrahedral collapse',description:'A tetrahedral carbon center reforms C=O as a leaving group departs; activation and leaving group differ.',keys:['acyl:1','fischer-esterification:3']},
  'heterolytic-ionization':{label:'C–X ionization',description:'A C–X bond pair leaves with X, creating a carbocation before capture or elimination.',keys:['sn1-core:0','sn1-water:0','e1:0']},
  'radical-atom-transfer':{label:'Radical atom transfer',description:'A radical abstracts an atom while homolytic bond changes propagate a chain.',keys:['radical-chain:0','radical-chain:1']}
 };
 const descriptors={
  'sn2:0':['Backside n(O)→σ*(C–Br)','Local substitution topology'],
  'e2:0':['Anti-periplanar β-C–H / C–Br','Concerted β-elimination topology'],
  'carbonyl-add:0':['Out-of-plane Nu→π*(C=O)','Planar-to-tetrahedral topology'],
  'diels-alder:0':['Thermal suprafacial–suprafacial [4+2] model','Six-center cycloaddition topology'],
  'claisen:0':['Thermal suprafacial [3,3] model','Six-center sigmatropic topology'],
  'electrocyclic:0':['Thermal 4π conrotatory mode','Electrocyclic ring closure topology']
 };
 const studies={
  sn2:{heading:'Why can the acceptor change a substitution pathway?',source:'qc_sn2',model:'Published model: Cl⁻ + CH₃Cl, NH₂Cl, OHCl or FCl in the gas phase; not HO⁻ + CH₃Br.',story:[
   'Electronic structure → The isolated A–Cl σ* energy becomes more negative from C to F in the reported ZORA-OLYP/TZ2P series. This is an orbital-energy comparison under one convention, not an observed rate.',
   'Geometry and energetics → At the authors’ TS (C/N/O) or transition complex (F), the fragment-interaction term is more stabilizing across the reported rows; strain and interaction must be considered together. The F structure is not the same stationary-point type.',
   'Mechanism and selectivity → Backside n→σ* donation rationalizes the O1/R2/G2 teaching model, but this series cannot predict the rate or SN2/E2 preference of hydroxide + methyl bromide. The four digits omit orbital level, deformation and solvation.'
  ]},
  'diels-alder':{heading:'Why can ionization change the cycloaddition path?',source:'qc_da_ion',model:'Published model: butadiene + acrolein versus acrolein radical cation at matched forming C···C distance 2.203 Å; not butadiene + ethene.',story:[
   'Electronic structure → ZORA-(U)BP86/TZ2P analysis finds stronger stabilizing orbital interaction and lower Pauli repulsion for the ionized acrolein pair at a matched geometry; the SOMO provides a distinct open-shell interaction.',
   'Geometry and mechanism → The neutral acrolein path is concerted asynchronous, whereas the radical-cation pathway is stepwise in the study. Its doublet state is not a small numerical variation of the neutral singlet event.',
   'Classification limit → The neutral [4+2] teaching event is 1333, with a cycloaddition subtype. Applying that code to the radical-cation path would erase both state and stepwise connectivity. EDA terms are not electronic-coupling constants.'
  ]},
  'carbonyl-add':{heading:'Why does attack have a preferred trajectory?',source:'qc_attack_angle',model:'Published model: gas-phase CN⁻ + acetone (total −1, singlet); the teaching equation R₂C=O + Nu⁻ is generic.',story:[
   'Electronic structure → Occupied cyanide donation toward carbonyl π* competes with occupied–occupied Pauli repulsion; the study decomposes the interaction using declared CN⁻ and acetone fragments.',
   'Geometry → The relaxed M06-2X/6-311+G(d,p) scan gives an approximate C(CN)–C(carbonyl)–O approach angle of 111°. Smaller angles raise Pauli repulsion; larger angles incur more acetone distortion in this model.',
   'Mechanism and selectivity → An out-of-plane trajectory leads from planar C=O toward tetrahedral alkoxide. This angle alone does not predict which enantiotopic face is attacked, or a universal angle for other Nu⁻/carbonyl systems. Candidate 1113 records neither the angle nor facial selectivity.'
  ]}
 };
 root.SorgLearning={cases,groups,descriptors,studies};
})(typeof window==='undefined'?module.exports:window);
