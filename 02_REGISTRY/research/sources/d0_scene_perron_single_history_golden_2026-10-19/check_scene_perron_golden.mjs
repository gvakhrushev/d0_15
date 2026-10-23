#!/usr/bin/env node
// D0 K(9,11,13) real scene Perron Cost-Info, stationary full source,
// one correlated F/R universal Markov code. Deterministic, no dependencies.
// Does NOT prove native physical Book/Cost-Info selection or physical GR.
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi),bphi=2+Math.log(2)/ell;
const fail=(what)=>{throw Error(what)};
const near=(a,b,tol=1e-9)=>{if(Math.abs(a-b)>tol)fail("mismatch: "+a+" != "+b)};
const groups=Array.from({length:33},(_,i)=>i<9?0:i<20?1:2),edges=[],degrees=[];
for(let i=0;i<33;i++){degrees[i]=0;for(let j=0;j<33;j++)if(groups[i]!==groups[j]){edges.push([i,j]);degrees[i]++;}}
if(edges.length!==718||degrees.reduce((s,d)=>s+d*d,0)!==15708
 ||degrees.reduce((s,d)=>s+d-1,0)!==685)fail("not original K9/11/13 scene");

function nativeTransfer(theta,t){
 const M=Array.from({length:33},()=>new Float64Array(33));
 const I=Array.from({length:33},(_,v)=>.2*(v%5)+.09*Math.sin(.6*(v+1)*t));
 for(const [u,v] of edges){
  const C=1+.027*((3*u+7*v)%11)+.018*t*((u+3*v)%5);
  M[u][v]=Math.exp(-ell*(C-theta*I[u]-(1-theta)*I[v]));
 }
 return M;
}
function times(M,v,tr=false){
 const out=new Float64Array(33);
 for(let i=0;i<33;i++)for(let j=0;j<33;j++){
  if(tr)out[j]+=v[i]*M[i][j];else out[i]+=M[i][j]*v[j];
 }
 return out;
}
function pf(M,tr=false){
 let v=new Float64Array(33).fill(1/33);
 for(let k=0;k<1000;k++){
  let w=times(M,v,tr),sum=w.reduce((x,y)=>x+y,0);
  for(let i=0;i<33;i++)w[i]/=sum;
  const err=Math.max(...w.map((x,i)=>Math.abs(x-v[i])));
  v=w;if(err<1e-16)break;
 }
 return {v,lambda:times(M,v,tr).reduce((s,x)=>s+x,0)};
}
function scene(theta,t){
 const M=nativeTransfer(theta,t),a=pf(M),b=pf(M,true);
 const r=a.v,l=b.v,lambda=a.lambda;
 const pi=l.map((x,i)=>x*r[i]),norm=pi.reduce((s,x)=>s+x,0);
 for(let i=0;i<33;i++)pi[i]/=norm;
 const P=M.map((row,i)=>Float64Array.from(row,(value,j)=>value*r[j]/(lambda*r[i])));
 for(let i=0;i<33;i++){
  near(P[i].reduce((s,x)=>s+x,0),1,1e-12);
  near(P.reduce((s,row,j)=>s+pi[j]*row[i],0),pi[i],1e-12);
 }
 return {M,P,pi,lambda,r,l};
}
function invert(matrix){
 const n=matrix.length,A=matrix.map((row,i)=>[...row,...Array.from({length:n},(_,j)=>+(i===j))]);
 for(let k=0;k<n;k++){
  let pivot=k;for(let i=k+1;i<n;i++)if(Math.abs(A[i][k])>Math.abs(A[pivot][k]))pivot=i;
  if(Math.abs(A[pivot][k])<1e-14)fail("singular stationary system");
  [A[pivot],A[k]]=[A[k],A[pivot]];
  const d=A[k][k];for(let j=0;j<2*n;j++)A[k][j]/=d;
  for(let i=0;i<n;i++)if(i!==k){const f=A[i][k];for(let j=0;j<2*n;j++)A[i][j]-=f*A[k][j];}
 }
 return A.map(row=>row.slice(n));
}
const t=.41,th=.25,base=scene(th,t);
const allocations=[-.6,0,th,.6,1.3];
let maxKernel=0,maxPi=0,maxRoot=0;
for(const theta of allocations){
 const m=scene(theta,t);
 maxRoot=Math.max(maxRoot,Math.abs(m.lambda-base.lambda));
 for(let i=0;i<33;i++){
  maxPi=Math.max(maxPi,Math.abs(m.pi[i]-base.pi[i]));
  for(let j=0;j<33;j++)maxKernel=Math.max(maxKernel,Math.abs(m.P[i][j]-base.P[i][j]));
 }
}
if(maxKernel>1e-12||maxPi>1e-12||maxRoot>1e-11)fail("Info diagonal Perron quotient failed");
// Exact field-source gradient and genuine moving stationary preparation.
const h=1e-5,up=scene(th,t+h),down=scene(th,t-h);
const dlogLambda=(Math.log(up.lambda)-Math.log(down.lambda))/(2*h);
let priceSource=0,entropy=0,meanS=0,relativeKL=0;
for(const [u,v] of edges){
 const w=base.pi[u]*base.P[u][v];
 priceSource+=w*(Math.log(up.M[u][v])-Math.log(down.M[u][v]))/(2*h);
 entropy-=w*Math.log(base.P[u][v])/ell;
 meanS-=w*Math.log(base.M[u][v])/ell;
 const alt=1/degrees[u];
 relativeKL+=degrees[u]/718*alt*Math.log(alt/base.P[u][v])/ell;
}
near(dlogLambda,priceSource,1e-8);
near(entropy,meanS+Math.log(base.lambda)/ell,1e-11);
const uniformEntropy=degrees.reduce((s,d)=>s+d/718*Math.log(d)/ell,0);
const uniformMean=edges.reduce((s,[u,v])=>s-degrees[u]/718/degrees[u]*Math.log(base.M[u][v])/ell,0);
near(Math.log(base.lambda)/ell-uniformEntropy+uniformMean,relativeKL,1e-10);
if(relativeKL<=0)fail("variational principle not strict");
const matrix=base.P.map((row,i)=>Array.from(row,(x,j)=>(i===j?1:0)-x+base.pi[j]));
const Mi=invert(matrix),dpi=new Float64Array(33);
for(let i=0;i<33;i++)for(let j=0;j<33;j++){
 const dP=(up.P[i][j]-down.P[i][j])/(2*h);
 for(let k=0;k<33;k++)dpi[k]+=base.pi[i]*dP*Mi[j][k];
}
let maxPreparation=0;
for(let j=0;j<33;j++)maxPreparation=Math.max(maxPreparation,Math.abs(dpi[j]-(up.pi[j]-down.pi[j])/(2*h)));
if(maxPreparation>1e-8)fail("real old stationary preparation source mismatch");

