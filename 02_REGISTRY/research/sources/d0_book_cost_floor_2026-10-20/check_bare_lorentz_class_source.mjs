// D0 original Lorentz source gate: class function bare link vs covariant coframe bivector.
// Pure exact integer 4x4 matrix identities; no physical full128 action selection.
const run=function run(){
 const eta=[1,-1,-1,-1], P=[1,-1,-1,1];
 const J=Array.from({length:4},()=>Array(4).fill(0));J[2][3]=1;J[3][2]=-1;
 const need=(ok,why)=>{if(!ok)throw Error(why)};
 const detP=P.reduce((a,b)=>a*b,1);
 need(detP===1 && P[0]===1,"proper time-oriented frame");
 for(let i=0;i<4;i++)for(let j=0;j<4;j++){
   if(i===j)need(P[i]*eta[i]*P[j]===eta[i],"metric conservation");
   need(P[i]*J[i][j]*P[j]===-J[i][j],"J23 odd under conjugation");
   const skew=J[j][i]*eta[j]+eta[i]*J[i][j];
   need(skew===0,"so(1,3) generator");
 }
 let trJ2=0;for(let i=0;i<4;i++)for(let k=0;k<4;k++)trJ2+=J[i][k]*J[k][i];
 need(trJ2===-2,"J23 trace normalization");
 const bivectorPair=-trJ2/2;
 need(bivectorPair===1,"coframe bivector paired source");
 return {status:"PASS_LORENTZ_CLASS_FUNCTION_FIRST_J23_SOURCE_ZERO",conjugacy:"P exp(t J23) P^-1 = exp(-t J23)",P,metric:"diag(+---)",detP,trJ2,bivectorPair};
};
console.log(JSON.stringify(run(),null,2));
