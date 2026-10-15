/* Reusable renderer for precomputed signed surfaces. No electronic calculation. */
export async function createSurfaceViewer(host,{geometryOnly=false}={}){
 const colors={C:0x344b53,H:0xd9dedb,Cl:0x6e9673};
 let state=null,scene,camera,renderer,controls,group,THREE,resizeObserver,webgl=false;
 const stage=document.createElement('div');stage.className='reaction-stage';host.replaceChildren(stage);
 const labels=document.createElement('div');labels.className='reaction-atom-labels';
 const status=document.createElement('p');status.className='small-note';host.append(status);
 function fallback(){
  stage.replaceChildren();const can=document.createElement('canvas');can.width=720;can.height=460;can.setAttribute('role','img');can.setAttribute('aria-label','Fixed projection of calculated geometry and sampled isosurfaces');stage.append(can);
  const ctx=can.getContext('2d');if(!ctx){stage.textContent='Canvas unavailable. Download geometry, coefficients and volumetric fields below.';return;}
  if(!state)return;
  const {atoms,mesh,reverse,singleColor}=state;
  ctx.fillStyle='#f2f4ec';ctx.fillRect(0,0,720,460);
  const project=([x,y,z])=>[360+((x*.8+y*.6)*48),230+((x*.22-y*.3-z*.92)*48),x*.3-y*.6+z*.35];
  const tris=[];
  if(!geometryOnly)for(const [sign,surf] of Object.entries(mesh||{})){
   if(!surf)continue;const points=[];for(let i=0;i<surf.vertices.length;i+=3)points.push(project(surf.vertices.slice(i,i+3)));
   const color=singleColor?'#397f79':(sign==='positive')!==Boolean(reverse)?'#397f79':'#bd8755';
   for(let i=0;i<surf.faces.length;i+=3){const p=surf.faces.slice(i,i+3).map(j=>points[j]);tris.push({p,color,depth:p.reduce((n,v)=>n+v[2],0)/3});}
  }
  tris.sort((a,b)=>a.depth-b.depth);ctx.globalAlpha=.38;
  for(const {p,color} of tris){ctx.beginPath();ctx.moveTo(p[0][0],p[0][1]);ctx.lineTo(p[1][0],p[1][1]);ctx.lineTo(p[2][0],p[2][1]);ctx.closePath();ctx.fillStyle=color;ctx.fill();}
  ctx.globalAlpha=1;
  const pts=atoms.map(a=>project(a.xyzAngstrom));
  for(let j=1;j<atoms.length;j++){ctx.beginPath();ctx.setLineDash(j<3?[5,5]:[]);ctx.strokeStyle='#7b8a86';ctx.moveTo(pts[0][0],pts[0][1]);ctx.lineTo(pts[j][0],pts[j][1]);ctx.stroke();}
  ctx.setLineDash([]);
  for(let i=0;i<atoms.length;i++){const p=pts[i],a=atoms[i];ctx.beginPath();ctx.arc(p[0],p[1],a.element==='H'?5:8,0,2*Math.PI);ctx.fillStyle='#'+colors[a.element].toString(16).padStart(6,'0');ctx.fill();ctx.fillStyle='#203c43';ctx.font='15px sans-serif';ctx.fillText(a.label,p[0]+9,p[1]-8);}
  status.textContent='FIXED CALCULATED PROJECTION · WebGL unavailable. Threshold and phase controls update the same computed meshes. Dashed C···Cl lines are distance guides, not assigned bonds.';
 }
 function draw(){
  if(!webgl){fallback();return;}
  renderer.render(scene,camera);
  for(const el of labels.children){const p=new THREE.Vector3(...JSON.parse(el.dataset.position)).project(camera);el.style.left=((p.x+1)*.5*stage.clientWidth)+'px';el.style.top=((-p.y+1)*.5*stage.clientHeight)+'px';}
 }
 function reset(){if(!webgl)return;controls.target.set(0,0,0);camera.position.set(8,6,9);controls.update();draw();}
 function update(next){
  state=next;if(!webgl){fallback();return;}
  for(const child of [...group.children]){group.remove(child);child.geometry?.dispose();child.material?.dispose();}
  labels.replaceChildren();
  if(!geometryOnly)for(const [sign,surf] of Object.entries(next.mesh||{})){
   if(!surf)continue;const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(surf.vertices,3));geo.setIndex(surf.faces);geo.computeVertexNormals();
   const color=next.singleColor?0x397f79:(sign==='positive')!==Boolean(next.reverse)?0x397f79:0xbd8755;
   group.add(new THREE.Mesh(geo,new THREE.MeshPhongMaterial({color,transparent:true,opacity:.58,depthWrite:false,side:THREE.DoubleSide})));
  }
  for(const a of next.atoms){const p=new THREE.Vector3(...a.xyzAngstrom);const ball=new THREE.Mesh(new THREE.SphereGeometry(a.element==='H'?.08:.14,14,10),new THREE.MeshPhongMaterial({color:colors[a.element]}));ball.position.copy(p);group.add(ball);const span=document.createElement('span');span.textContent=a.label;span.dataset.position=JSON.stringify(a.xyzAngstrom);labels.append(span);}
  for(let j=1;j<next.atoms.length;j++){const pts=[new THREE.Vector3(...next.atoms[0].xyzAngstrom),new THREE.Vector3(...next.atoms[j].xyzAngstrom)];const geo=new THREE.BufferGeometry().setFromPoints(pts);const line=new THREE.Line(geo,j<3?new THREE.LineDashedMaterial({color:0x7b8a86,dashSize:.08,gapSize:.07}):new THREE.LineBasicMaterial({color:0x7b8a86}));line.computeLineDistances();group.add(line);}
  draw();
 }
 try{
  const probe=document.createElement('canvas');if(!probe.getContext('webgl2'))throw Error('WebGL2 unavailable');
  THREE=await import('three');const {OrbitControls}=await import('three/addons/controls/OrbitControls.js');
  renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));stage.append(renderer.domElement,labels);
  renderer.domElement.style.touchAction='none';scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(38,1,.05,120);group=new THREE.Group();scene.add(group,new THREE.HemisphereLight(0xffffff,0xb9c9c0,2.5));
  const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(3,4,6);scene.add(light);
  controls=new OrbitControls(camera,renderer.domElement);controls.enablePan=false;controls.minDistance=3;controls.maxDistance=25;controls.touches.ONE=THREE.TOUCH.ROTATE;controls.touches.TWO=THREE.TOUCH.DOLLY_PAN;
  controls.addEventListener('change',draw);webgl=true;
  const resize=()=>{const w=stage.clientWidth,h=stage.clientHeight;if(!w||!h)return;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);draw();};
  resizeObserver=new ResizeObserver(resize);resizeObserver.observe(stage);resize();reset();status.textContent='INTERACTIVE 3D · drag/swipe to rotate, wheel/pinch to zoom. Dashed C···Cl lines indicate measured separations, not bond orders.';
 }catch(e){webgl=false;fallback();}
 return {update,reset,get interactive(){return webgl;},dispose(){resizeObserver?.disconnect();controls?.dispose();renderer?.dispose();host.replaceChildren();}};
}
