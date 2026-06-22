#!/usr/bin/env python3
"""verify_unified_backbone.py - verify D0-v15 unified spine backbone (§2,§3,§6,§7,§11) from source.
Builds operators from combinatorial Q8/graph data; checks each claimed identity exactly (SymPy).
"""
import sympy as sp
import sys
sys.stdout.reconfigure(encoding="utf-8")
ok = True
def check(name, cond):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    ok = ok and bool(cond)

z, lam = sp.symbols('z lambda')

print("== §2.1 raw constant-part quotient ==")
# symmetric divisor (part-size weighted): off-diag sqrt(n_i n_j)
n = [9, 11, 13]
Aw = sp.Matrix([[0, sp.sqrt(99), sp.sqrt(117)],
                [sp.sqrt(99), 0, sp.sqrt(143)],
                [sp.sqrt(117), sp.sqrt(143), 0]])
x = sp.symbols('x')
chi = sp.expand(Aw.charpoly(x).as_expr())
check("chi_{A|W} = x^3 - 359 x - 2574", sp.simplify(chi - (x**3 - 359*x - 2574)) == 0)

print("== §2.2 zone current ==")
Dw = sp.diag(24, 22, 20)
J = sp.I*(Dw*Aw - Aw*Dw)
chiJ = sp.expand(J.charpoly(x).as_expr())
# expect x*(x^2 - Lambda^2) = x^3 - Lambda^2 x ; read Lambda^2 = -coeff of x
Lam2 = -chiJ.coeff(x, 1)
check("chi_J = x^3 - Lambda^2 x (no x^2, no const)", chiJ.coeff(x,2)==0 and chiJ.coeff(x,0)==0)
check("Lambda^2 = 2840", sp.simplify(Lam2 - 2840) == 0)

print("== §3 Q8 Fourier projectors ==")
# Q8 elements ordered: 1,i,j,k,-1,-i,-j,-k  (indices 0..7)
els = ['1','i','j','k','-1','-i','-j','-k']
# multiplication table for quaternion group
def mul(a, b):
    # represent as (sign, unit) unit in {1,i,j,k}
    def parse(s): return (-1,s[1:]) if s.startswith('-') else (1,s)
    sa,ua = parse(a); sb,ub = parse(b); s=sa*sb
    if ua=='1': return fmt(s,ub)
    if ub=='1': return fmt(s,ua)
    table={('i','i'):(-1,'1'),('j','j'):(-1,'1'),('k','k'):(-1,'1'),
           ('i','j'):(1,'k'),('j','k'):(1,'i'),('k','i'):(1,'j'),
           ('j','i'):(-1,'k'),('k','j'):(-1,'i'),('i','k'):(-1,'j')}
    s2,u=table[(ua,ub)]; return fmt(s*s2,u)
def fmt(s,u):
    return ('' if s==1 else '-')+u if u!='1' else ('1' if s==1 else '-1')
idx={e:i for i,e in enumerate(els)}
def Lq(q):
    M=sp.zeros(8,8)
    for r in range(8):
        M[idx[mul(q,els[r])], r] = 1
    return M
I8=sp.eye(8)
E0=sp.Rational(1,8)*sum((Lq(q) for q in els), sp.zeros(8,8))
E4=sp.Rational(1,2)*(I8-Lq('-1'))
E3=sp.Rational(1,2)*(I8+Lq('-1'))-E0
check("E0 idempotent", sp.simplify(E0*E0-E0)==sp.zeros(8,8))
check("E4 idempotent", sp.simplify(E4*E4-E4)==sp.zeros(8,8))
check("E3 idempotent", sp.simplify(E3*E3-E3)==sp.zeros(8,8))
check("E0+E3+E4 = I", sp.simplify(E0+E3+E4-I8)==sp.zeros(8,8))
check("E0 E3 = 0", sp.simplify(E0*E3)==sp.zeros(8,8))
check("E0 E4 = 0", sp.simplify(E0*E4)==sp.zeros(8,8))
check("E3 E4 = 0", sp.simplify(E3*E4)==sp.zeros(8,8))
check("ranks (E0,E4,E3) = (1,4,3)", (E0.rank(),E4.rank(),E3.rank())==(1,4,3))

