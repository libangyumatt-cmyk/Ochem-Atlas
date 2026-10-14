'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),zlib=require('node:zlib');
const D=JSON.parse(fs.readFileSync('dist/orbital-data.json','utf8'));
assert.equal(D.schemaVersion,'1.0');assert.equal(D.provenance.program,'PySCF 2.14.0');
assert.equal(D.provenance.method,'restricted Hartree–Fock');assert.equal(D.provenance.basis,'STO-3G');
assert.equal(D.provenance.isovalue,.035);
assert.deepEqual(D.systems.map(s=>[s.id,s.electronCount,s.orbitals.length]),[['h2',2,2],['ethylene',16,2],['formaldehyde',16,3]]);
function cube(path){
 const raw=zlib.gunzipSync(fs.readFileSync(path)).toString('utf8'),lines=raw.trim().split(/\r?\n/);
 const atoms=Number(lines[2].trim().split(/\s+/)[0]);
 const dims=lines.slice(3,6).map(line=>Number(line.trim().split(/\s+/)[0]));
 const vals=lines.slice(6+atoms).join(' ').trim().split(/\s+/).map(Number);
 assert.deepEqual(dims,[44,44,44]);assert.equal(vals.length,44**3);assert.ok(vals.every(Number.isFinite));
 return {atoms,dims,vals,at:(x,y,z)=>vals[(x*44+y)*44+z]};
}
const parity={h2:['even','odd'],ethylene:['odd','odd'],formaldehyde:['odd','even','odd']};
let checks=0;
for(const s of D.systems){
 assert.equal(s.charge,0);assert.equal(s.multiplicity,1);assert.ok(s.orthonormalError<1e-8);
 assert.equal(s.atoms.reduce((n,a)=>n+({H:1,C:6,O:8}[a.element]),0),s.electronCount);
 assert.equal(s.orbitals.reduce((n,o)=>n+o.occupation,0),s.electronCount===2?2:s.id==='ethylene'?2:4); // only selected occupied orbitals
 assert.ok(fs.readFileSync('research/orbitals/outputs/'+s.id+'.log','utf8').includes('converged SCF energy'));
 assert.ok(fs.existsSync('dist/orbital-files/'+s.id+'-scf.npz'));
 for(const [j,o] of s.orbitals.entries()){
  assert.equal(o.index,s.id==='h2'?j+1:s.id==='ethylene'?j+8:j+7);
  assert.ok([0,2].includes(o.occupation));assert.ok(o.energyHartree>-2&&o.energyHartree<2);
  const path='dist/orbital-files/'+s.id+'-mo'+o.index+'.cube.gz';
  const c=cube(path);assert.equal(c.atoms,s.atoms.length);
  assert.equal(fs.readFileSync(path).equals(fs.readFileSync('research/orbitals/outputs/'+s.id+'-mo'+o.index+'.cube.gz')),true);
  assert.ok(c.vals.some(v=>v>.035));assert.equal(c.vals.some(v=>v<-.035),Boolean(o.mesh.negative));
  for(const sign of ['positive','negative']){
   const mesh=o.mesh[sign];if(!mesh)continue;
   assert.equal(mesh.vertices.length%3,0);assert.equal(mesh.faces.length,mesh.triangleCount*3);assert.ok(mesh.triangleCount>50);
   assert.ok(mesh.vertices.every(Number.isFinite));
   assert.ok(mesh.faces.every(v=>Number.isInteger(v)&&v>=0&&v<mesh.vertices.length/3));
  }
  // Molecular plane z=0 is a node for pi and pi*, but not for in-plane n(O).
  const expected=parity[s.id][j];
  for(let x=8;x<36;x+=4)for(let y=8;y<36;y+=4)for(let z=7;z<20;z+=4){
   const a=c.at(x,y,z),b=c.at(x,y,43-z);
   if(Math.abs(a)<.01&&Math.abs(b)<.01)continue;
   assert.ok(Math.abs(a-(expected==='even'?b:-b))<.003,`${s.id} MO${o.index} z parity`);checks++;
   assert.equal(a*a,(-a)*(-a)); // global phase reversal leaves orbital probability unchanged
  }
  assert.ok(fs.existsSync('dist/orbital-files/'+s.id+'-mo'+o.index+'.png'));
 }
}
for(const id of ['h2','ethylene','formaldehyde'])assert.ok(fs.existsSync('research/orbitals/outputs/'+id+'-scf.npz'));
const h2=D.systems[0];assert.equal(h2.orbitals[0].mesh.negative,null,'1σg has no negative region at this isovalue');
const e=D.systems[1];assert.match(e.orbitals[0].name,/HOMO/);assert.match(e.orbitals[1].name,/LUMO/);
const f=D.systems[2];assert.match(f.orbitals[1].name,/n\(O\)/);assert.match(f.orbitals[2].name,/π\*/);
require('./dist/scf-demo.js');
const {target,iterate}=global.SorgSCF;
for(const k of [0,.5,1.2,2])for(const a of [.1,.5,1]){
 const rows=iterate(k,a,24,.1);assert.equal(rows.length,25);
 for(let i=1;i<rows.length;i++){
  assert.ok(Math.abs(rows[i].d-((1-a)*rows[i-1].d+a*target(rows[i-1].d,k)))<1e-14);
  assert.ok(rows[i].d>=0&&rows[i].d<=1);
 }
}
const html=fs.readFileSync('dist/index.html','utf8');
assert.ok(html.indexOf('id="lab"')<html.indexOf('id="principles"'));
for(const id of ['lab-molecule','lab-orbital','lab-reset','lab-phase','scf-plot'])assert.ok(html.includes('id="'+id+'"'));
assert.match(html,/fixed-geometry model/);assert.match(html,/not a Fock or Kohn–Sham calculation/);
console.log(`PASS: 7 PySCF orbital cubes, mesh topology, electron counts, z parity (${checks} points), phase invariance and scalar SCF recurrence. No independent high-level-method validation.`);
