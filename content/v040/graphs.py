"""Small connectivity-only SMILES reader/2D graph renderer for authored examples.
Not an electronic calculation, conformer generator, or general SMILES implementation.
Supported subset is checked strictly; chirality/stereo must be annotated separately.
"""
import re,math
from html import escape
TOKEN=re.compile(r'\[[^\]]+\]|Br|Cl|[BCNOSPFI]|[cnos]|[0-9]|[()=.#-]')
VAL={'C':4,'N':3,'O':2,'S':2,'P':3,'B':3,'F':1,'Cl':1,'Br':1,'I':1,'Zn':2}
def parse(text):
 tokens=TOKEN.findall(text);assert ''.join(tokens)==text,('Unsupported graph notation',text)
 atoms=[];edges=[];stack=[];rings={};previous=None;order=None
 for t in tokens:
  if t=='(':stack.append(previous);continue
  if t==')':previous=stack.pop();continue
  if t=='.':previous=None;continue
  if t in ['=','#','-']:order={'=':2,'#':3,'-':1}[t];continue
  if t.isdigit():
   if t in rings:
    other,bond=rings.pop(t);edges.append((other,previous,order or bond or (1.5 if atoms[other]['aromatic'] and atoms[previous]['aromatic'] else 1)))
   else:rings[t]=(previous,order)
   order=None;continue
  bracket=t.startswith('[');raw=t[1:-1] if bracket else t;match=re.match(r'([A-Z][a-z]?|[cnos])',raw);assert match,raw;element=match[1].capitalize();assert element in VAL,element
  charge=(int(re.search(r'\+(\d+)',raw)[1]) if re.search(r'\+(\d+)',raw) else raw.count('+'))-(int(re.search(r'-(\d+)',raw)[1]) if re.search(r'-(\d+)',raw) else raw.count('-'))
  hm=re.search(r'H(\d*)',raw);h=int(hm[1] or 1) if hm else (0 if bracket else None)
  i=len(atoms);atoms.append(dict(element=element,charge=charge,hydrogens=h,aromatic=match[1].islower()))
  if previous is not None:edges.append((previous,i,order or (1.5 if atoms[previous]['aromatic'] and atoms[i]['aromatic'] else 1)))
  previous=i;order=None
 assert not stack and not rings
 for i,a in enumerate(atoms):
  val=sum(b for x,y,b in edges if i in [x,y]);target=VAL[a['element']]+(1 if a['element']=='N' and a['charge']>0 else -1 if a['element']=='O' and a['charge']<0 else 0)
  if a['hydrogens'] is None:a['hydrogens']=max(0,round(target-val))
  assert val+a['hydrogens']<=max(target,6 if a['element'] in ['S','P'] else target)+.01,(text,a,val)
 return atoms,edges

