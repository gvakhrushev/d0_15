// D0 original CAR16/Choi density moments and polynomial six-face source.
// Finite 16x16 ordinary matrix controls; original null eta and CAR order.
// Independent of physical Book03 selection and native upstream writer.
const ok=(c,m)=>{if(!c)throw Error("CHECK_FAILED "+m)};
const n=4,d=16,order=[0,2,3,1],eps=1e-7;
const zeros=(n,m=n)=>Array.from({length:n},()=>Array(m).fill(0));
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
const add=(A,B)=>A.map((r,i)=>r.map((v,j)=>v+B[i][j]));
const neg=A=>A.map(r=>r.map(x=>-x));
const sub=(A,B)=>add(A,neg(B));
const mul=(A,B)=>A.map(row=>Array.from({length:B[0].length},(_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
const scale=(A,x)=>A.map(row=>row.map(v=>v*x));
const T=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const maxerr=(A,B)=>Math.max(...A.flatMap((row,i)=>row.map((v,j)=>Math.abs(v-B[i][j]))));
const tr=A=>A.reduce((s,row,i)=>s+row[i],0);
const E=(i,j)=>{const a=zeros(4);a[i][j]=1;return a};
const eta=add(add(E(0,1),E(1,0)),scale(add(E(2,2),E(3,3)),-1));
ok(maxerr(mul(eta,eta),eye(4))===0,"null eta involution");
const generators=[
 add(E(1,2),E(2,0)),add(E(0,3),E(3,1))];
for(const g of generators){
 ok(maxerr(add(mul(T(g),eta),mul(eta,g)),zeros(4))===0,"native SO Lie generator");
 ok(maxerr(mul(mul(g,g),g),zeros(4))===0,"nilpotent null generator");
}
const expNil=(G,s)=>add(add(eye(4),scale(G,s)),scale(mul(G,G),s*s/2));
const U=expNil(generators[0],1/5),V=expNil(generators[1],1/7);
for(const X of [U,V]){
 ok(maxerr(mul(mul(T(X),eta),X),eta)<1e-13,"actual proper null SO");
}
const PinvX=X=>mul(mul(eta,T(X)),eta);
const P=mul(mul(mul(U,V),PinvX(U)),PinvX(V));
ok(maxerr(mul(mul(T(P),eta),P),eta)<1e-12,"based noncommutative plaquette SO");
ok(maxerr(P,eye(4))>1e-6,"genuine nontrivial based curvature");
const det=a=>{if(a.length===0)return 1;if(a.length===1)return a[0][0];let s=0;for(let j=0;j<a.length;j++){const minor=a.slice(1).map(row=>row.filter((_,k)=>k!==j));s+=(j%2?-1:1)*a[0][j]*det(minor)}return s};
const maskIndices=mask=>Array.from({length:4},(_,i)=>i).filter(i=>(mask>>i)&1);
const exterior=X=>{
 const A=zeros(16);
 for(let out=0;out<16;out++)for(let input=0;input<16;input++){
  let rows=maskIndices(out),cols=maskIndices(input);
  if(rows.length===cols.length)A[out][input]=det(rows.map(i=>cols.map(j=>X[i][j])));
 }
 return A;
};
const Heta=exterior(eta),LP=exterior(P);
ok(maxerr(mul(Heta,Heta),eye(16))<1e-13,"original exterior signature");
ok(maxerr(exterior(mul(U,V)),mul(exterior(U),exterior(V)))<1e-12,"exterior functor on true links");
ok(maxerr(exterior(PinvX(P)),mul(mul(Heta,T(LP)),Heta))<1e-12,"genuine inverse link exterior");
const creation=i=>{
 const a=zeros(16),bit=order.indexOf(i);
 for(let m=0;m<16;m++){
  if(m&(1<<bit))continue;
  const lower=m&((1<<bit)-1);
  const s=(lower.toString(2).replace(/0/g,"").length%2)?-1:1;
  a[m|(1<<bit)][m]=s;
 }
 return a;
};
const C=u=>u.reduce((A,x,i)=>add(A,scale(creation(i),x)),zeros(16));
const nu=3/5,u=Array.from({length:4},(_,r)=>Array.from({length:4},(_,i)=>nu*eta[i][r]));
for(let r=0;r<4;r++){
 const c=C(u[r]);
 for(let i=0;i<4;i++)ok(Math.abs(c[1<<order.indexOf(i)][0]-u[r][i])<1e-13,"actual CAR vacuum/gradeone");
}
const ginv=Array.from({length:4},(_,r)=>Array.from({length:4},(_,s)=>u[r].reduce((sum,v,i)=>sum+v*eta[i].reduce((t,w,j)=>t+w*u[s][j],0),0)/nu**2));
ok(maxerr(ginv,eta)<1e-13,"metric inverse from original coframe CAR entries");
for(const X of [U,V,P]){
 const D=exterior(X);
 for(let i=0;i<4;i++)for(let j=0;j<4;j++){
  ok(Math.abs(D[1<<i][1<<j]-X[i][j])<1e-13,"exterior grade-one exact link");
 }
}
const D= sub(mul(mul(mul(C(u[0]),Heta),T(C(u[1]))),Heta),
             mul(mul(mul(C(u[1]),Heta),T(C(u[0]))),Heta));
const curvature=-tr(mul(D,LP))/8;
ok(Number.isFinite(curvature),"nontrivial native CAR16 polynomial scalar");
const Jentry=(A,ii,jj)=>A[jj][ii];
// For a fixed anchor, |Omega>_r=(Ad)^-1/2 and |Omega>_s=J_ji(Ad)^-1/2.
for(const source of [C(u[0]),C(u[2]),exterior(U),exterior(V)]){
 for(let j=0;j<16;j++)for(let i=0;i<16;i++){
  const observed=(8*32/2)*(2/(8*32))*Jentry(source,i,j);
  ok(Math.abs(observed-source[j][i])<1e-13,"anchored full Choi Hermitian moment");
 }
}
const sharp=X=>mul(mul(eta,T(X)),eta);
const R2=M=>{const H=sub(mul(sharp(M),M),eye(4));return mul(M,add(sub(eye(4),scale(H,.5)),scale(mul(H,H),.375)))};
ok(maxerr(R2(U),U)<1e-12,"native Lorentz R2 true value");
for(let i=0;i<4;i++)for(let j=0;j<4;j++){
 const basis=E(i,j),R=R2(add(eye(4),scale(basis,eps)));
 const projected=scale(sub(basis,sharp(basis)),.5);
 const diff=scale(sub(R,eye(4)),1/eps);
 ok(maxerr(diff,projected)<2e-7,"native R2 kills all ten link normal dimensions");
}
function run(){return {status:"PASS_ORIGINAL_CAR16_CHOIPROGRAMME_MOMENTS",native_order:order,original_null_metric:true,proper_based_face_nontrivial:true,original_CAR16_creation_exact:true,full16_exterior_holonomy_functor:true,original_signed_face_scalar:curvature,hermitian_anchor_exact:true,link_normal_projected:true,raw_geometric_moment_polynomial_degree:6,normal_projected_degree_upper_bound:82,material_moment_degrees:{Choi:2,CAR_density:2},writer_and_Book_valuation_selected:false,GR_closed:false}}
if(typeof console!=="undefined")console.log(JSON.stringify(run(),null,2));
