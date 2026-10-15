'use strict';
// DOM integration checks. Dialog APIs are modeled, NOT native-browser tested.
const assert=require('node:assert/strict'),fs=require('node:fs');
const {JSDOM,VirtualConsole}=require('jsdom');
const D=JSON.parse(fs.readFileSync('dist/data.json','utf8'));
assert.match(fs.readFileSync('dist/index.html','utf8'),/app\.js\?v=0\.3\.4/);
let assertions=0;
function app({storage='[]',blocked=false,hash=''}={}){
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(String(e)));
 const dom=new JSDOM(fs.readFileSync('dist/index.html','utf8'),{url:'https://example.test/Ochem-Atlas/'+hash,runScripts:'outside-only',virtualConsole:vc});
 const w=dom.window,d=w.document;
 w.HTMLElement.prototype.scrollIntoView=function(){};
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};
 w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'));};
 if(blocked)Object.defineProperty(w,'localStorage',{value:{getItem(){throw Error('blocked')},setItem(){throw Error('blocked')}}});
 else w.localStorage.setItem('sorg-saved-v1',storage);
 for(const f of ['data.js','core.js','diagrams.js','learning.js','research-data.js','foundations.js','scf-demo.js','research.js','app.js'])w.eval(fs.readFileSync('dist/'+f,'utf8'));
 const $=s=>d.querySelector(s), $$=s=>[...d.querySelectorAll(s)];
 const click=s=>{const el=$(s);assert.ok(el,'missing '+s);el.click();};
 const change=(s,value,type='change')=>{const el=$(s);if(el.type==='checkbox')el.checked=value;else el.value=value;el.dispatchEvent(new w.Event(type,{bubbles:true}));};
 const ids=()=>$$('.card-title').map(e=>e.dataset.open);
 return {w,d,$,$$,click,change,ids,errors,close:()=>w.close()};
}
let t=app();assert.equal(t.ids().length,31);
assert.equal(t.$$('.foundation-lesson').length,5);
assert.match(t.$('#scf-readout').textContent,/scalar model is not a molecular calculation/);
t.change('#scf-feedback','0.8','input');t.change('#scf-mix','1','input');assert.match(t.$('#scf-feedback-value').textContent,/0.80 eV/);assert.match(t.$('#scf-mix-value').textContent,/1.00/);
assert.equal(t.$$('.foundation-lesson .equation math').length,6);
assert.equal(t.$$('.foundation-lesson details').length,5);
assert.equal(t.$$('.axis-quantum').length,4);
assert.match(t.$('#coupling-readout').textContent,/level separation/);
t.change('#coupling-gap','0','input');t.change('#coupling-v','0','input');assert.match(t.$('#coupling-readout').textContent,/not uniquely defined/);
t.change('#coupling-v','1','input');assert.match(t.$('#coupling-readout').textContent,/2.00 eV/);assert.match(t.$('#coupling-readout').textContent,/50.0%/);
for(const mode of ['phase','probability','total','difference']){
 t.click(`[data-density="${mode}"]`);
 assert.equal(t.$(`[data-density="${mode}"]`).getAttribute('aria-pressed'),'true');
 const curves=t.$$('#density-plot path');assert.ok(curves.length>0);
 for(const curve of curves){assert.doesNotMatch(curve.getAttribute('d'),/NaN|Infinity/);assert.match(curve.getAttribute('d'),/^M[\d.]+,[\d.-]+/);}
}
assert.match(t.$('#density-caption').textContent,/integral is zero/);
t.click('[data-density="phase"]');assert.match(t.$('#density-caption').textContent,/never.*charge/);
t.change('#pes-x','0','input');assert.match(t.$('#pes-readout').textContent,/first-order saddle/);
t.change('#pes-barrier','1.5','input');assert.match(t.$('#pes-readout').textContent,/Barrier from either minimum: 1.5 eV/);
assert.match(t.$('#research-viewer .research-discrete-plot').textContent,/not.*reaction coordinate/);
assert.equal(t.$$('#research-viewer [data-research-point]').length,3);
assert.match(t.$('#research-viewer').textContent,/1.79 Å/);
t.click('[data-research-point="1"]');assert.match(t.$('.research-focus').textContent,/−?9.2| -9.2/);assert.match(t.$('.research-focus').textContent,/1.835 Å/);
t.click('[data-research-point="2"]');assert.match(t.$('.research-focus').textContent,/2.351 Å/);assert.match(t.$('.research-focus').textContent,/31.6/);assert.match(t.$('.research-focus').textContent,/0.215/);
assert.equal(t.$('[data-research-point="2"]').getAttribute('aria-pressed'),'true');
assert.match(t.$('.research-focus').textContent,/From stated TS symmetry/);
assert.match(t.$('.research-section').textContent,/no Atlas quantum calculation/);
assert.equal(t.$$('#research-descriptors article').length,9);
assert.equal(t.$$('#reason-case option').length,4);assert.equal(t.$$('#map-focus option').length,69);
for(const id of ['sn2','e2','carbonyl-add','diels-alder']){
 t.change('#reason-case',id);assert.match(t.$('#reason-output').textContent,/TEACHING MODEL/);
 for(let i=0;i<5;i++){
  assert.equal(t.$$('.reason-progress .done').length,i);
  const options=t.w.SorgLearning.cases[id].questions[i][1],bad=options.findIndex(o=>o[1]==='no'),good=options.findIndex(o=>o[1]==='yes');
  t.click(`[data-reason-choice="${bad}"]`);assert.match(t.$('.reason-feedback').textContent,/Not for this equation/);assert.equal(t.$('#reason-next'),null);
  t.click(`[data-reason-choice="${good}"]`);assert.match(t.$('.reason-feedback').textContent,/Yes—follow/);t.click('#reason-next');
 }
 assert.match(t.$('#reason-output').textContent,/Mechanistic chain complete/);t.click('#reason-open');assert.equal(t.$('#dialog-title').textContent,t.w.SORG.reactions.find(r=>r.id===id).name);t.click('#close-dialog');assertions+=5;
}
t.change('#map-focus','hbr:0');t.click('#map-next');assert.match(t.$('.map-list').textContent,/Feature only/);
assert.match(t.$('.map-list').textContent,/Proton transfer/);
const totalWithFeature=t.$('.map-neighbors h3').textContent;
t.change('#map-feature-toggle',false);assert.doesNotMatch(t.$('.map-list').textContent,/Feature only/);assert.notEqual(t.$('.map-neighbors h3').textContent,totalWithFeature);
t.change('#map-feature-toggle',true);t.change('#map-focus','sn2:0');assert.match(t.$('#map-output').textContent,/Williamson ether synthesis/);
t.click('#map-next');assert.equal(t.$('#map-prev').disabled,false);
t.change('#map-focus','fischer-esterification:2');t.click('#map-open');assert.equal(t.$('.step-button.active').dataset.step,'2');assert.match(t.w.location.hash,/step=3/);t.click('#close-dialog');
for(const key of [...t.$$('#map-focus option')].map(o=>o.value)){
 t.change('#map-focus',key);assert.ok(t.$('.map-summary strong'));assert.ok(t.$('.map-graphic svg'));assertions++;
}
t.change('#map-focus','hbr:0');t.click('#map-next');const featureButton=t.$('.map-list button');featureButton.click();assert.equal(t.$('#map-focus').value,featureButton.dataset.mapTarget);
for(const id of ['sn2','carbonyl-add','diels-alder']){
 t.click(`[data-open="${id}"]`);t.click('[data-tab="data"]');assert.equal(t.$$('.case-study li').length,3);assert.match(t.$('.case-study').textContent,/Published model|Published-model|PUBLISHED-MODEL/);t.click('#close-dialog');
}
// All selectable codes have events in at least two distinct reaction entries.
for(const option of t.$$('#compare-code option')){
 t.change('#compare-code',option.value);
 const first=t.$('#compare-first').value,second=t.$('#compare-second').value;
 assert.notEqual(first.split(':')[0],second.split(':')[0]);
 assert.equal(t.$$('.compare-event').length,2);
 assert.equal(t.$$('.compare-event .compare-equation').length,2);
 const candidate=D.reactions.filter(r=>r.steps.some(s=>s.code===option.value));
 assert.ok(candidate.length>=2);assertions++;
}
t.change('#compare-code','1122');
t.change('#compare-first','proton-transfer:0');
assert.notEqual(t.$('#compare-first').value.split(':')[0],t.$('#compare-second').value.split(':')[0]);
const alternative=[...t.$('#compare-second').options].find(x=>x.value.startsWith('sn2:'));
assert.ok(alternative);t.change('#compare-second',alternative.value);
assert.match(t.$('#compare-output').textContent,/Cyanide carbon/);
assert.match(t.$('#compare-output').textContent,/hydroxide oxygen/);
t.click('[data-compare-open="sn2"]');assert.equal(t.$('#dialog-title').textContent,'SN2 substitution');t.click('#close-dialog');
t.change('#compare-code','1133');assert.match(t.$('#compare-output').textContent,/remain candidates/);
t.click('[data-compare-open="e2"]');t.click('[data-tab="data"]');assert.match(t.$('#panel-data').textContent,/HOO⁻/);t.click('#close-dialog');
t.click('[data-open="carbonyl-add"]');t.click('[data-tab="data"]');assert.match(t.$('#panel-data').textContent,/≈111°/);assert.match(t.$('#panel-data').textContent,/CN⁻ \+ acetone/);t.click('#close-dialog');
assert.equal(t.$('#panel-data .angle-visual svg').getAttribute('viewBox'),'0 0 190 125');
t.change('#compare-code','1122');t.change('#compare-first','fischer-esterification:2');
assert.equal(t.$('.compare-event img').getAttribute('src'),'mechanisms/fischer-esterification-step-3.svg');
t.click('[data-compare-open="fischer-esterification"]');assert.equal(t.$('.step-button.active').dataset.step,'2');assert.match(t.w.location.hash,/step=3/);
assert.equal(t.$('.event-focus img').getAttribute('src'),'mechanisms/fischer-esterification-step-3.svg');
assert.equal(t.$('.mechanism-svg'),null);assert.match(t.$('.event-focus figcaption').textContent,/overview follows below/);
t.click('#step-next');assert.equal(t.$('.step-button.active').dataset.step,'3');assert.match(t.w.location.hash,/step=4/);t.click('#close-dialog');
t.change('#compare-code','1333');assert.match(t.$('#compare-output').textContent,/Cycloaddition/);assert.equal(t.$('.compare-event img').getAttribute('src'),'mechanisms/diels-alder.svg');
t.click('[data-compare-open="claisen"]');assert.equal(t.$('.step-button.active').dataset.step,'0');t.click('#close-dialog');
t.click('[data-open="sn2"]');t.click('[data-tab="data"]');assert.equal(t.$$('#panel-data .published-chart .chart-group').length,2);t.click('#close-dialog');
t.click('[data-open="diels-alder"]');t.click('[data-tab="data"]');assert.equal(t.$$('#panel-data .published-chart .chart-row').length,4);t.click('#close-dialog');
// Each family and all valid combinations of S/O/R/G use same-event matching.
for(const family of new Set(D.reactions.map(r=>r.family))){t.click(`[data-family="${family}"]`);assert.deepEqual(t.ids(),D.reactions.filter(r=>r.family===family).map(r=>r.id));assertions++;}
t.click('#reset');
for(const code of Object.keys(D.codebook)){
 for(let i=0;i<4;i++)t.change('#axis-'+i,code[i]);
 assert.deepEqual(t.ids(),D.reactions.filter(r=>r.steps.some(s=>s.code===code)).map(r=>r.id));assertions++;
}
t.click('#reset');t.change('#axis-0','2');t.change('#axis-1','3');assert.equal(t.ids().length,0);assert.equal(t.$('#empty').hidden,false);t.click('#empty-reset');
for(const n of new Set(D.reactions.map(r=>r.steps.length))){t.change('#step-filter',String(n));assert.deepEqual(t.ids(),D.reactions.filter(r=>r.steps.length===n).map(r=>r.id));assertions++;}
t.click('#reset');
for(const query of ['SN2','SN₂','CH3Br','1113','iminium']){t.change('#search',query,'input');assert.ok(t.ids().length,query);assertions++;}
t.change('#search','<img src=x onerror=alert(1)>','input');assert.equal(t.ids().length,0);assert.equal(t.$('#active-filters img'),null);t.click('#reset');
t.change('#candidate-filter',true);assert.ok(t.ids().includes('hydride'));assert.ok(t.ids().every(id=>D.reactions.find(r=>r.id===id).steps.some(s=>t.w.SorgCore.isCandidate(s,D.codebook))));t.click('#reset');
// Save/unsave and persisted state use the existing storage key.
t.click('[data-save="sn2"]');assert.equal(t.$('#saved-count').textContent,'1');assert.equal(t.w.localStorage.getItem('sorg-saved-v1'),'["sn2"]');t.click('#show-saved');assert.deepEqual(t.ids(),['sn2']);t.click('[data-open="sn2"]');t.click('#save-reaction');assert.equal(t.ids().length,0);t.click('#close-dialog');t.click('#reset');
// Every modal, every listed event and all tabs execute actual rendering code.
for(const r of D.reactions){
 t.click(`.card-title[data-open="${r.id}"]`);assert.equal(t.$('#reaction-dialog').open,true);assert.equal(t.$('#dialog-title').textContent,r.name);
 assert.equal(t.$$('.full-step').length,r.steps.length);
 assert.equal(t.$$('.source-figure img').length,r.figure.display?1:0);
 for(let i=0;i<r.steps.length;i++){t.click(`[data-step="${i}"]`);assert.equal(t.$('.step-equation').textContent,r.steps[i].equation);assert.equal(t.$$('.why-item').length,4);assertions++;}
 for(const tab of ['data','sources','mechanism']){t.click(`[data-tab="${tab}"]`);assert.equal(t.$('#panel-'+tab).hidden,false);assertions++;}
 const img=t.$('.source-figure img');if(img){img.dispatchEvent(new t.w.Event('error'));assert.equal(img.hidden,true);assert.equal(t.$('.source-figure .image-error').hidden,false);}
 t.click('#close-dialog');assert.equal(t.$('#reaction-dialog').open,false);assert.equal(t.d.body.classList.contains('dialog-open'),false);
}
// Keyboard tab cycling, search shortcut, and direct route.
t.click('[data-open="sn2"]');t.$('[data-tab="mechanism"]').dispatchEvent(new t.w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));assert.equal(t.$('#panel-data').hidden,false);t.click('#close-dialog');t.d.body.focus();t.d.dispatchEvent(new t.w.KeyboardEvent('keydown',{key:'/',bubbles:true}));assert.equal(t.d.activeElement.id,'search');assert.deepEqual(t.errors,[]);t.close();
for(const storage of ['broken JSON','{}','["sn2","sn2","unknown-id"]']){t=app({storage});assert.equal(t.ids().length,31);assert.equal(t.$('#saved-count').textContent,storage.includes('sn2')?'1':'0');assert.deepEqual(t.errors,[]);t.close();}
t=app({blocked:true});t.click('[data-save="sn2"]');t.click('#show-saved');assert.deepEqual(t.ids(),['sn2']);assert.match(t.$('#toast').textContent,/session/);assert.deepEqual(t.errors,[]);t.close();
t=app({hash:'#reaction/acid-epoxide'});assert.equal(t.$('#reaction-dialog').open,true);assert.equal(t.$$('.full-step').length,2);assert.deepEqual(t.errors,[]);t.close();
t=app({hash:'#reaction/imine-formation?step=5'});assert.equal(t.$('.step-button.active').dataset.step,'4');assert.equal(t.$('.event-focus img').getAttribute('src'),'mechanisms/imine-formation-step-5.svg');assert.deepEqual(t.errors,[]);t.close();
console.log(`PASS: DOM integration (${assertions} parameterized cases plus storage, routes, errors and keyboard checks). Native dialog, network image loading, CSS layout, mobile touch and browser console remain UNTESTED.`);
