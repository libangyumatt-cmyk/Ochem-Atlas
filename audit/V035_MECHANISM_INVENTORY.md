# v0.3.5 mechanism illustration inventory

Status is reviewed chemical coverage, not file existence. All original sources are retained in JSON, including rejected/representative references. “Missing” means no displayed reviewed image; existing written equations are retained. Inherited reviews are identified explicitly.

| Reaction | v0.3.4 status | Previously displayed | v0.3.5 status | Events | Focused event images |
|---|---|---|---|---:|---:|
| Proton transfer | complete | True | complete | 1 | 0 |
| Lewis acid–base association | complete | True | complete | 1 | 0 |
| SN2 substitution | complete | True | complete | 1 | 1 |
| Williamson ether synthesis | representative | False | complete | 1 | 1 |
| SN1: ionization & capture | representative | True | complete | 2 | 2 |
| SN1 solvolysis | complete | True | complete | 3 | 3 |
| Electrophilic HBr addition | missing | False | complete | 2 | 2 |
| Acid-catalyzed hydration | scientifically inconsistent | False | complete | 3 | 3 |
| E2 elimination | complete | True | complete | 1 | 0 |
| E1 elimination | partial | True | complete | 2 | 2 |
| Carbonyl nucleophilic addition | complete | True | complete | 1 | 0 |
| Lithium aluminum hydride reduction | partial | False | partial | 3 | 0 |
| Grignard addition to an aldehyde | representative | True | representative | 3 | 0 |
| Cyanohydrin formation | representative | False | complete | 2 | 2 |
| Nucleophilic acyl substitution | representative | True | complete | 2 | 2 |
| Basic epoxide opening | representative | False | complete | 2 | 2 |
| Aldol addition | representative | False | complete | 3 | 3 |
| Radical alkene addition | representative | False | complete | 1 | 1 |
| Radical recombination | complete | True | complete | 1 | 0 |
| Radical chlorination: propagation | representative | False | complete | 2 | 2 |
| Diels–Alder cycloaddition | complete | True | complete | 1 | 0 |
| Claisen rearrangement | representative | False | complete | 1 | 1 |
| Thermal electrocyclic closure | representative | False | complete | 1 | 1 |
| E1cB dehydration | partial | True | complete | 2 | 2 |
| Bromination of an alkene | representative | True | complete | 2 | 2 |
| Halohydrin formation | missing | False | complete | 3 | 3 |
| Nitration of benzene | missing | False | complete | 4 | 4 |
| Fischer esterification | complete | True | complete | 5 | 5 |
| Imine formation from a ketone | complete | True | complete | 6 | 6 |
| Base-catalyzed aldol condensation | missing | False | complete | 5 | 5 |
| Acid-promoted epoxide opening | complete | True | complete | 2 | 0 |

## Proton transfer

Previous review: Original drawing of the stated model: reactants, formal charges, electron-flow arrows and product. No calculated geometry is implied.

Current: complete. Image: `mechanisms/proton-transfer.svg`.

- Event 1 · 1122 · complete: CH₃CO₂H + CN⁻ ⇌ CH₃CO₂⁻ + HCN
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Solvent relay and pKa standard-state/temperature metadata are not a computed microscopic pathway.

## Lewis acid–base association

Previous review: Original drawing of the stated model: reactants, formal charges, electron-flow arrows and product. No calculated geometry is implied.

Current: complete. Image: `mechanisms/lewis.svg`.

- Event 1 · 1111 · complete: NH₃ + BF₃ ⇌ H₃N⁺–BF₃⁻
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. G1 is the inherited approach convention despite boron pyramidalization.

## SN2 substitution

Previous review: Hydroxide + methyl bromide; reaction, electron arrows and transition structure match. Methyl carbon is achiral.

Current: complete. Image: `mechanisms/v035/sn2.svg`.

- Event 1 · 1122 · complete: HO⁻ + CH₃Br → CH₃OH + Br⁻
  Image: `mechanisms/v035/sn2-step-1.svg`. Authored focused structural SVG. Literature calculations concern chloride + A–Cl, not hydroxide + methyl bromide.

