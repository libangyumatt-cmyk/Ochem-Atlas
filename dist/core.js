(function(root){
  'use strict';
  const isCandidate=(s,book)=>book[s.code]?.status==='candidate'||s.assignmentStatus==='candidate';
  const normalize=value=>String(value??'').normalize('NFKC').toLowerCase();
  function matches(reaction,filters,codebook,saved){
    if(filters.family && reaction.family!==filters.family)return false;
    if(filters.steps!=='all' && reaction.steps.length!==Number(filters.steps))return false;
    if(filters.candidate && !reaction.steps.some(s=>isCandidate(s,codebook)))return false;
    if(filters.saved && !saved.includes(reaction.id))return false;
    if(!reaction.steps.some(s=>filters.axes.every((v,i)=>!v||s.code[i]===v)))return false;
    const q=normalize(filters.query).trim();
    const hay=normalize([reaction.name,reaction.zh,reaction.family,reaction.equation,reaction.summary,reaction.conditions,...reaction.steps.flatMap(s=>[s.code,s.title,s.equation,s.orbital,s.flow])].join(' '));
    return !q||hay.includes(q);
  }
  const api={matches,isCandidate};
  if(typeof module!=='undefined')module.exports=api;else root.SorgCore=api;
})(typeof window!=='undefined'?window:globalThis);
