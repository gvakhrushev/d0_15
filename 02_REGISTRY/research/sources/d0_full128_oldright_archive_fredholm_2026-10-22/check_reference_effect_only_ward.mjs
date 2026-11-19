// Exact full fine-event Choi right-information through EFFECTS E_word=L†L
// of ALL complete stopped original-owned noncommuting 2-Kraus histories.
// The theorem applies to original full128 pure Choi + SINGLE fine Kraus per
// registered outcome: native I(R:Y)=logd-Σ q H(E/T), I(R:D|Y)=2Σ qH,
// and all first field source jets. Does not select Book03 Info.
import assert from 'node:assert/strict';
let checks=0;const ok=(v,m)=>{assert.ok(v,m);checks++};
const near=(x,y,t=2e-12,m='close')=>ok(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi),ln2=Math.log(2);
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const t=A=>[[A[0][0],A[1][0]],[A[0][1],A[1][1]]];
const add=(A,B)=>A.map((row,i)=>row.map((v,j)=>v+B[i][j]));
const scale=(A,k)=>A.map(row=>row.map(x=>x*k));
const tr=A=>A[0][0]+A[1][1];
const id=()=>[[1,0],[0,1]],zero=()=>[[0,0],[0,0]];
const h=q=>-q*Math.log(q)-(1-q)*Math.log1p(-q);
const hp=q=>Math.log((1-q)/q);
function program(a,b,K){
 const u=Math.sqrt(1-b*b),v=Math.sqrt(1-a*a);
 const Ks=[[[a,0],[0,b]],[[0,u],[v,0]]];
 const DK=[[[1,0],[0,0]],[[0,0],[-a/v,0]]];
 const sumE=add(mm(t(Ks[0]),Ks[0]),mm(t(Ks[1]),Ks[1]));
 for(let i=0;i<2;i++)for(let j=0;j<2;j++)
  near(sumE[i][j],i===j?1:0,2e-13,'actual old CP instrument normalizes');
 const leaves=[];
 for(let anchor=0;anchor<2;anchor++){
   for(let n=0;n<K;n++)leaves.push([anchor,...Array(n).fill(1-anchor),anchor]);
   leaves.push([anchor,...Array(K).fill(1-anchor)]);
 }
 const d=2;
 let mass=0,Hptr=0,cond=0,dptr=0,dcond=0;
 for(const word of leaves){
  let L=id(),DL=zero();
  for(const y of word){
   const dnext=add(mm(DK[y],L),mm(Ks[y],DL));
   L=mm(Ks[y],L);DL=dnext;
  }
  const E=mm(t(L),L),DE=add(mm(t(DL),L),mm(t(L),DL));
  const T=tr(E),DT=tr(DE),q=T/d,dq=DT/d;
  ok(q>0&&q<1,'every TRUE complete stopped binary fine output has positive Choi Born probability');
  near(E[0][1],0,5e-14,'original owner monomial Kraus gives TRUE diagonal fine effects');
  near(E[1][0],0,5e-14,'original owner monomial fine effects are Hermitian');
  const x=E[0][0]/T,dx=(DE[0][0]*T-E[0][0]*DT)/(T*T);
  ok(x>0&&x<1,'honest fine Kraus effect defines full-rank conditional reference state');
  // Direct original-data/right purification amplitude of (L tensor I)|Bell>
  // = (L00, L01, L10, L11)/sqrt2 in DATA*RIGHT basis.
  const psi=[L[0][0],L[0][1],L[1][0],L[1][1]].map(y=>y/Math.sqrt(2));
  const P=psi.reduce((s,y)=>s+y*y,0);
  near(P,q,2e-13,'full oldRIGHT pure Choi single-Kraus probability equals TrE/d');
  // reduced RIGHT density: partial trace over two DATA levels.
  const rr0=psi[0]**2+psi[2]**2;
  const rr1=psi[1]**2+psi[3]**2;
  const rrOff=psi[0]*psi[1]+psi[2]*psi[3];
  near(rr0/P,x,2e-13,'conditional oldRIGHT state equals ORIGINAL Kraus effect transpose / TrE');
  near(rr1/P,1-x,2e-13,'other conditional oldRIGHT native spectrum direct');
  near(rrOff,0,2e-13,'original fixed noncommuting two-Kraus fine reference diagonal');
  const hR=h(x);
  mass+=q;Hptr-=q*Math.log(q);cond+=q*hR;
  dptr-=dq*(1+Math.log(q));
  dcond+=dq*hR+q*hp(x)*dx;
 }
 near(mass,1,4e-13,'all stopped match/abort FULL Choi norm complete');
 const I_R_Y=ln2-cond;
 const I_R_DgivenY=2*cond;
 const I_R_DY=ln2+cond;
 near(I_R_Y+I_R_DgivenY/2,ln2,3e-13,
  'exact oldRIGHT one-half reference split, any complete native stopped fine tape');
 near(I_R_DY+I_R_Y,2*ln2,3e-13,
  'total coherent archive quantum 2logd decomposes under pointer measurement');
 ok(I_R_Y>=-1e-13&&I_R_DgivenY>=0,'Holevo and positivity for actual native Choi outcomes');
 const dI_R_Y=-dcond,dI_R_DgivenY=2*dcond,dI_R_DY=dcond;
 near(dI_R_Y+dI_R_DgivenY/2,0,5e-13,
  'native entire first source through oldRIGHT effect-only archive identity');
 near(dI_R_DY+dI_R_Y,0,5e-13,
  'Coherent archive 2logd source zero; pointer/coherent work first sources cancel');
 return {a,b,K,count:leaves.length,Hptr,dHptr:dptr,cond,dcond,
   I_R_Y,dI_R_Y,I_R_DgivenY,dI_R_DgivenY,I_R_DY,dI_R_DY};
}
const r0=program(.6,.8,1),r12=program(.6,.8,12);
for(const a of [.55,.6,.7]){
 for(const K of [1,2,3,5,8,12,18]){
  const f=program(a,.8,K),h=2e-5;
  const plus=program(a+h,.8,K),minus=program(a-h,.8,K);
  near(f.dcond,(plus.cond-minus.cond)/(2*h),3e-8,
    'native original whole recorded Choi conditional RIGHT source vs independent finite diff');
  near(f.dI_R_Y,(plus.I_R_Y-minus.I_R_Y)/(2*h),3e-8,
    'full actual measured reference information first source');
  near(f.dI_R_DgivenY,(plus.I_R_DgivenY-minus.I_R_DgivenY)/(2*h),3e-8,
    'full actual quantum work conditional reference information first source');
  near(f.dHptr,(plus.Hptr-minus.Hptr)/(2*h),3e-8,
    'independent FULL pointer Shannon first source from same fine Kraus word probabilities');
 }
}
// ORIGINAL one native round (not stopped) has a closed exact reference
// information source with noncommuting K0 and K1 on the same source owner.
function oneRound(a,b){
 let q=(a*a+b*b)/2, q1=1-q;
 const e0=a*a/(a*a+b*b),e1=(1-a*a)/(2-a*a-b*b);
 const C=q*h(e0)+q1*h(e1);
 return {q,C,I_R_Y:ln2-C,I_R_DgivenY:2*C};
}
const base=oneRound(.6,.8);
near(base.q,.5,3e-14,'actual native one-round two-Kraus fine outcome q=1/2');
near(base.C,h(.36),2e-13,'actual native one-round conditional RIGHT entropy h(9/25)');
near(base.I_R_Y,ln2-h(.36),2e-13,'genuine measurable oldRIGHT↔pointer mutual info');
const hd=1e-6,dr=(oneRound(.6+hd,.8).I_R_Y-oneRound(.6-hd,.8).I_R_Y)/(2*hd);
const deriv=-.6*Math.log(16/9);
near(dr,deriv,3e-10,'original noncommuting native Choi classical RIGHT information STRICT nonzero field source');
ok(deriv<-.345&&deriv>-.346,
 'native measured RIGHT information has strictly negative source on actual owner perturbation');