## Williamson ether synthesis

Previous review: Examples use ethoxide/ethyl bromide or methoxide/ethyl iodide, rather than methoxide/ethyl bromide.

Current: complete. Image: `mechanisms/v035/williamson.svg`.

- Event 1 · 1122 · complete: CH₃O⁻ + CH₃CH₂Br → CH₃OCH₂CH₃ + Br⁻
  Image: `mechanisms/v035/williamson-step-1.svg`. Authored focused structural SVG. Exact substrate illustration and solution/counterion effects remain to be established.

## SN1: ionization & capture

Previous review: Image is tert-butyl bromide solvolysis with water and a third deprotonation; card is a two-event generic anionic-nucleophile core.

Current: complete. Image: `mechanisms/v035/sn1-core.svg`.

- Event 1 · 1111 · complete: R₃C–X → R₃C⁺ + X⁻
  Image: `mechanisms/v035/sn1-core-step-1.svg`. Authored focused structural SVG. Generic core is a limiting model; explicit-solvent iPrCl literature does not establish this two-step pathway.

- Event 2 · 1111 · complete: R₃C⁺ + Nu⁻ → R₃C–Nu
  Image: `mechanisms/v035/sn1-core-step-2.svg`. Authored focused structural SVG. Generic core is a limiting model; explicit-solvent iPrCl literature does not establish this two-step pathway.

## SN1 solvolysis

Previous review: Tert-butyl bromide, water capture, oxonium and deprotonation match the three displayed events.

Current: complete. Image: `mechanisms/v035/sn1-water.svg`.

- Event 1 · 1111 · complete: (CH₃)₃CBr → (CH₃)₃C⁺ + Br⁻
  Image: `mechanisms/v035/sn1-water-step-1.svg`. Authored focused structural SVG. Ion-pair structure and E1 competition are not resolved by the textbook mechanism.

- Event 2 · 1111 · complete: (CH₃)₃C⁺ + H₂O → (CH₃)₃COH₂⁺
  Image: `mechanisms/v035/sn1-water-step-2.svg`. Authored focused structural SVG. Ion-pair structure and E1 competition are not resolved by the textbook mechanism.

- Event 3 · 1122 · complete: (CH₃)₃COH₂⁺ + H₂O → (CH₃)₃COH + H₃O⁺
  Image: `mechanisms/v035/sn1-water-step-3.svg`. Authored focused structural SVG. Ion-pair structure and E1 competition are not resolved by the textbook mechanism.

## Electrophilic HBr addition

Previous review: The upper propene-to-2-bromopropane branch matches. The lower primary-carbocation branch is not a validated minor pathway for this card.

Current: complete. Image: `mechanisms/v035/hbr.svg`.

- Event 1 · 1111 · complete: CH₃CH=CH₂ + HBr → (CH₃)₂CH⁺ + Br⁻
  Image: `mechanisms/v035/hbr-step-1.svg`. Authored focused structural SVG. 1111 retains the inherited dominant-bond convention despite accompanying H–Br cleavage and π redistribution.

- Event 2 · 1111 · complete: (CH₃)₂CH⁺ + Br⁻ → CH₃CHBrCH₃
  Image: `mechanisms/v035/hbr-step-2.svg`. Authored focused structural SVG. 1111 retains the inherited dominant-bond convention despite accompanying H–Br cleavage and π redistribution.

## Acid-catalyzed hydration

Previous review: Propene hydration is intended, but the terminal carbon remains labeled CH2 after protonation instead of CH3; image withheld.

Current: complete. Image: `mechanisms/v035/hydration.svg`.

- Event 1 · 1111 · complete: CH₃CH=CH₂ + H₃O⁺ → (CH₃)₂CH⁺ + H₂O
  Image: `mechanisms/v035/hydration-step-1.svg`. Authored focused structural SVG. Microscopic solvent participation and a corrected exact external figure remain open.

