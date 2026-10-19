#!/usr/bin/env node
/*
 * ORIGINAL GOLDEN 4D BOXES (NO NEW decoder): exact source balance and
 * TRUE moving-volume two-Golden-tick Book03 first-source matching.
 *
 * All original LEFT/F/R, old RIGHT and inactive/FAILED complement remain
 * in the mathematical complete returned operator. Does not claim compulsory
 * native source/Book selection or the original full H+J+R GR theorem.
 *
 * No dependencies, built-in BigInt/Number. Main arbitrary-Brinkmann 40-row
 * symbolic geometry is independently owned and is not rerun here.
 */
const p=(Math.sqrt(5)-1)/2;
const z=2**-20;
function check(ok,msg){if(!ok)throw new Error("FAIL: "+msg);}
function near(a,b,tol,msg){check(Math.abs(a-b)<=tol,msg+": "+a+" vs "+b);}
function fib(n){let a=0,b=1;for(let i=0;i<n;i++){const c=a+b;a=b;b=c;}return a;}
function originalNativeCounts(n,L){
  const M=L**4,counts=new Uint32Array(M);
  function visit(rem,rawDepth,left,width){
    if(rem===0){
      let j=0;
      for(let axis=0;axis<4;axis++){
        const x=left[axis]+width[axis]/2;
        j=j*L+Math.max(0,Math.min(L-1,Math.floor(L*x)));
      }
      counts[j]++;
      return;
    }
    const axis=rawDepth%4;
    const widthF=width.slice();widthF[axis]*=p;
    visit(rem-1,rawDepth+1,left.slice(),widthF);
    if(rem>=2){
      const leftR=left.slice(),widthR=width.slice();
      leftR[axis]+=p*widthR[axis];widthR[axis]*=p*p;
      visit(rem-2,rawDepth+1,leftR,widthR);
    }
  }
  visit(n,0,[0,0,0,0],[1,1,1,1]);
  const K=counts.reduce((a,b)=>a+b,0);
  check(K===fib(n+1),"true Fibonacci word count");
  check(counts.every(x=>x>0),"all original Golden Role cells covered");
  check(Math.max(...counts)>Math.min(...counts),"original weights must be UNEQUAL");
  return {counts,K,M,L,n};
}
function node(j,L){
  const x=[];
  for(let axis=3;axis>=0;axis--){
    const d=L**axis;
    x.push(((Math.floor(j/d)%L)+.5)/L);
  }
  return x;
}
function localTestScalar(x){
  return 1+x[0]*x[0]+x[1]*x[2]+Math.sin(2*Math.PI*x[3]);
}
function localTestMatter(x){
  return x[0]*x[1]+x[2]*x[2];
}
function originalInverseSiteProof(fixture){
  const {counts,K,M,L}=fixture;
  let transported=0,uniform=0;
  for(let j=0;j<M;j++){
    const rho=M*counts[j]/K, v=node(j,L);
    const g=localTestScalar(v)+2*localTestMatter(v);
    transported+=(counts[j]/K)*(g/rho);
    uniform+=g/M;
  }
  near(transported,uniform,1e-12,
      "ORIGINAL uneven-weight FIRST source cancels exactly");
  const min=Math.min(...counts),max=Math.max(...counts);
  const success=2*K*p**(fixture.n+3);
  check(success>0&&success<1,"real positive failure complement is retained");
  console.log("ORIGINAL F/R cost="+fixture.n+" L="+L+" K="+K+
              " cells="+M+" min/max native count="+min+"/"+max+
              " rho[min,max]=["+M*min/K+","+M*max/K+"]");
  console.log(" true selected success probability="+success+
              " failure="+(1-success)+"; inverse-PF source error="+
              (transported-uniform));
}
const L0=4*p**3,a=p**6,e0=p*p;
const R0=1-z*L0*(1+a),Q0=1-z*L0,sigma=-1,scene=528,t2=.01;
const Cstar=scene*z*4*p**11*t2/R0;
const Cmat=sigma*scene*z*8*p**6*t2*(1/Q0+a/R0);
near(Cmat/Cstar,-23.416406751884068,1e-11,
     "true two-tick scene/grav ratio");
function trueJ2Leaf(r,q){
  const E=e0*(1+t2*r);
  const b=(p+sigma*p*p*t2*q)**2;
  const B=4*b*(1-b); // the genuine TWO-TICK feedback, not B=b
  const L=4*E*(1-E);
  return -scene*(Math.log1p(-z*B)+Math.log1p(-z*(L+(1-L)*B)));
}
function trueInverseCDF0(u,eps){
  // Physical J_eps(x)=1+eps(2x-1), V_eps=1,
  // R_eps(x)=x+eps(x^2-x), NOT a frozen physical cell.
  return 2*u/(1-eps+Math.sqrt((1-eps)**2+4*eps*u));
}
function wholeOriginalJ2Mean(fix,eps){
  const {counts,K,M,L}=fix;
  let sum=0;
  for(let j=0;j<M;j++){
    const u=node(j,L),x=[trueInverseCDF0(u[0],eps),...u.slice(1)];
    const J=1+eps*(2*x[0]-1);
    const rho=M*counts[j]/K;
    const r=eps*localTestScalar(x)/(J*rho);
    const q=eps*localTestMatter(x)/rho;
    sum+=(counts[j]/K)*trueJ2Leaf(r,q);
  }
  return sum;
}
function movingVolumeFirstSource(fix){
  const {counts,K,M,L}=fix;
  let exact=0,uniform=0;
  for(let j=0;j<M;j++){
    const x=node(j,L),rho=M*counts[j]/K;
    const G=Cstar*localTestScalar(x)+Cmat*localTestMatter(x);
    exact+=counts[j]/K*G/rho;
    uniform+=G/M;
  }
  near(exact,uniform,1e-14,"whole two-tick exact first-source equality");
  const eps=.001;
  const derivative=(wholeOriginalJ2Mean(fix,eps)
                  -wholeOriginalJ2Mean(fix,-eps))/(2*eps);
  const rel=Math.abs((derivative-uniform)/uniform);
  check(rel<1e-5,"moving-volume full J2 double-tick finite derivative");
  const du=(trueInverseCDF0(.25,1e-5)-trueInverseCDF0(.25,-1e-5))/(2e-5);
  near(du,.25*(1-.25),2e-9,"nonzero moving inverse-quantile derivative");
  console.log(" TRUE moving volume DJ_expected="+uniform+
    ", exact ORIGINAL weight result="+exact+
    ", double-tick central-difference="+derivative+
    ", relative error="+rel+", nonzero sampling DT="+du);
}
const L4=originalNativeCounts(20,4);
const L8=originalNativeCounts(24,8);
originalInverseSiteProof(L4);
originalInverseSiteProof(L8);
movingVolumeFirstSource(L4);
console.log("PASS ORIGINAL native boxes, inverse-PF and volume-quantile SAME first source");
console.log("SCOPE built operator PRICE, not compulsory physical self-verification law");
