#!/usr/bin/env node
"use strict";
// Original D0 finite verification MDL: closure under ALL finite future
// action words via deterministic partition refinement.
// Exhaustive EVERY Boolean-readout machine: n2 two actions, n3 two,
// n4 one action. No privileged external infinite future-test catalogue.
// A bounded n-state exact detector has future equivalence stable at
// depth <=n-k, k=current observational classes. If k=1 it is already
// stable; k>=2 -> max n-2. Bound is SHARP.
const requireCheck=(q,m)=>{if(!q)throw Error("FAIL "+m);console.log("PASS "+m)};
const norm=keys=>{const t=new Map();return keys.map(k=>{const x=JSON.stringify(k);if(!t.has(x))t.set(x,t.size);return t.get(x)})};
function quotient(n,actions,reads){
 let label=norm(Array.from({length:n},(_,i)=>reads.map(row=>row[i])));
 const initial=new Set(label).size;let depth=0,history=[initial];
 for(;;){
  const next=norm(Array.from({length:n},(_,i)=>[label[i],...actions.map(A=>label[A[i]])]));
  const oldN=new Set(label).size,nN=new Set(next).size;
  if(nN===oldN){
   if(next.some((v,i)=>v!==label[i]))throw Error("partition numbering invariant");
   return {initial,classes:oldN,depth,history,label};
  }
  if(nN<=oldN)throw Error("strict refinement failed");
  label=next;depth++;history.push(nN);
  if(depth>n)throw Error("refinement nontermination");
 }
}
function allWords(a,depth){
 let layer=[[]],out=[[]];
 for(let n=1;n<=depth;n++){
  layer=layer.flatMap(w=>Array.from({length:a},(_,i)=>w.concat(i)));
  out.push(...layer);
 }return out;
}
function run(s,w,acts,reads){for(const i of w)s=acts[i][s];return reads.map(r=>r[s])}
function exhaustive(n,a){
 const maps=Array.from({length:n**n},(_,code)=>{let x=code;return Array.from({length:n},()=>{const r=x%n;x=Math.floor(x/n);return r})});
 const words=allWords(a,n),count=maps.length**a;
 let total=0,maxDepth=0,maxClasses=0;
 for(let c=0;c<count;c++){
  let j=c,actions=[];for(let i=0;i<a;i++){actions.push(maps[j%maps.length]);j=Math.floor(j/maps.length)}
  for(let m=0;m<2**n;m++){
   const reads=[Array.from({length:n},(_,i)=>(m>>i)&1)];
   const q=quotient(n,actions,reads);if(q.depth>Math.max(0,n-2))throw Error("finite MDL bound failed");
   for(let s=0;s<n;s++)for(let t=s;t<n;t++){
    const trueEq=words.every(w=>JSON.stringify(run(s,w,actions,reads))===JSON.stringify(run(t,w,actions,reads)));
    if(trueEq!==(q.label[s]===q.label[t]))throw Error("all-future bisimulation disagreement");
   }
   maxDepth=Math.max(maxDepth,q.depth);maxClasses=Math.max(maxClasses,q.classes);total++;
  }
 }
 return {n,a,total,maxDepth,maxClasses};
}
const exhaustiveResults=[];
for(const [n,a] of [[2,2],[3,2],[4,1]]){
 const r=exhaustive(n,a);exhaustiveResults.push(r);
 requireCheck(r.total===(n**n)**a*2**n,
  "all transition maps + all binary tests exhausted n="+n+" actionCount="+a);
}
const sharp=[];
for(let n=3;n<=12;n++){
 const Q=quotient(n,[Array.from({length:n},(_,i)=>Math.min(n-1,i+1))],
                  [Array.from({length:n},(_,i)=>+(i===n-1))]);
 requireCheck(Q.depth===n-2&&Q.classes===n,
  "sharp original finite contextual MDL horizon n-2 at n="+n);
 sharp.push({n,depth:Q.depth});
}
const current=quotient(4,[[0,1,2,3],[0,2,2,3]],[[0,0,1,1]]);
requireCheck(current.initial===2&&current.classes===3,
 "same present 2-label record but one future action forces 3 genuine memory classes");
const leanToy=quotient(4,[[0,1,2,3],[0,3,0,3]],[[0,0,1,1]]);
requireCheck(leanToy.initial===2&&leanToy.classes===4&&leanToy.depth===1,
 "same Lean archive toy: 2 current Boolean outcomes require ALL FOUR future classes");
requireCheck(leanToy.label.every((v,i)=>leanToy.label.indexOf(v)===i),
 "minimal physical predictive record needs TWO archive bits, not one visible bit");
console.log(JSON.stringify({
 theorem:"ANY native finite n-state test/action system has an exact canonical all-future minimal quotient in <=n-k refinements (k observed blocks), n-2 for k>=2; sharp",
 exhaustive:exhaustiveResults,
 sharp,archive3:current,archive4:leanToy,
 extra_line_not_a_primitive_generator:true,
 archived_future_memory_is_not_redundant:true,
 actual_physical_M1_G0_Book_selector_unproved:true,
 GR_closed:false
},null,2));
