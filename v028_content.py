"""Event-specific v0.2.8 teaching copy on top of the audited codebook.

No numeric code or source table is redefined here. The text describes the
equation actually displayed on each card, not a universal pathway.
"""

# Generic proton-transfer and carbonyl-addition snippets were repeated across
# chemically different intermediates. Each tuple is (orbital, geometry).
EVENTS = {
 ('proton-transfer',0):('Cyanide carbon lone pair → σ*(O–H) of acetic acid; the O–H pair localizes on carboxylate oxygen.','The C···H···O transfer coordinate shortens C–H as O–H stretches; solvent can introduce a relay.'),
 ('sn1-water',2):('Water lone pair accepts the oxonium proton while the tert-butyl O–H bonding pair returns to oxygen.','Water approaches an O–H bond of protonated tert-butanol; C–O connectivity stays intact.'),
 ('hydration',2):('Water abstracts H from protonated 2-propanol; the alcohol O–H pair returns to its oxygen.','A hydrogen-bonded water/oxonium encounter loses H without changing the C–O bond.'),
 ('carbonyl-add',0):('The occupied nucleophile lone pair mixes with π*(C=O); the π electrons move toward oxygen.','An out-of-plane approach to planar R₂C=O forms a tetrahedral alkoxide; its attack face is unspecified.'),
 ('cyanohydrin',0):('Cyanide carbon donates to benzaldehyde π*(C=O), while π(C=O) polarizes onto oxygen.','CN⁻ approaches one face of planar PhCHO; the benzylic alkoxide is tetrahedral and can be chiral.'),
 ('cyanohydrin',1):('Alkoxide O takes H from H–CN and the H–C electron pair returns to cyanide carbon.','The alkoxide/HCN proton-transfer encounter converts O⁻ to OH without changing its new C–CN bond.'),
 ('acyl',0):('Methoxide O donates into π*(C=O) of acetyl chloride and the carbonyl π pair shifts to O.','The planar acyl carbon becomes tetrahedral, retaining the chloride until collapse or a concerted alternative.'),
 ('epoxide',1):('The newly formed terminal alkoxide O attacks H of H₃O⁺; the donor O–H pair returns to water.','This separate aqueous work-up protonates the alkoxide after backside epoxide opening.'),
 ('aldol',0):('Hydroxide abstracts an acetaldehyde α-H; the C–H pair enters the enolate π system and electron density delocalizes onto O.','At the α carbon, deprotonation permits an enolate-like planar π arrangement; carbon and oxygen resonance forms are not extra events.'),
 ('aldol',1):('The carbon-centered enolate contributor attacks a second acetaldehyde C=O; its π pair shifts to O.','The acceptor aldehyde carbon changes from planar to tetrahedral; a new Cα–Ccarbonyl bond forms.'),
 ('aldol',2):('The aldolate O⁻ takes H from water; water O–H electrons return to hydroxide.','Protonation changes the new O⁻ to β-OH without breaking the aldol C–C bond.'),
 ('halohydrin',2):('Water removes H from the attached oxonium O⁺; the substrate O–H electrons return to oxygen.','Deprotonation leaves the anti-installed C–Br and C–OH bonds in place.'),
 ('nitration-benzene',0):('Nitric-acid hydroxyl O donates to H of sulfuric acid; the sulfuric O–H pair gives HSO₄⁻.','An acid encounter protonates the hydroxyl oxygen destined to depart as water.'),
 ('fischer-esterification',0):('The acetic-acid carbonyl O lone pair accepts H from H₃O⁺; the donor O–H pair returns to water.','Protonated CH₃C(=OH⁺)OH retains a planar acyl carbon and bears +1 on the original carbonyl O.'),
 ('fischer-esterification',1):('Ethanol O lone pair → π*(C=OH⁺), with C=O π electrons returning to the original oxygen.','The acyl carbon becomes tetrahedral; the incoming ethoxy O bears +1 until deprotonated.'),
 ('fischer-esterification',2):('Water removes the ethoxy oxonium H; a subsequent solvent-acid transfer protonates the original hydroxyl O.','Two solvent-mediated proton transfers connect oxonium and water-leaving-group states; this listed stage is grouped.'),
 ('fischer-esterification',4):('Water removes H from the protonated ester carbonyl O; the O–H electrons neutralize that oxygen.','The ester acyl carbon remains planar while hydronium is regenerated.'),
 ('imine-formation',0):('Acetone carbonyl O donates to H of H₃O⁺; the hydronium O–H pair goes to water.','The O-protonated carbonyl is still planar, with +1 on oxygen.'),
 ('imine-formation',1):('Methylamine N lone pair attacks acetone π*(C=OH⁺); the C=O π pair returns to O.','The new tetrahedral carbinolammonium has a neutral OH and four-coordinate N⁺.'),
 ('imine-formation',2):('Water removes one N–H proton from carbinolammonium; the N–H pair neutralizes N.','Neutral carbinolamine retains tetrahedral carbon and has one N–H bond.'),
 ('imine-formation',3):('The carbinolamine OH lone pair accepts H from H₃O⁺; donor O–H electrons return to water.','Tetrahedral C–OH becomes C–OH₂⁺, making neutral water a potential leaving group.'),
 ('imine-formation',5):('Water abstracts H from iminium N⁺; the N–H pair returns to N.','Deprotonation retains planar C=N and removes its positive charge.'),
 ('aldol-condensation',0):('Hydroxide removes an acetone α-H; the C–H electrons enter the enolate π system.','The α carbon becomes part of a delocalized enolate; the CH₂⁻ formula is one resonance contributor.'),
 ('aldol-condensation',1):('The acetone enolate carbon attacks another acetone C=O; its π pair goes to O.','The acceptor carbonyl carbon becomes tetrahedral at the new C–C bond.'),
 ('aldol-condensation',2):('The aldolate O takes H from water, returning the donor O–H pair to hydroxide.','The product β-hydroxyl group appears at the formerly planar acceptor carbonyl carbon.'),
 ('aldol-condensation',3):('Hydroxide removes the α-H next to the surviving ketone; its C–H pair enters the conjugated enolate.','α-Deprotonation occurs before β-OH departure in the E1cB teaching path.'),
 ('acid-epoxide',0):('Epoxide O lone pair takes H from HCl while the H–Cl bond pair goes to Cl⁻.','O protonation leaves both strained epoxide C–O bonds in place and creates O⁺H before ring opening.'),
}

