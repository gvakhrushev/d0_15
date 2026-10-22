// First-return ALL RECORDS on a positive stationary sequential Markov carrier.
// Original Golden p^2+p=1, 0/10 native Kraft charges, NO iid restart.
// Only standard Node.js assert. Scope: classical Markov output quotient, not
// literal original CAR16 complete quantum hidden-memory full128 instrument.
import assert from 'node:assert/strict';
let checks=0;
const check=(x,m)=>{assert.ok(x,m);checks++};
const close=(a,b,t=8e-12,label="close")=>check(Math.abs(a-b)<=t*Math.max(1,Math.abs(a),Math.abs(b)),label+": "+a+" vs "+b);
const p=(Math.sqrt(5)-1)/2,ell=Math.log(1/p),pi=[p,p*p],beta=2*p*p;
const ent=row=>-row.reduce((s,x)=>s+x*Math.log(x),0);
const sq=(a,b)=>({a,b});
const add=(x,y)=>({a:x.a+y.a,b:x.b+y.b});
const mul=(x,y)=>({a:x.a*y.a+x.b*y.b,b:x.a*y.b+x.b*y.a-x.b*y.b});
const eq=(x,y)=>x.a===y.a&&x.b===y.b;
const ZERO=sq(0,0),ONE=sq(1,0),P=sq(0,1),P2=sq(1,-1),P3=sq(-1,2);
const T2=sq(2,-2);
check(eq(add(P2,P),ONE),"exact native p²+p=1 in Q(p)");
check(eq(mul(P,P2),P3),"exact original p³=2p-1");
const Pg=[[T2,P3],[P2,P]];
check(eq(add(Pg[0][0],Pg[0][1]),ONE),"actual Golden row0 normalized exactly");
check(eq(add(Pg[1][0],Pg[1][1]),ONE),"actual Golden row1 normalized exactly");
const piExact=[P,P2];
for(let j=0;j<2;j++){
 const rhs=add(mul(piExact[0],Pg[0][j]),mul(piExact[1],Pg[1][j]));
 check(eq(rhs,piExact[j]),"Golden (p,p²) stationary Q(p) identity");
}
function transition(s,prior=pi){
 const q=prior,mat=q.map((_,i)=>q.map((v,j)=>(i===j?(1-s):0)+s*v));
 for(const row of mat)close(row.reduce((a,b)=>a+b,0),1,1e-14,"transition rows normalized");
 for(let j=0;j<q.length;j++)close(q.reduce((t,v,i)=>t+v*mat[i][j],0),q[j],1e-14,"stationary actual moving row law");
 return mat;
}
function fields(prior,P){
 const hpi=ent(prior);
 const rate=prior.reduce((s,vi,i)=>s+vi*ent(P[i]),0);
 const mutual=hpi-rate;
 return {hpi,rate,mutual,oracleIid:3*hpi,actualFullEntropy:hpi+prior.length*rate,
   price:prior.length+1, meanLength:prior.length+1};
}
function treeFinite(prior,P,K,c){
 const m=prior.length;
 let totalE=ent(prior),meanT=1,meanCost=prior.reduce((s,v,i)=>s+v*c[i],0);
 let terminalWeight=0;
 for(let anchor=0;anchor<m;anchor++){
  let alive=prior.map((_,i)=>i===anchor?prior[anchor]:0);
  for(let k=0;k<K;k++){
    const survive=alive.reduce((a,b)=>a+b,0);
    meanT+=survive;
    const next=Array(m).fill(0);
    for(let i=0;i<m;i++)for(let j=0;j<m;j++){
      const mass=alive[i]*P[i][j];
      if(!mass)continue;
      totalE-=mass*Math.log(P[i][j]);
      meanCost+=mass*c[j];
      if(j!==anchor)next[j]+=mass;
      else terminalWeight+=mass;
    }
    alive=next;
  }
  terminalWeight+=alive.reduce((a,b)=>a+b,0); // cap abort mass
 }
 close(terminalWeight,1,3e-12,"every first-return/abort path is retained");
 return {ent:totalE,len:meanT,cost:meanCost};
}
function directBinaryLeaves(prior,P,K,c){
 const u=P[0][1],v=P[1][0],q0=prior[0],q1=prior[1];
 let norm=0,H=0,T=0,C=0;
 const add=(prob,len,cost)=>{
  norm+=prob;H-=prob*Math.log(prob);T+=prob*len;C+=prob*cost;
 };
 add(q0*(1-u),2,2*c[0]);
 add(q1*(1-v),2,2*c[1]);
 for(let n=1;n<K;n++){
  add(q0*u*(1-v)**(n-1)*v,n+2,2*c[0]+n*c[1]);
  add(q1*v*(1-u)**(n-1)*u,n+2,2*c[1]+n*c[0]);
 }
 add(q0*u*(1-v)**(K-1),K+1,c[0]+K*c[1]);
 add(q1*v*(1-u)**(K-1),K+1,c[1]+K*c[0]);
 close(norm,1,2e-12,"complete binary stopped tree normalized");
 return {ent:H,len:T,cost:C};
}
for(const s of [p*p,p,.35,.7,.96]){
 const Pmat=transition(s),q=fields(pi,Pmat);
 check(q.mutual>0,"genuine stationary history correlation not iid");
 for(const K of [1,2,3,5,12,40,180]){
  const a=treeFinite(pi,Pmat,K,[1,2]),b=directBinaryLeaves(pi,Pmat,K,[1,2]);
  close(a.ent,b.ent,8e-12,"independent tree vs occupation entropy");
  close(a.len,b.len,5e-12,"all actual charged match/abort lengths");
  close(a.cost,b.cost,7e-12,"all original charged Golden labels");
  if(K>=180){
   close(a.ent,q.actualFullEntropy,2e-12,"Kac Shannon stopped-entropy theorem exact limit");
   close(a.len,3,2e-12,"three expected native trials at stationarity");
   const s1=pi[0]*1+pi[1]*2-q.hpi/ell;
   const sStop=a.cost-a.ent/ell;
   close(sStop,3*s1+2*q.mutual/ell,2e-11,"native Golden Markov complete Cost−Info correction");
  }
 }
}
const G=transition(p);
const u=G[0][1],v=G[1][0],h0=-u*Math.log(v)/(1-v),h1=-v*Math.log(u)/(1-u);
close(u,p**3,2e-14,"genuine p³ departure");
close(v,p*p,2e-14,"genuine p² return");
close(h0,2*p*p*ell,4e-14,"EXACT sequential Golden harmonic m0");
close(h1,1.5*ell,4e-14,"EXACT sequential Golden harmonic m1");
check(Math.abs(h0+Math.log(pi[0]))>.1,"conditional m0 differs from iid -log q0");
check(Math.abs(h1+Math.log(pi[1]))>.2,"conditional m1 differs from iid -log q1");
for(let k=1;k<=550;k++){
 // Native actual conditional first-match nonmatch survival tails.
 const s0=u*(1-v)**(k-1),s1=v*(1-u)**(k-1);
 if(k===1){close(s0,u);close(s1,v)}
}
let hm0=0,hm1=0;
for(let k=1;k<=550;k++){hm0+=u*(1-v)**(k-1)/k;hm1+=v*(1-u)**(k-1)/k}
close(hm0,h0,1e-13,"full actual no-reset harmonic 0 sum");
close(hm1,h1,1e-13,"full actual no-reset harmonic 1 sum");
const qFirst=fields(pi,G);
close(qFirst.hpi,ell*(p+2*p*p),1e-13,"full stationary one-shot Golden Shannon=code");
const avgNativeCode=p+2*p*p;
close(avgNativeCode-qFirst.hpi/ell,0,2e-13,"Golden one-trial Kraft Cost−Info zero");
const Sstop=3*avgNativeCode-qFirst.actualFullEntropy/ell;
close(Sstop,2*qFirst.mutual/ell,5e-13,"nonzero original Golden stopped memory cost exact");
check(Sstop>.3&&Sstop<.31,"quantitative native non-iid pointer-Info source gap");
function sourceS(s){
 const Pmat=transition(s),f=fields(pi,Pmat);
 return 3*avgNativeCode-f.actualFullEntropy/ell;
}
const h=1e-6,deriv=(sourceS(p+h)-sourceS(p-h))/(2*h);
const ana=-2*p**3*Math.log(2/(p*p))/ell;
close(deriv,ana,4e-9,"independent moving transition source with fixed all Born marginals");
check(Math.abs(deriv)>1.6,"strong nonzero memory-only source");
const stateH=qFirst.hpi, rowH0=ent(G[0]),rowH1=ent(G[1]);
const gibbsRows=G.map(row=>{
 const vmax=Math.max(...row),energy=row.map(x=>Math.log(vmax/x)/beta);
 const ex=energy.map(x=>Math.exp(-beta*x)),z=ex.reduce((a,b)=>a+b,0);
 const gibbs=ex.map(x=>x/z);
 for(let j=0;j<row.length;j++)close(gibbs[j],row[j],1e-13,"native transition-Gibbs row exact");
 const energyPrice=row.reduce((s,x,j)=>s+x*energy[j],0)+Math.log(z)/beta;
 close(energyPrice,ent(row)/beta,2e-13,"entire conditional transition entropy");
 return energyPrice;
});
close((stateH+2*(pi[0]*rowH0+pi[1]*rowH1))/beta,
 (stateH+2*(pi[0]*beta*gibbsRows[0]+pi[1]*beta*gibbsRows[1]))/beta,
 2e-13,"all Markov correlations reconstructed via NATIVE CONDITIONAL Gibbs rows");
