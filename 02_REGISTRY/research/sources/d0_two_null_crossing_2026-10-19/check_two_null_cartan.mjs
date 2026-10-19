#!/usr/bin/env node
// Bounded exact-dyadic 2-jet and torsion checks for the double-null
// coframe. No native programme, Book price, or finite all-40 closure implied.
// Coordinates (u,v,x,y); internal frame (+,-,2,3); eta=(+ - offdiag,-,-).
import assert from 'node:assert/strict';

const n=4, Z=()=>Array.from({length:n},()=>Array(n).fill(0));
const E=(a,b)=>{let M=Z();M[a][b]=1;return M};
const add=(A,B)=>A.map((r,i)=>r.map((v,j)=>v+B[i][j]));
const sc=(A,t)=>A.map(r=>r.map(v=>v*t));
const N=[add(E(1,2),E(2,0)),add(E(1,3),E(3,0))];
const M=[add(E(0,2),E(2,1)),add(E(0,3),E(3,1))];
const Boost=add(E(1,1),sc(E(0,0),-1));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const near=(a,b)=>Math.abs(a-b)<1e-11;

function cartanTorsion(H,J,A,B) {
  const Omega=1-H*J/4;assert.ok(Omega!==0);
  const e=[[1,J/2,0,0],[H/2,1,0,0],[0,0,1,0],[0,0,0,1]];
  // Spin-connection coefficients in the coframe basis, obtained via Koszul.
  const wb=[Z(),Z(),Z(),Z()];
  for(let i=0;i<2;i++){
    const a=A[i]/(2*Omega),b=B[i]/(2*Omega);
    const c=-(H*B[i]+J*A[i])/(8*Omega);
    const d=(J*A[i]-H*B[i])/(8*Omega);
    wb[0]=add(wb[0],add(sc(N[i],a),sc(M[i],c)));
    wb[1]=add(wb[1],add(sc(N[i],c),sc(M[i],b)));
    wb[i+2]=add(wb[i+2],sc(Boost,d));
  }
  const wc=Array.from({length:n},(_,mu)=>wb.reduce((acc,Q,k)=>add(acc,sc(Q,e[k][mu])),Z()));
  const de=(a,mu,nu)=>{
    if(a===0&&mu===1&&nu>=2)return -B[nu-2]/2;
    if(a===1&&mu===0&&nu>=2)return -A[nu-2]/2;
    return 0;
  };
  for(let mu=0;mu<n;mu++)for(let nu=mu+1;nu<n;nu++)for(let a=0;a<n;a++){
    let T=de(a,mu,nu);
    for(let b=0;b<n;b++)T+=wc[mu][a][b]*e[b][nu]-wc[nu][a][b]*e[b][mu];
    assert.ok(near(T,0), 'torsion ('+[a,mu,nu]+')='+T);
  }
  return Omega;
}

