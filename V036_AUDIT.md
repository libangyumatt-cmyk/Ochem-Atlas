# Ochem Atlas v0.3.6 audit — Carbonyl Reaction Electronic Structure

Date: 2026-10-16 UTC. Baseline: `ff06aba92d8b35b2d2d6ae44ed6c9b04c7b03d75` (v0.3.5).

## Scope and preservation

- Exactly 31 reaction records / 69 listed events. Full reaction records, figures,
  SORG assignments, citations, codebook, lessons and published research data are
  preserved. Only the reaction payload version/date changed. Carbonyl addition
  remains **candidate 1113**; SN2 remains 1122. No new catalog entry or taxonomy.
- `audit/V036_PRESERVED_DATA.json` records SHA-256 checksums of all original
  reaction-laboratory assets plus original orbital/diversity/research JSON.
  Automated tests enforce byte preservation. SN2 is adapted into a new schema
  record; its original five computed frames are not recomputed or overwritten.
- Conventional coverage remains v0.3.5's 29 complete, one partial (LAH), one
  representative (Grignard). The new original two-arrow hydride/formaldehyde
  model SVG complements the unchanged generic carbonyl event; it does not alter
  the inventory or claim to complete the metal-organic gaps.

## Implemented laboratory

`dist/reaction-lab/index.json` registers independently computed SN2 and carbonyl
systems. `build_reaction_systems.py` generates schema-2 adapters; `research/carbonyl/SCHEMA.md`
documents the extensible arrays. Molecular counts/atom indices/bonds/geometry
coordinates in the renderer are supplied by data rather than SN2 assumptions.

Controls synchronize system, catalog event, geometry series, discrete geometry,
quantity, orbital and threshold. Each system retains its own selections. A
load-generation guard prevents a late system/mesh response replacing a newer
selection. Conventional/quantum/both modes retain the event. Unsupported events
explicitly lack calculated frames rather than displaying schematic clouds.

Two series for carbonyl: four constrained approach frames plus a separately
verified product minimum, and three matched-distance angle points (one shared).
Orbital amplitude/probability selects among hydride-projected, carbonyl-pi-projected,
and carbonyl-pi*-projected canonical orbitals. Total density, fixed-coordinate
geometry difference and same-geometry fragment deformation are separate fields.
The three supplied isovalues per field are actual extracted grid contours.
Probability surfaces use +/-sqrt(threshold) amplitude contours; no independently
computed probability frames or occupation-weighted density are implied.

Expandable comparison cards show each system's last selected actual frame,
electronic surface, energy reference, bond distances and indices. Cross-system
absolute/relative energy subtraction is explicitly disallowed: molecular
compositions differ. Desktop/mobile CSS stacks columns on narrow screens.
WebGL supports rotation and zoom; the fallback draws the same supplied calculated
mesh in a labeled fixed projection. Neither representation calculates chemistry
in the browser or interpolates uncomputed densities/energies/geometries.

## Explicit carbonyl model and provenance

H(nu)− + H2C=O → CH3O−. Total charge −1, multiplicity 1, 18 electrons.
Isolated gas phase, no solvent, counterion, metal reagent or work-up.
**RHF/6-31++G(d,p)**, PySCF 2.14.0, Python 3.12, NumPy 2.3.5 / SciPy 1.17.0.
Diffuse functions are present on hydrogen as well as heavy atoms. This finite-basis
mean-field model neglects correlation; it is not an experimental energy profile.

SCF: 1e-11 Eh energy tolerance; orbital-gradient tolerance 1e-7; max 150 cycles;
Newton fallback if necessary. All seven full complexes converged and passed
internal/external RHF determinant stability checks. A stable SCF determinant is
not proof of a global electronic/chemical ground state or a stable molecule.

C is fixed at origin, O on +x; incoming H lies in xz with z>0. Original H1/H2
are mirror-related across xz. For fixed incoming distance/angle, four parameters
(C–O, H-pair x/y/z) relax by analytic-gradient BFGS with 3e-7 requested free-gradient
tolerance. Product relaxes all six internal parameters, including incoming
radius/angle. This spans a Cs parameterization; the product is additionally
checked with the **full Cartesian gradient and analytic Hessian**, including
symmetry-breaking vibrational directions. Coordinates/parameters are stored.
No constrained geometry is labeled a transition state or minimum.

| Geometry | E / Eh | ΔE / eV vs first | C–H(nu) / Å | O–C–H(nu) / ° | C–O / Å | Mayer C–O / C–H | C height / Å |
| --- | --- | --- | --- | --- | --- | --- | --- |
| addition-0 | -114.372198286 | 0.000000 | 3.0000 | 110.00 | 1.1931 | 1.8107 / 0.1429 | 0.00020 |
| addition-1 | -114.371319281 | 0.023919 | 2.4000 | 110.00 | 1.2009 | 1.7108 / 0.3012 | 0.03030 |
| addition-2 | -114.370537263 | 0.045199 | 1.9000 | 110.00 | 1.2263 | 1.4650 / 0.6065 | 0.12551 |
| addition-3 | -114.387567790 | -0.418226 | 1.5000 | 110.00 | 1.2801 | 1.1723 / 0.9097 | 0.25583 |
| product | -114.415725697 | -1.184441 | 1.1228 | 115.15 | 1.3294 | 1.0561 / 0.9696 | 0.35997 |
| angle-90 | -114.350897898 | 0.579613 | 1.9000 | 90.00 | 1.2230 | 1.4939 / 0.7983 | 0.08678 |
| angle-130 | -114.368056851 | 0.112694 | 1.9000 | 130.00 | 1.2275 | 1.4667 / 0.4043 | 0.15284 |

