"""Reviewed corrections to v0.2.6; preserve the numeric codebook and entry IDs."""
from copy import deepcopy

# Match and coverage are independent: a picture can use the same substrate but
# omit events, or show a full pathway for an analogous substrate.
FIGURES = {
 'proton-transfer':('pending','unreviewed','Dead image URL (HTTP 404).'),
 'lewis':('exact','complete','NH3 and BF3, donor arrow and formal charges match.'),
 'sn2':('exact','complete','Hydroxide + methyl bromide; reaction, electron arrows and transition structure match. Methyl carbon is achiral.'),
 'williamson':('representative','complete','Examples use ethoxide/ethyl bromide or methoxide/ethyl iodide, rather than methoxide/ethyl bromide.'),
 'sn1-core':('representative','complete','Image is tert-butyl bromide solvolysis with water and a third deprotonation; card is a two-event generic anionic-nucleophile core.'),
 'sn1-water':('exact','complete','Tert-butyl bromide, water capture, oxonium and deprotonation match the three displayed events.'),
 'hbr':('exact','complete','The upper propene-to-2-bromopropane branch matches. The lower primary-carbocation branch is not a validated minor pathway for this card.'),
 'hydration':('partial','partial','Propene hydration is intended, but the terminal carbon remains labeled CH2 after protonation instead of CH3; image withheld.'),
 'e2':('representative','complete','Generic base/leaving group. Slide prose incorrectly says two arrows originate at the base; image withheld.'),
 'e1':('representative','partial','Generic alkyl skeleton and X; solvent base and its protonated product are omitted.'),
 'carbonyl-add':('representative','complete','Acetone + hydroxide followed by protonation; card describes generic carbonyl addition only. Original page URL returns 404.'),
 'hydride':('partial','partial','Acetone hydride-addition motif omits aluminum coordination/speciation and uses free H− shorthand; not the complete three-stage reagent model.'),
 'grignard':('representative','complete','Generic ketone/RMgX and water hydrolysis; card uses benzaldehyde/CH3MgBr followed by hydronium work-up.'),
 'cyanohydrin':('representative','complete','Ethanal rather than benzaldehyde; the cyanide-addition/protonation sequence is analogous.'),
 'acyl':('representative','complete','Generic RCOCl and R′O−; R=CH3 and R′=CH3 recover the card. Original page URL returns 404.'),
 'epoxide':('representative','complete','Substituted epoxide + ethoxide/ethanol, not ethylene oxide + methoxide/acid work-up.'),
 'aldol':('representative','complete','Generic ketone aldol addition; the card uses acetaldehyde.'),
 'radical-add':('representative','complete','Generic initiating R radical and ethene chain growth, not specifically methyl radical. Initiation/termination also appear.'),
 'radical-combine':('pending','mismatch','Image depicts Br-atom transfer from Br2 to a carbon radical, not combination of two methyl radicals.'),
 'radical-chain':('representative','complete','Generic CR3 radical/alkane, not explicitly methane. Only propagation is compared.'),
 'diels-alder':('exact','complete','Butadiene + ethene to cyclohexene and three cyclic arrows match.'),
 'claisen':('representative','complete','Aromatic Claisen: allyl phenyl ether rearranges and rearomatizes; card is allyl vinyl ether to pent-4-enal.'),
 'electrocyclic':('representative','partial','Substituted (E,E)-diene frontier-orbital/conrotation diagram; card is unsubstituted butadiene. Electron-pair flow is not fully depicted.'),
 'e1cb-dehydration':('representative','partial','Generic carbanion/X elimination; no carbonyl stabilization or specific diacetone-alcohol/OH group.'),
 'alkene-bromination':('representative','complete','Substituted alkene bromonium/anti opening, not ethene. Bridge formation is condensed in the drawing.'),
 'halohydrin':('pending','unreviewed','Image fetch rate-limited/access-blocked. File page describes an NBS scheme, whereas the card uses Br2/water; exactness not established.'),
 'nitration-benzene':('pending','unreviewed','Image fetch rate-limited/access-blocked; file-page metadata is not visual verification.'),
 'fischer-esterification':('pending','unreviewed','Image fetch rate-limited/access-blocked; substrate match and proton-relay coverage remain unreviewed.'),
 'imine-formation':('pending','unreviewed','Downloaded SVG rendered with unreadable molecular labels in the inspection renderer. Exact substrate and arrow coverage could not be verified.'),
 'aldol-condensation':('pending','unreviewed','Image fetch rate-limited/access-blocked. The filename alone does not establish full five-stage coverage.'),
 'acid-epoxide':('representative','complete','Tertiary-substituted epoxide/HCl gives attack at its tertiary site; this cannot establish regioselectivity of propylene oxide.'),
}

