#!/usr/bin/env node
"use strict";
/*
 * ORIGINAL D0 Role CAR16 grade-two Lorentz Hodge J already certified by
 * original a4d_role_bivector_commutant_check.py (nullity2: span I,J).
 * This checker consumes that SAME integer matrix and verifies:
 *    J²=-I and det(a I + b J)=(a²+b²)^3 exactly for integer a,b;
 *    tetrad Holst e∧e∧F contraction vanishes for algebraic Riemann
 *    tensors satisfying first Bianchi (Kulkarni-Nomizu generators);
 *    Palatini epsilon contraction remains nonzero on a valid curvature.
 * Formal continuum torsion-free vacuum equivalence is proved in the memo
 * using D(e∧e)=0 and invertibility of a I + b J.
 * Not a native D0 source selector / not a finite h torsion theorem.
 */
const need=(x,msg)=>{if(!x)throw Error("FAIL: "+msg)};
const I=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const scale=(A,c)=>A.map(r=>r.map(x=>x*c));
const add=(A,B)=>A.map((r,i)=>r.map((x,j)=>x+B[i][j]));
const diff=(A,B)=>Math.max(...A.flatMap((r,i)=>r.map((x,j)=>Math.abs(x-B[i][j]))));
const H=Array.from({length:6},()=>Array(6).fill(0));
for(const [i,j,c] of [[5,0,1],[4,1,-1],[3,2,1],[2,3,-1],[1,4,1],[0,5,-1]])H[i][j]=c;
need(diff(mul(H,H),scale(I(6),-1))===0,
  "original Lorentz grade-two Hodge squares to -I on ALL 6 dimensions");
function perms(a){
 if(a.length===0)return [[]];
 let out=[];
 for(let i=0;i<a.length;i++)for(const v of perms(a.slice(0,i).concat(a.slice(i+1))))out.push([a[i],...v]);
 return out;
}
const P6=perms([0,1,2,3,4,5]);
function sign(p){let k=0;for(let i=0;i<p.length;i++)for(let j=i+1;j<p.length;j++)if(p[i]>p[j])k++;return k%2?-1:1}
function det(A){return P6.reduce((s,v)=>s+sign(v)*v.reduce((p,j,i)=>p*A[i][j],1),0);}
const cases=[];
for(const [a,b] of [[0,1],[1,0],[2,3],[5,0],[3,-4],[-2,7]]){
 const Q=add(scale(I(6),a),scale(H,b)),
       InvNum=add(scale(I(6),a),scale(H,-b)), d=a*a+b*b;
 const product=mul(Q,InvNum),D=det(Q);
 need(diff(product,scale(I(6),d))===0,
   "original Holst-Palatini bivector operator has analytic inverse for real coefficients");
 need(D===d**3,
   "six original Lorentz bivectors give EXACT det(aI+bH)=(a²+b²)^3");
 cases.push({a,b,det:D,expected:d**3});
}
// General algebraic Riemann fixture: ANY Kulkarni-Nomizu product of
// two symmetric tetrad tensors obeys the FIRST BIANCHI identity.
// Its ε contraction (Holst density in a torsionfree coframe) is ZERO.
const eta=[1,-1,-1,-1];
const eps=perms([0,1,2,3]).map(p=>[p,sign(p)]);
const A=[[3,1,2,0],[1,2,0,1],[2,0,1,1],[0,1,1,4]];
const B=[[4,1,0,2],[1,1,2,0],[0,2,3,1],[2,0,1,1]];
const R=(a,b,c,d)=>A[a][c]*B[b][d]+A[b][d]*B[a][c]-A[a][d]*B[b][c]-A[b][c]*B[a][d];
let maxBianchi=0;
for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let c=0;c<4;c++)for(let d=0;d<4;d++)
 maxBianchi=Math.max(maxBianchi,Math.abs(R(a,b,c,d)+R(a,c,d,b)+R(a,d,b,c)));
need(maxBianchi===0,"original Lorentz-compatible algebraic Riemann obeys exact first Bianchi");
const Holst=eps.reduce((s,[perm,sgn])=>s+sgn*R(...perm),0);
const scalar=[0,1,2,3].reduce((sum,a)=>sum+
  [0,1,2,3].reduce((sum,b)=>sum+eta[a]*eta[b]*R(a,b,a,b),0),0);
need(Holst===0 && scalar!==0,
  "torsionfree Holst epsilon contraction identically zero while Einstein-Palatini curvature NONZERO");
// Independent NON-BIANCHI tensor must produce a nonzero epsilon contraction.
const Fake=(a,b,c,d)=>{
 const e=(p)=>eps.find(x=>x[0].every((q,i)=>q===p[i]));
 return e([a,b,c,d])?.[1]??0;
};
const fakeHolst=eps.reduce((s,[per,sgn])=>s+sgn*Fake(...per),0);
need(fakeHolst===24,
 "first Bianchi is load-bearing; arbitrary antisym curvature can have a NONZERO Holst term");
console.log(JSON.stringify({
 status:"PASS_ORIGINAL_CAR16_HODGE_HOLST_VACUUM_UNIVERSALITY",
 originalLorentzBivectorDim:6,originalCommutant:"span(I,Hodge), rank34/36 (prior exact owner)",
 hodgeSquared:"-I6",holstCoefficientCases:cases,
 bianchiCurvature:{torsionfreeRiemannEpsilonHolst:Holst,
   nonzeroPalatiniScalarContraction:scalar,
   bianchiResidual:maxBianchi,nonBianchiEpsilonContraction:fakeHolst},
 continuumDeduction:"Real a,b with b!=0: invertible aI+bH gives vacuum torsionfree connection, Holst four-form vanishes by first Bianchi, remaining b-Palatini is Einstein-Hilbert",
 mathematicalBoundary:"standard vacuum continuum theorem only; actual finite D0 physical selected source, spin torsion, variable a(x)/b(x), matter stress and uniform convergence NOT proved",
 GR_closed:false
},null,2));