print("== §6 terminal return + holonomy det ==")
# C4(lambda): 4-cycle with holonomy: C4^4 = lambda I ; build as companion-like
w4=sp.exp(2*sp.pi*sp.I/4)
# use diagonal eigenform: eigenvalues lambda^{1/4} * i^r ; det(I - z C4) = 1 - lambda z^4
# verify via cyclic matrix C4 = shift with corner = lambda
C4=sp.zeros(4,4)
for r in range(3): C4[r+1,r]=1
C4[0,3]=lam
check("C4^4 = lambda I", sp.simplify(C4**4-lam*sp.eye(4))==sp.zeros(4,4))
detU4=sp.simplify((sp.eye(4)-z*C4).det())
check("det(I - z C4) = 1 - lambda z^4", sp.simplify(detU4-(1-lam*z**4))==0)
C3=sp.zeros(3,3)
for r in range(2): C3[r+1,r]=1
C3[0,2]=lam
check("C3^3 = lambda I", sp.simplify(C3**3-lam*sp.eye(3))==sp.zeros(3,3))
detU3=sp.simplify((sp.eye(3)-z*C3).det())
check("det(I - z C3) = 1 - lambda z^3", sp.simplify(detU3-(1-lam*z**3))==0)
detUterm=sp.simplify((1-z)*detU4*detU3)
check("det(I - z U_term) = (1-z)(1-lam z^4)(1-lam z^3)",
      sp.simplify(detUterm-(1-z)*(1-lam*z**4)*(1-lam*z**3))==0)

print("== §7 bare lepton Green kernel (block traces) ==")
# G block = (1/rank) tr (I - z U_block)^{-1}  must equal 1/(1-lam z^d) for cyclic, 1/(1-z) for trivial
def block_green(C, d):
    R=(sp.eye(d)-z*C).inv()
    return sp.simplify(sp.Rational(1,d)*sp.trace(R))
g_e = sp.simplify(sp.Rational(1,1)*sp.trace((sp.eye(1)-z*sp.eye(1)).inv()))
check("G_e = 1/(1-z)", sp.simplify(g_e-1/(1-z))==0)
g_mu=block_green(C4,4)
check("G_mu = 1/(1-lam z^4)", sp.simplify(g_mu-1/(1-lam*z**4))==0)
g_tau=block_green(C3,3)
check("G_tau = 1/(1-lam z^3)", sp.simplify(g_tau-1/(1-lam*z**3))==0)

print("== §11 Fibonacci / Pisot replication ==")
phi=(1+sp.sqrt(5))/2; psi=-1/phi
nn=sp.symbols('n', integer=True)
def F(k): return sp.fibonacci(k)
A1=sp.symbols('A1')
# A_{n+1}-phi A_n = psi^n A_1  (A_n = F_n A_1)
lhs=sp.simplify((F(7)-phi*F(6)))
check("F_{n+1}-phi F_n = psi^n  (n=6)", sp.simplify(lhs-psi**6)==0)
check("|psi|<1 (Pisot decay)", sp.simplify(sp.Abs(psi))<1)
check("A_{n+1}=A_n+A_{n-1} (Fibonacci, n=6)", F(7)==F(6)+F(5))

print()
# negative control: a deliberately-wrong identity must be rejected (proves the checker can fail)
assert not (sp.simplify(Lam2 - 9999) == 0), "negative control breached: Lambda^2 should be 2840, not 9999"
# guillotine: the whole certificate fails (non-zero exit) if any checked identity did not hold
assert ok, "RESULT: SOME FAIL — a claimed identity did not hold"
print("RESULT:", "ALL PASS")
sys.exit(0)
