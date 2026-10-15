'use strict';
// Numerical file integrity and actual laboratory DOM behavior with no WebGL.
const assert=require('node:assert/strict'),fs=require('node:fs'),zlib=require('node:zlib');
const {JSDOM}=require('jsdom');
const extra=JSON.parse(fs.readFileSync('dist/orbital-diversity.json','utf8'));
assert.deepEqual(extra.systems.map(s=>[s.id,s.electronCount,s.multiplicity,s.orbitals.length]),[
 ['allyl',23,2,2],['benzene',42,1,6],['butadiene',30,1,4]]);
assert.deepEqual(extra.scan.map(s=>s.torsionDegrees),[0,15,30,45,60]);
let grids=0;
for(const s of [...extra.systems,...extra.scan]){
 assert.equal(s.scfConverged,true);assert.ok(s.orthonormalError<1e-10);
 assert.equal(s.atoms.reduce((n,a)=>n+({H:1,C:6}[a.element]),0),s.electronCount);
 assert.ok(Math.abs(s.electronCounts.reduce((a,b)=>a+b,0)-s.electronCount)<1e-9);
 assert.match(fs.readFileSync(`dist/orbital-files/v034/${s.id}.log`,'utf8'),/converged SCF energy/);
 for(const o of s.orbitals){
  const stem='dist/orbital-files/'+o.fileStem;
  assert.ok(fs.statSync(stem+'.png').size>5000);
  const lines=zlib.gunzipSync(fs.readFileSync(stem+'.cube.gz')).toString().trim().split(/\r?\n/);
  assert.equal(Number(lines[2].trim().split(/\s+/)[0]),s.atoms.length);
  const vals=lines.slice(6+s.atoms.length).join(' ').trim().split(/\s+/).map(Number);
  assert.equal(vals.length,44**3);assert.ok(vals.every(Number.isFinite));grids++;
  for(const sign of ['positive','negative']){
   const m=o.mesh[sign];if(!m)continue;
   assert.ok(m.vertices.every(Number.isFinite));assert.equal(m.vertices.length%3,0);
   assert.equal(m.faces.length,m.triangleCount*3);
   assert.ok(m.faces.every(i=>Number.isInteger(i)&&i>=0&&i<m.vertices.length/3));
  }
 }
}
const allyl=extra.systems[0];assert.equal(allyl.method,'ROHF');assert.equal(allyl.s2,.75);
assert.equal(allyl.orbitals[0].occupation,1);assert.equal(allyl.orbitals[1].kind,'spin-density');
assert.equal(allyl.orbitals[1].mesh.negative,null);
for(const s of extra.scan.slice(1))for(const t of s.tracking){assert.ok(t.alignedOverlap>.95);assert.ok(t.alignedOverlap>t.nextBestOverlap);}
for(let i=1;i<5;i++){
 assert.ok(extra.scan[i].totalEnergyHartree>extra.scan[i-1].totalEnergyHartree);
 assert.ok(extra.scan[i].localPAOOverlap<extra.scan[i-1].localPAOOverlap);
}
async function domTest(missingExtra=false){
 const dom=new JSDOM(fs.readFileSync('dist/index.html','utf8'),{url:'https://example.test/',runScripts:'outside-only'});
 const w=dom.window,d=w.document,$=s=>d.querySelector(s);
 w.HTMLCanvasElement.prototype.getContext=()=>null;
 w.fetch=async url=>({ok:!(missingExtra&&url.startsWith('orbital-diversity')),status:404,
  json:async()=>JSON.parse(fs.readFileSync('dist/'+url.split('?')[0],'utf8'))});
 const change=(id,value,type='change')=>{$(id).value=String(value);$(id).dispatchEvent(new w.Event(type));};
 await w.eval(fs.readFileSync('dist/orbital-lab.js','utf8'));
 assert.match($('#orbital-status').textContent,/STATIC IMAGE/);
 assert.equal($('#lab-molecule').options.length,missingExtra?3:7);
 if(missingExtra){change('#lab-molecule','formaldehyde');assert.equal($('#lab-orbital').options.length,3);dom.window.close();return;}
 for(const s of extra.systems){
  change('#lab-molecule',s.id);
  assert.equal($('#lab-orbital').options.length,s.orbitals.length);
  for(const o of s.orbitals){
   change('#lab-orbital',o.index);
   assert.ok($('#lab-orbital-title').textContent.includes(o.name));
   assert.ok($('#orbital-fallback').src.endsWith(o.fileStem+'.png'));
   assert.equal($('#lab-phase').disabled,true);
  }
 }
 change('#lab-molecule','allyl');change('#lab-orbital',0);
 assert.match($('#lab-phase-note').textContent,/not a wavefunction phase/);
 assert.match($('#lab-positive-label').textContent,/alpha excess/);
 change('#lab-molecule','torsion');change('#lab-orbital',9);
 for(let i=0;i<5;i++){
  change('#lab-torsion',i,'input');assert.equal($('#lab-orbital').selectedIndex,1);
  assert.match($('#lab-orbital-title').textContent,/π\*-derived virtual/);
  assert.equal($('#lab-torsion-value').textContent,extra.scan[i].torsionDegrees+'°');
  assert.equal($('#lab-scan').hidden,false);
 }
 change('#lab-molecule','h2');assert.equal($('#lab-scan').hidden,true);
 $('#lab-reset').click();assert.match($('#orbital-status').textContent,/Static projection/);
 dom.window.close();
}
(async()=>{await domTest();await domTest(true);console.log(`PASS: ${grids} new grids and meshes; molecule/orbital/scan selection, spin labels, downloads, reset, missing-data and WebGL fallback DOM integration. This is not a 3D/mobile browser test.`);})().catch(e=>{console.error(e);process.exitCode=1;});
