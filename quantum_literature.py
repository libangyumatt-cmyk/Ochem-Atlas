"""Transcribed electronic-structure results with explicit model boundaries.

Numbers below are from the indicated primary articles and tables. They are not
SORG scores, calculations performed by this project, or rate constants.
"""

CASES = {
    'sn2': [{
        'title': 'SN2 electronic-structure comparison across C, N, O, and F centers',
        'model': 'Cl⁻ + A–Cl, with A–Cl = CH₃Cl, NH₂Cl, OHCl, or FCl; gas phase.',
        'relation': 'Related benchmark. This card uses HO⁻ + CH₃Br, so none of these numbers describes its substrate.',
        'method': 'ZORA-OLYP/TZ2P; activation-strain analysis at the symmetric transition state for C, N, O and at the transition complex for F. The vacant σ*(A–Cl) energies refer to the isolated substrates under the authors’ orbital convention.',
        'columns': ['A–Cl substrate', 'σ*(A–Cl) (eV)', 'ΔEstrain (kcal/mol)', 'ΔEinteraction (kcal/mol)', 'Structure'],
        'rows': [
            ['CH₃Cl', '−5.13', '+31.6', '−31.9', 'TS'],
            ['NH₂Cl', '−6.96', '+25.7', '−34.9', 'TS'],
            ['OHCl', '−8.95', '+26.1', '−37.9', 'TS'],
            ['FCl', '−11.08', '+27.7', '−44.5', 'transition complex'],
        ],
        'interpretation': 'The acceptor σ* orbital is lower in this series while the fragment interaction becomes more stabilizing. These are a specified orbital energy and an interaction-energy decomposition, not a transferable scalar “coupling degree.”',
        'limits': 'Orbital energies depend on the method and orbital convention; the interaction term depends on the chosen fragments and geometry. The F entry is a transition complex rather than the same kind of stationary point as the first three. Values transcribed from Tables 3 and 4; no value for HO⁻ + CH₃Br is implied.',
        'source': 'qc_sn2',
        'location': 'Tables 3–4',
    }],
    'diels-alder': [{
        'title': 'Orbital interaction and electron donation in a Diels–Alder model',
        'model': '1,3-Butadiene + acrolein (neutral O) versus 1,3-butadiene + acrolein radical cation (O•⁺).',
        'relation': 'Related dienophile. The teaching reaction on this card uses ethene, and the radical-cation pathway is a distinct open-shell mechanism.',
        'method': 'ZORA-(U)BP86/TZ2P; fragments are butadiene and acrolein/acrolein radical cation. EDA evaluated at matched transition-state-like geometries with forming C(diene)···Cβ(dienophile) = 2.203 Å.',
        'columns': ['Dienophile state', 'ΔEstrain (kcal/mol)', 'ΔEinteraction (kcal/mol)', 'ΔEPauli (kcal/mol)', 'ΔEorbital (kcal/mol)'],
        'rows': [
            ['Neutral acrolein', '+14.6', '−3.2', '+70.8', '−41.3'],
            ['Acrolein radical cation', '+9.5', '−40.6', '+52.0', '−68.8'],
        ],
        'interpretation': 'At the matched geometry, ionization changes the EDA orbital term by −27.5 kcal/mol and reduces Pauli repulsion by 18.8 kcal/mol. In the open-shell case, the butadiene π-HOMO and acrolein-cation SOMO have reported overlap S = 0.05 and about 0.7 electron donated into the SOMO under this analysis. The neutral path is concerted asynchronous; the radical-cation path becomes stepwise.',
        'limits': 'ΔEorbital is the total EDA orbital-interaction term, S is a dimensionless overlap, and 0.7 electron is a method-specific charge-transfer analysis. None is a diabatic electronic-coupling matrix element H_DA or an intrinsic SORG score. The radical-cation pathway is not assigned the neutral card’s 1333 code.',
        'source': 'qc_da_ion',
        'location': 'Table 1 and orbital analysis',
    }],
}

