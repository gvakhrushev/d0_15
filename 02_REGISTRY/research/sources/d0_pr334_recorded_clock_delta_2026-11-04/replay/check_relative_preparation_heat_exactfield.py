#!/usr/bin/env python3
"""Exact relative-preparation stationarity for the complete growing-clock heat.

Matrix application of EV19c, not a new native primitive or task selector.
The hand proof covers arbitrary Hermitian unequal old-age flags. Tests keep
those flags noncommuting with the reader, and use the actual Golden reader.
"""
import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


p = (sp.sqrt(5)-1)/2
a = sp.sqrt(p)
field = sp.QQ.algebraic_field(a, sp.I)
cache = {}
checks = []


def need(value, label):
    if not bool(value):
        raise ArithmeticError(label)
    checks.append(label)


def scalar(value):
    value = sp.sympify(value)
    if value not in cache:
        cache[value] = field.from_sympy(value)
    return cache[value]


def dm(matrix):
    rows = {}
    for (i,j), value in matrix.todok().items():
        c = scalar(value)
        if c != field.zero:
            rows.setdefault(i,{})[j] = c
    return DomainMatrix(rows, matrix.shape, field)


def ident(n):
    return dm(sp.eye(n))


def mul(*items):
    out=items[0]
    for item in items[1:]:
        out=out.matmul(item)
    return out


def scaled(matrix, value):
    return matrix.scalarmul(scalar(value))


def eq(left,right,label):
    need(not left.sub(right).to_dok(),label)


def tr(matrix):
    entries=matrix.to_dok()
    return sum((entries.get((i,i),field.zero) for i in range(matrix.shape[0])),field.zero)


conjugate_generator = scalar(sp.conjugate(field.ext.as_expr()))
conjugate_cache = {}


def conj(value):
    if value not in conjugate_cache:
        out = field.zero
        for coefficient in value.to_list():
            out = out*conjugate_generator+field.convert(coefficient)
        conjugate_cache[value] = out
    return conjugate_cache[value]


def adj(matrix):
    rows = {}
    for (i,j), value in matrix.to_dok().items():
        rows.setdefault(j,{})[i] = conj(value)
    return DomainMatrix(rows, (matrix.shape[1],matrix.shape[0]), field)


def direct_logjet(W, dW, age):
    return -tr(mul(ident(8).sub(mul(W,age)).inv(),dW,age))


def real_rotation(i,j,c=sp.Rational(3,5),s=sp.Rational(4,5)):
    out=sp.eye(4)
    out[i,i]=out[j,j]=c
    out[i,j]=-s
    out[j,i]=s
    return out


I=ident(4)
F=dm(sp.diag(1,1,0,0))
G=dm(sp.diag(0,0,-1,-1))
Q=mul(G,G)
A=scaled(F,a).add(scaled(G,p))
H=scaled(F,a).sub(scaled(G,p))
B=scaled(G,a).add(scaled(F,p))
C=scaled(G,a).sub(scaled(F,p))
R=Q.sub(scaled(I,p*p))
W=A.hstack(B).vstack(C.hstack(H))
eq(mul(adj(W),W),ident(8),'actual Golden completed reader is unitary on every active column')
eq(mul(B,C),R,'actual off-diagonal reader product is Q minus p squared')

O=dm(real_rotation(0,2)*real_rotation(1,3,sp.Rational(5,13),sp.Rational(12,13))*real_rotation(0,1))
eq(mul(adj(O),O),I,'old-age flag basis is an exact real orthogonal basis')
X=dm(sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-2],[0,0,2,0]]))
Xi=dm(sp.I*sp.diag(1,2,3,4))
for name,generator in [('real',X),('complex',Xi)]:
    eq(adj(generator),scaled(generator,-1),name+' relative preparation generator is skew-Hermitian')
    eq(mul(generator,F),mul(F,generator),name+' generator preserves all F effects')
    eq(mul(generator,G),mul(G,generator),name+' generator preserves all G effects')

K=dm(real_rotation(0,1)*real_rotation(2,3,sp.Rational(5,13),sp.Rational(12,13)))
Ki=dm(sp.diag((3+4*sp.I)/5,(5-12*sp.I)/13,1,(3-4*sp.I)/5))


