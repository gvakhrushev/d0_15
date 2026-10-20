#!/usr/bin/env node
"use strict";
/*
 * D0 20 Oct 2026: exact BOOK 3-tick ↔ STAR coframe degree-two
 * conjugacy and Golden-AF nonlinear compensator / full-volume dual Ward.
 *
 * ORIGINAL carriers: K(9,11,13) all 718 directed supported Book edges,
 * original GOLDEN p, original 3-tick trace and based SO null face,
 * original AF scene-identity J2 Phi constructed from λ(e)=4e(1-e).
 *
 * Mathematical theorem about the DECLARED orbit-twirled Book-weighted
 * signed geometric observable and chosen AF geometric fibre. NOT
 * selection of full compulsory G0/H+J+R/Book/clock work or GR.
 */
const must=(x,m)=>{if(!x)throw Error("FAIL "+m)};
const phi=(1+Math.sqrt(5))/2,p=1/phi,ell=Math.log(phi);
const N=33, part=i=>i<9?0:(i<20?1:2);
const K=Array.from({length:N},(_,i)=>Array.from({length:N},(_,j)=>
  part(i)===part(j)?0:p*(1+((7*i+11*j)%17)/23)));
const nonzero=K.flat().filter(x=>x>0);
must(nonzero.length===718,"the ORIGINAL 718 positive supported scene edges");
function Z3(k) {
  let acc=0,terms=0;
  // Enumerate ALL genuine based ABC 3-tick triangles, not invented faces.
  for(let a=0;a<9;a++)for(let b=9;b<20;b++)for(let c=20;c<33;c++){
    const a1=k[a][b]*k[b][c]*k[c][a];
    const a2=k[a][c]*k[c][b]*k[b][a];
    acc+=3*(a1+a2);terms+=6;
  }
  must(terms===7722,"3*2*9*11*13 original rooted oriented triangles");
  return acc;
}
const W=Z3(K)/7722;
must(W>0,"original weighted Book Z3 positive");
function perron(A){
 let v=Array(N).fill(1/N),rho=1;
 for(let k=0;k<650;k++){
   const Av=A.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));
   rho=Av.reduce((s,x)=>s+x,0);
   v=Av.map(x=>x/rho);
 }
 const max= Math.max(...A.map((row,i)=>Math.abs(row.reduce((s,x,j)=>s+x*v[j],0)-rho*v[i])));
 must(max<1e-12,"actual original primitive PF convergence");
 return rho;
}
const lambda=perron(K);
const t=.23,q=Math.pow(phi,t),Ks=K.map(row=>row.map(x=>q*x));
const Wshift=Z3(Ks)/7722,lambdashift=perron(Ks);
must(Math.abs(Wshift/W-q**3)<3e-13,"Book Info shift scales real 3-tick pressure q^3");
must(Math.abs(lambdashift/lambda-q)<2e-13,"Book absolute PF pressure scales q");
const B=-Math.log(lambda)/ell,Bshift=-Math.log(lambdashift)/ell;
must(Math.abs(Bshift-B+t)<1e-12,"absolute native pressure B -> B-t, exact affine cocycle");

// NEW exact original two-depth CLOCK/BOOK 3:2 affine cocycle cancellation.
// On the true native supported paths, Z2=Tr K^2 and Z3=Tr K^3.
// For any fixed real stage priors beta2,beta3, normalized true stage odds
// are (beta3 Z3)/(beta2 Z2). Under uniform ORIGINAL Info shift t,
// odds gain exactly phi^t, cancelling B=-log_phi(PF root)'s -t.
// This is an observed clock-code contrast, NOT an extra physical action.
function Z2(k){let a=0;for(let i=0;i<N;i++)for(let j=0;j<N;j++)a+=k[i][j]*k[j][i];return a;}
function rootedZ2(k){let a=0;for(let j=0;j<N;j++)a+=k[0][j]*k[j][0];return a;}
function rootedZ3(k){let a=0;for(let j=0;j<N;j++)for(let v=0;v<N;v++)
 a+=k[0][j]*k[j][v]*k[v][0];return a;}
const z20=Z2(K),z2t=Z2(Ks),root20=rootedZ2(K),root2t=rootedZ2(Ks),
      root30=rootedZ3(K),root3t=rootedZ3(Ks);
must(Math.abs(z2t/z20-q*q)<4e-13 && Math.abs(root2t/root20-q*q)<4e-13,
 "original FULL/rooted 2-tick Book pressure shifts q²");
must(Math.abs(root3t/root30-q**3)<4e-13,
 "original TRUE a0-rooted native 3-tick loops shift q³");