- Event 2 · 1111 · complete: (CH₃)₂CH⁺ + H₂O → (CH₃)₂CHOH₂⁺
  Image: `mechanisms/v035/hydration-step-2.svg`. Authored focused structural SVG. Microscopic solvent participation and a corrected exact external figure remain open.

- Event 3 · 1122 · complete: (CH₃)₂CHOH₂⁺ + H₂O → (CH₃)₂CHOH + H₃O⁺
  Image: `mechanisms/v035/hydration-step-3.svg`. Authored focused structural SVG. Microscopic solvent participation and a corrected exact external figure remain open.

## E2 elimination

Previous review: Original condensed-structure pathway checked against every listed equation, charge, intermediate and electron-pair move; Fischer step 3 expands a grouped solvent relay. The diagram does not specify computed transition-state geometry.

Current: complete. Image: `mechanisms/e2.svg`.

- Event 1 · 1133 · complete: CH₃CHBrCH₃ + EtO⁻ → CH₂=CHCH₃ + EtOH + Br⁻
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. 1133 remains a candidate; anti/syn competition depends on actual conformers.

## E1 elimination

Previous review: Generic alkyl skeleton and X; solvent base and its protonated product are omitted.

Current: complete. Image: `mechanisms/v035/e1.svg`.

- Event 1 · 1111 · complete: (CH₃)₃CCl → (CH₃)₃C⁺ + Cl⁻
  Image: `mechanisms/v035/e1-step-1.svg`. Authored focused structural SVG. 1133 is a candidate for deprotonation/π formation; solvent and ion pairs are unresolved.

- Event 2 · 1133 · complete: (CH₃)₃C⁺ + H₂O → (CH₃)₂C=CH₂ + H₃O⁺
  Image: `mechanisms/v035/e1-step-2.svg`. Authored focused structural SVG. 1133 is a candidate for deprotonation/π formation; solvent and ion pairs are unresolved.

## Carbonyl nucleophilic addition

Previous review: Original condensed-structure pathway checked against every listed equation, charge, intermediate and electron-pair move; Fischer step 3 expands a grouped solvent relay. The diagram does not specify computed transition-state geometry.

Current: complete. Image: `mechanisms/carbonyl-add.svg`.

- Event 1 · 1113 · complete: R₂C=O + Nu⁻ → R₂C(O⁻)Nu
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Generic local event, not a complete neutral-product preparation; 1113 remains candidate.

## Lithium aluminum hydride reduction

Previous review: Acetone hydride-addition motif omits aluminum coordination/speciation and uses free H− shorthand; not the complete three-stage reagent model.

Current: partial. Image: `https://image3.slideserve.com/6508687/reduction-of-carbonyls1-l.jpg`.

- Event 1 · 1111 · partial: (CH₃)₂C=O + AlH₄⁻ ⇌ (CH₃)₂C=O→AlH₄⁻
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Discrete AlH4− precoordination is an unvalidated schematic assumption. Aggregation and hydrolysis require research.

- Event 2 · 1113 · partial: (CH₃)₂C=O→AlH₄⁻ → [(CH₃)₂CH–O–AlH₃]⁻
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Discrete AlH4− precoordination is an unvalidated schematic assumption. Aggregation and hydrolysis require research.

- Event 3 · 1122 · partial: [(CH₃)₂CH–O–AlH₃]⁻ + H₂O → (CH₃)₂CHOH + [AlH₃OH]⁻
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Discrete AlH4− precoordination is an unvalidated schematic assumption. Aggregation and hydrolysis require research. The code labels the dominant component process; no unique elementary-event code is established for the whole grouped stage.

## Grignard addition to an aldehyde

Previous review: Generic ketone/RMgX and water hydrolysis; card uses benzaldehyde/CH3MgBr followed by hydronium work-up.

Current: representative. Image: `https://ncstate.pressbooks.pub/app/uploads/sites/52/2023/11/image42-21.jpeg`.

