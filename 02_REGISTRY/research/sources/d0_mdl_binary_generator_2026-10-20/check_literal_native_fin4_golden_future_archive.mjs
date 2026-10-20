#!/usr/bin/env node
"use strict";
/* ORIGINAL literal D0.Representation.GoldenCoherentMemory:
 * fullStep(a,p) : Matrix(Fin4)(Fin4) Real with a=sqrt(p), p=phi^-1.
 * Input two-qubit quantum state [u,0,v,0] with u,v COMPLEX,
 * output literal [a*u-p*v,0,0,p*u+a*v].
 * Genuine reduced-Z vs saved joint XX/YX perfect Bloch reconstruction,
 * plus ORIGINAL GoldenProcessContext A/B endpoint-vs-reset future test.
 * Generic Q8 central Bool is NOT coupled by literal fullStep signature,
 * hence current/future SO/Golden readout is blind to it.
 */
const p=(Math.sqrt(5)-1)/2,a=Math.sqrt(p),c=p-p*p,s=2*a*p;
const test=(q,m)=>{if(!q)throw Error("FAIL "+m);console.log("PASS "+m)};
const cmul=(x,y)=>[x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]];
const cadd=(x,y)=>[x[0]+y[0],x[1]+y[1]];
const conj=x=>[x[0],-x[1]],csq=x=>x[0]*x[0]+x[1]*x[1];
const dot=(x,y)=>x.reduce((v,z,k)=>v+z*y[k],0);
const U=[[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]];
const gram=U.map((row,i)=>U.map((col,j)=>U.reduce((sum,r,k)=>sum+r[i]*r[j],0)));
test(Math.max(...gram.flatMap((row,i)=>row.map((x,j)=>Math.abs(x-Number(i===j)))))<1e-15,
 "literal original Fin4 two-qubit Golden+CNOT fullStep exactly orthogonal");
test(Math.abs(a*a-p)<1e-15&&Math.abs(p+p*p-1)<1e-15&&Math.abs(c*c+s*s-1)<1e-14,
 "true D0 Golden coefficients p=phi^-1, a=sqrt(p), and native Bloch rotation identity");
const inputVectors=[
 [[1,0],[0,0]],
 [[0,0],[0,1]],
 [[Math.sqrt(.37),0],[0,Math.sqrt(.63)]],
 [[.2,.6],[.65,-.4]],
 [[.61,.13],[-.32,.71]]
];
let worst=0;
for(let i=0;i<inputVectors.length;i++){
 const [u0,v0]=inputVectors[i],
 norm=Math.sqrt(csq(u0)+csq(v0)),u=u0.map(t=>t/norm),v=v0.map(t=>t/norm);
 const psi=[u,[0,0],v,[0,0]];
 const out=U.map(row=>row.reduce((z,q,k)=>cadd(z,[q*psi[k][0],q*psi[k][1]]),[0,0]));
 const expectedA=cadd([a*u[0],a*u[1]],[-p*v[0],-p*v[1]]);
 const expectedB=cadd([p*u[0],p*u[1]],[a*v[0],a*v[1]]);
 test(Math.max(...out[0].map((z,k)=>Math.abs(z-expectedA[k])),
               ...out[3].map((z,k)=>Math.abs(z-expectedB[k])),
               ...out[1].map(Math.abs),...out[2].map(Math.abs))<3e-15,
     "original EXACT 4x4 fullStep blankRecord evolution on complex input "+i);
 const ip=cmul(conj(u),v),x=2*ip[0],y=2*ip[1],z=csq(u)-csq(v);
 const iq=cmul(conj(out[0]),out[3]);
 const localZ=csq(out[0])-csq(out[3]),
       jointXX=2*iq[0],jointYX=2*iq[1];
 const intended=[c*z-s*x,s*z+c*x,y],actual=[localZ,jointXX,jointYX];
 const err=Math.max(...actual.map((q,k)=>Math.abs(q-intended[k])));
 worst=Math.max(worst,err);
 test(err<2e-14,"native localZ, joint XxX, joint YxX are exact Bloch Golden source on complex input "+i);
 const backX=c*jointXX-s*localZ,backZ=s*jointXX+c*localZ;
 test(Math.abs(backX-x)<2e-14&&Math.abs(backZ-z)<2e-14&&Math.abs(jointYX-y)<2e-14,
      "actual original full record jointly reconstructs COMPLETE Bloch input (x,y,z) "+i);
}
const pure=[c,0,s],mixed=[0,0,0];
const local=([x,y,z])=>c*z-s*x,
      jointX=([x,y,z])=>s*z+c*x;
