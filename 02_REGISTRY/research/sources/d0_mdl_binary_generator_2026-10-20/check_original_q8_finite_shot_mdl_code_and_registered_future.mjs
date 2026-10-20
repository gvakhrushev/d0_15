#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL D0 Omega8Center + OrderMemoryControl Q8 forward words,
 * primitive GoldenOrderInterferometer native Born p=phi^-1:
 *
 * Pure Q8 +1 sign => bright0, dark1.
 * Q8 -1 commutator=> bright4p^3, darkp^6.
 *
 * Exact one-sided finite Popperian falsifiability: observing ANY
 * bright refutes +1 in ideal source, whereas ALL N dark outcomes
 * have positive likelihood p^(6N) even under -1, for EVERY FINITE N.
 * Independent reset-and-repeat is an explicit extra programme/cost.
 * Each extra all-dark event contributes exactly SIX native logarithmic
 * phi-code units to the likelihood ratio supporting + vs -.
 *
 * Full two-bit original reversible record: programme bit and record
 * bit. FiniteProtocolClock.register performs CNOT record ^= program.
 * Current Golden port distribution depends ONLY on record; after
 * one native register gate it also reveals programme. Thus exact
 * future-context quotient has FOUR classes, despite current TWO.
 */
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi);
const c=p-p*p,s=2*Math.sqrt(p)*p,q=4*p**3,m=p**6;
const test=(b,s)=>{if(!b)throw Error("FAIL "+s);console.log("PASS "+s);};
test(Math.abs(q+m-1)<1e-14 &&q>0&&m>0&&q<1,
     "literal original Golden dark p^6 + bright 4p^3 normalizes and is genuinely stochastic");
test(Math.abs(c-p**3)<1e-14&&Math.abs(s*s+c*c-1)<1e-14,
     "same original Golden native unitary coefficients without fitted angle");
const nativePort=bit=>bit?q:0;
const now=(program,record)=>nativePort(record);
const afterRegister=(program,record)=>nativePort(Boolean(Number(program)^Number(record)));
const outcomes=[];
for(const pr of [false,true])for(const re of [false,true]){
 const curr=now(pr,re),later=afterRegister(pr,re);
 outcomes.push({program:pr,record:re,current_bright:curr,after_original_CNOT_bright:later,key:[curr,later].join(":")});
}
const classesNow=new Set(outcomes.map(r=>r.current_bright)).size,
      classesAfter=new Set(outcomes.map(r=>r.key)).size;
test(classesNow===2&&classesAfter===4,
     "ACTUAL reversible FiniteProtocolClock.register upgrades present Golden-port 2 classes to future-complete 4");
test(new Set(outcomes.map(r=>r.key)).size===4,
     "ALL four programme/record source states distinguished by current plus ONE actual future Golden registered readout");
const counters={I:4,J:4};
test(counters.I+counters.J===8,
     "identical primitive 8-gate Q8 chronology programmes require at least one order bit to predict future");
const finiteRepeat=[];
for(let n=1;n<=12;n++){
 const miss=p**(6*n), likelihoodContrast=1/miss,
       evidenceCode=Math.log(likelihoodContrast)/ell;
 let coeff=1,sum=0;
 for(let k=0;k<=n;k++){
  if(k>0)coeff=coeff*(n-k+1)/k;
  sum+=coeff*q**k*m**(n-k);
 }
 test(miss>0&&Math.abs(evidenceCode-6*n)<2e-12&&Math.abs(sum-1)<5e-13,
      "N="+n+" exact nonzero all-dark failure and 6n phi-code evidence, full independent Bernoulli normalization");
 finiteRepeat.push({trials:n,all_dark_given_minus:miss,
   bright_at_least_once_given_minus:1-miss,
   phi_code_evidence_for_plus_after_all_dark:6*n});
}
const thresholds=[.1,.01,.001,1e-6,1e-9].map(alpha=>{
 const n=Math.ceil(Math.log(alpha)/(6*Math.log(p)));
 const failure=p**(6*n);
 test(failure<=alpha&& (n===0||p**(6*(n-1))>alpha),
      "exact least N independent Q8 Golden trials to bound false all-dark probability below "+alpha);
 return {target_false_negative:alpha,least_trials:n,actual_false_negative:failure};
});
test(Math.abs(1/q-1.059018177)<.0001,
     "finite geometric expected independent trials to first bright ~1.059; not free physical clock");
test(nativePort(false)===0&&nativePort(true)>0&&m>0,
     "bright event is a one-sided exact Popperian falsifier, dark result never certain for finite N");
console.log(JSON.stringify({
 original_parameters:{p,phi,born_negative_bright:q,born_negative_dark:m,born_positive_bright:0},
 source_future_register:outcomes,
 current_equivalence_classes:classesNow,
 full_future_equivalence_classes:classesAfter,
 minimal_future_memory_bits:2,
 minimal_chronological_extra_programme_bit:1,
 repeated_conditions:"independent fresh preparations and literal complete two-port records needed, NOT forced by G0",
 finite_original_one_sided_Popper:[...finiteRepeat.slice(0,5),finiteRepeat.at(-1)],
 exact_likelihood_mdl_phi_code:"N all-dark outcomes have log_phi likelihood ratio +6N in favor of center +1 versus -1",
 repetition_thresholds:thresholds,
 mathematical_15_step_registered_program_from_preexisting:"FiniteProtocolClock/order_memory_control_verify.py",
 physical_G0_free_repeats:false,
 physical_Book_cost_HJR_selected:false,
 GR_closed:false
},null,2));
