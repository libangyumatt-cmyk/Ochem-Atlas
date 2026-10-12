(function(root){
  'use strict';
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
  const api={matches};
  if(typeof module!=='undefined')module.exports=api;else root.SorgCore=api;
})(typeof window!=='undefined'?window:globalThis);
