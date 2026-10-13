"""v0.2.9 editorial clarification; preserve numeric SORG assignments."""

def apply_v029(reactions, codebook):
    book=codebook['1113']
    book['label']='Polar tetrahedral–planar carbon-center change'
    book['why']=['Closed-shell electron-pair model',
      'Lone-pair or σ donation to a polarized C=O center, or a heteroatom lone pair forming C=O/C=N on collapse',
      'One C–nucleophile bond forms or one C–leaving-group bond breaks as the principal event',
      'The carbon center changes between planar π-bonded and tetrahedral forms']
    book['boundary']='Candidate for polar addition to C=O and collapse of tetrahedral C–O/C–N intermediates. The incoming donor, leaving group, and newly made π bond must be specified; the iminium C=N case is a provisional extension. Use R3 when a concerted multi-center π reorganization, rather than local addition/collapse, dominates.'
    book=codebook['1133']
    book['why']=['Closed-shell electron-pair model',
      'Polar donor–acceptor interaction, including σ or π donation; not cyclic pericyclic overlap',
      'Coupled σ/π bond redistribution across multiple centers is the defining bookkeeping feature',
      'Several atom positions or a conjugated π framework reorganize together']
    book['boundary']='Candidate for E2/E1cB alkene formation, bromonium bridging and electrophilic aromatic attack/rearomatization when two or more bond orders change in a coupled polar event. Distinct mechanisms can share this code; proton-only transfer remains 1122, simple local carbonyl addition/collapse remains 1113, and symmetry-governed cyclic overlap remains O3/1333. Staged reactions must retain separate event records.'
    codebook['1333']['subtypes']=['Cycloaddition','Electrocyclic reaction','Sigmatropic rearrangement']
    R={r['id']:r for r in reactions}
    for rid,subtype in [('diels-alder','Cycloaddition'),('electrocyclic','Electrocyclic reaction'),('claisen','Sigmatropic rearrangement')]:
        R[rid]['steps'][0]['subtype']=subtype
    for rid in ('fischer-esterification','imine-formation'):
        for i,step in enumerate(R[rid]['steps']):
            step['eventFigure']={'src':f'mechanisms/{rid}-step-{i+1}.svg',
                                 'scope':'exact selected teaching stage extracted from the full original SVG; a grouped stage may contain more than one microscopic transfer'}