DESCRIPTORS = {
 'proton-transfer':['O–H versus H–C bond orders during acetate/cyanide proton transfer','Solvent-dependent localization of charge on acetate and cyanide'],
 'lewis':['N→B donor interaction and B–N bond order in H₃N–BF₃','Charge redistribution on nitrogen and boron as boron changes coordination'],
 'sn2':['Cl⁻/A–Cl benchmark: σ*(A–Cl) energy versus interaction and strain','For HO⁻/CH₃Br, the unperformed backside attack and C–Br cleavage coordinate'],
 'williamson':['Methoxide/alkyl-bromide backside interaction and ether-bond growth','C–Br bond extension versus nucleophile approach in this substrate'],
 'sn1-core':['C–X ionization and ion-pair stabilization under an explicit solvent model','Nu capture versus solvent-assisted displacement along the same substrate coordinate'],
 'sn1-water':['Tert-butyl C–Br ionization and water contact-ion-pair stabilization','Water capture versus E1 and oxonium deprotonation under the stated conditions'],
 'hbr':['Propene π donation into H–Br and secondary-carbocation charge distribution','Bromide capture versus ion-pair separation on the propene/HBr path'],
 'hydration':['Propene protonation and water attack at secondary carbon','Solvent stabilization of secondary cation and 2-propanol oxonium'],
 'e2':['Anti Hβ–Cβ–Cα–Br torsion and C–H/C–Br cleavage','Ethoxide interaction, propene π-bond formation and competing substitution'],
 'e1':['tert-Butyl chloride ionization versus delayed β-deprotonation','Cation stabilization and C=C development in the stated solvent'],
 'carbonyl-add':['Nu⁻ approach angle to R₂C=O and n(Nu)→π*(C=O)','C–Nu growth and O⁻ formation in the unprotonated local event'],
 'hydride':['Provisional AlH₄⁻ encounter and possible hydride-to-carbonyl interaction','O–Al contacts, H-transfer bond orders and aggregate sensitivity'],
 'grignard':['Aldehyde–Mg contact geometry in solvated Grignard aggregates','C–Mg loss, C–C formation and carbonyl-oxygen charge transfer'],
 'cyanohydrin':['Benzaldehyde/CN⁻ approach angle and C–CN bond formation','Alkoxide protonation by HCN after the addition event'],
 'acyl':['Methoxide attack on acetyl chloride and C=O π opening','Tetrahedral versus concerted C–Cl departure pathways'],
 'epoxide':['Methoxide backside ring opening at an epoxide carbon','Ring C–O rupture followed by distinct hydronium work-up'],
 'aldol':['Acetaldehyde enolate delocalization at α-C and O','C–C growth into a second aldehyde and aldolate protonation'],
 'radical-add':['Alkene π and incoming radical SOMO overlap','Spin redistribution to the terminal carbon after bond formation'],
 'radical-combine':['Methyl radical SOMO overlap and spin-pairing condition','C–C bond-order growth toward closed-shell ethane'],
 'radical-chain':['Methane C–H homolysis in Cl• abstraction','Methyl radical transfer at Cl₂ and regenerated Cl• spin density'],
 'diels-alder':['Butadiene s-cis/ethene orbital phases for suprafacial [4+2]','Two forming σ bonds and the internal diene π bond at matched coordinates'],
 'claisen':['Allyl vinyl ether six-center orbital phase relationship','O–allyl cleavage and new C–C bond asynchronicity on an ELF path'],
 'electrocyclic':['4π terminal-orbital phases under thermal conrotation','Terminal C–C σ growth and stereochemical orientation'],
 'e1cb-dehydration':['Carbonyl α-enolate stabilization before C–OH departure','Cα=Cβ growth and β-C–O cleavage as distinct stages'],
 'alkene-bromination':['Propene π donation to Br₂ and bromonium charge distribution','Backside Br⁻ ring opening and anti relative geometry'],
 'halohydrin':['Propene/Br₂ bromonium formation in water','Water attack at the substituted carbon and subsequent oxonium deprotonation'],
 'nitration-benzene':['Nitronium generation from mixed acids and N–O charge changes','Arene–NO₂⁺ interaction and arenium π-delocalization through rearomatization'],
 'fischer-esterification':['Acetic-acid carbonyl activation and ethanol O attack','Tetrahedral proton-relay structures and water departure under acid catalysis'],
 'imine-formation':['Acetone protonation and methylamine addition','Carbinolamine dehydration, iminium formation and N deprotonation'],
 'aldol-condensation':['Acetone enolate donation into a second acetone C=O','E1cB enolate stabilization and β-hydroxide loss'],
 'acid-epoxide':['Propylene-oxide O protonation and primary-site Cl⁻ attack','Strained C–O cleavage coupled to neutral alcohol formation'],
}

