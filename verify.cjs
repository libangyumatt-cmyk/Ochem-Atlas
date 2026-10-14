'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const D=JSON.parse(fs.readFileSync('dist/data.json','utf8')),C=require('./dist/core.js');
const L=require('./dist/learning.js').SorgLearning;
const base={family:'',query:'',axes:['','','',''],steps:'all',candidate:false,saved:false};
const match=(r,f)=>C.matches(r,{...base,...f},D.codebook,[]);
assert.equal(D.reactions.length,31);assert.equal(D.reactions.reduce((n,r)=>n+r.steps.length,0),69);
assert.equal(new Set(D.reactions.map(r=>r.id)).size,D.reactions.length);
assert.equal(D.reactions.filter(r=>r.quantumData).length,D.reactions.length);
assert.equal(D.reactions.filter(r=>r.figure).length,D.reactions.length,'every reaction must display a sourced mechanism image');
assert.equal(D.reactions.find(r=>r.id==='sn2').quantumData.status,'literature-related-numerical');
assert.equal(D.reactions.find(r=>r.id==='diels-alder').quantumData.status,'literature-related-numerical');
assert.equal(D.reactions.filter(r=>r.quantumData.literatureCases.length>0).length,2);
assert.equal(D.version,'0.3.2');
const research=JSON.parse(fs.readFileSync('research/evidence.json','utf8'));
assert.equal(research.schemaVersion,'1.0');
assert.deepEqual(research,JSON.parse(fs.readFileSync('dist/research-data.json','utf8')));
const study=research.studies[0];assert.equal(study.reactionEvent,'sn2:0');
assert.equal(study.model.totalCharge,-1);assert.equal(study.model.multiplicity,1);
assert.equal(study.reactionCoordinate.kind,'published-irc-stationary-subset');assert.equal(study.reactionCoordinate.sampledValuesAvailable,false);
assert.deepEqual(study.points.map(p=>p.id),['R','RC','TS']);
assert.deepEqual(study.points.map(p=>p.energy.value),[0,-9.2,-0.3]);
assert.deepEqual(study.points.map(p=>p.geometry['C-Cl_out'].value),[1.790,1.835,2.351]);
assert.ok(study.points.every(p=>p.coordinatesFile===null));
assert.equal(study.points[2].geometry['Cl_in-C'].status,'derived-from-published');
assert.ok(Math.abs(study.points[2].descriptors.strain.value+study.points[2].descriptors.interaction.value-study.points[2].energy.value)<1e-9);
assert.equal(study.points[0].descriptors['sigma-star-energy'].value,-5.13);
assert.equal(study.points[2].descriptors['orbital-overlap'].value,0.215);
assert.ok(study.descriptors.every(d=>d.method&&d.unit&&d.normalization&&d.applicability));
assert.equal(study.descriptors.find(d=>d.id==='bond-order').status,'unavailable');
assert.ok(study.artifacts.some(a=>a.localPath==='research/workflows/sn2_psi4.py'&&a.availability.includes('not executed')));
const validEvents=new Set(D.reactions.flatMap(r=>r.steps.map((_,i)=>r.id+':'+i)));
assert.equal(validEvents.size,69);
assert.deepEqual(Object.keys(L.cases),['sn2','e2','carbonyl-add','diels-alder']);
for(const [id,c] of Object.entries(L.cases)){
 assert.ok(validEvents.has(c.event));assert.equal(c.event,id+':0');assert.equal(c.questions.length,5);
 for(const [prompt,options] of c.questions){assert.ok(prompt&&options.length>=3);assert.equal(options.filter(o=>o[1]==='yes').length,1);for(const [label,correct,feedback] of options){assert.ok(label&&feedback.length>30);assert.ok(['yes','no'].includes(correct));}}
}
for(const g of Object.values(L.groups)){assert.ok(g.description&&g.keys.length>=2);assert.equal(new Set(g.keys).size,g.keys.length);for(const key of g.keys)assert.ok(validEvents.has(key),key);}
for(const [key,items] of Object.entries(L.descriptors)){assert.ok(validEvents.has(key));assert.ok(items.every(x=>x.length>12));}
for(const [id,study] of Object.entries(L.studies)){assert.ok(L.cases[id]);assert.ok(D.sources[study.source]);assert.ok(study.model&&study.story.length===3);assert.ok(D.reactions.find(r=>r.id===id).sources.includes(study.source));}
assert.ok(D.reactions.every(r=>r.quantumData.proposedProtocol.model&&r.quantumData.proposedProtocol.workflow));
assert.equal(D.reactions.filter(r=>r.quantumData.literatureInsights.length>0).length,7);
assert.ok(D.reactions.find(r=>r.id==='claisen').quantumData.literatureInsights[0].finding.includes('not occur simultaneously'));
for(const r of D.reactions)for(const x of r.quantumData.literatureInsights){assert.ok(D.sources[x.source]?.url.startsWith('https://'));assert.ok(x.model&&x.method&&x.finding&&x.limits);assert.ok(r.sources.includes(x.source));}
const sn2Case=D.reactions.find(r=>r.id==='sn2').quantumData.literatureCases[0];
assert.deepEqual(sn2Case.rows[0],['CH₃Cl','−5.13','+31.6','−31.9','TS']);
assert.equal(sn2Case.rows[3][4],'transition complex');
const daCase=D.reactions.find(r=>r.id==='diels-alder').quantumData.literatureCases[0];
assert.deepEqual(daCase.rows[1],['Acrolein radical cation','+9.5','−40.6','+52.0','−68.8']);
assert.match(daCase.limits,/None is a diabatic electronic-coupling matrix element/);
for(const r of D.reactions)for(const c of r.quantumData.literatureCases){assert.equal(c.columns.length,c.rows[0].length);for(const row of c.rows)assert.equal(row.length,c.columns.length);assert.ok(D.sources[c.source]?.url.startsWith('https://'));assert.match(c.relation,/card|entry/i);}
assert.ok(D.sources.qc_sn2.url.startsWith('https://'));
const context={window:{}};vm.createContext(context);vm.runInContext(fs.readFileSync('dist/data.js','utf8'),context);
assert.equal(JSON.stringify(context.window.SORG),JSON.stringify(D));
vm.runInContext(fs.readFileSync('dist/diagrams.js','utf8'),context);
for(const r of D.reactions){
  for(const s of r.steps){assert.match(s.code,/^[123][1234][1234][123]$/);assert.ok(D.codebook[s.code]);for(let i=0;i<4;i++)assert.ok(D.axes[i].values[s.code[i]]);const svg=context.window.SorgDiagram(s.diagram);assert.ok(svg.includes('<svg'));assert.ok(svg.includes('<text'),'diagram must not be blank: '+s.diagram);assert.ok(s.flow&&s.orbital&&s.geometry);assert.doesNotMatch(s.flow,/illustrated in the embedded mechanism figure|See the embedded mechanism/);}
  for(const id of r.sources)assert.ok(D.sources[id]?.url.startsWith('https://'));
  assert.ok(r.scope&&r.facts.length);assert.equal(typeof r.mechanismComplete,'boolean');assert.ok(r.mechanismNote&&r.audit.researchNeeded);
  if(r.figure){assert.ok(r.figure.src.startsWith('https://')||fs.existsSync('dist/'+r.figure.src));assert.ok(r.figure.href.startsWith('https://')||fs.existsSync('dist/'+r.figure.href));assert.ok(['exact','representative','partial','pending'].includes(r.figure.match));if(r.figure.display){assert.ok(r.figure.reviewed);assert.notEqual(r.figure.rightsStatus,'unconfirmed');}assert.ok(r.figure.alt&&r.figure.credit);}
}
for(const f of ['dist/index.html','dist/app.js','dist/diagrams.js','dist/data.json'])assert.doesNotMatch(fs.readFileSync(f,'utf8'),/[\u3400-\u9fff]/,'all visible content must be English: '+f);
assert.equal(D.reactions.filter(r=>match(r,{})).length,31);
assert.equal(D.reactions.filter(r=>match(r,{query:'SN2'})).some(r=>r.id==='sn2'),true);
assert.ok(D.reactions.filter(r=>match(r,{axes:['2','','','']})).every(r=>r.family==='Radical reactions'));
assert.equal(D.reactions.filter(r=>match(r,{axes:['3','','','']})).length,0);
assert.ok(D.reactions.filter(r=>match(r,{steps:'2'})).every(r=>r.steps.length===2));
assert.ok(D.reactions.filter(r=>match(r,{candidate:true})).every(r=>r.steps.some(s=>C.isCandidate(s,D.codebook))));
assert.equal(D.reactions.filter(r=>match(r,{saved:true})).length,0);
// Cross-step false positives: S2 in one event and O3 in another must not match.
const synthetic={...D.reactions[0],steps:[{code:'2211'},{code:'1333'}]};
assert.equal(match(synthetic,{axes:['2','3','','']}),false);
assert.equal(C.matches(D.reactions[0],{...base,saved:true},D.codebook,[D.reactions[0].id]),true);
const html=fs.readFileSync('dist/index.html','utf8');
for(const asset of ['styles.css','data.js','core.js','diagrams.js','learning.js','research-data.js','research.js','app.js','data.json','research-data.json','sorg-atlas-source.zip'])assert.ok(html.includes(asset+'?v='+D.version),asset+' cache key differs from data version');
assert.ok(html.includes('foundations.js?v='+D.version+'.1'),'foundation visualization fix has a distinct cache key');
assert.ok(html.indexOf('id="foundations"')<html.indexOf('id="principles"'));
for(const id of ['wave','orbitals','density','pes','sorg'])assert.ok(html.includes('id="foundation-'+id+'"'));
assert.match(html,/<section class="research-section section wrap" id="research"/);
assert.match(html,/not interpolated IRC frames/);
assert.ok(html.includes('31 reactions / 69 listed events'));assert.doesNotMatch(html,/concentration-rate|relative-barrier/);
assert.doesNotMatch(fs.readFileSync('dist/app.js','utf8'),/calc-a|orbitalMixing|两轨道耦合与混合模型/);
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(ids.length,new Set(ids).size);
for(const [,asset] of html.matchAll(/(?:src|href)="([^"#:]+\.(?:js|css|svg|json))(?:\?[^"]*)?"/g))assert.ok(fs.existsSync('dist/'+asset),asset);
console.log('PASS: 31 entries / 69 listed events; two numerical cases, seven mapped literature conclusions, 31 proposed computational protocols, pathway review metadata, figure states, diagrams, assets and same-event filters. This is a structural test, not independent scientific verification.');

// Regression checks for errors found in this audit, not a general chemistry validator.
const acidEpoxide=D.reactions.find(r=>r.id==='acid-epoxide');
assert.equal(acidEpoxide.steps.length,2);
assert.match(acidEpoxide.equation,/ClCH₂CH\(OH\)CH₃/);
assert.doesNotMatch(acidEpoxide.steps[1].equation,/OH₂⁺/);
assert.match(acidEpoxide.conditions,/HCl in ether/);
assert.match(D.reactions.find(r=>r.id==='nitration-benzene').steps[2].flow,/N=O π pair shifts/);
assert.equal(D.reactions.find(r=>r.id==='radical-combine').figure.rightsStatus,'original');
assert.match(D.reactions.find(r=>r.id==='sn1-core').quantumData.literatureInsights[0].limits,/generic/);
assert.ok(D.reactions.filter(r=>match(r,{query:'CH3Br'})).some(r=>r.id==='sn2'));
assert.ok(D.reactions.filter(r=>match(r,{query:'SN₂'})).some(r=>r.id==='sn2'));
for(const r of D.reactions)for(const s of r.steps){assert.equal(s.why.length,4);assert.ok(s.assignmentNote&&s.eventKind&&s.assignmentStatus);}
const review=JSON.parse(fs.readFileSync('audit/events.json','utf8'));
assert.equal(review.length,70);assert.equal(review.filter(x=>x.disposition==='removed-invalid-event').length,1);
const baselineBook=JSON.parse(fs.readFileSync('audit/codebook-v0.2.6.json','utf8'));
assert.deepEqual(Object.keys(D.codebook),Object.keys(baselineBook));
for(const c of Object.keys(D.codebook)){
 assert.equal(D.codebook[c].status,baselineBook[c].status);
 if(!['1113','1133','1333'].includes(c))assert.deepEqual(D.codebook[c],baselineBook[c]);
}
assert.match(D.codebook['1113'].boundary,/C=N/);assert.match(D.codebook['1133'].boundary,/O3\/1333/);
assert.deepEqual(D.codebook['1333'].subtypes,['Cycloaddition','Electrocyclic reaction','Sigmatropic rearrangement']);
for(const r of D.reactions)for(const [i,s] of r.steps.entries()){
 const ledger=review.find(x=>x.reaction===r.id&&x.originalStep===i+1&&x.disposition!=='removed-invalid-event');
 assert.equal(s.code,ledger?.currentCode,r.id+' step '+(i+1)+' code changed');
 if(['1113','1133'].includes(s.code))assert.equal(s.assignmentStatus,ledger.assignmentStatus);
}
console.log('PASS: corrected epoxide, nitrate octet, figure provenance, Unicode search, 70-event baseline ledger and documented 1113/1133 clarification.');

// Check the five exact new figures against their equation and stage inventory.
const exact={e2:['CH₂=CHCH₃','EtOH','Br⁻','Hβ–Cβ–Cα–Br'],
 'diels-alder':['butadiene + ethene','cyclohexene','C1=C2','C5=C6','C3=C4'],
 'carbonyl-add':['R₂C=O + Nu⁻','R₂C(O⁻)Nu','Net charge stays −1'],
 'fischer-esterification':['CH₃CO₂H + HOCH₂CH₃','CH₃CO₂CH₂CH₃','Solvent-mediated proton relay','Tetrahedral collapse'],
 'imine-formation':['(CH₃)₂C=O + CH₃NH₂','(CH₃)₂C=NCH₃','Carbinolammonium','N⁺(H)CH₃']};
for(const [id,labels] of Object.entries(exact)){
 const r=D.reactions.find(x=>x.id===id),svg=fs.readFileSync('dist/'+r.figure.src,'utf8');
 assert.equal(r.figure.match,'exact');assert.equal(r.figure.coverage,'complete');assert.equal(r.figure.rightsStatus,'original');
 for(const label of labels)assert.ok(svg.includes(label),id+' missing '+label);
 assert.ok((svg.match(/marker-end="url\(#pair\)"/g)||[]).length>=r.steps.length*2,id+' electron-arrow inventory');
}
assert.ok(!fs.readFileSync('dist/mechanisms/e2.svg','utf8').includes('CH₃</text><text x="279"'),'E2 must not acquire an extra carbon');
assert.match(D.reactions.find(r=>r.id==='imine-formation').steps.at(-1).equation,/C=N⁺\(H\)CH₃/);
assert.ok(D.reactions.every(r=>new Set(r.quantumData.descriptors).size===r.quantumData.descriptors.length));
assert.ok(D.reactions.find(r=>r.id==='carbonyl-add').quantumData.literatureInsights[0].teachingPoint.includes('111°'));
assert.ok(html.includes('id="compare-output"'));assert.ok(html.includes('Same code, different chemistry'));
assert.ok(html.includes('v0.3.2'));assert.ok(html.includes('app.js?v=0.3.2'));
for(const id of ['fischer-esterification','imine-formation']){
 const r=D.reactions.find(x=>x.id===id);
 for(const [i,s] of r.steps.entries()){
  const path='dist/'+s.eventFigure.src,svg=fs.readFileSync(path,'utf8');
  assert.match(svg,new RegExp('stage '+(i+1)));assert.ok((svg.match(/marker-end="url\(#pair\)"/g)||[]).length>=2,id+' stage '+i+' arrow inventory');
 }
}
console.log('PASS: v0.2.8 figure labels, arrow inventories, unique descriptors, comparison markup and iminium notation. Visual and scientific figure review are recorded separately.');
