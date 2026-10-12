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
  function calculate(type,a,b){
    if(!Number.isFinite(a)||!Number.isFinite(b))throw new Error('请填入有效数字。');
    if(type==='acid'){
      if(Math.abs(a)>100||Math.abs(b)>100)throw new Error('本教学工具的 pKa 输入范围为 −100 到 100。');
      return {value:Math.pow(10,b-a),log10:b-a};
    }
    if(type==='rate1'||type==='rate2'){
      if(a<0||b<0||a>1000000||b>1000000)throw new Error('浓度倍数须在 0 到 10⁶ 之间。');
      return {value:type==='rate1'?a:a*b};
    }
    if(b<=0||b>5000||Math.abs(a)>200)throw new Error('温度须为 0–5000 K（不含 0）；能垒差须在 ±200 kJ/mol 内。');
    const log10=1000*a/(R*b*Math.LN10);
    return {value:Math.exp(1000*a/(R*b)),log10};
  }
  const api={matches,calculate,R};
  if(typeof module!=='undefined')module.exports=api;else root.SorgCore=api;
})(typeof window!=='undefined'?window:globalThis);
