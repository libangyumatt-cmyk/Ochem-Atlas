/* Fixed-geometry PySCF orbital meshes; Three.js provides the camera and rendering. */
(async function(){
 'use strict';
 const $=s=>document.querySelector(s),status=$('#orbital-status');
 let data,extra,system,orbital,phaseReversed=false,view=null;
 let webglAvailable=false,previousSystem=null;
 const scan=$('#lab-scan'),step=$('#lab-torsion');
 const fallback=$('#orbital-fallback'),canvas=$('#orbital-canvas'),labels=$('#orbital-labels');
 try{
  const response=await fetch('orbital-data.json?v=0.3.4');
  if(!response.ok)throw Error(`dataset HTTP ${response.status}`);
  data=await response.json();
  if(data.schemaVersion!=='1.0'||data.systems.length!==3)throw Error('unexpected orbital dataset');
 }catch(error){status.textContent=`Computed orbital data unavailable (${error.message}); static H₂ image shown.`;return;}
 try{const r=await fetch('orbital-diversity.json?v=0.3.4');if(!r.ok)throw Error(r.status);extra=await r.json();data.systems.push(...extra.systems);for(const m of extra.systems)$('#lab-molecule').add(new Option(m.name,m.id));$('#lab-molecule').add(new Option('Ethylene torsion · computed scan','torsion'));}catch(e){$('#lab-evolution-note').textContent='New datasets unavailable; the original laboratory remains usable. '+e.message;}
 const atomColor={H:0xd9dedb,C:0x344b53,O:0xc97961};
 const bondsFor=(atoms)=>{
  const result=[];
  for(let i=0;i<atoms.length;i++)for(let j=i+1;j<atoms.length;j++){
   const a=atoms[i],b=atoms[j],d=Math.hypot(...a.xyzAngstrom.map((v,k)=>v-b.xyzAngstrom[k]));
   const radii={H:.31,C:.76,O:.66};
   if(d<1.2*(radii[a.element]+radii[b.element]) && (a.element!=='H'||b.element!=='H'||atoms.length===2))result.push([i,j]);
  }
  return result;
 };
 function selectedSystem(){
  return $('#lab-molecule').value==='torsion'?extra.scan[Number(step.value)]:data.systems.find(s=>s.id===$('#lab-molecule').value)||data.systems[0];
 }
 function refresh(){
  system=selectedSystem();
  orbital=system.orbitals.find(o=>o.index===Number($('#lab-orbital').value))||system.orbitals[0];
  const density=orbital.kind==='spin-density',isScan=$('#lab-molecule').value==='torsion';
  scan.hidden=!isScan;
  const method=system.method||'RHF',stem=orbital.fileStem||`${system.id}-mo${orbital.index}`;
  const base=orbital.fileStem?'v034/':'';
  $('#lab-orbital-title').textContent=`${orbital.name} · ${system.name}`;
  $('#lab-orbital-explain').textContent=orbital.description;
  $('#lab-metadata').innerHTML=`<dt>System</dt><dd>${system.name} · charge ${system.charge} · multiplicity ${system.multiplicity} · ${system.electronCount} electrons · ${system.geometryKind||'fixed input geometry'}</dd><dt>Identity</dt><dd>${density?'ρα − ρβ (all occupied orbitals)':`MO ${orbital.index} · ${orbital.spinChannel||'restricted'} · ${orbital.occupation} electron(s) · ${orbital.energyHartree.toFixed(5)} hartree (model eigenvalue) · ${orbital.symmetry||'see orbital description'}${system.pointGroup?` (group ${system.pointGroup}; subgroup labels depend on axes)`:''}`}</dd><dt>Calculation</dt><dd>PySCF 2.14.0 · ${method} · ${system.basis||'STO-3G'} · isolated gas phase${system.method?` · SCF converged · ⟨S²⟩ ${system.s2.toFixed(5)} · max |CᵀSC−I| ${system.orthonormalError.toExponential(1)}`:''}</dd><dt>Surface</dt><dd>${density?'ρα − ρβ':'ψ'} = ±${orbital.isovalue||.035} ${orbital.isovalueUnit||'bohr⁻³ᐟ²'} · 44³ grid · display rounding 0.001 Å</dd>`;
  $('#lab-phase').disabled=!webglAvailable||density;
  const reverse=!density&&phaseReversed;
  $('#lab-phase-note').textContent=density?'Spin density is not a wavefunction phase. Colors indicate alpha/beta excess; phase reversal is disabled. This ROHF density has no negative region at this threshold.':reverse?'Colors reversed: ψ → −ψ; density and nodes are unchanged.':'Global orbital sign is arbitrary. Reversing colors leaves density and nodes unchanged.';
  $('#phase-legend-plus').className=reverse?'phase-minus':'phase-plus';
  $('#phase-legend-minus').className=reverse?'phase-plus':'phase-minus';
  $('#lab-positive-label').textContent=density?'alpha excess (positive spin density)':'+ wavefunction phase';
  $('#lab-negative-label').textContent=density?'beta excess (negative spin density)':'− wavefunction phase';
  $('#lab-phase').setAttribute('aria-pressed',String(reverse));
  $('#lab-cube').href=`orbital-files/${stem}.cube.gz`;
  $('#lab-cube').textContent=density?'Sampled spin-density cube ↓':'Sampled orbital cube ↓';
  $('#lab-geometry').href=`orbital-files/${base}${system.id}.xyz`;
  $('#lab-output').href=`orbital-files/${base}${system.id}.log`;
  $('#lab-coeff').href=`orbital-files/${base}${system.id}-scf.npz`;
  fallback.src=`orbital-files/${stem}.png`;
  fallback.alt=`Computed static projection: ${system.name}, ${orbital.name}, threshold ${orbital.isovalue||.035} ${orbital.isovalueUnit||'bohr⁻³ᐟ²'}`;
  if(isScan){
   $('#lab-torsion-value').textContent=`${system.torsionDegrees}°`;
   const t=system.tracking[system.orbitals.indexOf(orbital)];
   $('#lab-scan-readout').textContent=`E(RHF) = ${system.totalEnergyHartree.toFixed(8)} Eh; ΔE from 0° = ${((system.totalEnergyHartree-extra.scan[0].totalEnergyHartree)*27.211386).toFixed(3)} eV. Local normalized carbon p-AO overlap = ${system.localPAOOverlap.toFixed(5)}. ${t?`Matched overlap ${t.alignedOverlap.toFixed(5)} (next candidate ${t.nextBestOverlap.toFixed(5)}); MO ${t.previousIndex} → ${t.currentIndex}, sign aligned.`:'First frame: largest AO coefficient positive.'} No interpolated meshes.`;
  }
  if(view)view.update(system,orbital,reverse,previousSystem!==system.id&&!(previousSystem?.startsWith('torsion-')&&isScan));
  previousSystem=system.id;
 }
 function selectMolecule(slot=0){
  const s=selectedSystem();
  $('#lab-orbital').replaceChildren(...s.orbitals.map(o=>new Option(`${o.name} · ${o.character}`,String(o.index))));
  $('#lab-orbital').selectedIndex=Number.isInteger(slot)?slot:0;
  refresh();
 }
 step.addEventListener('input',()=>selectMolecule($('#lab-orbital').selectedIndex));
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
   const radius=new THREE.Box3().setFromObject(group).getBoundingSphere(new THREE.Sphere()).radius;
   const halfAngle=Math.min(THREE.MathUtils.degToRad(camera.fov/2),Math.atan(Math.tan(THREE.MathUtils.degToRad(camera.fov/2))*camera.aspect));
   const distance=Math.min(17,Math.max(5,1.1*radius/Math.sin(halfAngle)));
   controls.target.copy(center);camera.position.copy(center.clone().add(new THREE.Vector3(3.6,2.9,4.7).normalize().multiplyScalar(distance)));
   controls.update();render();
  }
  function clear(){
   while(group.children.length){const o=group.children[0];group.remove(o);o.geometry?.dispose();o.material?.dispose();}
   labels.replaceChildren();atoms=[];
  }
  function update(s,o,reverse,resetCamera=true){
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
   if(resetCamera)reset();else render();
  }
  renderer.domElement.setAttribute('aria-label','Rotatable computed molecular orbital; use molecule and orbital selectors to change the surface');
  canvas.append(renderer.domElement);canvas.hidden=false;fallback.hidden=true;
  view={update,reset};webglAvailable=true;$('#lab-phase').disabled=orbital.kind==='spin-density';
  controls.addEventListener('change',render);
  if(typeof ResizeObserver==='function')new ResizeObserver(resize).observe(canvas);
  else window.addEventListener('resize',resize);
  resize();update(system,orbital,phaseReversed);
  status.textContent='INTERACTIVE 3D · drag or swipe directly on the molecular surface to rotate; wheel or pinch to zoom.';
 }catch(error){
  canvas.hidden=true;fallback.hidden=false;
  view=null;webglAvailable=false;phaseReversed=false;$('#lab-phase').disabled=true;refresh();
  status.textContent=`STATIC IMAGE — rotation unavailable. 3D initialization failed: ${error.message}. Try Chrome Settings → Site settings → JavaScript / hardware acceleration, or another device.`;
 }
})();
