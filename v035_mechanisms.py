"""Original atom/bond-anchored SVG additions. Run through build_data.py.
RDKit supplies 2D atom positions; the authored electron moves below are not
inferred by software. SMILES formula/charge checks complement visual review.
"""
from pathlib import Path
from copy import deepcopy
from html import escape
import json, re

# Each record: mapped reactant and product structures; electron origins and
# destinations (atom map or bond-map pair); explicit electron-flow legend.
S={}
def add(rid,left,right,moves,legend):S.setdefault(rid,[]).append((left,right,moves,legend))
add('sn2','[OH-:1].[CH3:2][Br:3]','[CH3:2][OH:1].[Br-:3]',[(1,2),((2,3),3)],'O lone pair → methyl C; C–Br bond pair → Br. Methyl carbon is achiral.')
add('williamson','[CH3:4][O-:1].[CH2:2]([CH3:5])[Br:3]','[CH3:4][O:1][CH2:2][CH3:5].[Br-:3]',[(1,2),((2,3),3)],'Methoxide O → ethyl C bearing Br; C–Br → Br. No stereocenter is present.')
add('sn1-core','[*:1][C:2]([*:3])([*:4])[*:5]','[*:1][C+:2]([*:3])[*:4].[*-:5]',[((2,5),5)],'C–X pair → X. R groups and X are generic placeholders, not specified atoms.')
add('sn1-core','[*:1][C+:2]([*:3])[*:4].[*-:6]','[*:1][C:2]([*:3])([*:4])[*:6]',[(6,2)],'Nu lone pair → planar cation C. Generic R/Nu labels do not establish stereoselectivity.')
add('sn1-water','[CH3:1][C:2]([CH3:3])([CH3:4])[Br:5]','[CH3:1][C+:2]([CH3:3])[CH3:4].[Br-:5]',[((2,5),5)],'C–Br pair → Br; tertiary carbocation is the stated limiting teaching model.')
add('sn1-water','[CH3:1][C+:2]([CH3:3])[CH3:4].[OH2:6]','[CH3:1][C:2]([CH3:3])([CH3:4])[OH2+:6]',[(6,2)],'Water O lone pair → tertiary C; oxygen becomes oxonium (+1).')
add('sn1-water','[CH3:1][C:2]([CH3:3])([CH3:4])[OH+:6][H:7].[OH2:8]','[CH3:1][C:2]([CH3:3])([CH3:4])[OH:6].[OH3+:8]',[(8,7),((6,7),6)],'Second water O → oxonium H; alcohol O–H pair → alcohol O.')
add('hbr','[CH3:1][CH:2]=[CH2:3].[H:4][Br:5]','[CH3:1][CH+:2][CH3:3].[Br-:5]',[((2,3),4),((4,5),5)],'Alkene π pair → H (bonding at terminal C); H–Br pair → Br. Secondary cation only.')
add('hbr','[CH3:1][CH+:2][CH3:3].[Br-:5]','[CH3:1][CH:2]([Br:5])[CH3:3]',[(5,2)],'Bromide lone pair → secondary cation; product is 2-bromopropane.')
add('hydration','[CH3:1][CH:2]=[CH2:3].[OH2+:5][H:4]','[CH3:1][CH+:2][CH3:3].[OH2:5]',[((2,3),4),((4,5),5)],'Alkene π pair → hydronium H; acid O–H pair → O. Terminal carbon becomes CH3.')
add('hydration','[CH3:1][CH+:2][CH3:3].[OH2:6]','[CH3:1][CH:2]([OH2+:6])[CH3:3]',[(6,2)],'Water O → secondary cation; protonated 2-propanol forms.')
add('hydration','[CH3:1][CH:2]([OH+:6][H:7])[CH3:3].[OH2:8]','[CH3:1][CH:2]([OH:6])[CH3:3].[OH3+:8]',[(8,7),((6,7),6)],'Water → oxonium H; oxonium O–H pair → O; hydronium is regenerated.')
add('e1','[CH3:1][C:2]([CH3:3])([CH3:4])[Cl:5]','[CH3:1][C+:2]([CH3:3])[CH3:4].[Cl-:5]',[((2,5),5)],'C–Cl pair → Cl; ionization precedes proton removal.')
add('e1','[CH2:1]([H:7])[C+:2]([CH3:3])[CH3:4].[OH2:8]','[CH2:1]=[C:2]([CH3:3])[CH3:4].[OH3+:8]',[(8,7),((1,7),(1,2))],'Water → beta H; beta C–H pair → C=C. 2-Methylpropene has no E/Z isomerism.')
add('cyanohydrin','[c:8]1([CH:2]=[O:3])ccccc1.[C-:1]#[N:4]','[c:8]1([CH:2]([O-:3])[C:1]#[N:4])ccccc1',[(1,2),((2,3),3)],'Cyanide carbon → benzaldehyde C; C=O π pair → O. Both carbonyl faces are possible.')
add('cyanohydrin','[c:8]1([CH:2]([O-:3])[C:1]#[N:4])ccccc1.[H:5][C:6]#[N:7]','[c:8]1([CH:2]([OH:3])[C:1]#[N:4])ccccc1.[C-:6]#[N:7]',[(3,5),((5,6),6)],'Alkoxide O → H of HCN; H–C pair → cyanide C. No enantiomer is selected.')
add('acyl','[CH3:4][C:2](=[O:3])[Cl:5].[CH3:6][O-:1]','[CH3:4][C:2]([O-:3])([Cl:5])[O:1][CH3:6]',[(1,2),((2,3),3)],'Methoxide O → acyl C; C=O π pair → O. Discrete intermediate is a teaching assumption.')
add('acyl','[CH3:4][C:2]([O-:3])([Cl:5])[O:1][CH3:6]','[CH3:4][C:2](=[O:3])[O:1][CH3:6].[Cl-:5]',[(3,(2,3)),((2,5),5)],'O lone pair → C=O; C–Cl pair → Cl. Carbonyl reforms as chloride leaves.')
add('epoxide','[CH2:2]1[CH2:3][O:4]1.[CH3:5][O-:1]','[CH3:5][O:1][CH2:2][CH2:3][O-:4]',[(1,2),((2,4),4)],'Methoxide O → epoxide C from backside; attacked C–O pair → ring O. Symmetric achiral substrate.')
add('epoxide','[CH3:5][O:1][CH2:2][CH2:3][O-:4].[OH2+:6][H:7]','[CH3:5][O:1][CH2:2][CH2:3][OH:4].[OH2:6]',[(4,7),((6,7),6)],'Acid work-up: alkoxide → hydronium H; acid O–H pair → O. Acid is added after opening.')
add('aldol','[CH2:1]([H:7])[CH:2]=[O:3].[OH-:8]','[CH2-:1][CH:2]=[O:3].[OH2:8]',[(8,7),((1,7),1)],'Base → alpha H; C–H pair → alpha C in the C-anion enolate contributor; resonance is not a new event.')
add('aldol','[CH2-:1][CH:2]=[O:3].[CH3:4][CH:5]=[O:6]','[CH3:4][CH:5]([O-:6])[CH2:1][CH:2]=[O:3]',[(1,5),((5,6),6)],'Enolate alpha C → second aldehyde C; acceptor C=O π pair → O. Enolate carbonyl remains.')
add('aldol','[CH3:4][CH:5]([O-:6])[CH2:1][CH:2]=[O:3].[OH:8][H:7]','[CH3:4][CH:5]([OH:6])[CH2:1][CH:2]=[O:3].[OH-:8]',[(6,7),((7,8),8)],'Alkoxide O → water H; water O–H pair → O. Hydroxide is regenerated; no stereoisomer selected.')
# Acetone aldol/E1cB atom identities are retained through all five listed events.
a='[CH3:9][C:2](=[O:3])[CH2:1][H:7]';en='[CH3:9][C:2](=[O:3])[CH2-:1]'
accept='[CH3:4][C:5]([CH3:10])=[O:6]'
alk='[CH3:9][C:2](=[O:3])[CH2:1][C:5]([CH3:4])([CH3:10])[O-:6]'
alc='[CH3:9][C:2](=[O:3])[CH2:1][C:5]([CH3:4])([CH3:10])[OH:6]'
depro='[CH3:9][C:2](=[O:3])[CH-:1][C:5]([CH3:4])([CH3:10])[OH:6]'
add('aldol-condensation',a+'.[OH-:8]',en+'.[OH2:8]',[(8,7),((1,7),1)],'Alpha-H removal gives the C-anion enolate contributor; the enolate is delocalized.')
add('aldol-condensation',en+'.'+accept,alk,[(1,5),((5,6),6)],'Enolate C → acetone C; acceptor C=O π pair → O.')
add('aldol-condensation',alk+'.[OH:8][H:7]',alc+'.[OH-:8]',[(6,7),((7,8),8)],'Alkoxide protonation by water produces diacetone alcohol and regenerates base.')
pre='[CH3:9][C:2](=[O:3])[CH:1]([H:7])[C:5]([CH3:4])([CH3:10])[OH:6]'
add('aldol-condensation',pre+'.[OH-:8]',depro+'.[OH2:8]',[(8,7),((1,7),1)],'Second alpha deprotonation forms the E1cB precursor; no carbonyl bond is broken.')
add('aldol-condensation',depro,'[CH3:9][C:2](=[O:3])[CH:1]=[C:5]([CH3:4])[CH3:10].[OH-:6]',[(1,(1,5)),((5,6),6)],'Enolate C pair → alpha/beta C=C; beta C–O pair → O. Mesityl oxide has no E/Z at this alkene.')
S['e1cb-dehydration']=S['aldol-condensation'][3:]
# A separate conventional chloride-model panel belongs to the quantum case,
# not a replacement of the hydroxide/methyl bromide teaching card.
add('sn2-chloride','[Cl-:1].[CH3:2][Cl:3]','[Cl:1][CH3:2].[Cl-:3]',[(1,2),((2,3),3)],'Incoming Cl lone pair → C; outgoing C–Cl bond pair → outgoing Cl. Total charge −1; singlet model.')


