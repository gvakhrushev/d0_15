#!/usr/bin/env node
"use strict";
/*
 * Flat small-field SYMBOL of original 40 independent Euler rows.
 * Six based plaquettes, original eta/star, all 16 solder and 24
 * proper Lorentz left-link directions, and BOTH adjacent faces.
 *
 * For real nonzero Laurent variables z=(zu,zv,zx,zy),
 * L(z) = dE_link / d omega; B(z)=dE_link / d e;
 * C(z)=dE_e / d omega, and S=-C L^-1 B.
 * The action is linear in curvature, quadratic in e, hence A_ee=0.
 *
 * Checks transpose-adjoint S(z)^T=S(1/z) and four exact difference
 * gradient gauge directions for each of several distinct z.
 * Ranks are NUMERICAL diagnostic only, not exact Laurent-rational rank
 * theorem or full native physical action.
 */
const n=4, ids=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];
const eye=()=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const zmat=()=>Array.from({length:n},()=>Array(n).fill(0));
const E=(a,b)=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(a===i&&b===j)));
const add=(A,B)=>A.map((r,i)=>r.map((x,j)=>x+B[i][j]));
const sub=(A,B)=>A.map((r,i)=>r.map((x,j)=>x-B[i][j]));
const sc=(A,k)=>A.map(r=>r.map(v=>v*k));
const mul=(A,B)=>A.map((r,i)=>r.map((_,j)=>r.reduce((s,v,k)=>s+v*B[k][j],0)));
const eps=(...a)=>{if(new Set(a).size!==4)return 0;let s=1;
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)if(a[i]>a[j])s=-s;return s};
const gens=ids.map(([i,j])=>mul(sub(E(i,j),E(j,i)),eta));
function pairing(F,u,v,R){
  let C=mul(R,eta),tot=0;
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
    const [c,d]=[0,1,2,3].filter(k=>k!==a&&k!==b);
    tot+=eps(a,b,c,d)*(F[a][u]*F[b][v]-F[b][u]*F[a][v])*C[c][d];
  }
  return tot;
}
function pairDeriv(a,mu,u,v,R){
  if(mu!==u&&mu!==v)return 0;
  let F=eye();for(let b=0;b<4;b++)F[b][mu]=+(a===b);
  return pairing(F,u,v,R);
}
const dot=(z,p)=>p.reduce((prod,x,i)=>prod*z[i]**x,1);
const shift=(p,dir,k=1)=>p.map((x,i)=>x+(dir===i?k:0));
function linkLinear(z,axis,inputgen){
  const point=[0,0,0,0],rows=Array(24).fill(0);
  const field=(p,dir)=>dir===axis?sc(gens[inputgen],dot(z,p)):zmat();
  for(let outdir=0;outdir<4;outdir++)for(let j=0;j<6;j++){
    let tot=0,X=gens[j];
    for(let [r,t] of ids){
      if(outdir!==r&&outdir!==t)continue;
      const other=outdir===r?t:r,[u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t);
      for(let base of [point,shift(point,other,-1)]){
        const edges=[[base,r,1],[shift(base,r),t,1],
                     [shift(base,t),r,-1],[base,t,-1]];
        const W=edges.map(([p,k,sgn])=>sc(field(p,k),sgn));
        const P1=W.reduce(add,zmat());
        let dP0=zmat(),dP1=zmat();
        for(let k=0;k<4;k++){
          const [p,dir,sgn]=edges[k];
          if(dir!==outdir||!p.every((v,i)=>v===point[i]))continue;
          const d0=sc(X,sgn);
          const d1=sgn===1?mul(X,field(p,dir)):mul(field(p,dir),X);
          dP0=add(dP0,d0);
          let tmp=d1;
          for(let l=0;l<k;l++)tmp=add(tmp,mul(W[l],d0));
          for(let l=k+1;l<4;l++)tmp=add(tmp,mul(d0,W[l]));
          dP1=add(dP1,tmp);
        }
        const dR=sub(dP1,sc(add(mul(P1,dP0),mul(dP0,P1)),.5));
        tot+=eps(r,t,u,v)*pairing(eye(),u,v,dR);
      }
    }
    rows[6*outdir+j]=tot;
  }
  return rows;
}
function matrices(z){
  const L=Array.from({length:24},()=>Array(24).fill(0));
  const B=Array.from({length:24},()=>Array(16).fill(0));
  const C=Array.from({length:16},()=>Array(24).fill(0));
  for(let j=0;j<24;j++){
    const out=linkLinear(z,Math.floor(j/6),j%6);
    for(let i=0;i<24;i++)L[i][j]=out[i];
  }
  for(let idir=0;idir<4;idir++)for(let j=0;j<6;j++){
    const row=6*idir+j,X=gens[j];
    for(let [r,t] of ids){
      if(idir!==r&&idir!==t)continue;
      const other=idir===r?t:r,[u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t);
      const sg=eps(r,t,u,v)*(idir===r?1:-1)*(1-1/z[other]);
      for(let a=0;a<4;a++)for(let mu=0;mu<4;mu++)
        B[row][4*a+mu]+=sg*pairDeriv(a,mu,u,v,X);
    }
  }
  for(let [r,t] of ids){
    const [u,v]=[0,1,2,3].filter(k=>k!==r&&k!==t);
    const sg=eps(r,t,u,v);
    for(let idir of [r,t])for(let j=0;j<6;j++){
      const R=sc(gens[j],idir===r?1-z[t]:z[r]-1),col=6*idir+j;
      for(let a=0;a<4;a++)for(let mu=0;mu<4;mu++)
        C[4*a+mu][col]+=sg*pairDeriv(a,mu,u,v,R);
    }
  }
  return {L,B,C};
}
function rank(M,tol=1e-10){
  const A=M.map(r=>r.slice()),N=A.length,K=A[0].length;
  const max=Math.max(...A.flat().map(Math.abs));if(!max)return 0;
  let p=0;for(let j=0;j<K&&p<N;j++){
    let best=p;for(let i=p+1;i<N;i++)if(Math.abs(A[i][j])>Math.abs(A[best][j]))best=i;
    if(Math.abs(A[best][j])<=tol*max)continue;
    [A[best],A[p]]=[A[p],A[best]];
    for(let i=p+1;i<N;i++){let q=A[i][j]/A[p][j];
      for(let k=j;k<K;k++)A[i][k]-=q*A[p][k];}
    p++;
  }
  return p;
}
function solveMultiple(L,Y){
  const n=L.length,k=Y[0].length,A=L.map((r,i)=>[...r,...Y[i]]);
  for(let c=0;c<n;c++){
    let p=c;for(let r=c+1;r<n;r++)if(Math.abs(A[r][c])>Math.abs(A[p][c]))p=r;
    if(Math.abs(A[p][c])<1e-12)throw Error("near singular "+c);
    [A[p],A[c]]=[A[c],A[p]];
    const t=A[c][c];for(let j=c;j<n+k;j++)A[c][j]/=t;
    for(let r=0;r<n;r++)if(r!==c){const f=A[r][c];
      for(let j=c;j<n+k;j++)A[r][j]-=f*A[c][j];}
  }
  return A.map(row=>row.slice(n));
}
function symbol(z){
  const {L,B,C}=matrices(z),X=solveMultiple(L,B);
  const Schur=C.map(row=>B[0].map((_,j)=>
    -row.reduce((sum,v,k)=>sum+v*X[k][j],0)));
  return {L,B,C,Schur};
}
const mv=(M,v)=>M.map(row=>row.reduce((s,x,i)=>s+x*v[i],0));
const maxAbs=A=>Math.max(...A.flat(Infinity).map(Math.abs));
function audit(){
  const zs=[[1.1,1.07,1.05,1.04],[1,1,1.02,1.03],
    [1.12,.94,1,1],[1.001,1.003,1.002,1.004],
    [1.05,1.05,1.05,1.05]];
  return zs.map(z=>{
    const v=symbol(z),back=symbol(z.map(t=>1/t)),S=v.Schur;
    const adjoint=maxAbs(S.map((row,i)=>row.map((x,j)=>x-back.Schur[j][i])));
    const lorentz=gens.map(G=>maxAbs(mv(S,G.flat())));
    const gradients={};
    for(let type of ["forward","backward","log"]){
      const k=z.map(q=>type==="forward"?q-1:
        type==="backward"?1-1/q:Math.log(q));
      const normals=Array.from({length:4},(_,a)=>
        Array.from({length:16},(_,i)=>+(Math.floor(i/4)===a)*k[i%4]));
      gradients[type]=Math.max(...normals.map(v=>maxAbs(mv(S,v))));
    }
    const Bgrad=Array.from({length:4},(_,a)=>Array.from({length:16},(_,i)=>
      +(Math.floor(i/4)===a)*(1-1/z[i%4])));
    return {z,link_rank:rank(v.L),
      fullSchurRank:rank(S,1e-10),rank_tol1e8:rank(S,1e-8),
      Schur_max:maxAbs(S),Laurent_adjoint_error:adjoint,
      maxLorentzWard:Math.max(...lorentz),
      gradients,
      B_backward_gauge_max:Math.max(...Bgrad.map(w=>maxAbs(mv(v.B,w))))};
  });
}


