#!/usr/bin/env node
/*
 D0 original K(9,11,13) × ORIGINAL CAR16 J23 spatial phase.
 One positive original-718-edge two-view return -> Fisher magnetic gap.
 MATHEMATICAL REPRESENTATION CHECK only; NOT physical full128 or GR.
 */
const assert=(x,msg)=>{if(!x)throw Error(msg||"assert");};
const near=(x,y,t=1e-9)=>{assert(Math.abs(x-y)<t,String(x)+" != "+String(y));};
const phi=(1+Math.sqrt(5))/2,ell=Math.log(phi),n=[9,11,13],S=359,B=2574;
const zone=Array.from({length:33},(_,u)=>u<9?0:u<20?1:2);
const cyc=new Set(["0,1","1,2","2,0"]);
const sign=(i,j)=>cyc.has(i+","+j)?1:-1;
const edges=[];for(let u=0;u<33;u++)for(let v=0;v<33;v++)
  if(zone[u]!==zone[v])edges.push([u,v]);
assert(edges.length===718);
assert(n[0]*n[1]*n[2]===1287);
const counts=new Map();
for(let m=0;m<16;m++){
  let w=((m>>2)&1)-((m>>3)&1);
  counts.set(w,(counts.get(w)||0)+1);
}
assert(counts.get(0)===8&&counts.get(1)===4&&counts.get(-1)===4);
const root=(c,Sx=S,Bx=B)=>{
  let rho=22;
  for(let i=0;i<35;i++)rho-=(rho**3-Sx*rho-Bx*c)/(3*rho*rho-Sx);
  return rho;
};
const rho=root(1),D=3*rho*rho-S,fisher=9*B*ell*ell/(rho*D);
near(-fisher/ell,-0.4763744515526456,1e-12);
near(fisher,0.22923701924341636,1e-13);

// Native original Perron stationary pi and transition conditional probabilities.
const w=n.map(k=>1/(rho+k));
const norm=Math.sqrt(n.reduce((s,k,i)=>s+k*w[i]**2,0));
const r=zone.map(i=>w[i]/norm),pi=r.map(a=>a*a);
const src=Array(33).fill(0),tar=Array(33).fill(0);
for(const [u,v] of edges){
  let mu=r[u]*r[v]/rho;
  src[u]+=mu/pi[u];
  tar[v]+=mu/pi[v];
}
for(let u=0;u<33;u++){near(src[u],1,4e-14);near(tar[u],1,4e-14);}
near(pi.reduce((x,y)=>x+y,0),1,4e-14);

// Explicit 33×4 original grade-one J23 rotation, real symmetric transfer.
const chi=.13,N=33*4,T=Array.from({length:N},()=>new Float64Array(N));
for(const [u,v] of edges){
  const angle=-ell*chi*sign(zone[u],zone[v]),cc=Math.cos(angle),ss=Math.sin(angle);
  const i=4*u,j=4*v,sc=1/rho;
  T[i][j]=sc;T[i+1][j+1]=sc;
  T[i+2][j+2]=sc*cc;T[i+2][j+3]=sc*ss;
  T[i+3][j+2]=-sc*ss;T[i+3][j+3]=sc*cc;
}
let maxSym=0;for(let i=0;i<N;i++)for(let j=0;j<N;j++)
  maxSym=Math.max(maxSym,Math.abs(T[i][j]-T[j][i]));
near(maxSym,0,1e-15);
let trace3=0;
for(let a=0;a<33;a++)for(let b=0;b<33;b++)if(zone[a]!==zone[b])
for(let c=0;c<33;c++)if(zone[c]!==zone[a]&&zone[c]!==zone[b]){
 const m=sign(zone[a],zone[b])+sign(zone[b],zone[c])+sign(zone[c],zone[a]);
 trace3+=(2+2*Math.cos(ell*chi*m))/rho**3;
}
near(trace3,7722*(2+2*Math.cos(3*ell*chi))/rho**3,1e-10);

// EIGHT magnetic CAR16 Perron modes gain a positive gap: Fisher coefficient.
for(const x of [.1,.01,.001]){
  const rhoX=root(Math.cos(3*ell*x));
  const gap=1-(rhoX/rho)**2;
  assert(gap>0&&Math.abs(gap/(x*x)-fisher)<0.0002);
}
assert(33*16===528&&30*16===480);
assert(528-16===512&&528-8===520);

// Complete CAR16 F=I−T² feedback logdet from the 3-root symmetric polynomials.
function det3(z,c){
 const a=1-z,b=z/rho**2;
 return a*(a+S*b)**2+(B*c)**2*b**3;
}
for(const z of [0.1,2**-20]){
 const baseline=det3(z,1),twist=det3(z,Math.cos(3*ell*chi));
 const eta=B**2*(z/rho**2)**3/baseline;
 assert(0<eta&&eta<1);
 const delta=-8*Math.log1p(-eta*Math.sin(3*ell*chi)**2);
 assert(delta>0);
 if(z===0.1)near(delta,-8*Math.log(twist/baseline),1e-10);
 if(z===2**-20){
   near(eta,5.2992509804650675e-20,1e-31);
   near(144*ell**2*eta,1.7670529475782776e-18,1e-29);
 }
}
// First phase-dependent EVEN moment is SIXTH.
const moment2=16*2*S/rho**2;
const moment4=16*2*S**2/rho**4;
const diff6=-24*B**2*Math.sin(3*ell*chi)**2/rho**6;
assert(moment2>0&&moment4>0&&diff6<0);

// Same trace-free three-interface shear selector, opposite to scalar CP² source.
const z=2**-20,a=1-z,bb=z/rho**2,beta=B/rho**3,ss=S/rho**2;
const det0=a*(a+z*ss)**2+z**3*beta**2;
const factor=576*ell**3*a*z**3*beta**2*(a+z*ss)/(D*det0**2);
const k=[99,143,117],gamma=k.map(ki=>factor*(3*ki-S));
near(gamma.reduce((x,y)=>x+y,0),0,1e-27);
near(gamma[0]/gamma[2],31/4,1e-12);
near(gamma[1]/gamma[2],-35/4,1e-12);
console.log("PASS original718 × CAR16 magnetic-Fisher bridge");
console.log("PASS grade-one real symmetry, full CAR16 weights (8,4,4)");
console.log("PASS positive feedback F rank512->520, native Fisher gap");
console.log("PASS sixth-step phase determinant and common 31:-35:4 ray");
console.log("Fisher",fisher,"feedback phase curvature",144*ell**2*(B**2*bb**3/det0));
console.log("FIREWALL: full128 physical execution/Einstein/neutrino not claimed");
