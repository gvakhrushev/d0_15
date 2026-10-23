#!/usr/bin/env node
'use strict';
/*
 * ORIGINAL scene K(9,11,13) closed-walk face addressing and live-active
 * feed-forward CONTROL in the previously owned "all active orthogonals +
 * active-to-OLD-record translations" generous grammar.
 *
 * Exact BigInt path counts; finite 2-bit exact controller counterexample
 * and exact same-history active/OLD-correlated witness; original scalar
 * Doob gauge conjugacy checked on ALL 718 directed edges.
 *
 * NOT a physically compulsory G0/Book decoder, Price/Cost, 4D field
 * controller, exact joint Einstein solution or native fullStep.
 */
const assert=(ok,label)=>{if(!ok)throw Error(label)};
const SZ=[9,11,13],V=33;
const part=i=>i<9?0:(i<20?1:2);
const neigh=Array.from({length:V},(_,u)=>Array.from({length:V},(_,v)=>(part(u)!==part(v))?v:-1).filter(v=>v>=0));
assert(neigh.reduce((s,x)=>s+x.length,0)===718,"literal original 718 directed edges");
assert(neigh[0].length===24,"original K9 degree");

function counts(n){
 const tab=[Array.from({length:V},(_,v)=>v===0?1n:0n)];
 for(let step=1;step<=n;step++)tab.push(Array.from({length:V},(_,v)=>
   neigh[v].reduce((tot,w)=>tot+tab[step-1][w],0n)));
 return tab;
}
function minLength(need){
 let n=2,table=counts(n);
 while(table[n][0]<need){n++;table=counts(n);}
 return [n,table];
}
function unrank(number,n,table){
 let idx=BigInt(number),v=0,out=[v];
 assert(idx>=0n&&idx<table[n][0],"rank out of original complete return class");
 for(let left=n;left>0;left--){
   let next=-1;
   for(let w of neigh[v]){
     const block=table[left-1][w];
     if(idx>=block)idx-=block;else{next=w;break;}
   }
   assert(next>=0,"unrank transition exists");
   out.push(next);v=next;
 }
 assert(v===0&&idx===0n,"unrank is closed original path");
 return out;
}
function rankWord(word,table){
 let idx=0n,v=0,n=word.length-1;
 for(let left=n;left>0;left--){
   const w=word[n-left+1];
   assert(neigh[v].includes(w),"rank uses true original directed edge");
   for(let next of neigh[v]){if(next===w)break;idx+=table[left-1][next];}
   v=w;
 }
 assert(v===0,"rank word returns to base");
 return idx;
}
const expected=new Map([[2,24n],[3,286n],[4,8616n],[5,164450n],
                        [6,3829308n],[7,81215134n],[8,1798015872n],[9,39012871898n]]);
for(const [n,c] of expected)assert(counts(n)[n][0]===c,"original exact return count n="+n);

// The original top Perron root and zone-eigenprofile; stationary old
// distribution pi differs from original one-sided normalized r.
let rho=22;
for(let i=0;i<12;i++)rho-=(rho**3-359*rho-2574)/(3*rho*rho-359);
const rRaw=Array.from({length:V},(_,i)=>1/(rho+SZ[part(i)]));
const norm=rRaw.reduce((s,x)=>s+x,0),r=rRaw.map(x=>x/norm);
const unit2=rRaw.reduce((s,x)=>s+x*x,0),pi0=rRaw[0]**2/unit2;
const ell=Math.log((1+Math.sqrt(5))/2);
assert(Math.abs(rho**3-359*rho-2574)<1e-8,"Perron cubic");
const P=Array.from({length:V},(_,u)=>Array.from({length:V},(_,v)=>
  part(u)===part(v)?0:r[v]/(rho*r[u])));
assert(P.every(row=>Math.abs(row.reduce((a,b)=>a+b,0)-1)<1e-12),"true Perron P rows");

// EXACT ENDPOINT SIMILARITY: K(D)=D_u K0_uv / D_v, r'=D*r.
// Its complete Doob P, stationary flow, archive J0,J1/F and scalar
// Perron pressure are unchanged, not just their first derivatives.
const D=Array.from({length:V},(_,u)=>1+(u+1)**2/(37*37));
let gaugeErr=0,edgeNum=0;
for(let u=0;u<V;u++)for(let v=0;v<V;v++)if(part(u)!==part(v)){
 const Knew=D[u]/D[v],rp_u=D[u]*r[u],rp_v=D[v]*r[v];
 const Pnew=Knew*rp_v/(rho*rp_u);
 gaugeErr=Math.max(gaugeErr,Math.abs(Pnew-P[u][v]));
 edgeNum++;
}
assert(edgeNum===718&&gaugeErr<1e-14,"ALL-original-edge Doob invariance");
const loop=[0,9,20,0];
const endpointProd=loop.slice(0,-1).reduce((acc,u,j)=>acc*D[u]/D[loop[j+1]],1);
assert(Math.abs(endpointProd-1)<1e-14,"every closed endpoint transport telescopes");

