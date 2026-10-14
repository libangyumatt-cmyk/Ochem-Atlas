/* Deliberately scalar educational fixed point; not an electronic-structure SCF. */
(function(root){
 'use strict';
 const target=(d,kappa,delta=-.25,width=.20)=>1/(1+Math.exp((delta+kappa*d)/width));
 function iterate(kappa,alpha,n=24,start=.1){
  const rows=[{n:0,d:start,residual:Math.abs(target(start,kappa)-start)}];
  for(let i=1;i<=n;i++){
   const prev=rows.at(-1).d,next=(1-alpha)*prev+alpha*target(prev,kappa);
   rows.push({n:i,d:next,residual:Math.abs(target(next,kappa)-next)});
  }
  return rows;
 }
 root.SorgSCF={target,iterate};
 if(!root.document)return;
 const $=s=>document.querySelector(s);
 const draw=()=>{
  const k=Number($('#scf-feedback').value),a=Number($('#scf-mix').value),rows=iterate(k,a);
  $('#scf-feedback-value').textContent=k.toFixed(2)+' eV';
  $('#scf-mix-value').textContent=a.toFixed(2);
  const points=rows.map(({n,d})=>`${30+n*18.5},${192-158*d}`).join(' ');
  $('#scf-plot').innerHTML=`<svg viewBox="0 0 520 226" role="img" aria-label="Illustrative scalar occupation over 24 iterations, from ${rows[0].d.toFixed(3)} to ${rows.at(-1).d.toFixed(3)}"><line x1="30" y1="192" x2="476" y2="192" class="axis-line"/><line x1="30" y1="34" x2="30" y2="192" class="axis-line"/><polyline points="${points}" class="model-teal-path"/><text x="40" y="20">d · dimensionless trial occupation</text><text x="402" y="211">iteration n →</text><text x="8" y="38">1</text><text x="9" y="190">0</text></svg>`;
  const last=rows.at(-1);
  $('#scf-readout').textContent=`After 24 updates: d = ${last.d.toFixed(5)}, |f(d) − d| = ${last.residual.toExponential(2)}. ${last.residual<1e-5?'Near a fixed point by this tolerance.':'Not converged to the displayed tolerance.'} This scalar model is not a molecular calculation.`;
 };
 $('#scf-feedback').addEventListener('input',draw);
 $('#scf-mix').addEventListener('input',draw);
 draw();
})(typeof window==='undefined'?globalThis:window);
