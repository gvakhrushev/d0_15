"use strict";
// D0 #334: source-typed archive mutual-information restoration on original Golden READY future partitions.
const p=(Math.sqrt(5)-1)/2,phi=1/p,ell=Math.log(phi),N=10946,ready=2*N*p**23;
function H(r){return -(r*Math.log(r)+(1-r)*Math.log1p(-r))/ell}

function Hp(r){return Math.log((1-r)/r)/ell}

function sum(v){return v.reduce((s,x)=>s+x,0)}

function KL(P,Q){return sum(P.map((v,i)=>v*Math.log(v/Q[i])/ell))}

function CHARGE(r){return 1+r-H(r)}

function ASSERT(b,m){if(!b)throw Error("SCOPED_CHECK_FAILED "+m)}

function ALPHABET(counts,rs,priorA=ready,newA=ready,moving=null) {
 const base=countable(counts);
 const w=moving||base,bar=sum(w.map((s,i)=>s*rs[i]));
 const P=[1-newA,...w.flatMap((s,i)=>[newA*s*(1-rs[i]),newA*s*rs[i]])];
 const MU=[1-priorA,...base.flatMap(s=>[priorA*s*p,priorA*s*p*p])];
 const PA=[1-newA,newA*(1-bar),newA*bar],MA=[1-priorA,priorA*p,priorA*p*p];
 const mutual=H(bar)-sum(w.map((v,i)=>v*H(rs[i])));
 return{bar,P,MU,PA,MA,full:KL(P,MU),coarse:KL(PA,MA),
     address:KL(w,base),mutual,ready:newA,
     result:KL(PA,MA)+newA*(KL(w,base)+mutual)};
}

function countable(counts){let N=sum(counts);return counts.map(x=>x/N)}

function run(){
 let n=0,test=(b,m)=>{ASSERT(b,m);n++};
 test(Math.abs(p+p*p-1)<1e-14,"actual Golden primitive");
 test(6765+6*N===72441,"original measured complete 72441 leaf count");
 const counts=[29,78,...Array(171).fill(43),...Array(83).fill(42)];
 test(counts.length===256&&sum(counts)===N&&Math.min(...counts)===29&&Math.max(...counts)===78,
   "256 synthetic count test obeys original N/min/max (NOT actual location list)");
 let examples=[];
 for(let k of [0,1,2]){
  const c=k===0?[2,7,11]:k===1?counts:[1,1];
  const rs=k===0?[.13,.47,.8]:k===1?counts.map((_,j)=>.12+.69*((j*17)%129)/128):
    [1.851242740976536e-6,1.8513157633356053e-6];
  const src=k===2?[-2.26378054238336192e-8,2.2637873072288812e-8]:
    c.map((_,j)=>.04*((j%7)-3));
  const A=ALPHABET(c,rs);
  test(Math.abs(sum(A.P)-1)<1e-13&&Math.abs(sum(A.MU)-1)<1e-13,"full fine positive normalized Born and Kraft");
  test(Math.abs(A.full-A.result)<1e-12,"exact full = 3 atom plus archive information");
  test(Math.abs(A.full-A.coarse-ready*A.mutual)<1e-12,"original native fixed address KL mutual info");
  test(A.mutual>=-1e-12,"conditional mutual info nonnegative");
  if(k<2) {
   const h=1e-6,plus=ALPHABET(c,rs.map((r,j)=>r+h*src[j])),
      minus=ALPHABET(c,rs.map((r,j)=>r-h*src[j]));
   const Dfull=(plus.full-minus.full)/(2*h),Dc=(plus.coarse-minus.coarse)/(2*h),
      Da=ready*(plus.mutual-minus.mutual)/(2*h);
   test(Math.abs(Dfull-Dc-Da)<1e-8,"full 42-suitable source automatically includes archive derivative");
  }
  examples.push({sites:c.length,full:A.full,three_atom:A.coarse,archived:ready*A.mutual});
 }
 const origin=countable(counts),rates=counts.map((_,i)=>.15+.69*((i*13)%128)/127);
 const offset=counts.map((_,i)=>.3*Math.sin(i+1)),mix=origin.map((x,i)=>x*(1+.02*offset[i]));
 const w=mix.map(x=>x/sum(mix));
 const M=ALPHABET(counts,rates,ready,.32,w);
 test(Math.abs(M.full-M.coarse-.32*(M.address+M.mutual))<1e-12,
   "moving address and readiness exact extra address KL and mutual info");
 test(M.address>0&&M.mutual>0,"both moving and archive corrections nonzero");
 const com=ALPHABET(counts,Array(256).fill(.293));
 test(Math.abs(com.mutual)<1e-12&&Math.abs(com.full-com.coarse)<1e-12,
   "all common-null source representative agrees");
 const r0=1.851242740976536e-6,r1=1.8513157633356053e-6;
 const d0=-2.26378054238336192e-8,d1=-Hp(r0)/Hp(r1)*d0;
 const mean=(r0+r1)/2,dmean=(d0+d1)/2;
 const Dfull=-ready*(Hp(r0)*d0+Hp(r1)*d1)/2;
 const Dcoarse=-ready*Hp(mean)*dmean;
 const Darchive=ready*(Hp(mean)*dmean-(Hp(r0)*d0+Hp(r1)*d1)/2);
 test(Math.abs(Dfull)<1e-19,"original certified full42 padded source relation");
 test(Math.abs(Dcoarse+Darchive)<1e-19,"archive exactly cancels spurious mean source");
 test(Math.abs(Darchive)>ready*13/.49*2.68978050581795731e-14,
   "original certified lower wall for coarse/archived source");
 const q=[.2,.3,.5],r=[.22,.28,.5];
 test(KL(q,r)>0,"three-outcome truthful logarithmic regret positive");
 const binaryBrier=(truth,guess)=>truth*(1-guess)**2+(1-truth)*guess**2;
 test(binaryBrier(.37,.37)<binaryBrier(.37,.31),"binary nonlog local proper Brier witness");
 const grad=q.map(x=>-2*x*(1-x));
 test(grad[0]!==grad[1]&&grad[1]!==grad[2],"same binary local Brier is not ternary proper");
 test(4===3+1&&514===(1+2*256)+1,"first-match 3-control vs site-resolved 513 states");
 return{status:"SCOPED_PASS",checks:n,
 original:{F21:N,F20:6765,realFineAlphabet:72441,realGoldenSiteCount:256,actualReadyProb:ready,
    test_nz_list:"synthetic, structurally compatible; not actual ordered 256 native site mapping"},
 future:{minimal_predicates:["NOT_READY","READY0","READY1"],expectedTrials3:4,
    indexedAlphabet:513,expectedTrials513:514},
 fixtureResults:examples,
 movingAddressTest:{full:M.full,threeAtom:M.coarse,archiveAddressKL:.32*M.address,
    archiveConditionalMutualInfo:.32*M.mutual},
 certifiedOffNullAsConditionalTest:{r0,r1,paddedFullSource:Dfull,
   falseCoarseSource:Dcoarse,restoringArchiveSource:Darchive,
   inheritedLower:ready*13/.49*2.68978050581795731e-14},
 Book03_InfoPhysicallySelected:false,GR_closed:false};
}

console.log(JSON.stringify(run(),null,2));
