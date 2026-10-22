// Exact coherent Golden/CNOT and combinatorial-scene consumer. No dependencies.

function runChecks() {
  const Z=()=>[0n,0n,0n,0n], one=[1n,0n,0n,0n], a=[0n,1n,0n,0n];
  const add=(x,y)=>x.map((v,i)=>v+y[i]);
  const neg=x=>x.map(v=>-v);
  const sub=(x,y)=>add(x,neg(y));
  const mul=(x,y)=>{
    const c=Array(7).fill(0n);
    for(let i=0;i<4;i++) for(let j=0;j<4;j++) c[i+j]+=x[i]*y[j];
    for(let k=6;k>=4;k--){c[k-4]+=c[k];c[k-2]-=c[k];}
    return c.slice(0,4);
  };
  const sc=(k,x)=>x.map(v=>BigInt(k)*v);
  const pow=(x,n)=>{let y=one;while(n){if(n%2)y=mul(y,x);x=mul(x,x);n=Math.floor(n/2);}return y;};
  const eq=(x,y)=>x.every((v,i)=>v===y[i]);
  const is0=x=>eq(x,Z());
  const val=x=>x.reduce((s,c,i)=>s+Number(c)*Math.pow(Math.sqrt((Math.sqrt(5)-1)/2),i),0);
  const fmt=x=>x.map(v=>v.toString());
  let count=0;const names=[];
  function ck(b,n){if(!b)throw new Error(n);count++;names.push(n);}
  const p=mul(a,a), p2=mul(p,p);
  ck(eq(add(p,p2),one),"Golden defining polynomial");
  const G=[[a,neg(p)],[p,a]], Gi=[[a,p],[neg(p),a]], X=[[Z(),one],[one,Z()]];
  const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((v,x,k)=>add(v,mul(x,B[k][j])),Z())));
  const me=(A,B)=>A.length===B.length&&A.every((row,i)=>row.every((x,j)=>eq(x,B[i][j])));
  const I=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?one:Z()));
  ck(me(mm(Gi,G),I(2)),"Golden orthogonality");
  ck(me(mm(mm(X,G),X),Gi),"native X G X inverse");
  function empty(n){return Array.from({length:1<<n},Z);}
  function g(v,t,inverse=false){
    const out=v.map(x=>x.slice()),bit=1<<t,M=inverse?Gi:G;
    for(let i=0;i<v.length;i++)if(!(i&bit)){
      out[i]=add(mul(M[0][0],v[i]),mul(M[0][1],v[i|bit]));
      out[i|bit]=add(mul(M[1][0],v[i]),mul(M[1][1],v[i|bit]));
    }return out;
  }
  function cx(v,c,t){const out=empty(Math.log2(v.length));for(let i=0;i<v.length;i++)out[(i&(1<<c))?i^(1<<t):i]=v[i];return out;}
  const invWord=w=>w.slice().reverse().map(l=>l[0]==="g"?["g",l[1],!l[2]]:l);
  function wControlled(controls,t){
    if(!controls.length)return [["g",t,false]];
    const c=controls[controls.length-1],w=wControlled(controls.slice(0,-1),t);
    return [["cx",c,t],...invWord(w),["cx",c,t],...w];
  }
  function phaseWord(controls,t){
    const k=controls.length;return [...Array.from({length:2**(k-1)},()=>["g",t,true]),...wControlled(controls,t)];
  }
  function apply(v,word){for(const l of word)v=l[0]==="g"?g(v,l[1],l[2]):cx(v,l[1],l[2]);return v;}
  for(const k of [1,2,3]){
    const dim=1<<k,mat=Array.from({length:dim},()=>Array.from({length:dim},Z));
    for(let input=0;input<dim;input++){
      let v=empty(k+1);v[input]=one;v=apply(v,phaseWord(Array.from({length:k},(_,i)=>i),k));
      for(let output=0;output<dim;output++)mat[output][input]=v[output|(1<<k)];
      const norm=v.reduce((s,x)=>add(s,mul(x,x)),Z());
      ck(eq(norm,one),"controlled phase full column norm k="+k+" input="+input);
    }
    const coeff=k===1?neg(p):k===2?sc(-2,pow(a,3)):sc(-4,pow(a,9));
    const target=I(dim).map((r,i)=>r.map((x,j)=>mul(x,i===dim-1?neg(coeff):coeff)));
    ck(me(mat,target),"literal controlled phase corner k="+k);
  }
  {
    let v=empty(2);v[0]=one;v=g(g(v,0),1);v=cx(v,0,1);
    ck(eq(v[2],pow(a,3))&&eq(v[3],pow(a,3)),"literal plus-resource corner");
  }
  const Hcorner=Array.from({length:2},()=>Array.from({length:2},Z));
  for(let input=0;input<2;input++){
    let v=empty(6);v[input]=one;
    const word=[
      ["g",1,false],["g",2,false],["cx",1,2],
      ...phaseWord([0,1],3),
      ["g",4,false],["cx",4,0],["g",4,false],
      ["g",5,false],["cx",5,0],["g",5,true],
      ["cx",0,1],["cx",1,0],["cx",0,1]
    ];
    v=apply(v,word);
    const work=(1<<2)|(1<<3)|(1<<4);
    for(let out=0;out<2;out++)Hcorner[out][input]=v[work|out];
    ck(eq(v.reduce((s,x)=>add(s,mul(x,x)),Z()),one),"literal H all-work column norm "+input);
  }
  const hscale=sc(-2,pow(a,9)),J=[[one,one],[one,neg(one)]];
  ck(me(Hcorner,J.map(r=>r.map(x=>mul(hscale,x)))),"literal fixed-schedule H corner");
  const H3=Array.from({length:8},(_,i)=>Array.from({length:8},(_,j)=>(i>>1)===(j>>1)?Hcorner[i&1][j&1]:Z()));
  const CCZ=I(8).map((r,i)=>r.map(x=>mul(x,sc(i===7?4:-4,pow(a,9)))));
  const Tcorner=mm(mm(H3,CCZ),H3),T=Array.from({length:8},()=>Array.from({length:8},Z));
  for(let i=0;i<8;i++)T[(i&6)===6?i^1:i][i]=one;
  const tscale=sc(-32,pow(a,27));
  ck(me(Tcorner,T.map(r=>r.map(x=>mul(tscale,x)))),"fresh-work composed exact Toffoli corner");
  const gammaT2=sc(1024,pow(p,27));
  ck(eq(mul(tscale,tscale),gammaT2),"exact Toffoli success effect");
  const sizes=[9,11,13],part=[];
  sizes.forEach((n,j)=>{for(let i=0;i<n;i++)part.push(j);});
  const N=33,L=Array.from({length:N},()=>Array(N).fill(0n)), edges=[];
  for(let u=0;u<N;u++)for(let v=u+1;v<N;v++)if(part[u]!==part[v]){
    edges.push([u,v]);L[u][u]++;L[v][v]++;L[u][v]--;L[v][u]--;
  }
  ck(edges.length===359,"actual K913 edge census");
  ck(L.every(row=>row.reduce((s,x)=>s+x,0n)===0n),"scene constant null vector");
  const im=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?1n:0n));
  const zm=()=>Array.from({length:N},()=>Array(N).fill(0n));
  const imul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0n)));
  let annih=im(N);
  for(const l of [0n,20n,22n,24n,33n])annih=imul(annih,L.map((r,i)=>r.map((x,j)=>x-(i===j?l:0n))));
  ck(annih.every(r=>r.every(x=>x===0n)),"exact scene annihilating polynomial");
  const spectrum=[[0n,1],[20n,12],[22n,10],[24n,8],[33n,2]];
  let LP=im(N);
  for(let k=0;k<5;k++){
    const tr=LP.reduce((s,r,i)=>s+r[i],0n),expect=spectrum.reduce((s,[l,m])=>s+BigInt(m)*(k===0?1n:l**BigInt(k)),0n);
    ck(tr===expect,"scene spectral multiplicity trace moment "+k);LP=imul(LP,L);
  }
  let balanced=0;
  for(let w=0;w<4096;w++){let b=w,n=0;while(b){n+=b&1;b>>=1;}if(n===6)balanced++;}
  ck(balanced===924&&balanced>=2*edges.length,"Golden equal-weight address capacity");
  ck(eq(pow(p,18),sub(sc(1597,one),sc(2584,p))),"exact Golden scene address coefficient");
  const pairs=2*edges.length,terms=zm();
  for(const [u,v] of edges){terms[u][u]++;terms[v][v]++;terms[u][v]--;terms[v][u]--;}
  ck(terms.every((r,i)=>r.every((x,j)=>x===L[i][j])),"signed transposition scene decomposition");
  const pv=(Math.sqrt(5)-1)/2;
  return {
    status:"PASS",arithmetic:"Z[a]/(a^4+a^2-1), exact BigInt; scene integer matrices",
    assertions:count,checks:names,
    exact:{H_corner_scale_on_integer_Hadamard:fmt(hscale),Toffoli_corner_scale:fmt(tscale),Toffoli_corner_probability:fmt(gammaT2),scene_weight:fmt(pow(p,18))},
    diagnostic_only:{Toffoli_success_probability:1024*pv**27,scene_weight:pv**18,scene_blank_norm:33*pv**18,signed_terms:pairs,balanced_addresses:balanced},
    scope:{actual_original_scene:"combinatorial K(9,11,13), embedded with 95 zeros in DATA128",moving_field_writer:false,default_normalized_scene_hodge_identified:false,complete_physical_price_selected:false,GR_closed:false}
  };
}

console.log(JSON.stringify(runChecks(), null, 2));