Product full maximum gradient: 3.4351e-07 Eh/bohr;
9 positive vibrational modes, 1243.33–2809.99 cm−1
(translations/rotations removed). The saved product Hessian and frequencies were
independently recomputed. This verifies a **local methoxide minimum at this level**.
No transition state, IRC, optimal attack trajectory or kinetic barrier is claimed.
Even the 3 Å frame is an interacting constrained complex, not separated reactants.
Relative electronic energies include nuclear repulsion, without ZPE/thermal corrections.

At 1.9 Å, 110° is the lowest of the three chosen constrained angles (90/110/130),
with independently relaxed substrate parameters. This is neither an optimized
angle nor a universal Bürgi–Dunitz angle. Formaldehyde has identical substituents;
no enantiomeric selectivity is claimed.

### Essential physical-model limitation: bare hydride

A separate same-basis calculation of neutral doublet H uses ROHF (charge 0,
multiplicity 2, one electron). It gives E(H) = −0.498801106200 Eh versus isolated
RHF H− E = −0.487072588981 Eh. E(H)+E(free electron at rest=0)−E(H−) =
**−0.011728517218 Eh**. Thus this HF model does not bind the isolated hydride
against detachment. The public viewer prominently labels the addition frames as
a **finite-basis restricted branch model, not a verified physical gas-phase
ground-state path**. This diagnoses model inadequacy; it does not assert that
real hydride is unbound. The one-atom diagnostic is not a radical-reaction dataset.

H abstraction to H2 + HCO−, complex electron detachment, alternative spin/electronic
states, solvent/counterion effects and metal-hydride speciation are not fully
compared. None of these frames proves global selectivity. The product local
minimum and SCF checks do not remove those limitations. Improving correlated
hydride energetics or a different well-bound donor is a next step, not an
unperformed calculation represented as completed.

## Orbitals and correspondence

Initial occupied donor reference: hydride 1s canonical orbital projected into
the full complex occupied space. Initial carbonyl references: neutral H2CO
canonical occupied pi / virtual pi* selected by maximal normalized valence
C 2pz + O 2pz / C 2pz − O 2pz AO-trial overlap within the respective fragment
subspace, then projected into full-complex occupied / virtual spaces. Formaldehyde
is nearly xy planar at the initial point. These are selection conventions, not
canonical MOs falsely called localized donor/acceptor orbitals.

Each main-branch frame uses full cross-geometry AO-metric MO overlaps. Hungarian
assignment maximizes total absolute overlap separately in occupied/virtual blocks,
then selected columns are sign-aligned to a positive predecessor overlap. Angle
branches both reference `addition-2`, not arbitrary order through the angle list.
Initial global sign makes the largest AO coefficient positive. Raw and aligned
coefficients and parent/matching indices are retained. Selected consecutive/branch
aligned overlaps range 0.859895–0.998762; alternative scores and the
<0.7 / larger-competitor ambiguity rule are displayed.

Product occupied orbitals enter near-degenerate pairs (same-occupation eigenvalue
gap <1e-5 Eh), explicitly flagged. Individual canonical partners there are not
unique. No degenerate-subspace tracking or unique mechanism determination from
one orbital is claimed. An orbital initially selected as pi need not remain a pure
carbonyl pi bond after pyramidalization.

## Density, grid, reference and normalization

All seven geometries retain AO-evaluated actual total rho, signed selected MO
amplitudes and reference fields. No invented or interpolated grids. Shape
91 × 71 × 101, origin (−9,−7,−7) bohr, spacing 0.2 bohr, C order with z fastest.
Same fixed Cartesian origin/axes/atom identities in every frame; no post-hoc fit.
The volume is extended toward incoming H. Every field's maximum absolute boundary
value is checked below its smallest displayed contour, preventing contour
clipping at the grid boundary. Those values are in per-frame metadata.

Density/difference/deformation: electron bohr−3. Amplitude: bohr−3/2.
Probability: bohr−3, one normalized spatial orbital, no occupancy factor.
Mesh coordinates: Å. Volumetric NPZ: float32; full SCF/overlap/density matrices
and raw/aligned MO coefficients: float64. 1 bohr = 0.529177210903 Å;
1 Eh = 27.211386245988 eV for the viewer.

- Total rho = sum over all occupied spatial MOs of occupation × |phi|².
- Geometry difference = rho(current) − rho(addition-0) on identical grid points.
  It includes nuclear displacement. It is not a unique electron-transfer field.
