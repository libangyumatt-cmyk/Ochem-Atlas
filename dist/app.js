(function(){
 'use strict';
 const D=window.SORG,C=window.SorgCore,$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const families=[...new Set(D.reactions.map(r=>r.family))];
 let filters={family:'',query:'',axes:['','','',''],steps:'all',candidate:false,saved:false};
 let saved=[];try{const value=JSON.parse(localStorage.getItem('sorg-saved-v1')||'[]');if(Array.isArray(value))saved=value.filter(id=>D.reactions.some(r=>r.id===id));}catch{}
 let selected=null,selectedStep=0,heroId='sn2',toastTimer,storageFailed=false,returnFocus=null,previousHash='';
 const code=(v,cls='')=>`<span class="code ${cls}" aria-label="S${v[0]} O${v[1]} R${v[2]} G${v[3]}">${v.split('').map((n,i)=>`<span class="code-digit" title="${D.axes[i].key}${n} · ${esc(D.axes[i].values[n])}">${n}</span>`).join('')}</span>`;
 const status=c=>D.codebook[c].status==='candidate';
 const sourceLink=id=>`<a href="${D.sources[id].url}" target="_blank" rel="noopener">${esc(D.sources[id].title)} ↗</a>`;
 function toast(s){$('#toast').textContent=s;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,2500);}
 function save(id){saved=saved.includes(id)?saved.filter(x=>x!==id):[...saved,id];try{localStorage.setItem('sorg-saved-v1',JSON.stringify(saved));storageFailed=false;}catch{storageFailed=true;toast('浏览器未允许保存；本次会话仍可使用收藏。');}updateSaved();renderCards();if(selected)updateSaveButton();}
 function updateSaved(){$('#saved-count').textContent=saved.length;}
 function updateSaveButton(){const yes=saved.includes(selected.id);$('#save-reaction').textContent=yes?'★ 已收藏':'☆ 收藏';$('#save-reaction').setAttribute('aria-pressed',String(yes));}

 $('#axis-grid').innerHTML=D.axes.map((a,i)=>`<article class="axis-card"><span class="axis-letter" style="color:var(--${a.key.toLowerCase()})">${a.key}</span><h3>${a.name}</h3><span class="axis-en">${a.en}</span><p>${a.question}</p><button aria-expanded="false" aria-controls="axis-options-${i}" data-axis-expand="${i}">查看取值 ＋</button><div class="axis-options" id="axis-options-${i}" hidden>${Object.entries(a.values).map(([k,v])=>`<div class="axis-option"><b>${a.key}${k}</b><span>${v}</span></div>`).join('')}</div></article>`).join('');
 $$('[data-axis-expand]').forEach(b=>b.addEventListener('click',()=>{const el=$('#axis-options-'+b.dataset.axisExpand),open=el.hidden;el.hidden=!open;b.setAttribute('aria-expanded',String(open));b.textContent=open?'收起取值 −':'查看取值 ＋';}));
 $('#example-code').innerHTML=code('1122');
 $('#reaction-total').textContent=D.reactions.length;
 $('#event-total').textContent=D.reactions.reduce((n,r)=>n+r.steps.length,0);
 $('#axis-filters').innerHTML=D.axes.map((a,i)=>`<div class="axis-filter-row"><label for="axis-${i}" style="color:var(--${a.key.toLowerCase()})">${a.key}</label><select id="axis-${i}" aria-label="${a.name}"><option value="">不限 ${a.key}</option>${Object.entries(a.values).map(([k,v])=>`<option value="${k}">${k} · ${v}</option>`).join('')}</select></div>`).join('');
 $('#codebook').innerHTML=Object.entries(D.codebook).map(([c,v])=>`<div class="codebook-row"><div>${code(c)}<div class="badge ${status(c)?'candidate':''}">${status(c)?'候选分配':'沿用项目约定'}</div></div><div><strong>${v.label}</strong><p>${v.boundary}</p></div></div>`).join('')+D.axes.map(a=>`<div class="codebook-row"><strong>${a.key} · ${a.name}</strong><p>${a.note}</p></div>`).join('');
 $('#all-sources').innerHTML=Object.keys(D.sources).map(sourceLink).join('');
 function renderFamily(){$('#family-filters').innerHTML=['',...families].map(f=>`<button class="family-button ${filters.family===f?'active':''}" data-family="${f}" aria-pressed="${filters.family===f}">${f||'全部反应'}<span>${f?D.reactions.filter(r=>r.family===f).length:D.reactions.length}</span></button>`).join('');$$('[data-family]').forEach(b=>b.addEventListener('click',()=>{filters.family=b.dataset.family;renderFamily();renderCards();}));}
 function renderCards(){
   const found=D.reactions.filter(r=>C.matches(r,filters,D.codebook,saved));
   $('#result-count').innerHTML=`<strong>${found.length}</strong> / ${D.reactions.length} 个条目`;
   $('#empty').hidden=found.length!==0;
   $('#reaction-grid').innerHTML=found.map(r=>{const candidate=r.steps.some(s=>status(s.code));return `<article class="reaction-card"><div class="card-meta"><span>${r.family} <span aria-hidden="true">/</span> ${r.steps.length} STEP${r.steps.length>1?'S':''}</span><button class="save-button ${saved.includes(r.id)?'saved':''}" data-save="${r.id}" aria-label="${saved.includes(r.id)?'取消收藏':'收藏'} ${esc(r.name)}" aria-pressed="${saved.includes(r.id)}">${saved.includes(r.id)?'★':'☆'}</button></div><h3><button class="card-title" data-open="${r.id}">${esc(r.name)}</button></h3><div class="card-zh">${r.zh}</div><div class="card-codes">${r.steps.map(s=>code(s.code)).join('<span class="path-arrow">→</span>')}</div><p class="card-desc">${r.summary}</p><div class="card-bottom"><span class="card-status ${candidate?'candidate':''}">${candidate?'◌ 含候选编码':'● 沿用教学编码'}</span><button class="card-open" data-open="${r.id}">查看机理 <span>↗</span></button></div></article>`;}).join('');
   $$('[data-open]').forEach(b=>b.addEventListener('click',()=>openReaction(b.dataset.open)));
   $$('[data-save]').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.save;save(id);const replacement=$(`[data-save="${id}"]`);if(replacement)replacement.focus({preventScroll:true});}));
   const chips=[];if(filters.family)chips.push(['family',filters.family]);filters.axes.forEach((v,i)=>{if(v)chips.push(['axis'+i,D.axes[i].key+v]);});if(filters.steps!=='all')chips.push(['steps',filters.steps+' 步']);if(filters.candidate)chips.push(['candidate','含候选编码']);if(filters.saved)chips.push(['saved','收藏']);if(filters.query)chips.push(['query','搜索：'+filters.query]);
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

 function setTab(t){$$('[data-tab]').forEach(b=>{const active=b.dataset.tab===t;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;$('#panel-'+b.dataset.tab).hidden=!active;});}
 $$('[data-tab]').forEach(b=>{b.addEventListener('click',()=>setTab(b.dataset.tab));b.addEventListener('keydown',e=>{const tabs=$$('[data-tab]');let i=tabs.indexOf(b);if(e.key==='ArrowRight')i=(i+1)%tabs.length;else if(e.key==='ArrowLeft')i=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')i=0;else if(e.key==='End')i=tabs.length-1;else return;e.preventDefault();setTab(tabs[i].dataset.tab);tabs[i].focus();});});
 function openReaction(id,fromHash=false){
   const r=D.reactions.find(r=>r.id===id);if(!r)return;
   if(!$('#reaction-dialog').open){returnFocus=document.activeElement;previousHash=location.hash.startsWith('#reaction/')?'#atlas':location.hash;}
   selected=r;selectedStep=0;
   $('#dialog-breadcrumb').textContent='SORG / '+r.family+' / '+String(D.reactions.indexOf(r)+1).padStart(2,'0');
   $('#dialog-category').textContent='REACTION '+String(D.reactions.indexOf(r)+1).padStart(2,'0')+' / '+r.steps.length+' CODED EVENT'+(r.steps.length>1?'S':'');
   $('#dialog-title').textContent=r.name;$('#dialog-zh').textContent=r.zh;$('#dialog-equation').textContent=r.equation;$('#dialog-conditions').textContent=r.conditions;$('#dialog-summary').textContent=r.summary;
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
 function energyDiagram(n){
   const start=35,end=615,w=(end-start)/n;let d='M35 96';for(let i=0;i<n;i++){const x=start+i*w,y=96-i*8,endY=96-(i+1)*8;d+=` C${x+w*.17} ${y} ${x+w*.25} 22 ${x+w*.47} 25 C${x+w*.70} 27 ${x+w*.75} ${endY} ${x+w} ${endY}`;}
   return `<svg viewBox="0 0 650 145" role="img" aria-label="${n} 个峰对应 ${n} 个教学事件的定性示意"><path d="M22 10V122H630" fill="none" stroke="#bbc6b6"/><path d="${d}" fill="none" stroke="#4d7a66" stroke-width="2.3"/><text x="580" y="140" fill="#718079" font-size="10">反应坐标</text><text x="28" y="16" fill="#718079" font-size="10">示意能量</text></svg>`;
 }
 function renderMechanism(){const r=selected,s=r.steps[selectedStep],book=D.codebook[s.code];
   $('#panel-mechanism').innerHTML=`<div class="mechanism-layout"><div class="step-list" role="group" aria-label="选择机理步骤">${r.steps.map((st,i)=>`<button class="step-button ${i===selectedStep?'active':''}" data-step="${i}" aria-pressed="${i===selectedStep}"><span class="step-number">STEP ${String(i+1).padStart(2,'0')}</span><strong>${st.title}</strong>${code(st.code)}</button>`).join('')}</div><div class="step-reader"><div class="step-heading"><h3>${s.title}</h3><span class="badge ${status(s.code)?'candidate':''}">${status(s.code)?'◌ 候选编码':'● 沿用教学编码'}</span></div><div class="step-equation">${esc(s.equation)}</div><div class="mechanism-svg">${window.SorgDiagram(s.diagram)}<div class="svg-caption">通用局部电子推动图，基团已简化；具体底物与成断键以上方反应式及下方文字为准。</div></div><p class="flow-text">${s.flow}</p><div class="orbital-grid"><div><strong>ORBITAL INTERACTION</strong><p>${esc(s.orbital)}</p></div><div><strong>NUCLEAR GEOMETRY</strong><p>${s.geometry}</p></div></div><h4 class="why-title">为什么编码为 ${s.code}？</h4><div class="why-grid">${book.why.map((w,i)=>`<div class="why-item"><b>${D.axes[i].key}${s.code[i]}</b><span>${w}</span></div>`).join('')}</div><div class="boundary"><strong>编码边界 · </strong>${book.boundary}</div></div></div><div class="energy-box"><h4>一步一个事件，多步保留中间体<span>定性示意 · 无数值标度 · 非计算势能面</span></h4>${energyDiagram(r.steps.length)}<p>峰的数量仅用于对应这里显示的教学事件；峰高、谷深、总能量方向均未取自实验或计算，不代表实际速控步骤。配位及金属反应的面板可能压缩了更细的物种变化。</p></div>`;
   $$('[data-step]').forEach(b=>b.addEventListener('click',()=>{selectedStep=Number(b.dataset.step);renderMechanism();$(`[data-step="${selectedStep}"]`).focus({preventScroll:true});}));
 }
 const calcConfigs={
   acid:{title:'从 pKa 估计平衡',formula:'K = 10^[pKa(HB) − pKa(HA)]',a:'反应物酸 HA 的 pKa',b:'产物酸 HB 的 pKa',av:4.76,bv:9.31,tag:'教材值 → 公式推算',unit:'平衡常数 K',note:'模型：HA + B⁻ ⇌ A⁻ + HB。默认值为 CH₃CO₂H 的 4.76 与 HCN 的 9.31，取自所引教材的同一比较标度。使用活度定义，K 无量纲；跨溶剂、温度或标准态不可直接比较。修改后结果仅对应你的输入。'},
   rate1:{title:'浓度改变，速率怎样变？',formula:'v′ / v = [RX]′ / [RX]',a:'底物浓度倍数',b:'亲核体 / 碱浓度倍数（此模型不计）',av:2,bv:1,tag:'理想速率模型',unit:'倍 · 相对初速率',note:'仅在电离控制速率、温度和溶剂不变、k 不变且机理不切换的一级模型下成立。不是 SN1/E1 在所有介质中的完整动力学。'},
   rate2:{title:'浓度改变，速率怎样变？',formula:'v′ / v = ([RX]′/[RX]) × ([Nu/B]′/[Nu/B])',a:'底物浓度倍数',b:'亲核体 / 碱浓度倍数',av:2,bv:2,tag:'理想速率模型',unit:'倍 · 相对初速率',note:'假设 v = k[RX][Nu/B]，温度、溶剂、k 与机理不变。比较的是初速率，不是完成反应所需时间；竞争反应未纳入。'},
   barrier:{title:'能垒降低，会快多少？',formula:'kB / kA ≈ exp[(ΔG‡A − ΔG‡B) / RT]',a:'A 与 B 的能垒差 ΔG‡A − ΔG‡B (kJ/mol)',b:'温度 T (K)',av:5,bv:298.15,tag:'假设输入 · 非实测',unit:'倍 · kB / kA',note:'默认 5 kJ/mol 只是演示，不是这个反应的势垒。比较同温度、相同分子数与标准态、相同传递系数的两条路径，使用过渡态理论；R = 8.314462618 J·mol⁻¹·K⁻¹。计算不考虑隧穿、扩散或动力学耦合，也不自动给出产物比例。'}
 };
 function renderData(){const r=selected,cfg=calcConfigs[r.calc];
   $('#panel-data').innerHTML=`<div class="fact-grid">${r.facts.map(([a,b])=>`<article class="fact"><strong>${a}</strong><p>${b}</p></article>`).join('')}</div><div class="source-inline">事实来源：${r.sources.map(sourceLink).join(' · ')}</div><div class="calculator"><div class="calculator-top"><h3>${cfg.title}</h3><span class="hypothetical">${cfg.tag}</span></div><div class="calc-formula">${cfg.formula}</div><div class="calc-inputs"><label>${cfg.a}<input id="calc-a" type="number" step="any" value="${cfg.av}" inputmode="decimal"></label><label>${cfg.b}<input id="calc-b" type="number" step="any" value="${cfg.bv}" inputmode="decimal" ${r.calc==='rate1'?'disabled':''}></label></div><div class="calc-output"><output id="calc-result" aria-live="polite"></output><span>${cfg.unit}</span></div><p class="calc-error" id="calc-error" role="status" hidden></p><p class="calc-note">${cfg.note}</p><div class="source-inline">公式依据：${sourceLink(r.calc==='barrier'?'tst':r.sources[0])}</div></div>`;
   $('#calc-a').addEventListener('input',compute);$('#calc-b').addEventListener('input',compute);compute();
 }
 function compute(){try{if($('#calc-a').value===''||$('#calc-b').value==='')throw new Error('请填入两个数值。');const result=C.calculate(selected.calc,Number($('#calc-a').value),Number($('#calc-b').value));let formatted;
     if(!Number.isFinite(result.value))formatted=`10^${result.log10.toFixed(2)}`;
     else if(result.value===0&&Number.isFinite(result.log10))formatted=`10^${result.log10.toFixed(2)}`;
     else if(result.value!==0&&(result.value<.001||result.value>=10000))formatted=result.value.toExponential(3);
     else formatted=Number(result.value.toPrecision(4)).toLocaleString('en-US',{maximumSignificantDigits:4});
     $('#calc-result').textContent=formatted;$('#calc-error').hidden=true;
   }catch(e){$('#calc-result').textContent='—';$('#calc-error').textContent=e.message;$('#calc-error').hidden=false;}}
 function renderSources(){const r=selected;$('#panel-sources').innerHTML=`<div class="sources-section"><h3>适用范围与简化</h3><p>${r.scope}</p>${r.note?`<div class="boundary">${r.note}</div>`:''}<h3>编码的来源</h3><p>四位码由本项目的 SORG 教学规则分配；下列文献支持机理与化学数据，不声称使用或验证了 SORG。本条中的 ${[...new Set(r.steps.map(s=>s.code))].map(c=>c+(status(c)?'（候选）':'（沿用）')).join('、')} 均为定性教学标签。</p><h3>可以继续读</h3><ul class="source-list">${r.sources.map(id=>`<li>${sourceLink(id)}<small>${D.sources[id].publisher} · 核对日期 ${D.sources[id].checked}</small></li>`).join('')}</ul><p class="small-note">Access for free at OpenStax Organic Chemistry. 教学文字整理按 CC BY-NC-SA 4.0 提供；示意图为本站原创。每个具体数值的条件见“数据与计算”。</p></div>`;}
 function route(){if(location.hash.startsWith('#reaction/')){let id;try{id=decodeURIComponent(location.hash.slice(10));}catch{return;}if(D.reactions.some(r=>r.id===id))openReaction(id,true);}else if($('#reaction-dialog').open)closeReaction();}
 window.addEventListener('hashchange',route);
 updateSaved();renderFamily();renderCards();renderHero();route();
})();
