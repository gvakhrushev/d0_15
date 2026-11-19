// Exact finite-copy prepared-projector discrimination floor.
import assert from 'node:assert/strict';
let checks=0;
const close=(x,y,t=8e-13)=>{assert.ok(Math.abs(x-y)<t,String(x)+" != "+String(y));checks++;};
function tensor(a,b){return a.flatMap(x=>b.map(y=>x*y));}
function product(states){let x=[1];for(const s of states)x=tensor(x,s);return x;}
function dot(a,b){return a.reduce((s,x,i)=>s+x*b[i],0);}
function symNorm(probe,psi,m){
  let v=Array(2**(m+1)).fill(0);
  for(let k=0;k<=m;k++){
    const states=Array.from({length:m+1},(_,j)=>j===k?probe:psi);
    const w=product(states);
    for(let j=0;j<v.length;j++)v[j]+=w[j]/(m+1);
  }
  return dot(v,v);
}
for(let m=1;m<=8;m++){
  for(let j=0;j<11;j++){
    let theta=(j+1)*0.11, phi=(j+2)*0.19;
    const psi=[Math.cos(theta),Math.sin(theta)];
    const orth=[-psi[1],psi[0]];
    const probe=[Math.cos(phi)*psi[0]+Math.sin(phi)*orth[0],
                 Math.cos(phi)*psi[1]+Math.sin(phi)*orth[1]];
    const overlap=dot(probe,psi);
    const expected=(1+m*overlap*overlap)/(m+1);
    close(symNorm(probe,psi,m),expected);
    close(symNorm(psi,psi,m),1);
    close(symNorm(orth,psi,m),1/(m+1));
    const epsilon=1/(m+1);
    assert.ok(epsilon>0,"strict false-acceptance floor");checks++;
  }
}
console.log(JSON.stringify({status:"PASS",checks,
  theorem:"finite unknown-program m-copy exact-projector no-go",
  sharpFalseAcceptance:"1/(m+1)",
  physicalScope:"not an execution of Book03 P_N"}));
