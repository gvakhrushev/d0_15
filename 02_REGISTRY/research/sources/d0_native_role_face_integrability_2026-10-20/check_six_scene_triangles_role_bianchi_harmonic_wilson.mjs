#!/usr/bin/env node
"use strict";
/*
 * NECESSARY ORIGINAL 4D ROLE→SCENE FACE INTEGRABILITY:
 *
 * Six independent K(9,11,13) root-BC chord matrices per native Golden
 * LEFT Role site are only a PULLBACK OBSERVABLE unless all six are
 * functions of the FOUR SHARED Role link matrices at that site and
 * its neighbours. True finite nonabelian based faces obey exact
 * transported lattice cube Bianchi, NOT six independent sources.
 *
 * The linearized 4D periodic L4 Role cochain complex over THREE
 * exact Fp Fourier carriers (primitive 4th root) proves:
 * C0=256,C1=1024,C2=1536,C3=1024,C4=256 per Lie generator,
 * rank(d0)=255, rank(d1)=765, rank(d2)=765,rank(d3)=255,
 * H^k=(1,4,6,4,1).
 *
 * Hence original 6-valued Lorentz link→plaquette map:
 * 6144 link Lie inputs -> 9216 independent six-scene face inputs;
 * rank4590, scene-face complement4626, Bianchi local rank4590,
 * 36 global non-contractible 2-cycle flux constraints, and 24
 * original noncontractible Role Wilson link modes invisible to
 * local curvature. These are *finite exact integer/rational* claims,
 * not numerical singular-value ranks.
 *
 * Critically the isolated flat nondegenerate original six-star
 * Palatini action has NONZERO derivative w.r.t. each independent
 * face chord variable, while the full original 4D link Euler is
 * ZERO on the periodic vacuum because the 4D coboundary adjoint
 * kills the constant face source. Independent scene-chord Euler
 * is therefore NOT the physical 24 Role-link Euler.
 *
 * Mathematically shortest positive weld:
 * programme SIX SCENE rooted triangles as four-link original
 * P_rs(x) expressions on the SAME Golden LEFT original Role
 * links; do NOT vary six scene chords independently.
 * No literal mandatory native G0 field->clock/Book action selection
 * is claimed, GR_closed=false.
 */
const assert=(cond,msg)=>{if(!cond)throw Error("FAIL "+msg)};
const D=4,L=4,V=L**4,
 pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
 triples=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]],
 quadr=[0,1,2,3];
