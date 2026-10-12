(function(){
 'use strict';
 let counter=0;
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 window.SorgDiagram=function(type){
   const id='m'+counter++;
   const text=(x,y,s,size=21,color='#203c43')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="middle" dominant-baseline="middle">${esc(s)}</text>`;
   const bond=(x1,y1,x2,y2,dash=false)=>`<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${dash?'#88a58d':'#435b5c'}" stroke-width="2" ${dash?'stroke-dasharray="5 5"':''}/>`;
   const arrow=(d,single=false)=>`<path d="${d}" fill="none" stroke="#aa6a4e" stroke-width="2.1" marker-end="url(#${id}${single?'f':'a'})"/>`;
   const label=(s)=>text(320,207,s,11,'#718079');
   let g='',caption='电子对推动的局部模式';
   if(type==='sn2'){
     g=text(110,120,'Nu:⁻')+text(307,120,'C')+text(458,120,'X')+bond(323,120,441,120)+bond(297,106,261,62)+bond(310,103,321,59)+bond(300,134,271,170)+arrow('M140 111 C197 33 255 45 290 102')+arrow('M383 116 C400 61 445 65 453 99')+label('n(Nu) → σ*(C–X) · 背面进攻 / 离去');
   }else if(type==='proton'){
     g=text(105,116,'B:')+text(295,116,'H')+text(434,116,'A')+bond(310,116,417,116)+arrow('M127 105 C174 42 247 47 281 103')+arrow('M365 112 C380 68 419 65 430 96')+label('n(B) → σ*(H–A) · B–H 形成，H–A 断裂');
   }else if(type==='carbonyl'){
     g=text(130,160,'Nu:⁻')+text(335,126,'C')+text(395,66,'O')+bond(347,112,379,80)+bond(355,119,387,87)+bond(320,127,282,97)+bond(337,143,347,176)+arrow('M160 154 C225 93 282 170 317 138')+arrow('M375 107 C414 132 436 84 413 71')+label('C–Nu 成键 · π(C=O) → O · 平面趋向四面体');
   }else if(type==='collapse'){
     g=text(329,128,'C')+text(334,43,'O:⁻')+text(474,128,'LG')+text(233,77,'R')+text(233,174,'OR′')+bond(330,58,330,108)+bond(346,128,451,128)+bond(314,117,247,84)+bond(314,139,254,164)+arrow('M351 52 C401 77 377 100 343 93')+arrow('M398 124 C424 69 465 78 472 105')+label('n(O) 恢复 C=O · C–LG 键电子对移向 LG');
   }else if(type==='ion'){
     g=text(187,116,'R₃C')+text(383,116,'X')+bond(220,116,366,116)+arrow('M293 110 C300 38 366 45 379 95')+text(310,159,'R₃C⁺  +  X⁻',16,'#376f69')+label('异裂：一对成键电子共同移向离去基团');
   }else if(type==='capture'){
     g=text(140,122,'Nu:')+text(367,122,'C⁺')+bond(350,116,307,72)+bond(367,103,381,59)+bond(370,139,387,179)+arrow('M169 111 C222 40 305 47 346 103')+label('孤对电子 → 空 p 轨道 · 新的 C–Nu 联系');
   }else if(type==='lewis'){
     g=text(160,117,'D:')+text(421,117,'A')+arrow('M184 104 C241 36 343 43 403 99')+text(310,163,'D → A',17,'#376f69')+label('Lewis donor 的孤对电子 → Lewis acceptor');
   }else if(type==='alkene'){
     g=text(153,114,'C')+text(266,114,'C')+bond(170,109,250,109)+bond(170,120,250,120)+text(370,114,'H')+text(507,114,'A')+bond(388,114,491,114)+arrow('M211 105 C240 34 324 48 357 97')+arrow('M445 110 C457 66 494 69 503 94')+label('π(C=C) → H · H–A → A · 形成碳正离子');
   }else if(type==='e2'||type==='e1'){
     g=text(73,62,'B:')+text(204,62,'H')+text(232,126,'Cβ',19)+text(375,126,'Cα',19)+bond(211,77,225,108)+bond(251,126,354,126)+arrow('M91 53 C128 9 181 21 197 43')+arrow('M214 90 C268 74 288 102 300 115');
     if(type==='e2')g+=text(403,179,'X')+bond(382,142,397,162)+arrow('M392 151 C455 133 452 187 425 180');
     else g+=text(401,106,'+',14);
     g+=label(type==='e2'?'三对电子耦合推动 · 构象要求见文字说明':'脱去 β-H，σ(C–H) 电子对形成新的 π 键');
   }else if(type==='radical'){
     g=text(107,130,'R•')+text(305,130,'C')+text(450,130,'C')+bond(323,123,432,123)+bond(323,134,432,134)+arrow('M125 117 C179 49 214 69 240 118',true)+arrow('M374 120 C331 42 275 62 245 116',true)+arrow('M379 136 C410 174 445 164 448 148',true)+label('半箭头各表示一个电子 · 新键由两个电子组成');caption='单电子推动：每一支弧形半箭头代表一个电子';
   }else if(type==='recombine'){
     g=text(164,122,'R•')+text(454,122,'•R′')+arrow('M179 112 C213 49 276 48 305 107',true)+arrow('M435 112 C400 49 336 48 314 107',true)+text(308,158,'R–R′',20,'#376f69')+label('两个单占轨道中的电子配对，形成 σ 键');caption='单电子推动：两个自由基各贡献一个电子';
   }else if(type==='hat'){
     g=text(107,125,'R•')+text(302,125,'A')+text(468,125,'B')+bond(321,125,452,125)+arrow('M122 113 C171 50 224 60 241 111',true)+arrow('M378 121 C331 45 276 57 247 112',true)+arrow('M385 130 C408 175 452 172 465 145',true)+label('A 可为 H 或卤素 · R–A 形成，A–B 均裂');caption='原子转移的单电子模式：三支弧形半箭头';
   }else if(type==='da'){
     const p=[[215,49],[144,84],[144,147],[215,180],[385,164],[385,66]];
     g=p.map((v,i)=>text(v[0],v[1],String(i+1),13)).join('');
     g+=bond(202,54,158,77)+bond(199,44,151,67)+bond(144,98,144,133)+bond(158,154,202,175)+bond(153,164,198,185)+bond(379,80,379,151)+bond(391,80,391,151)+bond(230,50,370,65,true)+bond(230,179,370,166,true);
     g+=arrow('M179 57 C207 9 268 9 298 51')+arrow('M392 115 C445 167 369 196 301 173')+arrow('M174 170 C106 203 97 143 132 116')+label('原子编号示意 · 3 π → 2 σ + 1 π · 虚线为新联系');
   }else if(type==='cyclic'){
     const p=[[235,35,'O'],[165,77,'C'],[165,150,'C'],[235,180,'C'],[307,150,'C'],[307,77,'C']];
     g=p.map(v=>text(v[0],v[1],v[2],17)).join('');
     g+=bond(222,43,179,70)+bond(160,91,160,137)+bond(171,91,171,137)+bond(178,157,222,175,true)+bond(249,175,294,154)+bond(253,183,301,163)+bond(307,91,307,136)+bond(294,70,249,43);
     g+=arrow('M274 53 C266 1 204 2 201 47')+arrow('M157 115 C102 138 151 194 196 175')+arrow('M279 172 C355 194 361 124 320 114')+text(461,90,'[3,3]',27)+text(461,124,'σ-migration',13,'#718079')+label('Allyl vinyl ether · 原 O–allyl 键断裂，新 C–C 键形成');
   }else if(type==='electro'){
     g=bond(144,71,229,115)+bond(148,82,225,124)+bond(229,115,329,115)+bond(329,115,414,71)+bond(333,124,418,82)+bond(144,71,414,71,true)+arrow('M182 88 C177 24 264 20 282 62')+arrow('M372 88 C355 158 305 161 282 127')+text(493,92,'4π',27)+text(493,123,'thermal',13,'#718079')+label('键重排示意（不是立体投影）· conrotatory 见文字');
   }
   return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 230" role="img" aria-label="${esc(caption)}"><defs><marker id="${id}a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="#aa6a4e" stroke-width="1.5"/></marker><marker id="${id}f" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5" fill="none" stroke="#aa6a4e" stroke-width="1.5"/></marker></defs><g font-family="Georgia,Times New Roman,serif">${g}</g></svg>`;
 };
})();