/* Exact closed TT null-wave connection for z=(t,1,1,1).
 * In the original generator ordering (01,02,03,12,13,23),
 * generators #3=-N2 and #4=-N3. The true independent linear
 * coframe and link equations are L(t)w+B(t)e=0, C(t)w=0.
 *
 * L(t) has Laurent degree -1,0,+1, B(t)e=(1-t^-1)b0,
 * and C(t)=(t-1)C1 on this axis. Thus checking
 * L(t)w0+b0 at t=1,2,4 is an EXACT Laurent interpolation proof,
 * not an extrapolation to other grid wavelengths. These 3
 * samples and all operations are integer/binary dyadic, exact in
 * IEEE-754 due the bounded integer coefficients.
 */
function exactTwoNullTT(){
  let checks=[];
  for(let role of [0,1])for(let type of ["plus","cross"]){
    const e=Array(16).fill(0),w0=Array(24).fill(0);
    const gen2=role===0?3:1,gen3=role===0?4:2;
    if(type==="plus"){
      e[10]=1;e[15]=-1;
      // w_x=+D_role^- N2 (or opposite M2), w_y=-D_role^- N3
      w0[12+gen2]=-1;w0[18+gen3]=1;
    }else{
      e[11]=1;e[14]=1;
      // w_x=+D_role^- N3, w_y=+D_role^- N2
      w0[12+gen3]=-1;w0[18+gen2]=-1;
    }
    const coord=t=>role===0?[t,1,1,1]:[1,t,1,1];
    const B2=matrices(coord(2)).B,
      b0=mv(B2,e).map(x=>2*x);
    for(let t of [1,2,4,8]){
      const {L,B,C}=matrices(coord(t));
      const linked=mv(L,w0).map((v,i)=>v+b0[i]);
      const scale=mv(B,e).map((v,i)=>v-(1-1/t)*b0[i]);
      const solder=mv(C,w0);
      if(maxAbs(linked)!==0 || maxAbs(scale)!==0 ||
         maxAbs(solder)!==0)
        throw Error("exact one-null TT failed "+role+"/"+type+" t="+t);
      checks.push({role:role===0?"u":"v",type,t,link_identity:true,coframe_identity:true});
    }
  }
  return {
    status:"PASS_EXACT_ALL_T_TT_LINEARIZED_40_EULER",
    role_wave:"(t,1,1,1) OR (1,t,1,1) with arbitrary nonzero t",
    plus:"delta e^2_x=f, delta e^3_y=-f; omega_x=D_u^- f N2, omega_y=-D_u^- f N3",
    cross:"delta e^2_y=delta e^3_x=f; omega_x=D_role^- f N3, omega_y=D_role^- f N2",
    opposite_v:"replace u→v, N_i→barN_i (all other TT entries unchanged)",
    algebraic_proof:"Laurent degree [-1,1] for L(t); three dyadic exact values fix each coefficient; C(t)=(t-1)C1",
    samples:checks,
    scope:"linearized vacuum all40 on original star carrier, not finite-amplitude nonlinear wave or compulsory native history"
  };
}

module.exports={audit,symbol,matrices,rank,exactTwoNullTT};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
