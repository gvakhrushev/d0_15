#!/usr/bin/env node
"use strict";
/*
 * EXACT FULL PERIODIC 4D ROLE LINEARIZED FACE→LINK SOURCE INVERSE.
 *
 * At the flat original proper SO+(1,3) connection, linearize the
 * same authentic 4-link six-based plaquette:
 *   F_rs(x) = A_r(x)+A_s(x+r)-A_r(x+s)-A_s(x).
 *
 * For one Fourier mode z=(ω^kr) and q_r=z_r−1:
 *   F_rs = q_r A_s - q_s A_r,
 *   (d2 F)_rst = q_r F_st - q_s F_rt + q_t F_rs.
 *
 * For nonzero q choose j with q_j != 0, put A_j=0 and
 * A_mu=F_(j,mu)/q_j. This EXACTLY reconstructs the face field
 * iff d2F=0, modulo A→A+q*chi (one gauge).
 *
 * For q=0 no nonzero F is integrable on the periodic torus:
 * six global 2-fluxes (per Lie generator) must vanish.
 * However the flat global link mode A_mu(0) is NOT gauge:
 * four rooted Polyakov/Wilson loop tangents W_mu=L*A_mu(0)
 * recover it exactly. Thus the map (six faces, four Wilsons)
 * from original 4 Role links has kernel EXACTLY local
 * Lorentz gauge, over all finite periodic L4 test momenta.
 *
 * Dimension/rank PER Lorentz generator:
 * 4*256 role link inputs=1024;
 * rank d1=3(256−1)=765;
 * extra 4 Wilson tangent rank=4;
 * total rank769=1024−(256−1).
 * With 6 real SO generators: 4614 genuine source coordinates.
 *
 * Exact checks at 3 odd primes permitting primitive 4th root,
 * including all 256 Fourier modes and six independent Lie
 * input dimensions. No false generic-h small-divisor theorem:
 * this is L4 finite flat link-jet reconstruction. Nonlinear
 * near-identity local injectivity follows from the ordinary
 * analytic constant-rank/IFT after a true vertex-tree gauge,
 * BUT actual native field-to-Book selected source still OPEN.
 */
const require=(cond,msg)=>{if(!cond)throw Error("FAIL "+msg)};
const L=4,V=256,N=4,G=6;
const faces=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
  triples=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]];
