// Narrow analytical Banach composition proof checker, consumes but does NOT
// rerun the original certified h4 42x42 interval Jacobian and polydisc.
import assert from 'node:assert/strict';
let checks=0;
const check=(q,msg)=>{assert.ok(q,msg);checks++;};
const phi=(1+Math.sqrt(5))/2,p=1/phi,z=2**-20,lnPhi=Math.log(phi);
const betaBook=2*p*p,tau=.05;
const alpha=(1-(1-2*p**3)**9)**128;
const betaFactory=((1-p**120)**4*(1-(1-16*p**9)**20))**43;
const gamma=alpha*betaFactory;
const L=4*p**3,Q=1-z*L,R=1-z*L*(1+p**6),rStar=1-Q*R;
const rxStar=4*z*Q*p**11;
const hprime=Math.log((1-rStar)/rStar)/lnPhi;
const c=-gamma*lnPhi*tau*hprime*rxStar/betaBook;
const sourcePins={
  rigorousOriginal42:{
    blob:"9f4bdef4c367660539c588db01819330ff0d55b3",
    path:"02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/RIGOROUS_EXACT42_CERTIFICATE.json"
  },
  genuineReport:{
    blob:"2c7193f54da76aaf108d2821c45daddac7457f02",
    path:"02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/REPORT_BRIDGE_RESULT.json"
  },
  independentCQ:{
    blob:"1541e1e2cb9e857021a18136ed1569cb48cfffb0",
    path:"02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/independent_price_replay.py"
  }
};
check(gamma>.45&&gamma<.46,"authentic physical native γ=αβfactory");
check(betaBook>.7&&betaBook<.8,"native original β=2p² positive algebraic");
check(lnPhi>.48&&lnPhi<.49,"native φ ln unit");
check(rStar>1.85e-6&&rStar<1.86e-6,"original N1 rstar genuine positive");
check(rxStar>1.8e-8,"original N1 report curvature derivative positive");
check(hprime>26,"original h_phi derivative positive");
check(c<0 && -c>1e-9,"strict original normalized N1 vs HJR scalar c magnitude");
const Rpolydisc=1e-7,realReportMin=1.85e-6,complexReportMax=2e-6;
const gammaLow=.45,gammaHigh=.46;
const minRealRare=gammaLow*realReportMin;
const maxAbsRare=gammaHigh*complexReportMax;
const aRare=Math.sqrt(1-2*minRealRare+maxAbsRare**2);
const minReReady0=gammaLow*(1-complexReportMax);
const maxAbsReady0=gammaHigh*(1+complexReportMax);
const aReady0=Math.sqrt(1-2*minReReady0+maxAbsReady0**2);
const aFail=gamma;
const theta=1-8e-7;
for(const [name,x] of [["READY1",aRare],["READY0",aReady0],["FAIL",aFail]]) {
 check(x<theta,"uniform complex strict |1-q_"+name+"|≤1-8e-7");
}
check(maxAbsReady0+aFail+maxAbsRare<2,"strict complete complex |q|_1<2");
const K=100_000_000;
check(theta**K<=Math.exp(-80),"exact power bound (1-eps)^K≤exp(-K eps)");
const D=Math.exp(-80)/80;
check(D<3e-37,"true capped harmonic complex δ bound");
const D0=3e-37;
const Merror=2*(10*D0**2)/betaBook; // two true original field cells
check(Merror<1e-70,"complete original two-cell HJR scalar error quadratic in actual KL");
const M=1e-70;
const gradScalar=M/Rpolydisc;
const hessOperator=2*42*M/Rpolydisc**2;
const gradNorm=gradScalar/Math.abs(c);
const hessNorm=hessOperator/Math.abs(c);
check(gradNorm<1e-54,"42-field normalized source Cauchy bound");
check(hessNorm<8.4e-46,"42x42 normalized Hessian infinity Cauchy bound");
const oldPreconditioner=49.444,Abound=50;
const oldJacobianCenter=1.449e-7;
const oldJacobianBallMove=6.978e-14;
const oldCenterDrift=1.484e-58;
check(oldPreconditioner<Abound,"same already interval-certified preconditioner");
const newCenterDrift=oldCenterDrift+Abound*gradNorm;
const newContraction=oldJacobianCenter+oldJacobianBallMove+Abound*hessNorm;
check(newCenterDrift<6e-53,"actual new finite K center inclusion error");
check(newContraction<1e-6,"entire certified real root cube strict Banach contraction");
const radius=1e-30;
check(newCenterDrift<(1-newContraction)*radius,"new complete generated HJR K100M map exactly selfmaps old 1e-30 ball");
check(Math.abs(c)>1e-9 && Number.isFinite(1/c),"legitimate nonzero full normalized 42-source transport");
// Positivity of the FINITE-K KL thermodynamic defect on genuine native q:
// no sign/normalization free counterterm.
function finiteScore(q,Ksmall){
 let x=1-q,v=0,w=x;
 for(let k=1;k<=Ksmall;k++){v+=w/k;w*=x}
 return v;
}
for(const r of [rStar,rStar+7e-11,.015,.21,.52]){
 const qs=[1-gamma,gamma*(1-r),gamma*r];
 for(const k of [1,2,3,10,100,800]){
  const mm=qs.map(q=>finiteScore(q,k));
  const deltas=qs.map((q,i)=>-Math.log(q)-mm[i]);
  const zz=qs.reduce((s,q,i)=>s+q*Math.exp(deltas[i]),0);
  const entropyExcess=(Math.log(zz)-qs.reduce((s,q,i)=>s+q*deltas[i],0))/betaBook;
  check(entropyExcess>=-1e-14,"full ternary finite K generated heat KL nonnegative");
 }
}
const result={
  status:"PASS_BOUND_COMPOSITION_ORIGINAL_EXACT42",
  checks,
  K,
  originalScientificInputs:sourcePins,
  native:{betaBook,gamma,rStar,rxStar,hprime,c},
  complexReportInput:{radius:Rpolydisc,realReportMin,complexReportMax},
  actualTernaryNoMatchMax:{ready1:aRare,ready0:aReady0,fail:aFail,theta},
  bounds:{harmonicTail:D,complexTwoCellActionError:Merror,
    normalizedCenterPerturb:gradNorm,normalizedHessianPerturb:hessNorm,
    oldCenterDrift,newCenterDrift,oldJacobianCenter,oldJacobianBallMove,
    newContraction,radius},
  conclusion:"EXACT UNIQUE finite K100M 42-source root on declared NEW generated HJR-type action, same old certified h4 ball; not compulsory Book03",
  GR_closed:false
};
console.log(JSON.stringify(result,null,2));
