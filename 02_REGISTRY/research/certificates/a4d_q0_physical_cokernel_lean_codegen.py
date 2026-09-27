#!/usr/bin/env python3
"""Temporary exact Q(i) rank-certificate codegen for A4DQ0PhysicalCokernel.

Emits only exact finite data needed by the Lean module: physical matrix P,
a 23x23 invertible submatrix and inverse, a nonzero left-cokernel vector,
cross-character forcings, q0 norms/residual pairings, and same-carrier metric
witnesses. This helper is removed before REVIEW.
"""
from __future__ import annotations
import json, os, sympy as sp

HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,"a4d_joint_resonance_linear_kernel_check.py")
text=open(SRC,encoding="utf-8").read()
cut=text.index("# ---------------------------------------------------------------------------\n# 2. Reproduce the nine owned singular orbit types")
ns={"__name__":"_q0_lean_codegen","__file__":SRC}
exec(compile(text[:cut],SRC,"exec"),ns)
HAB,HAQ,z,SYM=ns["HAB"],ns["HAQ"],ns["z"],ns["SYM"]

q0=sp.Matrix([(1/z[a]-1)*(1/z[b]-1) for a,b in SYM])
DC=[sp.simplify(z[j]*HAQ.diff(z[j])) for j in range(4)]
Dq=[sp.simplify(z[j]*q0.diff(z[j])) for j in range(4)]
ORB={5:(sp.I,sp.I,-sp.I,-sp.I),7:(-sp.Integer(1),sp.I,sp.I,-sp.Integer(1))}

def qi(x):
    x=sp.expand_complex(sp.simplify(x))
    re=sp.Rational(sp.re(x)); im=sp.Rational(sp.im(x))
    return [int(re.p),int(re.q),int(im.p),int(im.q)]

def mat(M): return [[qi(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
def vec(v): return [qi(v[i]) for i in range(v.rows)]

out={}
for orb,phase in ORB.items():
    sub={z[j]:phase[j] for j in range(4)}
    csub={z[j]:sp.conjugate(phase[j]) for j in range(4)}
    A=HAB.subs(sub)
    C=HAQ.subs(csub)
    P=A.row_join(C)
    assert P.rank()==23

    # Pivot columns then independent rows give an explicit invertible 23x23 block.
    _,pivcols=P.rref()
    cols=list(pivcols)
    assert len(cols)==23
    Q=P[:,cols]
    _,pivrows=Q.T.rref()
    rows=list(pivrows)
    assert len(rows)==23
    B=P.extract(rows,cols)
    assert B.det()!=0
    Binv=B.inv()

    left=sp.conjugate(P).T.nullspace()
    assert len(left)==1
    ell=left[0]

    qv=sp.simplify(q0.subs(sub))
    qnorm=sp.simplify((sp.conjugate(qv).T*qv)[0])
    en=sp.simplify((sp.conjugate(ell).T*ell)[0])

    cross=[]; same=[]
    for j in range(4):
        w=sp.simplify((DC[j]*q0).subs(sub))
        alpha=sp.simplify((sp.conjugate(ell).T*w)[0])
        raw=sp.simplify(sp.conjugate(alpha)*alpha/en)
        ws=sp.simplify((DC[j]*q0).subs(csub))
        dq=sp.simplify(Dq[j].subs(csub))
        assert sp.simplify(ws+C*dq)==sp.zeros(24,1)
        cross.append({"w":vec(w),"pair":qi(alpha),"raw2":qi(raw)})
        same.append({"w":vec(ws),"dq":vec(dq)})
    out[str(orb)]={
      "P":mat(P),"rows":rows,"cols":cols,"Binv":mat(Binv),
      "ell":vec(ell),"qnorm2":qi(qnorm),"ellnorm2":qi(en),
      "cross":cross,"same":same
    }

print("Q0_LEAN_CODEGEN_JSON="+json.dumps(out,separators=(",",":")))