add('alkene-bromination','[CH2:2]=[CH2:3].[Br:4][Br:5]','[Br+:4]1[CH2:2][CH2:3]1.[Br-:5]',[((2,3),4),((4,5),5),(4,2)],'Pi pair → Br; Br–Br pair → departing Br; attached Br lone pair → second C. Cyclic bromonium, not free Br+.')
add('alkene-bromination','[Br+:4]1[CH2:2][CH2:3]1.[Br-:5]','[Br:5][CH2:2][CH2:3][Br:4]',[(5,2),((2,4),4)],'Bromide → C from behind its bridge bond; attacked C–Br pair → bridging Br. Ethene product is achiral.')
add('halohydrin','[CH3:1][CH:2]=[CH2:3].[Br:4][Br:5]','[Br+:4]1[CH:2]([CH3:1])[CH2:3]1.[Br-:5]',[((2,3),4),((4,5),5),(4,2)],'Pi pair → Br; Br–Br pair → departing Br; attached Br lone pair closes bromonium bridge.')
add('halohydrin','[Br+:4]1[CH:2]([CH3:1])[CH2:3]1.[OH2:6]','[CH3:1][CH:2]([OH2+:6])[CH2:3][Br:4]',[(6,2),((2,4),4)],'Water → more substituted bromonium C from backside; bridge C–Br pair → Br. Racemic product; no enantiomer selected.')
add('halohydrin','[CH3:1][CH:2]([OH+:6][H:7])[CH2:3][Br:4].[OH2:8]','[CH3:1][CH:2]([OH:6])[CH2:3][Br:4].[OH3+:8]',[(8,7),((6,7),6)],'Second water → oxonium H; oxonium O–H pair → O. Bromide spectator is omitted on both sides in events 2/3.')
add('nitration-benzene','[OH:1][N+:2](=[O:3])[O-:4].[OH:5][S:6](=[O:8])(=[O:9])[O:10][H:11]','[OH2+:1][N+:2](=[O:3])[O-:4].[OH:5][S:6](=[O:8])(=[O:9])[O-:10]',[(1,11),((10,11),10)],'Nitric acid hydroxyl O → sulfuric acid H; acid O–H pair → acid O. Formal N+/O− charges preserve octets.')
add('nitration-benzene','[OH2+:1][N+:2](=[O:3])[O-:4]','[O:3]=[N+:2]=[O:4].[OH2:1]',[((1,2),1),(4,(2,4))],'N–OH2 bond pair → leaving water O; remaining O− lone pair → N=O. Linear nitronium results.')
add('nitration-benzene','[CH:1]1=[CH:2][CH:3]=[CH:4][CH:5]=[CH:6]1.[O:8]=[N+:7]=[O:9]','[CH:1]1([N+:7](=[O:8])[O-:9])[CH+:2][CH:3]=[CH:4][CH:5]=[CH:6]1',[((1,2),7),((7,9),9)],'Benzene pi pair → nitronium N; N=O pi pair → O (N octet). One arenium contributor, not a localized unique ion.')
add('nitration-benzene','[C:1]1([H:12])([N+:7](=[O:8])[O-:9])[CH+:2][CH:3]=[CH:4][CH:5]=[CH:6]1.[O-:10][S:11](=O)(=O)O','[C:1]1([N+:7](=[O:8])[O-:9])=[CH:2][CH:3]=[CH:4][CH:5]=[CH:6]1.[OH:10][S:11](=O)(=O)O',[(10,12),((1,12),(1,2))],'Bisulfate O → substituted ring H; C–H pair → adjacent C=C. Aromaticity and sulfuric acid are restored.')
add('radical-add','[CH3:1].[CH2:2]=[CH2:3]','[CH3:1][CH2:2][CH2:3]',[(1,(1,2),1),((2,3),(1,2),1),((2,3),3,1)],'Three fishhooks: methyl radical and one pi electron → new C–C bond; other pi electron → terminal carbon radical.')
add('radical-chain','[Cl:1].[CH3:2][H:3]','[Cl:1][H:3].[CH3:2]',[(1,(1,3),1),((2,3),(1,3),1),((2,3),2,1)],'Cl radical and one C–H electron → H–Cl; other C–H electron → methyl radical. Propagation, not initiation.')
add('radical-chain','[CH3:1].[Cl:2][Cl:3]','[CH3:1][Cl:2].[Cl:3]',[(1,(1,2),1),((2,3),(1,2),1),((2,3),3,1)],'Methyl radical and one Cl–Cl electron → C–Cl; other Cl–Cl electron → departing chlorine radical.')


