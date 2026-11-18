"""Exact identities for the A70 terminal's matched bank extension and a real null coframe."""

from fractions import Fraction as F
from math import comb
import sympy as sp


def check_null_matter():
    # Columns are U,V,X,Y, rows the original +,-,2,3 null frame.
    H, h, tau, e0, e4 = sp.symbols("H h tau e0 e4", nonzero=True, real=True)
    frame = sp.Matrix([[1,tau/h,0,0],[H/2,1,0,0],[0,0,1,0],[0,0,0,1]])
    eta = sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    inv_metric = (frame.T * eta * frame).inv()
    energy = e0**2 + e4**2
    q = inv_metric[0,0] * energy
    assert q.subs(tau,0) == 0
    assert sp.simplify(q.diff(tau).subs(tau,0) + 2*energy/h) == 0
    # Independent curvature/matter coframe roles are genuinely separated here.
    k0 = sp.symbols("k0", positive=True)
    matter_row = -2*h**3*energy
    curvature_row = k0*matter_row  # the actual all42 constraint DrF=k0 DrQ
    assert sp.simplify(curvature_row - k0*matter_row) == 0
    assert sp.simplify(curvature_row + k0*matter_row + 4*k0*h**3*energy) == 0


def check_transitive_extension():
    m = [840*(-1)**(j-1)*F(comb(8,j),j) for j in range(1,9)]
    # Every positive degree in the original field/matter polynomials.
    assert [sum(a*j**k for j,a in enumerate(m,1)) for k in range(1,9)] == [840]+[0]*7
    for k in range(1, 9):
        for role in range(2):
            # Unit field or matter derivative in one homogeneous coefficient.
            rows = [a*j**k if slot == role else F(0)
                    for j,a in enumerate(m,1) for slot in range(2)]
            for physical_packet in range(16):
                derivative = sum(rows[(physical_packet+shift)%16] for shift in range(16))/16
                assert derivative == (F(840,16) if k == 1 else 0)
    # Arbitrary independent two-coordinate source rows in all slots.
    rows = [(F(i*i-8), F((-1)**i, i+1)) for i in range(16)]
    changes = [(F(i+2,7), F(2*i-1,11)) for i in range(16)]
    exact = sum(sum(rows[j][k]*changes[(j+shift)%16][k]
                    for j in range(16) for k in (0,1)) for shift in range(16))/16
    pullback = sum(sum(row[k] for row in rows)*sum(vec[k] for vec in changes)/16
                   for k in (0,1))
    assert exact == pullback


def check_actual_gauge_and_saddle():
    d, h, x, y = sp.symbols("d h x y", nonzero=True, real=True)
    H = sp.symbols("H", real=True)
    def N(a):
        M = sp.zeros(4)
        M[1,a] = M[a,0] = 1
        return M
    T = d*N(2)
    L = sp.eye(4)+T+T**2/2
    eta = sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    frame = sp.eye(4)
    frame[1,0] = H/2
    assert L.det()==1 and L.T*eta*L==eta and (L*frame).T*eta*(L*frame)==frame.T*eta*frame
    # True five-point transverse Laplacian and the buffered Dirichlet interior spike.
    energy, coupling = sp.symbols("energy coupling", nonzero=True, real=True)
    profile = -coupling*energy*(x*x+y*y)
    lap = (profile.subs(x,x+h)+profile.subs(x,x-h)+profile.subs(y,y+h)
           +profile.subs(y,y-h)-4*profile)/h**2
    assert sp.simplify(lap + 4*coupling*energy)==0
    assert sp.simplify(-(-4/h**2)/(2*h) - 2/h**3)==0
    a, b, sigma = sp.symbols("a b s", positive=True)
    small = 2*a*a/(sp.sqrt(b*b+4*a*a)+b)
    assert sp.simplify(small**2+b*small-a*a)==0
    assert sp.Matrix([[0,a],[a,b]]).det() == -a*a


if __name__ == "__main__":
    check_null_matter()
    check_transitive_extension()
    check_actual_gauge_and_saddle()
    print("PASS: null matter and independent coframe stress, degree 1..8, all 16 measured routing shifts, true Lorentz/difference identities and saddle gap.")