RESEARCH = {
 'proton-transfer':'Solvent relay and pKa standard-state/temperature metadata are not a computed microscopic pathway.',
 'lewis':'G1 is the inherited approach convention despite boron pyramidalization.',
 'sn2':'Literature calculations concern chloride + A–Cl, not hydroxide + methyl bromide.',
 'williamson':'Exact substrate illustration and solution/counterion effects remain to be established.',
 'sn1-core':'Generic core is a limiting model; explicit-solvent iPrCl literature does not establish this two-step pathway.',
 'sn1-water':'Ion-pair structure and E1 competition are not resolved by the textbook mechanism.',
 'hbr':'1111 retains the inherited dominant-bond convention despite accompanying H–Br cleavage and π redistribution.',
 'hydration':'Microscopic solvent participation and a corrected exact external figure remain open.',
 'e2':'1133 remains a candidate; anti/syn competition depends on actual conformers.',
 'e1':'1133 is a candidate for deprotonation/π formation; solvent and ion pairs are unresolved.',
 'carbonyl-add':'Generic local event, not a complete neutral-product preparation; 1113 remains candidate.',
 'hydride':'Discrete AlH4− precoordination is an unvalidated schematic assumption. Aggregation and hydrolysis require research.',
 'grignard':'Aggregation, Schlenk equilibria and grouped work-up are unresolved; the monomer contact model is provisional.',
 'cyanohydrin':'Acetone attack-angle data are analogous, not benzaldehyde results.',
 'acyl':'A discrete tetrahedral intermediate for this highly reactive pair is a teaching assumption; check concerted alternatives.',
 'epoxide':'Actual solvent and order of acid work-up must be retained when comparing paths.',
 'aldol':'1122 for enolate formation is a dominant proton-transfer convention; delocalization is not encoded separately.',
 'radical-add':'One propagation event only; spin density and initiation conditions are not computed.',
 'radical-combine':'Only a spin-compatible radical pair forms the singlet product directly.',
 'radical-chain':'Propagation only; initiation, termination and further chlorination are outside this card.',
 'diels-alder':'Numerical model uses acrolein, not ethene; radical-cation data cannot inherit 1333.',
 'claisen':'ELF conclusion checked at abstract level; full electronic method/basis still needs inspection.',
 'electrocyclic':'Thermal symmetry rule retained; closure feasibility and equilibrium are separate questions.',
 'e1cb-dehydration':'1133 fits bond redistribution but the codebook example refers to base attack; here the leaving-group event starts from enolate.',
 'alkene-bromination':'1133 is a retained candidate: polar bridging is not a pericyclic O3 process; codebook examples do not explicitly cover it.',
 'halohydrin':'Same 1133 boundary as bromination; Br2/water must not be equated with an NBS scheme.',
 'nitration-benzene':'1133 at arene attack/rearomatization is broader than the codebook examples; preserve candidate status pending codebook discussion.',
 'fischer-esterification':'The proton relay is grouped; its displayed 1122 refers to component proton transfers, not a verified single event.',
 'imine-formation':'1113 for iminium dehydration extends the carbonyl-elimination analogy to C=N; retained as candidate, not a taxonomy change.',
 'aldol-condensation':'Enolate and E1cB steps retain their convention/candidate boundaries; dehydration depends on conditions.',
 'acid-epoxide':'Corrected HCl/ether major pathway attacks primary carbon; do not generalize tertiary-epoxide selectivity to this substrate.',
}


