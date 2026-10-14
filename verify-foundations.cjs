'use strict';
// Analytical checks for original teaching models, not molecular computations.
const assert=require('node:assert/strict');
require('./dist/foundations.js');
const {twoState,pes,density}=globalThis.SorgModels;
const close=(a,b,tol=1e-10)=>assert.ok(Math.abs(a-b)<tol,`${a} differs from ${b}`);
let n=0;
for(const gap of [0,.2,1,2,4])for(const v of [0,.05,.5,1,2]){
 const m=twoState(gap,v);close(m.lower+m.upper,gap);close(m.lower*m.upper,-v*v);
 close(m.gap,Math.hypot(gap,2*v));
 if(gap||v){assert.ok(m.acceptorWeight>=0&&m.acceptorWeight<=.5);if(gap===0)close(m.acceptorWeight,.5);if(v===0)close(m.acceptorWeight,0);}
 else assert.equal(m.acceptorWeight,null);
 n++;
}
close(twoState(2,0).lower,0);close(twoState(2,0).upper,2);
close(twoState(0,1).lower,-1);close(twoState(0,1).upper,1);
close(twoState(2,1).lower,1-Math.sqrt(2));
for(const a of [.4,1,2]){
 const left=pes(-1,0,a),right=pes(1,0,a),saddle=pes(0,0,a);
 close(left.energy,0);close(right.energy,0);close(saddle.energy,a);
 left.gradient.forEach(v=>close(v,0));saddle.gradient.forEach(v=>close(v,0));
 assert.ok(left.hessian.every(x=>x>0));assert.ok(saddle.hessian[0]<0&&saddle.hessian[1]>0);
 for(const x of [-.8,-.3,.25,.75]){
  const h=1e-5,der=(pes(x+h,0,a).energy-pes(x-h,0,a).energy)/(2*h);
  close(der,pes(x,0,a).gradient[0],1e-8);n++;
 }
}
// Numerical quadrature verifies the two-electron toy normalization and signed difference.
const h=.004;let prob=0,total=0,diff=0;
for(let i=0;i<=4000;i++){
 const x=-8+i*h,w=(i===0||i===4000)?.5:1,d=density(x);
 prob+=w*d.probability*h;total+=w*d.total*h;diff+=w*d.difference*h;
 assert.ok(d.probability>=0&&d.total>=0);
 close(density(-x).phase,-density(x).phase,1e-12);
 n++;
}
close(prob,1,1e-5);close(total,2,1e-5);close(diff,0,1e-5);
console.log(`PASS: ${n} analytic/grid model cases: Hermitian eigenvalue identities, mixing bounds, PES gradients/Hessian, normalized density and zero-integral difference. No molecular calculation.`);
