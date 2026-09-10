"""Exact complex-density and repeated internal-record controls, using SymPy."""
import json
from pathlib import Path
import sympy as s

a, p = s.symbols('a p', real=True)
x, y, z = s.symbols('x y z', real=True)
gb = s.groebner([a*a-p, p*p+p-1], a, p, domain=s.QQ)
checks = 0
def reduce(expr):
    return s.expand(gb.reduce(s.expand(expr))[1])
def zero(expr):
    global checks
    # Coefficients may involve external Bloch variables and i.
    poly = s.Poly(s.expand(expr), x, y, z)
    assert all(reduce(s.re(c)) == 0 and reduce(s.im(c)) == 0 for c in poly.coeffs()), expr
    checks += 1
def matrix_zero(m):
    for e in m:
        zero(e)

I = s.eye(2)
X = s.Matrix([[0,1],[1,0]])
Y = s.Matrix([[0,-s.I],[s.I,0]])
Z = s.diag(1,-1)
G = s.Matrix([[a,-p],[p,a]])
W = s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
E = W[:,[0,2]]
c, t = p-p*p, 2*a*p
matrix_zero(W.T*W-s.eye(4))
matrix_zero(E.T*E-I)
matrix_zero(E.T*s.kronecker_product(Z,I)*E-(c*Z-t*X))
matrix_zero(E.T*s.kronecker_product(X,X)*E-(t*Z+c*X))
matrix_zero(E.T*s.kronecker_product(Y,X)*E-Y)
# The local phase readouts vanish after recording, but the joint phase does not.
matrix_zero(E.T*s.kronecker_product(X,I)*E)
matrix_zero(E.T*s.kronecker_product(Y,I)*E)
rho = (I+x*X+y*Y+z*Z)/2
joint = E*rho*E.T
matrix_zero(E.T*joint*E-rho)
local = s.Matrix(2,2,lambda i,j: sum(joint[2*i+r,2*j+r] for r in range(2)))
matrix_zero(local-(I+(c*z-t*x)*Z)/2)
zero((c*z-t*x)**2+(t*z+c*x)**2+y*y-x*x-y*y-z*z)

# Opposite input Z states, evolved coherently with a NEW retained blank at each step.
# No trace/discard is used to generate the global states. A local readout alone contracts.
V = I
steps = []
for n in range(1,6):
    old_mem = V.rows//2
    new_mem = 2*old_mem
    next_V = s.zeros(2*new_mem,2)
    for src in range(2):
        for old_sys in range(2):
            for mem in range(old_mem):
                for new_sys in range(2):
                    row = new_sys*new_mem+2*mem+new_sys
                    next_V[row,src] += G[new_sys,old_sys]*V[old_sys*old_mem+mem,src]
    V = next_V.applyfunc(reduce)
    matrix_zero(V.T*V-I)
    probs = []
    for src in range(2):
        probs.append([reduce(sum(V[sys*new_mem+r,src]**2 for r in range(new_mem)))
                      for sys in range(2)])
        zero(probs[src][0]+probs[src][1]-1)
        zero(probs[src][0]-probs[src][1]-(-1)**src*c**n)
    # Global columns stay orthogonal: globally perfect distinguishability remains.
    steps.append(dict(steps=n, joint_dimension=V.rows,
                      global_orthogonal=True, local_contrast=f'(2 delta)^{n}'))

result = dict(status='PASS', exact_scalar_checks=checks, repeated_record_controls=steps,
              scope='Complex input, exact polynomial reduction, full retained archive; dimension is sufficient, not minimal')
Path(__file__).with_name('coherent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
