// Original CAR constructor blob ee8de4635d24c668949ac9a0186616ab7d59f2ed.
// Exact witness: separately paid Choi16, not a full-rank RIGHT128 preparation.

function exactNativeChoiCNOTSource() {
 const d=16,Z=()=>Array.from({length:d*d},()=>[0n,0n]),I=Z();for(let j=0;j<d;j++)I[j*d+j]=[1n,0n];
 const add=(a,b,s=1n)=>a.map((z,k)=>[z[0]+s*b[k][0],z[1]+s*b[k][1]]);
 const scale=(a,c)=>a.map(z=>[z[0]*c,z[1]*c]);
 const ii=a=>a.map(z=>[-z[1],z[0]]);
 const adj=a=>a.map((_,k)=>[a[(k%d)*d+Math.floor(k/d)][0],-a[(k%d)*d+Math.floor(k/d)][1]]);
 const mul=(a,b)=>{const c=Z();for(let r=0;r<d;r++)for(let k=0;k<d;k++){const x=a[r*d+k];if(x[0]===0n&&x[1]===0n)continue;for(let s=0;s<d;s++){const y=b[k*d+s],z=c[r*d+s];z[0]+=x[0]*y[0]-x[1]*y[1];z[1]+=x[0]*y[1]+x[1]*y[0];}}return c;};
 const tr=a=>{let re=0n,im=0n;for(let j=0;j<d;j++){re+=a[j*d+j][0];im+=a[j*d+j][1];}if(im!==0n)throw Error("nonreal trace");return re;};
 const eq=(a,b)=>a.every((x,k)=>x[0]===b[k][0]&&x[1]===b[k][1]);
 let checks=0;const names=[];const ck=(b,n)=>{if(!b)throw Error(n);checks++;names.push(n);};
 const order=[0,2,3,1],cs=Array.from({length:4},(_,r)=>{const c=Z();for(let b=0;b<d;b++)if(!(b&(1<<r))){const parity=order.slice(0,order.indexOf(r)).reduce((s,j)=>s+((b>>j)&1),0)%2;c[(b|(1<<r))*d+b]=[parity?-1n:1n,0n];}return c;});
 for(let r=0;r<4;r++)for(let s=0;s<4;s++){
   ck(eq(add(mul(cs[r],cs[s]),mul(cs[s],cs[r])),Z()),"CAR creation anticommutator "+r+","+s);
   ck(eq(add(mul(cs[r],adj(cs[s])),mul(adj(cs[s]),cs[r])),r===s?I:Z()),"CAR mixed anticommutator "+r+","+s);
 }
 const G=add(mul(cs[0],adj(cs[1])),mul(cs[1],adj(cs[0]))),P=mul(G,G);
 ck(eq(mul(P,P),P)&&eq(adj(G),G),"boost projector and Hermiticity");
 const Uint=add(add(scale(I,40n),P),scale(G,9n)),UGint=add(scale(G,41n),scale(P,9n));
 ck(eq(mul(Uint,G),UGint),"literal proper boost derivative at exp(theta)=5/4");
 let H=Z();
 for(let r=0;r<4;r++){
   let xu=mul(cs[r],r===1?Uint:scale(I,40n));
   xu=r===2?scale(xu,-1n):scale(ii(xu),r===3?-1n:1n);
   H=add(H,add(add(xu,adj(xu)),scale(add(cs[r],adj(cs[r])),-40n)));
 }
 const D=add(ii(mul(cs[1],UGint)),scale(ii(mul(UGint,adj(cs[1]))),-1n));
 ck(eq(H,adj(H))&&eq(D,adj(D)),"original blank and its exact jet Hermitian");
 const H2=mul(H,H),H3=mul(H2,H),dH2=add(mul(H,D),mul(D,H));
 const c1=cs[1],c1d=adj(c1),Nvac=mul(c1d,c1);
 const Sint=add(add(mul(mul(c1,mul(Uint,Uint)),c1d),mul(mul(Uint,Nvac),Uint)),scale(I,-1600n));
 const dSint=add(mul(mul(c1,add(mul(UGint,Uint),mul(Uint,UGint))),c1d),add(mul(mul(UGint,Nvac),Uint),mul(mul(Uint,Nvac),UGint)));
 const traces={TrH2:tr(H2),TrHD:tr(mul(H,D)),TrH3D:tr(mul(H3,D)),TrH2S:tr(mul(H2,Sint)),TrdH2S:tr(mul(dH2,Sint)),TrH2dS:tr(mul(H2,dSint))};
 const expected={TrH2:251536n,TrHD:-7216n,TrH3D:-98629472n,TrH2S:21164832n,TrdH2S:2385216n,TrH2dS:188623936n};
 for(const k of Object.keys(traces))ck(traces[k]===expected[k],"literal trace "+k);
 const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
 const fr=(a,b)=>{const g=gcd(a,b);return[a/g,b/g];};
 const fm=(a,b)=>fr(a[0]*b[0],a[1]*b[1]),fa=(a,b)=>fr(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const mu=fr(9n*traces.TrH2,3200n**2n*16n),dmu=fr(18n*traces.TrHD,3200n**2n*16n),dm2=fr(324n*traces.TrH3D,3200n**4n*16n);
 const M=fr(9n*traces.TrH2S,3200n**2n*1600n*16n),dM=fr(9n*(traces.TrdH2S+traces.TrH2dS),3200n**2n*1600n*16n);
 const gap=fm([4n,1n],fa(fm([41n,50n],mu),fm([-9n,400n],M)));
 const dgap=fm([4n,1n],fa(fm([41n,50n],dmu),fm([-9n,400n],dM)));
 const allgap=fm([4n,1n],fa(dmu,[-dm2[0],dm2[1]]));
 ck(gap[0]===37073140119n&&gap[1]===819200000000n,"strict same-Choi single-CNOT price difference");
 ck(dgap[0]===-653413779n&&dgap[1]===204800000000n,"strict same-Choi single-CNOT source difference");
 ck(allgap[0]===-10141384149n&&allgap[1]===3276800000000n,"all-nonblank independent trace crosscheck");
 const fmt=x=>x.map(String).join("/");
 return {status:"PASS",arithmetic:"exact Gaussian BigInt matrices and rational BigInt fractions",assertions:checks,checks:names,
 fixture:{theta:"log(5/4)",r:"1/9",nu:"3/5",CAROrder:order,phases:["i","i","-1","-i"],CNOT:"alpha bit1 -> alpha bit0",DATA_marginal:"I16/16; no inverse-square substitution"},
 traces:Object.fromEntries(Object.entries(traces).map(([k,v])=>[k,String(v)])),
 mu:fmt(mu),dmu:fmt(dmu),dm2:fmt(dm2),M:fmt(M),dM:fmt(dM),
 singleCNOTGapCoefficientOfP5:fmt(gap),singleCNOTSourceCoefficientOfP5:fmt(dgap),allNonblankSourceCoefficientOfP5:fmt(allgap),
 scope:{proofConsumesAnalyticWalshIdentity:true,full128NumericalReplayClaimed:false,independent42FieldMap:false,GR_closed:false}};
}

console.log(JSON.stringify(exactNativeChoiCNOTSource(), null, 2));