- Event 1 · 1111 · representative: PhCHO + CH₃MgBr ⇌ PhCH=O→MgBrCH₃
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Aggregation, Schlenk equilibria and grouped work-up are unresolved; the monomer contact model is provisional.

- Event 2 · 1113 · representative: PhCH=O→MgBrCH₃ → PhCH(O–MgBr)CH₃
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Aggregation, Schlenk equilibria and grouped work-up are unresolved; the monomer contact model is provisional.

- Event 3 · 1122 · representative: PhCH(O–MgBr)CH₃ + H₃O⁺ → PhCH(OH)CH₃ + MgBr⁺ + H₂O
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Aggregation, Schlenk equilibria and grouped work-up are unresolved; the monomer contact model is provisional. The code labels the dominant component process; no unique elementary-event code is established for the whole grouped stage.

## Cyanohydrin formation

Previous review: Ethanal rather than benzaldehyde; the cyanide-addition/protonation sequence is analogous.

Current: complete. Image: `mechanisms/v035/cyanohydrin.svg`.

- Event 1 · 1113 · complete: PhCHO + CN⁻ → PhCH(O⁻)CN
  Image: `mechanisms/v035/cyanohydrin-step-1.svg`. Authored focused structural SVG. Acetone attack-angle data are analogous, not benzaldehyde results.

- Event 2 · 1122 · complete: PhCH(O⁻)CN + HCN → PhCH(OH)CN + CN⁻
  Image: `mechanisms/v035/cyanohydrin-step-2.svg`. Authored focused structural SVG. Acetone attack-angle data are analogous, not benzaldehyde results.

## Nucleophilic acyl substitution

Previous review: Generic RCOCl and R′O−; R=CH3 and R′=CH3 recover the card. Original page URL returns 404.

Current: complete. Image: `mechanisms/v035/acyl.svg`.

- Event 1 · 1113 · complete: CH₃COCl + CH₃O⁻ → CH₃C(O⁻)(OCH₃)Cl
  Image: `mechanisms/v035/acyl-step-1.svg`. Authored focused structural SVG. A discrete tetrahedral intermediate for this highly reactive pair is a teaching assumption; check concerted alternatives.

- Event 2 · 1113 · complete: CH₃C(O⁻)(OCH₃)Cl → CH₃CO₂CH₃ + Cl⁻
  Image: `mechanisms/v035/acyl-step-2.svg`. Authored focused structural SVG. A discrete tetrahedral intermediate for this highly reactive pair is a teaching assumption; check concerted alternatives.

## Basic epoxide opening

Previous review: Substituted epoxide + ethoxide/ethanol, not ethylene oxide + methoxide/acid work-up.

Current: complete. Image: `mechanisms/v035/epoxide.svg`.

- Event 1 · 1122 · complete: ethylene oxide + CH₃O⁻ → CH₃OCH₂CH₂O⁻
  Image: `mechanisms/v035/epoxide-step-1.svg`. Authored focused structural SVG. Actual solvent and order of acid work-up must be retained when comparing paths.

- Event 2 · 1122 · complete: CH₃OCH₂CH₂O⁻ + H₃O⁺ → CH₃OCH₂CH₂OH + H₂O
  Image: `mechanisms/v035/epoxide-step-2.svg`. Authored focused structural SVG. Actual solvent and order of acid work-up must be retained when comparing paths.

## Aldol addition

Previous review: Generic ketone aldol addition; the card uses acetaldehyde.

Current: complete. Image: `mechanisms/v035/aldol.svg`.

- Event 1 · 1122 · complete: CH₃CHO + HO⁻ ⇌ ⁻CH₂CHO + H₂O
  Image: `mechanisms/v035/aldol-step-1.svg`. Authored focused structural SVG. 1122 for enolate formation is a dominant proton-transfer convention; delocalization is not encoded separately.

- Event 2 · 1113 · complete: ⁻CH₂CHO + CH₃CHO → CH₃CH(O⁻)CH₂CHO
  Image: `mechanisms/v035/aldol-step-2.svg`. Authored focused structural SVG. 1122 for enolate formation is a dominant proton-transfer convention; delocalization is not encoded separately.

