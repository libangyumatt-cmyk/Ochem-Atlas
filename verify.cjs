'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const D=JSON.parse(fs.readFileSync('dist/data.json','utf8')),C=require('./dist/core.js');
const base={family:'',query:'',axes:['','','',''],steps:'all',candidate:false,saved:false};
const match=(r,f)=>C.matches(r,{...base,...f},D.codebook,[]);
assert.equal(D.reactions.length,31);assert.equal(D.reactions.reduce((n,r)=>n+r.steps.length,0),70);
assert.equal(new Set(D.reactions.map(r=>r.id)).size,D.reactions.length);
assert.equal(D.reactions.filter(r=>r.quantumData).length,D.reactions.length);
assert.equal(D.reactions.filter(r=>r.figure).length,D.reactions.length,'every reaction must display a sourced mechanism image');
assert.equal(D.reactions.find(r=>r.id==='sn2').quantumData.status,'literature-related-numerical');
assert.equal(D.reactions.find(r=>r.id==='diels-alder').quantumData.status,'literature-related-numerical');
assert.equal(D.reactions.filter(r=>r.quantumData.literatureCases.length>0).length,2);
assert.equal(D.version,'0.2.6');
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
  assert.ok(r.scope&&r.facts.length);assert.ok(r.mechanismComplete&&r.mechanismNote,'complete pathway metadata: '+r.id);
  if(r.figure){assert.ok(r.figure.src.startsWith('https://'));assert.ok(r.figure.href.startsWith('https://'));assert.ok(r.figure.alt&&r.figure.credit);}
}
for(const f of ['dist/index.html','dist/app.js','dist/diagrams.js','dist/data.json'])assert.doesNotMatch(fs.readFileSync(f,'utf8'),/[\u3400-\u9fff]/,'all visible content must be English: '+f);
assert.equal(D.reactions.filter(r=>match(r,{})).length,31);
assert.equal(D.reactions.filter(r=>match(r,{query:'SN2'})).some(r=>r.id==='sn2'),true);
assert.ok(D.reactions.filter(r=>match(r,{axes:['2','','','']})).every(r=>r.family==='Radical reactions'));
assert.equal(D.reactions.filter(r=>match(r,{axes:['3','','','']})).length,0);
assert.ok(D.reactions.filter(r=>match(r,{steps:'2'})).every(r=>r.steps.length===2));
assert.ok(D.reactions.filter(r=>match(r,{candidate:true})).every(r=>r.steps.some(s=>D.codebook[s.code].status==='candidate')));
assert.equal(D.reactions.filter(r=>match(r,{saved:true})).length,0);
// Cross-step false positives: S2 in one event and O3 in another must not match.
const synthetic={...D.reactions[0],steps:[{code:'2211'},{code:'1333'}]};
assert.equal(match(synthetic,{axes:['2','3','','']}),false);
assert.equal(C.matches(D.reactions[0],{...base,saved:true},D.codebook,[D.reactions[0].id]),true);
const html=fs.readFileSync('dist/index.html','utf8');
assert.ok(html.includes('31 reactions / 70 events'));assert.doesNotMatch(html,/concentration-rate|relative-barrier/);
assert.doesNotMatch(fs.readFileSync('dist/app.js','utf8'),/calc-a|orbitalMixing|两轨道耦合与混合模型/);
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(ids.length,new Set(ids).size);
for(const [,asset] of html.matchAll(/(?:src|href)="([^"#:]+\.(?:js|css|svg|json))(?:\?[^"]*)?"/g))assert.ok(fs.existsSync('dist/'+asset),asset);
console.log('PASS: 31 entries / 70 events; two numerical cases, seven mapped literature conclusions, 31 proposed computational protocols, complete pathways, figures, diagrams, assets and same-event filters.');