test(Math.abs(c*c+s*s-1)<2e-14 &&
     Math.abs(local(pure)-local(mixed))<2e-14 &&
     Math.abs(jointX(pure)-1)<2e-14 &&Math.abs(jointX(mixed))<1e-14,
     "hostile pure-vs-maximally-mixed input has IDENTICAL local Golden Z yet DISTINCT full retained correlation");
const channel=r=>[0,0,local(r)],
      reset=r=>[0,0,1],
      processA=(r,intervene)=>channel(intervene(channel(r))),
      processB=(r,intervene)=>channel(channel(intervene(r)));
for(let v of [pure,mixed,[.18,.27,-.38]]){
 const eA=processA(v,r=>r),eB=processB(v,r=>r),
       rA=processA(v,reset),rB=processB(v,reset);
 test(eA.every((z,i)=>Math.abs(z-eB[i])<1e-14),
      "ACTUAL GoldenProcessContext process A/B identical ENDPOINT under id");
 test(Math.abs(rA[2]-c)<2e-14&&Math.abs(rB[2]-c*c)<2e-14&&
      Math.abs(rA[2]-rB[2])>1e-2,
      "existing GoldenProcessContext retained-reset future context EXPOSES hidden process-order memory");
}
// This negative control is conditional on only the declared Fin4
// fullStep/channel/joint tomography acting on CAR system+record:
// Q8 central spin signs are NOT an input type of the literal GCM gate.
function nativeFutureSignature(state,hiddenQ8,word){
 let rho=state.slice(),results=[];
 for(const op of word){
  if(op==="step"){
   const xp=rho[0],yp=rho[1],zp=rho[2];
   rho=[s*zp+c*xp,yp,c*zp-s*xp];
 }else if(op==="read"){
   results.push([...rho]);
 }else if(op==="local"){
   results.push(rho[2]);
 }else throw Error("not a declared native operation");
 }
 return results;
}
const base=[.17,.31,.43],choices=[[],["step"],["step","step","read"],["step","local","step","read"]];
for(const word of choices)
 test(JSON.stringify(nativeFutureSignature(base,+1,word))===
      JSON.stringify(nativeFutureSignature(base,-1,word)),
      "literal Golden Fin4/Bloch declared future actions NEVER read unattached Q8 central sign word="+word.join(":"));
console.log(JSON.stringify({
 original_Lean_signatures:{
  coherentGate:"D0.Representation.GoldenCoherentMemory.fullStep(a,p): Real Fin4->Fin4",
  original_readouts:"local Z, joint XxX, joint YxX",
  original_processContext:"D0.Representation.GoldenProcessContext.processA/processB resetRetained",
  Q8_Center:"D0.Foundation.Omega8Center.qONE/qNEG on UQuat, NOT native fullStep argument"
 },
 primitive_p:p,rotation_c:c,rotation_s:s,
 full_literal_Golden_readout_max_error:worst,
 local_channel_kernel_dimension:"at least 2 real Bloch coordinates per input; joint full signature rank3",
 original_process_future_reset_exposes_order:c-c*c,
 minimal_future_programme_reduction:"full retained joint outcomes needed IF those actual Golden readouts/contexts admitted",
 negative_control:"without Spin-coupled operation, all native Golden Fin4 future tests identical for ± Q8 sign",
 G0_native_paid_spin_admission:false,
 selected_Book_cost_info_action:false,
 GR_closed:false
},null,2));
