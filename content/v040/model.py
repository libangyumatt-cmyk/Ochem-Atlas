"""Authored teaching events and condensed structural SVGs. No quantum computation."""
from pathlib import Path
from html import escape
import re,json,textwrap
ROOT=Path(__file__).resolve().parents[2]
SOURCES={
 'v4-openstax':dict(title='John McMurry, Organic Chemistry (OpenStax, 2023)',url='https://openstax.org/details/books/organic-chemistry',publisher='OpenStax / Rice University',scope='Open textbook: functional-group reactions, selectivity and teaching mechanisms; topic locators are attached to each entry.',checked=None),
 'v4-clayden':dict(title='Clayden, Greeves and Warren, Organic Chemistry, 2nd ed. (Oxford, 2012), ISBN 9780199270293',url='https://search.worldcat.org/isbn/9780199270293',publisher='Oxford University Press',scope='Mechanistic reference for rearrangements, radicals, stereoelectronics and synthesis. No unverified page numbers asserted.',checked=None),
 'v4-hartwig':dict(title='John F. Hartwig, Organotransition Metal Chemistry: From Bonding to Catalysis (2010), ISBN 9781891389535',url='https://search.worldcat.org/isbn/9781891389535',publisher='University Science Books',scope='Elementary organometallic transformations and catalytic-cycle models; actual speciation can differ.',checked=None),
 'v4-nobel':dict(title='Nobel Prize in Chemistry 2010: Palladium-catalyzed cross couplings in organic synthesis — scientific background',url='https://www.nobelprize.org/uploads/2018/06/advanced-chemistryprize2010.pdf',publisher='Royal Swedish Academy of Sciences',scope='Historical and mechanistic background for Heck, Negishi and Suzuki coupling.',checked=None),
 'v4-sonogashira':dict(title='Chinchilla and Nájera, The Sonogashira Reaction: A Booming Methodology in Synthetic Organic Chemistry, Chem. Rev. 107 (2007), 874–922',url='https://doi.org/10.1021/cr050992x',publisher='American Chemical Society',scope='Pd/Cu and copper-free variants, side reactions and mechanistic models.',checked=None)}
KINDS={
 'pt':('1122','Proton transfer','Lone-pair donation into the donor H–X antibonding coordinate; the X–H pair returns to X.','A near-collinear donor–H–acceptor arrangement; solution can use solvent relays.'),
 'sn2':('1122','Bond-replacing displacement','Occupied nucleophile orbital donates into the electrophile–leaving-group antibonding orbital.','Approach opposite the leaving group; inversion at a stereogenic carbon in the direct SN2 model.'),
 'add':('1113','Nucleophilic carbonyl addition','Occupied donor orbital overlaps the polarized carbonyl π* orbital; C=O π electrons move to oxygen.','Attack on a carbonyl face changes planar carbon toward a tetrahedral center; facial selectivity is substrate dependent.'),
 'collapse':('1113','Tetrahedral intermediate collapse','A heteroatom lone pair forms a C=O or C=N π bond while a leaving-group bond breaks.','The tetrahedral center approaches a planar π-bonded arrangement; protonation controls leaving-group ability.'),
 'polar':('1133','Coupled polar bond reorganization','Polar donor–acceptor interactions couple the stated σ/π bond changes; this is the inherited candidate R3 convention.','The specifically named reacting bonds must align; concerted polar bookkeeping is not automatically a symmetry-governed pericyclic assignment.'),
 'ion':('1111','Heterolytic ionization','The departing group takes the indicated bond electron pair; solvation or Lewis-acid coordination stabilizes charge.','Bond separation precedes capture in the limiting ionization model; tight ion pairs may persist.'),
 'capture':('1111','Lone-pair capture','An occupied donor orbital overlaps the empty orbital of the named cation or Lewis acid.','Approach follows the acceptor geometry; capture is not evidence for a freely solvated cation.'),
 'peri':('1333','Concerted cyclic reorganization','A cyclic array of interacting orbitals redistributes the stated electron pairs in one event.','Orbital phases and the stated electron count control allowed topology; no discrete intermediate is inserted into a concerted event.'),
 'radadd':('2211','Radical bond formation','SOMO/π interaction forms a bond and redistributes one electron to the stated radical center.','Radical approach and substrate conformation control regioselectivity; a fishhook denotes one electron.'),
 'hat':('2222','Radical atom transfer','A SOMO interacts with a σ bond; one electron accompanies the transferred atom and the other remains at the new radical center.','A donor–atom–acceptor transfer geometry is required; atom transfer is not heterolytic proton transfer.'),
 'open':(None,'Mechanistic boundary / grouped stage','The stated electron-transfer, metal or surface process is not uniquely described by the existing eight-code project codebook.','Follow the specified molecular or surface geometry. No four-digit code is invented for an undefined event type.')}