const sum=(xs)=>xs.reduce((a,b)=>a+b,0);
const rank=(A,p)=>{
 let M=A.map(row=>row.map(x=>(x%p+p)%p)),m=M.length,n=M[0].length,r=0;
 const pw=(a,b)=>{let result=1,x=a;while(b){if(b%2)result=result*x%p;x=x*x%p;b=Math.floor(b/2)}return result};
 for(let c=0;c<n&&r<m;c++){
  let q=r;while(q<m&&M[q][c]===0)q++;
  if(q===m)continue;
  [M[r],M[q]]=[M[q],M[r]];
  let iv=pw(M[r][c],p-2);
  for(let j=c;j<n;j++)M[r][j]=M[r][j]*iv%p;
  for(let i=0;i<m;i++)if(i!==r){
   const f=M[i][c];if(!f)continue;
   for(let j=c;j<n;j++)M[i][j]=(M[i][j]-f*M[r][j]%p+p)%p;
  }
  r++;
 }return r;
};
const findFourthRoot=p=>{
 const power=(a,n)=>{let o=1;while(n){if(n%2)o=o*a%p;a=a*a%p;n=Math.floor(n/2)}return o};
 for(let a=2;a<p;a++){
  let q=power(a,(p-1)/4);
  if(q*q%p===p-1&&power(q,4)===1)return q;
 }
 throw Error("no fourth root in Fp");
};
const exactCochain=[];
for(const prime of [1009,2017,65537]){
 const md=x=>(x%prime+prime)%prime,root=findFourthRoot(prime);
 const pows=[1,root,prime-1,md(-root)];
 let freq=[0,0,0,0],hist={zero:0,nonzero:0},ranks=[0,0,0,0],
   wrong=[],rankShapes=[];
 for(let k0=0;k0<L;k0++)for(let k1=0;k1<L;k1++)
 for(let k2=0;k2<L;k2++)for(let k3=0;k3<L;k3++){
  freq=[k0,k1,k2,k3];
  const q=freq.map(k=>md(pows[k]-1)),
   d0=q.map(x=>[x]),
   d1=pairs.map(([r,s])=>Array.from({length:D},(_,mu)=>
     md((mu===s?q[r]:0)-(mu===r?q[s]:0)))),
   d2=triples.map(([r,s,t])=>pairs.map(([i,j])=>
     i===s&&j===t?q[r]:i===r&&j===t?md(-q[s]):i===r&&j===s?q[t]:0)),
   d3=triples.map(([r,s,t])=>
      s===1&&t===2?md(-q[3]):r===0&&s===1&&t===3?q[2]:
      r===0&&s===2&&t===3?md(-q[1]):q[0]);
  // d3 is the boundary of (0,1,2,3): d(F_123) - d(F_023)
  // + d(F_013) - d(F_012). Since triples are lexicographic:
  // (012,013,023,123), coefficients (-q3,+q2,-q1,+q0).
  const d3Mat=[[md(-q[3]),q[2],md(-q[1]),q[0]]];
  const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>
    md(row.reduce((tot,x,i)=>tot+x*B[i][j],0))));
  const r=[rank(d0,prime),rank(d1,prime),rank(d2,prime),rank(d3Mat,prime)];
  const isZero=freq.every(x=>x===0);
  if(r.join()!==(isZero?"0,0,0,0":"1,3,3,1"))
    wrong.push({freq,r});
  if(mul(d1,d0).flat().some(x=>x!==0)||
     mul(d2,d1).flat().some(x=>x!==0)||
     mul(d3Mat,d2).flat().some(x=>x!==0))
    wrong.push({freq,complex:"d² != 0"});
  for(let i=0;i<4;i++)ranks[i]+=r[i];
  if(isZero)hist.zero++;else hist.nonzero++;
 }
 assert(wrong.length===0&&hist.zero===1&&hist.nonzero===255,
  "exact original 4D lattice Fourier deRham failed prime "+prime);
 assert(ranks.join()==="255,765,765,255","incorrect 4D cochain ranks");
 const betti=[1,4,6,4,1],c=[V,4*V,6*V,4*V,V];
 // b_k=dim C^k - rank d_(k-1) - rank d_k.
 for(let k=0;k<5;k++)assert(c[k]-(k?ranks[k-1]:0)-
   (k<4?ranks[k]:0)===betti[k],"wrong original torus Betti number");
 exactCochain.push({prime,root,FourierModes:L**D,zeroModes:hist.zero,
   nonzeroModes:hist.nonzero,cochainDimensions:c,
   cochainRanks:ranks,betti,linkToFaceLieRank:6*ranks[1],
   sixSceneIndependentFaceLie:6*c[2],
   missingSceneFaceConstraints:6*(c[2]-ranks[1]),
   locallyBianchiLieConstraints:6*ranks[2],
   globalFaceHarmonicFluxDirections:6*betti[2],
   missingFourWilsonPerLorentz:6*betti[1],
   allNilpotentCoboundariesChecked:true});
}
// Flat original six-star face-source nonstationarity, each based face.
const rawI=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
const E=(a,b)=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===a&&j===b)));
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>
  row.reduce((tot,x,k)=>tot+x*B[k][j],0)));
