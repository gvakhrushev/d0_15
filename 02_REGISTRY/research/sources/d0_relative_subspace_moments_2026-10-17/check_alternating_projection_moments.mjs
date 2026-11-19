// Exact rational projector-history check; Node.js .mjs, no packages.
// Use: node check_alternating_projection_moments.mjs
// This verifies an independent 3D-in-6D fixture, NOT native D0 admission.
const gcd=(a,b)=>{while(b!==0n){let t=a%b;a=b;b=t;}return a<0n?-a:a;};
const r=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];};
const z=r(0),o=r(1);
const plus=(a,b)=>r(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>[-a[0],a[1]],minus=(a,b)=>plus(a,neg(b));
const mul=(a,b)=>r(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>r(a[0]*b[1],a[1]*b[0]);
const eq=(a,b)=>a[0]*b[1]===b[0]*a[1];
const str=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
const grid=(n,m,f)=>Array.from({length:n},(_,i)=>Array.from({length:m},(_,j)=>f(i,j)));
const id=n=>grid(n,n,(i,j)=>i===j?o:z);
const zero=(n,m)=>grid(n,m,()=>z);
const tp=A=>grid(A[0].length,A.length,(i,j)=>A[j][i]);
const dot=(A,B)=>grid(A.length,B[0].length,(i,j)=>A[i].reduce((v,x,k)=>plus(v,mul(x,B[k][j])),z));
const sum=(A,B)=>grid(A.length,A[0].length,(i,j)=>plus(A[i][j],B[i][j]));
const diff=(A,B)=>grid(A.length,A[0].length,(i,j)=>minus(A[i][j],B[i][j]));
const scale=(A,c)=>grid(A.length,A[0].length,(i,j)=>mul(A[i][j],c));
const tr=A=>A.reduce((v,row,i)=>plus(v,row[i]),z);
const power=(A,n)=>{let M=id(A.length);for(let i=0;i<n;i++)M=dot(M,A);return M;};
const matrixEq=(A,B)=>A.length===B.length&&A.every((row,i)=>row.every((a,j)=>eq(a,B[i][j])));
const diag=a=>grid(a.length,a.length,(i,j)=>i===j?a[i]:z);
const stack=(A,B)=>[...A,...B];
const pyth=u=>{
 const u2=mul(u,u),den=plus(o,u2);
 return {c:div(minus(o,u2),den),s:div(mul(r(2),u),den),
  dc:div(mul(r(-4),u),mul(den,den)),
  ds:div(mul(r(2),minus(o,u2)),mul(den,den))};
};
const assert=(b,msg)=>{if(!b)throw Error("EXACT-CONTROL FAILED: "+msg);checks++;};
let checks=0;
const u=[r(1,2),r(2,3),r(3,4)],du=[r(1,11),r(-1,13),z];
const c=u.map(x=>pyth(x).c),s=u.map(x=>pyth(x).s);
const dc=u.map((x,i)=>mul(pyth(x).dc,du[i]));
const ds=u.map((x,i)=>mul(pyth(x).ds,du[i]));
const Q=[[r(3,5),r(-4,5),z],[r(4,5),r(3,5),z],[z,z,o]];
const K=[[z,r(-1,11),z],[r(1,11),z,z],[z,z,z]];
const dQ=dot(Q,K);
const C=dot(diag(c),Q),dC=sum(dot(diag(dc),Q),dot(diag(c),dQ));
const J0=stack(id(3),zero(3,3)),J1=stack(tp(C),diag(s));
const dJ1=stack(tp(dC),diag(ds));
const P0=dot(J0,tp(J0)),P1=dot(J1,tp(J1));
const dP1=sum(dot(dJ1,tp(J1)),dot(J1,tp(dJ1)));
const F=diff(id(3),dot(tp(C),C));
const dF=scale(sum(dot(tp(dC),C),dot(tp(C),dC)),r(-1));
assert(matrixEq(dot(tp(J0),J0),id(3)),"J0 isometry");
assert(matrixEq(dot(tp(J1),J1),id(3)),"J1 isometry");
assert(matrixEq(sum(dot(tp(dJ1),J1),dot(tp(J1),dJ1)),zero(3,3)),"true isometry jet");
assert(matrixEq(dot(dot(tp(J0),diff(id(6),P1)),J0),F),"relative failure");
assert(matrixEq(scale(dot(dot(tp(J0),dP1),J0),r(-1)),dF),"moving P1 source");
assert(!matrixEq(dot(F,dF),dot(dF,F)),"genuine noncommuting source");
let L=J0,dL=zero(6,3);
const moments=[],derivatives=[];
for(let k=1;k<=6;k++){
 const T=k%2===1?diff(id(6),P1):P0;
 const dT=k%2===1?scale(dP1,r(-1)):zero(6,6);
 const old=L,oldD=dL;L=dot(T,old);
 dL=sum(dot(dT,old),dot(T,oldD));
 const actual=div(tr(dot(tp(L),L)),r(3));
 const expected=div(tr(power(F,k)),r(3));
 const actualJet=mul(r(2,3),tr(dot(tp(L),dL)));
 let source=zero(3,3);
 for(let a=0;a<k;a++)source=sum(source,dot(dot(power(F,a),dF),power(F,k-1-a)));
 const expectedJet=div(tr(source),r(3));
 assert(eq(actual,expected),"moment "+k);
 assert(eq(actualJet,expectedJet),"source "+k);
 moments.push(str(actual));
 derivatives.push(str(actualJet));
}
const output={status:"PASS",exact_controls:checks,ambient_dimension:6,
 input_dimension:3,alternating_prefix_lengths:[1,2,3,4,5,6],
 complete_outcome_complements:true,noncommuting_field_jet:true,
 moments,moving_source_derivatives:derivatives,
 is_native_d0_admission:false,is_original_gr_closure:false};
console.log(JSON.stringify(output));
