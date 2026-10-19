#!/usr/bin/env node
"use strict";
/**
 * Original D0 GoldenOrderInterferometer.gate / GoldenCoherentMemory.fullStep
 * plus ORIGINAL binary CNOT: integer Lie-algebra SPAN certificate.
 *
 * The exact mathematical theorem:
 *   p=(sqrt(5)-1)/2, a=sqrt(p), G=[[a,-p],[p,a]];
 *   fullStep = CNOT_(system->fresh) (G \otimes I_fresh).
 *   theta/pi is irrational because t=2cos(2theta)=2sqrt(5)-4
 *   has conjugate -2sqrt(5)-4 outside [-2,2], impossible for an
 *   algebraic conjugate of ζ+ζ^-1 if ζ is a root of unity.
 *   Thus <G> dense in SO(2).
 *
 * Exact CNOT conjugation on binary Pauli labels:
 *   (x,z) -> (Ax,A^(-T)z), x_target ^= x_control,
 *   z_control ^= z_target.
 * Its orbit on Y_i=(e_i,e_i) is precisely all x.z=1 over F2.
 * These W_(x,z)=X^x Z^z form a REAL skew-orthogonal basis of
 * so(2^n); number (4^n-2^n)/2.
 * Consequently G_i and connected reversible CNOTs have closure
 * SO(2^n), n>=3 (n=2 closure O(4) with SO(4) component).
 *
 * ONLY a mathematical gate-SPAN theorem, conditional on applying the
 * original primitives to ANY required still-ACTIVE wires (or routing
 * them through allowed active SWAP). Does NOT establish literal G0
 * gate placement, run length, compiler work, actual fullStep cut,
 * field-dependent first source, proper-Lorentz boosts as orthogonal
 * physical matrices, oldRIGHT-controlled routing, Book selection,
 * exact finite words for generic smooth input, or GR.
 */
const require=(ok,message)=>{if(!ok)throw Error(message)};
const parity=n=>{let r=0;while(n){r^=n&1;n>>=1}return r};
const popcnt=n=>{let r=0;while(n){r+=n&1;n>>=1}return r};

function cnotPauli(x,z,control,target){
  return [
    x^(((x>>control)&1)<<target),
    z^(((z>>target)&1)<<control)
  ];
}
function pauliOrbit(n){
  const mask=(1<<n)-1;
  const originals=Array.from({length:n},(_,i)=>(1<<i)|((1<<i)<<n));
  const seen=new Set(originals),queue=[...originals];
  for(let cursor=0;cursor<queue.length;cursor++){
    const label=queue[cursor],x=label&mask,z=label>>n;
    for(let c=0;c<n;c++)for(let t=0;t<n;t++){
      if(c===t)continue;
      const [xx,zz]=cnotPauli(x,z,c,t),next=xx|(zz<<n);
      if(!seen.has(next)){seen.add(next);queue.push(next)}
    }
  }
  return {labels:[...seen],size:seen.size,mask};
}
const mm=(A,B)=>A.map(r=>B[0].map((_,j)=>
  r.reduce((v,x,k)=>v+x*B[k][j],0)));
const maxDiff=(A,B)=>Math.max(...A.flatMap((row,i)=>
  row.map((v,j)=>Math.abs(v-B[i][j]))));