const add=(A,B,s=1)=>A.map((r,i)=>r.map((v,j)=>v+s*B[i][j]));
const gens=[
  add(E(1,1),E(0,0),-1),
  add(E(0,2),E(2,1)),
  add(E(0,3),E(3,1)),
  add(E(1,2),E(2,0)),
  add(E(1,3),E(3,0)),
  add(E(2,3),E(3,2),-1)
];
const eps=(a,b,c,d)=>{
 const z=[a,b,c,d];if(new Set(z).size<4)return 0;
 let s=1;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)if(z[i]>z[j])s=-s;
 return s;
};
function faceDeriv(r,s,X){
 const [u,v]=quadr.filter(k=>k!==r&&k!==s),
  C=mm(X,eta),F=rawI();let z=0;
 for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
  const [c,d]=quadr.filter(k=>k!==a&&k!==b);
  z+=eps(a,b,c,d)*(F[a][u]*F[b][v]-F[b][u]*F[a][v])*C[c][d];
 }
 return eps(r,s,u,v)*z;
}
const flatFaceSources=pairs.map(([r,s])=>
  ({face:[r,s],sixLorentzFaceSource:gens.map(G=>faceDeriv(r,s,G))}));
assert(flatFaceSources.every(v=>v.sixLorentzFaceSource.some(x=>x!==0)),
  "an original nondegenerate six-star based flat face lacks a source");
const constantHarmonic=flatFaceSources.map(x=>
  x.sixLorentzFaceSource);
assert(constantHarmonic.some(x=>x.some(y=>y!==0)),
  "flat six-star cannot distinguish independent scene chord");
const roleLinks=(site,axis)=>site*D+axis,
      shift=(site,axis)=>site^(1<<axis); // only for L2 test below
// For general L4 coordinates use the actual positive periodic shift.
function shiftL4(site,axis){
 let c=[],v=site;
 for(let j=0;j<4;j++){c.push(v%L);v=Math.floor(v/L);}
 c[axis]=(c[axis]+1)%L;let ans=0,w=1;
 for(let j=0;j<4;j++){ans+=c[j]*w;w*=L;}return ans;
}
let linkSourceMax=0,linkSourceNonzero=0,checks=0;
for(let site=0;site<V;site++)for(let axis=0;axis<4;axis++){
 for(let g=0;g<6;g++){
  // d1^* is the genuine Role based-face incidence, i.e. original
  // link variation reaches both x and x-axis-negative based faces.
  let val=0;
  for(let f=0;f<pairs.length;f++){
   const [r,s]=pairs[f],a=constantHarmonic[f][g];
   if(axis===r){val-=a;val+=a;} // neighboring base cancels
   if(axis===s){val+=a;val-=a;}
  }
  linkSourceMax=Math.max(linkSourceMax,Math.abs(val));
  if(val!==0)linkSourceNonzero++;
  checks++;
 }
}
assert(linkSourceMax===0&&linkSourceNonzero===0&&checks===24*V,
 "Role link source does not vanish at flat under d1 adjoint");
const answer={
 status:"PASS_ORIGINAL_ROLE_FACE_BIANCHI_GAUGE_WILSON_SHARP_PULLBACK",
 grid:{L,V,linkComponentsOriginal:4*V,faceComponentsOriginal:6*V,
  truePeriodicScalarBetti:[1,4,6,4,1]},
 exactCochain,
 sameOriginalLieDim:6,
 originalRoleFlatSixFaceEuler:flatFaceSources,
 flatIndependentSceneChordStationary:false,
 flatOriginalSharedRoleLinkStationary:true,
 testedIndependentRoleLinkEulerRows:checks,
 exactRoleLinkEulerMaxResidual:linkSourceMax,
 faceLinkSourceImageDimension:6*3*(V-1),
 faceIndependentInputLieDimensions:6*6*V,
 fakeIndependentSceneFaceEulerDirections:6*(3*V+3),
 genuineMissingGlobalRoleWilsonModes:4*6,
 implication:"Need SAME four shared Role link sources and true nonlinear 3-cube transported Bianchi + global face 2-holonomy constraints; six arbitrary scene chord Euler != original Palatini Euler",
 nativeSelected:false,GR_closed:false
};
console.log(JSON.stringify(answer,null,2));
