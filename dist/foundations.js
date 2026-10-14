/* Original, analytic teaching models. No values here are quantum-chemical calculations. */
(function(root){
 'use strict';
 const twoState=(delta,v)=>{
  const radius=Math.hypot(delta/2,v), lower=delta/2-radius, upper=delta/2+radius;
  return {lower,upper,gap:2*radius,acceptorWeight:radius===0?null:(1-delta/(2*radius))/2};
 };
 const pes=(x,y,a=1,b=0.6)=>({energy:a*(x*x-1)**2+b*y*y,
  gradient:[4*a*x*(x*x-1),2*b*y],hessian:[4*a*(3*x*x-1),2*b]});
 const gauss=(x,c,s)=>Math.PI**(-0.25)/Math.sqrt(s)*Math.exp(-(((x-c)/s)**2)/2);
 const density=(x)=>{
  const s=0.85,c=1.15,gA=gauss(x,-c,s),gB=gauss(x,c,s);
  const overlap=Math.exp(-c*c/(s*s)),bond=(gA+gB)/Math.sqrt(2*(1+overlap));
  const p=Math.sqrt(2/Math.sqrt(Math.PI))*x*Math.exp(-x*x/2);
  return {phase:p,probability:p*p,total:2*bond*bond,difference:2*bond*bond-gA*gA-gB*gB};
 };
 root.SorgModels={twoState,pes,density};
 if(!root.document)return;
 const $=s=>document.querySelector(s),svg=(contents,label)=>`<svg viewBox="0 0 520 252" role="img" aria-label="${label}" preserveAspectRatio="xMidYMid meet"><title>${label}</title>${contents}</svg>`;
 const line=(x1,y1,x2,y2,klass='gridline')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${klass}"/>`;
 const fmt=(v,n=2)=>v.toFixed(n).replace('-', '−');
 function drawCoupling(){
  const delta=Number($('#coupling-gap').value),v=Number($('#coupling-v').value),m=twoState(delta,v);
  $('#coupling-gap-value').textContent=`${fmt(delta,1)} eV`;
  $('#coupling-v-value').textContent=`${fmt(v,2)} eV`;
  const y=e=>210-(e+2)*38;
  const baseline=line(38,210,480,210,'axis-line');
  $('#coupling-plot').innerHTML=svg(`${baseline}<text x="40" y="228">Energy relative to εD · eV ↑</text><text x="102" y="36">No coupling (V = 0)</text><text x="330" y="36">Coupled levels</text>
    ${line(115,y(0),210,y(0),'model-muted')}${line(115,y(delta),210,y(delta),'model-muted')}
    ${line(325,y(m.lower),435,y(m.lower),'model-teal')}${line(325,y(m.upper),435,y(m.upper),'model-gold')}
    <text x="52" y="${y(0)+4}">εD 0</text><text x="52" y="${y(delta)+4}">εA ${fmt(delta,1)}</text>
    <text x="439" y="${y(m.lower)+4}">E−</text><text x="439" y="${y(m.upper)+4}">E+</text>`,
    `Uncoupled energies 0 and ${fmt(delta,1)} electronvolts; with coupling ${fmt(v,2)} electronvolts, eigenvalues ${fmt(m.lower)} and ${fmt(m.upper)} electronvolts`);
  $('#coupling-readout').innerHTML=`E<sub>−</sub> = ${fmt(m.lower)} eV · E<sub>+</sub> = ${fmt(m.upper)} eV · level separation = ${fmt(m.gap)} eV. ${m.acceptorWeight===null?'Exact degeneracy: mixing is not uniquely defined.':`Lower-state |A⟩ weight = ${fmt(m.acceptorWeight*100,1)}% in this chosen orthonormal basis.`}`;
 }
 $('#coupling-gap').addEventListener('input',drawCoupling);$('#coupling-v').addEventListener('input',drawCoupling);drawCoupling();
 let densityMode='phase';
 const densCaption={phase:'Signed ψp(x) has opposite phases across a node at x = 0. The two colors identify phase sign, never positive/negative charge.',probability:'|ψp(x)|² is nonnegative and zero at the node. The area integrates to one in this normalized 1D model.',total:'Two electrons occupy the normalized bonding combination of two Gaussian basis functions. ρbond(x) ≥ 0 and integrates to two electrons per dimensionless x.',difference:'Δρ(x) = ρbond(x) − [|gA(x)|² + |gB(x)|²]. Positive/negative regions mean accumulation/depletion relative to that reference; the signed integral is zero.'};
 function drawDensity(){
  const mode=densityMode,points=Array.from({length:181},(_,i)=>-3.6+i*7.2/180);
  const ymax=mode==='phase'?0.95:mode==='difference'?0.35:1.15;
  const zero=mode==='phase'||mode==='difference'?129:209;
  const y=v=>zero-v*(mode==='phase'||mode==='difference'?93:154)/ymax;
  const xy=(x)=>50+(x+3.6)*430/7.2;
  const segment=(filter)=>points.map((x,i)=>`${i?'L':'M'}${xy(x).toFixed(1)},${y(filter(density(x))).toFixed(1)}`).join(' ');
  let paths='';
  if(mode==='phase'||mode==='difference'){
   const plus=x=>Math.max(0,density(x)[mode]),minus=x=>Math.min(0,density(x)[mode]);
   paths=`<path d="${segment(plus)}" class="model-teal-path"/><path d="${segment(minus)}" class="model-gold-path"/>`;
  }else paths=`<path d="${segment(x=>density(x)[mode])}" class="model-teal-path"/>`;
  $('#density-plot').innerHTML=svg(`${line(50,zero,480,zero,'axis-line')}${line(265,25,265,215,'gridline')}${paths}<text x="42" y="232">−3.6</text><text x="253" y="232">x = 0</text><text x="454" y="232">3.6</text><text x="57" y="24">${mode==='phase'?'ψp · signed amplitude':mode==='probability'?'|ψp|² · probability density':mode==='total'?'ρbond · electron density':'Δρ · density difference'}</text>`,densCaption[mode]);
  $('#density-caption').textContent=densCaption[mode];
  document.querySelectorAll('[data-density]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.density===mode)));
 }
 document.querySelectorAll('[data-density]').forEach(b=>b.addEventListener('click',()=>{densityMode=b.dataset.density;drawDensity();}));drawDensity();
 function drawPes(){
  const a=Number($('#pes-barrier').value),x=Number($('#pes-x').value),m=pes(x,0,a);
  $('#pes-barrier-value').textContent=`${fmt(a,1)} eV`;$('#pes-x-value').textContent=fmt(x);
  const px=x=>62+(x+1.4)*222/2.8,py=y=>216-(y+1)*172/2;
  const profileX=x=>320+(x+1)*150/2,profileY=e=>206-e*118/2;
  let cells='';for(let i=0;i<35;i++)for(let j=0;j<24;j++){
   const xx=-1.4+(i+.5)*2.8/35,yy=-1+(j+.5)*2/24,v=pes(xx,yy,a).energy;
   const alpha=Math.max(.07,Math.min(.78,v/3));
   cells+=`<rect x="${(62+i*222/35).toFixed(1)}" y="${(44+j*172/24).toFixed(1)}" width="6.5" height="7.5" fill="rgba(169,121,56,${alpha.toFixed(2)})"/>`;
  }
  const path=Array.from({length:81},(_,i)=>{const z=-1+i*2/80;return `${i?'L':'M'}${profileX(z).toFixed(1)},${profileY(pes(z,0,a).energy).toFixed(1)}`}).join(' ');
  $('#pes-plot').innerHTML=svg(`${cells}${line(px(-1),py(0),px(1),py(0),'model-path')}${line(318,206,478,206,'axis-line')}<path d="${path}" class="model-teal-path"/>
   <circle cx="${px(-1)}" cy="${py(0)}" r="5" class="model-teal-fill"/><circle cx="${px(1)}" cy="${py(0)}" r="5" class="model-teal-fill"/><circle cx="${px(0)}" cy="${py(0)}" r="5" class="model-gold-fill"/>
   <circle cx="${px(x)}" cy="${py(0)}" r="7" class="model-point"/><circle cx="${profileX(x)}" cy="${profileY(m.energy)}" r="6" class="model-point"/>
   <text x="65" y="29">U(x,y) · color = energy</text><text x="319" y="29">Path y = 0</text><text x="70" y="235">x = −1 min</text><text x="173" y="235">0 saddle</text><text x="315" y="235">−1</text><text x="391" y="235">0</text><text x="465" y="235">1</text>`,
   `Illustrative two-dimensional potential energy surface. At x ${fmt(x)}, y zero, energy ${fmt(m.energy)} electronvolts; minima at plus and minus one and saddle at zero`);
  const stationary=Math.abs(x+1)<1e-9?'minimum (−1,0)':Math.abs(x-1)<1e-9?'minimum (+1,0)':Math.abs(x)<1e-9?'first-order saddle (0,0)':'nonstationary point';
  $('#pes-readout').innerHTML=`U = ${fmt(m.energy)} eV; ∂U/∂x = ${fmt(m.gradient[0])} eV per model x; Hessian diagonal = (${fmt(m.hessian[0])}, ${fmt(m.hessian[1])}) eV per model-coordinate squared. <strong>${stationary}</strong>. Barrier from either minimum: ${fmt(a,1)} eV.`;
 }
 $('#pes-barrier').addEventListener('input',drawPes);$('#pes-x').addEventListener('input',drawPes);drawPes();
})(typeof window==='undefined'?globalThis:window);
