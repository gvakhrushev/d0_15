// Complete ACTUAL previous-owner nonunital two-Kraus (rational K0,K1) first
// return tree. Correlated quantum DATA, NO iid reset / postselection.
// Every cap abort is retained. Validates exact prefix chain-rule entropy,
// moving stationary input source, native conditional Gibbs node decomposition.
// No claim of compulsory Book03 trace or whole original 128-CAR.
import assert from 'node:assert/strict';
let checks=0;
const check=(x,m)=>{assert.ok(x,m);checks++};
const close=(x,y,t=5e-11,m='close')=>check(Math.abs(x-y)<=t*Math.max(1,Math.abs(x),Math.abs(y)),m+': '+x+' vs '+y);
const p=(Math.sqrt(5)-1)/2,beta=2*p*p;
function mm(A,B){return A.map((row)=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)))}
const tr=A=>A.reduce((s,row,i)=>s+row[i],0);
const T=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const add=(A,B)=>A.map((row,i)=>row.map((x,j)=>x+B[i][j]));
const h=law=>-law.reduce((s,x)=>s+x*Math.log(x),0);
function fixture(a=.6,b=.8){
 const flip0=Math.sqrt(1-a*a),flip1=Math.sqrt(1-b*b);
 const K=[[[a,0],[0,b]],[[0,flip1],[flip0,0]]];
 const complete=add(mm(T(K[0]),K[0]),mm(T(K[1]),K[1]));
 for(let i=0;i<2;i++)for(let j=0;j<2;j++)
   close(complete[i][j],+(i===j),1e-13,'true no-reset 2-Kraus complete instrument');
 const pi0=(1-b*b)/((1-a*a)+(1-b*b)),pi1=1-pi0;
 const rho=[[pi0,0],[0,pi1]];
 const apply=(b,X)=>mm(mm(K[b],X),T(K[b]));
 let newR=[[0,0],[0,0]];
 for(let j=0;j<2;j++)newR=add(newR,apply(j,rho));
 for(let i=0;i<2;i++)for(let j=0;j<2;j++)
   close(newR[i][j],rho[i][j],2e-14,'FULL moving stationary DATA input');
 return {K,rho,apply};
}
function fullTree(K,a=.6,b=.8){
 const F=fixture(a,b);
 const rec=[],nodes=[];
 function go(word,state){
  const weight=tr(state);
  check(weight>0&&Number.isFinite(weight),'actual full Kraus positive prefix');
  const raws=[F.apply(0,state),F.apply(1,state)];
  const qs=raws.map(x=>tr(x)/weight);
  close(qs[0]+qs[1],1,3e-14,'every conditional fine Born distribution exact');
  const entropy=h(qs);
  const chosen=qs.map((q,i)=>{
    const E=Math.log(Math.max(...qs)/q)/beta;
    return E;
  });
  const ex=chosen.map(E=>Math.exp(-beta*E)),z=ex.reduce((s,x)=>s+x,0);
  const soft=ex.map(v=>v/z);
  for(let i=0;i<2;i++)close(soft[i],qs[i],5e-14,'true native conditional Gibbs pointwise');
  const heat=qs.reduce((s,x,i)=>s+x*chosen[i],0)+Math.log(z)/beta;
  close(heat,entropy/beta,2e-13,'complete conditional heat+energy entropy');
  nodes.push({word,weight,entropy,heat,qs});
  for(let j=0;j<2;j++){
    const w=word.concat([j]),s=raws[j];
    const term=w.length>=2&&(w[w.length-1]===w[0]||w.length===K+1);
    if(term)rec.push({w,weight:tr(s)});
    else go(w,s);
  }
 }
 go([],F.rho);
 const P=rec.reduce((s,v)=>s+v.weight,0);
 const pointerH=rec.reduce((s,v)=>s-v.weight*Math.log(v.weight),0);
 const chainH=nodes.reduce((s,n)=>s+n.weight*n.entropy,0);
 const weightedHeat=nodes.reduce((s,n)=>s+n.weight*n.heat,0);
 const unweightedHeat=nodes.reduce((s,n)=>s+n.heat,0);
 const meancount=rec.reduce((s,v)=>s+v.weight*v.w.length,0);
 const live=nodes.slice(1);
 const N=live.reduce((s,node)=>s+node.weight,0);
 const nb=[0,1].map(b=>live.reduce((s,node)=>s+node.weight*node.qs[b],0));
 const qbase=nodes[0].qs,Hp=h(qbase);
 const predKL=live.reduce((s,node)=>s+node.weight*node.qs.reduce(
   (k,v,b)=>k+v*Math.log(v/qbase[b]),0),0);
 const capCorrection=-nb.reduce((s,x,b)=>s+(x-N*qbase[b])*Math.log(qbase[b]),0);
 const fullPredicted=(1+N)*Hp-predKL+capCorrection;
 close(fullPredicted,pointerH,6e-13,'exact native quantum predicted Info + finite cap source');
 check(predKL>=-1e-13,'predictive KL of the ORIGINAL no-reset history positive');
 const firstNodes=live.filter(node=>node.word.length===1);
 const pairMI=firstNodes.reduce((s,node)=>s+node.weight*node.qs.reduce(
   (k,v,b)=>k+v*Math.log(v/qbase[b]),0),0);
 check(predKL+1e-13>=pairMI,'native predictive KL dominates actual Y0/Y1 MI');
 close(N,meancount-1,6e-13,'true number of later native comparisons');
 close(nb.reduce((s,x)=>s+x,0),N,5e-13,'all actual comparison outputs counted');
 close(P,1,3e-13,'full capped matching/abort leaf mass ONE');
 close(pointerH,chainH,6e-13,'exact full correlated quantum prefix tree Shannon chain rule');
 close(beta*weightedHeat,pointerH,6e-13,'source-ready full CONDITIONAL Gibbs energy+heat with TRUE occupancy weights');
 check(Math.abs(beta*unweightedHeat-pointerH)>.01,'no cheap unweighted sum of local Book heats');
 const q0=nodes[0].qs[0],q1=nodes[0].qs[1];
 const p00=rec.length>0?tr(F.apply(0,F.apply(0,F.rho))):0;
 return {F,rec,nodes,P,pointerH,chainH,weightedHeat,unweightedHeat,meancount,q0,q1,p00,N,nb,predKL,capCorrection,fullPredicted,pairMI};
}
const base=fullTree(7);
close(base.F.rho[0][0],9/25,1e-14,'SAME owned 2-Kraus stationarity rho00=9/25');
close(base.F.rho[1][1],16/25,1e-14,'SAME owned 2-Kraus stationarity rho11=16/25');
close(base.q0,337/625,2e-14,'SAME owned q0=337/625');
close(base.q1,288/625,2e-14,'SAME owned q1=288/625');
close(base.p00-base.q0**2,7056/390625,3e-14,'SAME owned non-iid original joint 00 gap');
check(Math.abs(base.nodes[1].qs[0]-base.q0)>.01,
      'actual conditional next-step report probability depends on past');
