// D0 research: exact primitive ActionProtocol floor versus scalar Book CP source; scoped.
// The same run() was evaluated in the research tool. No physical GR closure.
const run=function run(){
 const phi=(1+Math.sqrt(5))/2, L=Math.log(phi), S=359, B=2574, p=1/phi;
 function need(b,name){if(!b)throw Error(name);}
 function root(F,guess=22){let x=guess;for(let i=0;i<50;i++){const y=F(x), der=(F(x+1e-5)-F(x-1e-5))/(2e-5);const nx=x-y/der;if(Math.abs(nx-x)<3e-13)return nx;x=nx;}return x;}
 function rootcp(t){return root(x=>x**3-S*x-B*Math.cosh(3*L*t));}
 function pressureCP(t){return 1-Math.log(rootcp(t))/L;}
 const rho=rootcp(0),A0=pressureCP(0),CP2=-9*L*B/(rho*(3*rho*rho-S));
 need(CP2<0 && Math.abs(CP2+0.476374451552645866)<1e-12,"CP curvature");
 let maxTwoErr=0;
 for(const h of [0.015,0.035,0.07,0.11]){
   const two=h*h+pressureCP(h*h)-A0;
   const one=h+pressureCP(h)-A0;
   need(two>0 && one>0,"floor-admissible pressure monotonic");
   maxTwoErr=Math.max(maxTwoErr,Math.abs(two-(h*h+CP2*h**4/2)));
 }
 need(maxTwoErr<3e-9,"quadratic floor Taylor");
 const delta=.3;for(const eps of [.05,.16,.29]){
   need(1+delta-eps>=1 && delta+pressureCP(eps)<delta+A0,"interior CP strictly unstable");
 }
 const k=[99,143,117],pairCard=[198,286,234], D=rho*(3*rho*rho-S);
 const q=k.map(z=>(2*z*rho+B)/D),perEdge=q.map((x,i)=>x/pairCard[i]);
 need(Math.abs(q.reduce((a,b)=>a+b,0)-1)<1e-13,"stationary orbit probs");
 need(perEdge.every(z=>z>0),"Perron primitive Cost partials");
 const I=[.21,-.37,.56],theta=.42;
 const C=[[0,1,1],[1,0,1],[1,1,0]];
 const K=I.map((x,u)=>I.map((y,v)=>u===v?0:Math.exp(-L*(C[u][v]-theta*x-(1-theta)*y))));
 const Ks=I.map((x,u)=>I.map((y,v)=>u===v?0:Math.exp(-L*(C[u][v]-(x+y)/2))));
 const Dz=I.map(x=>Math.exp(L*(theta-.5)*x));let err=0;
 for(let u=0;u<3;u++)for(let v=0;v<3;v++)err=Math.max(err,Math.abs(K[u][v]-Dz[u]*Ks[u][v]/Dz[v]));
 need(err<5e-15,"Info endpoint similarity");
 const cpCycle=[[0,1],[1,2],[2,0]],reverse=[[0,2],[2,1],[1,0]];
 const logLoop=w=>w.reduce((c,[u,v])=>c+Math.log(K[u][v]),0);
 need(Math.abs(logLoop(cpCycle)-logLoop(reverse))<5e-15,"Info cannot generate scalar circulation");
 const epsilonNative=p*p*(.25**2)/64,lam=288/25;
 const pr=p*epsilonNative*lam, dpr=p*epsilonNative*(-lam/2);
 need(Math.abs(dpr/pr+.5)<1e-14,"actual full128 J23 port source");
 return {status:"PASS_ORIGINAL_COST_FLOOR_CP_SOURCE_SELECTION",
  rho,scalarBookCP2:CP2,
  admissibleFloorC2:2,admissibleFloorC4:12*CP2,
  stationarityCostsPerDirectedEdge:perEdge,
  nativeFull128Port1Probability:pr,full128J23RelativeJet:dpr/pr,
  full128PortSurprisalJet:-dpr/(L*pr),
  infoGaugeResidual:err,
  numericalTests:"floor 4 samples, interior 3 samples, native 3x3 Info similarity, genuine J23 port source"};
};
console.log(JSON.stringify(run(),null,2));