- Event 3 · 1122 · complete: CH₃CH(O⁻)CH₂CHO + H₂O ⇌ CH₃CH(OH)CH₂CHO + HO⁻
  Image: `mechanisms/v035/aldol-step-3.svg`. Authored focused structural SVG. 1122 for enolate formation is a dominant proton-transfer convention; delocalization is not encoded separately.

## Radical alkene addition

Previous review: Generic initiating R radical and ethene chain growth, not specifically methyl radical. Initiation/termination also appear.

Current: complete. Image: `mechanisms/v035/radical-add.svg`.

- Event 1 · 2211 · complete: CH₃• + CH₂=CH₂ → CH₃CH₂CH₂•
  Image: `mechanisms/v035/radical-add-step-1.svg`. Authored focused structural SVG. One propagation event only; spin density and initiation conditions are not computed.

## Radical recombination

Previous review: Original drawing of the stated model: reactants, formal charges, electron-flow arrows and product. No calculated geometry is implied.

Current: complete. Image: `mechanisms/radical-combine.svg`.

- Event 1 · 2211 · complete: CH₃• + •CH₃ → CH₃CH₃
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Only a spin-compatible radical pair forms the singlet product directly.

## Radical chlorination: propagation

Previous review: Generic CR3 radical/alkane, not explicitly methane. Only propagation is compared.

Current: complete. Image: `mechanisms/v035/radical-chain.svg`.

- Event 1 · 2222 · complete: Cl• + CH₄ → HCl + CH₃•
  Image: `mechanisms/v035/radical-chain-step-1.svg`. Authored focused structural SVG. Propagation only; initiation, termination and further chlorination are outside this card.

- Event 2 · 2222 · complete: CH₃• + Cl₂ → CH₃Cl + Cl•
  Image: `mechanisms/v035/radical-chain-step-2.svg`. Authored focused structural SVG. Propagation only; initiation, termination and further chlorination are outside this card.

## Diels–Alder cycloaddition

Previous review: Original condensed-structure pathway checked against every listed equation, charge, intermediate and electron-pair move; Fischer step 3 expands a grouped solvent relay. The diagram does not specify computed transition-state geometry.

Current: complete. Image: `mechanisms/diels-alder.svg`.

- Event 1 · 1333 · complete: CH₂=CH–CH=CH₂ + CH₂=CH₂ → cyclohexene
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Numerical model uses acrolein, not ethene; radical-cation data cannot inherit 1333.

## Claisen rearrangement

Previous review: Aromatic Claisen: allyl phenyl ether rearranges and rearomatizes; card is allyl vinyl ether to pent-4-enal.

Current: complete. Image: `mechanisms/v035/claisen.svg`.

- Event 1 · 1333 · complete: allyl vinyl ether → pent-4-enal
  Image: `mechanisms/v035/claisen-step-1.svg`. Authored focused structural SVG. ELF conclusion checked at abstract level; full electronic method/basis still needs inspection.

## Thermal electrocyclic closure

Previous review: Substituted (E,E)-diene frontier-orbital/conrotation diagram; card is unsubstituted butadiene. Electron-pair flow is not fully depicted.

Current: complete. Image: `mechanisms/v035/electrocyclic.svg`.

- Event 1 · 1333 · complete: 1,3-butadiene ⇌ cyclobutene
  Image: `mechanisms/v035/electrocyclic-step-1.svg`. Authored focused structural SVG. Thermal symmetry rule retained; closure feasibility and equilibrium are separate questions.

## E1cB dehydration

Previous review: Generic carbanion/X elimination; no carbonyl stabilization or specific diacetone-alcohol/OH group.

Current: complete. Image: `mechanisms/v035/e1cb-dehydration.svg`.