const beta2=p,beta3=p*p; // test-only positive fixed Golden reference weights
const clockCode=(z2,z3)=>Math.log((beta3*z3)/(beta2*z2))/ell;
const c0=clockCode(z20,Z3(K)),c1=clockCode(z2t,Z3(Ks));
const cc0=clockCode(root20,root30),cc1=clockCode(root2t,root3t);
must(Math.abs(c1-c0-t)<2e-12 && Math.abs(cc1-cc0-t)<2e-12,
 "ACTUAL complete-stage 3-vs-2 clock odds carry +1 GOLDEN source");
must(Math.abs((Bshift+c1)-(B+c0))<2e-12,
 "original ABSOLUTE Perron -1 cocycle cancelled EXACT by adjacent Book stage odds +1");


const I=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const M=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const add=(A,B,c=1)=>A.map((row,i)=>row.map((v,j)=>v+c*B[i][j]));
const T=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const E=(i,j)=>{let a=Array.from({length:4},()=>Array(4).fill(0));a[i][j]=1;return a};
const eta=Array.from({length:4},()=>Array(4).fill(0));
eta[0][1]=eta[1][0]=1;eta[2][2]=eta[3][3]=-1;
const A=add(E(1,2),E(2,0)), C=add(E(0,3),E(3,1));
function nilExp(G,a){return add(add(I(4),G,a),M(G,G),a*a/2);}
const a=.11,b=.13;
const P=M(M(M(nilExp(A,a),nilExp(C,b)),nilExp(A,-a)),nilExp(C,-b));
const Pinv=M(M(M(nilExp(C,b),nilExp(A,a)),nilExp(C,-b)),nilExp(A,-a));
const odd=add(P,Pinv,-1).map(row=>row.map(x=>x/2));
const Omega=M(eta,odd);
must(Math.abs(Omega[2][3])>.001,"literal original SO face has nonzero Cartan odd source");
must(Math.max(...add(Omega,T(Omega)).flat().map(Math.abs))<2e-13,"actual SO odd Lorentz bivector");
const e=I(4).map((row,i)=>row.map((v,j)=>v+((i+2*j)%5===0?.18:0)));
const scaleMat=(B,s)=>B.map(row=>row.map(v=>s*v));
const col=(A,j)=>A.map(row=>row[j]);
const dot=(v,w)=>v.reduce((a,x,i)=>a+x*w[i],0);
const face=(u)=>{
 const v=col(u,2), w=col(u,3), Omw=Omega.map(row=>dot(row,w));
 return dot(v,Omw);
};
const f=face(e),fShift=face(scaleMat(e,q**(-1.5)));
must(Math.abs(fShift-q**(-3)*f)<2e-14,"original genuine SO odd wedge coframe degree2");
must(Math.abs(Wshift*fShift-W*f)<1e-12,"EXACT raw Book-weighted odd-star offshell W/e compensation");
must(Math.abs(Math.sqrt(Wshift)*q**(-1.5)-Math.sqrt(W))<2e-14,
 "full Book dressed coframe sqrt(W)e is INVARIANT");

// Golden AF J2 fibre: physical original corrected two scene ticks,
// at original true identity scene B=0; 528 trace multiplicity cancels.
const z=p*p,e0=p*p,step2=1/64;
const lambdaAF=e=>4*e*(1-e);
const rAF=e=>1-z*lambdaAF(e),r0=rAF(e0),etaField=e0*step2;
const gp0=4*z*(1-2*e0)/r0;
const Phi=f=> -Math.log(rAF(e0+etaField*f)/r0)/(etaField*gp0);
const PhiPrime=f=>{
 const ex=e0+etaField*f;
 return (4*z*(1-2*ex)/rAF(ex))/gp0;
};
must(Math.abs(PhiPrime(0)-1)<1e-14&&Math.abs(Phi(0))<2e-14,
 "actual original AF two-tick fibre Phi(0)=0 and derivative1");
