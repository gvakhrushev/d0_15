"use strict";
// Exact source-sufficient one-moment criterion for the Golden Book response.
const p=(Math.sqrt(5)-1)/2,z=2**-20;
function F(e){return 4*p*e*(1-p*e)}

function fprime(e){return 4*p*(1-2*p*e)}

function K(e){return z*fprime(e)/(1-z*F(e))}

function Kprime(e){return z*(-8*p*p*(1-z*F(e))+z*fprime(e)**2)/(1-z*F(e))**2}

function ensure(b,msg){if(!b)throw Error("VALIDATION FAILED: "+msg)}

function run(){
 let checks=0;const test=(b,m)=>{ensure(b,m);checks++};
 test(Math.abs(p+p*p-1)<1e-14,"Golden root");
 const r=.5,X=[[.1,.23],[.23,-.31]];
 const trX=X[0][0]+X[1][1],dBar=trX/2;
 const source=K(r)*trX;
 test(Math.abs(source-2*K(r)*dBar)<1e-20,"exact scalar first source");
 const eps=1e-5;
 const evalBook=(e0,e1)=>-Math.log1p(-z*F(e0))-Math.log1p(-z*F(e1));
 const hostile=K(.2)-K(.7);
 const numeric=(evalBook(.2+eps,.7-eps)-evalBook(.2-eps,.7+eps))/(2*eps);
 test(Math.abs(numeric-hostile)<1e-12,"effect direction trace 0 but Book source nonzero");
 test(hostile>1.45e-6 && trX<0,"hostile source");
 for(const e of [0,.2,.5,.7,1]){test(Kprime(e)<0,"strict Golden response monotone "+e)}
 const L=8*p*p*z*(1+2*z)/(1-z)**2;
 const eA=.51,eB=.49,dE0=.2,dE1=-.35;
 const v=K(eA)*dE0+K(eB)*dE1;
 const approx=K(r)*(dE0+dE1);
 const margin=2*L*.01*Math.max(Math.abs(dE0),Math.abs(dE1));
 test(Math.abs(v-approx)<margin,"quantitative nearly scalar bound");
 const rootGain=4*p**3*z/(1-z*(3*p-1));
 test(Math.abs(rootGain-K(.5))<1e-18,"original native Golden fair gain");
 test(Math.abs(K(1/(2*p)))<1e-18,"exceptional Golden zero-source point");
 return {status:"SCOPED_PASS",checks,anchored_scalar:{r,trace_dE:trX,
  one_bit_expectation_slope:dBar,book_source:source,exact_gain:K(r)},
   hostile_nonscalar:{effect_eigenvalues:[.2,.7],
      trace_of_dE:0,source:hostile,numerical_source:numeric},
   near_scalar:{effect:[eA,eB],first_source:v,one_moment_approx:approx,
      actual_error:Math.abs(v-approx),rigorous_bound:margin},
   open_physics:{native_42_effect_scalar_on_actual_root:false,
     physical_Book_cut_selected:false,
     upstream_stationarity_closed:false,GR_closed:false}};
}

console.log(JSON.stringify(run(),null,2));
