#!/usr/bin/env node
// Exact native 3-zone lumping of the real K(9,11,13), not a new graph.
// Exhaustive zone paths retain the exact multiplicities of original vertices.
// This verifies finite score/product differentiation and illustrates approach
// to the analytic source. The uniform rate is proved in the accompanying text.
const parts=[9,11,13],ell=Math.log((1+Math.sqrt(5))/2),z=2**-20;
const assert=(ok,msg)=>{if(!ok)throw Error(msg);};
const near=(a,b,t,msg)=>assert(Math.abs(a-b)<=t,`${msg}: ${a} vs ${b}`);
const cross=(i,j)=>+(i+j===1);
function scene(t){
  const q=Math.exp(-ell*t);
  let lambda=22;
  for(let k=0;k<20;k++)
    lambda-=(lambda**3-(260+99*q*q)*lambda-2574*q)/
      (3*lambda*lambda-(260+99*q*q));
  const raw=[143*q+13*lambda,117*q+13*lambda,lambda*lambda-99*q*q];
  const total=raw.reduce((s,x,i)=>s+parts[i]*x,0);
  const r=raw.map(x=>x/total);
  const mu=r.map((x,i)=>parts[i]*x);
  const P=parts.map((_,i)=>parts.map((nj,j)=>i===j?0:
    nj*(cross(i,j)?q:1)*r[j]/(lambda*r[i])));
  const pi=r.map((x,i)=>parts[i]*x*x);
  const norm=pi.reduce((a,b)=>a+b);
  for(let i=0;i<3;i++)pi[i]/=norm;
  return {lambda,r,mu,P,pi};
}
const base=scene(0),up=scene(1e-4),down=scene(-1e-4);
const lambda=base.lambda;
const lambdaDot=-(198*lambda+2574)*ell/(3*lambda*lambda-359);
const dlogrho=lambdaDot/lambda;
const raw=[143+13*lambda,117+13*lambda,lambda*lambda-99];
const rawDot=[-143*ell+13*lambdaDot,-117*ell+13*lambdaDot,
  2*lambda*lambdaDot+198*ell];
const total=raw.reduce((s,x,i)=>s+parts[i]*x,0);
const totalDot=rawDot.reduce((s,x,i)=>s+parts[i]*x,0);
const dlogr=raw.map((x,i)=>rawDot[i]/x-totalDot/total);
const Pdot=base.P.map((row,i)=>row.map((p,j)=>p===0?0:
  p*(-ell*cross(i,j)+dlogr[j]-dlogr[i]-dlogrho)));
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,a,k)=>s+a*B[k][j],0)));
const tr=A=>A.reduce((s,row,i)=>s+row[i],0);
const I=Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>+(i===j)));
function logdetFeedback(F){
  const trace=tr(F);
  const second=F[0][0]*F[1][1]-F[0][1]*F[1][0]
    +F[0][0]*F[2][2]-F[0][2]*F[2][0]
    +F[1][1]*F[2][2]-F[1][2]*F[2][1];
  const det=F[0][0]*(F[1][1]*F[2][2]-F[1][2]*F[2][1])
    -F[0][1]*(F[1][0]*F[2][2]-F[1][2]*F[2][0])
    +F[0][2]*(F[1][0]*F[2][1]-F[1][1]*F[2][0]);
  return -Math.log1p(-z*trace+z*z*second-z*z*z*det);
}
function inverse(A){
  const aug=A.map((row,i)=>row.concat(I[i]));
  for(let k=0;k<3;k++){
    const pivot=aug[k][k];assert(Math.abs(pivot)>1e-10,"invertible return");
    for(let j=0;j<6;j++)aug[k][j]/=pivot;
    for(let i=0;i<3;i++)if(i!==k){
      const scale=aug[i][k];
      for(let j=0;j<6;j++)aug[i][j]-=scale*aug[k][j];
    }
  }
  return aug.map(row=>row.slice(3));
}
const T=base.P.map((row,i)=>row.map((p,j)=>Math.sqrt(base.pi[i]/base.pi[j])*p));
const dT=T.map((row,i)=>row.map((v,j)=>v*(-ell*cross(i,j)-dlogrho)));
const T2=mul(T,T),F=I.map((row,i)=>row.map((v,j)=>v-T2[i][j]));
const returnM=I.map((row,i)=>row.map((v,j)=>v-z*F[i][j]));
const source=-2*z*tr(mul(mul(inverse(returnM),T),dT));
const J3=logdetFeedback(F),J33=-30*Math.log1p(-z)+J3;
near(J33,0.000030035369315208,1e-16,"owned full33 feedback");