# Literature conclusions are indexed by the reaction they can illuminate. The
# cited model and its limitations travel with every card; these are not results
# computed for the teaching equation unless the model exactly matches it.
INSIGHTS = {
    'sn2': [
        ('qc_competition', 'HOO⁻(H₂O)n + CH₃CH₂Cl, n = 0–4', 'CCSD(T)/aug-cc-pVTZ energies on MP2/6-311++G(d,p) geometries; activation-strain and molecular-orbital analyses.', 'For this microsolvated ethyl chloride network, backside SN2 is preferred to anti-E2, and adding water increases the preference. E2 requires greater characteristic substrate distortion; solvation attenuates the fragment interaction.', 'The teaching card is HO⁻ + CH₃Br, so the computed preference and energies do not transfer.', 'Abstract; Fig. 4; activation-strain analysis'),
    ],
    'e2': [
        ('qc_competition', 'HOO⁻(H₂O)n + CH₃CH₂Cl, n = 0–4', 'CCSD(T)/aug-cc-pVTZ//MP2/6-311++G(d,p); activation-strain and MO analysis.', 'The computed anti-E2 pathway has more characteristic distortion than backside SN2 for this model. Microsolvation weakens nucleophile–substrate interaction and changes the relative pathway preference.', 'This is a model comparison, not a calculated result for the base and leaving group in this E2 teaching card.', 'Abstract; Fig. 4; activation-strain analysis'),
    ],
    'sn1-core': [
        ('qc_borderline', 'Isopropyl chloride hydrolysis with explicit water clusters and continuum solvent', 'M06-2X/aug-cc-pVDZ geometry and frequency calculations; explicit and hybrid explicit–implicit solvation.', 'The computed borderline substitution has a solvent-assisted, loose transition structure with carbocation character; changing the placement of nearby water changes the mechanistic description.', 'The card uses tert-butyl bromide, a different substrate and leaving group. This study does not establish its pathway or a universal SN1/SN2 boundary.', 'Abstract and solvent-configuration analysis'),
    ],
    'carbonyl-add': [
        ('qc_attack_angle', 'CN⁻ attack on acetone', 'Two-dimensional distortion–interaction/activation-strain and EDA analysis versus attack distance and angle.', 'The model favors an attack near 111°. Its angular preference reflects a balance of substrate distortion and fragment interactions; steric Pauli repulsion contributes at larger angles. An orbital-overlap picture alone does not determine the trajectory.', 'This card uses a different carbonyl/nucleophile combination. The reported angle is model specific.', 'Abstract; two-dimensional EDA; Fig. 9'),
    ],
    'cyanohydrin': [
        ('qc_attack_angle', 'CN⁻ attack on acetone', 'Two-dimensional distortion–interaction/activation-strain and EDA analysis versus attack distance and angle.', 'In the CN⁻/acetone model the preferred carbonyl approach is near 111°, set by both deformation and interaction terms, including Pauli repulsion at larger angles.', 'This card uses benzaldehyde + HCN and includes proton transfer. The acetone attack angle and surface cannot be assigned to benzaldehyde.', 'Abstract; two-dimensional EDA; Fig. 9'),
    ],
    'claisen': [
        ('qc_claisen_elf', 'Thermal allyl vinyl ether rearrangement to allylacetaldehyde', 'Theoretical reaction-path bonding evolution tracked with the electron localization function (ELF).', 'The C3–O bond-breaking and C1–C5 bond-forming electron-density changes do not occur simultaneously. A concerted pathway therefore need not be synchronous at the level of bonding evolution.', 'The paper studies the same parent rearrangement, but the ELF topology depends on the electronic-structure setup and does not supply a universal timing scale.', 'Abstract; ELF bonding-evolution analysis'),
    ],
    'nitration-benzene': [
        ('qc_nitration_solvent', 'Benzene + nitronium in sulfuric acid or water', 'RISM-SCF-cSED: solute electronic structure and liquid solvation determined self-consistently.', 'The sulfuric-acid solvation structure changes substantially during C–N bond formation and affects the free-energy surface. Valence-electronic analysis distinguishes important resonance contributions to the Wheland intermediate in gas and solution.', 'The result concerns the specified solvent models and method; it does not endorse a single charge or resonance weight for every mixed-acid composition.', 'Abstract; solvation free-energy and valence-electronic analyses'),
    ],
}

