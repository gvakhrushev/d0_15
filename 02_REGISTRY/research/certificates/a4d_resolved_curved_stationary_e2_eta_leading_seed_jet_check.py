#!/usr/bin/env python3
"""Exact obstruction for eta-leading germs from the degenerate solder seed.

A=A0+eps*v+O(eps^2), Theta=eps*eta+O(eps^2), arbitrary L=2 translations,
and constant coefficients of the four selected F4 channels. One absolute
solder and homogeneous links are used; all 16 real Fourier modes of the
64-edge translation field enter the necessary homogeneous Euler rows.

This is a genuine stationary seed at Theta=0 (all base residuals vanish),
not the nonstationary seed Theta=eta of the earlier unit-Newton gate. Every
owned seven-support is blocked through solder/link order two plus affine
order three. The leading solder is prescribed eta; general critical leading
solder and finite seven-amplitude points are outside this result.
"""
from __future__ import annotations
import contextlib, importlib.util, io
from itertools import combinations, product
from pathlib import Path
import sympy as sp

def check(name,condition):
    if not condition: raise AssertionError(name)
    print('PASS_'+name,flush=True)

here=Path(__file__).resolve().parent
def load(name,filename):
    spec=importlib.util.spec_from_file_location(name,here/filename)
    m=importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m

g=load('joint_channels','a4d_resolved_curved_stationary_e2_all_supports_joint_channel_check.py')
j=load('jet2','a4d_resolved_curved_stationary_e2_support7_affine_order2_check.py')
o=g.owner;z4=sp.zeros(4);z416=sp.zeros(4,16)
H0=g.joint_owner.hessian;eta=sp.Matrix(list(o.ETA))
check('DEGENERATE_SOLDER_SEED_EXACTLY_STATIONARY',all(M.det()==0 and M.adjugate()==z4 for M in g.factors.values()))
check('ETA_IS_NONDEGENERATE_CRITICAL_LEADING_SOLDER',H0*eta==sp.zeros(16,1) and o.ETA.det()==-1)
# [eps^2] EL_Theta = H0 Y + H1(v) eta. Cokernel elimination is linear.
L=sp.Matrix.vstack(*[v.T for v in H0.nullspace()]);P=L*g.S
expected=sp.Matrix.hstack(*[sp.Matrix(v)for v in (
 (1,1,0,0,0,0,0,0,0,0,0,0),
 (0,0,1,0,0,0,0,0,0,0,0,0),
 (0,0,0,1,0,0,0,0,0,0,0,0),
 (0,0,0,0,1,1,0,0,0,0,0,0),
 (0,0,0,0,0,0,0,0,1,1,0,0),
 (-4,0,0,0,0,0,-1,0,0,0,0,1))])
check('FULL_NORMAL_SOLDER_COKERNEL_KERNEL_DIMENSION_SIX',P.rank()==6 and P*expected==sp.zeros(P.rows,6) and expected.rank()==6)
for index,support in enumerate(o.MINIMUM_SUPPORTS):
    cols=[g.names.index(name)for name in support];N=P[:,cols].nullspace()
    K=sp.Matrix.hstack(*N);active=[i for i,name in enumerate(support)if name in ('N2_2','N3_3')]
    check(f'SUPPORT_{index}_SOLDER_LIFT_KERNEL_DIMENSION',K.cols==(2,1,1,2,2,3,1,1)[index])
    if index!=5:
        check(f'SUPPORT_{index}_FIRST_RESIDUAL_FORCED_ZERO',K[active,:]==sp.zeros(len(active),K.cols))
V1=[z4,z4,o.K1,z4]
V2=[o.N3,o.N3,z4,z4]
V3=[-4*o.K1,z4,-o.N2,o.N3]
Vs=[V1,V2,V3]
selected=sp.Matrix([[0,0,-4],[1,0,0],[0,0,-1],[0,1,0],[0,1,0],[0,0,0],[0,0,1]])
cols=[g.names.index(name)for name in o.SELECTED_NAMES]
check('SUPPORT_FIVE_TANGENT_KERNEL_EXACT',P[:,cols]*selected==sp.zeros(P.rows,3) and selected.rank()==3)
# w: a homogeneous role-0 Lorentz variation whose first residual is zero.
w=sp.Rational(9,2)*o.J23-sp.Rational(3,2)*o.N2+o.N3
Ws=[[w,z4,z4,z4],[z4,z4,o.N2,z4],[z4,z4,z4,o.N2]]
check('THREE_LITERAL_STAR_SOURCES',
      [o.d_star(o.role0,o.generators0,r,a)for r,a in ((0,w),(2,o.N2),(3,o.N2))]==[24,-32,0])

