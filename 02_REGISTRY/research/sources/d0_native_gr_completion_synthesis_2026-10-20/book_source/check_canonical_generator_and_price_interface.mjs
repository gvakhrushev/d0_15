// Exact bounded checker for CANONICAL_GENERATOR_AND_PRICE_INTERFACE.md.
// Standard ECMAScript only. All checks remain active; no assert elision.
function runCanonicalGeneratorChecks() {
  "use strict";
  const passed = [];
  function gcd(a,b) { a=a<0n?-a:a; b=b<0n?-b:b; while(b){const t=a%b;a=b;b=t;} return a; }
  function r(a,b=1n) { a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
  const R=x=>Array.isArray(x)?x:r(x);
  const add=(a,b)=>{a=R(a);b=R(b);return r(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);};
  const neg=a=>{a=R(a);return [-a[0],a[1]];};
  const sub=(a,b)=>add(a,neg(b));
  const mul=(a,b)=>{a=R(a);b=R(b);return r(a[0]*b[0],a[1]*b[1]);};
  const div=(a,b)=>{b=R(b);return mul(a,r(b[1],b[0]));};
  const eq=(a,b)=>{a=R(a);b=R(b);return a[0]===b[0]&&a[1]===b[1];};
  const sq=a=>mul(a,a);
  const sum=xs=>xs.reduce(add,r(0));
  const dot=(a,b)=>sum(a.map((x,i)=>mul(x,b[i])));
  const mat=a=>a.map(row=>row.map(R));
  const tr=a=>a[0].map((_,j)=>a.map(row=>row[j]));
  const mm=(a,b)=>{const bt=tr(b);return a.map(row=>bt.map(col=>dot(row,col)));};
  const mv=(a,v)=>a.map(row=>dot(row,v));
  const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>r(i===j?1:0)));
  const meq=(a,b)=>a.length===b.length&&a.every((row,i)=>row.length===b[i].length&&row.every((x,j)=>eq(x,b[i][j])));
  const veq=(a,b)=>a.length===b.length&&a.every((x,i)=>eq(x,b[i]));
  const scale=(a,c)=>a.map(row=>row.map(x=>mul(x,c)));
  const madd=(a,b)=>a.map((row,i)=>row.map((x,j)=>add(x,b[i][j])));
  const msub=(a,b)=>madd(a,scale(b,-1));
  const det2=a=>sub(mul(a[0][0],a[1][1]),mul(a[0][1],a[1][0]));
  const inv=a=>{
    const n=a.length,b=a.map((row,i)=>row.concat(eye(n)[i]));
    for(let k=0;k<n;k++){
      let i=k;while(i<n&&eq(b[i][k],0))i++;
      if(i===n)throw Error("singular matrix");
      [b[k],b[i]]=[b[i],b[k]];
      const pivot=b[k][k];b[k]=b[k].map(x=>div(x,pivot));
      for(let j=0;j<n;j++)if(j!==k){const f=b[j][k];b[j]=b[j].map((x,l)=>sub(x,mul(f,b[k][l])));}
    }
    return b.map(row=>row.slice(n));
  };
  function check(name,ok) { if(!ok)throw Error("FAIL: "+name);passed.push(name); }
  const T=mat([[0,1],[1,-1]]),A=mat([[1,-1],[-1,2]]),J=mat([[0,1],[-1,0]]);
  check("owned integer two-tick matrix",meq(mm(T,T),A));
  check("two-tick symplectic identity",meq(mm(mm(tr(A),J),A),J));
  const L=(q,Q)=>add(sub(div(sq(q),2),mul(q,Q)),sq(Q));
  const F=(q,P)=>div(sub(add(sq(q),mul(2,mul(q,P))),sq(P)),4);
  const q=r(3,7),p=r(-5,11),[Q,P]=mv(A,[q,p]);
  check("type-I input momentum",eq(sub(q,Q),p));
  check("type-I output momentum",eq(sub(q,mul(2,Q)),P));
  check("type-II exact Legendre value",eq(F(q,P),add(L(q,Q),mul(P,Q))));
  check("type-II input momentum",eq(div(add(q,P),2),p));
  check("type-II output coordinate",eq(div(sub(q,P),2),Q));
  check("omitted Legendre pairing is detected",!eq(F(q,P),L(q,Q)));
  const HL=mat([[1,-1],[-1,2]]),HF=scale(mat([[1,1],[1,-1]]),r(1,2));
  check("positive type-I Hessian by Sylvester",HL[0][0][0]>0n&&det2(HL)[0]>0n);
  check("indefinite type-II Hessian",det2(HF)[0]<0n);
  check("exact type-II eigenvalue square",meq(mm(HF,HF),scale(eye(2),r(1,2))));
  const m=r(2),n=r(-3),b=add(mul(2,m),n);
  const Qw=sub(Q,m),Pw=sub(P,n);
  const Lw=(q,Q)=>add(sub(L(q,Q),mul(m,q)),mul(b,Q));
  const Fw=(q,P)=>sub(sub(div(sq(q),2),mul(m,q)),div(sq(sub(sub(q,b),P)),4));
  check("winding input momentum",eq(sub(sub(q,Qw),m),p));
  check("winding output momentum",eq(sub(sub(q,mul(2,Qw)),b),Pw));
  check("winding partial Legendre value",eq(Fw(q,Pw),add(Lw(q,Qw),mul(Pw,Qw))));
  check("winding type-II input momentum",eq(sub(div(add(add(q,b),Pw),2),m),p));
  check("winding type-II output coordinate",eq(div(sub(sub(q,b),Pw),2),Qw));
  check("omitted winding term is detected",!eq(sub(q,Qw),p));
  const shear=h=>mat([[1,0],[neg(div(h,2)),1]]);
  const h0=r(2,3),h1=r(-4,5);
  const S0=shear(h0),S1=shear(h1),AH=mm(mm(S1,A),inv(S0));
  const z0=mv(S0,[q,p]),z1=mv(S1,[Q,P]);
  check("coframe shear is symplectic",meq(mm(mm(tr(S0),J),S0),J));
  check("endpoint-frame conjugated step",veq(mv(AH,z0),z1));
  check("sheared type-I input momentum",eq(sub(sub(q,Q),mul(div(h0,2),q)),z0[1]));
  check("sheared type-I output momentum",eq(sub(sub(q,mul(2,Q)),mul(div(h1,2),Q)),z1[1]));
  const qs=[r(-1,3),r(2,5),r(4,7),r(-2,9)];
  const hs=[r(0),r(2),r(-3,2),r(5,7)];
  const LH=(x,y,h,k)=>add(sub(L(x,y),div(mul(h,sq(x)),4)),div(mul(k,sq(y)),4));
  const base=sum(qs.slice(0,-1).map((x,i)=>L(x,qs[i+1])));
  const framed=sum(qs.slice(0,-1).map((x,i)=>LH(x,qs[i+1],hs[i],hs[i+1])));
  const boundary=sub(div(mul(hs[3],sq(qs[3])),4),div(mul(hs[0],sq(qs[0])),4));
  check("complete shear contribution telescopes",eq(sub(framed,base),boundary));
  check("every interior H coefficient cancels",[1,2].every(i=>eq(add(neg(div(sq(qs[i]),4)),div(sq(qs[i]),4)),0)));
  const wrong=sum(qs.slice(0,-1).map((x,i)=>add(L(x,qs[i+1]),div(mul(hs[i+1],sq(qs[i+1])),4))));
  check("one-sided frame omission is detected",!eq(sub(wrong,base),boundary));
  // Exact off-shell homogeneous fixture, with NONZERO history mixing:
  // t=e^2 x, w=1+z, H=1+2z, B=z^4, Theta=(e sqrt(1+Ht/w),x,z).
  const e=r(1),x=r(2),z=r(1),w=add(1,z),H=add(1,mul(2,z));
  const t=mul(sq(e),x),ratio=div(H,w),s=r(2),E=mul(e,s);
  check("coframe fixture exact positive square root",eq(sq(s),add(1,mul(ratio,t))));
  const Dt=[mul(2,mul(e,x)),sq(e),r(0)];
  const ratioZ=div(sub(mul(2,w),H),sq(w));
  const Ds=[div(mul(ratio,Dt[0]),mul(2,s)),div(mul(ratio,Dt[1]),mul(2,s)),div(mul(ratioZ,t),mul(2,s))];
  const D=mat([[add(s,mul(e,Ds[0])),mul(e,Ds[1]),mul(e,Ds[2])],[0,1,0],[0,0,1]]);
  const expectedD=mat([[r(7,2),r(3,8),r(1,8)],[0,1,0],[0,0,1]]);
  check("full coframe/history Jacobian",meq(D,expectedD));
  const oldPi=[r(5),r(7),r(11)],newPi=mv(tr(inv(D)),oldPi);
  check("full cotangent inverse transpose",veq(mv(tr(D),newPi),oldPi));
  for(let i=0;i<3;i++){
    const v=eye(3)[i];
    check("Liouville identity direction "+i,eq(dot(newPi,mv(D,v)),dot(oldPi,v)));
  }
  const Ay=mat([[D[0][0],D[0][1]],[0,1]]),C=[D[0][2],r(0)];
  const py=mv(tr(inv(Ay)),oldPi.slice(0,2));
  const pz=sub(oldPi[2],dot(C,py));
  check("explicit full history momentum correction",veq(newPi,py.concat([pz])));
  check("history correction is not zero",!eq(pz,oldPi[2]));
  const S=add(add(sq(sq(z)),mul(w,t)),mul(H,sq(t)));
  const Sbase=add(sq(sq(z)),mul(w,mul(sq(E),x)));
  check("exact actual normal-form value",eq(S,Sbase));
  const g0=[mul(2,mul(w,mul(E,x))),mul(w,sq(E)),add(mul(4,mul(sq(z),z)),mul(sq(E),x))];
  const factor=add(w,mul(2,mul(H,t)));
  const g=[mul(factor,Dt[0]),mul(factor,Dt[1]),add(add(mul(4,mul(sq(z),z)),t),mul(2,sq(t)))];
  check("complete source graph pullback",veq(mv(tr(D),g0),g));
  check("cotangent source graph transport",veq(mv(tr(inv(D)),g),g0));
  check("frozen history dressing loses actual source",!eq(g[2],g0[2]));
  const Dshell=mat([[1,r(1,2),0],[0,1,0],[0,0,1]]);
  const N=msub(Dshell,eye(3));
  check("shell shear nilpotent",meq(mm(N,N),scale(eye(3),0)));
  check("shell exact inverse I-N",meq(inv(Dshell),msub(eye(3),N)));
  return {
    status:"PASS", arithmetic:"exact BigInt rational", checks:passed.length,
    scope:"Algebraic local lift, full source cotangent transport; no native Book-price, field-writer, or GR-admission claim.",
    passed
  };
}
const canonicalGeneratorResult = runCanonicalGeneratorChecks();
if (typeof console !== 'undefined') console.log(JSON.stringify(canonicalGeneratorResult, null, 2));
canonicalGeneratorResult;