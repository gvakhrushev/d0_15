#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact joint-rank theorem on the quarter-temporal spatial-diagonal stratum.

For the curved z=1 full joint Bloch operator Q(lambda) (136 x 96), consider

  lambda_0 = zeta in mu_4,   lambda_1=lambda_2=lambda_3=x in C^*.

The certificate proves that the only rank drop on this entire complex
one-dimensional stratum is x=zeta.  Thus the continuous metric-block
rank-drop stratum contains no additional joint resonance.

Method:
* consume the literal 21-term Laurent stencil;
* use the 95-row folded transverse range chart and augment it by connection
  rows 4 and 15 to obtain two 96x96 minors;
* on the zeta=1 stratum, clear the common stencil denominator 14 and reconstruct
  P_i(x)=x^96 det(14 M_i(x)) exactly by 256-root finite-field DFT + CRT;
* use a Hadamard/Cauchy coefficient bound to stop CRT only when centered
  reconstruction is mathematically unique;
* remove the Laurent-unit x-powers and contents, then compute the exact
  primitive gcd in Z[x], which is x-1;
* prove global quarter-phase covariance entry by entry, transferring the
  zeta=1 result to all four zeta in mu_4.

No floating-point rank or interpolation tolerance enters the certificate.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

import a4d_y_curved_joint_torus_lipschitz_check as L
import a4d_y_curved_joint_folded_range_check as F

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_quarter_spatial_diagonal_results.json"

DEN=14
NFFT=256
PSTART=600000
EXTRA_ROWS=(4,15)
ROWSETS=[F.ROWS+[r] for r in EXTRA_ROWS]


def ck(name,cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name,flush=True)


def row_phase(row):
    return row//24 if row<96 else (row-96)//10


def col_phase(col):
    return col//24


# Global covariance under a common fourth-root multiplication of all Bloch
# characters.  This is stronger than the diagonal-only use in the folded
# range owner.
phase_covariant=True
for d,M in L.T.items():
    e=sum(d)%4
    for (r,c),v in M.todok().items():
        if v and e!=(col_phase(c)-row_phase(r))%4:
            phase_covariant=False
ck("GLOBAL_QUARTER_PHASE_COVARIANCE",phase_covariant)


# On lambda0=1, lambda1=lambda2=lambda3=x, every selected entry is Laurent
# degree -1,0,1 in x.  Scale all matrix entries by DEN so coefficients are
# integral.  The determinant scaling DEN^96 is irrelevant to its zero set.
rawsets=[]
hadamard_square_bounds=[]
for si,rows in enumerate(ROWSETS):
    ck("ROWSET_SIZE_"+str(si),len(rows)==96 and len(set(rows))==96)
    rpos={r:i for i,r in enumerate(rows)}
    raw=[]
    envelope=[[0]*96 for _ in range(96)]
    for d,M in L.T.items():
        exponent=sum(d[1:])
        if exponent not in (-1,0,1):
            raise AssertionError("SPATIAL_DIAGONAL_ENTRY_DEGREE")
        selected=[]
        for (r,c),v in M.todok().items():
            if r not in rpos or not v:
                continue
            q=sp.Rational(v)
            if DEN%int(q.q)!=0:
                raise AssertionError("COMMON_DENOMINATOR")
            a=int(q*DEN)
            selected.append((rpos[r],c,a))
            envelope[rpos[r]][c]+=abs(a)
        if selected:
            raw.append((exponent,selected))
    rawsets.append(raw)
    ck("INTEGER_LAURENT_STENCIL_"+str(si),True)

    # For |x|=1, |entry| is bounded by its Laurent coefficient l1 envelope.
    # Hadamard gives |det|^2 <= product(row_l2_bound^2).  Every Laurent
    # coefficient is bounded by sup_|x|=1 |det| by Cauchy's coefficient
    # formula, so this is also a squared bound for every integer coefficient.
    b2=1
    for row in envelope:
        n2=sum(a*a for a in row)
        ck("NONZERO_ROW_ENVELOPE_"+str(si),n2>0)
        b2*=n2
    hadamard_square_bounds.append(b2)


def detmod(A,p):
    A=A.copy()%p
    n=A.shape[0]
    det=1
    for c in range(n):
        nz=np.flatnonzero(A[c:,c])
        if not len(nz):
            return 0
        rr=c+int(nz[0])
        if rr!=c:
            A[[c,rr]]=A[[rr,c]]
            det=(-det)%p
        piv=int(A[c,c])
        det=det*piv%p
        inv=pow(piv,-1,p)
        ids=np.arange(c+1,n)
        ids=ids[A[ids,c]!=0]
        if len(ids):
            fac=(A[ids,c].copy()*inv)%p
            A[ids,c:]=(A[ids,c:]-fac[:,None]*A[c,c:])%p
    return int(det%p)


def prime_1mod256(start):
    n=start+((1-start)%NFFT)
    while not sp.isprime(n):
        n+=NFFT
    return int(n)