def apply_v028(reactions):
    for r in reactions:
        rid=r['id']
        assert rid in DESCRIPTORS
        r['quantumData']['descriptors']=DESCRIPTORS[rid]
        for i, s in enumerate(r['steps']):
            if (rid,i) in EVENTS:
                old_orbital,old_geometry=s['orbital'],s['geometry']
                orbital,geometry=EVENTS[(rid,i)]
                s.update(orbital=orbital,geometry=geometry)
                s['why'][1]=orbital;s['why'][3]=geometry
        q=r['quantumData']
        q['note']=(f"For {r['name']}, distinguish the named published system below from this card's equation. "
                   'The proposed protocol has not been run by the Atlas.' if q['literatureCases'] or q['literatureInsights'] else
                   f"No computed result is mapped to {r['name']}. The following observables and protocol are proposals, not results.")
    R={r['id']:r for r in reactions}
    R['sn2']['facts']=[['This substrate','Methyl bromide has no stereogenic carbon and no β-carbon; this example cannot show inversion or ordinary E2.'],['Orbital interaction','Hydroxide O attacks opposite the C–Br bond along the near-linear O···C···Br path. The published Cl⁻/A–Cl series is a different model.']]
    R['carbonyl-add']['facts']=[['Charge and scope','Nu⁻ becomes bonded to carbonyl carbon; the O⁻ alkoxide is the endpoint of this local equation, before any work-up.'],['Approach face','Planar R₂C=O can be approached from either face. When the two R groups are identical, this generic product center is not stereogenic.']]
    R['diels-alder']['facts']=[['Six-electron bookkeeping','The butadiene terminal π bonds and ethene π bond become two ring σ bonds and one internal C=C in cyclohexene.'],['Stereochemistry','Both components engage suprafacially; unsubstituted butadiene and ethene create no stereocenter or endo/exo choice.']]
    R['fischer-esterification']['facts']=[['Oxygen identities','The ethanol O becomes the ester single-bonded O; the original acetic-acid carbonyl O reforms C=O.'],['Relay and equilibrium','Neutralizing the incoming oxonium and activating OH as H₂O requires solvent-mediated proton transfers; removal of water or alcohol excess shifts the reversible reaction.']]
    R['imine-formation']['facts']=[['Charge sequence','Acetone carbonyl O⁺ → N⁺ carbinolammonium → neutral carbinolamine → O⁺ leaving group → N⁺ iminium → neutral imine.'],['Acidity window','Mild acid assists addition and water departure; strongly acidic conditions deplete free methylamine by protonation.']]
    R['imine-formation']['steps'][5]['equation']='(CH₃)₂C=N⁺(H)CH₃ + H₂O ⇌ (CH₃)₂C=NCH₃ + H₃O⁺'
    # Preserve audited numbers while adding a concise, model-specific reading.
    R['sn2']['quantumData']['literatureCases'][0]['teachingPoint']='For Cl⁻ + A–Cl, a lower σ*(A–Cl) level accompanies a more attractive fragment-interaction term; the HO⁻/CH₃Br teaching pair was not calculated.'
    R['diels-alder']['quantumData']['literatureCases'][0]['teachingPoint']='At the fixed 2.203 Å geometry, ionizing acrolein changes both orbital stabilization and Pauli repulsion. Its stepwise doublet path differs from the neutral butadiene/ethene card.'
    R['carbonyl-add']['quantumData']['literatureInsights'][0]['teachingPoint']='The 111° CN⁻/acetone result is an approach-angle optimum, not a universal nucleophile angle or a value computed for R₂C=O + Nu⁻.'
    for rid in ('carbonyl-add','cyanohydrin'):
        R[rid]['quantumData']['literatureInsights'][0]['publishedQuantity']='Preferred C(CN)–C(carbonyl)–O angle ≈111° for gas-phase CN⁻ + acetone (−1, singlet); M06-2X/6-311+G(d,p) geometry scan. The teaching substrate is different.'
    for rid in ('e2','diels-alder','carbonyl-add','fischer-esterification','imine-formation'):
        r=R[rid];f=r['figure'];f['priorReference']={k:v for k,v in f.items() if k!='priorReference'}
        f.update(src='mechanisms/'+rid+'.svg',href='mechanisms/'+rid+'.svg',alt='Original equation-matched electron-flow pathway: '+r['name'],
                 match='exact',coverage='complete',reviewed=True,display=True,
                 reviewNote='Original condensed-structure pathway checked against every listed equation, charge, intermediate and electron-pair move; Fischer step 3 expands a grouped solvent relay. The diagram does not specify computed transition-state geometry.',
                 rightsStatus='original',license='Original SORG Atlas illustration · CC BY-NC-SA 4.0',
                 licenseUrl='https://creativecommons.org/licenses/by-nc-sa/4.0/',credit='SORG Atlas · original SVG')
        for s in r['steps']:s['diagramScope']='partial' # Existing local motif remains an intentionally partial teaching motif.