def add(a,b):return [x+y for x,y in zip(a,b)]
cache={}
def kin(h):
    key=tuple(tuple(m)for m in h)
    if key in cache:return cache[key]
    U=[j.cayley_jet(a,b)for a,b in zip(o.generators0,h)];Ui=[j.jet_inv(u)for u in U]
    faces={};one=[sp.eye(4),z4,z4]
    for r,s in o.PAIRS:
        q=j.jet_mul(j.jet_mul(j.jet_mul(U[r],U[s]),Ui[r]),Ui[s])
        M=j.jet_add(one,j.jet_neg(q));D=j.det_jet(M);A=j.adj_jet(M)
        assert D[0]==D[1]==0 and A[0]==z4
        faces[r,s]=(q,M,D,A)
    cache[key]=(U,faces);return cache[key]

def residuals(data,signs):
    U,faces=data;B=[]
    for r in range(4):
        b=sp.zeros(4,16);b[:,4*r:4*r+4]=sp.eye(4);B.append(b)
    T={}
    for r,s in o.PAIRS:
        aa=j.jet_add(j.constant_jet(B[r]),j.jet_mul(U[r],j.constant_jet(signs[r]*B[s])))
        bb=j.jet_add(j.constant_jet(B[s]),j.jet_mul(U[s],j.constant_jet(signs[s]*B[r])))
        T[r,s]=j.jet_add(aa,j.jet_neg(j.jet_mul(faces[r,s][0],bb)))
    out={}
    for f in o.PAIRS:
        _,M,D,A=faces[f]
        for h in o.PAIRS:
            if f==h:continue
            R=j.jet_add(j.scalar_jet_mul(D,T[h]),j.jet_neg(j.jet_mul(j.jet_mul(faces[h][1],A),T[f])))
            assert R[0]==z416
            out[f,h]=R[1:]
    return out

monomials=[(i,i)for i in range(3)]+list(combinations(range(3),2))
kv=[kin(v)for v in Vs];kw=[kin(w)for w in Ws]
kp={(i,k):kin(add(Vs[i],Vs[k]))for i,k in combinations(range(3),2)}
km={(i,w):kin(add(Vs[i],Ws[w]))for i in range(3)for w in range(3)}

def psd_by_congruence(M):
    M=M.copy()
    while M.rows:
        pivot=next((i for i in range(M.rows)if M[i,i]),None)
        if pivot is None:return M==sp.zeros(M.rows)
        if M[pivot,pivot]<0:return False
        inds=[i for i in range(M.rows)if i!=pivot];v=M[inds,pivot]
        M=M.extract(inds,inds)-v*v.T/M[pivot,pivot]
    return True

