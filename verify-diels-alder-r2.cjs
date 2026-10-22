'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const data=read('dist/reaction-lab/diels-alder-system.json');
const original=read('dist/reaction-lab/diels-alder/diels-alder.json');
assert.equal(data.validationR2.validatedIRCSeriesExposed,false);
assert.deepEqual(data.series.map(s=>s.id),['scan']);
assert.equal(data.frames.length,5);
for(let i=0;i<5;i++){
 assert.equal(data.frames[i].energyHartree,original.frames[i].energyHartree);
 assert.deepEqual(data.frames[i].atoms,original.frames[i].atoms);
 assert.deepEqual(data.frames[i].bonds,original.frames[i].bonds);
 assert.equal(data.frames[i].fieldFile,original.frames[i].fieldFile);
}
assert.match(data.pathKind,/Not an IRC/);
assert.match(data.warnings.join(' '),/IRC VALIDATION/);
for(const f of data.sourceFiles)assert.ok(fs.statSync('dist/'+f.path).size>0,f.path);
const hashes=read('audit/V037_R2_PRESERVED_DATA.json');assert.equal(Object.keys(hashes).length,373);
for(const [file,hash] of Object.entries(hashes))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),hash,file);
const report=read('dist/reaction-lab/diels-alder/r2/restart-20261022/path-validation.json');
assert.ok(['incomplete','path-and-minima-pass-pending-connectivity-comparison'].includes(report.result));
for(const branch of Object.values(report.branches)){
 assert.ok(branch.acceptedIRCPoints.length>0);
 for(const p of branch.acceptedIRCPoints){assert.equal(p.coordinatesAngstrom.length,16);assert.ok(Number.isFinite(p.energyHartree));assert.ok(p.formingDistancesAngstrom.every(x=>x>0));}
}
console.log('PASS: r2 actual validation status, no premature IRC selector, unchanged original fields and 373 scientific payload hashes.');
