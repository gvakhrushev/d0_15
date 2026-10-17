// Exact golden native-port control in Z[a]/(a^4+a^2-1).
// Run: node check_native_port_only.mjs (no dependencies).
// This is a finite algebraic control of the GENERAL proof, not native GR closure.
const zero=[0n,0n,0n,0n],one=[1n,0n,0n,0n],
      a=[0n,1n,0n,0n],p=[0n,0n,1n,0n];
const add=(x,y)=>x.map((v,i)=>v+y[i]);
const neg=x=>x.map(v=>-v);
const sub=(x,y)=>add(x,neg(y));
function mul(x,y){
 const c=Array(7).fill(0n);
 for(let i=0;i<4;i++)for(let j=0;j<4;j++)c[i+j]+=x[i]*y[j];
 for(let k=6;k>=4;k--){c[k-4]+=c[k];c[k-2]-=c[k];}
 return c.slice(0,4);
}
const eq=(x,y)=>x.every((v,i)=>v===y[i]);
const grid=(n,m,f)=>Array.from({length:n},(_,i)=>
 Array.from({length:m},(_,j)=>f(i,j)));
const I=n=>grid(n,n,(i,j)=>i===j?one:zero);
const Z=(n,m)=>grid(n,m,()=>zero);
const T=A=>grid(A[0].length,A.length,(i,j)=>A[j][i]);
const dot=(A,B)=>grid(A.length,B[0].length,(i,j)=>
 A[i].reduce((z,v,k)=>add(z,mul(v,B[k][j])),zero));
const plus=(A,B)=>grid(A.length,A[0].length,(i,j)=>add(A[i][j],B[i][j]));
const minus=(A,B)=>grid(A.length,A[0].length,(i,j)=>sub(A[i][j],B[i][j]));
const scale=(A,v)=>grid(A.length,A[0].length,(i,j)=>mul(A[i][j],v));
const matrixEq=(A,B)=>A.length===B.length&&
 A.every((row,i)=>row.every((v,j)=>eq(v,B[i][j])));
const stack=(A,B)=>[...A,...B];
const hcat=(A,B)=>A.map((r,i)=>[...r,...B[i]]);
const psq=mul(p,p),amp=mul(a,p);
const Ws=[
 grid(4,4,(i,j)=>i+j===3?one:zero),
 grid(4,4,(i,j)=>i===j?(i%2===0?one:neg(one)):zero),
 I(4)
];
const Ms=[
 grid(4,2,(i,j)=>i===j?a:(i===j+2?p:zero)),
 grid(4,2,(i,j)=>i===j+2?a:(i===j?p:zero))
];
const port=stack(hcat(scale(I(4),a),scale(I(4),neg(p))),
                 hcat(scale(I(4),p),scale(I(4),a)));
const assert=(yes,msg)=>{if(!yes)throw Error("EXACT GOLDEN CONTROL FAILED: "+msg);checks++;};
let checks=0;
assert(eq(add(mul(p,p),p),one),"p+p²=1 in quartic ring");
for(let wi=0;wi<Ws.length;wi++)for(let mi=0;mi<Ms.length;mi++){
 const W=Ws[wi],pre=Ms[mi];
 const K0=plus(scale(I(4),p),scale(W,psq));
 const K1=scale(minus(W,I(4)),amp);
 const J=stack(dot(K0,pre),dot(K1,pre));
 const norms=plus(dot(T(K0),K0),dot(T(K1),K1));
 const skew=minus(dot(T(K0),K1),dot(T(K1),K0));
 const C=dot(dot(T(J),port),J);
 assert(matrixEq(dot(T(pre),pre),I(2)),"pre-port isometry "+wi+","+mi);
 assert(matrixEq(norms,I(4)),"complete Kraus "+wi+","+mi);
 assert(matrixEq(skew,Z(4,4)),"native port cross skew "+wi+","+mi);
 assert(matrixEq(dot(T(J),J),I(2)),"full record isometry "+wi+","+mi);
 assert(matrixEq(C,scale(I(2),a)),"whole golden-port overlap "+wi+","+mi);
}

// Fixed *signed* output-port contrast of two golden-branch full images.
// Unlike the SO(2) port rotation, its cross overlap is nontrivial.
const signPort=grid(8,8,(i,j)=>i===j?(i<4?one:neg(one)):zero);
const p3=mul(a,amp),p5=mul(psq,p3),twoPsq=add(psq,psq);
let signedCases=[];
for(let wi=0;wi<Ws.length;wi++)for(let mi=0;mi<Ms.length;mi++){
 const W=Ws[wi],pre=Ms[mi];
 const K0=plus(scale(I(4),p),scale(W,psq));
 const K1=scale(minus(W,I(4)),amp);
 const J=stack(dot(K0,pre),dot(K1,pre));
 const E1=dot(dot(T(pre),dot(T(K1),K1)),pre);
 const C=minus(I(2),scale(E1,twoPsq));
 const J0aug=stack(scale(J,a),scale(J,p));
 const J1aug=stack(scale(J,a),scale(dot(signPort,J),p));
 const overlap=dot(T(J1aug),J0aug);
 assert(matrixEq(dot(T(J0aug),J0aug),I(2)),"full branched record 0 isometry "+wi+","+mi);
 assert(matrixEq(dot(T(J1aug),J1aug),I(2)),"full branched record 1 isometry "+wi+","+mi);
 assert(matrixEq(overlap,C),"signed port cross operator "+wi+","+mi);
 assert(matrixEq(minus(C,scale(I(2),p3)),scale(minus(I(2),E1),twoPsq)),
         "strict golden source gap "+wi+","+mi);
 signedCases.push({wi,mi,nontrivial:!matrixEq(E1,Z(2,2)),
                   E1,C});
}
// genuine first source from changing the pre-port geometry, W fixed
const W=Ws[0],pre=Ms[0],K1=scale(minus(W,I(4)),amp);
const hcat0=grid(4,4,(i,j)=>i===0&&j===2?one:
                                   i===2&&j===0?neg(one):zero);
const dpre=dot(hcat0,pre),H=dot(T(K1),K1);
const E1=dot(dot(T(pre),H),pre);
const dE1=plus(dot(dot(T(dpre),H),pre),dot(dot(T(pre),H),dpre));
const C=minus(I(2),scale(E1,twoPsq)),dC=scale(dE1,neg(twoPsq));
const ddet=sub(add(mul(dC[0][0],C[1][1]),mul(C[0][0],dC[1][1])),
               add(mul(dC[0][1],C[1][0]),mul(C[0][1],dC[1][0])));
assert(!eq(ddet,zero),"nonzero native-compressed signed price first source");
assert(signedCases.some(c=>c.nontrivial)&&signedCases.some(c=>!c.nontrivial),
       "curved versus zero literal W control");
assert(!matrixEq(signedCases[0].C,signedCases[2].C),
       "not a constant port-only scalar");
const result={status:"PASS",exact_controls:checks,finite_cases:signedCases.length,
  algebraic_ring:"Z[a]/(a^4+a^2-1)",
  positive_comparison:"C_signed=I-2p^2 E_port1",
  universal_lower_bound:"p^3 I <= C_signed <= I",
  exact_full_port_effect:"E_port1=p epsilon Delta",
  exact_native_source:"d C_signed=-2p^2 d E_port1",
  nonzero_first_source_witness:ddet.map(String),
  old_record_phase_admitted:false,
  physical_Cost_Info_selected:false,
  GR_hm2_terminal_closed:false};
console.log(JSON.stringify(result));
