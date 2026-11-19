function runCoherentAttenuationAudit(){
  "use strict";
  const abs=n=>n<0n?-n:n;
  function gcd(a,b){a=abs(a);b=abs(b);while(b){const t=a%b;a=b;b=t;}return a||1n;}
  function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return {n:n/g,d:d/g};}
  const fadd=(x,y)=>F(x.n*y.d+y.n*x.d,x.d*y.d),fneg=x=>F(-x.n,x.d);
  const fsub=(x,y)=>fadd(x,fneg(y)),fmul=(x,y)=>F(x.n*y.n,x.d*y.d);
  const fdiv=(x,y)=>F(x.n*y.d,x.d*y.n),feq=(x,y)=>x.n===y.n&&x.d===y.d;
  const fsign=x=>x.n<0n?-1:x.n>0n?1:0;
  const Q=(a=F(0),b=F(0))=>({a,b}),rat=(n,d=1)=>Q(F(n,d));
  const add=(x,y)=>Q(fadd(x.a,y.a),fadd(x.b,y.b)),neg=x=>Q(fneg(x.a),fneg(x.b));
  const sub=(x,y)=>add(x,neg(y));
  const mul=(x,y)=>Q(fadd(fmul(x.a,y.a),fmul(x.b,y.b)),fsub(fadd(fmul(x.a,y.b),fmul(x.b,y.a)),fmul(x.b,y.b)));
  const eq=(x,y)=>feq(x.a,y.a)&&feq(x.b,y.b);
  const Z=rat(0),I=rat(1),P=Q(F(0),F(1)),TWO=rat(2),HALF=rat(1,2);
  function pow(x,n){let y=I;while(n){if(n&1)y=mul(y,x);x=mul(x,x);n=Math.floor(n/2);}return y;}
  function sign(x){
    const A=fsub(x.a,fdiv(x.b,F(2))),B=fdiv(x.b,F(2));
    if(!B.n)return fsign(A);if(!A.n)return fsign(B);
    if(fsign(A)===fsign(B))return fsign(A);
    const d=fsub(fmul(A,A),fmul(F(5),fmul(B,B)));
    if(!d.n)throw Error("unexpected rational sqrt5 equality");
    return fsign(d)>0?fsign(A):fsign(B);
  }
  const lt=(x,y)=>sign(sub(x,y))<0,le=(x,y)=>sign(sub(x,y))<=0;
  function isqrt(n){if(n<2n)return n;let x=1n<<BigInt((n.toString(2).length+1)>>1);for(;;){const y=(x+n/x)>>1n;if(y>=x)return x;x=y;}}
  const prec=384n,scale=1n<<prec,sqrt5floor=isqrt(5n*scale*scale);
  const pApprox=F(2n*sqrt5floor+1n-2n*scale,4n*scale);
  function floatF(x){
    if(!x.n)return 0;const nn=abs(x.n),nd=x.d;
    const sn=Math.max(0,nn.toString(2).length-53),sd=Math.max(0,nd.toString(2).length-53);
    return (x.n<0n?-1:1)*(Number(nn>>BigInt(sn))/Number(nd>>BigInt(sd)))*2**(sn-sd);
  }
  const fl=x=>floatF(fadd(x.a,fmul(x.b,pApprox)));
  let checks=0;
  const check=(ok,label)=>{checks++;if(!ok)throw Error("FAIL "+label);};
  const exact=(a,b,label)=>check(eq(a,b),label),diagnostics={};
  exact(add(P,pow(P,2)),I,"golden partition");
  check(lt(rat(3,5),P)&&lt(P,rat(5,8)),"golden order");
  function zeros(){return Array.from({length:4},()=>Array.from({length:4},()=>Z));}
  function put(M,i,j,x){M[i][j]=add(M[i][j],x);}
  function pop(n){let k=0;while(n){k+=n&1;n>>=1;}return k;}
  // Full isometry partial trace for every matrix unit on S x R.
  for(let m=0;m<=3;m++){
    const a=pow(P,m);
    for(let i=0;i<4;i++)for(let j=0;j<4;j++){
      const actual=zeros(),expected=zeros(),si=i>>1,sj=j>>1,ri=i&1,rj=j&1;
      for(let w=0;w<(1<<m);w++){
        const prob=pow(P,m+pop(w));
        for(let f=0;f<2;f++)for(let fp=0;fp<2;fp++){
          const pass=w===0,outi=pass?si:f,outj=pass?sj:fp,enni=pass?f:si,ennj=pass?fp:sj;
          if(enni===ennj)put(actual,2*outi+ri,2*outj+rj,mul(HALF,prob));
        }
      }
      put(expected,i,j,a);
      if(si===sj)for(let f=0;f<2;f++)for(let fp=0;fp<2;fp++)put(expected,2*f+ri,2*fp+rj,mul(HALF,sub(I,a)));
      for(let k=0;k<4;k++)for(let l=0;l<4;l++)exact(actual[k][l],expected[k][l],"matrix-unit m"+m+" i"+i+" j"+j+" k"+k+" l"+l);
    }
  }
  function local(M,a,which){
    const out=zeros();
    for(let i=0;i<4;i++)for(let j=0;j<4;j++){
      put(out,i,j,mul(a,M[i][j]));
      const si=which===0?i>>1:i&1,sj=which===0?j>>1:j&1,ri=which===0?i&1:i>>1,rj=which===0?j&1:j>>1;
      if(si===sj)for(let f=0;f<2;f++)for(let fp=0;fp<2;fp++){
        const oi=which===0?2*f+ri:2*ri+f,oj=which===0?2*fp+rj:2*rj+fp;
        put(out,oi,oj,mul(mul(HALF,sub(I,a)),M[i][j]));
      }
    }
    return out;
  }
  const bellTangent=zeros();
  for(let i=0;i<4;i++)for(let j=0;j<4;j++)bellTangent[i][j]=rat(((-1)**pop(i)+(-1)**pop(j)),4);
  function partial(M,which){
    const out=Array.from({length:2},()=>[Z,Z]);
    for(let i=0;i<4;i++)for(let j=0;j<4;j++){
      const ti=which===0?i>>1:i&1,tj=which===0?j>>1:j&1,ri=which===0?i&1:i>>1,rj=which===0?j&1:j>>1;
      if(ti===tj)out[ri][rj]=add(out[ri][rj],M[i][j]);
    }
    return out;
  }
  for(let w=0;w<2;w++)for(const row of partial(bellTangent,w))for(const x of row)exact(x,Z,"Bell tangent marginal zero");
  function ZZ(M){let q=Z;for(let i=0;i<4;i++)q=add(q,mul(rat((-1)**pop(i)),M[i][i]));return q;}
  exact(ZZ(bellTangent),TWO,"Bell tangent joint moment");
  const aa=pow(P,3);
  exact(ZZ(local(local(bellTangent,aa,0),aa,1)),mul(TWO,pow(aa,2)),"independent coherent attenuation of correlation");
  const shared=bellTangent.map(row=>row.map(x=>mul(aa,x)));
  exact(ZZ(shared),mul(TWO,aa),"shared prefix wrong correlation law");
  check(!eq(ZZ(shared),ZZ(local(local(bellTangent,aa,0),aa,1))),"shared-prefix negative control");
  const d=rat(1,64),z=rat(1,1048576),p2=pow(P,2),sigma=rat(-1),FOUR=rat(4),signed=(v,b)=>mul(v,rat(b?1:-1));
  function ellRow(bits){
    const e1=mul(p2,add(I,signed(d,bits&1))),e2=mul(p2,add(I,signed(d,(bits>>1)&1)));
    return mul(FOUR,mul(e1,sub(I,e2)));
  }
  function bRow(bits){
    const b=[];for(let k=0;k<4;k++)b.push(add(P,mul(sigma,mul(p2,signed(d,(bits>>k)&1)))));
    return mul(FOUR,mul(mul(b[0],b[1]),sub(I,mul(b[2],b[3]))));
  }
  const ellTab=Array.from({length:4},(_,i)=>ellRow(i)),bTab=Array.from({length:16},(_,i)=>bRow(i));
  for(const [i,x] of [...ellTab,...bTab].entries())check(lt(Z,x)&&lt(x,I),"positive constant table "+i);
  function report(l,b1,b2){const a=add(l,mul(sub(I,l),b1));return sub(mul(z,add(a,b2)),mul(pow(z,2),mul(a,b2)));}
  function analytic(x,y){
    const e=mul(p2,add(I,x)),l=mul(FOUR,mul(e,sub(I,e))),b=add(P,mul(sigma,mul(p2,y))),b2=pow(b,2),B=mul(FOUR,mul(b2,sub(I,b2)));
    return report(l,B,B);
  }
  const Lf=rat(3,2),Lq=rat(7,4),tf=rat(2,5),tq=rat(-1,3),tau=pow(P,12),af=mul(rat(64),mul(Lf,tau)),aq=mul(rat(64),mul(Lq,tau));
  check(le(af,I)&&le(aq,I),"native attenuations admissible");
  const f=mul(Lf,tf),q=mul(Lq,tq),means=[...Array(2).fill(mul(af,tf)),...Array(8).fill(mul(aq,tq))];
  let sum=Z,weight=Z;
  for(let bits=0;bits<1024;bits++){
    let w=I;for(let j=0;j<10;j++)w=mul(w,mul(HALF,add(I,signed(means[j],(bits>>j)&1))));
    weight=add(weight,w);
    sum=add(sum,mul(w,report(ellTab[bits&3],bTab[(bits>>2)&15],bTab[(bits>>6)&15])));
  }
  exact(weight,I,"ten independent slots complete");
  const target=analytic(mul(tau,f),mul(tau,q));
  exact(sum,target,"full 1024-leaf nonlinear r(tau u,tau v)");
  const r0=analytic(Z,Z),bad=add(mul(sub(I,tau),r0),mul(tau,analytic(f,q)));
  check(!eq(sum,bad),"branch averaging does not equal operand attenuation");
  function depth(x){let n=0,pp=I;while(lt(I,mul(x,pp))){n++;pp=mul(pp,P);if(n>10000)throw Error("depth overflow");}return n;}
  for(const lm of [Lf,Lq]){
    const b=depth(mul(rat(64),lm)),beta=mul(mul(rat(64),lm),pow(P,b));
    check(le(beta,I)&&(b===0||lt(P,beta)),"constant beta positive feasible");
    exact(mul(beta,pow(P,12-b)),mul(mul(rat(64),lm),tau),"native depth factorization");
  }
  const depthExamples=[];
  for(const L of [4,8,16,32,64])for(const power of [0,2,4]){
    const norm=rat(BigInt(L)**BigInt(power)),m=Math.max(depth(rat(L*L)),depth(mul(rat(64),norm))),th=pow(P,m);
    check(le(th,rat(1,L*L)),"h2 aperture");
    check(le(mul(rat(64),mul(norm,th)),I),"norm-aware feasible aperture");
    depthExamples.push({L,norm_power:power,m,tau:fl(th)});
  }
  // Quantitative positive-Q(p)-partition preparation with actual table rows.
  const partitions=[...ellTab,...bTab].map(w=>[w,sub(I,w)]);
  for(const lm of [Lf,Lq]){
    const b=depth(mul(rat(64),lm)),beta=mul(mul(rat(64),lm),pow(P,b));partitions.push([beta,sub(I,beta)]);
  }
  const lcm=(a,b)=>a/gcd(a,b)*b;let D=1n;
  for(const row of partitions)for(const w of row){D=lcm(D,w.a.d);D=lcm(D,w.b.d);}
  const intRows=partitions.map(row=>row.map(w=>[w.a.n*(D/w.a.d),w.b.n*(D/w.b.d)]));let Hheight=1n;
  for(const row of intRows)for(const [a,b] of row)Hheight=[Hheight,abs(a),abs(b)].reduce((x,y)=>x>y?x:y);
  let nn=0,phin=I;while(lt(phin,rat(4n*Hheight))){nn++;phin=mul(phin,add(I,P));}
  let f0=0n,f1=1n;for(let k=0;k<nn+2;k++){const f=f0+f1;f0=f1;f1=f;}
  const K=D*f0;
  for(const row of intRows){
    let Krow=0n;
    for(let [a,b] of row){
      if(a!==0n||b!==0n)check(le(I,mul(mul(Q(F(a),F(b)),pow(add(I,P),2)),rat(Hheight))),"integer norm lower bound");
      for(let k=0;k<nn;k++){const next=a+b;b=a;a=next;}
      check(a>=0n&&b>=0n,"positive prefix integer coefficients");Krow+=a+b;
    }
    check(Krow===K,"sum of label counts is D Fibonacci(n+2)");
  }
  let twok=1n,klabel=0;while(twok<K){twok*=2n;klabel++;}
  const arow=rat(D,twok);
  check(lt(I,mul(arow,rat(22n*Hheight))),"polynomial actual herald lower bound");
  diagnostics.partition_height=Hheight.toString();diagnostics.partition_prefix_depth=nn;diagnostics.partition_label_bits=klabel;diagnostics.partition_actual_herald=fl(arow);
  const Gamma=mul(rat(1024),pow(P,27));
  check(lt(Z,Gamma)&&lt(Gamma,I),"exact coherent Toffoli gamma");
  const probs=[sub(I,Gamma),mul(Gamma,sub(I,target)),mul(Gamma,target)];
  exact(probs.reduce(add,Z),I,"full abort/report distribution");
  const phi=(1+Math.sqrt(5))/2,ell=Math.log(phi),gn=fl(Gamma),rn=fl(target),entropy=xs=>xs.reduce((v,x)=>v-(x===0?0:x*Math.log(x)/ell),0);
  const h=x=>entropy([x,1-x]),hp=x=>Math.log((1-x)/x)/ell,H=entropy(probs.map(fl)),factorized=h(gn)+gn*h(rn);
  check(Math.abs(H-factorized)<2e-14,"complete CQ entropy numerical identity");
  const dr=.2,pr=[1-gn,gn*(1-rn),gn*rn],dpr=[0,-gn*dr,gn*dr],dH=-pr.reduce((v,x,i)=>v+dpr[i]*(Math.log(x)+1)/ell,0);
  check(Math.abs(dH-gn*hp(rn)*dr)<2e-13,"complete CQ entropy source numerical identity");
  check(Math.abs((gn*dr-dH)-gn*(1-hp(rn))*dr)<2e-13,"full 0/10 price source numerical identity");
  diagnostics.gamma_coherent_toffoli=gn;diagnostics.tau=fl(tau);diagnostics.attenuation_f=fl(af);diagnostics.attenuation_q=fl(aq);diagnostics.report=rn;
  diagnostics.naive_branch_average=fl(bad);diagnostics.complete_entropy_phi=H;diagnostics.factorized_entropy_phi=factorized;diagnostics.depth_examples=depthExamples;
  return {status:"PASS",checks,exact_field:"Q(p), p^2+p-1=0",source_commit:"3fcabfa0688f581fbbe54c70a342c8a49b9ca5fb",scope:["all SR matrix units through coherent attenuation; no diagonal-input assumption","10 independent sign slots and exact original ordered tables","correlated Bell tangent and shared-prefix negative control","native Golden norm-aware aperture factorization","quantitative positive-partition integer norm, Perron prefix and actual herald bound","complete abort/report CQ entropy and 0/10 price source"],limitations:["native table and measured-factory constructions consumed from pinned owners, not re-proved by this checker","entropy evaluations use floating logarithms; all channel, probability, report and aperture identities use exact rational arithmetic in Q(p)","no paid arbitrary continuous input-state writer, joint-bank preparation Euler, Book03 selection or GR closure is asserted"],diagnostics};
}
console.log(JSON.stringify(runCoherentAttenuationAudit(), null, 2));
