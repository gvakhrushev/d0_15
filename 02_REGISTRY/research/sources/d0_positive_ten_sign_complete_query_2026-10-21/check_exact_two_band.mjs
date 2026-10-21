// D0 complete positive two-band outcome. Exact Golden field Q(p), p^2+p=1.
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const x=a%b;a=b;b=x}return a||1n};
const QD=10n**50n,PLO=61803398874989484820458683436563811772030917980576n,PHI=PLO+1n;
const ok=(v,msg)=>{if(!v)throw Error("CHECK_FAIL: "+msg)};
ok(PLO*PLO+PLO*QD<QD*QD && PHI*PHI+PHI*QD>QD*QD,"rational bracket isolates p");
class K{
 constructor(a,b=0,d=1){a=BigInt(a);b=BigInt(b);d=BigInt(d);ok(d>0n,"denominator");const g=gcd(gcd(a,b),d);this.a=a/g;this.b=b/g;this.d=d/g}
 static of(v){return v instanceof K?v:new K(v)}
 add(v){v=K.of(v);return new K(this.a*v.d+v.a*this.d,this.b*v.d+v.b*this.d,this.d*v.d)}
 neg(){return new K(-this.a,-this.b,this.d)}
 sub(v){return this.add(K.of(v).neg())}
 mul(v){v=K.of(v);return new K(this.a*v.a+this.b*v.b,this.a*v.b+this.b*v.a-this.b*v.b,this.d*v.d)}
 div(n){return new K(this.a,this.b,this.d*BigInt(n))}
 eq(v){v=K.of(v);return this.a===v.a&&this.b===v.b&&this.d===v.d}
 sign(){const a=this.a*QD+this.b*PLO,b=this.a*QD+this.b*PHI;if(a>0n&&b>0n)return 1;if(a<0n&&b<0n)return -1;if(this.a===0n&&this.b===0n)return 0;throw Error("ambiguous "+this.a+" "+this.b)}
 val(){return Number(this.a*QD+this.b*PLO)/Number(this.d*QD)}
 dyadic(){return (this.d&(this.d-1n))===0n}
}
const N=new K(0),O=new K(1),p=new K(0,1),eps=O.div(64),z=O.div(1048576),power=(x,k)=>{let y=O;for(let j=0;j<k;j++)y=y.mul(x);return y};
ok(p.mul(p).eq(O.sub(p)),"p^2=1-p");
class T{
 constructor(items=[]){this.m=new Map(items)}
 static c(x){return new T([["0,0",K.of(x)]])}
 static v(k){return new T([[k==="s"?"1,0":"0,1",O]])}
 add(x){const r=new T(this.m);for(const[k,v]of x.m){const a=(r.m.get(k)||N).add(v);if(a.sign()===0)r.m.delete(k);else r.m.set(k,a)}return r}
 scale(x){return new T([...this.m].map(([k,v])=>[k,v.mul(x)]))}
 sub(x){return this.add(x.scale(-1))}
 mul(x){const r=new T();for(const[k,v]of this.m)for(const[l,w]of x.m){const[a,b]=k.split(",").map(Number),[c,d]=l.split(",").map(Number),j=[a+c,b+d].join(","),q=(r.m.get(j)||N).add(v.mul(w));if(q.sign()===0)r.m.delete(j);else r.m.set(j,q)}return r}
 at(i,j){return this.m.get(i+","+j)||N}
 calc(s,t){let sum=0;for(const[k,v]of this.m){const[a,b]=k.split(",").map(Number);sum+=v.val()*s**a*t**b}return sum}
}
const I=T.c(O),s=T.v("s"),t=T.v("t"),p2=power(p,2),L=power(p,3).mul(4),outputs=[];
for(const sigma of [-1,1]){
 const E=I.add(s.scale(eps)).scale(p2),u=I.scale(p).add(t.scale(eps.mul(p2).mul(sigma)));
 const l=E.mul(I.sub(E)).scale(4),u2=u.mul(u),B=u2.mul(I.sub(u2)).scale(4);
 const A=l.add(I.sub(l).mul(B));
 const r=I.sub(I.sub(B.scale(z)).mul(I.sub(A.scale(z))));
 ok(r.m.size===27 && [...r.m.keys()].every(q=>{const[a,b]=q.split(",").map(Number);return a<=2&&b<=8}),"exact degree 2x8");
 ok([...r.m.values()].every(v=>v.dyadic()),"all conditional coefficients Z[p,1/2]");
 ok(r.at(2,8).eq(power(p,20).mul(power(eps,10)).mul(power(z,2)).mul(-64)),"nonzero top degree");
 const Q=O.sub(z.mul(L)),A0=L.mul(new K(2).sub(L)),R=O.sub(z.mul(A0)),r0=O.sub(Q.mul(R));
 const df=z.mul(Q).mul(power(p,11)).mul(4);
 const dq=z.mul(power(p,6)).mul(R.add(Q.mul(power(p,6)))).mul(8);
 ok(r.at(0,0).eq(r0),"actual complete Golden baseline");
 ok(r.at(1,0).eq(eps.mul(df)),"geometric jet");
 ok(r.at(0,1).eq(eps.mul(dq).mul(sigma)),"matter jet");
 const lhs=dq.mul(power(p,5)).mul(Q);
 const rhs=df.mul(2).mul(R.add(Q.mul(power(p,6))));
 ok(lhs.eq(rhs),"native finite lambda exact");
 let vNorm=N;for(const[key,c]of r.m)if(key!=="0,0")vNorm=vNorm.add(c.sign()<0?c.neg():c);
 ok(r0.sub(vNorm).sign()>0 && O.sub(r0.add(vNorm)).sign()>0,"strict all-word positivity");
 let min=Infinity,max=-Infinity;
 for(let mask=0;mask<1024;mask++){
  const g=[mask&1?1:-1,mask&2?1:-1],m=Array.from({length:8},(_,j)=>mask&(1<<(j+2))?1:-1);
  let beta=N;
  for(const[key,c]of r.m){
    const[a,b]=key.split(",").map(Number);let sign=1;
    for(let j=0;j<a;j++)sign*=g[j];
    for(let j=0;j<b;j++)sign*=m[j];
    beta=beta.add(c.mul(sign));
  }
  ok(beta.sign()>0&&O.sub(beta).sign()>0&&beta.dyadic(),"positive original branch "+mask);
  min=Math.min(min,beta.val());max=Math.max(max,beta.val());
 }
 const ss=.173,tt=-.221;let sum=0;
 for(let mask=0;mask<1024;mask++){
  const g=[mask&1?1:-1,mask&2?1:-1],m=Array.from({length:8},(_,j)=>mask&(1<<(j+2))?1:-1);
  let prob=1,beta=0;for(const a of g)prob*=(1+a*ss)/2;for(const b of m)prob*=(1+b*tt)/2;
  for(const[key,c]of r.m){const[a,b]=key.split(",").map(Number);let sign=1;for(let j=0;j<a;j++)sign*=g[j];for(let j=0;j<b;j++)sign*=m[j];beta+=sign*c.val()}
  sum+=prob*beta;
 }
 ok(Math.abs(sum-r.calc(ss,tt))<1e-16,"complete normalized 1024-path expectation");
 outputs.push({sigma,monomials:r.m.size,base:r0.val(),total_nonconstant_coefficients:vNorm.val(),strict_beta_lower:r0.sub(vNorm).val(),strict_beta_upper:r0.add(vNorm).val(),min_branch:min,max_branch:max,top_degree:r.at(2,8).val(),df_s:r.at(1,0).val(),dq_t:r.at(0,1).val(),ratio:sigma*dq.val()/df.val()});
}
function run(){return {status:"PASS_EXACT_TWO_BAND_FULL_POSITIVE_REPORT",rational_Golden_root_verified:true,complete_branch_count:1024,copy_degrees:[2,8],all_coefficient_branch_weights:"Z[p,1/2]",sigma_checks:outputs,writer_admitted:false,Book03_Info_selected:false,GR_closed:false}}
if(typeof console!=="undefined")console.log(JSON.stringify(run(),null,2));
