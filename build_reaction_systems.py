"""Adapt retained v0.3.5 SN2 data and new carbonyl data to laboratory schema 2.
Does not modify original wavefunctions, fields, literature data or SORG codes.
"""
from pathlib import Path
import json,copy
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist/reaction-lab'
def read(path):return json.loads((OUT/path).read_text())
def write(path,data):(OUT/path).write_text(json.dumps(data,indent=2))
def sourcefiles(prefix,id):
    return [dict(label=label,path=f'{prefix}/{id}{suffix}') for label,suffix in [('Cartesian geometry','.xyz'),('SCF coefficients + density matrix','-scf.npz'),('Volumetric fields + grid','-fields.npz'),('Aligned coefficients','-tracked.npz'),('SCF output','.log')]]
def common(d):
    d=copy.deepcopy(d);d['schemaVersion']='2.0'
    d['fieldDefinitions']=[dict(id=k,label=label,kind=kind,units='e bohr⁻³',signed=k!='total') for k,label,kind in [('total','Total electron density ρ','electron-density'),('difference','Geometry density difference','density-difference'),('deformation','Same-geometry fragment deformation density','deformation-density')]]
    return d

def main():
    sn=common(read('sn2.json'));sn.update(id='chloride-identity-sn2',title='SN2 · Cl⁻ + CH₃Cl',event='sn2:0',modelEquation='Cl(in)⁻ + CH₃Cl(out) → Cl(in)CH₃ + Cl(out)⁻',modelScope='Computed chloride identity model; the unchanged catalog example uses hydroxide + methyl bromide.',modelMechanism='mechanisms/v035/sn2-chloride-step-1.svg',
      energyReference=dict(frameId='frame-0',label='first constrained SN2 frame; not separated reactants'),
      orbitalDefinitions=[dict(id=k,title=t,meshKey=k,description=desc) for k,t,desc in [('occupied','Tracked occupied canonical MO','Initial chloride 3px-like fragment projection; not a localized donor.'),('virtual','Tracked virtual canonical MO','Initial substrate sigma-antibonding trial projection; not a localized acceptor or necessarily LUMO.')]],
      series=[dict(id='scan',title='Five computed constrained distance frames',frameIds=[f'frame-{i}' for i in range(5)],coordinateLabel='q = (r(out) − r(in))/2 / Å')],
      evidence=['S1: singlet restricted determinant is consistent with a paired-electron model; HF stability was not checked for this retained SN2 dataset.','O1: backside arrangement and stated fragment projections inform a donor–acceptor interpretation. Canonical MO pictures alone do not establish it uniquely.','R2: incoming/outgoing C–Cl distances and Mayer indices exchange.','G2: approach and departure are coupled; the symmetric frame is a Hessian-verified saddle. This constrained sequence is not an IRC.'],
      limitations=['RHF omits correlation; no solvent, counterion, free energies, HF stability or basis-convergence study.','Uniform display grid under-resolves nuclear cores. AO metric and independent Becke quadrature validate normalization; do not integrate charge transfer on this grid.'],
      protocol=[sn['pathKind'],sn['grid']['alignment'],sn['references']['difference'],sn['references']['deformation'],sn['initialSelection']['identity'],'Tracking: maximum absolute cross-geometry AO-metric overlap, Hungarian assignment within occupied/virtual spaces, then phase alignment. Low overlap or a larger competing candidate is flagged; no degenerate-subspace tracking is claimed.'],
      sourceFiles=[dict(label='Original SN2 metadata',path='reaction-lab/sn2.json'),dict(label='SN2 computation',path='reaction-lab/compute_sn2.py'),dict(label='SN2 fields',path='reaction-lab/fields_sn2.py')])
    for f in sn['frames']:
        f.update(label=f['id']+' · q '+str(f['qAngstrom'])+' Å',coordinateLabel=str(f['qAngstrom']),
          bonds=[dict(atoms=[0,1],label='C···Cl(in)',distanceAngstrom=f['rinAngstrom'],mayer=f['mayerCClIn']),dict(atoms=[0,2],label='C···Cl(out)',distanceAngstrom=f['routAngstrom'],mayer=f['mayerCClOut'])],geometryDescriptors=[],
          connections=[dict(atoms=[0,j],style='guide' if j<3 else 'bond') for j in range(1,6)],files=sourcefiles('reaction-lab',f['id']))
        for o,k in zip(f['orbitals'],['occupied','virtual']):o['id']=k
    write('sn2-system.json',sn)
    ca=common(read('carbonyl/carbonyl.json'));detach=read('carbonyl/detachment-check.json');ca.update(id='hydride-formaldehyde',warnings=[f"METHOD LIMIT: isolated H− is not bound against electron detachment at this HF level (E(H)−E(H−) = {detach['detachmentEnergyHartree']:.6f} Eh). These are finite-basis restricted addition-branch models, not a verified physical gas-phase ground-state path."],title='Carbonyl addition · H⁻ + H₂CO',event='carbonyl-add:0',modelEquation='H(nu)⁻ + H₂C=O → H₃C–O⁻',modelScope='One explicit instance of the unchanged generic R₂C=O + Nu⁻ → R₂C(O⁻)Nu event. Bare gas-phase hydride is not LiAlH₄/NaBH₄; methoxide is before protonation.',modelMechanism='mechanisms/v036/carbonyl-hydride-step-1.svg',
      energyReference=dict(frameId='addition-0',label='3.0 Å / 110° constrained complex; not separated reactants'),
      orbitalDefinitions=[dict(id=k,title=t,meshKey=k,description=desc) for k,t,desc in [('donor','Hydride-projected occupied canonical MO','Initial hydride 1s fragment projection, then tracked canonical complex MO; not localized H⁻.'),('pi','Carbonyl π-projected occupied canonical MO','Initial formaldehyde π reference, then overlap-tracked complex canonical orbital; its later shape need not remain a pure π bond.'),('pistar','Carbonyl π*-projected virtual canonical MO','Initial formaldehyde π* reference, then tracked complex canonical MO; not a uniquely defined localized acceptor.')]],
      series=[dict(id='addition',title='Addition: four constrained frames + verified product minimum',frameIds=['addition-0','addition-1','addition-2','addition-3','product'],coordinateLabel='C–H(nu) distance / Å (product angle relaxed)'),dict(id='angles',title='Matched-distance angle comparison · C···H = 1.9 Å',frameIds=['angle-90','addition-2','angle-130'],coordinateLabel='O–C–H(nu) angle / °')],
      evidence=['S1: all complex frames use 18 electrons, singlet RHF; internal and external determinant stability checked. This is a model, not proof against all other electronic states.','O1: hydride 1s / carbonyl π* fragment projections and the computed approach support donor–acceptor interpretation; displayed complex MOs remain canonical.','R1 (existing candidate code): shorter C–H distance accompanies lower C–O Mayer index and density redistribution. Inspect both bond-index conventions; neither is an integer bond count. The code omits the simultaneous π redistribution and numerical bond indices.','G3 (existing candidate code): carbon leaves the O/H1/H2 plane while bonding reorganizes. The defined pyramidalization descriptors quantify what the code omits.'],
      limitations=[ca['competingPathways'],'Only three fixed angles at one distance were compared, with Cs-constrained substrate relaxation. No universal Bürgi–Dunitz angle, optimal trajectory, transition state, barrier or IRC is inferred.','The deformed neutral H2CO fragment can have an external RHF instability; its same-geometry restricted determinant remains the explicitly defined deformation reference, not a verified fragment ground state.','RHF / finite basis; no correlation, solvent, free energy or basis/grid-convergence study. Fragment densities are defined references, not unique charge-transfer partitions.','Uniform display grid is not a quantitative electron-transfer integration grid; normalization uses Tr(PS) and independent level-5 Becke quadrature.'],
      protocol=[ca['pathKind'],ca['atomMapping'],ca['references']['difference'],ca['references']['deformation'],ca['initialSelection']['protocol'],'Tracking: sequential full cross-geometry AO-metric Hungarian assignment within occupied/virtual blocks, then sign alignment. Angle branches use addition-2 as their shared parent. Low score (<0.7) or larger alternative is flagged; no arbitrary canonical surface is called a unique mechanistic observable.'],
      sourceFiles=[dict(label='Full carbonyl metadata + references',path='reaction-lab/carbonyl/carbonyl.json'),dict(label='Calculation script',path='reaction-lab/carbonyl/compute.py'),dict(label='Fields + tracking script',path='reaction-lab/carbonyl/fields.py'),dict(label='Hydride binding diagnostic',path='reaction-lab/carbonyl/detachment-check.json'),dict(label='Calculation inputs + constraints',path='reaction-lab/carbonyl/inputs.json'),dict(label='Independent validation report',path='reaction-lab/carbonyl/validation.json'),dict(label='Product Hessian + normal modes',path='reaction-lab/carbonyl/product-hessian.npz')])
    for f in ca['frames']:
        f['label']=f['id']+f" · {f['distanceAngstrom']:.3f} Å / {f['angleDegree']:.1f}°"
        f['coordinateLabel']=f"{f['distanceAngstrom']:.3f} Å / {f['angleDegree']:.1f}°";f['files']=sourcefiles('reaction-lab/carbonyl',f['id'])
        f['files'] += [dict(label=name+' fragment '+label,path=f"reaction-lab/carbonyl/{f['id']}-{name}{suffix}") for name in ['hydride','formaldehyde'] for label,suffix in [('output','.log'),('coefficients + density','-scf.npz')]]
    write('carbonyl-system.json',ca)
    write('index.json',dict(schemaVersion='2.0',systems=[dict(id=d['id'],event=d['event'],title=d['title'],dataFile=f'reaction-lab/{name}-system.json') for d,name in [(sn,'sn2'),(ca,'carbonyl')]],
      capabilities=dict(multipleBondDescriptors=True,multipleOrbitals=True,geometryDescriptorArrays=True,spinResolvedFieldDefinitions=True),futureDatasets='Diels–Alder, E2 and radical reaction systems are NOT implemented. Schema supports fields marked spin-density/alpha/beta only if computed data are supplied.'))
    import v035_mechanisms as draw
    draw.OUT=ROOT/'dist/mechanisms/v036'
    draw.render_record('carbonyl-hydride',0,('[H-:1].[CH2:2]=[O:3]','[CH2:2]([H:1])[O-:3]',[(1,2),((2,3),3)],'Hydride electron pair → C; carbonyl pi pair → O. Methoxide, charge −1; no protonation/work-up.'),'Hydride addition to formaldehyde','H− + H2C=O → H3C–O−')
    import shutil
    for name in ['analyze.py','validate.py','detachment.py']:shutil.copy2(ROOT/'research/carbonyl'/name,OUT/'carbonyl'/name)
    from build_diels_alder import extend
    extend()
    print('Built schema 2 adapters for three independently computed reaction systems; original SN2 files untouched.')
if __name__=='__main__':main()
