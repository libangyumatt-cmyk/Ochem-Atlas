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


def attach_literature(reactions):
    for reaction in reactions:
        cases = CASES.get(reaction['id'], [])
        reaction['quantumData']['literatureCases'] = cases
        if cases:
            reaction['quantumData']['status'] = 'literature-related-numerical'
            reaction['quantumData']['note'] = (
                'The table contains published calculations for the explicitly named model, '
                'not new values calculated for this teaching entry. Do not transfer the numbers '
                'to another substrate, solvent, or orbital convention.'
            )
            for case in cases:
                if case['source'] not in reaction['sources']:
                    reaction['sources'].append(case['source'])
