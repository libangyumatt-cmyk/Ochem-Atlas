'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const d=read('dist/reaction-lab/diels-alder-system.json');assert.equal(d.schemaVersion,'2.0');assert.equal(d.event,'diels-alder:0');assert.equal(d.electronCount,46);assert.equal(d.charge,0);assert.equal(d.multiplicity,1);assert.match(d.method,/B3LYP/);assert.match(d.pathKind,/Not an IRC/);assert.equal(d.frames.length,5);assert.equal(read('dist/reaction-lab/index.json').systems.length,3);assert.deepEqual(read('dist/reaction-lab/index.json').systems.slice(0,2),read('audit/V037_SYSTEM_REGISTRY_BASELINE.json').systems);
for(const f of d.frames){
 assert.equal(f.atoms.length,16);assert.equal(f.atoms.filter(a=>a.element==='C').length,6);assert.equal(f.bonds.length,6);assert.equal(f.orbitals.length,2);assert.ok(f.scfConverged);assert.ok(Math.abs(f.electronCountAOMetric-46)<1e-8);assert.ok(Math.abs(f.quadratureElectronCount-46)<.001);assert.ok(f.scfOrbitalGradientNorm<3e-6);assert.ok(f.orthonormalError<1e-8);
 for(const b of f.bonds)assert.ok([b.distanceAngstrom,b.mayer,b.lowdinWiberg].every(Number.isFinite));
 if(f.id==='ts'){assert.ok(f.stationaryPointVerified);assert.equal(f.frequenciesCm.filter(x=>x<-20).length,1);assert.ok(f.maxNuclearGradientEhPerBohr<2e-4);assert.ok(f.geometryDescriptors[0].value<.002);}
 if(f.id==='product'){assert.ok(f.stationaryPointVerified);assert.equal(f.frequenciesCm.length,42);assert.ok(f.frequenciesCm.every(x=>x>20));}
 for(const file of f.files)assert.ok(fs.statSync('dist/'+file.path).size>0);
 const m=read('dist/'+f.meshFile);for(const key of Object.keys(d.levels)){assert.equal(m[key].length,3);for(const layer of m[key])for(const surf of Object.values(layer))if(surf){assert.equal(surf.faces.length,surf.triangleCount*3);assert.ok(surf.vertices.every(Number.isFinite));assert.ok(surf.faces.every(i=>Number.isInteger(i)&&i>=0&&i<surf.vertices.length/3));}}
}
const partial=d.frames.find(f=>f.id==='post-ts');assert.equal(partial.constrainedGradientTargetMet,false);assert.match(partial.geometryKind,/partially relaxed/);assert.match(d.warnings.join(' '),/PARTIAL GEOMETRY RELAXATION/);
const validation=read('dist/reaction-lab/diels-alder/validation.json');assert.equal(validation.result,'pass');assert.ok(validation.frames.every(f=>f.passed));assert.ok(d.symmetry.samePhaseProducts.every(x=>x>0));
const D=read('dist/data.json');assert.equal(D.reactions.length,31);assert.equal(D.reactions.reduce((n,r)=>n+r.steps.length,0),69);assert.equal(D.reactions.find(r=>r.id==='diels-alder').steps[0].code,'1333');assert.match(d.evidence[0],/S1/);assert.match(d.evidence[0],/NOT/);
for(const [path,sha] of Object.entries(read('audit/V037_PRESERVED_DATA.json')))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex'),sha,path+' preserved');
for(const file of d.sourceFiles)assert.ok(fs.statSync('dist/'+file.path).size>0);
console.log('PASS: 5 computed Diels–Alder geometries, full Hessian saddle/minimum, six bond descriptors, genuine grids, phase references, schema3 systems and preserved original scientific data.');