- Event 1 · 1122 · complete: CH₃COCH₂C(OH)(CH₃)₂ + HO⁻ ⇌ CH₃COCH⁻C(OH)(CH₃)₂ + H₂O
  Image: `mechanisms/v035/e1cb-dehydration-step-1.svg`. Authored focused structural SVG. 1133 fits bond redistribution but the codebook example refers to base attack; here the leaving-group event starts from enolate.

- Event 2 · 1133 · complete: CH₃COCH⁻C(OH)(CH₃)₂ → CH₃COCH=C(CH₃)₂ + HO⁻
  Image: `mechanisms/v035/e1cb-dehydration-step-2.svg`. Authored focused structural SVG. 1133 fits bond redistribution but the codebook example refers to base attack; here the leaving-group event starts from enolate.

## Bromination of an alkene

Previous review: Substituted alkene bromonium/anti opening, not ethene. Bridge formation is condensed in the drawing.

Current: complete. Image: `mechanisms/v035/alkene-bromination.svg`.

- Event 1 · 1133 · complete: CH₂=CH₂ + Br₂ → [CH₂–Br⁺–CH₂] + Br⁻
  Image: `mechanisms/v035/alkene-bromination-step-1.svg`. Authored focused structural SVG. 1133 is a retained candidate: polar bridging is not a pericyclic O3 process; codebook examples do not explicitly cover it.

- Event 2 · 1122 · complete: [CH₂–Br⁺–CH₂] + Br⁻ → BrCH₂CH₂Br
  Image: `mechanisms/v035/alkene-bromination-step-2.svg`. Authored focused structural SVG. 1133 is a retained candidate: polar bridging is not a pericyclic O3 process; codebook examples do not explicitly cover it.

## Halohydrin formation

Previous review: Image fetch rate-limited/access-blocked. File page describes an NBS scheme, whereas the card uses Br2/water; exactness not established.

Current: complete. Image: `mechanisms/v035/halohydrin.svg`.

- Event 1 · 1133 · complete: CH₃CH=CH₂ + Br₂ → [CH₃CH–CH₂–Br]⁺ + Br⁻
  Image: `mechanisms/v035/halohydrin-step-1.svg`. Authored focused structural SVG. Same 1133 boundary as bromination; Br2/water must not be equated with an NBS scheme.

- Event 2 · 1122 · complete: [CH₃CH–CH₂–Br]⁺ + H₂O → BrCH₂CH(OH₂⁺)CH₃
  Image: `mechanisms/v035/halohydrin-step-2.svg`. Authored focused structural SVG. Same 1133 boundary as bromination; Br2/water must not be equated with an NBS scheme.

- Event 3 · 1122 · complete: BrCH₂CH(OH₂⁺)CH₃ + H₂O ⇌ BrCH₂CH(OH)CH₃ + H₃O⁺
  Image: `mechanisms/v035/halohydrin-step-3.svg`. Authored focused structural SVG. Same 1133 boundary as bromination; Br2/water must not be equated with an NBS scheme.

## Nitration of benzene

Previous review: Image fetch rate-limited/access-blocked; file-page metadata is not visual verification.

Current: complete. Image: `mechanisms/v035/nitration-benzene.svg`.

- Event 1 · 1122 · complete: HNO₃ + H₂SO₄ ⇌ H₂NO₃⁺ + HSO₄⁻
  Image: `mechanisms/v035/nitration-benzene-step-1.svg`. Authored focused structural SVG. 1133 at arene attack/rearomatization is broader than the codebook examples; preserve candidate status pending codebook discussion.

- Event 2 · 1111 · complete: H₂NO₃⁺ → NO₂⁺ + H₂O
  Image: `mechanisms/v035/nitration-benzene-step-2.svg`. Authored focused structural SVG. 1133 at arene attack/rearomatization is broader than the codebook examples; preserve candidate status pending codebook discussion.

- Event 3 · 1133 · complete: C₆H₆ + NO₂⁺ → [C₆H₆NO₂]⁺
  Image: `mechanisms/v035/nitration-benzene-step-3.svg`. Authored focused structural SVG. 1133 at arene attack/rearomatization is broader than the codebook examples; preserve candidate status pending codebook discussion.