add('claisen','[CH2:1]=[CH:2][O:3][CH2:4][CH:5]=[CH2:6]','[CH:2](=[O:3])[CH2:1][CH2:6][CH:5]=[CH2:4]',[((1,2),(2,3)),((3,4),(4,5)),((5,6),(6,1))],'Concerted [3,3]: vinyl pi → C=O; O–allyl sigma → allyl C=C; allyl pi → new C–C. 2D connectivity is not a TS conformer.')
add('electrocyclic','[CH2:1]=[CH:2][CH:3]=[CH2:4]','[CH2:1]1[CH:2]=[CH:3][CH2:4]1',[((1,2),(1,4)),((3,4),(2,3))],'Thermal 4-pi conrotatory closure: terminal carbons rotate in the same sense. No substituted stereocenter or E/Z product is implied.')

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist/mechanisms/v035'

def render_record(rid,index,record,title,equation):
    from rdkit import Chem
    from rdkit.Chem import rdDepictor,rdMolDescriptors
    from rdkit.Chem.Draw import rdMolDraw2D
    left,right,moves,legend=record
    params=Chem.SmilesParserParams();params.removeHs=False
    lm,rm=[Chem.MolFromSmiles(x,params) for x in (left,right)]
    assert lm is not None and rm is not None,(rid,index)
    assert rdMolDescriptors.CalcMolFormula(lm)==rdMolDescriptors.CalcMolFormula(rm),(rid,index,rdMolDescriptors.CalcMolFormula(lm),rdMolDescriptors.CalcMolFormula(rm))
    assert Chem.GetFormalCharge(lm)==Chem.GetFormalCharge(rm)
    positions={};parts=[]
    for n,mol in enumerate([lm,rm]):
        maps={a.GetAtomMapNum():a.GetIdx() for a in mol.GetAtoms() if a.GetAtomMapNum()}
        for a in mol.GetAtoms():a.SetAtomMapNum(0)
        rdDepictor.Compute2DCoords(mol)
        drawer=rdMolDraw2D.MolDraw2DSVG(550,300)
        opts=drawer.drawOptions();opts.clearBackground=False;opts.padding=.15;opts.fixedFontSize=19
        if rid=='sn1-core':
            for num,idx in maps.items():
                if mol.GetAtomWithIdx(idx).GetAtomicNum()==0:opts.atomLabels[idx]={1:'R',3:'R',4:'R',5:'X',6:'Nu'}[num]+('−' if mol.GetAtomWithIdx(idx).GetFormalCharge()<0 else '')
        if rid=='sn2-chloride':
            for num in (1,3):
                if num in maps:opts.atomLabels[maps[num]]=('Cl(in)' if num==1 else 'Cl(out)')+('−' if mol.GetAtomWithIdx(maps[num]).GetFormalCharge()<0 else '')
        drawer.DrawMolecule(mol);drawer.FinishDrawing()
        raw=drawer.GetDrawingText();inner=raw[raw.index('> ',raw.index('<svg'))+2:] if False else raw[raw.index('>',raw.index('<svg'))+1:raw.rindex('</svg>')]
        parts.append(f'<g transform="translate({25+n*600},100)">{inner}</g>')
        if n==0:
            for num,idx in maps.items():
                p=drawer.GetDrawCoords(idx);positions[num]=(p.x+25,p.y+100)
    def point(ref):
        if isinstance(ref,int):return positions[ref]
        a,b=[positions[i] for i in ref];return ((a[0]+b[0])/2,(a[1]+b[1])/2)
    arrows=''
    for j,move in enumerate(moves):
        origin,target=move[:2];electrons=move[2] if len(move)>2 else 2
        x,y=point(origin);u,v=point(target);dx,dy=u-x,v-y;length=max(1,(dx*dx+dy*dy)**.5)
        if isinstance(origin,int):x+=dx/length*12;y+=dy/length*12
        if isinstance(target,int):u-=dx/length*14;v-=dy/length*14
        bend=(1 if j%2==0 else -1)*min(70,length*.65)
        cx=(x+u)/2-dy/length*bend;cy=(y+v)/2+dx/length*bend
        arrows+=f'<path data-electrons="{electrons}" d="M{x:.2f},{y:.2f} Q{cx:.2f},{cy:.2f} {u:.2f},{v:.2f}" fill="none" stroke="#aa6a4e" stroke-width="2.6" marker-end="url(#{'fish' if electrons==1 else 'pair'})"/>'
    # Structural panels plus an explicit chemical-arrow legend; neither is computed geometry.
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 525" role="img" aria-label="{escape(title)} event {index+1}"><title>{escape(title)} event {index+1}</title><desc>{escape(equation+' '+legend)}</desc><rect width="1200" height="525" fill="#fffefa"/><defs><marker id="pair" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="#aa6a4e" stroke-width="1.5"/></marker><marker id="fish" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1 L9 5" fill="none" stroke="#aa6a4e" stroke-width="1.5"/></marker></defs><g font-family="DejaVu Sans,sans-serif" fill="#203c43"><text x="30" y="35" font-size="22">{escape(title)} · event {index+1}</text><text x="30" y="68" font-size="17">{escape(equation)}</text>{''.join(parts)}{arrows}<text x="580" y="260" font-size="36">→</text><text x="30" y="438" font-size="15">{escape(legend[:145])}</text><text x="30" y="467" font-size="15">{escape(legend[145:])}</text><text x="30" y="502" font-size="14">Original structural mechanism · {'1-electron fishhooks' if rid.startswith('radical') else '2-electron curved arrows'} · 2D depiction, not a calculated trajectory.</text></g></svg>'''
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/f'{rid}-step-{index+1}.svg';path.write_text(svg)
    return {'src':str(path.relative_to(ROOT/'dist')),'scope':'Original substrate-matched structural event with atom/bond-anchored '+('one-electron fishhooks' if rid.startswith('radical') else 'two-electron arrows')+'; schematic 2D geometry.',
            'arrowCount':len(moves),'reactantSmiles':left,'productSmiles':right,'electronMoves':moves,'reviewLegend':legend,'formula':rdMolDescriptors.CalcMolFormula(lm)}