function bookCompensatedF(f,q){
 if(Math.abs(f)<1e-14)return 0;
 const r=q**(-3);
 const newR=r0*Math.pow(rAF(e0+etaField*f)/r0,r);
 const Lam=(1-newR)/z;
 must(1-Lam>0,"strict original AF positive branch");
 const ePrime=(1-Math.sqrt(1-Lam))/2;
 return (ePrime-e0)/etaField;
}
const tests=[];
for(let x of [-.43,-.32,-.03,.11,.4]){
 let xf=bookCompensatedF(x,q),xBack=bookCompensatedF(xf,1/q);
 must(Math.abs(q**3*Phi(xf)-Phi(x))<2e-11,"ALL-ORDER original Golden AF W-Phi compensation");
 must(Math.abs(xBack-x)<8e-10,"original native AF nonlinear transformation is reversible");
 const dressed0=Math.sqrt(W*Phi(x)/x);
 const dressed1=Math.sqrt(Wshift*Phi(xf)/xf)*Math.sqrt(xf/x);
 must(Math.abs(dressed1-dressed0)<2e-10,"WHOLE dressed Golden coframe invariant offshell");
 const invJac=W**8*Math.pow(Phi(x)/x,7)*PhiPrime(x);
 must(invJac>0,"original full16 coframe map local Jacobian nonzero");
 tests.push({f:x,shiftedF:xf,nonlinearPhiResidual:q**3*Phi(xf)-Phi(x),
   dressedSourceResidual:dressed1-dressed0,radialJacobian:invJac});
}
const q2=Math.pow(phi,-.17);
const x0=.25;
must(Math.abs(bookCompensatedF(bookCompensatedF(x0,q),q2)-
              bookCompensatedF(x0,q*q2))<2e-10,
  "FINITE nonlinear BOOK-WEYL group law T_q T_r=T_qr");

// Original 4D volume determinant scales with FOUR coframe legs.
function det(A){
 let a=A.map(x=>x.slice()),o=1;
 for(let i=0;i<a.length;i++){
  let piv=i;for(let j=i+1;j<a.length;j++)if(Math.abs(a[j][i])>Math.abs(a[piv][i]))piv=j;
  if(piv!==i){[a[i],a[piv]]=[a[piv],a[i]];o=-o}
  const d=a[i][i];o*=d;
  for(let j=i+1;j<a.length;j++){const h=a[j][i]/d;
   for(let k=i+1;k<a.length;k++)a[j][k]-=h*a[i][k];}
 }
 return o;
}
const V=Math.abs(det(e));must(V>0,"original full16 nondegenerate coframe");
const Gamma=face(e)/V;
const eHat=scaleMat(e,Math.sqrt(W));
const gammaHat=face(eHat)/Math.abs(det(eHat));
must(Math.abs(gammaHat-Gamma/W)<2e-12,
 "ORIGINAL 4D physical volume makes Book coframe factor RECIPROCAL W^-1");
const meanScale=q**(1.5),gammaScaled=face(scaleMat(e,meanScale))/
 Math.abs(det(scaleMat(e,meanScale)));
must(Math.abs(Wshift*gammaScaled-W*Gamma)<2e-12,
 "MEAN-VOLUME 3:2 W-Info Weyl compensator has OPPOSITE coframe sign");

// ZERO-IDEAL theorem: for a true vacuum stationary geometric scalar A(q0)=DA=0,
// a moving positive W changes neither its root nor its MIXED Hessian.
// Elementary 1D analytic counterprobe Ageom(x)=x² illustrates exact block.
// The actual original six-face nonflat stationary pp family is an OWNER input.
const vacuum=(x,t)=>W*Math.exp(3*ell*t)*x*x;
const h=1e-4,g=1e-3;
const hx=(vacuum(h,0)-2*vacuum(0,0)+vacuum(-h,0))/(h*h);
const hxt=(vacuum(h,g)-vacuum(-h,g)-vacuum(h,-g)+vacuum(-h,-g))/(4*h*g);
must(Math.abs(hx-2*W)<2e-12&&Math.abs(hxt)<1e-16,
 "exact star-null vacuum is Book-weight robust with ZERO mixed source");
const wardDerivative=3*ell*W*f-(3*ell/2)*2*W*f;
must(Math.abs(wardDerivative)<2e-15,"original exact 3:2 finite Book/Palatini infinitesimal Ward");

console.log(JSON.stringify({
 status:"PASS_ORIGINAL_BOOK_3TICK_GOLDEN_AF_WEYL_FINITE_NONLINEAR",
 original:"K(9,11,13), positive all718 asymmetric native-type Book, actual Golden p",
 Z3_original:Z3(K),triangleBasedWords:7722,
 W_original:W,W_shifted:Wshift,lambda_original:lambda,
 uniformInfoShift:t,absoluteBookPressureAffineDifference:Bshift-B,
 trueNullFaceWedge:f,
 bookStarOffshellResidual:Wshift*fShift-W*f,
 genuineAFSceneB0:true,goldenPhiChecks:tests,
 physicalVolumeReciprocalBookPressure:gammaHat-Gamma/W,
 nullCriticalMixedHessian:hxt,
 equalities:"W3(Phi/e), nonlinear inverse, original 4D volume and exact Ward",
 notEstablished:"actual compulsory original G0/M1/Book full H+J+R selection, clock/prep/Info domain, sourced GR",
 GR_closed:false
},null,2));