// SINGLE correlated native Golden Markov history: full finite enumeration on a
// THREE-VERTEX native triangle only, global 33/718 theorem remains analytic.
const factorial=[1];for(let j=1;j<=16;j++)factorial[j]=factorial[j-1]*j;
const neighbors=[[1,2],[0,2],[0,1]];
function triangle(y){
 const a=p*Math.exp(y)/(p*Math.exp(y)+p*p*Math.exp(-y)),ap=2*a*(1-a);
 const b=p*p,c=p;
 const W=[b+c-b*c,1-c+a*c,1-a*b],dW=[0,c*ap,-b*ap],
       total=W.reduce((s,v)=>s+v,0),dtot=dW.reduce((s,v)=>s+v,0);
 const pi=W.map(v=>v/total),dip=W.map((v,i)=>(dW[i]*total-v*dtot)/(total*total));
 const P=[[0,a,1-a],[b,0,1-b],[c,1-c,0]],dP=[[0,ap,-ap],[0,0,0],[0,0,0]];
 for(let i=0;i<3;i++)near(pi.reduce((s,v,j)=>s+v*P[j][i],0),pi[i],1e-14);
 return {pi,dip,P,dP};
}
function markovQ(path){
 const cnt=Array.from({length:3},()=>[0,0]);
 for(let i=1;i<path.length;i++){const j=neighbors[path[i-1]].indexOf(path[i]);cnt[path[i-1]][j]++;}
 return cnt.reduce((s,[a,b])=>s*factorial[a]*factorial[b]/factorial[a+b+1],1/3);
}
function pathProb(path,m){
 let q=m.pi[path[0]],score=m.dip[path[0]]/m.pi[path[0]];
 for(let i=1;i<path.length;i++){
  const a=path[i-1],b=path[i],pab=m.P[a][b];
  q*=pab;score+=m.dP[a][b]/pab;
 }
 return {q,score};
}
function goldenCode(start,weight){
 const middle=start+weight/2,end=start+weight;
 let lower=0,width=1,code="",cost=0;
 for(let i=0;i<150&&width>weight/2;i++){
  if(middle<lower+p*width){code+="F";cost++;width*=p;}
  else {code+="R";cost+=2;lower+=p*width;width*=p*p;}
 }
 if(lower<start-1e-8||lower+width>end+1e-8)fail("wrong native Golden F/R interval");
 return {code,cost,excess:cost+Math.log(weight)/ell};
}
function completeTriangle(N,y=.23){
 const paths=[];
 function visit(arr,k){if(k===0){paths.push(arr);return;}for(const v of neighbors[arr.at(-1)])visit([...arr,v],k-1);}
 for(let i=0;i<3;i++)visit([i],N);
 const m=triangle(y);
 let totalQ=0,totalP=0,totalScore=0,ec=0,dec=0,H=0,dH=0,maxOverhead=0,codes=[];
 for(const path of paths){
  const Q=markovQ(path),G=goldenCode(totalQ,Q),{q,score}=pathProb(path,m);
  if(Q<q/(3*(N+2)**3)-1e-13)fail("Dirichlet-MLE path-regret bound");
  totalQ+=Q;totalP+=q;totalScore+=q*score;
  ec+=q*G.cost;dec+=q*score*G.cost;
  H-=q*Math.log(q)/ell;dH-=q*score*Math.log(q)/ell;
  maxOverhead=Math.max(maxOverhead,G.excess);codes.push(G.code);
 }
 near(totalQ,1,1e-9);near(totalP,1,1e-9);near(totalScore,0,1e-9);
 codes.sort();for(let j=1;j<codes.length;j++)if(codes[j].startsWith(codes[j-1]))fail("not prefix-free");
 const upper=(3*Math.log(N+2)+Math.log(3))/ell+bphi;
 if(ec-H<-.000001||ec-H>upper+1e-8||maxOverhead>bphi+1e-8)fail("native Golden coding bounds");
 return {N,paths:paths.length,meanCodeRate:ec/N,entropyRate:H/N,
         excessRate:(ec-H)/N,sourceExcessRate:(dec-dH)/N};
}
const triangleRuns=[2,3,4,5,6,8,10].map(N=>completeTriangle(N));
console.log(JSON.stringify({
 status:"PASS",scene:{vertices:33,directedEdges:edges.length,twoStepWalks:degrees.reduce((s,d)=>s+d*d,0),
               stochasticDimensions:degrees.reduce((s,d)=>s+d-1,0)},
 allocationTest:{values:allocations,maxKernelDifference:maxKernel,maxStationaryPreparationDifference:maxPi,maxPressureRootDifference:maxRoot},
 movingSource:{pressureDerivative:dlogLambda,actualEdgeScore:priceSource,fullPreparationDerivativeError:maxPreparation},
 variationalCost:{goldenEntropyRate:entropy,meanNativeEdgePrice:meanS,
                  partitionPressure:Math.log(base.lambda)/ell,alternativeUniformKLgap:relativeKL},
 oneCorrelatedHistoryCode:triangleRuns,
 boundary:"canonical Perron stationary path model with GIVEN scene Cost/Info only; NOT compulsory physical D0 Book action or GR."
},null,2));