function run(p){
 const md=n=>(n%p+p)%p,
       mult=(a,b)=>md(a*b),
       power=(a,n)=>{let r=1,b=md(a);while(n){if(n%2)r=mult(r,b);b=mult(b,b);n=Math.floor(n/2)}return r},
       inv=a=>{require(md(a)!==0,"division by 0");return power(a,p-2)};
 let root=0;
 for(let c=2;c<p;c++){
  const r=power(c,(p-1)/4);
  if(mult(r,r)===p-1){root=r;break}
 }
 require(root!==0,"no primitive fourth root");
 const powers=[1,root,p-1,md(-root)];
 function extFace(F,i,j){
  if(i===j)return 0;
  for(let f=0;f<faces.length;f++){
    const [a,b]=faces[f];
    if(i===a&&j===b)return F[f];
    if(i===b&&j===a)return md(-F[f]);
  }
  throw Error("invalid original ordered face");
 }
 const Fof=(q,A)=>faces.map(([r,s])=>
    md(mult(q[r],A[s])-mult(q[s],A[r])));
 const bianchi=(q,F)=>triples.map(([r,s,t])=>
    md(mult(q[r],extFace(F,s,t))
       -mult(q[s],extFace(F,r,t))
       +mult(q[t],extFace(F,r,s))));
 function inverseJet(q,F,globalWilson=null){
  let j=q.findIndex(v=>v!==0);
  if(j<0){
   require(F.every(x=>x===0),"original harmonic two-flux is not integrable");
   require(globalWilson!==null,"zero mode requires actual four rooted Wilson tangents");
   return globalWilson.map(w=>mult(w,inv(L)));
  }
  require(bianchi(q,F).every(x=>x===0),"not a closed authentic Role face");
  const A=Array(4).fill(0),qinv=inv(q[j]);
  for(let mu=0;mu<4;mu++)if(mu!==j)
    A[mu]=mult(extFace(F,j,mu),qinv);
  require(Fof(q,A).every((x,i)=>x===F[i]),"original pivot inverse failed");
  return A;
 }
 const stats={prime:p,root,nonzeroModes:0,zeroModes:0,
   roleLieSourcesReconstructed:0,nonzeroGaugeReconstructionErrors:0,
   nonzeroBianchiErrors:0,zeroFluxRejections:0,openCubeRejections:0,
   testedGlobalWilsonDirections:0};
 for(let k0=0;k0<4;k0++)for(let k1=0;k1<4;k1++)
  for(let k2=0;k2<4;k2++)for(let k3=0;k3<4;k3++){
   const indices=[k0,k1,k2,k3],
    q=indices.map(k=>md(powers[k]-1)),zero=indices.every(k=>k===0);
   if(zero)stats.zeroModes++;else stats.nonzeroModes++;
   for(let g=0;g<G;g++){
    const actualA=Array.from({length:4},(_,r)=>
      md((17+k0+3*k1+5*k2+7*k3)*(r+1)*(g+2)+41+g*g*r));
    const F=Fof(q,actualA);
    require(bianchi(q,F).every(x=>x===0),"d2 d1 not zero");
    const originalGlobalWilson=actualA.map(x=>mult(L,x));
    const reconstructed=inverseJet(q,F,zero?originalGlobalWilson:null);
    if(zero){
      require(reconstructed.every((x,i)=>x===actualA[i]),
        "four original noncontractible Wilson holonomies not recovered");
      stats.testedGlobalWilsonDirections+=4;
      const bad=[1,0,0,0,0,0];
      try{inverseJet(q,bad,originalGlobalWilson)}catch(e){stats.zeroFluxRejections++}
      continue;
    }
    const pivot=q.findIndex(x=>x!==0),sourceGauge=mult(actualA[pivot],inv(q[pivot]));
    const diff=actualA.map((x,i)=>md(x-reconstructed[i]));
    if(!diff.every((x,i)=>x===mult(q[i],sourceGauge)))
      stats.nonzeroGaugeReconstructionErrors++;
    // A face 2-form with exactly ONE nonzero component is generally
    // nonclosed when its transverse frequency component is nonzero.
    // Rather than guess which, test the d2 first.
    const raw=[1,0,0,0,0,0];
    if(bianchi(q,raw).some(x=>x!==0)){
      try{inverseJet(q,raw)}catch(e){stats.openCubeRejections++}
    }
    stats.roleLieSourcesReconstructed++;
   }
 }
 require(stats.nonzeroModes===255&&stats.zeroModes===1&&
    stats.roleLieSourcesReconstructed===255*G,
    "did not replay entire original Fourier four-Role face source");
 require(stats.nonzeroGaugeReconstructionErrors===0&&
  stats.testedGlobalWilsonDirections===24&&
  stats.zeroFluxRejections===6&&stats.openCubeRejections>500,
  "original Fourier face/Wilson inverse failed");
 return {...stats,
  linkLieDimensions:4*V*G,
  faceLieDimensions:6*V*G,
  faceRank:3*(V-1)*G,
  facePlusRootWilsonRank:(3*(V-1)+4)*G,
  pureVertexGaugeKernel:(V-1)*G,
  missingFaceCoherenceLieConstraints:(6*V-3*(V-1))*G,
  extraFourGlobalWilsonDirections:4*G,
  exactFlatRoleGaugeModuloReconstruction:true};
}
const samples=[1009,2017,65537].map(run);
const result={
 status:"PASS_ORIGINAL_FULL_PERIODIC_ROLE_FACE_PLUS_FOUR_WILSON_LOCAL_INVERSE",
 validAllThreeExactPrimeCases:samples.every(s=>s.exactFlatRoleGaugeModuloReconstruction),
 mathematicalRankPerOriginalSOGenerator:769,
 sixGeneratorTotalSourceRank:4614,
 originalNativeUnderlyingChart:"L4 4D Golden LEFT Role link/faces, not scene K913 33-vertex connection",
 physicalSufficiency:"Must recover all original local based face matrices plus four rooted noncontractible role Wilson holonomies, with true real coframe/reference and native paid programme; actual G0/Book compulsory action NOT selected",
 GR_closed:false,
 samples
};
console.log(JSON.stringify(result,null,2));
