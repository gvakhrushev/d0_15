"""An orthogonal history tape with constant passive compression, on positive native gates."""
from collections import Counter
from importlib import util
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOT=Path(__file__).resolve().parents[7]
SOURCE=ROOT/"02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
spec=util.spec_from_file_location("original_positive_gate_domain",SOURCE)
nt=util.module_from_spec(spec)
sys.modules[spec.name]=nt
spec.loader.exec_module(nt)
p,a,G=nt.P,nt.A,nt.G_LOCAL
e0,e1=sp.eye(2)[:,0],sp.eye(2)[:,1]
v=sp.Matrix([a,p])
X=sp.Matrix([[0,1],[1,0]])
FIELD=nt.GOLDEN_FIELD


def equal(x,y):
    if isinstance(x,sp.MatrixBase):
        return (DomainMatrix.from_Matrix(sp.Matrix(x)).convert_to(FIELD).to_dense()
                ==DomainMatrix.from_Matrix(sp.Matrix(y)).convert_to(FIELD).to_dense())
    return FIELD.from_sympy(sp.sympify(x))==FIELD.from_sympy(sp.sympify(y))


def gate(name,*bits):
    return nt.Gate(name,bits)


def execution(n,word,port,spin):
    return nt.Execution(n,(),(),tuple(word),nt.G_CX_SOURCE_I,port,spin)


def expanded_reset():
    # All 16 input columns, not only an initialized PORT or one chosen Spin vector.
    E=execution(4,[gate("G",1)],0,(2,3))
    word=nt.inverse_word(E,max_qubits=4,max_expanded_stages=16)
    assert Counter(g.op for g in word)=={"CX":6,"SourceI":4,"G":1}
    inverse=nt.word_matrix(execution(4,word,0,(2,3)),max_qubits=4,max_expanded_stages=16)
    assert equal(inverse,sp.kronecker_product(sp.eye(2),G.T,sp.eye(4)))
    return word


def archive_word():
    # 0 PORT, 1/2 Spin, 3 unknown original history bit, 4..10 seven fresh v.
    h=3
    reset=nt.inverse_word(execution(11,[gate("G",4)],0,(1,2)),
                          max_qubits=11,max_expanded_stages=32)
    gates=list(reset)+[gate("CX",h,4)]
    for i in range(5,10):
        gates.extend((gate("CX",h,i),gate("G",i)))
    gates.extend((gate("G",10),gate("CX",h,10),gate("G",10),gate("CX",h,10)))
    E=nt.Execution(11,tuple(range(4,11)),(),tuple(gates),nt.G_CX_SOURCE_I,0,(1,2))
    inv=nt.inventory(E,max_qubits=11,max_expanded_stages=26)
    assert (inv.blank_count,inv.g_count,inv.cx_count,inv.source_i_count)==(7,8,14,4)
    assert 7+len(gates)==33
    return gates


def deterministic():
    assert equal(G.T*v,e0) and equal(G*X*v,e1)
    assert equal((v.T*G*v)[0],a)
    assert equal((v.T*(G**2)*v)[0],p**3)
    assert equal(X*G*X*G,sp.eye(2))
    memory=[]
    for h in (0,1):
        x=X if h else sp.eye(2)
        outputs=[x*G.T*v]+[G*x*v]*5+[x*G*x*G*v]
        assert all(equal((w.T*w)[0],1) for w in outputs)
        cold=sp.prod((v.T*w)[0] for w in outputs)
        assert equal(cold,p**6)
        assert equal(outputs[0],(e0,e1)[h])
        memory.append(outputs)
    assert equal((memory[0][0].T*memory[1][0])[0],0)
    print("per history bit: 7 births, 8 G, 14 CX, 4 SourceI; cold amplitude p^6 both ways")


def no_inverse():
    # C is a fresh golden source sampled before any field. g=0 has h=0 on idle.
    for C,h in ((0,0),(1,0),(1,1)):
        key=X if C else sp.eye(2)
        x=X if h else sp.eye(2)
        r0=x*key*G*key*v
        r1=x*G*key*v
        if C==1:
            assert equal(r0,(e0,e1)[h]) and equal(r1,(e1,e0)[h])
        else:
            assert equal(r0,G*v) and equal(r1,G*v)
        assert equal((v.T*r0)[0]*(v.T*r1)[0],a*p if C else p)
    print("heralded variant: 2 births, 2 G, 5 CX; readiness p^2, success overlap a*p, idle p")


def distinguish_measurements():
    # Old input 0, genuine A=G; penalty sign selects the relative phase.
    # Passive-only contraction is coherent. A sharp read before it erases cross terms.
    lam=p**6
    coh=lam**2*(a**2-p**2)**2
    pinched=lam**2*(a**4+p**4)
    assert equal(pinched-coh,2*lam**2*p**3) and not equal(coh,pinched)
    e=sp.Matrix([[sp.Rational(1,2),sp.Rational(1,6)],
                 [sp.Rational(1,6),sp.Rational(2,3)]])
    e0x=sp.eye(2)-e
    # Noncommuting positive outcomes on two fine branches of one T value.
    k0=sp.diag(sp.Rational(1,4),sp.Rational(1,8))
    k1=e-k0
    assert k0.det()>0 and k1.det()>0 and e0x.det()>0 and k0*k1!=k1*k0
    d0,d1=sp.Rational(2,3),sp.Rational(4,5)
    compressed=lam*d0*e0x+lam*d1*k0+lam*d1*k1
    assert equal(compressed,lam*(d0*sp.eye(2)+(d1-d0)*e))
    print("fine archive is readable; sharp measurement and coherent passive test differ")


if __name__=="__main__":
    expanded_reset()
    archive_word()
    deterministic()
    no_inverse()
    distinguish_measurements()
