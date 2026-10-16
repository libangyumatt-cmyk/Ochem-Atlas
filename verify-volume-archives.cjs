'use strict';
// Validate full NPZ archives, including ZIP directories, deflate streams and CRCs.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const table=Array.from({length:256},(_,n)=>{let c=n;for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0;});
function crc32(b){let c=0xffffffff;for(const x of b)c=table[(c^x)&255]^(c>>>8);return (c^0xffffffff)>>>0;}
function verify(file){
 const b=fs.readFileSync(file);let end=-1;
 for(let i=b.length-22;i>=Math.max(0,b.length-65557);i--)if(b.readUInt32LE(i)===0x06054b50&&i+22+b.readUInt16LE(i+20)===b.length){end=i;break;}
 assert.ok(end>=0,file+': complete ZIP end record missing');
 const count=b.readUInt16LE(end+10),offset=b.readUInt32LE(end+16),size=b.readUInt32LE(end+12);assert.ok(count>0,file);assert.equal(offset+size,end,file+': central-directory bounds');let p=offset;
 for(let k=0;k<count;k++){
  assert.ok(p+46<=end,file);assert.equal(b.readUInt32LE(p),0x02014b50,file);const flags=b.readUInt16LE(p+8),method=b.readUInt16LE(p+10),crc=b.readUInt32LE(p+16),compressed=b.readUInt32LE(p+20),uncompressed=b.readUInt32LE(p+24),nameLen=b.readUInt16LE(p+28),extraLen=b.readUInt16LE(p+30),commentLen=b.readUInt16LE(p+32),local=b.readUInt32LE(p+42),name=b.subarray(p+46,p+46+nameLen).toString();
  assert.equal(flags&1,0,file+': encrypted member');assert.ok(local+30<=offset,file);assert.equal(b.readUInt32LE(local),0x04034b50,file);const data=local+30+b.readUInt16LE(local+26)+b.readUInt16LE(local+28);assert.ok(data+compressed<=offset,file+': incomplete member '+name);
  const packed=b.subarray(data,data+compressed),raw=method===8?zlib.inflateRawSync(packed):method===0?packed:null;assert.ok(raw,file+': unsupported ZIP method');assert.equal(raw.length,uncompressed,file+': member size '+name);assert.equal(crc32(raw),crc,file+': member CRC '+name);assert.ok(raw.subarray(0,6).equals(Buffer.from([147,78,85,77,80,89])),file+': NPY header '+name);p+=46+nameLen+extraLen+commentLen;
 }
 assert.equal(p,end,file+': directory entry count');return count;
}
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>{const p=path.join(dir,e.name);return e.isDirectory()?walk(p):p.endsWith('.npz')?[p]:[];});}
let members=0;const files=['dist/reaction-lab','dist/orbital-files'].flatMap(walk);for(const f of files)members+=verify(f);const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'ochem-npz-'));try{const raw=fs.readFileSync(files[0]),bad=path.join(tmp,'truncated.npz');fs.writeFileSync(bad,raw.subarray(0,Math.floor(raw.length/2)));assert.throws(()=>verify(bad),/ZIP end record/);const corrupt=Buffer.from(raw);corrupt[100]^=255;fs.writeFileSync(bad,corrupt);assert.throws(()=>verify(bad));}finally{fs.rmSync(tmp,{recursive:true});}console.log(`PASS: ${files.length} NPZ archives / ${members} arrays: ZIP directories, decompression, NPY headers and CRC integrity.`);