def expanded(k):
    zero=dm(sp.zeros(4))
    return k.hstack(zero).vstack(zero.hstack(k))


def schur(k,D,t):
    E=I.sub(scaled(mul(H,k),t))
    L=mul(A,k).add(scaled(mul(E.inv(),R,k,k),t))
    return E,L,E.det()*I.sub(mul(L,D)).det()


diagnostics={}
for q in [sp.Rational(1,7),sp.Rational(2,7),sp.Rational(3,7)]:
    # Multiplicities1,1,2 are actual finite birth-detail dimensions;
    # the final new record has all four of its complement columns at age4.
    D=mul(O,dm(sp.diag(q**7,q**6,q**5,q**5)),adj(O))
    t=q**4
    zero=dm(sp.zeros(4))
    age=D.hstack(zero).vstack(zero.hstack(scaled(I,t)))
    need(bool(D.matmul(F).sub(F.matmul(D)).to_dok()),'old age flags fail to commute with F at '+str(q))
    need(bool(D.matmul(X).sub(X.matmul(D)).to_dok()),'old age flags fail to commute with relative generator at '+str(q))
    E,L,schur_det=schur(I,D,t)
    need(schur_det==ident(8).sub(mul(W,age)).det(),'entire unequal-age determinant equals exact Schur formula at '+str(q))
    eq(adj(L),L,'unperturbed effective return is Hermitian at '+str(q))
    metric=mul(D,I.sub(mul(L,D)).inv())
    eq(adj(metric),metric,'noncommuting age resolvent pairing is Hermitian at '+str(q))

    for name,generator in [('real',X),('complex',Xi)]:
        dw=mul(W,expanded(generator))
        direct=direct_logjet(W,dw,age)
        dE=scaled(mul(H,generator),-t)
        coefficient=A.add(scaled(mul(E.inv(),E.inv(),H,R),t*t)).add(scaled(mul(E.inv(),R),2*t))
        dL=mul(coefficient,generator)
        eq(adj(dL),scaled(dL,-1),name+' Schur derivative is skew-Hermitian at '+str(q))
        derived=tr(mul(E.inv(),dE))-tr(mul(metric,dL))
        need(direct==derived,name+' exact direct/Schur complete clock jet agrees at '+str(q))
        need(direct+conj(direct)==field.zero,name+' complete clock logjet has zero real part at '+str(q))
        if name=='real':
            need(direct==field.zero,'real complete clock logjet itself vanishes at '+str(q))
        else:
            need(direct!=field.zero,'complex clock logjet need not vanish before taking real part at '+str(q))

    for name,k in [('real',K),('complex',Ki)]:
        E1,L1,det1=schur(k,D,t)
        E2,L2,det2=schur(adj(k),D,t)
        eq(E2,adj(E1),name+' finite E has adjoint reversal at '+str(q))
        eq(L2,adj(L1),name+' finite L has adjoint reversal at '+str(q))
        need(det2==conj(det1),name+' entire clock determinant has conjugate reversal at '+str(q))
        direct=ident(8).sub(mul(W,expanded(k),age)).det()
        need(direct==det1,name+' finite direct full-clock determinant agrees at '+str(q))

    if q==sp.Rational(2,7):
        Xbad=dm(sp.Matrix([[0,0,-1,0],[0,0,0,0],[1,0,0,0],[0,0,0,0]]))
        bad=direct_logjet(W,mul(W,expanded(Xbad)),age)
        need(bad!=field.zero and conj(bad)==bad,'hostile noncommutant direction has nonzero real complete-clock logjet')
        diagnostics['noncommutant_clock_logjet']=str(field.to_sympy(bad))
        # A prepared-cut complement control. The physical input is the
        # OLDEST age eigenspace, so it is compatible with the birth filtration.
        jold=dm(O.to_Matrix()[:,0:1])
        local_extra=dm(sp.Matrix([[0,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,0]]))
        extra=mul(O,local_extra,adj(O))
        eq(mul(extra,jold),dm(sp.zeros(4,1)),'prepared complement generator annihilates actual oldest input cut')
        eq(mul(D,jold),scaled(jold,q**7),'physical input occupies actual oldest birth-age subspace')
        Vextra=mul(O,dm(real_rotation(1,2)),adj(O))
        eq(mul(Vextra,jold),jold,'finite complement preparation preserves the entire prepared input state')
        oldcorner=mul(adj(jold),A,jold)
        eq(mul(adj(jold),A,Vextra,jold),oldcorner,'forward complement change preserves the actual proper return corner')
        eq(mul(adj(jold),adj(Vextra),A,jold),oldcorner,'backward complement change preserves the actual proper return corner')
        complement_jet=direct_logjet(W,mul(W,expanded(extra)),age)
        need(complement_jet!=field.zero and conj(complement_jet)==complement_jet,
             'prepared-cut invisible complement has nonzero real complete-clock polynomial jet')
        diagnostics['prepared_complement_clock_logjet']=str(field.to_sympy(complement_jet))
        Dnew=mul(dm(real_rotation(0,2)*real_rotation(1,2)),dm(sp.diag(q**4,q**3,q**2,q)),adj(dm(real_rotation(0,2)*real_rotation(1,2))))
        age_bad=D.hstack(zero).vstack(zero.hstack(Dnew))
        badnew=direct_logjet(W,mul(W,expanded(X)),age_bad)
        need(badnew!=field.zero and conj(badnew)==badnew,'hostile nonscalar last-record age block breaks the zero real logjet')
        diagnostics['nonscalar_record_clock_logjet']=str(field.to_sympy(badnew))

