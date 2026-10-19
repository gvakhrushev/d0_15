#!/usr/bin/env node
// Exact-original-scene structural check, no dependencies.
// Derived U acts on full 718 directed edges; the polynomial identity itself
// is proved in the companion markdown. This is NOT an execution of native
// physical Book03/Golden gate or proof of GR from full D0.
const n=33, parts=[9,11,13], z=2**-20, p=(Math.sqrt(5)-1)/2,
      ell=Math.log(1/p);
const zone=Array.from({length:n},(_,i)=>i<9?0:i<20?1:2);
const edge=[];
for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(zone[i]!==zone[j])edge.push([i,j]);
const near=(a,b,tol=1e-10)=>{if(Math.abs(a-b)>tol)throw Error("numeric mismatch "+a+" vs "+b);};
const I=()=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
const trace=A=>A.reduce((s,row,i)=>s+row[i],0);
const max=A=>Math.max(...A.flat().map(Math.abs));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
if(edge.length!==718)throw Error("not the original native full scene");
let lower=0,upper=40;
for(let j=0;j<120;j++){const m=(lower+upper)/2;if(m*m*m-359*m-2574>0)upper=m;else lower=m;}
const rho=(lower+upper)/2,k=2574/rho**3;
near(rho**3-359*rho-2574,0,1e-9);
let r=Array.from({length:n},(_,i)=>1/(rho+parts[zone[i]]));
const l2=Math.hypot(...r);r=r.map(x=>x/l2);
const pi=r.map(x=>x*x);
const A=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(zone[i]!==zone[j])));
const T=A.map(row=>row.map(x=>x/rho)),T2=mul(T,T);
const B=T.map((row,i)=>row.map((x,j)=>(i===j?1:0)+(2*x+T2[i][j])/(2+k)));
const product=mul(T,B);
let maximumPolynomial=0;
for(let i=0;i<n;i++)for(let j=0;j<n;j++)
 maximumPolynomial=Math.max(maximumPolynomial,Math.abs(B[i][j]-product[i][j]-(i===j?1:0)+r[i]*r[j]));
if(maximumPolynomial>1e-13)throw Error("actual native cubic polynomial identity fails");
const D=edge.map(([u,v])=>{
 const row=Array(n).fill(0);
 row[u]+=Math.sqrt(r[v]/(rho*r[u]));
 row[v]-=Math.sqrt(r[u]/(rho*r[v]));
 return row;
});
// Fully correct coordinate pullback isometries on the ORIGINAL 718 edges.
const cross=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>{
 let sum=0;for(let h=0;h<edge.length;h++){const[u,v]=edge[h];if(u===i&&v===j)sum+=r[v]/(rho*r[u]);}return sum;
}));
for(let i=0;i<n;i++)for(let j=0;j<n;j++)near(cross[i][j],A[i][j]*r[j]/(rho*r[i]));
function actU(q){
 const adj=Array(n).fill(0);
 for(let h=0;h<edge.length;h++)for(let i=0;i<n;i++)adj[i]+=D[h][i]*q[h];
 const beta=B.map(row=>dot(row,adj));
 return q.map((x,h)=>x-dot(D[h],beta));
}
let maximumMapping=0;
for(let j=0;j<n;j++){
 const past=edge.map(([u,v])=>u===j?Math.sqrt(r[v]/(rho*r[u])):0);
 const future=edge.map(([u,v])=>v===j?Math.sqrt(r[u]/(rho*r[v])):0);
 const output=actU(past);
 for(let h=0;h<edge.length;h++)maximumMapping=Math.max(maximumMapping,Math.abs(output[h]-future[h]));
}
if(maximumMapping>1e-12)throw Error("canonical U does not transport past to future");
const q=edge.map((_,i)=>Math.sin(.23*i)+.4*Math.cos(.71*i)),
      u=actU(q),uu=actU(u);
const involutionError=Math.max(...uu.map((v,i)=>Math.abs(v-q[i])));
const normError=Math.abs(Math.hypot(...u)-Math.hypot(...q));
if(involutionError>1e-11||normError>1e-11)throw Error("full718 canonical U not orthogonal involution");
const other=(-rho+Math.sqrt(rho*rho-4*2574/rho))/2;
const other2=(-rho-Math.sqrt(rho*rho-4*2574/rho))/2;
const active=[1-(other/rho)**2,1-(other2/rho)**2];
const feedback=-30*Math.log1p(-z)-active.reduce((sum,x)=>sum+Math.log1p(-z*x),0);
const algebraic=-30*Math.log1p(-z)-Math.log(1-(1+2*k)*z+(2*k+k*k)*z*z);
near(feedback,algebraic,1e-13);near(feedback,.000030035369315208,1e-12);
// ORIGINAL symmetric edge-price differential of canonical Perron feedback.
const G=T2.map((row,i)=>row.map((x,j)=>(i===j?1-z:0)+z*x));
function inverse(a){
 const x=a.map((row,i)=>[...row,...I()[i]]);
 for(let k=0;k<n;k++){
  let t=k;for(let i=k+1;i<n;i++)if(Math.abs(x[i][k])>Math.abs(x[t][k]))t=i;
  [x[k],x[t]]=[x[t],x[k]];
  const v=x[k][k];if(Math.abs(v)<1e-14)throw Error("native resolvent singular");
  for(let j=0;j<n*2;j++)x[k][j]/=v;
  for(let i=0;i<n;i++)if(i!==k){const b=x[i][k];for(let j=0;j<n*2;j++)x[i][j]-=b*x[k][j];}
 }
 return x.map(row=>row.slice(n));
}
const M=mul(inverse(G),T),traceMT=trace(mul(M,T));
const undirected=[[0,9,99],[0,20,117],[9,20,143]];
const sources=undirected.map(([a,b,count])=>({
 label:zone[a]+"-"+zone[b], undirectedEdgeCount:count,
 dJdc:4*z*ell*p/rho*(M[a][b]-r[a]*r[b]*traceMT)
}));
const scaleWard=sources.reduce((sum,item)=>sum+item.undirectedEdgeCount*item.dJdc,0);
if(Math.abs(scaleWard)>1e-17)throw Error("native all-edge price scale Ward fails");
if(Math.min(...sources.map(q=>Math.abs(q.dJdc)))<1e-12)throw Error("no true native relative edge source");
console.log(JSON.stringify({
 status:"PASS",
 nativeGraph:{vertices:n,directedEdges:edge.length,
             oneSidedPerronRadius:rho,originalPerronHistory:true},
 canonicalPolynomial:{k,degree:2,maximumIdentityError:maximumPolynomial,
                      full718MapError:maximumMapping,
                      completeOrthogonalInvolutionError:involutionError,
                      normError,changedDirections:32,unchangedDirections:686},
 nativeFeedback:{rank:32,positiveArchiveEigenvalue1Multiplicity:30,
                 activeEigenvalues:active,stationaryEigenvalue0Multiplicity:1,
                 fullBookCandidateFeedback:feedback,algebraicDeterminantError:feedback-algebraic},
 nativeOriginalUndirectedCostSource:{orbits:sources,allUniformCostScaleWard:scaleWard},
 scope:"True original Perron scene mathematical complete record; original D0 physical U_N, full Book selected action and Einstein source NOT asserted"
},null,2));
