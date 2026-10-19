#!/usr/bin/env node
"use strict";
/**
 * Bounded analytic example of a decisive SOURCE fact:
 *
 * for FIELD-INDEPENDENT orthogonals U and W and a genuine smooth active
 * preparation rho(y), a FIXED native word W whose operator error is eps
 * controls ALL output-POVM derivatives on that same input chart:
 *
 * |D_y^j Tr[rho(y)(W^T E W-U^T E U)]|
 *    <=2 eps ||E||_op ||D_y^j rho(y)||_trace.
 *
 * For actual Golden, its irrational angle makes positive powers dense
 * in SO2; no oracle continuously chooses a different gate word per y.
 *
 * This does NOT construct admitted rho(y), real 4D Role->CAR input,
 * same-history Book cost or uniform word-length/refinement bounds.
 */
const p=(Math.sqrt(5)-1)/2,a=Math.sqrt(p),theta=Math.atan2(p,a);
const normDifference=t=>2*Math.abs(Math.sin(t/2));
const targetAngle=0.4;
let best={m:-1,error:Infinity,angle:NaN};
for(let m=1;m<=25000;m++){
  const alpha=m*theta,eps=normDifference(alpha-targetAngle);
  if(eps<best.error)best={m,error:eps,angle:alpha};
}
if(!(best.error<1e-3))throw Error("Golden finite rotation failed bounded density control");
const samples=[];
let ratios=[0,0,0];
for(let j=0;j<=20;j++){
  const x=(j-10)/7;
  const value=angle=>Math.cos(x+angle)**2;
  const first=angle=>-Math.sin(2*(x+angle));
  const second=angle=>-2*Math.cos(2*(x+angle));
  const A=[value(targetAngle),first(targetAngle),second(targetAngle)],
    B=[value(best.angle),first(best.angle),second(best.angle)],
    bounds=[2*best.error,4*best.error,8*best.error];
  const diffs=A.map((v,i)=>Math.abs(v-B[i]));
  if(diffs.some((v,i)=>v>bounds[i]+1e-14))
    throw Error("not bounded by fixed-unitary C2 source estimate at sample "+j);
  for(let i=0;i<3;i++)ratios[i]=Math.max(ratios[i],diffs[i]/bounds[i]);
  samples.push({x,difference:diffs});
}
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_GOLDEN_FIXED_WORD_C2_SOURCE_BOUND",
 p,theta,targetAngle,finitePositiveWordLength:best.m,
 operatorError:best.error,
 allDerivativeOrder0to2Tested:21,
 largestRatioToRigorousBound:ratios,
 operatorNormStatement:"||U^TEU-W^TEW||<=2*eps*||E||",
 sourceNormStatement:"||D^j probability_error||<=2*eps*||D^j rho||_1, j=0,1,2",
 selectionScope:"U,W must be fixed in y; actual physical preparation, Book selection, native clock and word budget remain OPEN",
 GR_closed:false
},null,2));