- Event 4 · 1133 · complete: [C₆H₆NO₂]⁺ + HSO₄⁻ → C₆H₅NO₂ + H₂SO₄
  Image: `mechanisms/v035/nitration-benzene-step-4.svg`. Authored focused structural SVG. 1133 at arene attack/rearomatization is broader than the codebook examples; preserve candidate status pending codebook discussion.

## Fischer esterification

Previous review: Original condensed-structure pathway checked against every listed equation, charge, intermediate and electron-pair move; Fischer step 3 expands a grouped solvent relay. The diagram does not specify computed transition-state geometry.

Current: complete. Image: `mechanisms/fischer-esterification.svg`.

- Event 1 · 1122 · complete: CH₃C(=O)OH + H₃O⁺ ⇌ CH₃C(=OH⁺)OH + H₂O
  Image: `mechanisms/fischer-esterification-step-1.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. The proton relay is grouped; its displayed 1122 refers to component proton transfers, not a verified single event.

- Event 2 · 1113 · complete: CH₃C(=OH⁺)OH + HOCH₂CH₃ → CH₃C(OH)(OH)(O⁺HCH₂CH₃)
  Image: `mechanisms/fischer-esterification-step-2.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. The proton relay is grouped; its displayed 1122 refers to component proton transfers, not a verified single event.

- Event 3 · 1122 · complete: CH₃C(OH)(OH)(O⁺HCH₂CH₃) ⇌ CH₃C(OH)(OH₂⁺)(OCH₂CH₃)
  Image: `mechanisms/fischer-esterification-step-3.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. The proton relay is grouped; its displayed 1122 refers to component proton transfers, not a verified single event. The code labels the dominant component process; no unique elementary-event code is established for the whole grouped stage.

- Event 4 · 1113 · complete: CH₃C(OH)(OH₂⁺)(OCH₂CH₃) → CH₃C(=OH⁺)OCH₂CH₃ + H₂O
  Image: `mechanisms/fischer-esterification-step-4.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. The proton relay is grouped; its displayed 1122 refers to component proton transfers, not a verified single event.

- Event 5 · 1122 · complete: CH₃C(=OH⁺)OCH₂CH₃ + H₂O ⇌ CH₃CO₂CH₂CH₃ + H₃O⁺
  Image: `mechanisms/fischer-esterification-step-5.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. The proton relay is grouped; its displayed 1122 refers to component proton transfers, not a verified single event.

## Imine formation from a ketone

Previous review: Original condensed-structure pathway checked against every listed equation, charge, intermediate and electron-pair move; Fischer step 3 expands a grouped solvent relay. The diagram does not specify computed transition-state geometry.

Current: complete. Image: `mechanisms/imine-formation.svg`.

- Event 1 · 1122 · complete: (CH₃)₂C=O + H₃O⁺ ⇌ (CH₃)₂C=OH⁺ + H₂O
  Image: `mechanisms/imine-formation-step-1.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. 1113 for iminium dehydration extends the carbonyl-elimination analogy to C=N; retained as candidate, not a taxonomy change.

- Event 2 · 1113 · complete: (CH₃)₂C=OH⁺ + CH₃NH₂ → (CH₃)₂C(OH)(NH₂CH₃)⁺
  Image: `mechanisms/imine-formation-step-2.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. 1113 for iminium dehydration extends the carbonyl-elimination analogy to C=N; retained as candidate, not a taxonomy change.

- Event 3 · 1122 · complete: (CH₃)₂C(OH)(NH₂CH₃)⁺ + H₂O ⇌ (CH₃)₂C(OH)(NHCH₃) + H₃O⁺
  Image: `mechanisms/imine-formation-step-3.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. 1113 for iminium dehydration extends the carbonyl-elimination analogy to C=N; retained as candidate, not a taxonomy change.