for(const cap of [1,2,3,4,6,12,24,60]){
 const out=fullTree(cap);
 check(out.meancount>=1.9&&out.meancount<=3.0000000001,"genuine finite original Kac occupation");
 if(cap>=60){
  close(out.meancount,3,5e-11,"stationary uncapped native Kac3 reached without reset");
  const iid=3*h([out.q0,out.q1]);
  close(out.predKL,iid-out.pointerH,1e-10,'full no-reset entropy deficit is KL not IID');
  close(out.capCorrection,0,1e-10,'stationary finite-cap boundary vanishes at infinite return');
  check(Math.abs(out.pointerH-iid)>.009,
    "actual original noncommuting first-label source differs from iid whole-Shannon");
 }
}
const e=1e-5;
for(const cap of [2,5,10,30]){
 const old=fullTree(cap,.6,.8);
 const high=fullTree(cap,.6+e,.8),low=fullTree(cap,.6-e,.8);
 const dH=(high.pointerH-low.pointerH)/(2*e);
 const dChain=(high.chainH-low.chainH)/(2*e);
 const dThermal=(high.weightedHeat-low.weightedHeat)/(2*e);
 close(dH,dChain,1e-8,'true correlated first source of whole tape EXACT occupation derivative');
 close(dH,beta*dThermal,1e-8,'all noncommuting conditional Gibbs first source including moving native preparation');
 const dOne=(h(high.nodes[0].qs)-h(low.nodes[0].qs))/(2*e);
 const dN=(high.N-low.N)/(2*e);
 const dPred=(high.predKL-low.predKL)/(2*e);
 const dCap=(high.capCorrection-low.capCorrection)/(2*e);
 close(dH,(1+old.N)*dOne+dN*h(old.nodes[0].qs)-dPred+dCap,1e-8,
       'ACTUAL full first source = moving occupation & predictive KL plus finite cap');
 check(Number.isFinite(dH),'finite original native moving input/field jet');
}
const last=fullTree(80);
console.log(JSON.stringify({status:"PASS",checks,
 nativeOwner:"check_stationary_occupation.py unchanged nonunital_two_kraus fixture",
 stationaryDataDensity:[base.F.rho[0][0],base.F.rho[1][1]],
 originalOneLabelQ:[base.q0,base.q1],
 nativeNonIIDJointGap:base.p00-base.q0**2,
 uncappedStoppedFullPointerEntropy:last.pointerH,
 falseIIDEntropy:3*h([base.q0,base.q1]),
 uncappedKacMean:last.meancount,
 intrinsicPredictiveKL:last.predKL,
 twoStepMutualInformationLowerWall:last.pairMI,
 finiteCapOccupationCorrection:last.capCorrection,
 allFiniteFullTapeMarkovOrIIDAssumed:false,
 fullKrausConditionalGibbsWeightedSource:true,
 compulsoryBook03SingleHeatAndOldRIGHTInfoIdentified:false,
 GR_closed:false},null,2));