ranks=[]
for parity in product(range(2),repeat=4):
    signs=[(-1)**p for p in parity]
    rv=[residuals(k,signs)for k in kv];rw=[residuals(k,signs)for k in kw]
    rp={p:residuals(k,signs)for p,k in kp.items()};rm={p:residuals(k,signs)for p,k in km.items()}
    assert all(R[0]==z416 for R in rw[0].values()) # R1(w)=0
    # Q3 on the solder-lift tangent. R1=z3*n*ell, so Q3 has
    # only z3*zi*zj monomials. Symmetrize its actual b-quadratic forms.
    qforms=[[],[],[]]
    for i,k in monomials:
        Fs=[sp.zeros(16)for _ in range(3)]
        for fg in rv[0]:
            f,h=fg;cls=0 if len(set(f)&set(h))==1 else 1
            ell=rv[2][fg][0][0,:]
            R2=rv[i][fg][1]if i==k else rp[i,k][fg][1]-rv[i][fg][1]-rv[k][fg][1]
            for metric,ch,sgn in ((o.ETA,cls,1),(sp.eye(4),2,1 if cls==0 else -1)):
                Fs[ch]+=16*sgn*(rv[2][fg][0].T*metric*R2+R2.T*metric*rv[2][fg][0])
        for ch,F in enumerate(Fs):qforms[ch].append(F)
    check(f'MODE_{parity}_ETA_Q3_ZERO',all(F==sp.zeros(16)for ch in (0,1)for F in qforms[ch]))
    check(f'MODE_{parity}_N_DIFF_Q3_ONLY_Z3_CUBED',all(qforms[2][i]==sp.zeros(16)for i in (0,1,3,4,5)))
    H3=qforms[2][2];N=H3.nullspace();K=sp.Matrix.hstack(*N)if N else sp.zeros(16,0)
    forms=[]
    for row in range(3):
        rowforms=[]
        for i,k in monomials:
            Fs=[sp.zeros(16)for _ in range(3)]
            for fg in rv[0]:
                f,h=fg;cls=0 if len(set(f)&set(h))==1 else 1
                r1i,r2i=rv[i][fg];mixedi=rm[i,row][fg][1]-r2i-rw[row][fg][1]
                if i==k: aa=r2i;b1=r1i;b2=mixedi;c1=z416;c2=z416
                else:
                    r1k,r2k=rv[k][fg];mixedk=rm[k,row][fg][1]-r2k-rw[row][fg][1]
                    aa=rp[i,k][fg][1]-r2i-r2k;b1=r1i;b2=mixedk;c1=r1k;c2=mixedi
                for metric,ch,sgn in ((o.ETA,cls,1),(sp.eye(4),2,1 if cls==0 else -1)):
                    Fs[ch]+=32*sgn*(aa.T*metric*rw[row][fg][0]+b1.T*metric*b2+c1.T*metric*c2)
            rowforms.append([(F+F.T)/2 for F in Fs])
        forms.append(rowforms)
    check(f'MODE_{parity}_W_ETA_CHANNEL_COKERNEL',all(F==sp.zeros(16)for fs in forms[0]for F in fs[:2]))
    restricted=[[[K.T*F*K for F in fs]for fs in row]for row in forms]
    check(f'MODE_{parity}_TWO_LINK_ROWS_ONLY_Z3_SQUARED',all(restricted[r][m][ch]==sp.zeros(K.cols)for r in (1,2)for m in (0,1,3,4,5)for ch in range(3)))
    check(f'MODE_{parity}_TWO_LINK_ROWS_ETA_EQUAL',all(restricted[r][2][0]==restricted[r][2][1]for r in (1,2)))
    check(f'MODE_{parity}_TWO_LINK_ROWS_N_DIFF_ZERO',all(restricted[r][2][2]==sp.zeros(K.cols)for r in (1,2)))
    A=restricted[2][2][0];B=restricted[1][2][0]
    check(f'MODE_{parity}_N2_ROLE3_FORM_POSITIVE_SEMIDEFINITE',psd_by_congruence(A))
    NA=A.nullspace();KA=sp.Matrix.hstack(*NA)if NA else sp.zeros(K.cols,0)
    check(f'MODE_{parity}_PSD_KERNEL_KILLS_N2_ROLE2_FORM',KA.T*B*KA==sp.zeros(KA.cols))
    ranks.append((parity,H3.rank(),A.rank()))
# Character orthogonality legitimizes the modewise sum for arbitrary b.
sites=list(product(range(2),repeat=4));Walsh=sp.Matrix([[(-1)**sum(p[r]*x[r]for r in range(4))for x in sites]for p in sites])
check('REAL_L2_FOURIER_BASIS_COMPLETE_ORTHOGONAL',Walsh*Walsh.T==16*sp.eye(16))
print('AFFINE_Q3_AND_POSITIVE_FORM_RANKS',ranks,flush=True)
print('EXACT_OBSTRUCTION: supports other than 5 force R1=0, giving w*EL2=24; support 5 with R1!=0 forces c_n_adj+c_n_opp=0. If c_n_adj-c_n_opp=0, w*EL2=24. Otherwise affine EL3 imposes H3*b=0 modewise. N2_role3 EL2 is a common coefficient times a sum of nonnegative squares; its zero set kills every N2_role2 channel term, leaving EL2=-32.',flush=True)
print('RESULT: all eight eta-leading germs from Theta=0 blocked through coupled order 3; no finite support-wide no-go and no L=2 active-residual witness',flush=True)
