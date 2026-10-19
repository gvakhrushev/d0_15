#!/usr/bin/env node
"use strict";
/*
 * Exact finite Golden LEFT ORIGINAL F/R same-cost prefix semantics and
 * LIVE active → fresh archive feed-forward controls, using the pre-existing
 * generous active-orthogonal + one-way CNOT grammar.
 *
 * The actual original x(w) Golden 4D native address is already OWNED by
 * A4D_BALANCED_NATIVE_GOLDEN_EXACT_SOURCE_SEAM_LOCAL_TO_VOLUME_MEAN;
 * this checker does NOT replace/readdress it and its small sample cells
 * are ONLY a miniature active-controller test.
 *
 * No physically compulsory G0 fullStep/controller, H+J+R price or GR claim.
 */
const check=(c,m)=>{if(!c)throw Error(m)};
const p=(Math.sqrt(5)-1)/2,a=Math.sqrt(p);
const ell=Math.log((1+Math.sqrt(5))/2);
check(Math.abs(p+p*p-1)<2e-15,"original Golden p+p²");
const G=[[a,-p],[p,a]];
const XG=[[p,a],[a,-p]];  // Xflip G, original flat Julia(p I)
const ortho=M=>Math.abs(M[0][0]**2+M[1][0]**2-1)<2e-14 &&
 Math.abs(M[0][1]**2+M[1][1]**2-1)<2e-14 &&
 Math.abs(M[0][0]*M[0][1]+M[1][0]*M[1][1])<2e-14;
check(ortho(G)&&ortho(XG),"literal original primitive Golden G and XG are orthogonal");
check(Math.abs(XG[0][0]**2-p*p)<1e-15&&Math.abs(XG[1][0]**2-p)<1e-15,
  "complete native Golden Good/Bad flat probabilities are (p²,p)");

const costs={F:1,R:2};
function allWords(n){
 const out=[];
 function recurse(n,word){if(n===0){out.push(word);return;}if(n>=1)recurse(n-1,word+"F");if(n>=2)recurse(n-2,word+"R");}
 recurse(n,"");return out;
}
let fib=[1,1];
for(let k=2;k<=25;k++)fib[k]=fib[k-1]+fib[k-2];
for(let n=1;n<=20;n++){
 const words=allWords(n);
 check(words.length===fib[n],"Fibonacci-native count cost "+n);
 check(new Set(words).size===words.length,"full Golden F/R old LEFT word labels distinct");
 check(words.every(w=>[...w].reduce((s,c)=>s+costs[c],0)===n),"original weighted F/R Cost fixed");
 // Every n-cost word has exactly the SAME original primitive probability p^n.
 const total=words.length*p**n;
 check(total>0&&total<2,"original finite exact-cost sum");
}
check(allWords(3).join("|")==="FFF|FR|RF","minimal exact-cost n3 toy words");
check(allWords(20).length===10946,"owned original Golden n20 count");
const L=4,m=29,selected=m*L**4,n=20;
const prefixMass=selected*p**n,readyMass=2*p**(n+3)*selected;
check(Math.abs(prefixMass-0.490778081)<3e-9,"owned actual n20 L4 prefix activation mass");
check(Math.abs(readyMass-0.2317)<0.001,"owned actual n20 L4 READY mass");
const aInfinity=(1+Math.sqrt(5))/2/Math.sqrt(5);
const limitREADY=2*p**3*aInfinity;
check(Math.abs(limitREADY-0.341640786499874)<3e-13,"nonvanishing original Golden READY limit");

// Small Golden same-cost n=3 test. Use arbitrary test address assignment
// to two macro buckets; real x(w) belongs to the separate owned theorem.
const W=allWords(3);
const liveIndex=new Map(W.map((w,i)=>[w,i]));
const logicalSite=[0,0,1];  // FFF,FR from site0; RF from site1
const active=[1,0,1];       // select first in each, FR remains present at baseline
const q=Array.from({length:3},()=>p**3);
check(Math.abs(q[0]-q[2])<1e-15,"native primitive costs produce exact equal site query weights");

