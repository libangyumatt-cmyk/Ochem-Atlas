'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const preserved=read('audit/V036_PRESERVED_DATA.json');
for(const [p,hash] of Object.entries(preserved.sha256))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),hash,'retained scientific data changed: '+p);
const index=read('dist/reaction-lab/index.json');assert.equal(index.schemaVersion,'2.0');assert.equal(index.systems.length,3);
const c=read('dist/reaction-lab/carbonyl-system.json');assert.equal(c.frames.length,7);assert.equal(c.event,'carbonyl-add:0');
assert.match(c.warnings.join(' '),/not bound/);const detachment=read('dist/reaction-lab/carbonyl/detachment-check.json');assert.ok(detachment.detachmentEnergyHartree<0);assert.equal(detachment.multiplicity,2);assert.equal(detachment.electronCount,1);assert.equal(c.basis,'6-31++G(d,p)');assert.equal(c.electronCount,18);assert.equal(c.multiplicity,1);assert.equal(c.charge,-1);
assert.match(c.pathKind,/Not an IRC/);assert.equal(c.orbitalDefinitions.length,3);assert.equal(c.series.length,2);
const ids=new Set(c.frames.map(f=>f.id));for(const s of c.series)assert.ok(s.frameIds.every(id=>ids.has(id)));
const angles=c.series[1].frameIds.map(id=>c.frames.find(f=>f.id===id));assert.deepEqual(angles.map(f=>Math.round(f.angleDegree)),[90,110,130]);assert.ok(angles.every(f=>f.distanceAngstrom===1.9));
for(const f of c.frames){
 assert.equal(f.atoms.length,5);assert.equal(f.atoms.reduce((n,a)=>n+({C:6,O:8,H:1}[a.element]),0)+1,18);
 assert.ok(f.scfConverged&&f.internalStable&&f.externalStable);assert.ok(f.scfOrbitalGradientNorm<1e-6);assert.ok(f.orthonormalError<1e-9);
 assert.ok(Math.abs(f.quadratureElectronCount-18)<5e-4);assert.ok(Math.abs(f.electronCountAOMetric-18)<1e-8);
 for(const b of f.bonds){assert.ok(Number.isFinite(b.mayer)&&Number.isFinite(b.lowdinWiberg));assert.ok(b.distanceAngstrom>0);}
 assert.ok(f.geometryDescriptors.length>=3);assert.equal(f.orbitals.length,3);
 for(const t of f.tracking){assert.ok(ids.has(t.parentFrame));assert.ok(t.alignedOverlap>=0);assert.equal(t.ambiguous,t.alignedOverlap<.7||t.alignedOverlap<=t.nextCandidate);}
 for(const [key,v] of Object.entries(f.maximumAbsoluteBoundaryField))assert.ok(v<Math.min(...c.levels[key]),'contour crosses volume boundary');
 const mesh=read('dist/'+f.meshFile);for(const k of Object.keys(c.levels)){
  assert.equal(mesh[k].length,3);for(const pair of mesh[k])for(const surface of Object.values(pair))if(surface){assert.ok(surface.vertices.every(Number.isFinite));assert.equal(surface.faces.length,surface.triangleCount*3);assert.ok(surface.faces.every(i=>Number.isInteger(i)&&i>=0&&i<surface.vertices.length/3));}
 }
 for(const file of f.files)assert.ok(fs.statSync('dist/'+file.path).size>0);
}
const product=c.frames.find(f=>f.id==='product');assert.equal(product.stationaryPointVerified,true);assert.ok(product.maxNuclearGradientEhPerBohr<2e-5);assert.equal(product.frequenciesCm.length,9);assert.ok(product.frequenciesCm.every(x=>x>20));
const validation=read('dist/reaction-lab/carbonyl/validation.json');assert.equal(validation.result,'pass');assert.equal(validation.frames.length,7);assert.ok(validation.frames.every(f=>f.passed));
const D=read('dist/data.json');assert.equal(D.reactions.find(r=>r.id==='carbonyl-add').steps[0].code,'1113');assert.equal(D.reactions.length,31);
for(const r of index.systems){const d=read('dist/'+r.dataFile);assert.equal(d.id,r.id);assert.equal(d.event,r.event);assert.ok(D.reactions.some(x=>r.event===x.id+':0'));}
console.log('PASS: schema-2 systems, seven computed carbonyl geometries, matched angle branch, orbitals/meshes, minimum validation, SORG and original scientific data preservation.');