def primitive_256(p):
    for a in range(2,1000):
        w=pow(a,(p-1)//NFFT,p)
        if pow(w,NFFT//2,p)==p-1:
            return w
    raise AssertionError("primitive 256th root not found")


def coefficients_mod(raw,p):
    w=primitive_256(p)
    values=[]
    z=1
    for _ in range(NFFT):
        M=np.zeros((96,96),dtype=np.int64)
        for exponent,entries in raw:
            phase=(pow(z,exponent,p) if exponent>=0
                   else pow(pow(z,-1,p),-exponent,p))
            for i,j,a in entries:
                M[i,j]=(M[i,j]+phase*(a%p))%p
        # x^96 clears every possible negative determinant exponent because
        # each matrix entry has exponent >= -1.
        values.append(detmod(M,p)*pow(z,96,p)%p)
        z=z*w%p

    invN=pow(NFFT,-1,p)
    coeff=[]
    for k in range(NFFT):
        wk=pow(w,(-k)%NFFT,p)
        cur=1
        total=0
        for value in values:
            total=(total+value*cur)%p
            cur=cur*wk%p
        coeff.append(total*invN%p)

    # Structural degree bound: x^96 det has degree at most 192.
    ck("DFT_NO_ALIAS_TAIL_MOD_"+str(p),
       all(c==0 for c in coeff[193:]))
    return coeff[:193]


# Incremental CRT.  Stop only when M_CRT > 2*sqrt(B2), checked without
# floating point as M_CRT^2 > 4*B2.
crt=[[0]*193 for _ in ROWSETS]
modulus=1
primes=[]
start=PSTART
while modulus*modulus<=4*max(hadamard_square_bounds):
    p=prime_1mod256(start)
    start=p+NFFT
    ck("GOOD_PRIME_DENOMINATOR_"+str(p),DEN%p!=0)
    residues=[coefficients_mod(raw,p) for raw in rawsets]
    inv_modulus=pow(modulus%p,-1,p)
    for si in range(len(ROWSETS)):
        for k in range(193):
            lift=((residues[si][k]-crt[si][k])%p)*inv_modulus%p
            crt[si][k]+=lift*modulus
    modulus*=p
    primes.append(p)

ck("CRT_UNIQUENESS_BOUND",
   modulus*modulus>4*max(hadamard_square_bounds))

x=sp.symbols("x")
primitive_polynomials=[]
records=[]
for si in range(len(ROWSETS)):
    coeff=[a if a<=modulus//2 else a-modulus for a in crt[si]]
    ck("HADAMARD_RECONSTRUCTION_BOUND_"+str(si),
       all(a*a<=hadamard_square_bounds[si] for a in coeff))
    nz=[k for k,a in enumerate(coeff) if a]
    ck("NONZERO_DETERMINANT_POLYNOMIAL_"+str(si),bool(nz))
    support=(min(nz),max(nz))

    P=sp.Poly(sum(a*x**k for k,a in enumerate(coeff)),x,domain=sp.ZZ)
    x_power=0
    while P.eval(0)==0:
        P=sp.Poly(P.as_expr()/x,x,domain=sp.ZZ)
        x_power+=1
    content,primitive=sp.polys.polytools.primitive(P)
    if primitive.LC()<0:
        primitive=-primitive
        content=-content

    ck("FOLDED_ROOT_"+str(si),primitive.eval(1)==0)
    quotient,remainder=sp.div(primitive,sp.Poly(x-1,x,domain=sp.ZZ))
    ck("FOLDED_ROOT_SIMPLE_"+str(si),
       remainder.is_zero and quotient.eval(1)!=0)

    plist=[int(primitive.nth(k)) for k in range(primitive.degree()+1)]
    phash=hashlib.sha256(",".join(map(str,plist)).encode()).hexdigest()
    primitive_polynomials.append(primitive)
    records.append({
      "extra_row":EXTRA_ROWS[si],
      "x96_integer_support":[support[0],support[1]],
      "removed_x_power":x_power,
      "primitive_degree":primitive.degree(),
      "primitive_content":str(content),
      "primitive_coefficients_sha256":phash,
      "folded_root_multiplicity":1,
    })

gcd=sp.gcd(primitive_polynomials[0],primitive_polynomials[1])
if gcd.LC()<0:
    gcd=-gcd
ck("EXACT_INTEGER_GCD_X_MINUS_ONE",
   gcd==sp.Poly(x-1,x,domain=sp.ZZ))

# The two minors cannot vanish simultaneously for any x in C^* except x=1.
# Quarter-phase covariance transfers this statement from zeta=1 to every
# zeta in mu_4 by x -> x/zeta.
result={
 "schema":"a4d-y-curved-joint-quarter-spatial-diagonal-v1",
 "terminal":"A4D-Y-CURVED-JOINT-QUARTER-SPATIAL-DIAGONAL-CERTIFIED",
 "stratum":"lambda0=zeta in mu4; lambda1=lambda2=lambda3=x in C^*",
 "operator_shape":[136,96],
 "common_denominator":DEN,
 "determinant_minors":records,
 "crt":{
   "prime_count":len(primes),
   "primes":primes,
   "modulus_bits":modulus.bit_length(),
   "hadamard_square_bound_bits":[b.bit_length() for b in hadamard_square_bounds],
   "unique_centered_reconstruction":True
 },
 "exact_primitive_gcd":"x - 1",
 "conclusion":"for lambda0=1 and lambda1=lambda2=lambda3=x, joint rank is 96 for every complex x!=1; quarter-phase covariance gives the unique rank drop x=zeta for each zeta in mu4",
 "phase_covariance":"Q(zeta*lambda)=D_out(zeta) Q(lambda) D_in(zeta) for zeta^4=1",
 "scope_fence":[
   "entire complex one-dimensional quarter-temporal spatial-diagonal stratum",
   "not the full four-dimensional unit torus",
   "no nonlinear reduced-center theorem",
   "no task-level response terminal"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)

print("TERMINAL A4D-Y-CURVED-JOINT-QUARTER-SPATIAL-DIAGONAL-CERTIFIED")