function check(){
  const p=(Math.sqrt(5)-1)/2,a=Math.sqrt(p);
  require(Math.abs(p+p*p-1)<1e-14,"not original golden value");
  const gate=[[a,-p],[p,a]];
  const full=[[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]];
  const GxI=[[a,0,-p,0],[0,a,0,-p],[p,0,a,0],[0,p,0,a]];
  const CNOT=[[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]];
  const signedFullError=maxDiff(mm(CNOT,GxI),full);
  const Id2=[[1,0],[0,1]];
  const transpose=M=>M[0].map((_,i)=>M.map(row=>row[i]));
  require(signedFullError===0,"GoldenCoherentMemory.fullStep != CNOT*(G tensor I)");
  require(maxDiff(mm(transpose(gate),gate),Id2)<1e-14,"original golden gate nonorthogonal");
  const t=2*(p-p*p);
  require(Math.abs(t-(2*Math.sqrt(5)-4))<1e-14,"golden double-angle identity");
  // Conjugate of root of quadratic X^2+8X-4; violates all-root-unity
  // conjugates-in-[-2,2] necessary bound.
  const other=-4-2*Math.sqrt(5);
  require(Math.abs(t*t+8*t-4)<1e-13&&other< -2,
    "irrational-angle cyclotomic conjugate witness failed");

  const orbits=[];
  for(let n=1;n<=7;n++){
    const orbit=pauliOrbit(n),mask=orbit.mask,expected=(4**n-2**n)/2;
    require(orbit.size===expected,"CNOT orbit not full so at n="+n);
    for(let id of orbit.labels){
      const x=id&mask,z=id>>n;
      require(x!==0&&z!==0&&parity(x&z)===1,
        "non-skew Pauli in CNOT orbit at n="+n);
      // W^T=(-1)^(x.z)W; all have an odd number of real XZ factors.
    }
    // The whole skew-Pauli basis is orthogonal because
    // Tr(W_a^T W_b)=2^n delta_(a,b).
    orbits.push({activeQubits:n,matrixDimension:2**n,
      cnotOrbit:orbit.size,dimensionSO:expected,exactFullSpan:true});
  }

  // An actual complete CAR16 + fresh flag uses five active bits.
  // The flat Julia block is the direct sum of 16 original GOLDEN
  // complete qubit effects p*I and sqrt(p)*I; as a 32x32 real
  // block operator its 2x2 per-CAR-basis block has determinant -1.
  // Product over 16 CAR basis states has determinant (-1)^16=+1.
  const juliaFlat2=[[p,a],[a,-p]],
        det2=juliaFlat2[0][0]*juliaFlat2[1][1]
             -juliaFlat2[0][1]*juliaFlat2[1][0];
  require(Math.abs(det2+1)<1e-14,"Golden flat Julia 2x2 incorrect");
  require(Math.abs(mm(transpose(juliaFlat2),juliaFlat2)[0][0]-1)<1e-14,
    "Golden flat Julia non-orthogonal");
  // Along any t in [0,1] for strict real 16x16 contraction C,
  // the standard Julia block J_(tC) continuously lies in O(32).
  // Its determinant is constant and equals det J_0=(-1)^16=1.

  // Strong independent n=5 check: ALL 496 real skew Pauli labels have
  // mutually orthogonal 32x32 actions, using signed basis permutations.
  const n=5,{labels,mask}=pauliOrbit(n),N=2**n;
  function frob(a,b){
    const x=a&mask,z=a>>n,X=b&mask,Z=b>>n;
    if(x!==X)return 0;
    let result=0;
    for(let basis=0;basis<N;basis++){
      const signA=parity(z&basis)?-1:1,
            signB=parity(Z&basis)?-1:1;
      result+=signA*signB;
    }
    return result;
  }
  let nonorthogonal=0;
  for(let i=0;i<labels.length;i++){
    require(frob(labels[i],labels[i])===N,"wrong Pauli normalization");
    for(let j=0;j<i;j++)if(frob(labels[i],labels[j])!==0)nonorthogonal++;
  }
  require(nonorthogonal===0,"skew Pauli basis not orthogonal");

  return {
    status:"PASS_ORIGINAL_GOLDEN_CNOT_DENSE_ACTIVE_SO",
    exactFullStepFactorization:true,
    fullStepFactorizationError:signedFullError,
    goldenValue:p,goldenTheta:Math.atan2(p,a),
    irrationalAngleProof:"2cos(2theta)=2sqrt(5)-4 has conjugate -2sqrt(5)-4<-2, impossible for root-of-unity sum",
    CNOT_action:"x_t ^= x_c; z_c ^= z_t",
    orbitRanks:orbits,
    fullCAR16PlusFreshFlag:{activeBits:5,realDimension:32,SO_dimension:496,
      all496SkewPauliOrthogonal:true,flatGoldenJuliaIsSO32:true},
    result:"Closure of original Golden_i and arbitrarily routed ACTIVE CNOT_ij contains SO(2^n) for all n>=1; n>=3 exact closure is SO(2^n)",
    action_scope:"Dense OPERATOR pointwise only; not exact arbitrary field-dependent finite gate, no uniform cost/C1 source and no oldRIGHT→active control",
    native_selected:false,
    GR_closed:false
  };
}
console.log(JSON.stringify(check(),null,2));