# The actual physical cut can be proper; no whole-old-input substitution.
embedding=dm(O.to_Matrix()[:,:2])
eq(mul(adj(embedding),embedding),ident(2),'proper physical input embedding is normalized')
corner=mul(adj(embedding),A,embedding)
zeta=sp.Rational(1,2**20)
Jbase=ident(2).scalarmul(scalar(1-zeta)).add(scaled(mul(adj(corner),corner),zeta)).det()
for name,generator in [('real',X),('complex',Xi)]:
    dc=mul(adj(embedding),A,generator,embedding)
    eq(adj(dc),scaled(dc,-1),name+' proper-cut corner derivative is skew-Hermitian')
    resolvent=ident(2).scalarmul(scalar(1-zeta)).add(scaled(mul(corner,corner),zeta)).inv()
    jet=tr(mul(resolvent,corner,dc))
    need(jet+conj(jet)==field.zero,name+' complete feedback first source vanishes on proper input cut')
for name,k in [('real',K),('complex',Ki)]:
    cp=mul(adj(embedding),A,k,embedding)
    cm=mul(adj(embedding),A,adj(k),embedding)
    eq(cm,adj(cp),name+' finite proper corners are adjoint under reversal')
    dp=ident(2).scalarmul(scalar(1-zeta)).add(scaled(mul(adj(cp),cp),zeta)).det()
    dm_=ident(2).scalarmul(scalar(1-zeta)).add(scaled(mul(adj(cm),cm),zeta)).det()
    need(dp==dm_,name+' finite full feedback prices agree under reversal')
    need(dp!=Jbase,name+' finite feedback is not constant over the commutant')

print(json.dumps({
    'schema':'d0.relative-preparation-full-heat/1','status':'PASS',
    'checks':len(checks),'check_labels':checks,
    'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'input':'724a5a1b8fb00ee065337a719508c9fbfc4e0048',
    'exact_field':'QQ(sqrt((sqrt(5)-1)/2),i)',
    'conclusion':'full original H+J(K)=H+J(K adjoint); independent commutant first rows vanish at matched preparation',
    'scope':{'fixed_frontloaded_layout':True,'record_last_scalar_age_block':True,
             'unequal_noncommuting_old_ages_retained':True,'original_cosine_heat_kernel':True,
             'proper_physical_cut_retained':True,'new_native_primitive_claimed':False,
             'full_price_constant_on_commutant':False,'minimum_claimed':False,'GR_closed':False},
    'hostile_controls':diagnostics,
},sort_keys=True,indent=2))