PROTOCOLS = {
    'Acid–base reactions': ('Model the same acid, base, counterion, protonation state and solvent; include alternative H-bonded relay structures.', 'Optimize reactant complex, proton-transfer transition structure and products; verify vibrational modes and trace the reaction path. Compare electron density, H–donor/acceptor bond orders and an explicitly defined donor–acceptor partition.'),
    'Substitution reactions': ('Fix the named substrate, nucleophile, leaving group, counterion and solvent; enumerate backside, ionization and competing conformers where relevant.', 'Optimize reactant complexes, intermediates and transition structures; confirm one imaginary mode and connecting IRC. At matched C–leaving-group distances, compare activation strain and EDA with stated fragments; inspect σ* occupancy and charge distribution.'),
    'Elimination reactions': ('Enumerate anti and syn β-H conformers plus competing substitution with the same reactants and solvent.', 'Locate each transition structure and its IRC; track C–H, C–LG and C=C distances, torsion, charge and bond orders. Compare activation strain and fragment interactions at matched reaction-coordinate geometries.'),
    'Alkene reactions': ('Include the named electrophile, its formation if relevant, counterion and the solvent/nucleophile that captures the intermediate.', 'Optimize each proposed ion pair or bridged intermediate and transition structure; verify frequencies and IRC. Follow charge transfer, spin if relevant, and C–C/C–X bond orders along each path.'),
    'Carbonyl reactions': ('Represent the exact carbonyl, nucleophile, protonation state, counterion and work-up as separate modeled events.', 'Scan nucleophile–carbonyl distance and approach angle, optimize intermediate/transition structures and check modes/IRC. Compare distortion and EDA at matched geometries; track π*(C=O), density and C–Nu/C–O bond orders.'),
    'Radical reactions': ('Define the correct spin multiplicity for each radical, substrate and product; search conformers and possible spin-state alternatives.', 'Use a suitable open-shell method and inspect spin contamination; locate stationary points and reaction path. Follow SOMO, spin density and breaking/forming bond orders; check a higher-level or multireference treatment if diagnostics require it.'),
    'Pericyclic reactions': ('Search relevant diene, dienophile or rearranging-substrate conformations and competing concerted/stepwise paths; define electronic state.', 'Optimize transition structure(s), confirm a single imaginary mode and trace both IRC directions. Track each forming/breaking bond and ELF or equivalent density topology; inspect orbital phases and test the wavefunction if near-degeneracy appears.'),
    'Aromatic substitution': ('Include electrophile generation, counterion, acid composition and solvent around the aromatic substrate.', 'Optimize encounter complex, σ-complex, attack and deprotonation structures; verify each proposed connection. Compare solvation-sensitive charge distribution, π density and bond orders through the reaction path.'),
}


def _insight(record):
    source, model, method, finding, limit, location = record
    return dict(model=model, method=method, finding=finding, limits=limit, source=source, location=location)


def attach_literature(reactions):
    for reaction in reactions:
        cases = CASES.get(reaction['id'], [])
        q = reaction['quantumData']
        q['literatureCases'] = cases
        q['literatureInsights'] = [_insight(x) for x in INSIGHTS.get(reaction['id'], [])]
        protocol = PROTOCOLS[reaction['family']]
        q['proposedProtocol'] = {'model': protocol[0], 'workflow': protocol[1]}
        for insight in q['literatureInsights']:
            if insight['source'] not in reaction['sources']:
                reaction['sources'].append(insight['source'])
        if cases:
            q['status'] = 'literature-related-numerical'
            q['note'] = (
                'The table contains published calculations for the explicitly named model, '
                'not new values calculated for this teaching entry. Do not transfer the numbers '
                'to another substrate, solvent, or orbital convention.'
            )
            for case in cases:
                if case['source'] not in reaction['sources']:
                    reaction['sources'].append(case['source'])
        elif q['literatureInsights']:
            q['status'] = 'literature-related-qualitative'
            q['note'] = ('The conclusion below comes from the named published calculation. '
                         'It is not a new calculation for this teaching entry; read its model and limits.')
