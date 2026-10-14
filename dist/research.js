(function(){
 'use strict';
 const study=window.SorgResearch.studies[0],root=document.getElementById('research-viewer');
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const show=q=>`${q.value} ${esc(q.unit)}`;
 let focus=0;
 document.getElementById('research-source').href=study.publication.url;
 function draw(){
  const p=study.points[focus],out=p.geometry['C-Cl_out'],incoming=p.geometry['Cl_in-C'];
  const state=p.kind==='separated-reactants'?'+':'···';
  root.innerHTML=`<div class="research-point-list" role="group" aria-label="Published discrete stationary points">${study.points.map((x,i)=>`<button data-research-point="${i}" aria-pressed="${i===focus}" class="${i===focus?'active':''}"><span>${esc(x.id)} · ${esc(x.label)}</span><strong>${show(x.energy)}</strong><small>C–Cl<sub>out</sub> ${show(x.geometry['C-Cl_out'])}</small></button>`).join('')}</div>
   <article class="research-focus"><div class="research-focus-top"><span class="eyebrow">${esc(p.label.toUpperCase())} · ${esc(p.kind)}</span><span class="research-provenance">PUBLISHED TABLE VALUES${incoming?' · ONE SYMMETRY-DERIVED DISTANCE':''}</span></div>
   <div class="research-axis" role="img" aria-label="Qualitative local Cl-in to carbon to Cl-out axis; only the distances written below are numerical, not the drawing scale"><span>Cl<sub>in</sub></span><span class="research-axis-bond">${state}</span><span class="research-carbon">C(H)<sub>3</sub></span><span class="research-axis-bond">${p.kind==='transition-state'?'···':'—'}</span><span>Cl<sub>out</sub></span></div>
   <p class="small-note">Local atom-label glyph, not Cartesian coordinates, a to-scale structure, orbital surface or animation. The isolated reactants have no fixed Cl<sub>in</sub>–C complex distance.</p>
   <dl class="research-measures"><div><dt>C–Cl<sub>out</sub></dt><dd>${show(out)} <small>${esc(out.sourceLocation)}</small></dd></div><div><dt>Cl<sub>in</sub>–C</dt><dd>${incoming?`${show(incoming)} <small>From stated TS symmetry, not independently tabulated</small>`:'Unavailable <small>Not reported for this state in Table 1</small>'}</dd></div><div><dt>ΔE vs separated reactants</dt><dd>${show(p.energy)} <small>${esc(p.energy.sourceLocation)}</small></dd></div></dl>
   <div class="research-measures extra">${Object.entries(p.descriptors).map(([key,q])=>`<p><strong>${esc(study.descriptors.find(d=>d.id===key)?.definition||key)}</strong><br>${show(q)} · ${esc(q.sourceLocation)}<small>${esc(q.convention)}</small></p>`).join('')||'<p>Additional electronic descriptors: unavailable at this tabulated point.</p>'}</div>
   <p class="research-missing"><strong>Not available in this record:</strong> ${p.missing.map(esc).join('; ')}.</p></article>`;
  root.querySelectorAll('[data-research-point]').forEach(b=>b.addEventListener('click',()=>{focus=Number(b.dataset.researchPoint);draw();root.querySelector(`[data-research-point="${focus}"]`).focus({preventScroll:true});}));
 }
 draw();
 document.getElementById('research-descriptors').innerHTML=study.descriptors.map(d=>`<article><h4>${esc(d.category)} · ${esc(d.id)}</h4><p>${esc(d.definition)}</p><dl><dt>Method</dt><dd>${esc(d.method)}</dd><dt>Unit / normalization</dt><dd>${esc(d.unit)} · ${esc(d.normalization)}</dd><dt>Applicability</dt><dd>${esc(d.applicability)} <em>${esc(d.status)}</em></dd></dl></article>`).join('');
})();
