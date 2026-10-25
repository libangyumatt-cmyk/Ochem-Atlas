/* Schema-2 laboratory: rendering consumes independently computed system records. */
(async function(){
 'use strict';const $=s=>document.querySelector(s),D=window.SORG;if(!D||!$('#reaction-lab'))return;
 const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const events=D.reactions.flatMap(r=>r.steps.map((s,i)=>({key:r.id+':'+i,r,s,i})));
 let selected=events.find(e=>e.key==='sn2:0'),registry=[],active=null,data=null,mode='both',playing=null,serial=0,loadTurn=0,geometryView=null,fieldView=null,createViewer=null;
 const route=location.hash.match(/^#reaction\/([^?]+)(?:\?step=(\d+))?/);if(route)selected=events.find(e=>e.key===route[1]+':'+(Number(route[2]||1)-1))||selected;
 const datasets=new Map(),loading=new Map(),memories=new Map(),meshes=new Map(),compareViews=new Map();
 let symmetryView=null,symmetryReverse=false,symmetryTurn=0;const symmetryMeshes=new Map();
 $('#rr-event').replaceChildren(...events.map(e=>new Option(`${e.r.name} · ${e.i+1}. ${e.s.title}`,e.key)));$('#rr-event').value=selected.key;
 const state=d=>{if(!memories.has(d.id))memories.set(d.id,{frameId:d.frames[0].id,series:d.series[0].id,kind:'total',level:1,orbitalId:d.orbitalDefinitions[0].id,reverse:false});return memories.get(d.id);};
 const current=()=>state(data);const frame=d=>d.frames.find(f=>f.id===state(d).frameId);const series=d=>d.series.find(s=>s.id===state(d).series);
 const getJSON=async path=>{const r=await fetch(path+'?v=0.3.7-r3');if(!r.ok)throw Error('HTTP '+r.status+' '+path);return r.json();};
 async function getData(r){if(datasets.has(r.id))return datasets.get(r.id);if(!loading.has(r.id))loading.set(r.id,getJSON(r.dataFile).then(d=>{if(d.schemaVersion!=='2.0'||d.id!==r.id||!d.frames.length)throw Error('Unsupported system record');datasets.set(r.id,d);state(d);return d;}).catch(e=>{loading.delete(r.id);throw e;}));return loading.get(r.id);}
 function stop(){if(playing){clearInterval(playing);playing=null;}$('#rr-play').textContent='Step through computed frames';}
 function conventional(){
  const e=selected,ef=e.s.eventFigure,f=e.r.figure,source=ef?.src||(f.display?f.src:null);
  $('#rr-event-title').textContent=`${e.r.name} · event ${e.i+1}`;$('#rr-equation').textContent=e.s.equation;
  $('#rr-conventional').innerHTML=source?`<img src="${esc(source)}" alt="Conventional mechanism for selected ${esc(e.r.name)} event ${e.i+1}"><p>${ef?'Selected event image.':esc(f.match+' '+f.coverage)+' overview; not isolated to this event.'}</p>`:'<p>A reviewed exact structural figure is unavailable. See the inventory for its remaining gap.</p>';
  $('#rr-flow').textContent=e.s.flow;$('#rr-sorg').textContent=`${e.s.code} · ${e.s.orbital}. ${e.s.geometry}. ${e.s.assignmentNote||''}${e.key==='diels-alder:0'?' This retained note describes the published acrolein dataset; the independent new laboratory case uses ethylene.':''}`;$('#rr-sorg-heading').textContent=`${e.s.code} · existing ${e.s.assignmentStatus||'teaching'} assignment`;
  $('#rr-open').href=`#reaction/${e.r.id}?step=${e.i+1}`;
  const available=registry.some(r=>r.event===e.key);$('#rr-calculated').hidden=!available;$('#rr-unavailable').hidden=available;$('#rr-model-mechanism').hidden=!available;
  $('#rr-symmetry').hidden=!available||!data?.symmetry;
  $('#rr-unavailable').textContent='No calculated reaction frames, density grids or quantitative energy profile are available for this selected event. Its written orbital account is conceptual interpretation; no ab initio surface is substituted.';
  $('#rr-conventional-wrap').hidden=mode==='quantum';$('#rr-quantum-wrap').hidden=mode==='conventional';
  if(!available){$('#rr-system').value='';$('#rr-evidence').replaceChildren();++serial;}
 }
 function syncControls(){const s=current(),ser=series(data);$('#rr-system').value=data.id;
  $('#rr-series').replaceChildren(...data.series.map(x=>new Option(x.title,x.id)));$('#rr-series').value=s.series;
  $('#rr-geometry').replaceChildren(...ser.frameIds.map(id=>new Option(data.frames.find(f=>f.id===id).label,id)));$('#rr-geometry').value=s.frameId;
  $('#rr-frame').max=String(ser.frameIds.length-1);$('#rr-frame').value=String(ser.frameIds.indexOf(s.frameId));
  $('#rr-field').replaceChildren(...data.fieldDefinitions.map(x=>new Option(x.label,x.id)),new Option('Selected canonical MO amplitude','amplitude'),new Option('Selected MO probability |φ|²','probability'));
  $('#rr-field').value=s.kind;$('#rr-orbital').replaceChildren(...data.orbitalDefinitions.map(x=>new Option(x.title,x.id)));$('#rr-orbital').value=s.orbitalId;$('#rr-isovalue').value=String(s.level);
 }
 async function selectSystem(id,{selectEvent=true}={}){
  const r=registry.find(x=>x.id===id);if(!r)return;const turn=++loadTurn;++serial;stop();
  if(selectEvent){selected=events.find(e=>e.key===r.event);$('#rr-event').value=selected.key;}
  conventional();$('#rr-system').value=id;$('#rr-status').textContent='Loading documented calculation system…';$('#rr-play').disabled=true;
  try{const next=await getData(r);if(turn!==loadTurn)return;data=next;active=id;syncControls();$('#rr-play').disabled=false;render();}
  catch(e){if(turn===loadTurn){data=null;active=null;$('#rr-status').textContent='Calculated dataset unavailable: '+e.message;}}
 }
 async function onEvent(key){const e=events.find(x=>x.key===key);if(!e)return;selected=e;$('#rr-event').value=key;stop();conventional();const r=registry.find(x=>x.event===key);if(r)return selectSystem(r.id,{selectEvent:false});++loadTurn;data=null;active=null;}
 $('#rr-event').addEventListener('change',()=>onEvent($('#rr-event').value));document.addEventListener('sorg:event-selected',e=>onEvent(e.detail));
 $('#rr-system').addEventListener('change',()=>selectSystem($('#rr-system').value));$('#rr-display').addEventListener('change',()=>{mode=$('#rr-display').value;conventional();});
 $('#rr-series').addEventListener('change',()=>{if(!data)return;stop();current().series=$('#rr-series').value;current().frameId=series(data).frameIds[0];syncControls();render();});
 const chooseFrame=id=>{if(!data)return;stop();current().frameId=id;render();};
 $('#rr-geometry').addEventListener('change',()=>chooseFrame($('#rr-geometry').value));$('#rr-frame').addEventListener('input',()=>data&&chooseFrame(series(data).frameIds[Number($('#rr-frame').value)]));
 $('#rr-field').addEventListener('change',()=>{if(!data)return;current().kind=$('#rr-field').value;current().reverse=false;render();});
 $('#rr-orbital').addEventListener('change',()=>{if(!data)return;current().orbitalId=$('#rr-orbital').value;current().reverse=false;render();});
 $('#rr-isovalue').addEventListener('input',()=>{if(!data)return;current().level=Number($('#rr-isovalue').value);render();});$('#rr-phase').addEventListener('click',()=>{if(!data)return;current().reverse=!current().reverse;render();});
 $('#rr-reset').addEventListener('click',()=>{geometryView?.reset();fieldView?.reset();});$('#rr-play').addEventListener('click',()=>{if(!data)return;if(playing){stop();return;}$('#rr-play').textContent='Pause';playing=setInterval(()=>{const ids=series(data).frameIds,s=current();s.frameId=ids[(ids.indexOf(s.frameId)+1)%ids.length];render();},2200);});document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
 function energy(){const ser=series(data),s=current(),base=data.frames.find(f=>f.id===data.energyReference.frameId).energyHartree;const fs=ser.frameIds.map(id=>data.frames.find(f=>f.id===id)),values=fs.map(f=>(f.energyHartree-base)*27.211386245988),lo=Math.min(...values)-.05,hi=Math.max(...values)+.05;
  $('#rr-energy').innerHTML=`<svg viewBox="0 0 680 235" role="img" aria-label="Separately computed relative electronic energies in eV; categorical geometry spacing, no interpolated curve"><g fill="#203c43" font-size="13"><text x="20" y="18">ΔE / eV · own-system reference</text><path d="M40 30V180H655" fill="none" stroke="#b8c3b6"/>${fs.map((f,i)=>{const x=65+i*560/Math.max(1,fs.length-1),y=165-(values[i]-lo)/(hi-lo)*125;return `<circle cx="${x}" cy="${y}" r="${f.id===s.frameId?7:5}" fill="${f.id===s.frameId?'#aa6a4e':'#397f79'}"/><text x="${x}" y="${y-12}" text-anchor="middle">${values[i].toFixed(3)}</text><text x="${x}" y="203" text-anchor="middle">${esc(f.plotLabel||f.id)}</text>`;}).join('')}<text x="20" y="230">Discrete geometry categories; horizontal spacing is not a continuous coordinate.</text></g></svg><p class="small-note">Reference: ${esc(data.energyReference.label)}. ${esc(ser.coordinateLabel)}. Electronic energies include nuclear repulsion; no ZPE/free energy or experimental barrier.</p>`;
 }

 function bondPlots(){
  const fs=series(data).frameIds.map(id=>data.frames.find(f=>f.id===id)),selectedId=current().frameId,colors=['#19776f','#b15834','#556ba5','#a16b19','#8a5299','#527e28'];
  const charts=[['distanceAngstrom','Bond distances / Å'],['mayer','Mayer bond indices / dimensionless']];
  $('#rr-bond-plots').innerHTML=charts.map(([key,title])=>{
   const vals=fs.flatMap(f=>f.bonds.map(b=>b[key])),lo=Math.min(...vals)-.05,hi=Math.max(...vals)+.05;
   return `<svg viewBox="0 0 680 245" role="img" aria-label="${title}; separately calculated categorical geometries, no interpolated values"><text x="20" y="20" fill="#203c43" font-size="14">${title}</text><path d="M42 35V185H650" fill="none" stroke="#b8c3b6"/><text x="2" y="55" font-size="11">${hi.toFixed(2)}</text><text x="2" y="180" font-size="11">${lo.toFixed(2)}</text>${fs.map((f,i)=>{const x=65+i*560/Math.max(1,fs.length-1);return `${f.id===selectedId?`<rect x="${x-12}" y="30" width="24" height="157" fill="#e3e7d9"/>`:''}<text x="${x}" y="210" text-anchor="middle" font-size="12">${esc(f.plotLabel||f.id)}</text>${f.bonds.map((b,j)=>{const y=175-(b[key]-lo)/(hi-lo)*125;return `<circle cx="${x+(j-(f.bonds.length-1)/2)*2}" cy="${y}" r="${f.id===selectedId?5:3}" fill="${colors[j%colors.length]}"><title>${esc(b.label)}: ${b[key].toFixed(4)}</title></circle>`;}).join('')}`;}).join('')}<text x="20" y="238" font-size="12">Discrete categories; selected column shaded. Small x offsets separate overlapping bonds.</text></svg>`;
  }).join('')+`<p class="small-note">${frame(data).bonds.map((b,j)=>`<span style="color:${colors[j%colors.length]}">● ${esc(b.label)}</span>`).join(' · ')}. Exact distances and both available bond-index conventions are listed below. No values between points are calculated or inferred.</p>`;
 }
 function joinSurfaces(a,b){if(!a)return b;if(!b)return a;return {vertices:[...a.vertices,...b.vertices],faces:[...a.faces,...b.faces.map(i=>i+a.vertices.length/3)],triangleCount:a.triangleCount+b.triangleCount};}
 async function symmetry(){
  const turn=++symmetryTurn,d=data;$('#rr-symmetry').hidden=!d?.symmetry;if(!d?.symmetry)return;
  const q=d.symmetry;$('#rr-symmetry-values').textContent=`Frozen TS fragments: butadiene MO ${q.dieneIndex} occupied; ethylene MO ${q.dienophileIndex} virtual. Forming-region midpoint amplitude products: ${q.samePhaseProducts.map(x=>x.toExponential(4)).join(', ')} bohr⁻³. Same sign at both regions: ${q.samePhaseProducts[0]*q.samePhaseProducts[1]>0}. Signed whole-fragment overlap ${q.interfragmentOverlap.toFixed(6)} (dimensionless, nonorthogonal fragment references).`;
  if(!$('#rr-symmetry').open)return;
  try{
   if(!symmetryMeshes.has(q.meshFile))symmetryMeshes.set(q.meshFile,getJSON(q.meshFile).catch(e=>{symmetryMeshes.delete(q.meshFile);throw e;}));
   const m=await symmetryMeshes.get(q.meshFile);if(turn!==symmetryTurn||d!==data)return;
   if(!symmetryView&&createViewer)symmetryView=await createViewer($('#rr-symmetry-stage'));
   if(turn!==symmetryTurn||d!==data)return;
   const level=Number($('#rr-symmetry-level').value),kind=$('#rr-symmetry-field').value,a=m.diene[level],b=m.dienophile[level],surface=kind==='both'?{positive:joinSurfaces(a.positive,b.positive),negative:joinSurfaces(a.negative,b.negative)}:m[kind][level],f=d.frames.find(f=>f.id===q.frameId);
   symmetryView?.update({atoms:f.atoms,connections:f.connections,mesh:surface,reverse:symmetryReverse,singleColor:false});
  }catch(e){$('#rr-symmetry-values').textContent+=' Surface unavailable: '+e.message;}
 }
 $('#rr-symmetry').addEventListener('toggle',symmetry);$('#rr-symmetry-field').addEventListener('change',symmetry);$('#rr-symmetry-level').addEventListener('change',symmetry);$('#rr-symmetry-phase').addEventListener('click',()=>{symmetryReverse=!symmetryReverse;$('#rr-symmetry-phase').setAttribute('aria-pressed',String(symmetryReverse));symmetry();});
 function fieldSpec(d){const s=state(d),o=d.orbitalDefinitions.find(o=>o.id===s.orbitalId),orb=['amplitude','probability'].includes(s.kind),prob=s.kind==='probability',key=orb?o.meshKey:s.kind,threshold=d.levels[key][s.level];return {o,orb,prob,key,threshold};}
 async function mesh(d,f){const key=d.id+':'+f.id;if(!meshes.has(key))meshes.set(key,getJSON(f.meshFile).catch(e=>{meshes.delete(key);throw e;}));return meshes.get(key);}
 const input=(d,f,m)=>{const s=state(d),sp=fieldSpec(d);return {atoms:f.atoms,connections:f.connections,mesh:m[sp.key][s.level],reverse:s.kind==='amplitude'&&s.reverse,singleColor:s.kind==='total'||sp.prob};};
 async function render(){if(!data||data.event!==selected.key)return;const turn=++serial,d=data,s=current(),f=frame(d),sp=fieldSpec(d),ser=series(d);
  $('#rr-frame').value=String(ser.frameIds.indexOf(f.id));$('#rr-geometry').value=f.id;$('#rr-frame-value').textContent=`${ser.frameIds.indexOf(f.id)+1} / ${ser.frameIds.length} · ${f.label}`;
  $('#rr-method').textContent=`CALCULATED · ${d.method} / ${d.basis} · ${d.title}`;$('#rr-model-equation').textContent=d.modelEquation;$('#rr-path-note').textContent=d.pathKind;$('#rr-model-warning').hidden=!d.warnings?.length;$('#rr-model-warning').textContent=(d.warnings||[]).join(' ');
  $('#rr-model-image').src=d.modelMechanism;$('#rr-model-scope').textContent=d.modelScope;
  $('#rr-orbital-label').hidden=!sp.orb;$('#rr-orbital-note').textContent=sp.orb?sp.o.description:'';
  $('#rr-isovalue-value').textContent=`${sp.prob?(sp.threshold**2).toPrecision(3):sp.threshold} ${s.kind==='amplitude'?'bohr⁻³ᐟ²':sp.prob?'bohr⁻³':'e bohr⁻³'}`;
  $('#rr-phase').disabled=s.kind!=='amplitude';$('#rr-phase').setAttribute('aria-pressed',String(s.kind==='amplitude'&&s.reverse));
  const legends={total:`TOTAL ELECTRON DENSITY · all occupied contributions, ${d.electronCount} electrons; nonnegative, one color.`,difference:'GEOMETRY DIFFERENCE · '+d.references.difference+' Includes nuclear motion.',deformation:'DEFORMATION DENSITY · same-geometry reference · '+d.references.deformation,amplitude:'CANONICAL ORBITAL AMPLITUDE · teal + / amber −; arbitrary global phase, not electron density or a localized fragment orbital.',probability:'ORBITAL PROBABILITY · |φ|² for one selected normalized spatial orbital, no occupation factor; not total electron density.'};
  if(s.kind==='difference'&&f.id===d.energyReference.frameId)legends.difference+=' This reference geometry has zero difference by definition; no signed surface is expected.';
  const unstableFragments=(f.fragments||[]).filter(x=>x.externalStable===false||x.internalStable===false);
  if(s.kind==='deformation'&&unstableFragments.length)legends.deformation+=' WARNING: chosen restricted fragment reference has a reported determinant instability ('+unstableFragments.map(x=>x.id).join(', ')+'); it is not a verified fragment ground state.';
  $('#rr-legend').textContent=(legends[s.kind]||d.fieldDefinitions.find(x=>x.id===s.kind)?.label)+ ' Signed colors do not mean positive/negative electrical charges.';
  const orbRows=f.orbitals.map(o=>`${esc(d.orbitalDefinitions.find(x=>x.id===o.id)?.title||o.id)}: MO ${o.index}, f=${o.occupation}, ε=${o.energyHartree.toFixed(5)} Eh${o.nearDegenerate?' · near-degenerate: canonical partner not unique':''}`).join('<br>');
  const rows=[['Geometry',f.geometryKind],['Model / method',`${d.modelEquation}; charge ${d.charge}, multiplicity ${d.multiplicity}, ${d.electronCount} electrons; ${d.method}/${d.basis}; ${d.environment}`],['Energy',`${f.energyHartree.toFixed(9)} Eh`],...f.bonds.map(b=>[b.label,`${b.distanceAngstrom.toFixed(4)} Å · Mayer ${b.mayer.toFixed(4)}${b.lowdinWiberg!==undefined?' · Löwdin Wiberg '+b.lowdinWiberg.toFixed(4):''}`]),...(f.geometryDescriptors||[]).map(x=>[x.label,`${x.unit==='Eh/bohr'?x.value.toExponential(3):x.value.toFixed(4)} ${x.unit}`]),...(f.frequenciesCm?[['Stationary-point validation',`max |gradient| ${f.maxNuclearGradientEhPerBohr.toExponential(3)} Eh/bohr; ${f.frequenciesCm.filter(x=>x>0).length} positive modes, ${f.frequenciesCm.filter(x=>x<0).length} imaginary modes (signed negative), ${Math.min(...f.frequenciesCm).toFixed(1)}–${Math.max(...f.frequenciesCm).toFixed(1)} cm⁻¹`]]:[]),['SCF checks',`Converged: ${f.scfConverged}; orbital gradient norm ${f.scfOrbitalGradientNorm.toExponential(3)}. ${f.internalStable!==undefined?'Internal/external determinant stability: '+f.internalStable+'/'+f.externalStable:'HF stability not established for retained dataset.'}`],['Density normalization',`Tr(PS) ${f.electronCountAOMetric.toFixed(8)}; independent Becke quadrature ${f.quadratureElectronCount.toFixed(6)} electrons. Coarse uniform grid ${f.uniformGridElectronEstimate.toFixed(3)}; under-resolved nuclear cores, no rescaling.`]];
  $('#rr-descriptors').innerHTML=rows.map(([a,b])=>`<dt>${esc(a)}</dt><dd>${esc(b)}</dd>`).join('')+`<dt>Canonical orbitals</dt><dd>${orbRows}</dd><dt>Correspondence</dt><dd>${f.tracking.length?f.tracking.map(t=>`${esc(t.role||'MO')} ${t.previousIndex}→${t.index}, overlap ${t.alignedOverlap.toFixed(4)}, alternative ${t.nextCandidate.toFixed(4)}${t.ambiguous?' · AMBIGUOUS':''}${t.parentFrame?' from '+esc(t.parentFrame):''}`).join('<br>'):'Initial fragment-projection selection; largest AO coefficient made positive.'}</dd><dt>Mayer convention</dt><dd>Σ(PS)μν(PS)νμ over AO blocks on each atom; occupation-weighted closed-shell P. Basis dependent; not a literal bond count. Where reported, Löwdin Wiberg uses Σ|S½PS½|² over atom blocks, not NBO orbitals. Both indices can depend strongly on diffuse functions.</dd>`;
  $('#rr-downloads').innerHTML=[...f.files,...d.sourceFiles].map(x=>`<a href="${esc(x.path)}" download>${esc(x.label)} ↓</a>`).join('');
  const validation=$('#rr-validation');if(validation){validation.hidden=!d.validationR3;if(d.validationR3){const v=d.validationR3;validation.innerHTML=`<h4>Scientific Validation Status</h4><p><strong>${esc(v.overallStatus)}</strong></p><p>Selected original frame: ${f.frequenciesCm?'Verified stationary point':'Verified constrained geometry'} at the stated model.</p><p>${esc(v.summary)}</p><p>Original constrained-study series retained. <a href="${esc(v.report)}">Read r3 numerical results and limitations</a>.</p>`;}else validation.replaceChildren();}
  $('#rr-protocol').innerHTML=`<p>Total density ρ = Σ fᵢ|φᵢ|²; amplitude φ has arbitrary phase; |φ|² for one spatial orbital integrates to 1. Probability is displayed using ±√(isovalue) amplitude contours; no extra electronic calculation is implied.</p><p>Grid: ${d.grid.shape.join(' × ')}; origin ${d.grid.originBohr.join(', ')} bohr; spacing ${d.grid.spacingBohr} bohr; ${esc(d.grid.order)}. Density: electron bohr⁻³; amplitude: bohr⁻³ᐟ²; mesh positions: Å. Float32 grids, full float64 coefficients retained.</p>${d.bondOrderConventions?'<p>Löwdin Wiberg convention: '+esc(d.bondOrderConventions.lowdinWiberg)+'</p>':''}${[...d.protocol,...d.limitations].map(x=>`<p>${esc(x)}</p>`).join('')}`;

  $('#rr-evidence').innerHTML=d.evidence.map(x=>`<p>${esc(x)}</p>`).join('');energy();bondPlots();symmetry();$('#rr-status').textContent='Loading calculated surfaces…';
  try{const m=await mesh(d,f);if(turn!==serial||d!==data)return;geometryView?.update(input(d,f,m));fieldView?.update(input(d,f,m));$('#rr-status').textContent='CALCULATED DISCRETE GEOMETRY · no interpolation of coordinates, energies, orbitals or densities.';}catch(e){if(turn===serial)$('#rr-status').textContent='Calculated surface unavailable: '+e.message+'. Raw files remain available; no schematic cloud is substituted.';}
  if($('#rr-comparison').open)compare();
 }
 async function compare(){
  if(!$('#rr-comparison').open)return;
  for(const r of registry){try{const d=await getData(r),f=frame(d),s=state(d);let card=document.getElementById('rr-card-'+d.id);
    if(!card){card=document.createElement('article');card.id='rr-card-'+d.id;card.innerHTML='<h4></h4><p class="rr-compare-values"></p><div class="rr-compare-stage"></div><p class="rr-compare-quantity small-note"></p>';$('#rr-compare-cards').append(card);if(createViewer)compareViews.set(d.id,await createViewer(card.querySelector('.rr-compare-stage')));}
    card.querySelector('h4').textContent=d.title+' · '+f.label;
    const ref=d.frames.find(x=>x.id===d.energyReference.frameId);card.querySelector('.rr-compare-values').innerHTML=`${esc(d.modelEquation)}<br>${esc(f.geometryKind)}<br>ΔE ${((f.energyHartree-ref.energyHartree)*27.211386245988).toFixed(4)} eV vs own reference<br>${f.bonds.map(b=>`${esc(b.label)} ${b.distanceAngstrom.toFixed(3)} Å · Mayer ${b.mayer.toFixed(3)}`).join('<br>')}${(f.geometryDescriptors||[]).map(x=>`<br>${esc(x.label)} ${x.unit==='Eh/bohr'?x.value.toExponential(3):x.value.toFixed(3)} ${esc(x.unit)}`).join('')}`;
    const sp=fieldSpec(d);card.querySelector('.rr-compare-quantity').textContent=`${s.kind}${sp.orb?' · '+sp.o.title:''}; threshold ${sp.prob?(sp.threshold**2).toPrecision(3):sp.threshold} ${s.kind==='amplitude'?'bohr⁻³ᐟ²':sp.prob?'bohr⁻³':'e bohr⁻³'}. ${s.kind==='total'||sp.prob?'Nonnegative, one color.':'Teal positive / amber negative; not electrical charge.'} Own energy reference: ${d.energyReference.label}. No cross-system energy comparison.`;
    const id=f.id,m=await mesh(d,f);if(state(d).frameId===id)compareViews.get(d.id)?.update(input(d,f,m));
   }catch(e){$('#rr-status').textContent='Comparison data unavailable: '+e.message;}}
 }
 $('#rr-comparison').addEventListener('toggle',compare);conventional();
 try{const index=await getJSON('reaction-lab/index.json');registry=index.systems;$('#rr-system').replaceChildren(...registry.map(x=>new Option(x.title,x.id)));$('#rr-system').disabled=false;conventional();
  try{const module=await import('./surface-viewer.js?v=0.3.7-r3');createViewer=module.createSurfaceViewer;geometryView=await createViewer($('#rr-geometry-stage'),{geometryOnly:true});fieldView=await createViewer($('#rr-field-stage'));}catch(e){$('#rr-status').textContent='Renderer unavailable; raw calculated data remain downloadable.';}
  const r=registry.find(x=>x.event===selected.key);if(r)await selectSystem(r.id,{selectEvent:false});
 }catch(e){$('#rr-status').textContent='System registry unavailable: '+e.message;$('#rr-play').disabled=true;}
 window.SorgReactionLab={selectEvent:onEvent,selectSystem,get state(){const s=data?current():null;return {event:selected.key,system:active,mode,frameId:s?.frameId,frameIndex:data?series(data).frameIds.indexOf(s.frameId):null,kind:s?.kind,level:s?.level,orbitalId:s?.orbitalId};}};
})();