def apply_review(reactions, sources):
    R={r['id']:r for r in reactions}
    r=R['acid-epoxide']
    r.update(name='Acid-promoted epoxide opening', equation='propylene oxide + HCl → ClCH₂CH(OH)CH₃ (major product)',
        conditions='HCl in ether; chloride is the nucleophile. This is acid-promoted, not an acid-regenerating catalytic cycle.',
        summary='Protonation followed by chloride attack at the primary carbon gives mainly 1-chloropropan-2-ol.',
        scope='OpenStax 18.5 gives HCl/ether opening of 1,2-epoxypropane mainly at its primary carbon. Tertiary-substituted epoxides can favor attack at the more substituted site; mixtures and solvent effects remain possible.')
    r['steps']=r['steps'][:2]
    r['steps'][0].update(equation='propylene oxide + HCl ⇌ protonated propylene oxide + Cl⁻',flow='Epoxide oxygen donates a lone pair to H of HCl; the H–Cl pair returns to chloride. The epoxide oxygen now has three bonds and formal charge +1.')
    r['steps'][1].update(equation='protonated propylene oxide + Cl⁻ → ClCH₂CH(OH)CH₃',
        flow='Chloride attacks the primary CH₂ carbon from the back of its C–O bond. That bond pair returns to oxygen, leaving a neutral alcohol directly; no additional deprotonation is needed.',
        geometry='Backside opening occurs at the primary carbon, which is not a stereocenter. The original secondary carbon retains its C–O bond.',
        orbital='n(Cl⁻) → σ*(Cprimary–O)',diagram='pending')
    r['facts']=[['Regioselectivity','For this HCl/ether example, the primary site is attacked preferentially.'],['Charge balance','Protonated epoxide (+1) + Cl⁻ (−1) → neutral chlorohydrin.'],['Acid balance','One HCl is consumed; chloride attack directly neutralizes the oxonium oxygen.']]
    R['epoxide']['conditions']='Methoxide opening, followed by a separate aqueous acid work-up.'
    R['epoxide']['steps'][1]['flow']='The alkoxide oxygen takes H from hydronium during work-up; the hydronium O–H bond pair returns to water.'
    R['aldol']['steps'][0]['equation']='CH₃CHO + HO⁻ ⇌ ⁻CH₂CHO + H₂O'
    R['aldol']['steps'][1]['equation']='⁻CH₂CHO + CH₃CHO → CH₃CH(O⁻)CH₂CHO'
    R['aldol']['scope']+=' The formula ⁻CH₂CHO is the carbon-anion resonance contributor of the enolate, not a localized isolated species.'
    R['halohydrin']['equation']='CH₃CH=CH₂ + Br₂ + 2 H₂O → BrCH₂CH(OH)CH₃ + H₃O⁺ + Br⁻'
    R['e1']['quantumData']['descriptors']=['Ionization and deprotonation paths in the stated solvent','Charge distribution and β-C–H donation into the carbocation p orbital']
    R['e1cb-dehydration']['quantumData']['descriptors']=['Conjugate-base stabilization and leaving-group loss along separate coordinates','Enolate charge delocalization and C=C/C–O bond-order changes']
    R['sn2']['scope']='Methyl carbon is achiral and has no β-carbon, so ordinary E2 elimination is unavailable for this substrate. Steric substitution/elimination competition applies to other alkyl substrates.'
    R['nitration-benzene']['steps'][0]['flow']='The hydroxyl oxygen of nitric acid accepts a proton from sulfuric acid; the sulfuric-acid O–H bond pair returns to its oxygen, giving HSO₄⁻.'
    R['nitration-benzene']['steps'][1]['flow']='The N–OH₂ bond pair goes to the departing water oxygen; a lone pair on the negatively charged remaining oxygen forms the second N=O bond, giving linear NO₂⁺.'
    R['nitration-benzene']['steps'][2]['flow']='A benzene π pair forms C–N with nitronium nitrogen while one N=O π pair shifts to oxygen to preserve nitrogen’s octet. The arenium ion is one delocalized intermediate; nitro is represented as N⁺/O⁻.'
    R['fischer-esterification']['steps'][3]['orbital']='An oxygen lone pair forms π(C=O), coupled to σ(C–OH₂⁺) cleavage.'
    R['imine-formation']['steps'][4]['orbital']='An N lone pair forms π(C=N), coupled to σ(C–OH₂⁺) cleavage.'
    R['imine-formation']['steps'][4]['equation']='(CH₃)₂C(OH₂⁺)(NHCH₃) → (CH₃)₂C=N⁺(H)CH₃ + H₂O'
    # Mismatched local motifs are explicitly pending until a correct molecular drawing is available.
    for rid,indices in {'e1cb-dehydration':[0,1],'alkene-bromination':[0], 'halohydrin':[0], 'nitration-benzene':[1,2,3], 'imine-formation':[4], 'aldol-condensation':[4]}.items():
        for i in indices:R[rid]['steps'][i]['diagram']='pending'
    # Neutral nucleophile/activated carbonyl needs different formal-charge labels.
    for rid in ['fischer-esterification','imine-formation']:R[rid]['steps'][1]['diagram']='pending'
    R['hydride']['steps'][0]['title']='Proposed carbonyl–aluminum encounter complex'
    R['hydride']['scope']+=' This precoordination picture is provisional, not an established discrete intermediate: AlH₄⁻ is not simply a free Lewis-acidic aluminum center. Aqueous work-up is grouped and does not describe subsequent Al–H hydrolysis/H₂ evolution.'
    R['hydride']['mechanismComplete']=False
    for r in reactions:
        r['audit']={'date':'2026-10-13','scope':'Editorial review against unchanged v0.2.6 codebook; not computational validation','researchNeeded':RESEARCH[r['id']]}
        grouped={'hydride':{2},'grignard':{2},'fischer-esterification':{2}}
        r['mechanismNote']='Pathway at the stated teaching resolution; inspect scope and event notes. This is not a claim that each listed stage is a verified elementary event.'
        if r['id'] in ['carbonyl-add','radical-add','radical-chain','sn1-core']:
            r['mechanismNote']+=' This entry covers only the stated local event, propagation cycle or formal core.'
        for i,s in enumerate(r['steps']):
            s['eventKind']='grouped-stage' if i in grouped.get(r['id'],set()) else 'elementary-model'
            s['assignmentStatus']='candidate' if s['code'] in ['1113','1133','2222'] or s['eventKind']=='grouped-stage' or r['id']=='hydride' else 'consistent-with-convention'
            s['assignmentNote']=RESEARCH[r['id']]
            if s['eventKind']=='grouped-stage':s['assignmentNote']+=' The code labels the dominant component process; no unique elementary-event code is established for the whole grouped stage.'
            reorg={'1111':'Principal bond formation or cleavage; accompanying changes remain in the electron-flow description.', '1122':'Replacement of a bond to H or C; read the flow for delocalization or accompanying metal–O cleavage.', '1113':'Candidate for tetrahedral addition or elimination with π-bond redistribution.', '1133':'Candidate for coupled polar bond redistribution; the individual bond changes are described above.', '2211':'Principal radical bond formation; a π bond may also change.', '1333':'Multiple bonds reorganize in a concerted pericyclic pathway.', '2222':'Candidate for H/halogen atom transfer between radical reaction centers.'}[s['code']]
            s['why']=['Open-shell reactant(s); product spin may differ.' if s['code'][0]=='2' else 'Closed-shell electron-pair model for this event.',s['orbital'],reorg,s['geometry']]
            s['diagramScope']='partial'
        match,coverage,note=FIGURES[r['id']]
        f=r['figure'];f.update(match=match,coverage=coverage,reviewNote=note,reviewed=coverage!='unreviewed',rightsStatus='unconfirmed',license='Reuse permission not established; external reference retained.',display=False)
        if r['id'] in ['sn2','sn1-core','sn1-water','grignard','acyl']:
            f.update(rightsStatus='source-license-checked',license='CC BY-NC-SA 4.0; unmodified source image',licenseUrl='https://creativecommons.org/licenses/by-nc-sa/4.0/',display=True)
        if r['id'] in ['e1','e1cb-dehydration','alkene-bromination','halohydrin','nitration-benzene','fischer-esterification']:
            f.update(rightsStatus='source-license-checked',license='Public domain (file-page declaration)',licenseUrl=f['href'],display=f['reviewed'])
        if r['id'] in ['imine-formation','aldol-condensation']:
            f.update(rightsStatus='source-license-checked',license='CC BY-SA 4.0; unmodified source image',licenseUrl='https://creativecommons.org/licenses/by-sa/4.0/',display=f['reviewed'])
        if r['id']=='sn2':f['credit']='Xin Liu · Organic Chemistry I · KPU Pressbooks'
        if r['id'] in ['sn1-core','sn1-water','grignard','acyl']:f['credit']='John McMurry / OpenStax · David Tully adaptation · NC State Pressbooks'
        if r['id']=='carbonyl-add':f['href']='https://www.chem.ucla.edu/~harding/IGOC/N/nucleophilic_addition.html'
        if r['id']=='acyl':f['href']='https://openstax.org/books/organic-chemistry/pages/21-2-nucleophilic-acyl-substitution-reactions'
        f['alt']=f'{match.capitalize()} illustration: {r["name"]}. {note}'
        q=r['quantumData'];q['performedCalculations']=[]
        q['evidenceTypes']=(['published-numerical'] if q['literatureCases'] else [])+(['published-qualitative'] if q['literatureInsights'] else [])+['proposed-not-performed']
    for rid in ['proton-transfer','lewis','radical-combine','acid-epoxide']:
        r=R[rid]
        r['figure']['priorReference']=deepcopy(r['figure'])
        r['figure'].update(src='mechanisms/'+rid+'.svg', href='mechanisms/'+rid+'.svg', match='exact', coverage='complete', reviewed=True, display=True,
            reviewNote='Original drawing of the stated model: reactants, formal charges, electron-flow arrows and product. No calculated geometry is implied.',
            rightsStatus='original',license='Original SORG Atlas illustration · CC BY-NC-SA 4.0',licenseUrl='https://creativecommons.org/licenses/by-nc-sa/4.0/',
            credit='SORG Atlas · original SVG',alt='Exact mechanism illustration: '+r['name'])
    sources['bromination']['url']='https://openstax.org/books/organic-chemistry/pages/8-2-halogenation-of-alkenes-addition-of-x2'
    sources['bromination']['title']='8.2 · Halogenation of alkenes: addition of X₂'
    for s in sources.values():
        s.pop('checked',None)
        s['reviewStatus']='Link requested during QC; reachability is recorded separately and does not establish content verification.'
    for k in ['acid','epoxide','epoxideacid','bromination']:
        sources[k]['reviewStatus']='Relevant source passage inspected during QC on 2026-10-13.'
    for k in ['qc_sn2','qc_da_ion','qc_attack_angle']:
        sources[k]['reviewStatus']='Quoted numerical claims and method checked in primary-source tables/text on 2026-10-13.'
    for k in ['qc_competition','qc_borderline']:
        sources[k]['reviewStatus']='Model, reported conclusion and energy/geometry method checked in indexed primary-source text; full analysis settings remain incomplete.'
    for k in ['qc_claisen_elf','qc_nitration_solvent']:
        sources[k]['reviewStatus']='Primary abstract checked; full electronic-structure method and basis not verified.'
    sources['qc_coupling_method']['reviewStatus']='Bibliographic identity checked against the authors’ institutional publication record; full derivation not reviewed.'
    for r in reactions:
        for c in r['quantumData']['literatureCases']:
            c['verification']='Numerical transcription checked against primary-source tables/text, 2026-10-13; calculations not reproduced.'
        for x in r['quantumData']['literatureInsights']:
            x['verification']=sources[x['source']]['reviewStatus']
    R['sn2']['quantumData']['literatureCases'][0]['method']+=' Fragments: singlet Cl⁻ (charge −1) and neutral singlet A–Cl; total charge −1, singlet. Strain is relative to the isolated equilibrium fragments; no solvent model.'
    R['diels-alder']['quantumData']['literatureCases'][0]['method']+=' Gas-phase model, no solvent term. Neutral pair: charge 0, singlet; radical-cation pair: charge +1, doublet (unrestricted). Butadiene remains a neutral singlet fragment.'
    x=R['sn1-core']['quantumData']['literatureInsights'][0]
    x['limits']='The card is a generic R₃C–X/anionic-nucleophile two-event core. The paper instead models secondary isopropyl chloride reacting with water; it does not validate the card’s discrete carbocation pathway.'
    for rid in ['carbonyl-add','cyanohydrin']:
        x=R[rid]['quantumData']['literatureInsights'][0]
        x['method']='Relaxed distance/angle scans: M06-2X/6-311+G(d,p), Gaussian 16. Single-point ASM/EDA: ZORA-M06-2X/TZ2P, ADF, all-electron, VERYGOOD integration. Gas-phase CN⁻ (charge −1, singlet) + neutral singlet acetone; total charge −1, singlet.'
        x['finding']='The model’s preferred C(CN)–C(carbonyl)–O angle is about 111°. At smaller angles Pauli repulsion limits approach; at larger angles acetone deformation costs rise. The balance, rather than overlap alone, sets the trajectory.'
        x['location']='Computational Methods; Figures 2 and 9'
        if 'published-numerical' not in R[rid]['quantumData']['evidenceTypes']:R[rid]['quantumData']['evidenceTypes'].insert(0,'published-numerical')
    for rid in ['sn2','e2']:
        x=R[rid]['quantumData']['literatureInsights'][0]
        x['method']+=' This specifies the energy/geometry protocol; the full orbital/activation-strain analysis settings have not been independently verified in this audit.'
    for rid in ['claisen','nitration-benzene']:
        R[rid]['quantumData']['literatureInsights'][0]['method']+=' Full electronic method and basis not verified in this audit; no numerical results are transcribed.'