- Deformation = complex rho minus separately SCF-solved H(nu)− (2e, singlet)
  and neutral H2CO (16e, singlet) at each **same geometry**, using each fragment's
  own basis, no ghosts. Membership never changes, even at product geometry.
  This is not counterpoise-corrected EDA or a unique fragment partition.
- Some deformed neutral H2CO RHF references have external determinant instabilities
  (addition-2, addition-3, product, angle-130). Metadata retains them, and deformation
  mode warns explicitly for affected frames. These chosen restricted fragment
  references are not labeled verified fragment ground states.
- Teal/amber denote positive/negative electron-number difference or amplitude
  sign, never positive/negative electric charge. Total density is nonnegative.

AO-metric Tr(PS) = 18 to numerical precision. Independent level-5 atom-centered
Becke integration gives 17.999999520–17.999999973 electrons. The display grid
is not a core-resolved integration grid: its unrescaled voxel sums are
18.542634–19.536292. These errors are disclosed in the UI. No fake
renormalization, quantitative grid-integrated charge-transfer claim, or grid
convergence claim is made. Full coefficients permit independent denser evaluation.

## Geometry and bond descriptors / SORG

Report C–O and C–H(nu) distances; angle O–C–H(nu); perpendicular displacement of
C from the O/H1/H2 plane; and 360° minus the three substrate bond-angle sum.
The latter two state precisely what is meant by pyramidalization here.

Mayer = sum (PS)uv(PS)vu over AO blocks on atoms A/B, spin-summed RHF P.
Löwdin Wiberg = sum |(S^(1/2) P S^(1/2))uv|² over those blocks with symmetric
positive overlap square root. It is **not** an NBO Wiberg index. Both are basis/
partition dependent, not integer bond counts; differences in magnitude are real
convention dependence. Their trends must be read with distances and density.

Existing carbonyl **candidate 1113**: S1 is informed by the paired determinant,
O1 by declared fragment projections and approach, R1 by bond formation accompanied
by carbonyl pi redistribution, G3 by carbon pyramidalization and coupled nuclear
changes. Existing SN2 **1122**: paired donor/acceptor account, replacement and
backside approach–departure exchange. These code interpretations stay unchanged;
SORG omits method, energies, solvent, orbital nonuniqueness, density references,
quantitative bond indices, attack angle, selectivity and path validation.

## Reproduction, tests and visual review

`research/carbonyl/README.md` gives the exact command sequence. Pinned requirements
are included. Computation, fields, analysis, detachment diagnostic, independent
validation and visual-review scripts are retained, plus model inputs/constraints,
XYZ files, final SCF outputs, fragment outputs/coefficients, product Hessian,
wavefunctions, volumetric arrays, meshes, metadata and validation report under
`dist/reaction-lab/carbonyl`. The Pages build regenerates schema adapters but does
not rerun quantum chemistry. Source ZIP generation includes all original/new data.

Independent validation reconstructs all seven complex energies, full nuclear/SCF
gradients, occupations, AO orthonormality, density matrices, Tr(PS), Becke counts,
700 deterministic volumetric samples, explicit fragment references and energies,
fragment stability, orbital correspondence/phase, two bond indices, distances/angles,
and the product analytic Hessian/frequencies. All seven pass (`validation.json`).

Original regressions plus new DOM tests cover 69 events, retained SN2 controls,
system-loading race rejection, per-system geometry/quantity/isovalue/orbital memory,
angle-series selection, product labeling, unsupported events, matching conventional
model panel, representation switching and unchanged SORG. New structural tests
check all meshes, frame files, matched angle constraints, metadata, normalization,
minimum records and checksums of original scientific assets.

Visual QA: original hydride/formaldehyde SVG checked for charge/formula, donor
arrow to C and C=O pi arrow to O; seven geometries × six quantities inspected in
an internal 3D projection montage from actual calculated meshes. Initial geometry
difference is empty; pi/pi* have distinct phase/nodes; product is pyramidal.
The review renderer may subsample triangles only for the internal raster montage;
all published meshes/grids retain the full extraction.

Live desktop publication checks are recorded separately after deployment. Native
WebGL rotation and real mobile/touch are not certified by jsdom or static CSS.
A cloud browser without WebGL can verify only the labeled fixed-mesh projection.

## Next steps (not implemented datasets)

- Correlated / basis-converged carbonyl model and improved hydride/detachment treatment;
  compare a well-bound donor, full competing paths and solvent/counterion effects.
- More angle/distance samples, unconstrained path/TS/IRC where warranted; no
  universal angle from these three points.
- Degenerate-subspace correspondence and denser/core-resolved density quadrature
  for quantitative spatial integrations.
- Real mobile/WebGL device testing. Diels–Alder, E2 and radical reaction datasets
  remain absent. Schema arrays permit future multiple bonds, orbital selections,
  geometric descriptors and calculated signed alpha/beta/spin fields; declaration
  alone does not implement those computations.

Method sources: [PySCF SCF/stability](https://pyscf.org/user/scf.html),
[stability implementation](https://pyscf.org/_modules/pyscf/scf/stability.html),
[Hessian/harmonic analysis](https://pyscf.org/pyscf_api_docs/pyscf.hessian.html).
These document algorithms, not the numerical data above, which were computed here.
