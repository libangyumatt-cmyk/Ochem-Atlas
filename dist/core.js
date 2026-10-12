(function(root){
  'use strict';
  const R=8.31446261815324;
  function matches(reaction,filters,codebook,saved){
    if(filters.family && reaction.family!==filters.family)return false;
    if(filters.steps!=='all' && reaction.steps.length!==Number(filters.steps))return false;
    if(filters.candidate && !reaction.steps.some(s=>codebook[s.code].status==='candidate'))return false;
    if(filters.saved && !saved.includes(reaction.id))return false;
    if(!reaction.steps.some(s=>filters.axes.every((v,i)=>!v||s.code[i]===v)))return false;
    const q=filters.query.trim().toLowerCase();
    const hay=[reaction.name,reaction.zh,reaction.family,reaction.equation,reaction.summary,reaction.conditions,...reaction.steps.flatMap(s=>[s.code,s.title,s.orbital,s.flow])].join(' ').toLowerCase();
    return !q||hay.includes(q);
  }
  function orbitalMixing(deltaE,V){
    if(!Number.isFinite(deltaE)||!Number.isFinite(V))throw new Error('请输入有效的轨道能量与耦合矩阵元。');
    if(Math.abs(deltaE)>100||Math.abs(V)>100)throw new Error('教学模型输入范围为 −100 到 100 eV。');
    const splitting=Math.hypot(deltaE,2*V);
    if(splitting===0)throw new Error('两个未耦合态完全简并时，此混合指标没有定义。');
    const mixing=(4*V*V)/(splitting*splitting);
    return {splitting,mixing,lowerStateDonorWeight:deltaE===0?0.5:(1+deltaE/splitting)/2};
  }
  const api={matches,orbitalMixing,R};
  if(typeof module!=='undefined')module.exports=api;else root.SorgCore=api;
})(typeof window!=='undefined'?window:globalThis);
