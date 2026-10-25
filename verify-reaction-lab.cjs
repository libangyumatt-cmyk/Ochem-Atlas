'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),{JSDOM,VirtualConsole}=require('jsdom');
const D=JSON.parse(fs.readFileSync('dist/data.json','utf8'));
const inventory=JSON.parse(fs.readFileSync('dist/mechanism-inventory.json','utf8'));
assert.equal(inventory.reactions.length,31);assert.equal(inventory.reactions.reduce((n,r)=>n+r.events.length,0),69);
assert.equal(inventory.reactions.filter(r=>r.afterStatus==='complete').length,29);
for(const r of inventory.reactions){
 const actual=D.reactions.find(x=>x.id===r.id);assert.equal(actual.steps.length,r.events.length);
 for(const e of r.events){assert.equal(e.equation,actual.steps[e.index-1].equation);assert.equal(e.code,actual.steps[e.index-1].code);}
}
for(const r of D.reactions)for(const s of r.steps){
 const f=s.eventFigure;if(!f?.src.includes('/v035/'))continue;
 const svg=fs.readFileSync('dist/'+f.src,'utf8');assert.match(svg,/<title>/);assert.match(svg,/<desc>/);
 assert.equal((svg.match(/data-electrons=/g)||[]).length,f.arrowCount);
 if(r.family==='Radical reactions')assert.match(svg,/data-electrons="1"/);
 else assert.doesNotMatch(svg,/data-electrons="1"/);
 assert.ok(f.reactantSmiles&&f.productSmiles&&f.reviewLegend&&f.formula);
}
const data=JSON.parse(fs.readFileSync('dist/reaction-lab/sn2.json','utf8'));
assert.equal(data.charge,-1);assert.equal(data.multiplicity,1);assert.equal(data.electronCount,44);
assert.equal(data.method,'RHF');assert.equal(data.basis,'6-31+G(d)');assert.match(data.pathKind,/not an IRC/);
assert.deepEqual(data.frames.map(f=>f.qAngstrom),[-.6,-.3,0,.3,.6]);
assert.equal(data.centerVerifiedTransitionState,true);assert.ok(data.centerMaxGradientEhPerBohr<2e-5);
assert.equal(data.centerFrequencies.filter(f=>f.imaginaryCm>20).length,1);
assert.equal(data.centerFrequencies.filter(f=>f.realCm>20).length,11);
assert.deepEqual(data.grid.shape,[81,49,49]);assert.equal(data.grid.spacingBohr,.25);
assert.match(data.references.difference,/nuclear displacement/);assert.match(data.references.deformation,/no ghost/);
for(const f of data.frames){
 assert.equal(f.atoms.length,6);assert.equal(f.atoms.reduce((n,a)=>n+({C:6,H:1,Cl:17}[a.element]),0)+1,44);
 assert.equal(f.scfConverged,true);assert.ok(f.orthonormalError<1e-9);assert.ok(Math.abs(f.electronCountAOMetric-44)<1e-8);
 assert.ok(Math.abs(f.quadratureElectronCount-44)<5e-4);assert.ok(f.scfOrbitalGradientNorm<1e-6);
 assert.equal(f.fragments.length,2);assert.equal(f.fragments.reduce((n,x)=>n+x.electronCount,0),44);
 for(const x of f.fragments)assert.ok(x.scfConverged&&Math.abs(x.quadratureElectronCount-x.electronCount)<5e-4);
 const mesh=JSON.parse(fs.readFileSync('dist/'+f.meshFile,'utf8'));
 for(const kind of Object.keys(data.levels)){
  assert.equal(mesh[kind].length,3);
  for(const surfaces of mesh[kind])for(const surf of Object.values(surfaces))if(surf){assert.ok(surf.vertices.every(Number.isFinite));assert.equal(surf.faces.length,surf.triangleCount*3);assert.ok(surf.faces.every(i=>Number.isInteger(i)&&i>=0&&i<surf.vertices.length/3));}
 }
 for(const suffix of ['.xyz','.log','-scf.npz','-fields.npz','-tracked.npz'])assert.ok(fs.statSync('dist/reaction-lab/'+f.id+suffix).size>0);
}
assert.ok(Math.abs(data.frames[0].energyHartree-data.frames[4].energyHartree)<1e-8);
assert.ok(Math.abs(data.frames[1].energyHartree-data.frames[3].energyHartree)<1e-8);
assert.ok(data.frames[2].energyHartree>data.frames[0].energyHartree);
async function domTests(){
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
 const dom=new JSDOM(fs.readFileSync('dist/index.html','utf8'),{url:'https://example.test/',runScripts:'outside-only',virtualConsole:vc});const w=dom.window,d=w.document,$=s=>d.querySelector(s);
 w.HTMLElement.prototype.scrollIntoView=function(){};w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'));};
 w.HTMLCanvasElement.prototype.getContext=()=>null;
 w.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync('dist/'+url.split('?')[0],'utf8'))});
 for(const file of ['data.js','core.js','diagrams.js','learning.js','research-data.js','foundations.js','scf-demo.js','research.js','app.js'])w.eval(fs.readFileSync('dist/'+file,'utf8'));
 await w.eval(fs.readFileSync('dist/reaction-lab.js','utf8'));
 const change=(id,v,type='change')=>{$(id).value=String(v);$(id).dispatchEvent(new w.Event(type));};
 assert.equal($('#rr-event').options.length,69);assert.equal(w.SorgReactionLab.state.event,'sn2:0');
 change('#rr-frame',2,'input');assert.match($('#rr-descriptors').textContent,/Hessian-verified/);
 change('#rr-field','amplitude');change('#rr-orbital','occupied');assert.equal($('#rr-phase').disabled,false);$('#rr-phase').click();assert.equal($('#rr-phase').getAttribute('aria-pressed'),'true');
 change('#rr-field','difference');assert.equal($('#rr-phase').disabled,true);assert.match($('#rr-legend').textContent,/nuclear motion/);
 change('#rr-field','probability');assert.match($('#rr-legend').textContent,/not total electron density/);change('#rr-isovalue',2,'input');assert.match($('#rr-isovalue-value').textContent,/0.00360/);
 change('#rr-display','quantum');assert.equal($('#rr-conventional-wrap').hidden,true);assert.equal(w.SorgReactionLab.state.event,'sn2:0');
 change('#rr-event','fischer-esterification:2');assert.equal($('#rr-unavailable').hidden,false);assert.equal($('#rr-calculated').hidden,true);
 change('#rr-display','both');assert.equal(w.SorgReactionLab.state.event,'fischer-esterification:2');assert.ok($('#rr-conventional img').src.includes('fischer-esterification-step-3'));
 $('[data-open="sn2"]').click();await new Promise(setImmediate);assert.equal(w.SorgReactionLab.state.event,'sn2:0');$('#event-quantum-open').click();assert.equal($('#reaction-dialog').open,false);assert.equal(w.location.hash,'#reaction-lab');
 await w.SorgReactionLab.selectEvent('sn2:0');change('#rr-field','deformation');assert.match($('#rr-legend').textContent,/same-geometry/);
 assert.doesNotMatch($('#rr-energy').innerHTML,/NaN|Infinity/);
 // Race: a system whose asynchronous load finishes later must not replace the latest selection.
 const pending=w.SorgReactionLab.selectSystem('hydride-formaldehyde');
 await w.SorgReactionLab.selectSystem('chloride-identity-sn2');await pending;
 assert.equal(w.SorgReactionLab.state.system,'chloride-identity-sn2');
 await w.SorgReactionLab.selectSystem('hydride-formaldehyde');
 assert.equal(w.SorgReactionLab.state.event,'carbonyl-add:0');assert.equal($('#rr-orbital').options.length,3);assert.equal($('#rr-model-warning').hidden,false);assert.match($('#rr-model-warning').textContent,/not bound/);
 change('#rr-field','amplitude');change('#rr-orbital','pistar');
 assert.match($('#rr-orbital-note').textContent,/π\*/);assert.match($('#rr-descriptors').textContent,/18 electrons/);
 change('#rr-series','angles');assert.equal($('#rr-geometry').options.length,3);
 change('#rr-geometry','angle-130');assert.match($('#rr-frame-value').textContent,/130/);
 change('#rr-isovalue',2,'input');change('#rr-display','conventional');
 assert.equal(w.SorgReactionLab.state.event,'carbonyl-add:0');
 await w.SorgReactionLab.selectSystem('chloride-identity-sn2');
 await w.SorgReactionLab.selectSystem('hydride-formaldehyde');
 assert.equal(w.SorgReactionLab.state.frameId,'angle-130');assert.equal(w.SorgReactionLab.state.orbitalId,'pistar');
 assert.equal(w.SorgReactionLab.state.level,2);assert.equal(w.SorgReactionLab.state.mode,'conventional');
 change('#rr-display','both');change('#rr-series','addition');change('#rr-geometry','product');
 assert.match($('#rr-descriptors').textContent,/Hessian-verified methoxide minimum/);
 assert.match($('#rr-descriptors').textContent,/9 positive modes/);

 await w.SorgReactionLab.selectSystem('butadiene-ethylene');
 assert.equal(w.SorgReactionLab.state.event,'diels-alder:0');assert.equal($('#rr-system').options.length,3);
 assert.equal($('#rr-validation').hidden,false);assert.match($('#rr-validation').textContent,/IRC validation incomplete/);assert.match($('#rr-validation').textContent,/Verified constrained geometry/);assert.equal($('#rr-series').options.length,1);
 assert.match($('#rr-bond-plots').textContent,/C1···C5 forming/);assert.match($('#rr-evidence').textContent,/S1/);
 change('#rr-geometry','ts');assert.match($('#rr-descriptors').textContent,/1 imaginary modes/);assert.match($('#rr-validation').textContent,/Verified stationary point/);
 assert.equal($('#rr-symmetry').hidden,false);assert.match($('#rr-symmetry-values').textContent,/Same sign at both regions: true/);
 change('#rr-field','deformation');assert.match($('#rr-legend').textContent,/neutral singlet butadiene/);
 change('#rr-field','amplitude');change('#rr-orbital','virtual');assert.match($('#rr-orbital-note').textContent,/canonical/);
 change('#rr-display','conventional');assert.equal(w.SorgReactionLab.state.frameId,'ts');change('#rr-display','both');
 await w.SorgReactionLab.selectSystem('chloride-identity-sn2');assert.equal($('#rr-symmetry').hidden,true);assert.equal($('#rr-validation').hidden,true);
 await w.SorgReactionLab.selectSystem('butadiene-ethylene');assert.equal(w.SorgReactionLab.state.frameId,'ts');
 assert.equal(w.SorgReactionLab.state.orbitalId,'virtual');
 await w.SorgReactionLab.selectEvent('e2:0');assert.equal($('#rr-unavailable').hidden,false);
 assert.equal($('#rr-calculated').hidden,true);

 assert.ok(errors.every(e=>/dynamic import/i.test(e)),errors.join('\n'));
 dom.window.close();
}
domTests().then(()=>console.log('PASS: 31/69 illustration inventory, authored-arrow structure, five retained SN2 frames, multi-system loading races/state retention, carbonyl frame/orbital/angle controls, density metadata, Hessian records, meshes and synchronized event/quantity/representation DOM integration. Native WebGL/touch are separate checks.')).catch(e=>{console.error(e);process.exitCode=1;});