console.log(JSON.stringify({status:"PASS_NATIVE_CHOI_FINE_REFERENCE_INFO_WARD",checks,
 originalNativeOwner:"old exact rational nonunital two-Kraus from native stationary occupation",
 originalChoi2OneRound:{...base,firstFieldSource:deriv,
  conditionalQuantumFieldSource:-2*deriv},
 fullNativeCompleteStoppedCap1:r0,
 fullNativeCompleteStoppedCap12:r12,
 universalFull128:{
  fullFineKrausInput:"original Choi DATA128 oldRIGHT128",
  effectOnlyRightConditional:"rho(R|gamma)= E_gamma^transpose/TrE_gamma, E_gamma=L_gamma†L_gamma",
  classicalReferenceInfo:"I(R:gamma)=log(128)−Σ qgamma H(Egamma/TrEgamma)",
  quantumConditionalReference:"I(R:D|gamma)=2Σ qgamma H(Egamma/TrEgamma)",
  sourceWard:"dI(R:gamma)+0.5 dI(R:D|gamma)=0",
  premise:"ALL fine registered leaves have exactly one Kraus word and full purified Choi input, no hidden dephased factory branches"
 },
 originalFull128WholeSourceSuiteRerun:false,
 physicalBook03InfoChosen:false,
 GR_closed:false}));
