#!/usr/bin/env python3
"""Golden native cost-cut source/pressure/terminal rigidity, exact bounded replay.

This is a finite algebraic consumer of the original two-state Fibonacci
cost-cut kernel. It does NOT physically select Book03 Info or the D0 clock.
The companion theorem proves the all-depth statements analytically.
"""
from __future__ import annotations
import sympy as s


def require(cond, name):
    if not bool(cond):
        raise RuntimeError("FAILED: " + name)


def zero(expr, name):
    require(s.simplify(expr) == 0, name)


def matrix_zero(M, name):
    require(all(s.simplify(t) == 0 for t in M), name)


p = (s.sqrt(5) - 1) / 2
ell = s.log((1 + s.sqrt(5)) / 2)
u, q, y, z = s.symbols('u q y z', real=True)
lam = s.Symbol('lambda')
K = s.Matrix([[p, p**2], [1, 0]])
Kq = s.Matrix([[q, 1 - q], [1, 0]])
Du = s.diag(1, s.exp(-u))
Kt = s.Matrix([[q*s.exp(-u), (1-q)*s.exp(-2*u)], [1, 0]])

zero(p**2+p-1, 'native Golden identity')
matrix_zero(Kt - s.exp(-u)*Du.inv()*Kq*Du, 'exact cost coboundary similarity')
zero(s.factor(Kq.charpoly(lam).as_expr()) - (lam-1)*(lam+1-q),
     'biased stochastic eigenvalues')
zero(s.factor(Kt.charpoly(lam).as_expr()) -
     (lam-s.exp(-u))*(lam+(1-q)*s.exp(-u)),
     'tilted Golden cost spectral radius')

pi1 = (1-q)/(2-q)
pi0 = 1/(2-q)
Pi = s.Matrix([[pi0, pi1], [pi0, pi1]])
Q = s.eye(2)-Pi
matrix_zero(Kq*Pi-Pi, 'stationary Perron rank-one projection')
matrix_zero(Kq*Q-(q-1)*Q, 'exact decaying two-state endpoint mode')

state0 = s.Matrix([[1, 0]])
ones = s.ones(2, 1)
for n in range(1, 17):
    beta = s.factor(pi1*(1-(q-1)**n))
    Zn = s.exp(-u*n)*(1-beta+beta*s.exp(-u))
    if n <= 8:
        # Entire genuine path law, including pending 1 and all failures.
        Z_mat = (state0*(Kt**n)*ones)[0]
        zero(Z_mat-Zn, 'all native state words marked n='+str(n))
        matrix_zero(Kq**n-(Pi+(q-1)**n*Q),
                    'closed exact Markov powers n='+str(n))
    native_beta = s.fibonacci(n)*p**(n+1)
    zero(beta.subs(q,p)-native_beta,
         'original exact Fibonacci overshoot n='+str(n))
    # Exact whole-code first-cost and cumulant on ALL leaves.
    mean = n+beta
    zero(-s.diff(s.log(Zn),u).subs(u,0)-mean,
         'full cost first mark n='+str(n))
    zero(s.diff(s.log(Zn),u,2).subs(u,0)-beta*(1-beta),
         'full cost second mark n='+str(n))

# End-state perturbations cannot be an unbounded invisible uniform future.
A, B, k = s.symbols('A B k', real=True)
h = s.Matrix([A, B])
center = (s.Matrix([[pi0,pi1]])*h)[0]
for j in range(0, 12):
    matrix_zero(Kq**j*h-(center*ones+(q-1)**j*(h-center*ones)),
                'exact center and endpoint residual j='+str(j))

# Full complete original q-dependent probability vs ORIGINAL native p^cost
# is a genuine KL of chronological Markov records, not a physical Book law.
d = (q*s.log(q/p)+(1-q)*s.log((1-q)/p**2))/ell
zero(d.subs(q,p), 'native KL reference value')
zero(s.diff(d,q).subs(q,p), 'native KL reference first source')
zero(s.diff(d,q,2).subs(q,p)-1/(ell*p**3),
     'exact one-branch Fisher curvature')
for n in range(1, 13):
    v = n*pi0 + (1-q)/(2-q)**2*(1-(q-1)**n)
    visits = sum((state0*Kq**j)[0] for j in range(n))
    zero(visits-v, 'full native branch occupancy n='+str(n))
    zero(s.diff(v*d,q).subs(q,p), 'whole history KL has zero first jet n='+str(n))
    zero(s.diff(v*d,q,2).subs(q,p)-v.subs(q,p)/(ell*p**3),
         'whole history native Fisher curvature n='+str(n))

# SHARP source/refinement countercontrol: analytically valid entire
# two-state no-11 stochastic history tower; native Golden q=p at y=0
# for EVERY stage, but source of intensive marked COST does not converge.
eps = s.Rational(1,100)
beta_nat = lambda j: s.Integer(0) if j == 0 else s.fibonacci(j)*p**(j+1)
beta_move = lambda j: beta_nat(j)+eps*s.sin(j*y)
# Uniform positivity proof: for j>=1, 0.23<beta_nat(j)<0.39;
# eps=0.01, so all moving beta in (0.22,0.40), and adjacent sums <0.80.
for j in range(0, 16):
    t_j = s.factor(beta_move(j+1)/(1-beta_move(j)))
    zero(t_j.subs(y,0)-p**2,
         'all stage kernels identical to native Golden at y=0 j='+str(j))
    if j >= 1:
        zero(beta_move(j).subs(y,0)-beta_nat(j),
             'native base law is original at all stages')
    if j >= 1:
        zero(s.diff((j+beta_move(j))/j, y).subs(y,0)-eps,
             'noncommuting continuum cost first source n='+str(j))
    # Entire mark pressure has universal C0 limit -u, but its field
    # source need not approach the source of that limiting value.
    if j >= 1:
        Zj = s.exp(-u*j)*(1+beta_move(j)*(s.exp(-u)-1))
        field_pressure_source = s.diff(s.log(Zj)/j, y).subs(y,0)
        prescribed = eps*(s.exp(-u)-1)/(1+beta_nat(j)*(s.exp(-u)-1))
        zero(field_pressure_source-prescribed,
             'nonuniform C1 marked pressure n='+str(j))

# Genuine native bounded two-state scalar/linear-vector martingale:
# delta_n=(q-1)^k delta_(n+k). With |q-1|<1 and uniform terminal
# bound all endpoint differences vanish. Exact test of the algebraic step:
h0,h1 = s.symbols('h0 h1')
H = s.Matrix([h0,h1])
zero((Kq*H)[0]-(Kq*H)[1]-(q-1)*(h0-h1),
     'endpoint difference contracts exactly')

print('PASS original Golden cost n + terminal bit and full marked polynomial')
print('PASS exact tilted stochastic similarity; bulk cost eigenvalue exp(-u)')
print('PASS Markov endpoint harmonic rigidity and exact finite-depth contraction')
print('PASS exact full finite-KL occupancy and zero native source / PSD Fisher')
print('PASS source/refinement hostile: same native base, C0 but not C1')
print('physical Book03 selected: FALSE; GR_closed: FALSE')
