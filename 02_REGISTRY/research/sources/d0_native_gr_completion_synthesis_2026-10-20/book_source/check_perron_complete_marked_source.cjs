function checkPerronCompleteMarkedSource(){
// Exact finite CP/path/marked-source regression.
// Pure JavaScript, BigInt rational first jets. Fixtures are not a native price selector.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
class F{
 constructor(n=0n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 add(b){return new F(this.n*b.d+b.n*this.d,this.d*b.d);}
 neg(){return new F(-this.n,this.d);}
 sub(b){return this.add(b.neg());}
 mul(b){return new F(this.n*b.n,this.d*b.d);}
 inv(){return new F(this.d,this.n);}
 div(b){return this.mul(b.inv());}
 eq(b){return this.n===b.n&&this.d===b.d;}
 is0(){return this.n===0n;}
 str(){return this.d===1n?String(this.n):this.n+"/"+this.d;}
}
const f=(n,d=1)=>new F(n,d),F0=f(0),F1=f(1);
class J{
 constructor(v=F0,d=F0){this.v=v;this.d=d;}
 add(b){return new J(this.v.add(b.v),this.d.add(b.d));}
 neg(){return new J(this.v.neg(),this.d.neg());}
 sub(b){return this.add(b.neg());}
 mul(b){return new J(this.v.mul(b.v),this.d.mul(b.v).add(this.v.mul(b.d)));}
 inv(){return new J(this.v.inv(),this.d.neg().div(this.v.mul(this.v)));}
 div(b){return this.mul(b.inv());}
 eq(b){return this.v.eq(b.v)&&this.d.eq(b.d);}
 pow(n){let a=this,b=j(1);for(let k=0;k<n;k++)b=b.mul(a);return b;}
}
const j=(n,d=1,dn=0,dd=1)=>new J(f(n,d),f(dn,dd)),J0=j(0),J1=j(1);
let checks=0;
function ok(x,msg){checks++;if(!x)throw Error(msg);}
function equal(a,b,msg){ok(a.eq(b),msg);}
function sum(a){return a.reduce((s,x)=>s.add(x),J0);}
function transpose(A){return A[0].map((_,k)=>A.map(r=>r[k]));}
function mm(A,B){return A.map(row=>B[0].map((_,k)=>sum(row.map((x,l)=>x.mul(B[l][k])))));}
function madd(A,B){return A.map((r,i)=>r.map((x,k)=>x.add(B[i][k])));}
function sm(c,A){return A.map(r=>r.map(x=>c.mul(x)));}
function eye(n){return Array.from({length:n},(_,i)=>Array.from({length:n},(_,k)=>i===k?J1:J0));}
function zeros(n){return Array.from({length:n},()=>Array(n).fill(J0));}
function meq(A,B,msg){for(let i=0;i<A.length;i++)for(let k=0;k<A[0].length;k++)equal(A[i][k],B[i][k],msg);}
function rot(t){let den=J1.add(t.mul(t)),c=J1.sub(t.mul(t)).div(den),s=j(2).mul(t).div(den);return [[c,s.neg()],[s,c]];}
function diag(a,b){return [[a,J0],[J0,b]];}
const X=[[J0,J1],[J1,J0]];
const t=j(1,4,1,5),u=j(1,3,1,7),a=j(1,6,1,9);
const den=J1.add(u.mul(u)),ca=J1.sub(u.mul(u)).div(den),sa=j(2).mul(u).div(den);
const M=[mm(rot(t),diag(ca,sa)),mm(X,diag(sa,ca))];
meq(madd(mm(transpose(M[0]),M[0]),mm(transpose(M[1]),M[1])),eye(2),"moving Kraus completeness");
ok(mm(M[0],M[1]).some((r,i)=>r.some((x,k)=>!x.v.eq(mm(M[1],M[0])[i][k].v))),"genuinely noncommuting Kraus pair");
const R=rot(a),v=[j(3,5).mul(R[0][0]),j(4,5).mul(R[0][1]),j(3,5).mul(R[1][0]),j(4,5).mul(R[1][1])];
equal(sum(v.map(x=>x.mul(x))),J1,"normalized moving pure preparation");
function applyLeft(A,w){return [0,1,2,3].map(i=>sum([0,1].map(k=>A[Math.floor(i/2)][k].mul(w[2*k+i%2]))));}
let oldR=[[J0,J0],[J0,J0]];
for(let b=0;b<2;b++)for(let c=0;c<2;c++)oldR[b][c]=sum([0,1].map(k=>v[2*k+b].mul(v[2*k+c])));
meq(oldR,diag(j(9,25),j(16,25)),"old RIGHT is exactly fixed, including derivative");
const P=[
 [J0,j(2,5,1,13),j(3,5,-1,13)],
 [j(3,7,-1,17),J0,j(4,7,1,17)],
 [j(5,11,1,19),j(6,11,-1,19),J0]
];
const r=[j(2,9,1,23),j(1,3,-1,29),j(4,9).sub(j(0,1,1,23)).add(j(0,1,1,29))];
const mu=[j(1,4,1,37),j(1,4,-1,37),j(1,2)],lam=j(7,5,1,31);
equal(sum(r),J1,"moving one-sided r normalization");equal(sum(mu),J1,"moving alternative mu normalization");
P.forEach(row=>equal(sum(row),J1,"moving stochastic row"));
const K=P.map((row,i)=>row.map((x,k)=>lam.mul(r[i]).mul(x).div(r[k])));
function mv(A,w){return A.map(row=>sum(row.map((x,i)=>x.mul(w[i]))));}
mv(K,r).forEach((x,i)=>equal(x,lam.mul(r[i]),"exact moving Perron equation"));
const As=[
 [[j(2),j(1,3)],[j(1,3),j(3)]],
 [[j(1),j(-1,2)],[j(-1,2),j(4)]],
 [[j(5),j(2,3)],[j(2,3),j(-1)]]
];
function cp(A){return M.reduce((z,m)=>madd(z,mm(transpose(m),mm(A,m))),zeros(2));}
function transfer(W,A){return W.map(row=>row.reduce((z,w,k)=>madd(z,sm(w,cp(A[k]))),zeros(2)));}
const lhs=transfer(K,As.map((A,i)=>sm(r[i],A))).map((A,i)=>sm(r[i].inv(),A));
const rhs=transfer(P,As).map(A=>sm(lam,A));
lhs.forEach((A,i)=>meq(A,rhs[i],"full CP Perron similarity and derivative"));
transfer(P,[eye(2),eye(2),eye(2)]).forEach(A=>meq(A,eye(2),"unital transformed CP transfer"));
const N=3;
let qsum=J0,raw=J0,endpointZ=J0,mean=J0,marked=J0;
let dPrice=F0,dLaw=F0,dEndpoint=F0,dConditional=F0,scoreMean=F0,leafCount=0;
function visit(start,last,depth,w,wp,wk,ones,code,dlogK){
 if(depth===N){
  leafCount++;let cond=sum(w.map(x=>x.mul(x)));
  ok(cond.v.n>0n,"strict positive retained leaf fixture");
  let q=r[start].mul(wp).mul(cond),rawLeaf=mu[start].mul(wk).mul(cond),end=wk.mul(r[last]).mul(cond);
  let cost=j(3).add(j(ones,5)).add(j(code,101)).add(j(0,1,last+1,11));
  let info=j(start+1,13).add(j(0,1,ones+1,7)),price=cost.sub(info);
  qsum=qsum.add(q);raw=raw.add(rawLeaf);endpointZ=endpointZ.add(end);
  mean=mean.add(q.mul(price));marked=marked.add(end.mul(price));
  dPrice=dPrice.add(q.v.mul(price.d));dLaw=dLaw.add(q.d.mul(price.v));
  let endScore=r[last].d.div(r[last].v),condScore=cond.d.div(cond.v);
  let score=dlogK.add(endScore).add(condScore).sub(lam.d.div(lam.v).mul(f(N)));
  equal(new J(score),new J(q.d.div(q.v)),"retained endpoint/pressure/conditional score");
  scoreMean=scoreMean.add(q.v.mul(score));
  dEndpoint=dEndpoint.add(q.v.mul(price.v).mul(endScore));
  dConditional=dConditional.add(q.v.mul(price.v).mul(condScore));
  return;
 }
 for(let next=0;next<3;next++)if(next!==last)for(let b=0;b<2;b++){
  let ke=K[last][next],pe=P[last][next];
  visit(start,next,depth+1,applyLeft(M[b],w),wp.mul(pe),wk.mul(ke),ones+b,code*7+2*next+b,dlogK.add(ke.d.div(ke.v)));
 }
}
for(let start=0;start<3;start++)visit(start,start,0,v,J1,J1,0,0,F0);
equal(qsum,J1,"complete normalized Doob event law");
equal(endpointZ,lam.pow(N),"raw terminal-marked partition lambda^N");
equal(mean,marked.div(lam.pow(N)),"finite actual marked mean and complete derivative");
let vec=[J1,J1,J1];for(let k=0;k<N;k++)vec=mv(K,vec);
equal(raw,sum(mu.map((x,i)=>x.mul(vec[i]))),"raw allbranch partition with moving preparation and initial weights");
ok(mean.d.eq(dPrice.add(dLaw)),"mean derivative includes actual price and sampling terms");
ok(scoreMean.is0(),"complete score mean is zero");
ok(!dPrice.is0(),"hostile omission of explicit cost/Info derivative rejected");
ok(!dEndpoint.is0(),"hostile omission of moving final endpoint rejected");
ok(!dConditional.is0(),"hostile omission of moving conditional instrument/preparation rejected");

// Flag-dependent stopping: lambda^{-length} stays inside the full sum.
let stopQ=J0,stopMean=J0,stopMarked=J0,stopLeaves=0,wrongFixedPressure=F0;
function visitStop(start,last,depth,w,wp,wk,ones,code,logK,terminal){
 if(terminal||depth===N){
  stopLeaves++;const cond=sum(w.map(x=>x.mul(x)));
  const q=r[start].mul(wp).mul(cond),correctRaw=wk.mul(r[last]).mul(cond).div(lam.pow(depth));
  const price=j(2+depth).add(j(code,97)).add(j(0,1,ones+1,11));
  equal(q,correctRaw,"complete stopped path with actual pressure exponent");
  stopQ=stopQ.add(q);stopMean=stopMean.add(q.mul(price));stopMarked=stopMarked.add(correctRaw.mul(price));
  wrongFixedPressure=wrongFixedPressure.add(q.v.mul(price.v).mul(lam.d.div(lam.v)).mul(f(N-depth)));
  return;
 }
 for(let next=0;next<3;next++)if(next!==last)for(let b=0;b<2;b++){
  const ke=K[last][next],pe=P[last][next];
  visitStop(start,next,depth+1,applyLeft(M[b],w),wp.mul(pe),wk.mul(ke),ones+b,code*7+2*next+b,logK.add(ke.d.div(ke.v)),b===1);
 }
}
for(let start=0;start<3;start++)visitStop(start,start,0,v,J1,J1,0,0,F0,false);
equal(stopQ,J1,"all stopped branches and cap retained");
equal(stopMean,stopMarked,"stopped marked mean and full derivative");
ok(!wrongFixedPressure.is0(),"hostile common N pressure on variable-length records rejected");

// Exact source support only: no repeated canonical Perron calculation.
const sizes=[9,11,13],part=Array(9).fill(0).concat(Array(11).fill(1),Array(13).fill(2));
const r718=part.map((_,i)=>j(i+1,561,i===0?1:i===1?-1:0,41));
const lambda718=j(3,2,1,17);
const K718=part.map((g,i)=>part.map((h,k)=>g===h?J0:lambda718.mul(r718[i]).div(j(33-sizes[g]).mul(r718[k]))));
let edges=0;part.forEach((g,i)=>part.forEach((h,k)=>{if(g!==h)edges++;}));
ok(edges===718,"literal K(9,11,13) directed edge support");
let rv=r718;for(let k=0;k<3;k++)rv=mv(K718,rv);
equal(sum(rv),lambda718.pow(3),"full718 scalar terminal partition and derivative");

// Ledger differential: hstar is a held symbolic constant instantiated rationally.
// This tests only the polynomial/product-rule identity, not a native entropy value.
const al=j(4,5,-1,17),be=j(5,6,1,19),mus=j(60,1,3,11),ht=j(2,1,1,13);
const cpref=j(5,1,1,23),hpref=j(1,1,-1,29),qs=j(2,9),hs=j(5,7),nc=4;
function EN(x,n){return sum(Array.from({length:n},(_,k)=>x.pow(k)));}
function ENprime(x,n){return sum(Array.from({length:n-1},(_,k)=>j(k+1).mul(x.pow(k))));}
const xx=be.mul(qs),EE=EN(xx,nc),EP=ENprime(xx,nc),aa=mus.sub(ht).sub(be.mul(hs));
const baseline=cpref.sub(hpref).add(al.mul(aa).mul(EE));
const dB=cpref.d.sub(hpref.d)
 .add(aa.v.mul(EE.v).mul(al.d))
 .add(al.v.mul(EE.v).mul(mus.d.sub(ht.d)))
 .add(al.v.mul(qs.v.mul(aa.v).mul(EP.v).sub(hs.v.mul(EE.v))).mul(be.d));
ok(baseline.d.eq(dB),"all moving complete compiler baseline terms retained");
const nextB=cpref.sub(hpref).add(al.mul(aa).mul(EN(xx,nc+1)));
equal(nextB.sub(baseline),al.mul(aa).mul(xx.pow(nc)),"held-bank exact horizon baseline increment and source");

return {
 result:"PASS", checks, complete_three_step_leaves:leafCount, stopped_leaves:stopLeaves, original_supported_edges:edges,
 exact_mean:mean.v.str(), exact_mean_derivative:mean.d.str(),
 omitted_explicit_price_source:dPrice.str(),
 omitted_final_endpoint_source:dEndpoint.str(),
 omitted_conditional_source:dConditional.str(),
 scope:"Noncommuting Kraus + fixed oldRIGHT first-jet algebra; full718 support scalar only. No physical Info selection, old native replay, or GR claim."
};

}
if (typeof module !== 'undefined') module.exports=checkPerronCompleteMarkedSource;
if (typeof require !== 'undefined' && require.main===module) console.log(JSON.stringify(checkPerronCompleteMarkedSource(),null,2));
