// Original six-face star + complete native compiler radial composition.
// Stdlib-only: node check_complete_compiler_coframe_equivalence.mjs.
// Consumed star_euler.py blob fb0d5d423e218f77ecd19d8e3acaf178e1321c79.
// This checks only the new composition, not the original all40 solution.
// Dyadic matrix fixture is exact in its elementary scaling checks;
// transcendental ledger comparisons are floating diagnostics of identities
// proved in COMPLETE_COMPILER_COFRAME_EQUIVALENCE.md.
function run() {
  const req=(q,m)=>{if(!q)throw Error(m);};
  const close=(a,b,m,tol=4e-11)=>req(Math.abs(a-b)<=tol*(1+Math.abs(a)+Math.abs(b)),m+": "+a+" / "+b);
  const Z=()=>Array.from({length:4},()=>Array(4).fill(0));
  const I=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>+(i===j)));
  const add=(A,B)=>A.map((r,i)=>r.map((x,j)=>x+B[i][j]));
  const sub=(A,B)=>A.map((r,i)=>r.map((x,j)=>x-B[i][j]));
  const mul=(A,B)=>A.map(r=>B[0].map((_,j)=>r.reduce((s,x,k)=>s+x*B[k][j],0)));
  const scale=(A,c)=>A.map(r=>r.map(x=>c*x));
  const tr=A=>A[0].map((_,j)=>A.map(r=>r[j]));
  const eq=(A,B)=>A.every((r,i)=>r.every((x,j)=>x===B[i][j]));
  const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
  const inv=A=>mul(mul(eta,tr(A)),eta);
  const pairs=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)pairs.push([a,b]);
  const eps=a=>{if(new Set(a).size!==4)return 0;let n=0;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)n+=+(a[i]>a[j]);return n%2?-1:1;};
  const col=(A,j)=>A.map(r=>r[j]);
  const wedge=(u,v)=>pairs.map(([a,b])=>u[a]*v[b]-u[b]*v[a]);
  const pairing=(W,R)=>{const C=mul(R,eta);let s=0;pairs.forEach(([a,b],k)=>pairs.forEach(([c,d])=>{s+=eps([a,b,c,d])*W[k]*C[c][d];}));return s;};
  const sites=Array.from({length:16},(_,i)=>[i&1,(i>>1)&1,(i>>2)&1,(i>>3)&1]);
  const idx=z=>z[0]+2*z[1]+4*z[2]+8*z[3];
  const shift=(z,a)=>{const v=z.slice();v[a]=1-v[a];return v;};
  const N2=Z(),N3=Z();N2[1][2]=N2[2][0]=1;N3[1][3]=N3[3][0]=1;
  const frames=sites.map((z,i)=>{const e=I();e[1][0]=(z[2]+2*z[3])/8;e[0][1]=(1+i%3)/64;e[2][3]=(i%2)/32;e[3][2]=z[0]/64;return e;});
  const links=sites.map(z=>[0,1,2,3].map(a=>{
    if(a)return I();
    const K=add(scale(N2,(1+z[2]+2*z[3])/16),scale(N3,(1+2*z[2]+z[3])/32));
    req(eq(mul(mul(K,K),K),Z()),"nilpotent original null link");
    return add(add(I(),K),scale(mul(K,K),.5));
  }));
  links.flat().forEach(U=>req(eq(mul(mul(tr(U),eta),U),eta),"exact proper-Lorentz link"));
  const weights=sites.map((_,i)=>1+i%3); // hostile unequal-weight fixture, not a new PF law
  const zeroFrames=()=>sites.map(Z);
  const zeroLinks=()=>sites.map(()=>[0,1,2,3].map(Z));
  function curves(dlinks=zeroLinks()){
    return sites.map((z,zi)=>pairs.map(([r,t])=>{
      const edges=[[zi,r,false],[idx(shift(z,r)),t,false],[idx(shift(z,t)),r,true],[zi,t,true]];
      let P=I(),dP=Z();
      for(const [k,a,reverse] of edges){
        let U=links[k][a],dU=dlinks[k][a];
        if(reverse){U=inv(U);dU=scale(mul(mul(U,dU),U),-1);}
        dP=add(mul(dP,U),mul(P,dU));P=mul(P,U);
      }
      const Pi=inv(P);
      return {R:scale(sub(P,Pi),.5),dR:scale(add(dP,mul(mul(Pi,dP),Pi)),.5)};
    }));
  }
  function densities(e,de,C){
    return sites.map((_,i)=>{
      let value=0,jet=0;
      pairs.forEach(([r,t],k)=>{
        const [u,v]=[0,1,2,3].filter(j=>j!==r&&j!==t),sign=eps([r,t,u,v]);
        const W=wedge(col(e[i],u),col(e[i],v));
        const dW=wedge(col(de[i],u),col(e[i],v)).map((a,j)=>a+wedge(col(e[i],u),col(de[i],v))[j]);
        value+=sign*pairing(W,C[i][k].R);
        jet+=sign*(pairing(dW,C[i][k].R)+pairing(W,C[i][k].dR));
      });
      return {value,jet};
    });
  }
  const C0=curves(),f=densities(frames,zeroFrames(),C0).map(x=>x.value);
  req(f.some(x=>x!==0),"fixture must leave zero-density shell");
  const radial=sites.map((_,i)=>(2+i%3)/2);
  const fs=densities(frames.map((e,i)=>scale(e,radial[i])),zeroFrames(),C0);
  fs.forEach((x,i)=>req(x.value===radial[i]**2*f[i],"exact independent site homogeneity"));
  const p=(Math.sqrt(5)-1)/2,z=2**-20,L=4*p**3,Q=1-z*L,A0=L*(1+p**6),R=1-z*A0;
  const r0=z*(L+A0)-z*z*L*A0,etaProbe=1/4,lnphi=Math.log(1/p);
  const Kbank=9,Lgate=20,b2=1-p**(6*Lgate),b3=1-(1-16*p**9)**Lgate;
  const alpha=(1-(1-2*p**3)**Kbank)**128,beta=(b2**4*b3)**43;
  req(128*(.53**Kbank)<=.5&&alpha>=.5&&beta>.5,"actual finite native readiness bounds");
  req(0<r0&&r0<2**-19,"native click corridor");
  const h=r=>-(r*Math.log(r)+(1-r)*Math.log1p(-r))/lnphi;
  const hp=r=>Math.log((1-r)/r)/lnphi;
  const hpp=r=>-1/(lnphi*r*(1-r));
  const Ax=4*p**11,Axx=-8*p**10;
  const rf0=Q*z*Ax*etaProbe**2,c=-alpha*beta*hp(r0)*rf0;
  const deltaH=dr=>{
    const r=r0+dr,d=1-r;
    return -(dr*Math.log(r0/(1-r0))+r*Math.log1p(dr/r0)+d*Math.log1p(-dr/(1-r0)))/lnphi;
  };
  function ledger(fv){
    const x=etaProbe**2*fv,dr=Q*z*(Ax*x+.5*Axx*x*x),r=r0+dr;
    const rf=Q*z*(Ax+Axx*x)*etaProbe**2,rff=Q*z*Axx*etaProbe**4;
    const phi=-alpha*beta*deltaH(dr),pf=-alpha*beta*hp(r)*rf;
    const chi=fv===0?1:phi/(c*fv);
    const pff=-alpha*beta*(hpp(r)*rf*rf+hp(r)*rff);
    const chif=fv===0?pff/(2*c):(pf*fv-phi)/(c*fv*fv);
    req(chi>0&&pf/c>0,"regular positive radial chart");
    return {phi,pf,chi,chif,s:Math.sqrt(chi),r,rf};
  }
  const F=f.map(ledger),dressed=frames.map((e,i)=>scale(e,F[i].s));
  const fd=densities(dressed,zeroFrames(),C0);
  fd.forEach((x,i)=>close(x.value,F[i].phi/c,"six-face action equality"));
  close(fd.reduce((s,x,i)=>s+weights[i]*x.value,0),F.reduce((s,x,i)=>s+weights[i]*x.phi/c,0),"weighted full action equality");
  let count=0,omittedLinkMap=0;const coframeGrad=[];
  function checkDirection(de,dlinks,label){
    const C=curves(dlinks),raw=densities(frames,de,C),df=raw.map(x=>x.jet);
    const det=de.map((v,i)=>add(scale(v,F[i].s),scale(frames[i],F[i].chif*df[i]/(2*F[i].s))));
    const transformed=densities(dressed,det,C);
    const lhs=df.reduce((s,x,i)=>s+weights[i]*F[i].pf*x/c,0);
    const rhs=transformed.reduce((s,x,i)=>s+weights[i]*x.jet,0);
    close(lhs,rhs,label);
    if(label.startsWith("link")){
      const wrong=densities(dressed,zeroFrames(),C).reduce((s,x,i)=>s+weights[i]*x.jet,0);
      omittedLinkMap=Math.max(omittedLinkMap,Math.abs(lhs-wrong));
    }
    count++;return df;
  }
  for(let a=0;a<4;a++)for(let r=0;r<4;r++){
    const de=zeroFrames();de[0][a][r]=1;
    const df=checkDirection(de,zeroLinks(),"coframe "+a+","+r);
    req(df.every((x,i)=>i===0||x===0),"coframe locality at other based cells");
    coframeGrad.push(df[0]);
  }
  const lie=pairs.map(([a,b])=>{const X=Z();X[a][b]=1;X[b][a]=-1;return mul(X,eta);});
  for(let a=0;a<4;a++)for(let k=0;k<6;k++){
    const du=zeroLinks();du[0][a]=mul(lie[k],links[0][a]);
    checkDirection(zeroFrames(),du,"link "+a+","+k);
  }
  req(count===40&&omittedLinkMap>1e-10,"shared-link pullback is necessary");
  function determinant(A){
    A=A.map(r=>r.slice());let out=1;
    for(let i=0;i<A.length;i++){
      let j=i;for(let k=i+1;k<A.length;k++)if(Math.abs(A[k][i])>Math.abs(A[j][i]))j=k;
      req(A[j][i]!==0,"nonsingular diagnostic Jacobian");
      if(j!==i){[A[i],A[j]]=[A[j],A[i]];out=-out;}
      const x=A[i][i];out*=x;
      for(let k=i+1;k<A.length;k++){const t=A[k][i]/x;for(let q=i+1;q<A.length;q++)A[k][q]-=t*A[i][q];}
    }return out;
  }
  const eflat=frames[0].flat(),s=F[0].s,ds=F[0].chif/(2*s);
  const Jac=eflat.map((v,i)=>coframeGrad.map((g,j)=>(i===j?s:0)+ds*v*g));
  close(determinant(Jac),F[0].chi**7*F[0].pf/c,"16-leg exact determinant formula");
  // Moving probe coordinate: includes the change of the coefficient c.
  const deEta=frames.map((e,i)=>scale(e,F[i].chif*f[i]/(etaProbe*F[i].s)));
  const dtEta=densities(dressed,deEta,C0);
  const leftEta=f.reduce((a,x,i)=>a+weights[i]*F[i].pf*(2*x/etaProbe)/c,0);
  const rightEta=fd.reduce((a,x,i)=>a+weights[i]*(2*x.value/etaProbe+dtEta[i].jet),0);
  close(leftEta,rightEta,"complete moving-probe/coefficient source");
  // Formal ledger sensitivities, not a claim that arbitrary prices are physical coordinates.
  const mass=weights.reduce((a,b)=>a+b,0);
  const alphaNonCost=f.reduce((a,_,i)=>a-weights[i]*beta*h(F[i].r),0);
  const alphaTarget=-mass*beta*h(r0)+fd.reduce((a,x,i)=>a+weights[i]*(c/alpha)*x.value,0);
  close(alphaNonCost,alphaTarget,"baseline alpha source retained");
  req(alpha*mass>0,"actual admitted mean-cost sensitivity cannot be erased");
  const entropyOccupationDerivative=-alpha*beta*rf0;
  req(entropyOccupationDerivative!==0,"N2 derivative per unit H_T omitted by coarse ledger");
  // Actual independent native two-density chart; no cost or kappa estimate.
  const By=8*p**6,Byy=8*p**4*(1-6*p*p),Ay=8*p**12,Axy=-32*p**11,Ayy=p**6*Byy;
  const rx=Q*z*Ax,ry=z*(R*By+Q*Ay);
  const rxx=Q*z*Axx,rxy=Q*z*Axy-z*z*By*Ax,ryy=z*(R*Byy+Q*Ayy)-2*z*z*By*Ay;
  req(rx>0&&ry>0&&rxx<0&&rxy<0&&ryy<0,"exact-sign native two-density jet");
  const ratio=rx/ry,rv=2*rx,rvv=rxx+2*ratio*rxy+ratio*ratio*ryy;
  const Hvv=-alpha*beta*(hpp(r0)*rv*rv+hp(r0)*rvv);
  req(Hvv>0,"strict two-density radial obstruction");
  // Finite one-sided AM-GM witness, evaluated without subtraction of nearly equal baselines.
  const t=1/100,x=t,y=ratio*t,Byv=4*(p+p*p*y)**2*(1-(p+p*p*y)**2);
  const ell=4*(p*p*(1+x))*(1-p*p*(1+x)),Av=ell+(1-ell)*Byv;
  const rr=z*(Byv+Av)-z*z*Byv*Av;
  const actual=-alpha*beta*deltaH(rr-r0),linear=-2*alpha*beta*hp(r0)*rx*t;
  req(actual>linear,"finite AM-GM obstruction witness");
  return {status:"PASS",geometry:"original six based faces, 16 sites",new_source_rows:count,
    alpha,beta,nonzero_native_c:c,max_omitted_link_pullback:omittedLinkMap,
    exact_density_signs:"rx,ry>0; rxx,rxy,ryy<0",two_density_Hvv:Hvv,
    finite_AMGM_gap:actual-linear,
    scope:"new vacuum ledger/coframe composition; no physical Info, preparation root or nonvacuum all42 inference"};
}
if(typeof console!=="undefined"&&typeof console.log==="function")console.log(JSON.stringify(run(),null,2));
