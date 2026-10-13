(function(){
 'use strict';
 const D=window.SORG,C=window.SorgCore,$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const families=[...new Set(D.reactions.map(r=>r.family))];
 let filters={family:'',query:'',axes:['','','',''],steps:'all',candidate:false,saved:false};
 let saved=[];try{const value=JSON.parse(localStorage.getItem('sorg-saved-v1')||'[]');if(Array.isArray(value))saved=[...new Set(value.filter(id=>D.reactions.some(r=>r.id===id)))];}catch{}
 let selected=null,selectedStep=0,heroId='sn2',toastTimer,storageFailed=false,returnFocus=null,previousHash='';
 const code=(v,cls='')=>`<span class="code ${cls}" aria-label="S${v[0]} O${v[1]} R${v[2]} G${v[3]}">${v.split('').map((n,i)=>`<span class="code-digit" title="${D.axes[i].key}${n} · ${esc(D.axes[i].values[n])}">${n}</span>`).join('')}</span>`;
 const status=c=>D.codebook[c].status==='candidate';
 const candidateStep=s=>C.isCandidate(s,D.codebook);
 const sourceLink=id=>`<a href="${D.sources[id].url}" target="_blank" rel="noopener">${esc(D.sources[id].title)} ↗</a>`;
 function toast(s){$('#toast').textContent=s;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,2500);}
 function save(id){saved=saved.includes(id)?saved.filter(x=>x!==id):[...saved,id];try{localStorage.setItem('sorg-saved-v1',JSON.stringify(saved));storageFailed=false;}catch{storageFailed=true;toast('Storage is unavailable; saved reactions remain available for this session.');}updateSaved();renderCards();if(selected)updateSaveButton();}
 function updateSaved(){$('#saved-count').textContent=saved.length;}
 function updateSaveButton(){const yes=saved.includes(selected.id);$('#save-reaction').textContent=yes?'★ Saved':'☆ Save';$('#save-reaction').setAttribute('aria-pressed',String(yes));}

 $('#axis-grid').innerHTML=D.axes.map((a,i)=>`<article class="axis-card"><span class="axis-letter" style="color:var(--${a.key.toLowerCase()})">${a.key}</span><h3>${a.name}</h3><span class="axis-en">${a.en}</span><p>${a.question}</p><button aria-expanded="false" aria-controls="axis-options-${i}" data-axis-expand="${i}">Show values +</button><div class="axis-options" id="axis-options-${i}" hidden>${Object.entries(a.values).map(([k,v])=>`<div class="axis-option"><b>${a.key}${k}</b><span>${v}</span></div>`).join('')}</div></article>`).join('');
 $$('[data-axis-expand]').forEach(b=>b.addEventListener('click',()=>{const el=$('#axis-options-'+b.dataset.axisExpand),open=el.hidden;el.hidden=!open;b.setAttribute('aria-expanded',String(open));b.textContent=open?'Hide values −':'Show values +';}));
 $('#example-code').innerHTML=code('1122');
 $('#reaction-total').textContent=D.reactions.length;
 $('#event-total').textContent=D.reactions.reduce((n,r)=>n+r.steps.length,0);
 $('#step-filter').innerHTML='<option value="all">Any number of events</option>'+[...new Set(D.reactions.map(r=>r.steps.length))].sort((a,b)=>a-b).map(n=>`<option value="${n}">${n} listed event${n===1?'':'s'}</option>`).join('');
 $('#axis-filters').innerHTML=D.axes.map((a,i)=>`<div class="axis-filter-row"><label for="axis-${i}" style="color:var(--${a.key.toLowerCase()})">${a.key}</label><select id="axis-${i}" aria-label="${a.name}"><option value="">Any ${a.key}</option>${Object.entries(a.values).map(([k,v])=>`<option value="${k}">${k} · ${v}</option>`).join('')}</select></div>`).join('');
 $('#codebook').innerHTML=Object.entries(D.codebook).map(([c,v])=>`<div class="codebook-row"><div>${code(c)}<div class="badge ${status(c)?'candidate':''}">${status(c)?'Candidate assignment':'Inherited project convention'}</div></div><div><strong>${v.label}</strong><p>${v.boundary}</p></div></div>`).join('')+D.axes.map(a=>`<div class="codebook-row"><strong>${a.key} · ${a.name}</strong><p>${a.note}</p></div>`).join('');
 $('#all-sources').innerHTML=Object.keys(D.sources).map(sourceLink).join('');
 function renderFamily(){$('#family-filters').innerHTML=['',...families].map(f=>`<button class="family-button ${filters.family===f?'active':''}" data-family="${f}" aria-pressed="${filters.family===f}">${f||'All reactions'}<span>${f?D.reactions.filter(r=>r.family===f).length:D.reactions.length}</span></button>`).join('');$$('[data-family]').forEach(b=>b.addEventListener('click',()=>{filters.family=b.dataset.family;renderFamily();renderCards();}));}
 function renderCards(){
   const found=D.reactions.filter(r=>C.matches(r,filters,D.codebook,saved));
   $('#result-count').innerHTML=`<strong>${found.length}</strong> / ${D.reactions.length} entries`;
   $('#empty').hidden=found.length!==0;
   $('#reaction-grid').innerHTML=found.map(r=>{const candidate=r.steps.some(candidateStep);return `<article class="reaction-card"><div class="card-meta"><span>${r.family} <span aria-hidden="true">/</span> ${r.steps.length} EVENT${r.steps.length>1?'S':''}</span><button class="save-button ${saved.includes(r.id)?'saved':''}" data-save="${r.id}" aria-label="${saved.includes(r.id)?'Unsave':'Save'} ${esc(r.name)}" aria-pressed="${saved.includes(r.id)}">${saved.includes(r.id)?'★':'☆'}</button></div><h3><button class="card-title" data-open="${r.id}">${esc(r.name)}</button></h3><div class="card-codes">${r.steps.map(s=>code(s.code)).join('<span class="path-arrow">→</span>')}</div><p class="card-desc">${r.summary}</p><div class="card-bottom"><span class="card-status ${candidate?'candidate':''}">${candidate?'◌ Has provisional assignments':'● Inherited teaching code'}</span><button class="card-open" data-open="${r.id}">View mechanism <span>↗</span></button></div></article>`;}).join('');
   $$('[data-open]').forEach(b=>b.addEventListener('click',()=>openReaction(b.dataset.open)));
   $$('[data-save]').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.save;save(id);const replacement=$(`[data-save="${id}"]`);if(replacement)replacement.focus({preventScroll:true});}));
   const chips=[];if(filters.family)chips.push(['family',filters.family]);filters.axes.forEach((v,i)=>{if(v)chips.push(['axis'+i,D.axes[i].key+v]);});if(filters.steps!=='all')chips.push(['steps',filters.steps+' events']);if(filters.candidate)chips.push(['candidate','Has candidate codes']);if(filters.saved)chips.push(['saved','Saved']);if(filters.query)chips.push(['query','Search:'+filters.query]);
   $('#active-filters').innerHTML=chips.map(([k,v])=>`<button class="filter-chip" data-clear="${k}">${esc(v)} ×</button>`).join('');
   $$('[data-clear]').forEach(b=>b.addEventListener('click',()=>{const k=b.dataset.clear;if(k.startsWith('axis'))filters.axes[Number(k.slice(4))]='';else filters[k]=k==='steps'?'all':(k==='saved'||k==='candidate'?false:'');syncFilters();}));
 }
 function syncFilters(){$('#search').value=filters.query;$('#step-filter').value=filters.steps;$('#candidate-filter').checked=filters.candidate;$('#saved-filter').checked=filters.saved;filters.axes.forEach((v,i)=>$('#axis-'+i).value=v);renderFamily();renderCards();}
 function reset(){filters={family:'',query:'',axes:['','','',''],steps:'all',candidate:false,saved:false};syncFilters();}
 $('#search').addEventListener('input',e=>{filters.query=e.target.value;renderCards();});
 D.axes.forEach((a,i)=>$('#axis-'+i).addEventListener('change',e=>{filters.axes[i]=e.target.value;renderCards();}));
 $('#step-filter').addEventListener('change',e=>{filters.steps=e.target.value;renderCards();});
 $('#candidate-filter').addEventListener('change',e=>{filters.candidate=e.target.checked;renderCards();});
 $('#saved-filter').addEventListener('change',e=>{filters.saved=e.target.checked;renderCards();});
 $('#reset').addEventListener('click',reset);$('#empty-reset').addEventListener('click',reset);
 $('#show-saved').addEventListener('click',()=>{reset();filters.saved=true;syncFilters();$('#atlas').scrollIntoView({behavior:'smooth'});});
 document.addEventListener('keydown',e=>{if(e.key==='/'&&!$('#reaction-dialog').open&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();$('#search').focus();$('#atlas').scrollIntoView({behavior:'smooth'});}});

 function renderHero(){const r=D.reactions.find(r=>r.id===heroId);$('#hero-example').innerHTML=`<div class="hero-codes">${r.steps.map(s=>`<div>${code(s.code,'hero-code')}<div class="code-labels"><span>S</span><span>O</span><span>R</span><span>G</span></div></div>`).join('<span class="path-arrow">→</span>')}</div><div class="hero-example-name">${r.name}</div><div class="hero-mechanism">${window.SorgDiagram(r.steps[0].diagram)}</div>`;$$('[data-hero]').forEach(b=>{const a=b.dataset.hero===heroId;b.classList.toggle('active',a);b.setAttribute('aria-pressed',String(a));});}
 $$('[data-hero]').forEach(b=>b.addEventListener('click',()=>{heroId=b.dataset.hero;renderHero();}));
 $('#hero-open').addEventListener('click',()=>openReaction(heroId));

 // Comparisons are between events, because a multistep reaction has several codes.
 const common={
  '1111':'One dominant polar bond-formation or cleavage event; solvent and accompanying bond changes may differ.',
  '1122':'A closed-shell donor–acceptor pair replaces a bond at the reaction center. The center may be H or C.',
  '1113':'A closed-shell attack or collapse changes a carbonyl-related π bond and local tetrahedral geometry. C=N dehydration is a provisional analogy.',
  '1133':'Several bonds redistribute in a polar event. E2, bromonium formation and arene attack do not share one elementary arrow pattern; these assignments remain candidates.',
  '1333':'A closed-shell cyclic orbital interaction changes multiple bonds in one concerted pericyclic event; asynchronous bond development remains possible.',
  '2211':'Open-shell orbitals contribute to a new bond. Radical addition leaves a radical at another carbon; recombination may terminate a pair.'
 };
 const sharedCodes=Object.keys(D.codebook).filter(c=>new Set(D.reactions.filter(r=>r.steps.some(s=>s.code===c)).map(r=>r.id)).size>=2);
 let comparison={code:sharedCodes.includes('1122')?'1122':sharedCodes[0],first:'',second:''};
 const eventsFor=c=>D.reactions.flatMap(r=>r.steps.map((s,i)=>({r,s,i,key:r.id+':'+i})).filter(x=>x.s.code===c));
 function comparisonOptions(){
   const events=eventsFor(comparison.code),find=k=>events.find(x=>x.key===k);
   const first=find(comparison.first)||events.find(x=>x.r.id==='sn2')||events[0];
   const chosenSecond=find(comparison.second);
   const second=chosenSecond&&chosenSecond.r.id!==first.r.id?chosenSecond:events.find(x=>x.r.id!==first.r.id);
   comparison.first=first.key;comparison.second=second.key;
   $('#compare-code').innerHTML=sharedCodes.map(c=>`<option value="${c}">${c} · ${esc(D.codebook[c].label)}</option>`).join('');
   $('#compare-code').value=comparison.code;
   for(const [selector,key,excluded] of [['#compare-first','first',null],['#compare-second','second',comparison.first]]){
     const excludedId=events.find(x=>x.key===excluded)?.r.id;
     $(selector).innerHTML=events.filter(x=>x.r.id!==excludedId).map(x=>`<option value="${esc(x.key)}">${esc(x.r.name)} · ${esc(x.s.title)}</option>`).join('');
     $(selector).value=comparison[key];
   }
 }
 function renderComparison(){
   comparisonOptions();const a=eventsFor(comparison.code).find(x=>x.key===comparison.first),b=eventsFor(comparison.code).find(x=>x.key===comparison.second);
   const event=x=>`<article class="compare-event"><div class="compare-event-head"><strong>${esc(x.r.name)}</strong>${code(x.s.code)}<span class="badge ${candidateStep(x.s)?'candidate':''}">${candidateStep(x.s)?'Provisional':'Inherited'}</span></div><h3>${esc(x.s.title)}</h3><p class="compare-equation">${esc(x.s.equation)}</p><dl><dt>Curved-arrow flow</dt><dd>${esc(x.s.flow)}</dd><dt>Orbital interaction</dt><dd>${esc(x.s.orbital)}</dd><dt>Geometric pathway</dt><dd>${esc(x.s.geometry)}</dd><dt>Classification limit</dt><dd>${esc(x.s.assignmentNote)}</dd></dl><button class="quiet-link" data-compare-open="${esc(x.r.id)}">Inspect complete mechanism ↗</button></article>`;
   $('#compare-output').innerHTML=`<div class="compare-common"><div>${code(comparison.code)}<strong>What this code groups</strong></div><p>${esc(common[comparison.code]||D.codebook[comparison.code].label)}</p><p class="small-note">${esc(D.codebook[comparison.code].boundary)} SORG is a provisional teaching index, not an independently measured quantum quantity.</p></div><div class="compare-pair">${event(a)}${event(b)}</div>`;
   $$('[data-compare-open]').forEach(el=>el.addEventListener('click',()=>openReaction(el.dataset.compareOpen)));
 }
 $('#compare-code').addEventListener('change',e=>{comparison.code=e.target.value;comparison.first='';comparison.second='';renderComparison();});
 $('#compare-first').addEventListener('change',e=>{comparison.first=e.target.value;comparison.second='';renderComparison();});
 $('#compare-second').addEventListener('change',e=>{comparison.second=e.target.value;renderComparison();});
 renderComparison();

 function setTab(t){$$('[data-tab]').forEach(b=>{const active=b.dataset.tab===t;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;$('#panel-'+b.dataset.tab).hidden=!active;});}
 $$('[data-tab]').forEach(b=>{b.addEventListener('click',()=>setTab(b.dataset.tab));b.addEventListener('keydown',e=>{const tabs=$$('[data-tab]');let i=tabs.indexOf(b);if(e.key==='ArrowRight')i=(i+1)%tabs.length;else if(e.key==='ArrowLeft')i=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')i=0;else if(e.key==='End')i=tabs.length-1;else return;e.preventDefault();setTab(tabs[i].dataset.tab);tabs[i].focus();});});
 function openReaction(id,fromHash=false){
   const r=D.reactions.find(r=>r.id===id);if(!r)return;
   if(!$('#reaction-dialog').open){returnFocus=document.activeElement;previousHash=location.hash.startsWith('#reaction/')?'#atlas':location.hash;}
   selected=r;selectedStep=0;
   $('#dialog-breadcrumb').textContent='SORG / '+r.family+' / '+String(D.reactions.indexOf(r)+1).padStart(2,'0');
   $('#dialog-category').textContent='REACTION '+String(D.reactions.indexOf(r)+1).padStart(2,'0')+' / '+r.steps.length+' CODED EVENT'+(r.steps.length>1?'S':'');
   $('#dialog-title').textContent=r.name;$('#dialog-zh').textContent='';$('#dialog-equation').textContent=r.equation;$('#dialog-conditions').textContent=r.conditions;$('#dialog-summary').textContent=r.summary;
   $('#dialog-path').innerHTML=r.steps.map((s,i)=>`<span class="step-tag">${String(i+1).padStart(2,'0')} ${code(s.code)}</span>`).join('<span class="path-arrow">→</span>');
   updateSaveButton();setTab('mechanism');renderMechanism();renderData();renderSources();
   document.body.classList.add('dialog-open');if(!$('#reaction-dialog').open)$('#reaction-dialog').showModal();$('#reaction-dialog').scrollTop=0;
   if(!fromHash)history.replaceState(null,'','#reaction/'+id);
 }
 function closeReaction(){if($('#reaction-dialog').open)$('#reaction-dialog').close();}
 $('#close-dialog').addEventListener('click',closeReaction);
 $('#reaction-dialog').addEventListener('close',()=>{document.body.classList.remove('dialog-open');if(location.hash.startsWith('#reaction/'))history.replaceState(null,'',location.pathname+location.search+(previousHash||'#atlas'));if(returnFocus&&returnFocus.isConnected)returnFocus.focus({preventScroll:true});});
 $('#reaction-dialog').addEventListener('click',e=>{if(e.target===$('#reaction-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeReaction();}});
 $('#save-reaction').addEventListener('click',()=>save(selected.id));
 function renderMechanism(){const r=selected,s=r.steps[selectedStep],book=D.codebook[s.code];
   const fullPath=r.steps.map((st,i)=>`<article class="full-step"><div class="full-step-top"><span>STEP ${String(i+1).padStart(2,'0')} / ${code(st.code)}</span><strong>${esc(st.title)}${st.eventKind==='grouped-stage'?' · grouped stage':''}</strong></div><div class="full-step-equation">${esc(st.equation)}</div><p><b>Curved-arrow / electron flow:</b> ${esc(st.flow)}</p><p class="full-step-orbital"><b>Intermediate and geometry:</b> ${esc(st.geometry)} ${esc(st.orbital)}.</p></article>`).join('<div class="full-path-arrow" aria-hidden="true">↓</div>');
   const f=r.figure;
   const large=f?.src?.includes('fischer-esterification.svg')||f?.src?.includes('imine-formation.svg');
   const imageBody=f?.display?`<div class="figure-viewport" role="region" aria-label="Scrollable mechanism illustration" tabindex="0"><a href="${esc(f.href)}" target="_blank" rel="noopener"><img src="${esc(f.src)}" alt="${esc(f.alt)}" loading="lazy"></a></div><p class="image-error" hidden>Image could not be loaded. The equations and scope notes remain available; use the source link below.</p>`:`<div class="figure-pending">Illustration pending · ${esc(f?.reviewNote||'No reviewed figure is available.')}<br>${f?.rightsStatus==='unconfirmed'?'Reuse permission has not been established.':''}</div>`;
   const figure=f?`<figure class="source-figure ${large?'large-diagram':''}">${imageBody}<figcaption><strong>${esc(f.match)} illustration · ${esc(f.coverage)} coverage</strong><br>${esc(f.reviewNote)}<br>${esc(f.credit)} · ${esc(f.license)} ${f.licenseUrl?`· <a href="${esc(f.licenseUrl)}" target="_blank" rel="noopener">License ↗</a>`:''} · <a href="${esc(f.href)}" target="_blank" rel="noopener">Source ↗</a></figcaption></figure>`:'';
   $('#panel-mechanism').innerHTML=`<section class="complete-path"><div class="complete-path-heading"><div><span class="eyebrow">STATED PATHWAY · ${r.steps.length} LISTED EVENT${r.steps.length===1?'':'S'}</span><h3>Reaction pathway and scope</h3></div><p>${esc(r.mechanismNote||r.scope)}</p></div><div class="full-path-list">${fullPath}</div>${figure}<div class="source-inline mechanism-references"><strong>Mechanism image and sources:</strong>${r.sources.map(sourceLink).join(' · ')}</div></section><div class="mechanism-layout"><div class="step-list" role="group" aria-label="Select a step for code details">${r.steps.map((st,i)=>`<button class="step-button ${i===selectedStep?'active':''}" data-step="${i}" aria-pressed="${i===selectedStep}"><span class="step-number">STEP ${String(i+1).padStart(2,'0')}</span><strong>${st.title}</strong>${code(st.code)}</button>`).join('')}</div><div class="step-reader"><div class="step-heading"><h3>${s.title}</h3><span class="badge ${candidateStep(s)?'candidate':''}">${candidateStep(s)?'◌ Provisional assignment':'● Inherited teaching code'}</span></div><div class="step-equation">${esc(s.equation)}</div><div class="mechanism-svg">${window.SorgDiagram(s.diagram)}<div class="svg-caption">Partial motif only: generic atoms, substituents and charges may differ. Use the stated equation and reference-figure scope for the actual reaction.</div></div><p class="flow-text">${esc(s.flow)}</p><div class="orbital-grid"><div><strong>ORBITAL INTERACTION</strong><p>${esc(s.orbital)}</p></div><div><strong>NUCLEAR GEOMETRY</strong><p>${esc(s.geometry)}</p></div></div><h4 class="why-title">Why is this event coded ${s.code}?</h4><div class="why-grid">${(s.why||book.why).map((w,i)=>`<div class="why-item"><b>${D.axes[i].key}${s.code[i]}</b><span>${w}</span></div>`).join('')}</div><div class="boundary"><strong>Code boundary · </strong>${esc(book.boundary)}<br><strong>Event-specific review · </strong>${esc(s.assignmentNote||'')}</div></div></div><div class="energy-box"><h4>Reaction coordinate: evidence required</h4><p>A listed stage does not establish one transition state or an energy maximum. Solvent relays, association and work-up may contain multiple microscopic events or lack a barrier. No reaction-specific energy profile has been computed for this card.</p></div>`;
   $$('#panel-mechanism img').forEach(img=>img.addEventListener('error',()=>{img.hidden=true;const message=img.closest('figure').querySelector('.image-error');if(message)message.hidden=false;},{once:true}));
   $$('[data-step]').forEach(b=>b.addEventListener('click',()=>{selectedStep=Number(b.dataset.step);renderMechanism();$(`[data-step="${selectedStep}"]`).focus({preventScroll:true});}));
 }
 function renderLiteratureCase(caseData){
   const head=caseData.columns.map(x=>`<th scope="col">${esc(x)}</th>`).join('');
   const rows=caseData.rows.map(row=>`<tr>${row.map((value,i)=>i===0?`<th scope="row">${esc(value)}</th>`:`<td>${esc(value)}</td>`).join('')}</tr>`).join('');
   return `<article class="literature-case"><div class="literature-label">PUBLISHED ELECTRONIC-STRUCTURE RESULTS · ${esc(caseData.location)}</div><h4>${esc(caseData.title)}</h4>${caseData.teachingPoint?`<p class="qc-reading"><strong>Why this case matters:</strong> ${esc(caseData.teachingPoint)}</p>`:''}<p><strong>Calculated model:</strong> ${esc(caseData.model)}</p><p><strong>Relation to this card:</strong> ${esc(caseData.relation)}</p><p><strong>Method, fragments and geometry:</strong> ${esc(caseData.method)}</p><div class="qc-table-scroll" tabindex="0" aria-label="Scrollable quantum-chemistry results"><table class="qc-table"><caption>${esc(caseData.title)} — published values for the stated model</caption><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div><p class="qc-reading"><strong>What the calculation says:</strong> ${esc(caseData.interpretation)}</p><p class="qc-limits"><strong>Meaning and limits:</strong> ${esc(caseData.limits)}</p><p class="qc-limits"><strong>Review:</strong> ${esc(caseData.verification||'Not independently verified.')}</p><p class="qc-source">Primary source: ${sourceLink(caseData.source)} · ${esc(caseData.location)}</p></article>`;
 }
 function renderLiteratureInsight(x){
   return `<article class="literature-insight"><div class="literature-label">${x.publishedQuantity?'PUBLISHED NUMERICAL GEOMETRY & CONCLUSION':'PUBLISHED QUANTUM-CHEMISTRY CONCLUSION'} · ${esc(x.location)}</div>${x.teachingPoint?`<p class="qc-reading"><strong>Why this case matters:</strong> ${esc(x.teachingPoint)}</p>`:''}${x.publishedQuantity?`<p><strong>Published quantity, system and method:</strong> ${esc(x.publishedQuantity)}</p>`:''}<p><strong>Calculated model:</strong> ${esc(x.model)}</p><p><strong>Method:</strong> ${esc(x.method)}</p><p class="qc-reading"><strong>Finding:</strong> ${esc(x.finding)}</p><p class="qc-limits"><strong>Transfer limit:</strong> ${esc(x.limits)}</p><p class="qc-limits"><strong>Review:</strong> ${esc(x.verification||'Not independently verified.')}</p><p class="qc-source">Primary study: ${sourceLink(x.source)}</p></article>`;
 }
 function renderData(){
   const r=selected,q=r.quantumData||{status:'not-yet-computed',descriptors:[],note:'No reaction-specific calculation is available.'};
   const cases=q.literatureCases||[],insights=q.literatureInsights||[],protocol=q.proposedProtocol||{};
   const factPanel=`<div class="fact-grid">${r.facts.map(([a,b])=>`<article class="fact"><strong>${esc(a)}</strong><p>${esc(b)}</p></article>`).join('')}</div>`;
   const evidence=cases.map(renderLiteratureCase).join('')+insights.map(renderLiteratureInsight).join('')||`<div class="qc-empty"><strong>No published quantum-chemistry case is mapped to this entry yet.</strong><p>The proposed calculation below is a protocol, not a completed result.</p></div>`;
   $('#panel-data').innerHTML=`<h3 class="fact-title">Chemistry context</h3>${factPanel}<section class="quantum-model"><div class="calculator-top"><h3>Quantum-chemical evidence</h3><span class="hypothetical">${cases.length||insights.some(x=>x.publishedQuantity)?'Published model data':insights.length?'Published conclusion':'Proposed method only'}</span></div><p class="qc-intro">${esc(q.note)}</p>${evidence}<div class="qc-protocol"><h4>How to calculate this entry · proposed protocol</h4><p><strong>Define the model:</strong> ${esc(protocol.model||'Define the exact substrate, state and conditions.')}</p><p><strong>Compute and verify:</strong> ${esc(protocol.workflow||'Optimize stationary points and validate the reaction path.')}</p><p><strong>Report:</strong> State the electronic-structure method and basis, solvation treatment, conformer coverage, stationary-point frequencies, reaction-path connectivity, and analysis conventions. Test sensitivity to basis and solvent; inspect spin or multireference diagnostics when applicable. An IRC verifies the local path from a transition structure but does not by itself establish solution-phase dynamics.</p></div><h4>Electronic-structure quantities to examine for this entry</h4><ul class="qc-descriptors">${q.descriptors.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><p class="small-note">Published results describe the specific named models above. The protocol is a proposed calculation for this teaching substrate and has not been run here. Orbital energies, overlaps, EDA terms and diabatic couplings are distinct and method dependent. No quantum-chemical calculations or reaction rates have been computed by this Atlas. Published numerical results, published qualitative conclusions and proposed calculations are distinct; there are no project-performed quantum results.</p></section><div class="source-inline">Mechanism and chemistry sources: ${r.sources.map(sourceLink).join(' · ')}</div>`;
 }
 function renderSources(){const r=selected;$('#panel-sources').innerHTML=`<div class="sources-section"><h3>Scope and model limitations</h3><p>${r.scope}</p>${r.note?`<div class="boundary">${r.note}</div>`:''}<h3>Code assignment</h3><p>The four-part code follows this project’s SORG teaching convention. The references below support mechanisms and experimental/theoretical evidence; they do not use or validate SORG. This entry’s ${[...new Set(r.steps.map(s=>s.code))].map(c=>c+(status(c)?' (candidate)':' (inherited)')).join(', ')} are qualitative teaching labels.</p><h3>Open research question</h3><p>${esc(r.audit.researchNeeded)}</p><h3>Further reading</h3><ul class="source-list">${r.sources.map(id=>`<li>${sourceLink(id)}<small>${esc(D.sources[id].publisher)} · ${esc(D.sources[id].reviewStatus)}</small></li>`).join('')}</ul><p class="small-note">Access for free at OpenStax Organic Chemistry. Educational text is shared under CC BY-NC-SA 4.0. Mechanism figures are credited to their sources. Conditions for each numerical value are listed under Data & calculations.</p></div>`;}
 function route(){if(location.hash.startsWith('#reaction/')){let id;try{id=decodeURIComponent(location.hash.slice(10));}catch{return;}if(D.reactions.some(r=>r.id===id))openReaction(id,true);}else if($('#reaction-dialog').open)closeReaction();}
 window.addEventListener('hashchange',route);
 updateSaved();renderFamily();renderCards();renderHero();route();
})();
