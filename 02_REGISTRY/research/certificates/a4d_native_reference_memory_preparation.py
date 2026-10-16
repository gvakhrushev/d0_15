#!/usr/bin/env python3
"""Exact existing-carrier reference/memory constructions, not an admission law.

The chronological gate, Fock basis and adjacent Jones frames are imported from
their existing owners. Endpoint transport is a conditional mathematical class.
The all-time faithful example is a state in the existing full16 representation;
its identification with self-conditioned native matter is not asserted.
"""
import importlib.util
from pathlib import Path
import sys

import sympy as s


def load(stem):
    path = Path(__file__).with_name(stem+'.py')
    spec = importlib.util.spec_from_file_location(stem,path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


C = load('a4d_native_record_metric_chronology_check')
J = load('a4d_native_jones_record_transport')
a,p,z = C.a,C.p,C.z
_ideal = s.groebner([a*a-p,p*p+p-1],a,p,domain=s.EX)


def red(value):
    num,den = s.cancel(value).as_numer_denom()
    num = _ideal.reduce(s.expand(num),auto=True)[1]
    den = _ideal.reduce(s.expand(den),auto=True)[1]
    assert den != 0,'ZERO_GOLDEN_DENOMINATOR'
    return s.cancel(num/den)


def mat(value):
    return value.applyfunc(red)


def literal_tuple():
    U = s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
    P = s.diag(1,1,0,0)
    blank = s.diag(1,0,1,0)
    T = s.Matrix([[1,0,1,0],[1,0,-1,0],[0,1,0,1],[0,1,0,-1]])/s.sqrt(2)
    return U,P,blank,T


def full_tuple():
    U,P,blank,T = literal_tuple()
    B = C.B0*s.kronecker_product(T.T,s.eye(4))
    return tuple(mat(B*s.kronecker_product(M,s.eye(4))*B.T)
                 for M in (U,P,blank))


def collision():
    basis = s.eye(16)
    A,B = basis[:,0]+basis[:,14],basis[:,1]+basis[:,15]
    u,v = -A/s.sqrt(2),B/s.sqrt(2)
    plus,minus = a*u+p*v,a*u-p*v
    Up,_ = C.record(s.eye(4),s.eye(4)[:,0])
    Um,_ = C.record(s.eye(4),-s.eye(4)[:,0])
    reflection = C.ext(s.diag(-1,1,1,1))
    return dict(u=u,v=v,plus=plus,minus=minus,Up=Up,Um=Um,reflection=reflection)


def jones_code(n):
    result = []
    for item in J.operators(n):
        entry = dict(item)
        G,F = item['G'],item['F']
        entry['Eu'] = mat((G+F)/(2*a))
        entry['Ev'] = mat((G-F)/(2*p))
        entry['code'] = entry['Eu'].row_join(entry['Ev'])
        result.append(entry)
    return result


def endpoint_frame(A):
    """Actual W-normalized full Fock frame, for positive determinant A."""
    omega = A.det()
    assert omega > 0
    B = C.ext(A)*C.B0
    W = omega*C.ext((A*A.T).inv())
    E = B/s.sqrt(omega)
    return E,W


def endpoint_adjoint(M,Wdomain,Wrange):
    return mat(Wdomain.inv()*M.T*Wrange)


def endpoint_tick(E1,W1,E0,W0,U):
    return mat(E1*U*endpoint_adjoint(E0,s.eye(E0.cols),W0))


def feedback(K,P0,PN,W0,WN):
    return mat(P0*endpoint_adjoint(K,W0,WN)*(s.eye(K.rows)-PN)*K*P0)


def chronological_determinant(c):
    lam,tr,det,tr0,det0 = C.polynomials(c)
    return (1-z*lam)**2*(1-z*tr+z*z*det)**2*(1-z*tr0+z*z*det0)


def golden_blank_matrix():
    """Literal apparatus rows, existing spectator columns; no extra tensor."""
    M = s.zeros(4)
    M[0,0],M[2,1] = a,p
    return M


def system_marginal(M):
    """Trace the old record bit and the existing four-dimensional spectator."""
    apparatus = mat(M*M.T)
    return mat(s.Matrix(2,2,lambda i,j:sum(apparatus[2*i+r,2*j+r]
                                        for r in range(2))))


def pauli_positive_pairing(sigma):
    """Real Pauli density -> normalized timelike observer positive Gram."""
    x = 2*sigma[0,1]
    y = sigma[0,0]-sigma[1,1]
    current = s.Matrix([1,x,0,y])
    eta = s.diag(1,-1,-1,-1)
    norm = (current.T*eta*current)[0]
    return mat(-eta+2*eta*current*current.T*eta/norm)


def golden_note_data():
    """Existing golden algebra, explicitly separated from physical dimension."""
    phi,psi,delta = 1+p,-p,(p-p*p)/2
    incidence = s.Matrix([[1,1],[1,0]])
    fixed_counts = [sum(value*value for value in incidence**r) for r in range(4)]
    return dict(phi=phi,psi=psi,delta=delta,incidence=incidence,
                fixed_counts=fixed_counts,
                Q={D:red(2*delta*phi**(D-1)) for D in range(1,6)})


if __name__ == '__main__':
    print('EXACT_REFERENCE_MEMORY_REPRESENTATION_NATIVE_SHARED_PREPARATION_OPEN')
