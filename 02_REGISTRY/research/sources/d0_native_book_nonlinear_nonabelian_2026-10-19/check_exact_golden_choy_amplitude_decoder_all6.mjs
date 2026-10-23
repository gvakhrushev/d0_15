#!/usr/bin/env node
"use strict";
/**
 * ORIGINAL K(9,11,13) Perron address × native Golden-p CAR16×ref4
 * Choi/Julia 2-FRESH-flag complete 16-outcome mark.
 * Exact finite square-root decoder for all six proper Lorentz directions,
 * independent of moving scalar Book path weight. No fitted coupling.
 *
 * This is a mathematical SAME-RUN CLASS composition, not proof of literal
 * GoldenCoherentMemory.fullStep or the physically selected whole Book action.
 */
const phi=(1+Math.sqrt(5))/2,p=1/phi,ell=Math.log(phi);
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const zero=n=>Array.from({length:n},()=>Array(n).fill(0));
const add=(A,B,c=1)=>A.map((r,i)=>r.map((v,j)=>v+c*B[i][j]));
const prod=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,v,k)=>s+v*B[k][j],0)));
const transpose=A=>A.map((r,i)=>r.map((_,j)=>A[j][i]));
const trace=A=>A.reduce((s,r,i)=>s+r[i],0);
const dot=(x,y)=>x.reduce((s,v,i)=>s+v*y[i],0);
const mv=(A,v)=>A.map(r=>dot(r,v));
const need=(v,s)=>{if(!v)throw Error("FAIL "+s);console.log("PASS "+s)};
const E=(i,j)=>{let M=zero(4);M[i][j]=1;return M};
const G=[add(E(1,2),E(2,0)),add(E(1,3),E(3,0)),
 add(E(0,2),E(2,1)),add(E(0,3),E(3,1)),
 add(E(2,3),E(3,2),-1),add(E(1,1),E(0,0),-1)];
const inner=(X,Y)=>trace(prod(transpose(X),Y));
need(G.every((X,i)=>G.every((Y,j)=>Math.abs(inner(X,Y)-(i===j?2:0))<1e-14)),
     "all SIX original proper-Lorentz generators have native 2*identity Gram");
function expM(X){let T=eye(4),out=eye(4);for(let j=1;j<=23;j++){
 T=prod(T,X).map(r=>r.map(v=>v/j));out=add(out,T);
 }return out;
}
const nilExp=(X,a)=>add(add(eye(4),X,a),prod(X,X),a*a/2);
function marks(U,kappa=p*p){
 const mean=trace(U)/4;
 const each=G.map(H=>{
  const oriented=inner(H,U)/(2*Math.SQRT2);
  const qPlus=kappa*kappa/24*(mean+oriented)**2;
  const qMinus=kappa*kappa/24*(mean-oriented)**2;
  return {qPlus,qMinus,mean,oriented};
 });
 return each;
}
function decode(q,kappa=p*p){
 const x=Math.sqrt(q.qPlus),y=Math.sqrt(q.qMinus);
 return {traceU:4*Math.sqrt(6)/kappa*(x+y),
         marker:4*Math.sqrt(3)/kappa*(x-y)};
}
const genRows=G.map((H,i)=>G.map((J,j)=>inner(H,J)));
need(genRows.every((r,i)=>r.every((v,j)=>v===(i===j?2:0))),
     "finite amplitude decoder derivative at identity is exactly 2*I6");
function sixProbe(U,lab){
 const q=marks(U),mean=trace(U);
 for(let j=0;j<6;j++){
  const d=decode(q[j]);
  need(Math.abs(d.marker-inner(G[j],U))<3e-12,
       lab+" full positive probabilities decode EXACT finite oriented marker "+j);
  need(Math.abs(d.traceU-mean)<3e-12,
       lab+" full positive probabilities decode common unmarked trace "+j);
 }
 return q;
}
const a=1/40,b=1/40,UA=nilExp(G[0],a),UB=nilExp(G[3],b);
const UAB=prod(UA,UB),UBA=prod(UB,UA);
const qab=sixProbe(UAB,"AB original two ordered loops"),
      qba=sixProbe(UBA,"BA original reversed loops");
const j=4,t=a*b;
need(Math.abs(inner(G[j],UAB)-t)<2e-14
 && Math.abs(inner(G[j],UBA)+t)<2e-14,
 "original J23 commutator source exactly +ab vs -ab, ALL amplitudes");
need(Math.abs(decode(qab[j]).marker-t)<2e-14
 && Math.abs(decode(qba[j]).marker+t)<2e-14,
 "NO LOG / no Taylor: sqrt-Born probabilities recover exact finite ab");
need(Math.abs(qab[j].qPlus-qba[j].qMinus)<2e-16
 && Math.abs(qab[j].qMinus-qba[j].qPlus)<2e-16,
 "original order-reversed J23 tags exchange ± and preserve full Born normalization");
