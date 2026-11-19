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
const result={status:"PASS",exact_controls:checks,finite_cases:Ws.length*Ms.length,
 algebraic_ring:"Z[a]/(a^4+a^2-1)",golden_overlap:"sqrt(p)*I",
 full_output_field_source:"zero",original_GR_closed:false,
 full_native_programme_admission_of_spatial_comparison:false};
console.log(JSON.stringify(result));