function testGeneral3(){
 const pr=[.2,.3,.5],s=.55,P=transition(s,pr),f=fields(pr,P);
 const c=[1,2,3];
 const K=180,t=treeFinite(pr,P,K,c);
 close(t.ent,f.actualFullEntropy,3e-10,"positive three-status stationary entropy theorem");
 close(t.len,4,3e-10,"positive three-status Kac mean4");
 const Cmean=pr.reduce((v,q,i)=>v+q*c[i],0);
 close(t.cost,4*Cmean,3e-10,"all executed ternary costs 4 mean");
 check(f.mutual>0,"truly non-iid ternary mutual information");
}testGeneral3();
console.log(JSON.stringify({status:"PASS",checks,
 exactGolden:{
   p,stationaryProbabilities:pi,
   transitionalMatrix:G,
   firstReturnHarmonic:[h0,h1],
   iidHarmonic:[-Math.log(pi[0]),-Math.log(pi[1])],
   KacMean:3,oneTrialCostMinusInfo:0,
   stoppedCostMinusInfo:Sstop,
   stationaryMemorySource:ana,lagMutualInformation:qFirst.mutual
 },
 correction:"H_stop=H(pi)+m h_rate=(m+1)H(pi)-m mutual_info",
 nativeQuantumFull128MarkovAssumed:false,GR_closed:false},null,2));