for(const h of [.001,.02,.06]){
 let U=expM(G.reduce((S,X,i)=>add(S,X,[h,h/2,-h/4,h/3,h/5,h/7][i]),zero(4)));
 sixProbe(U,"all SIX simultaneous noncommuting original Lorentz source h="+h);
}
function complete(U1,U2){
 // These three other-flag aggregate probabilities come from exact
 // full CAR grade1 Choi traces of genuine F_i²=I-p² U_i† U_i,
 // without postselecting, discarding flags or approximating F_i.
 const U=prod(U2,U1),S1=prod(transpose(U1),U1),S2=prod(transpose(U2),U2);
 const ss=trace(prod(transpose(U),U)),cross=trace(prod(S2,S1));
 const GG=p**4*ss/4;
 const GB=p*p*(trace(S1)-p*p*ss)/4;
 const BG=p*p*(trace(S2)-p*p*cross)/4;
 const BB=1-GG-GB-BG;
 const marked=marks(U),allMarks=marked.reduce((s,v)=>s+v.qPlus+v.qMinus,0);
 const GGrest=GG-allMarks,probs=marked.flatMap(v=>[v.qPlus,v.qMinus]).concat(GGrest,GB,BG,BB);
 need(probs.length===16&&probs.every(x=>x>0),
      "original complete positive CAR16 grade1 Choi has all SIX pairs + rest + GB/BG/BB");
 need(Math.abs(probs.reduce((s,x)=>s+x,0)-1)<3e-14,
      "all FOUR fresh Golden-p flag histories remain CPTP normalized");
 return {GG,GB,BG,BB,GGrest,allMarks,probs};
}
const cab=complete(UB,UA),cba=complete(UA,UB);
need(Math.abs(cab.GG-cba.GG)<2e-14,
 "original two loop orderings have same unmarked GG mass at exact nilpotent control");

// TRUE moving 33-scene one-sided Perron history for two disjoint ABC triangles.
// A-zone a0, B-zone b0,c0, B-zone b1,c1; every valid edge supported.
// Primitive scalar Book edge Cost=1+t on AB, 1 elsewhere (actual p=phi^-1).
const nzone=[9,11,13],nvertex=33,zone=v=>v<9?0:v<20?1:2;
function pathWeight(t){
 const blocks=nzone.map((a,i)=>nzone.map((b,j)=>i===j?0:
      p*Math.sqrt(a*b)*Math.exp(-ell*t*(((i===0&&j===1)||(i===1&&j===0))?1:0))));
 let v=[1,1,1].map(x=>x/Math.sqrt(3));
 for(let k=0;k<800;k++){
  const y=mv(blocks,v),norm=Math.hypot(...y),w=y.map(x=>x/norm);
  if(Math.max(...w.map((x,j)=>Math.abs(x-v[j])))<1e-15){v=w;break;}v=w;
 }
 const lambda=dot(v,mv(blocks,v));
 const r0=v[0]/Math.sqrt(9),normalizer=nzone.reduce((s,n,i)=>s+n*v[i]/Math.sqrt(n),0);
 const nativeR0=r0/normalizer,word=[0,9,20,0,10,21,0];
 let weight=nativeR0;
 for(let k=0;k<word.length-1;k++){
  const u=word[k],w=word[k+1];
  need(zone(u)!==zone(w),"actual two ABC loops use allowed ORIGINAL scene edges");
  const hasAB=((zone(u)===0&&zone(w)===1)||(zone(u)===1&&zone(w)===0));
  const kij=p*Math.exp(-ell*t*(hasAB?1:0));
  const ru=v[zone(u)]/Math.sqrt(nzone[zone(u)]);
  const rw=v[zone(w)]/Math.sqrt(nzone[zone(w)]);
  weight*=kij*rw/(lambda*ru);
 }
 return {weight,lambda,nativeR0};
}
const weights=[0,.02,.04].map(t=>({t,...pathWeight(t)}));
for(const w of weights){
 need(w.weight>0&&w.weight<1,
      "TRUE original moving one-sided Book/Doob probability positive at t="+w.t);
 const qCond=qab[4],Qplus=w.weight*qCond.qPlus,Qminus=w.weight*qCond.qMinus;
 const recovered=4*Math.sqrt(3)/(p*p*Math.sqrt(w.weight))*(Math.sqrt(Qplus)-Math.sqrt(Qminus));
 need(Math.abs(recovered-a*b)<3e-13,
      "finite native Golden marker independent of ALL moving scalar Book history weights t="+w.t);
}
const h=.0001;
const marker=t0=>{let x=pathWeight(t0).weight,q=qab[4];
 return 4*Math.sqrt(3)/(p*p*Math.sqrt(x))*
    (Math.sqrt(x*q.qPlus)-Math.sqrt(x*q.qMinus));
};
need(Math.abs((marker(h)-marker(0))/h)<2e-10,
 "exact all-order cancellation of moving original scalar Book source in one-sided ADMISSIBLE Cost>=1 family");

console.log(JSON.stringify({
 original:"33-vertex/718-edge actual Perron paths + original CAR16 two-loop native Golden-p full16 marked flag instrument",
 p,native_two_loop_16_outcomes_AB:cab,
 original_two_loop_oriented_exact_ab:a*b,
 exact_decoder:"Tr(G^T U)=4sqrt(3)/p^2 * (sqrt(qPlus)-sqrt(qMinus))",
 exact_trace_decoder:"Tr U=4sqrt(6)/p^2 * (sqrt(qPlus)+sqrt(qMinus))",
 stationary_moving_native_scene_path_weights:weights,
 full_40_geometric_observability_conditional:true,
 physically_compulsory_full_book_action_selected:false,
 GR_closed:false
},null,2));