def status(f):
    if 'terminal carbon remains' in f.get('reviewNote',''):return 'scientifically inconsistent'
    if not f.get('display'):return 'missing' if f.get('match') in ['pending','exact'] else ('partial' if f.get('match')=='partial' else 'representative')
    if f.get('coverage')=='partial':return 'partial'
    return 'complete' if f.get('match')=='exact' and f.get('reviewed') else 'representative'

def apply_v035(reactions):
    inventory=[]
    for r in reactions:
        before=deepcopy(r['figure']);entry={'id':r['id'],'name':r['name'],'beforeStatus':status(before),'beforeFigure':before,'events':[]}
        if r['id'] in S:
            assert len(S[r['id']])==len(r['steps'])
            paths=[]
            for i,(s,rec) in enumerate(zip(r['steps'],S[r['id']])):
                s['eventFigure']=render_record(r['id'],i,rec,r['name'],s['equation']);paths.append(s['eventFigure']['src'])
            # Full overview embeds the identical reviewed event drawings, without redrawing.
            body=''.join(f'<image href="{Path(p).name}" x="0" y="{i*525}" width="1200" height="525"/>' for i,p in enumerate(paths))
            # Inline each original SVG to keep source downloads self-contained.
            body=''.join(f'<g transform="translate(0,{i*525})">'+re.sub(r'^.*?<svg[^>]*>|</svg>\s*$','', (ROOT/'dist'/p).read_text(),flags=re.S)+'</g>' for i,p in enumerate(paths))
            overview=OUT/(r['id']+'.svg');overview.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {525*len(paths)}">'+body+'</svg>')
            rel=str(overview.relative_to(ROOT/'dist'))
            r['figure']={**before,'priorReference':before,'src':rel,'href':rel,'alt':'Original exact structural mechanism: '+r['name'],
                'match':'exact','coverage':'complete','reviewed':True,'display':True,'credit':'SORG Atlas · original SVG; RDKit 2D depiction',
                'rightsStatus':'original','license':'Original SORG Atlas illustration · CC BY-NC-SA 4.0','licenseUrl':'https://creativecommons.org/licenses/by-nc-sa/4.0/',
                'reviewNote':'Authored electron arrows originate at mapped atoms or bonds. Formula/charge balance checked; structural intermediates and arrows visually reviewed. Stereochemistry is unspecified unless explicitly drawn; existing pathway-model limitations apply.'}
        entry['afterStatus']=status(r['figure']);entry['afterFigure']=r['figure']['src'];entry['afterDisplayed']=r['figure']['display']
        for i,s in enumerate(r['steps']):
            ef=s.get('eventFigure')
            entry['events'].append({'index':i+1,'code':s['code'],'title':s['title'],'equation':s['equation'],
               'beforeStatus':entry['beforeStatus'],'afterStatus':entry['afterStatus'],
               'focusedImage':ef['src'] if ef else None,'coverageBasis':'Authored focused structural SVG' if r['id'] in S else 'Inherited v0.3.4 image/scope record; no new external-image verification',
               'limitations':s.get('assignmentNote','')})
        inventory.append(entry)
    # The calculated model remains outside the 31-entry teaching reaction catalog.
    render_record('sn2-chloride',0,S['sn2-chloride'][0],'Chloride identity SN2','Cl⁻ + CH₃Cl → ClCH₃ + Cl⁻ (incoming/outgoing Cl labeled)')
    target=ROOT/'dist/mechanism-inventory.json';target.write_text(json.dumps({'version':'0.3.5','reactions':inventory},indent=2,ensure_ascii=False))
    lines=['# v0.3.5 mechanism illustration inventory','', 'Status is reviewed chemical coverage, not file existence. All original sources are retained in JSON, including rejected/representative references. “Missing” means no displayed reviewed image; existing written equations are retained. Inherited reviews are identified explicitly.','', '| Reaction | v0.3.4 status | Previously displayed | v0.3.5 status | Events | Focused event images |','|---|---|---|---|---:|---:|']
    lines += [f"| {e['name']} | {e['beforeStatus']} | {e['beforeFigure']['display']} | {e['afterStatus']} | {len(e['events'])} | {sum(bool(x['focusedImage']) for x in e['events'])} |" for e in inventory]
    for e in inventory:
        lines += ['', '## '+e['name'], '', 'Previous review: '+e['beforeFigure'].get('reviewNote',''),'', 'Current: '+e['afterStatus']+'. Image: `'+e['afterFigure']+'`.']
        for s in e['events']:lines+=['',f"- Event {s['index']} · {s['code']} · {s['afterStatus']}: {s['equation']}",f"  Image: `{s['focusedImage'] or 'full overview only'}`. {s['coverageBasis']}. {s['limitations']}"]
    (ROOT/'audit/V035_MECHANISM_INVENTORY.md').write_text('\n'.join(lines)+'\n')