// Whole cut retains ALL three labels and their archive copies; conditioning
// selected label produces exact equal source weights over the two cells.
const source1=[2.25,-19,-0.75];  // FR unused baseline source, not erased
const source2=[-3.5,7,4.125];
const mean=(arr)=>active.reduce((s,mask,i)=>s+mask*q[i]*arr[logicalSite[i]],0)/
 active.reduce((s,mask,i)=>s+mask*q[i],0);
check(Math.abs(mean([source1[0],source1[2]])-(source1[0]+source1[2])/2)<1e-14,"exact conditional balanced native source");
check(Math.abs(mean([source2[0],source2[2]])-(source2[0]+source2[2])/2)<1e-14,"second original source tangent");

// LIVE a∈{0,1,2}, active target c∈{0,1}, OLD fresh bit r∈{0,1,2}.
// 'selected last-cell' uses CAR flip only if a=2. OLD translated register
// is never read by the live operator.
const triples=Array.from({length:3*2*3},(_,i)=>[Math.floor(i/6),Math.floor(i/3)%2,i%3]);
const live=([a,c,r])=>[a,c^(a===2?1:0),r];
const old=([a,c,r])=>[a,c^(r===2?1:0),r];
const xOld=([a,c,r])=>[a,c,(r+1)%3];
const copy=([a,c,r])=>[a,c,(r+a)%3];
const equals=(x,y)=>x.every((v,i)=>v===y[i]);
check(triples.every(v=>equals(live(xOld(v)),xOld(live(v)))),"LIVE-active query commutes with OLD translations");
check(triples.every(v=>equals(copy(xOld(v)),xOld(copy(v)))),"old archive one-way COPY commutes with translations");
check(triples.some(v=>!equals(old(xOld(v)),xOld(old(v)))),"OLD-controlled query violates prior exact invariant");
check(triples.filter(v=>v[0]===v[2]).every(v=>equals(live(v),old(v))),
  "LIVE gate realizes old-conditioned desired action ONLY on pre-existing correlated active/OLD subspace");
check(triples.filter(v=>v[2]===0).every(v=>copy(v)[2]===v[0]),
  "fresh archive can copy original live orthogonal prefix without old-control");

// Fixed within-site class permutations preserve the exact complete
// per-class J2 return PRICE when all original READY blocks have the
// same literal terminal type and same original finite defining weight.
const F4=allWords(4),sites=[0,0,1,1,1],selA=[1,0,1,1,0],selB=[0,1,1,0,1];
const probeValues=(site,x)=>site===0?(x*x+3*x):(Math.sin(x)+2*x*x);
for(const x of [-0.21,0,0.37]){
 const sum=s=>s.reduce((acc,v,i)=>acc+v*probeValues(sites[i],x),0);
 check(Math.abs(sum(selA)-sum(selB))<1e-13,"exact same-cell selected-block multiplicity yields same geometrical J2 value");
}
check(selA.reduce((a,b)=>a+b,0)===selB.reduce((a,b)=>a+b,0),"same admitted k");

// Dynamic Role fields, real controller gate budget and OLD preparation are
// not inferred from this exact GENEROUS grammar, nor is Book03 H+J+R.
console.log(JSON.stringify({
 status:"PASS_GOLDEN_LEFT_LIVE_QUERY_WITH_COMPLETE_OLD_ARCHIVE",
 nativePrimitive:{p,operatorG:G,operatorFlatJulia:XG,n20Fibonacci:F4.length===5?10946:null,
  actualL4PrefixActivated:selected, actualPrefixMass:prefixMass,
  actualREADYMass:readyMass, limitREADYMass:limitREADY},
 faceFirstSource:"fixed same-Cost balanced Golden word counts give equal site first jets, inactive histories retained",
 verifiedFiniteSemantics:["source Golden F/R same-cost labels","complete native Golden flat GOOD/BAD",
 "live old-correlated query without old-read","old translation invariant",
 "source equivalence for within-cell permutations at fixed k"],
 missingPhysical:"actual fullStep LIVE word supply, native addressed CAR/scene unitary, controller/clock/work/oldRIGHT/reference and whole Book selected price",
 GR_closed:false
},null,2));