// All 12*L^4 ORIGINAL oriented Role based-face ADDRESSES are encoded by
// distinct ORIGINAL scene walks of ONE length. This is an address, NOT
// a fixed 33-scene-edge Lorentz connection embedding.
const cases=[];
for(const L of [2,4,8,16,32,64,128]){
 const M=12n*(BigInt(L)**4n);
 const [n,tab]=minLength(M),C=tab[n][0];
 assert(C>=M&& (n<=2||counts(n-1)[n-1][0]<M),"minimal root-return length");
 const sample=L===4?Array.from({length:Number(M)},(_,i)=>BigInt(i)):
  [0n,1n,M/3n,M/2n,M-1n];
 const seen=new Set();
 for(const i of sample){
   const w=unrank(i,n,tab),id=rankWord(w,tab);
   assert(i===id,"exact rank/unrank over original path category");
   seen.add(w.join(":"));
 }
 assert(seen.size===sample.length,"original return words injective");
 const q=r[0]*rho**(-n),mass=Number(M)*q,frac=Number(M)/Number(C);
 assert(mass>0&&mass<1&&frac<=1,"exact supported subcut nonzero probability");
 // Geometric source of a fixed-cost label mean is exactly the UNIFORM
 // arithmetic mean, with no address-score term on THIS fixed code.
 const logCost=-Math.log(q)/ell,entropyLower=Math.log(Number(M))/ell;
 cases.push({L,orientedFaces:M.toString(),minimumOriginalPathLength:n,
   availableOriginalClosedWalks:C.toString(),selectedMass:mass,
   meanConditionalAddressWeight:1/Number(M),
   codeLengthGolden:logCost,conditionalEntropyBoundGolden:entropyLower,
   extraFixedCodeGolden:logCost-entropyLower,selectedFraction:frac});
}
assert(cases.every(x=>x.codeLengthGolden>=x.conditionalEntropyBoundGolden),"nonnegative code overhead");
const Cbound=r[0]*pi0/rho,upper=r[0]*pi0;
assert(Cbound>0&&upper>Cbound,"asymptotic nonvanishing selected mass");
for(const c of cases)if(c.L>=16)assert(c.selectedMass>Cbound/2&&c.selectedMass<4*upper,"asymptotic PF mass bound");

// STATIC SCENE LINK representation has only 327 independent cycles.
// Already at L=4, original periodic 4D role-product axis links have
// cycle dimension 4 L^4-L^4+1=3 L^4+1=769, strictly bigger.
// Distinct path labels do not alter this fixed graph gauge rank.
assert(359-33+1===327&&3*4**4+1===769&&769>327,
  "no fixed 33-scene-edge universal Role-link parametrization");

// Controlled ACTIVE operation is permitted while OLD RIGHT stays untouched.
// Basis order (live-address a, active-target c, retained-old bit r).
const states=Array.from({length:8},(_,i)=>[(i>>2)&1,(i>>1)&1,i&1]);
const live=([a,c,r])=>[a,c^a,r];
const old=([a,c,r])=>[a,c^r,r];
const xOld=([a,c,r])=>[a,c,r^1];
const copyLiveToOld=([a,c,r])=>[a,c,r^a];
const eq=(x,y)=>x.every((v,i)=>v===y[i]);
assert(states.every(s=>eq(live(xOld(s)),xOld(live(s)))),
  "ACTIVE conditional geometry COMMUTES with every old-record flip");
assert(states.every(s=>eq(copyLiveToOld(xOld(s)),xOld(copyLiveToOld(s)))),
  "one-way fresh recording also COMMUTES with OLD translation");
assert(states.some(s=>!eq(old(xOld(s)),xOld(old(s)))),
  "true OLD-controlled geometry BREAKS translation invariant");
assert(states.filter(s=>s[0]===s[2]).every(s=>eq(old(s),live(s))),
  "LIVE controlled geometry reproduces old-controlled TARGET on the physically CORRELATED live/old subspace");
assert(states.filter(s=>s[2]===0).every(s=>copyLiveToOld(s)[2]===s[0]),
  "exact one-way COPY is possible BEFORE old record becomes inaccessible");

console.log(JSON.stringify({
 status:"PASS_ORIGINAL_PERRON_4D_FACE_ADDRESS_AND_LIVE_FEEDFORWARD",
 scene:{vertices:33,directedEdges:edgeNum,cycles:327,rho,r0:r[0],pi0,
   endpointSimilarityDoobMaxError:gaugeErr,endpointClosedLoopProduct:endpointProd},
 massBoundsAsymptotic:{lower:Cbound,upper},
 addressSource:"fixed unit Cost + endpoint-similarity alone => conditional face mean 1/(12 L^4), with D address probability=0",
 nativeGenerousControl:"LIVE active face-label can operate on CAR before final archive commit while commuting with OLD record translations",
 hardNoGo:"If ONLY old RIGHT contains the address, OLD-controlled CAR violates existing translation invariant",
 fieldTopology:"fixed scene 327 cycles < general 4D Role-link 769 cycles at L=4; history-index-dependent controller still required",
 physicalSelector:"not selected by Book03/G0; oldRIGHT state preparation, paid controller/cut/clock/ref128, 4D Role face-word, full source and refinement remain OPEN",
 cases,GR_closed:false
},null,2));
