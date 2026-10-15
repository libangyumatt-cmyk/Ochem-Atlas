/* Synchronizes one catalog event with a separately identified calculated model. */
(async function(){
 'use strict';const $=s=>document.querySelector(s),D=window.SORG;
 if(!D||!$('#reaction-lab'))return;
 const events=D.reactions.flatMap(r=>r.steps.map((s,i)=>({key:r.id+':'+i,r,s,i})));
 let selected=events.find(e=>e.key==='sn2:0'),data=null,frameIndex=0,mode='both',kind='total',level=1,reverse=false,playing=null,serial=0;
 const route=location.hash.match(/^#reaction\/([^?]+)(?:\?step=(\d+))?/);if(route)selected=events.find(e=>e.key===route[1]+':'+(Number(route[2]||1)-1))||selected;
 const cache=new Map();let geometryView=null,fieldView=null;
 const sel=$('#rr-event');sel.replaceChildren(...events.map(e=>new Option(`${e.r.name} · ${e.i+1}. ${e.s.title}`,e.key)));sel.value=selected.key;
 function conventional(){
  const e=selected,ef=e.s.eventFigure,f=e.r.figure;const source=ef?.src||(f.display?f.src:null);
  $('#rr-event-title').textContent=`${e.r.name} · event ${e.i+1}`;$('#rr-equation').textContent=e.s.equation;
  $('#rr-conventional').innerHTML=source?`<img src="${source}" alt="Conventional mechanism for selected ${e.r.name} event ${e.i+1}"><p>${ef?'Selected event image.':f.match+' '+f.coverage+' overview; it is not isolated to this event.'}</p>`:'<p>A reviewed exact structural figure is unavailable. The written event and the inventory identify the remaining gap.</p>';
  $('#rr-flow').textContent=e.s.flow;$('#rr-sorg').textContent=`${e.s.code} · ${e.s.orbital}. ${e.s.geometry}. ${e.s.assignmentNote||''}`;
  $('#rr-open').href=`#reaction/${e.r.id}?step=${e.i+1}`;
  const computed=e.key==='sn2:0';$('#rr-calculated').hidden=!computed;$('#rr-unavailable').hidden=computed;
  $('#rr-model-mechanism').hidden=!computed;
  $('#rr-unavailable').textContent='No calculated reaction frames, density grids or quantitative energy profile are available for this selected event. Its written orbital account is conceptual interpretation; it is not an ab initio surface. Conventional illustrations and existing sourced evidence remain available.';
  $('#rr-conventional-wrap').hidden=mode==='quantum';$('#rr-quantum-wrap').hidden=mode==='conventional';
 }
 function stop(){if(playing){clearInterval(playing);playing=null;}$('#rr-play').textContent='Step through computed frames';}
 function onEvent(key){const e=events.find(e=>e.key===key);if(!e)return;selected=e;sel.value=key;stop();conventional();if(key==='sn2:0'&&data)render();}
 sel.addEventListener('change',()=>onEvent(sel.value));
 document.addEventListener('sorg:event-selected',e=>onEvent(e.detail));
 $('#rr-display').addEventListener('change',()=>{mode=$('#rr-display').value;conventional();});
 $('#rr-frame').addEventListener('input',()=>{frameIndex=Number($('#rr-frame').value);stop();render();});
 $('#rr-field').addEventListener('change',()=>{kind=$('#rr-field').value;reverse=false;render();});
 $('#rr-isovalue').addEventListener('input',()=>{level=Number($('#rr-isovalue').value);render();});
 $('#rr-phase').addEventListener('click',()=>{reverse=!reverse;render();});
 $('#rr-reset').addEventListener('click',()=>{geometryView?.reset();fieldView?.reset();});
 $('#rr-play').addEventListener('click',()=>{if(playing){stop();return;}$('#rr-play').textContent='Pause';playing=setInterval(()=>{frameIndex=(frameIndex+1)%data.frames.length;render();},2200);});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
 function energy(f){
  const base=data.frames[0].energyHartree;const values=data.frames.map(x=>(x.energyHartree-base)*27.211386245988);
  const lo=Math.min(...values)-.05,hi=Math.max(...values)+.05,w=640,h=200;
  const points=values.map((v,i)=>{const x=65+i*125,y=165-(v-lo)/(hi-lo)*130;return `<g><circle cx="${x}" cy="${y}" r="${i===frameIndex?7:5}" fill="${i===frameIndex?'#aa6a4e':'#397f79'}"/><text x="${x}" y="190" text-anchor="middle">${data.frames[i].qAngstrom.toFixed(2)}</text><text x="${x}" y="${y-14}" text-anchor="middle">${v.toFixed(3)}</text></g>`;}).join('');
  $('#rr-energy').innerHTML=`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Five separately computed constrained-frame energies in eV relative to first frame; no interpolated energy curve"><g font-size="13" fill="#203c43"><text x="20" y="18">ΔE / eV relative to frame 1</text><path d="M40 30V170H600" fill="none" stroke="#b8c3b6"/>${points}</g></svg>`;
 }
 async function render(){
  if(!data||selected.key!=='sn2:0')return;const turn=++serial,f=data.frames[frameIndex],physical=['occupied','virtual'].includes(kind),prob=kind==='probability';
  $('#rr-frame').value=String(frameIndex);$('#rr-frame-value').textContent=`${frameIndex+1} / ${data.frames.length} · q = ${f.qAngstrom.toFixed(2)} Å`;
  const sourceKind=prob?'occupied':kind;const threshold=data.levels[sourceKind][level];
  $('#rr-isovalue-value').textContent=`${prob?(threshold*threshold).toPrecision(3):threshold} ${physical?'bohr⁻³ᐟ²':(prob?'bohr⁻³':'e bohr⁻³')}${prob?' (one-orbital probability; no electron occupancy factor)':''}`;
  $('#rr-phase').disabled=!physical;$('#rr-phase').setAttribute('aria-pressed',String(physical&&reverse));
  const label={total:'TOTAL ELECTRON DENSITY · ρ ≥ 0; one color; 44-electron complex',difference:'GEOMETRY DIFFERENCE · teal accumulation / amber depletion relative to frame 1 at fixed grid coordinates; includes nuclear motion',deformation:'DEFORMATION DENSITY · teal positive / amber negative relative to same-geometry Cl(in)⁻ + CH₃Cl(out) fragments; own fragment bases, no ghosts',occupied:'OCCUPIED CANONICAL ORBITAL · teal + / amber − amplitude; not a localized chloride donor',virtual:'VIRTUAL CANONICAL ORBITAL · teal + / amber − amplitude; not a localized substrate acceptor',probability:'ORBITAL PROBABILITY · |φ|², one spatial orbital normalized to 1; not total electron density'}[kind];
  $('#rr-legend').textContent=label+'. Difference colors are not positive/negative electrical charges.';
  $('#rr-descriptors').innerHTML=`<dt>Frame</dt><dd>${f.geometryKind}</dd><dt>Model / method</dt><dd>Cl⁻ + CH₃Cl · charge −1 · singlet · 44 electrons · ${data.method}/${data.basis} · isolated gas phase</dd><dt>Energy</dt><dd>${f.energyHartree.toFixed(9)} Eh; ${((f.energyHartree-data.frames[0].energyHartree)*27.211386245988).toFixed(4)} eV relative to frame 1</dd><dt>Distances</dt><dd>C···Cl(in) ${f.rinAngstrom.toFixed(4)} Å · C···Cl(out) ${f.routAngstrom.toFixed(4)} Å</dd><dt>Mayer bond indices</dt><dd>C/Cl(in) ${f.mayerCClIn.toFixed(4)} · C/Cl(out) ${f.mayerCClOut.toFixed(4)}; AO-density convention, basis dependent</dd><dt>Density validation</dt><dd>Tr(PS) ${f.electronCountAOMetric.toFixed(8)}; independent Becke quadrature ${f.quadratureElectronCount.toFixed(6)} electrons. Uniform display-grid integral ${f.uniformGridElectronEstimate.toFixed(3)}; nuclear cores are under-resolved, no rescaling.</dd><dt>Tracked canonical MOs</dt><dd>${f.orbitals.map((o,i)=>`${i?'Virtual':'Occupied'} MO ${o.index}, occupation ${o.occupation}, ε ${o.energyHartree.toFixed(5)} Eh`).join('; ')}. ${f.tracking.length?f.tracking.map(t=>`MO ${t.previousIndex}→${t.index}, aligned overlap ${t.alignedOverlap.toFixed(4)}, next candidate ${t.nextCandidate.toFixed(4)}${t.ambiguous?' · correspondence AMBIGUOUS':''}`).join('; '):'First-frame fragment-projection selection; largest AO coefficient positive.'}</dd>`;
  $('#rr-downloads').innerHTML=`<a href="reaction-lab/${f.id}.xyz" download>Cartesian geometry ↓</a><a href="reaction-lab/${f.id}-scf.npz" download>Full SCF coefficients + density matrix ↓</a><a href="${f.fieldFile}" download>Volumetric fields + grid ↓</a><a href="reaction-lab/${f.id}-tracked.npz" download>Phase-aligned coefficients ↓</a><a href="reaction-lab/${f.id}.log" download>SCF output ↓</a><a href="reaction-lab/sn2.json" download>Metadata + references ↓</a>`;
  energy(f);$('#rr-status').textContent='Loading calculated surfaces…';
  try{
   if(!cache.has(f.id))cache.set(f.id,fetch(f.meshFile+'?v=0.3.5').then(r=>{if(!r.ok)throw Error('surface HTTP '+r.status);return r.json();}).catch(e=>{cache.delete(f.id);throw e;}));
   const meshes=await cache.get(f.id);if(turn!==serial)return;
   const input={atoms:f.atoms,mesh:meshes[sourceKind][level],reverse:physical&&reverse,singleColor:kind==='total'||prob};
   geometryView?.update(input);fieldView?.update(input);
   $('#rr-status').textContent='CALCULATED DISCRETE FRAME · no interpolation of geometry, energy, orbital or density fields.';
  }catch(e){if(turn===serial)$('#rr-status').textContent='Calculated surface unavailable: '+e.message+'. Use the raw-data downloads; no schematic cloud is substituted.';}
 }
 conventional();
 try{
  const response=await fetch('reaction-lab/sn2.json?v=0.3.5');if(!response.ok)throw Error('data HTTP '+response.status);data=await response.json();
  $('#rr-path-note').textContent=data.pathKind+` The symmetric center ${data.centerVerifiedTransitionState?'has a verified first-order saddle at this level':'is not a verified transition state'}; this scan is not an IRC. Endpoint energies are constrained-frame references, not separated-reactant energies or a measured barrier.`;
  $('#rr-frame').max=String(data.frames.length-1);
  try{const {createSurfaceViewer}=await import('./surface-viewer.js?v=0.3.5');geometryView=await createSurfaceViewer($('#rr-geometry-stage'),{geometryOnly:true});fieldView=await createSurfaceViewer($('#rr-field-stage'));}catch(e){$('#rr-status').textContent='Renderer unavailable: '+e.message+'. Raw computed data remain downloadable.';}
  render();
 }catch(e){$('#rr-status').textContent='Calculated dataset unavailable: '+e.message;$('#rr-play').disabled=true;$('#rr-frame').disabled=true;}
 window.SorgReactionLab={selectEvent:onEvent,get state(){return {event:selected.key,frameIndex,mode,kind,level};}};
})();
