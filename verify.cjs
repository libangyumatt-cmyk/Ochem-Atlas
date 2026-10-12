'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const D=JSON.parse(fs.readFileSync('dist/data.json','utf8')),C=require('./dist/core.js');
const base={family:'',query:'',axes:['','','',''],steps:'all',candidate:false,saved:false};
const match=(r,f)=>C.matches(r,{...base,...f},D.codebook,[]);
assert.equal(D.reactions.length,31);assert.equal(D.reactions.reduce((n,r)=>n+r.steps.length,0),69);
assert.equal(new Set(D.reactions.map(r=>r.id)).size,D.reactions.length);
const context={window:{}};vm.createContext(context);vm.runInContext(fs.readFileSync('dist/data.js','utf8'),context);
assert.equal(JSON.stringify(context.window.SORG),JSON.stringify(D));
vm.runInContext(fs.readFileSync('dist/diagrams.js','utf8'),context);
for(const r of D.reactions){
  for(const s of r.steps){assert.match(s.code,/^[123][1234][1234][123]$/);assert.ok(D.codebook[s.code]);for(let i=0;i<4;i++)assert.ok(D.axes[i].values[s.code[i]]);const svg=context.window.SorgDiagram(s.diagram);assert.ok(svg.includes('<svg'));assert.ok(svg.includes('<text'),'diagram must not be blank: '+s.diagram);assert.ok(s.flow&&s.orbital&&s.geometry);}
  for(const id of r.sources)assert.ok(D.sources[id]?.url.startsWith('https://'));
  assert.ok(r.scope&&r.facts.length);assert.ok(r.mechanismComplete&&r.mechanismNote,'complete pathway metadata: '+r.id);
  if(r.figure){assert.ok(r.figure.src.startsWith('https://'));assert.ok(r.figure.href.startsWith('https://'));assert.ok(r.figure.alt&&r.figure.credit);}
}
assert.equal(D.reactions.filter(r=>match(r,{})).length,31);
assert.equal(D.reactions.filter(r=>match(r,{query:'SN2'})).some(r=>r.id==='sn2'),true);
assert.ok(D.reactions.filter(r=>match(r,{axes:['2','','','']})).every(r=>r.family==='自由基反应'));
assert.equal(D.reactions.filter(r=>match(r,{axes:['3','','','']})).length,0);
assert.ok(D.reactions.filter(r=>match(r,{steps:'2'})).every(r=>r.steps.length===2));
assert.ok(D.reactions.filter(r=>match(r,{candidate:true})).every(r=>r.steps.some(s=>D.codebook[s.code].status==='candidate')));
assert.equal(D.reactions.filter(r=>match(r,{saved:true})).length,0);
// Cross-step false positives: S2 in one event and O3 in another must not match.
const synthetic={...D.reactions[0],steps:[{code:'2211'},{code:'1333'}]};
assert.equal(match(synthetic,{axes:['2','3','','']}),false);
assert.equal(C.matches(D.reactions[0],{...base,saved:true},D.codebook,[D.reactions[0].id]),true);
assert.ok(Math.abs(C.calculate('acid',4.76,9.31).value-35481.338923)<.001);
assert.equal(C.calculate('rate2',2,2).value,4);assert.equal(C.calculate('rate1',2,10).value,2);
assert.equal(C.calculate('barrier',0,298.15).value,1);
assert.ok(Math.abs(C.calculate('barrier',5,298.15).value-7.515)<=.002);
assert.ok(Math.abs(C.calculate('barrier',5,298.15).value*C.calculate('barrier',-5,298.15).value-1)<1e-12);
for(const [type,a,b] of [['barrier',5,0],['barrier',5,-100],['acid',NaN,2],['rate2',-1,2]])assert.throws(()=>C.calculate(type,a,b));
assert.ok(C.calculate('barrier',200,.001).log10>300); // display handles overflow using log10
const html=fs.readFileSync('dist/index.html','utf8');
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(ids.length,new Set(ids).size);
for(const [,asset] of html.matchAll(/(?:src|href)="([^"#:]+\.(?:js|css|svg|json))"/g))assert.ok(fs.existsSync('dist/'+asset),asset);
console.log('PASS: 31 entries / 69 events; complete pathway metadata, figure attribution, data, diagrams, assets, same-event filters, calculator formulas and invalid inputs. Browser QA not run.');
