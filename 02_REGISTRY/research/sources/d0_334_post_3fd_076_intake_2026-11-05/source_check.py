"""Exact Golden-field target algebra for the literal final CX reader.

The final reader is one actual native CX. F is the owned smooth XF target;
the check does not assert that every F has an exact finite positive word.
All predicates remain active with python -O.
"""
import json
import sympy as s

a = s.Symbol('a', real=True)
p = a*a
minimal = s.Poly(a**4+a*a-1, a, domain=s.QQ)
checks = []

def red(x):
    return s.rem(s.Poly(s.expand(x), a, domain=s.QQ), minimal).as_expr()

def matred(m):
    return m.applyfunc(red)

def zero(x, label):
    good = all(red(t) == 0 for t in x) if isinstance(x, s.MatrixBase) else red(x) == 0
    if not good:
        raise RuntimeError(label)
    checks.append(label)

I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
P0 = s.diag(1, 0)
P1 = s.diag(0, 1)
G = s.Matrix([[a, -p], [p, a]])
v = s.Matrix([a, p])
Pb = matred(v*v.T)
E = P1
ce = s.kronecker_product(E, I)+s.kronecker_product(I-E, X)
cp = s.kronecker_product(Pb, I)+s.kronecker_product(I-Pb, X)
F = matred(ce*cp)
CX = s.kronecker_product(P0, I)+s.kronecker_product(P1, X)
reader = s.kronecker_product(I, CX)
U = matred(reader*s.kronecker_product(F, I))
V = s.kronecker_product(U, I)  # last spectator t, retained in full
born = s.kronecker_product(v, v, v, v)
out = matred(V*born)
Q = red((v.T*E*v)[0])
q = red(p*p+p**4-p**6*Q)
flag_event = s.kronecker_product(I, P1, I, I)
pointer_event = s.kronecker_product(I, I, P1, I)

zero(G.T*G-I, 'Golden G is orthogonal on the actual field')
zero((v.T*v)[0]-1, 'canonical birth is normalized')
zero((v.T*G*v)[0]-a, 'actual Golden cold amplitude is a')
zero(CX.T*CX-s.eye(4), 'literal final CX is all-column orthogonal')
zero(F.T*F-s.eye(4), 'full XF target is orthogonal')
zero(U.T*U-s.eye(8), 'complete read target is all-column orthogonal')
zero(V.T*V-s.eye(16), 'last spectator and every target column retained')
zero(red(F.det())-1, 'fixture XF determinant is plus one')
zero(CX.det()+1, 'local two-bit CX determinant is minus one')
zero(CX.det()**4-1, 'even bank and spectator multiplicity give SO target')
zero((out.T*out)[0]-1, 'complete initialized output is normalized')

partial_trace_reader = s.Matrix([[sum(CX[2*i+r, 2*j+r] for r in range(2))
                                  for j in range(2)] for i in range(2)])
zero(partial_trace_reader-2*P0, 'reader partial trace is exactly two P0')
zero(s.trace(U)-s.trace(F), 'complete newest-detail trace unchanged by paid CX read')
zero(s.trace(V)-2*s.trace(F), 'full spectator trace multiplicity retained')
zero((out.T*flag_event*out)[0]-(p-p**3*Q), 'flag probability is unchanged by pointer read')
zero((out.T*pointer_event*out)[0]-q, 'actual pointer law p2 plus p4 minus p6 Q')
zero(q-((1+p**6)/2-p**6*Q), 'pointer law has symmetric interval about one half')
zero(q-(p*p+p**3*(p-p**3*Q)), 'literal noisy-channel composition has gain p3')

cold = red((born.T*out)[0])
cold_formula = a*p+2*p**3+p**4*(1-a)*Q
zero(cold-cold_formula, 'original born cold corner after the literal reader')
zero(cold_formula-(a*p+2*p**3+(p+2*a*p**3-a*p-2*p**3)*Q),
     'both stated cold formulas agree')

# Original projection varies by a genuine real orthogonal conjugation.
generator = s.Matrix([[0, -1], [1, 0]])
dE = generator*E-E*generator
dQ = red((v.T*dE*v)[0])
dce = s.kronecker_product(dE, I-X)
dF = matred(dce*cp)
dU = matred(reader*s.kronecker_product(dF, I))
dV = s.kronecker_product(dU, I)
dout = matred(dV*born)
zero(s.trace(dF)-4*dQ, 'XF full trace source is four DQ')
zero(s.trace(dU)-4*dQ, 'paid reader retains the full trace source')
zero(2*(out.T*pointer_event*dout)[0]+p**6*dQ,
     'full pointer derivative is minus p6 DQ')
zero((born.T*dout)[0]-p**4*(1-a)*dQ,
     'full cold derivative retains its true coefficient')
if dQ == 0:
    raise RuntimeError('nonzero source fixture')
checks.append('nonzero original-projection tangent in the same fixture')

# Hostile controls: no perfect copy is alleged; omitted read and unretained
# full state cannot be silently identified with the new pointer.
if red(q-(p-p**3*Q)) == 0:
    raise RuntimeError('noisy pointer differs from original flag')
checks.append('negative control: pointer is noisy and differs from original flag')
for bit, proj in enumerate((s.eye(16)-pointer_event, pointer_event)):
    branch = matred(proj*out)
    weight = red((branch.T*branch)[0])
    zero(weight-(1-q if bit == 0 else q), f'full branch {bit} has correct weight')
    rho = matred(branch*branch.T)
    zero(rho*rho-weight*rho, f'full retained branch {bit} is rank-one before normalization')

rho_coherent = matred(out*out.T)
rho_pinched = matred(pointer_event*rho_coherent*pointer_event
                    +(s.eye(16)-pointer_event)*rho_coherent*(s.eye(16)-pointer_event))
prelast = matred(s.kronecker_product(F, I, I)*born)
g_last = s.kronecker_product(reader, I)
zero(g_last*(prelast*prelast.T)*g_last.T-rho_coherent,
     'output predicate is the original generated cut transported by the real last CX')
zero(s.trace(rho_coherent*rho_coherent)-1,
     'coherent output has unit expectation in its generated predicate')
zero(s.trace(rho_coherent*rho_pinched)-(q*q+(1-q)**2),
     'pinched output has the exact nonunit proper-cut expectation')
if red(1-s.trace(rho_coherent*rho_pinched)) == 0:
    raise RuntimeError('proper-cut distinction was erased')
checks.append('negative control: full generated predicate distinguishes coherent and CQ states')

payload = {
    'scope': 'Exact Golden target/readout algebra; last reader is a literal CX; compilation and complete-price selection are separate.',
    'field': 'QQ[a]/(a^4+a^2-1), positive real root a=sqrt(phi^-1)',
    'checks': checks,
    'check_count': len(checks),
    'fixture_Q': str(Q),
    'fixture_DQ': str(dQ),
    'fixture_pointer_probability': str(q),
    'fixture_cold': str(cold),
    'full_target_dimension': 16,
    'literal_final_reader_calls': 1,
    'full_Cost_Info_selected': False,
    'GR_closed': False,
}
print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