- Event 4 · 1122 · complete: (CH₃)₂C(OH)(NHCH₃) + H₃O⁺ ⇌ (CH₃)₂C(OH₂⁺)(NHCH₃) + H₂O
  Image: `mechanisms/imine-formation-step-4.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. 1113 for iminium dehydration extends the carbonyl-elimination analogy to C=N; retained as candidate, not a taxonomy change.

- Event 5 · 1113 · complete: (CH₃)₂C(OH₂⁺)(NHCH₃) → (CH₃)₂C=N⁺(H)CH₃ + H₂O
  Image: `mechanisms/imine-formation-step-5.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. 1113 for iminium dehydration extends the carbonyl-elimination analogy to C=N; retained as candidate, not a taxonomy change.

- Event 6 · 1122 · complete: (CH₃)₂C=N⁺(H)CH₃ + H₂O ⇌ (CH₃)₂C=NCH₃ + H₃O⁺
  Image: `mechanisms/imine-formation-step-6.svg`. Inherited v0.3.4 image/scope record; no new external-image verification. 1113 for iminium dehydration extends the carbonyl-elimination analogy to C=N; retained as candidate, not a taxonomy change.

## Base-catalyzed aldol condensation

Previous review: Image fetch rate-limited/access-blocked. The filename alone does not establish full five-stage coverage.

Current: complete. Image: `mechanisms/v035/aldol-condensation.svg`.

- Event 1 · 1122 · complete: (CH₃)₂CO + HO⁻ ⇌ CH₃COCH₂⁻ + H₂O
  Image: `mechanisms/v035/aldol-condensation-step-1.svg`. Authored focused structural SVG. Enolate and E1cB steps retain their convention/candidate boundaries; dehydration depends on conditions.

- Event 2 · 1113 · complete: CH₃COCH₂⁻ + (CH₃)₂CO → CH₃COCH₂C(O⁻)(CH₃)₂
  Image: `mechanisms/v035/aldol-condensation-step-2.svg`. Authored focused structural SVG. Enolate and E1cB steps retain their convention/candidate boundaries; dehydration depends on conditions.

- Event 3 · 1122 · complete: CH₃COCH₂C(O⁻)(CH₃)₂ + H₂O ⇌ CH₃COCH₂C(OH)(CH₃)₂ + HO⁻
  Image: `mechanisms/v035/aldol-condensation-step-3.svg`. Authored focused structural SVG. Enolate and E1cB steps retain their convention/candidate boundaries; dehydration depends on conditions.

- Event 4 · 1122 · complete: CH₃COCH₂C(OH)(CH₃)₂ + HO⁻ ⇌ CH₃COCH⁻C(OH)(CH₃)₂ + H₂O
  Image: `mechanisms/v035/aldol-condensation-step-4.svg`. Authored focused structural SVG. Enolate and E1cB steps retain their convention/candidate boundaries; dehydration depends on conditions.

- Event 5 · 1133 · complete: CH₃COCH⁻C(OH)(CH₃)₂ → CH₃COCH=C(CH₃)₂ + HO⁻
  Image: `mechanisms/v035/aldol-condensation-step-5.svg`. Authored focused structural SVG. Enolate and E1cB steps retain their convention/candidate boundaries; dehydration depends on conditions.

## Acid-promoted epoxide opening

Previous review: Original drawing of the stated model: reactants, formal charges, electron-flow arrows and product. No calculated geometry is implied.

Current: complete. Image: `mechanisms/acid-epoxide.svg`.

- Event 1 · 1122 · complete: propylene oxide + HCl ⇌ protonated propylene oxide + Cl⁻
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Corrected HCl/ether major pathway attacks primary carbon; do not generalize tertiary-epoxide selectivity to this substrate.

- Event 2 · 1122 · complete: protonated propylene oxide + Cl⁻ → ClCH₂CH(OH)CH₃
  Image: `full overview only`. Inherited v0.3.4 image/scope record; no new external-image verification. Corrected HCl/ether major pathway attacks primary carbon; do not generalize tertiary-epoxide selectivity to this substrate.