// Fixed cutoff for empirical ZONE masses. This is the exact lumped consumer
// of the theorem; full33 theorem uses all718 empirical edge counts instead.
const cutoff=.1;
function observable(counts,N){
  const out=counts.map(row=>row.reduce((a,b)=>a+b,0));
  if(out.some(x=>x/N<cutoff))return 0;
  const incoming=[0,1,2].map(j=>counts.reduce((s,row)=>s+row[j],0));
  const Fhat=I.map((row,i)=>row.map((_,j)=>{
    let v=i===j?incoming[i]/N:0;
    for(let u=0;u<3;u++)v-=counts[u][i]*counts[u][j]/(N*out[u]);
    return v/Math.sqrt(out[i]*out[j]/(N*N));
  }));
  return logdetFeedback(Fhat);
}
function exhaustive(N){
  let histories=0,mass=0,scoreMean=0,mean=0,scoreSource=0,directSource=0,
    plus=0,minus=0,noTerminal=0,noPressure=0,failedMass=0;
  const counts=Array.from({length:3},()=>[0,0,0]);
  function walk(at,depth,p,dp,pplus,pminus,crossings){
    if(depth===N){
      const O=observable(counts,N);
      const score=-ell*crossings-N*dlogrho+dlogr[at];
      histories++;mass+=p;scoreMean+=p*score;mean+=p*O;
      scoreSource+=p*O*score;directSource+=dp*O;
      plus+=pplus*O;minus+=pminus*O;
      noTerminal+=p*O*(score-dlogr[at]);
      noPressure+=p*O*(score+N*dlogrho);
      if(O===0)failedMass+=p;
      return;
    }
    for(let next=0;next<3;next++)if(next!==at){
      counts[at][next]++;
      walk(next,depth+1,p*base.P[at][next],
        dp*base.P[at][next]+p*Pdot[at][next],
        pplus*up.P[at][next],pminus*down.P[at][next],
        crossings+cross(at,next));
      counts[at][next]--;
    }
  }
  for(let start=0;start<3;start++)
    walk(start,0,base.mu[start],base.mu[start]*dlogr[start],
      up.mu[start],down.mu[start],0);
  const fd=(plus-minus)/2e-4;
  near(mass,1,1e-9,"complete original multiplicity normalization");
  near(scoreMean,0,1e-9,"whole score mean");
  near(scoreSource,directSource,1e-15,"score and independent recursive product derivative");
  near(scoreSource,fd,3e-13,"central difference");
  assert(Math.abs(noTerminal-scoreSource)>1e-14,"terminal term matters");
  assert(Math.abs(noPressure-scoreSource)>1e-14,"Perron pressure matters");
  return {N,zoneHistories:histories,normalizedMass:mass,failedMass,
    empiricalMean:mean,targetJ3:J3,valueError:mean-J3,
    scoreSource,independentProductSource:directSource,centralDifference:fd,
    targetAnalyticSource:source,sourceError:scoreSource-source,
    omittedTerminalSource:noTerminal,omittedPressureSource:noPressure,
    scoreMean};
}
const results=[4,8,12,16,20].map(exhaustive);
console.log(JSON.stringify({
  status:"PASS",originalVertices:33,originalDirectedEdges:718,
  nativeZoneSizes:parts,full33TargetJ:J33,analyticTargetSource:source,
  fixedZoneMassCutoff:cutoff,results,
  scope:"Exact native zone-lumped complete path source controls. Universal full33 C1 recovery is proved separately; empirical convergence rates are not inferred from this finite table."
},null,2));