def draw(text,x,y,width,height,stereo=None):
 atoms,edges=parse(text);n=len(atoms);positions=[[math.cos(i*2*math.pi/n)*90,math.sin(i*2*math.pi/n)*90] for i in range(n)];bonded={(min(a,b),max(a,b)) for a,b,_ in edges}
 # Deterministic force-directed graph drawing only. These positions carry no
 # molecular-energy or stereochemical interpretation.
 for iteration in range(350):
  f=[[0.,0.] for _ in atoms]
  for a in range(n):
   for b in range(a):
    dx=positions[a][0]-positions[b][0];dy=positions[a][1]-positions[b][1];d=max(2,math.hypot(dx,dy));rep=1100/(d*d)
    for k,v in enumerate([dx/d*rep,dy/d*rep]):f[a][k]+=v;f[b][k]-=v
  for a,b,_ in edges:
   dx=positions[b][0]-positions[a][0];dy=positions[b][1]-positions[a][1];d=max(.1,math.hypot(dx,dy));spring=(d-55)*.06
   for k,v in enumerate([dx/d*spring,dy/d*spring]):f[a][k]+=v;f[b][k]-=v
  for a in range(n):
   for k in range(2):positions[a][k]+=max(-3,min(3,f[a][k]))*.7
 if stereo:
  double=next(((a,b) for a,b,o in edges if o==2 and atoms[a]['element']==atoms[b]['element']=='C'),None)
  if double:
   a,b=double;adj={i:[] for i in range(n)}
   for i,j,_ in edges:
    if {i,j}!={a,b}:adj[i].append(j);adj[j].append(i)
   for center,other,target in [(a,b,(-35,45)),(b,a,(35,45 if stereo=='Z' else -45))]:
    neighbors=adj[center]
    if not neighbors:continue
    neighbor=neighbors[0];old=positions[center][:];dx=positions[neighbor][0]-old[0];dy=positions[neighbor][1]-old[1];angle=math.atan2(target[1],target[0])-math.atan2(dy,dx);visited={center};queue=[center]
    while queue:
     for j in adj[queue.pop()]:
      if j not in visited:visited.add(j);queue.append(j)
    assert other not in visited,'Stereo constraint requires an acyclic alkene'
    origin=(0,0) if center==a else (65,0)
    for i in visited:
     x0=positions[i][0]-old[0];y0=positions[i][1]-old[1];positions[i]=[origin[0]+x0*math.cos(angle)-y0*math.sin(angle),origin[1]+x0*math.sin(angle)+y0*math.cos(angle)]
 lo=[min(p[k] for p in positions) for k in range(2)];hi=[max(p[k] for p in positions) for k in range(2)];scale=min((width-65)/max(1,hi[0]-lo[0]),(height-45)/max(1,hi[1]-lo[1]),1.3);pos=[(x+width/2+(p[0]-(hi[0]+lo[0])/2)*scale,y+height/2+(p[1]-(hi[1]+lo[1])/2)*scale) for p in positions];out=''
 for a,b,order in edges:
  ax,ay=pos[a];bx,by=pos[b];dx=bx-ax;dy=by-ay;d=max(1,math.hypot(dx,dy));ox=-dy/d*3;oy=dx/d*3
  shifts=[0] if order==1 else [-1,1] if order in [1.5,2] else [-1.4,0,1.4]
  for j,q in enumerate(shifts):out+=f'<path d="M{ax+q*ox:.2f},{ay+q*oy:.2f} L{bx+q*ox:.2f},{by+q*oy:.2f}" stroke="#203c43" stroke-width="2" fill="none"'+(' stroke-dasharray="4 3"' if order==1.5 and j==1 else '')+'/>'
 for a,(ax,ay) in zip(atoms,pos):
  label=a['element']+('H'+(str(a['hydrogens']) if a['hydrogens']>1 else '') if a['hydrogens'] else '')+('+' if a['charge']==1 else '−' if a['charge']==-1 else str(a['charge']) if a['charge'] else '')
  out+=f'<rect x="{ax-len(label)*5:.2f}" y="{ay-10:.2f}" width="{len(label)*10}" height="20" fill="#fffefa"/><text x="{ax:.2f}" y="{ay+5:.2f}" font-size="16" text-anchor="middle" fill="#203c43">{escape(label)}</text>'
 return out

def cover(r,pair):
 stereo='Z' if r['id']=='lindlar-reduction' else 'E' if r['id'] in ['dissolving-metal-reduction','horner-wadsworth-emmons','heck'] else None
 body=draw(pair[0],25,58,500,245)+draw(pair[1],665,58,500,245,stereo)
 note='Representative substrate/product connectivity; other reagents/byproducts are in the equation. No computed geometry.'
 svg=f'<g font-family="DejaVu Sans,sans-serif"><rect width="1200" height="350" fill="#fffefa"/><text x="25" y="32" font-size="21" fill="#203c43">{escape(r["name"])} · representative molecular graphs</text>{body}<text x="580" y="180" font-size="32" fill="#203c43">→</text><text x="25" y="330" font-size="15" fill="#203c43">{escape(note)}</text>'
 if stereo:svg+=f'<text x="680" y="60" font-size="20">{stereo} alkene · relative double-bond geometry specified</text>'
 return svg+'</g>',350