// Exact local two-jet of metric with H=A_x x+A_y y and
// J=B_x x+B_y y, evaluated at H=J=x=y=0.
// First derivatives dg and mixed second derivative of g_uv completely
// determine connection derivative and Riemann. All coefficients are dyadic,
// so these fixtures are exact in IEEE double at the designated point.
function crossingJet(A,B){
  const dg=Array.from({length:n},()=>Array.from({length:n},()=>Array(n).fill(0)));
  const ddg=Array.from({length:n},()=>Array.from({length:n},()=>Array.from({length:n},()=>Array(n).fill(0))));
  for(let i=0;i<2;i++){
    dg[i+2][0][0]=A[i];dg[i+2][1][1]=B[i];
    for(let j=0;j<2;j++){
      const v=(A[i]*B[j]+A[j]*B[i])/4;
      ddg[i+2][j+2][0][1]=v;
      ddg[i+2][j+2][1][0]=v;
    }
  }
  const dgi=Array.from({length:n},()=>Array.from({length:n},()=>Array(n).fill(0)));
  for(let p=0;p<n;p++)for(let a=0;a<n;a++)for(let b=0;b<n;b++)
    for(let c=0;c<n;c++)for(let d=0;d<n;d++)
      dgi[p][a][b]-=eta[a][c]*dg[p][c][d]*eta[d][b];

  const Gam=Array.from({length:n},()=>Array.from({length:n},()=>Array(n).fill(0)));
  const dGam=Array.from({length:n},()=>Array.from({length:n},()=>Array.from({length:n},()=>Array(n).fill(0))));
  for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let c=0;c<n;c++)for(let t=0;t<n;t++){
    const V=dg[b][t][c]+dg[c][t][b]-dg[t][b][c];
    Gam[a][b][c]+=eta[a][t]*V/2;
    for(let p=0;p<n;p++)
      dGam[p][a][b][c]+=(dgi[p][a][t]*V+
         eta[a][t]*(ddg[p][b][t][c]+ddg[p][c][t][b]-ddg[p][t][b][c]))/2;
  }
  const R=Array.from({length:n},()=>Array.from({length:n},()=>Array.from({length:n},()=>Array(n).fill(0))));
  const Ric=Z();
  for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let c=0;c<n;c++)for(let d=0;d<n;d++){
    let val=dGam[c][a][d][b]-dGam[d][a][c][b];
    for(let k=0;k<n;k++)val+=Gam[a][c][k]*Gam[k][d][b]-Gam[a][d][k]*Gam[k][c][b];
    R[a][b][c][d]=val;
    if(a===c)Ric[b][d]+=val;
  }
  const dual=[1,0,2,3],sgn=[1,1,-1,-1];
  const lower=(a,b,c,d)=>sgn[a]*R[dual[a]][b][c][d];
  let K=0;
  for(let a=0;a<n;a++)for(let b=0;b<n;b++)
    for(let c=0;c<n;c++)for(let d=0;d<n;d++)
      K+=lower(a,b,c,d)*lower(dual[a],dual[b],dual[c],dual[d])*
         sgn[a]*sgn[b]*sgn[c]*sgn[d];
  const dot=A[0]*B[0]+A[1]*B[1],wedge=A[0]*B[1]-A[1]*B[0];
  for(let i=0;i<n;i++)for(let j=0;j<n;j++){
    const expect=((i===0&&j===1)||(i===1&&j===0))?-dot/4:0;
    assert.ok(near(Ric[i][j],expect), 'Ric '+i+','+j);
  }
  assert.ok(near(R[2][3][0][1],wedge/4));
  assert.ok(near(R[0][0][2][3],wedge/4));
  assert.ok(near(K,(dot*dot-3*wedge*wedge)/4));
  return {dot,wedge,Ric_uv:Ric[0][1],R_xyuv:R[2][3][0][1],K};
}

const tests=[
 [[1,0],[0,1]],[[1,0],[1,0]],[[1,0],[1,1]],
 [[1,1],[1,-1]],[[1,2],[3,4]],[[2,-3],[-4,5]],
 [[1,0],[0,0]],[[0,0],[0,1]],
];
for(const [A,B] of tests)crossingJet(A,B);
for(const [H,J,A,B] of [
 [0.4,0.5,[2,-1],[3,1]],
 [1,0.8,[-2.6,1.1],[2.3,-4]],
 [-1,0.2,[0,3],[-6,8]],
 [0.4,0,[2,-1],[0,0]],
 [0,0.7,[0,0],[3,2]]
])cartanTorsion(H,J,A,B);
const pure=crossingJet([1,0],[0,1]);
assert.equal(pure.Ric_uv,0);
assert.equal(pure.R_xyuv,1/4);
assert.equal(pure.K,-3/4);
console.log('PASS: 24 torsion rows on all bounded fixtures');
console.log('PASS: exact dyadic metric 2-jet, mixed Ricci/Weyl and Kretschmann');
console.log('PASS: two affine flat branches produce local Ricci-free curved crossing');
console.log('SCOPE: continuum Cartan and exact point jets; NOT finite full-40, native admission, or global GR.');
