'use strict';
// Independent reconstruction from saved arrays; no PySCF or new SCF calculation.
const fs=require('node:fs'),path=require('node:path'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const base='dist/reaction-lab/diels-alder/r2/restart-20261022',BOHR=0.52917721092;
const json=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const crcTable=Array.from({length:256},(_,n)=>{let c=n;for(let i=0;i<8;i++)c=(c&1)?0xedb88320^(c>>>1):c>>>1;return c>>>0;});
function crc32(b){let c=0xffffffff;for(const x of b)c=crcTable[(c^x)&255]^(c>>>8);return(c^0xffffffff)>>>0;}
function unzip(file){
 const b=fs.readFileSync(file);let end=b.length-22;
 while(end>=Math.max(0,b.length-65557)&&b.readUInt32LE(end)!==0x06054b50)end--;
 assert.ok(end>=0,'ZIP end: '+file);let p=b.readUInt32LE(end+16);const count=b.readUInt16LE(end+10),out=new Map();
 for(let i=0;i<count;i++){
  assert.equal(b.readUInt32LE(p),0x02014b50);const method=b.readUInt16LE(p+10),crc=b.readUInt32LE(p+16),size=b.readUInt32LE(p+20),rawSize=b.readUInt32LE(p+24),nl=b.readUInt16LE(p+28),el=b.readUInt16LE(p+30),cl=b.readUInt16LE(p+32),local=b.readUInt32LE(p+42),name=b.toString('utf8',p+46,p+46+nl);
  assert.ok(rawSize<200000000);assert.equal(b.readUInt32LE(local),0x04034b50);
  const start=local+30+b.readUInt16LE(local+26)+b.readUInt16LE(local+28),packed=b.subarray(start,start+size),data=method===8?zlib.inflateRawSync(packed):packed;
  assert.ok(method===0||method===8);assert.equal(data.length,rawSize);assert.equal(crc32(data),crc,'ZIP CRC: '+name);out.set(name,data);p+=46+nl+el+cl;
 }return out;
}
function array(b){
 assert.equal(b.toString('latin1',0,6),'\x93NUMPY');const version=b[6],len=version===1?b.readUInt16LE(8):b.readUInt32LE(8),offset=(version===1?10:12)+len,header=b.toString('utf8',version===1?10:12,offset);
 const dtype=header.match(/'descr'\s*:\s*'([^']+)'/)[1],shape=header.match(/'shape'\s*:\s*\(([^)]*)\)/)[1].split(',').map(s=>s.trim()).filter(Boolean).map(Number),fortran=/'fortran_order'\s*:\s*True/.test(header),n=shape.reduce((a,b)=>a*b,1);
 assert.ok(dtype==='<f8'||dtype==='<f4'||dtype==='=f8'||dtype==='=f4','Float array required: '+dtype);
 const bytes=dtype.endsWith('8')?8:4;assert.equal(b.length-offset,n*bytes);const raw=new Float64Array(n);
 for(let i=0;i<n;i++){raw[i]=bytes===8?b.readDoubleLE(offset+i*bytes):b.readFloatLE(offset+i*bytes);assert.ok(Number.isFinite(raw[i]));}
 if(!fortran||shape.length<2)return{shape,data:raw};
 const data=new Float64Array(n),strides=[];let stride=1;for(const s of shape){strides.push(stride);stride*=s;}
 for(let i=0;i<n;i++){let rest=i,fi=0;for(let d=shape.length-1;d>=0;d--){const idx=rest%shape[d];rest=Math.floor(rest/shape[d]);fi+=idx*strides[d];}data[i]=raw[fi];}
 return{shape,data};
}
const get=(z,key)=>{assert.ok(z.has(key+'.npy'),key);return array(z.get(key+'.npy'));};
function multiply(a,b,n,m,k){const c=new Float64Array(n*k);for(let i=0;i<n;i++)for(let t=0;t<m;t++){const v=a[i*m+t];for(let j=0;j<k;j++)c[i*k+j]+=v*b[t*k+j];}return c;}
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
let matrices=0;
for(const file of walk(base).filter(f=>f.endsWith('.npz'))){
 const z=unzip(file);if(!z.has('mo_coeff.npy')||!z.has('density_matrix.npy')||!z.has('overlap.npy'))continue;
 const c=get(z,'mo_coeff'),s=get(z,'overlap'),p=get(z,'density_matrix'),n=s.shape[0],m=c.shape[1];assert.deepEqual(s.shape,[n,n]);assert.deepEqual(p.shape,[n,n]);assert.equal(c.shape[0],n);
 const sc=multiply(s.data,c.data,n,n,m);let error=0,electrons=0,hermitian=0;
 for(let j=0;j<m;j++)for(let k=0;k<m;k++){let v=0;for(let i=0;i<n;i++)v+=c.data[i*m+j]*sc[i*m+k];error=Math.max(error,Math.abs(v-(j===k?1:0)));}
 for(let i=0;i<n;i++)for(let j=0;j<n;j++){electrons+=p.data[i*n+j]*s.data[j*n+i];hermitian=Math.max(hermitian,Math.abs(p.data[i*n+j]-p.data[j*n+i]));}
 const expected=file.includes('reactant-ethylene')?16:file.includes('reactant-butadiene')?30:46;
 assert.ok(error<1e-8,'MO metric: '+file+' '+error);assert.ok(Math.abs(electrons-expected)<1e-8,'Electron count: '+file);assert.ok(hermitian<1e-10,'Density Hermiticity: '+file);matrices++;
}
const report=json(base+'/path-validation.json');let retainedPoints=0;
for(const direction of ['forward','backward']){
 const z=unzip(base+'/'+direction+'/evaluations.zip'),ev=new Map();
 for(const [name,b]of z){if(!name.endsWith('.json'))continue;const e=JSON.parse(b.toString('utf8'));ev.set(e.evaluation,e);assert.equal(e.scfConverged,true);assert.ok(Math.abs(e.electronCount-46)<1e-8);assert.ok(e.orbitalGradientNorm<3e-6);}
 for(const point of report.branches[direction].acceptedIRCPoints){
  const e=ev.get(point.evaluation);assert.ok(e,'Retained SCF provenance: '+direction+' '+point.evaluation);assert.ok(Math.abs(e.energyHartree-point.energyHartree)<1e-10);assert.equal(e.coordinatesBohr.length,16);
  for(let i=0;i<16;i++)for(let j=0;j<3;j++)assert.ok(Math.abs(e.coordinatesBohr[i][j]*BOHR-point.coordinatesAngstrom[i][j])<1e-8);
  for(const [k,pair]of [[0,[0,4]],[1,[3,5]]]){const d=Math.hypot(...e.coordinatesBohr[pair[0]].map((v,j)=>v-e.coordinatesBohr[pair[1]][j]))*BOHR;assert.ok(Math.abs(d-point.formingDistancesAngstrom[k])<1e-8);}
  retainedPoints++;
 }
}
const soft=json(base+'/soft-mode/results.json'),definition=json(base+'/soft-mode/definition.json');assert.equal(soft.points.length,10);
for(const p of soft.points){
 const z=unzip(base+'/soft-mode/'+p.id+'.npz'),x=get(z,'coordinatesAngstrom'),e=get(z,'energyHartree').data[0];assert.ok(Math.abs(e-p.energyHartree)<1e-12);
 for(let i=0;i<16;i++)for(let j=0;j<3;j++)assert.ok(Math.abs(x.data[3*i+j]-definition.coordinatesAngstrom[i][j]-p.displacementNormAngstrom*definition.cartesianUnitMode[i][j])<1e-12);
}
for(const check of soft.directionalChecks){
 const e=s=>soft.points.find(p=>p.gridLevel===check.gridLevel&&p.displacementNormAngstrom===s).energyHartree,h=check.displacementNormAngstrom,v=(e(h)+e(-h)-2*e(0))/((h/BOHR)**2);
 assert.ok(Math.abs(v-check.energyCurvatureEhPerBohr2)<1e-12);assert.ok(v<0,'Unresolved-mode negative curvature is retained, not hidden.');
}
const z=unzip(base+'/endpoints/forward/wavefunction.npz'),h=get(z,'hessian'),v=definition.cartesianUnitMode.flat();assert.deepEqual(h.shape,[16,16,3,3]);let curvature=0,residual=0;
for(let a=0;a<16;a++)for(let b=0;b<16;b++)for(let i=0;i<3;i++)for(let j=0;j<3;j++){const x=h.data[((a*16+b)*3+i)*3+j],y=h.data[((b*16+a)*3+j)*3+i];curvature+=v[3*a+i]*x*v[3*b+j];residual=Math.max(residual,Math.abs(x-y));}
assert.ok(curvature<0);assert.ok(residual<1e-4);assert.equal(report.endpoints.forward.minimumVerified,false);
const state=json('dist/reaction-lab/diels-alder/r2/execution-interruption.json');assert.equal(state.scientificOutcome,'incomplete');assert.equal(state.completedMethodCases,7);
console.log('PASS: independent saved-array reconstruction: '+matrices+' wavefunctions, '+retainedPoints+' documented IRC-attempt points, ZIP CRCs, electron counts, MO normalization, density Hermiticity and four negative energy curvatures. This does NOT establish a validated IRC.');

const adapter=json('dist/reaction-lab/diels-alder-system.json');assert.equal(adapter.validationR2.executionStatus,'interrupted');
