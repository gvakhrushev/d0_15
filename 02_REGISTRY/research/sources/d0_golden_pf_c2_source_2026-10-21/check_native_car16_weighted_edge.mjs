// Original CAR16 creator/contraction and true 2-node weighted stored shift.
// This is a bounded original-CAR layer diagnostic, NOT the whole L^4 Dirac.
const must=(x,s)=>{if(!x)throw Error("FAIL "+s)};
const order=[0,2,3,1],n=16,d=32;
const C=Array.from({length:n},()=>Array(n).fill(0));
const bit=order.indexOf(0);
for(let mask=0;mask<16;mask++){
  if(mask&(1<<bit))continue;
  let parity=0;
  for(let i=0;i<bit;i++)if(mask&(1<<i))parity^=1;
  C[mask|(1<<bit)][mask]=parity?-1:1;
}
must(C.flat().filter(x=>x!==0).length===8,"all8 original creation entries");
const transpose=A=>A[0].map((_,i)=>A.map(row=>row[i]));
const matmul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,i)=>s+v*B[i][j],0)));
const subtract=(A,B)=>A.map((row,i)=>row.map((x,j)=>x-B[i][j]));
const normF=A=>Math.sqrt(A.flat().reduce((s,v)=>s+v*v,0));
function Dirac(h,rhoPlus,rhoMinus){
  const alpha=Math.sqrt(rhoPlus/rhoMinus);
  const S=[[0,alpha],[1/alpha,0]],Sinv=S;
  const out=Array.from({length:32},()=>Array(32).fill(0));
  for(let site=0;site<2;site++)for(let target=0;target<2;target++){
    const coeff=(S[site][target]-(site===target?1:0))/h,
      coeffInv=(Sinv[site][target]-(site===target?1:0))/h;
    for(let i=0;i<n;i++)for(let j=0;j<n;j++)
      out[site*n+i][target*n+j]=coeff*C[i][j]+coeffInv*C[j][i];
  }
  return {out,S};
}
const rows=[];
for(const L of [8,16,32,64]){
  const h=1/L,delta=9*h**3,{out:D,S}=Dirac(h,1+delta,1-delta),
    {out:D0}=Dirac(h,1,1);
  const d=normF(subtract(D,D0));
  const Q=matmul(transpose(D),D),Q0=matmul(transpose(D0),D0);
  const q=normF(subtract(Q,Q0));
  must(d<1000*h*h&&q<1000*h,"literal original CAR operator rate");
  must(Math.abs(S[0][1]-S[1][0])>0,"true adjoint shift differs from inverse");
  rows.push({L,d_D_Frobenius:d,d_D_over_h2:d/(h*h),
             d_positive_quadratic_Frobenius:q,
             d_positive_quadratic_over_h:q/h});
}
function report(){return {status:"PASS_NATIVE_CAR16_TRUE_ADJOINT_PF_SCALE",
     original_mode_order:order,all_eight_creator_pairs:true,results:rows,
     scope:{full_4D_hjr_operator_checked:false,
            Book_info_selected:false,GR_closed:false}}}
if(typeof console!=="undefined")console.log(JSON.stringify(report(),null,2));
