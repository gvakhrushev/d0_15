"""Exact complement design and complete finite return histories for unequal native banks."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

import numpy as np

SOURCE = Path(__file__).resolve().parents[4] / 'd0_native_execution_domain_2026-10-24'
sys.path.insert(0, str(SOURCE))
import native_execution as native

p, a = float(native.P), float(native.A)
G = np.array(native.G_LOCAL, dtype=float)


def mul(m, v):
    return np.einsum('ij,j...->i...', m, v)


def close(x, y):
    np.testing.assert_allclose(x, y, atol=3e-13, rtol=2e-12, equal_nan=False)


def native_banks():
    # Logical chart with canonical WORK conjugated by the paid G,G inverse.
    # Input copy emissions and inverse calls use the same four-address frame.
    cx01 = np.eye(4)[[0, 1, 3, 2]]
    cx10 = np.eye(4)[[0, 3, 2, 1]]
    ops = (np.kron(G, np.eye(2)), np.kron(np.eye(2), G), cx01, cx10)
    gate = native.Gate
    words = ((0,0,2,0,1,3), (0,0,0,1,1,1,3), (0,1,2,0,1,1,3))
    primitive = (gate("G",(0,)), gate("G",(1,)), gate("CX",(0,1)), gate("CX",(1,0)))
    z = np.diag([1,1,-1,-1])
    result = []
    for indices in words:
        ex = native.Execution(4,(),(),tuple(primitive[i] for i in indices),
                              profile=native.G_CX_SOURCE_I,source_port=0,source_spin=(2,3))
        native.validate_execution(ex,max_qubits=4,max_expanded_stages=7)
        u = np.eye(4)
        for i in indices:
            u = mul(ops[i],u)
        r = mul(u.T,mul(z,u))
        close(mul(r,r),np.eye(4))
        assert 0.24 < r[0,0] < 0.53
        result.append(r)
    return result


def complement_design():
    # Multiplication by a primitive element of GF(4) cycles nonzero words.
    shift = np.array([[0,0,1],[1,0,0],[0,1,0]], dtype=int)
    group = []
    for v in range(4):
        signs = np.diag([(-1)**(bin(v & x).count('1')) for x in (1,2,3)])
        mat = signs
        for _ in range(3):
            group.append(mat)
            mat = mul(shift,mat)
    for j,k in product(range(3),repeat=2):
        e = np.zeros((3,3),dtype=int)
        e[j,k]=1
        total = sum(mul(g,mul(e,g.T)) for g in group)
        assert np.array_equal(total, (4 if j==k else 0)*np.eye(3,dtype=int))
    return group


def guard(k, l):
    # Rotate the two nonzero edges 01--11 and 10--11. These are the exact
    # single-pattern Walsh rotations of angle 2*K*theta (fixed zero address).
    def edge(x, y, power):
        rotation = np.linalg.matrix_power(G, 2*power)
        out = np.eye(3)
        out[np.ix_([x,y],[x,y])] = rotation
        return out
    return mul(edge(0,2,k),edge(1,2,l))


def tree(banks, group, guards, ell, tail, theta):
    total = 0.
    margin = 1.
    def visit(stage, initial, mass):
        nonlocal total, margin
        after = mul(banks[stage],initial)
        yes = after[0]**2
        no = sum(after[1:]**2)
        margin = min(margin,yes,no)
        assert yes>1e-13 and no>1e-13
        # Occupied success = I, final overflow/selection rejection = 0.
        total += mass*(ell + tail*yes)
        if stage == len(banks)-1:
            return
        failed = after[1:]/np.sqrt(no)
        for g in group:
            aligned = mul(guards[stage],mul(g,failed))
            visit(stage+1, np.r_[0., aligned], mass*ell*theta/len(group))
    visit(0,np.array([1.,0.,0.,0.]),1.)
    return total, margin


def closed(banks, ell, tail, theta, d):
    w = ell*theta
    s = sum(w**j for j in range(1,len(banks)))
    cs = [r[0,0]**2 for r in banks]
    return ell*(1+s)+tail*(cs[0]+sum(w**j*(1-cs[j])/d for j in range(1,len(banks))))


def verify():
    banks = native_banks()
    group = complement_design()
    guards = [guard(1,2),guard(2,3)]
    n=3
    # A single geometric selector attempt: twelve distinct pairs of four-bit
    # Golden index strings 01/10. Each has the same true/passive mass p^12.
    tail=p**(2*n)
    ell=p*p*(1-tail)
    one_attempt=12*p**12
    theta=1-(1-one_attempt)**15
    omega=ell*theta
    traces=[]
    margins=[]
    for j in range(3):
        ordered = banks[j:]+banks[:j]
        h, floor = tree(ordered,group,guards,ell,tail,theta)
        close(h,closed(ordered,ell,tail,theta,3))
        traces.append(h)
        margins.append(floor)
    s = omega+omega**2
    xs=np.array([r[0,0]**2 for r in banks])
    mean=ell*(1+s)+tail*(s/3+(1-s/3)*np.mean(xs))
    close(np.mean(traces),mean)
    # Exact inversion for arbitrary independently assigned layers, including unequal centres.
    w=F(7,20)
    identity=np.eye(3,dtype=int)
    shift=np.roll(identity,1,axis=0)
    from sympy import Matrix, Rational, eye
    sh=Matrix(shift.tolist())
    weight=Rational(w.numerator,w.denominator)
    frame=eye(3)-(weight*sh+weight**2*sh**2)/3
    inv=frame.inv()
    assert all(v>=0 for v in inv) and all(sum(inv.row(j))==1/(1-(weight+weight**2)/3) for j in range(3))
    # Vary only the last full geometric bank using a moving native target,
    # rotating the leakage direction in addition to changing its return.
    def perturbed(v):
        c,sn=np.cos(v),np.sin(v)
        u=np.eye(4)
        u[np.ix_([0,3],[0,3])]=[[c,-sn],[sn,c]]
        return banks[:2]+[mul(u.T,mul(banks[2],u))]
    e=1e-5
    values=[tree(perturbed(x),group,guards,ell,tail,theta)[0] for x in (e,-e)]
    dx=perturbed(e)[2][0,0]**2-perturbed(-e)[2][0,0]**2
    close(values[0]-values[1],-tail*omega**2*dx/3)
    # Without the design the old failure orientation contributes on unequal banks.
    bare=tree(banks,[np.eye(3)],[np.eye(3),np.eye(3)],ell,tail,theta)[0]
    assert abs(bare-closed(banks,ell,tail,theta,3))>1e-5
    print('exact GF(4) design on 9 matrix units; physical C =', [round(r[0,0],9) for r in banks])
    print('three cyclic RC3 histories match; minimum occupied probability %.8g' % min(margins))
    print('twirled h = %.12g; uncorrected range discrepancy %.8g' % (traces[0],bare-traces[0]))


if __name__=='__main__':
    verify()