def E(kind,left,right,flow,moves=(),title=None,scope=None):
 code,default,orb,geo=KINDS[kind]
 if kind=='add' and 'N+' in left and '=O' not in left:orb='The reagent sigma donor transfers to iminium pi*(C=N); C=N pi electrons return to nitrogen.';geo='Approach to a planar iminium carbon produces a tetrahedral amine carbon; facial selectivity depends on substrate.'
 return dict(kind=kind,title=title or default,code=code,left=left,right=right,flow=flow,moves=list(moves),orbital=orb,geometry=geo,scope=scope)
def R(rid,name,family,equation,conditions,selectivity,steps,aliases=(),scope='',source='v4-openstax',topic=''):
 return dict(id=rid,name=name,family=family,equation=equation,conditions=conditions,selectivity=selectivity,events=steps,aliases=list(aliases),scope=scope,reference=source,referenceTopic=topic)
def plain(s):return re.sub(r'\{([^|{}]+)\|([^{}]+)\}',lambda m:m[2],s)
def structural_line(s,x,y,width):
 # Condensed structural formula convention: branches in parentheses, explicit
 # double/triple bonds, charges, radicals and defined spectator R/Ar/L groups.
 tokens=[];cursor=0
 for m in re.finditer(r'\{([^|{}]+)\|([^{}]+)\}',s):
  if m.start()>cursor:tokens.append((None,s[cursor:m.start()]))
  tokens.append((m[1],m[2]));cursor=m.end()
 if cursor<len(s):tokens.append((None,s[cursor:]))
 size=min(24,width/max(1,len(plain(s))*.62));size=max(11,size);advance=size*.62;out=[];points={};pos=x
 for key,value in tokens:
  out.append(f'<text x="{pos:.2f}" y="{y}" font-size="{size:.2f}">{escape(value)}</text>')
  if key:assert key not in points;points[key]=(pos+advance*len(value)/2,y-size*.35)
  pos+=advance*len(value)
 return ''.join(out),points
def render(r,event,i):
 rid=r['id'];ident=f'{rid}-{i+1}';body,points=structural_line(event['left'],24,155,520);right,_=structural_line(event['right'],665,155,510);body+=right
 def point(ref):
  if isinstance(ref,str):return points[ref]
  a,b=map(point,ref);return((a[0]+b[0])/2,(a[1]+b[1])/2)
 for j,move in enumerate(event['moves']):
  a,b=move[:2];electrons=move[2] if len(move)>2 else 2;x,y=point(a);u,v=point(b);bend=(-1 if j%2==0 else 1)*(48+j*9)
  body+=f'<path data-electrons="{electrons}" d="M{x:.2f},{y-5:.2f} Q{(x+u)/2:.2f},{y+bend:.2f} {u:.2f},{v-9:.2f}" fill="none" stroke="#aa6a4e" stroke-width="2.3" marker-end="url(#{ident}-'+('fish' if electrons==1 else 'pair')+')"/>'
 if not event['moves']:
  # Explicitly model-level stages use process arrows, not fictitious electron arrows.
  body+='<text x="30" y="202" font-size="16">Process model: no unique microscopic electron-arrow sequence asserted.</text>'
 for n,line in enumerate(textwrap.wrap(event['flow'],132)):body+=f'<text x="24" y="{235+n*23}" font-size="16">{escape(line)}</text>'
 height=290+23*max(0,len(textwrap.wrap(event['flow'],132))-2)
 header=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" role="img"><title>{escape(r["name"]+": "+event["title"])}</title><desc>{escape(plain(event["left"])+" → "+plain(event["right"])+". "+event["flow"])}</desc><rect width="1200" height="{height}" fill="#fffefa"/><defs><marker id="{ident}-pair" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#aa6a4e"/></marker><marker id="{ident}-fish" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5" fill="none" stroke="#aa6a4e"/></marker></defs><g fill="#203c43" font-family="DejaVu Sans Mono,monospace"><text x="24" y="32" font-size="21">{escape(r["name"])} · {i+1}</text><text x="24" y="65" font-size="17">{escape(event["title"])}</text><text x="585" y="155" font-size="28">→</text>'
 svg=header+body+'</g></svg>';p=ROOT/'dist/mechanisms/v040'/f'{ident}.svg';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(svg);return str(p.relative_to(ROOT/'dist')),svg,height
