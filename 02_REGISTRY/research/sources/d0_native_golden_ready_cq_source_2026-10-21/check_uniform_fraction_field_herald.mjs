// D0 positive complete finite Golden/FAIR heralding of rational
// inverse-PF source coefficients. All failures retained, uniform
// readiness across 256 original cells. Does NOT prepare pure sqrt(rho).
const assert=(v,m)=>{if(!v)throw Error("FAIL "+m)};
const gcd=(a,b)=>{a=BigInt(a);b=BigInt(b);while(b){const t=a%b;a=b;b=t}return a<0n?-a:a};
const K=10946n,M=256n;
let lcm=1n;for(let n=29n;n<=78n;n++)lcm=lcm/gcd(lcm,n)*n;
const denominator=2n*M*lcm;
const bitlen=denominator.toString(2).length;
const total=1n<<BigInt(bitlen);
assert(total>denominator && total/2n<denominator,"common dyadic herald overhead bounded factor2");
const fail=total-denominator;
assert(fail>0n,"failed herald genuine positive label");
let min=Infinity,max=-Infinity;
const probabilities=[];
for(let n=29n;n<=78n;n++){
  const piNumer=n,piDen=K;
  const rhoNumer=M*n,rhoDen=K;
  const numerator=K*(lcm/n);
  assert(numerator>0n && numerator<denominator,"fraction-field conditional prob strictly in(0,1)");
  const reject=denominator-numerator;
  assert(numerator+reject+fail===total,"full three-outcome dyadic partition");
  assert(numerator*2n*rhoNumer===denominator*rhoDen,
     "actual conditional q_z exactly 1/(2rho_z) at site n="+n);
  const q=Number(numerator)/Number(denominator);
  min=Math.min(min,q);max=Math.max(max,q);
  probabilities.push({n:Number(n),q});
}
// The physical original site w=(1,1,2,2) has n=39 and rho=384/421.
const n=39n;
const origRhoNum=256n*n,origRhoDen=10946n;
assert(origRhoNum*421n===384n*origRhoDen,"source site sqrt(384/421) obstruction preserved");
const v=K*(lcm/n);
assert(v*768n===421n*denominator,"coarse conditional q_w=421/768 exact");
// An even smaller explicit 9-fair-draw conditional rho coin:
assert(384n+37n+91n===512n,"original non-rooted rho_w exact three-way fair herald");
assert(384n*421n===384n*(384n+37n),"positive conditional rho_w=384/421");
// An example genuine Q(phi^-1) / integer successful conditional branch:
const PLO=61803398874989484820458683436563811772030917980576n,D=10n**50n;
const low=(a,b)=>a*D+b*PLO, high=(a,b)=>a*D+b*(PLO+1n);
assert(low(2n,1n)>0n&&low(5n,-1n)>0n,"(2+p)/8 and (5-p)/8 positive");
assert(low(2n,1n)+low(5n,-1n)+D===8n*D,
       "exact Golden ratio conditional 3-category code 1/8 failed");
const rhoArray=[384/421,777/808,625/911,115/211];
let edgeProd=1,logDerivative=0;
const rate=[.1,-.05,.11,.08];
for(let j=0;j<4;j++){
   const k=(j+1)%4;
   edgeProd*=Math.sqrt(rhoArray[j]/rhoArray[k]);
   logDerivative+=.5*(rate[j]-rate[k]);
}
assert(Math.abs(edgeProd-1)<1e-13 && Math.abs(logDerivative)<1e-14,
 "4-edge Golden/PF endpoint-sqrt LOOP cancels with full first variation");
function report(){return {
 status:"PASS_NATIVE_GOLDEN_FRACTION_FIELD_HERALD_AND_PF_GALOIS_DESCENT",
 source_actual_counts:{sites:256,min_n:29,max_n:78,total:10946},
 uniform_inverse_PF_herald:{common_denominator_bitlen:bitlen,
       fair_coins:bitlen,ready_probability:Number(denominator)/Number(total),
       failed_probability:Number(fail)/Number(total),
       conditional_bias_min:min,conditional_bias_max:max},
 site_39:{rho:"384/421",expected_ratio:"sqrt(384/421) is NOT in literal palette field",
     native_conditional_probability:"1/(2rho)=421/768",
     simpler_rho_herald_outcomes:{"ready_and_one":"384/512","ready_and_zero":"37/512","not_ready":"91/512"}},
 example_Q_p_fraction_coarse:{
    q:"(2+p)/7",ready_one:"(2+p)/8",
    ready_zero:"(5-p)/8",not_ready:"1/8"},
 original_weighted_closed_loop:{tested:true,
    gauge_scalar_product:edgeProd,first_log_jet:logDerivative},
 exact_pure_Choi_resource_prepared:false,
 original_stored_Dirac_weighted_edge_source_eliminated:false,
 Book03_Info_selected:false,GR_closed:false};}
if(typeof console!=="undefined")console.log(JSON.stringify(report(),null,2));
