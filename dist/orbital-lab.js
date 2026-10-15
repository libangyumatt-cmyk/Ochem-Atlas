/* Fixed-geometry PySCF orbital meshes; Three.js provides the camera and rendering. */
(async function(){
 'use strict';
 const $=s=>document.querySelector(s),status=$('#orbital-status');
 let data,system,orbital,phaseReversed=false,view=null;
 const fallback=$('#orbital-fallback'),canvas=$('#orbital-canvas'),labels=$('#orbital-labels');
 try{
  const response=await fetch('orbital-data.json?v=0.3.3');
  if(!response.ok)throw Error(`dataset HTTP ${response.status}`);
  data=await response.json();
  if(data.schemaVersion!=='1.0'||data.systems.length!==3)throw Error('unexpected orbital dataset');
 }catch(error){status.textContent=`Computed orbital data unavailable (${error.message}); static H₂ image shown.`;return;}
 const atomColor={H:0xd9dedb,C:0x344b53,O:0xc97961};
 const bondsFor=(atoms)=>{
  const result=[];
  for(let i=0;i<atoms.length;i++)for(let j=i+1;j<atoms.length;j++){
   const a=atoms[i],b=atoms[j],d=Math.hypot(...a.xyzAngstrom.map((v,k)=>v-b.xyzAngstrom[k]));
   if(d<1.47 && (a.element!=='H'||b.element!=='H'||atoms.length===2))result.push([i,j]);
  }
  return result;
 };
 function refresh(){
  system=data.systems.find(s=>s.id===$('#lab-molecule').value)||data.systems[0];
  orbital=system.orbitals.find(o=>o.index===Number($('#lab-orbital').value))||system.orbitals[0];
  $('#lab-orbital-title').textContent=`${orbital.name} · ${system.name}`;
  $('#lab-orbital-explain').textContent=orbital.description;
  $('#lab-metadata').innerHTML=`<dt>System</dt><dd>${system.name} · neutral singlet · ${system.electronCount} electrons · fixed input geometry</dd><dt>Identity</dt><dd>MO ${orbital.index} · ${orbital.character} · ${orbital.occupation} occupied electron${orbital.occupation===1?'':'s'} · ${orbital.energyHartree.toFixed(5)} hartree (method-dependent eigenvalue)</dd><dt>Calculation</dt><dd>PySCF 2.14.0 · restricted Hartree–Fock · STO-3G · isolated gas-phase molecule</dd><dt>Surface</dt><dd>ψ = ±0.035 bohr⁻³ᐟ² · sampled 44³ grid · mesh points rounded to 0.001 Å · global phase arbitrary</dd>`;
  $('#lab-phase-note').textContent=phaseReversed?'Colors reversed: the entire real orbital was multiplied by −1. |ψ|² and the nodes are unchanged.':'Reversing both colors multiplies ψ by −1 and leaves |ψ|² and the nodes unchanged.';
  $('#phase-legend-plus').className=phaseReversed?'phase-minus':'phase-plus';
  $('#phase-legend-minus').className=phaseReversed?'phase-plus':'phase-minus';
  if(!orbital.mesh.negative)$('#lab-phase-note').textContent+=' This 1σg grid has no negative-amplitude region at the chosen isovalue.';
  $('#lab-phase').setAttribute('aria-pressed',String(phaseReversed));
  $('#lab-cube').href=`orbital-files/${system.id}-mo${orbital.index}.cube.gz`;
  $('#lab-geometry').href=`orbital-files/${system.id}.xyz`;
  $('#lab-output').href=`orbital-files/${system.id}.log`;
  $('#lab-coeff').href=`orbital-files/${system.id}-scf.npz`;
  fallback.src=`orbital-files/${system.id}-mo${orbital.index}.png`;
  fallback.alt=`Static projection of computed ${system.name} ${orbital.name} isosurface at 0.035 bohr to minus three halves; positive and negative phases are different colors`;
  if(view)view.update(system,orbital,phaseReversed);
 }
 function selectMolecule(){
  const s=data.systems.find(x=>x.id===$('#lab-molecule').value)||data.systems[0];
  $('#lab-orbital').replaceChildren(...s.orbitals.map(o=>new Option(`${o.name} · ${o.character}`,String(o.index))));
  refresh();
 }
 $('#lab-molecule').addEventListener('change',selectMolecule);
 $('#lab-orbital').addEventListener('change',refresh);
 $('#lab-phase').addEventListener('click',()=>{phaseReversed=!phaseReversed;refresh();});
 $('#lab-reset').addEventListener('click',()=>{if(view)view.reset();else status.textContent='Static projection: WebGL camera unavailable.';});
 selectMolecule();
 try{
  const probe=document.createElement('canvas');
  const gl=probe.getContext('webgl2')||probe.getContext('webgl');
  if(!gl)throw Error('WebGL context unavailable in this browser');
  const THREE=await import('three');
  const {OrbitControls}=await import('three/addons/controls/OrbitControls.js');
  const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(38,1,.05,100);
  scene.add(new THREE.HemisphereLight(0xffffff,0xb9c9c0,2.4));
  const key=new THREE.DirectionalLight(0xffffff,2.2);key.position.set(3,4,6);scene.add(key);
  const controls=new OrbitControls(camera,renderer.domElement);
  controls.enablePan=false;controls.enableRotate=true;controls.enableZoom=true;controls.minDistance=1.2;controls.maxDistance=18;
  renderer.domElement.style.touchAction='none';
  controls.touches.ONE=THREE.TOUCH.ROTATE;controls.touches.TWO=THREE.TOUCH.DOLLY_PAN;
  const group=new THREE.Group();scene.add(group);
  let atoms=[];
  function render(){
   renderer.render(scene,camera);
   for(const [el,pos] of atoms){
    const p=pos.clone().project(camera);
    el.style.left=((p.x+1)*.5*canvas.clientWidth)+'px';
    el.style.top=((-p.y+1)*.5*canvas.clientHeight)+'px';
    el.hidden=p.z>1;
   }
  }
  function resize(){
   const w=canvas.clientWidth,h=canvas.clientHeight;
   if(!w||!h)return;
   camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);render();
  }
  function reset(){
   const pts=system.atoms.map(a=>a.xyzAngstrom);
   const center=new THREE.Vector3(...[0,1,2].map(k=>pts.reduce((sum,p)=>sum+p[k],0)/pts.length));
   controls.target.copy(center);camera.position.copy(center.clone().add(new THREE.Vector3(3.6,2.9,4.7)));
   controls.update();render();
  }
  function clear(){
   while(group.children.length){const o=group.children[0];group.remove(o);o.geometry?.dispose();o.material?.dispose();}
   labels.replaceChildren();atoms=[];
  }
  function update(s,o,reverse){
   clear();
   for(const [sign,color] of [['positive',reverse?0xbd8755:0x397f79],['negative',reverse?0x397f79:0xbd8755]]){
    const mesh=o.mesh[sign];if(!mesh)continue;
    const geometry=new THREE.BufferGeometry();
    geometry.setAttribute('position',new THREE.Float32BufferAttribute(mesh.vertices,3));
    geometry.setIndex(mesh.faces);geometry.computeVertexNormals();
    group.add(new THREE.Mesh(geometry,new THREE.MeshPhongMaterial({color,transparent:true,opacity:.65,depthWrite:false,side:THREE.DoubleSide,shininess:40})));
   }
   const sphere=new THREE.SphereGeometry(1,16,12);
   for(const atom of s.atoms){
    const p=new THREE.Vector3(...atom.xyzAngstrom),r=atom.element==='H'?.10:.16;
    const point=new THREE.Mesh(sphere.clone(),new THREE.MeshPhongMaterial({color:atomColor[atom.element]}));
    point.scale.setScalar(r);point.position.copy(p);group.add(point);
    const label=document.createElement('span');label.textContent=atom.label;labels.append(label);atoms.push([label,p]);
   }
   sphere.dispose();
   for(const [i,j] of bondsFor(s.atoms)){
    const p=new THREE.Vector3(...s.atoms[i].xyzAngstrom),q=new THREE.Vector3(...s.atoms[j].xyzAngstrom),v=q.clone().sub(p);
    const bond=new THREE.Mesh(new THREE.CylinderGeometry(.027,.027,v.length(),9),new THREE.MeshPhongMaterial({color:0x7b8a86}));
    bond.position.copy(p.clone().add(q).multiplyScalar(.5));bond.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());group.add(bond);
   }
   reset();
  }
  renderer.domElement.setAttribute('aria-label','Rotatable computed molecular orbital; use molecule and orbital selectors to change the surface');
  canvas.append(renderer.domElement);canvas.hidden=false;fallback.hidden=true;
  view={update,reset};
  controls.addEventListener('change',render);
  if(typeof ResizeObserver==='function')new ResizeObserver(resize).observe(canvas);
  else window.addEventListener('resize',resize);
  resize();update(system,orbital,phaseReversed);
  status.textContent='INTERACTIVE 3D · drag or swipe directly on the molecular surface to rotate; wheel or pinch to zoom.';
 }catch(error){
  canvas.hidden=true;fallback.hidden=false;
  view=null;phaseReversed=false;$('#lab-phase').disabled=true;refresh();
  status.textContent=`STATIC IMAGE — rotation unavailable. 3D initialization failed: ${error.message}. Try Chrome Settings → Site settings → JavaScript / hardware acceleration, or another device.`;
 }
})();
