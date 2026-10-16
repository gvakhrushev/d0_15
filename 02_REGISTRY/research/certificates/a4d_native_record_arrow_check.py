#!/usr/bin/env python3
"""Exact support-to-record arrow and positive detector controls.

The analytic proof is in A4D_NATIVE_FINITE_PROBE_COMPLETION.md, Sections 13-15.
Default execution replays the immutable results; --output explicitly writes.
"""
from fractions import Fraction as F
from itertools import product
import json
import argparse
from pathlib import Path
import sympy as s

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
parser.add_argument('--expect',type=Path,default=Path(__file__).with_name(
    'a4d_native_record_arrow_results.json'))
args=parser.parse_args()

z,w,p=s.symbols('z w p',real=True)
D=lambda x:s.diag(1,x+1,x-1,0)
R=lambda x:D(x)*D(x)
delta=z-w
target=s.diag(0,delta*(z+w+2),delta*(z+w-2),0)
assert s.simplify(R(z)-R(w)-target)==s.zeros(4)
assert s.factor(s.trace(target*target)-delta**2*(2*(z+w)**2+8))==0
T=lambda x:3+2*x*x
P=lambda x:R(x)/T(x)
decoder=lambda x:(P(x)[1,1]-P(x)[2,2])/(4*P(x)[0,0])
assert s.simplify(decoder(z)-z)==0
inverse_identity=(P(z)[1,1]-P(w)[1,1]
                  -P(z)[2,2]+P(w)[2,2]
                  -4*w*(P(z)[0,0]-P(w)[0,0]))
assert s.simplify(inverse_identity-4*delta*P(z)[0,0])==0

norm_controls=[]
for zz in (F(-7,3),F(-2),F(-1),F(0),F(1),F(2),F(11,7)):
    for ww in (F(-4),F(-1,2),F(0),F(3,5),F(4)):
        norm=max(abs((zz-ww)*(zz+ww+2)),abs((zz-ww)*(zz+ww-2)))
        assert norm==abs(zz-ww)*(abs(zz+ww)+2)
        assert norm>=2*abs(zz-ww)
        probs=lambda q:[F(1,T(q)),(q+1)**2/T(q),(q-1)**2/T(q),F(0)]
        aa,bb=probs(zz),probs(ww)
        Z=max(abs(zz),abs(ww)); l1=sum(abs(a-b) for a,b in zip(aa,bb))
        assert abs(zz-ww)<=T(Z)*max(F(1,4),Z)*l1
        norm_controls.append([str(zz),str(ww),str(norm)])

prefix_controls=[]
for B in (([F(0)],[F(-1),F(1)],[F(2)]),
          ([F(-3),F(-2)],[F(0),F(1)],[F(4),F(5)])):
    rho=lambda bits:tuple(B[i][0 if not bit else -1] for i,bit in enumerate(bits[2:]))
    for k in range(1,len(B)+1):
        image={rho(bits) for bits in product((False,True),repeat=k+2)}
        assert image==set(product(*B[:k]))
        for bits in product((False,True),repeat=k+2):
            assert rho(bits)[:-1]==rho(bits[:-1])
        prefix_controls.append({'record_level':k,'support_level':k+2,
                                'binary_count':2**(k+2),'image_count':len(image)})

relation=s.groebner([p*p+p-1],p)

def reduce_matrix(matrix):
    def reduce_entry(entry):
        terms=s.Poly(s.expand(entry),z,w).terms()
        return s.expand(sum(relation.reduce(coef)[1]*z**powers[0]*w**powers[1]
                            for powers,coef in terms))
    return matrix.applyfunc(reduce_entry)

# The state word selects z,w; matrix addresses remain independent variables.
# This replays n=3 -> n=4, including the two-letter initialization.
J=lambda m:s.kronecker_product(s.eye(m),s.Matrix([1,1]))
Pfx=lambda m:s.kronecker_product(s.eye(m),s.Matrix([[p,p*p]]))
W=lambda m:s.kronecker_product(s.eye(m),s.Matrix([p,-1]))
Wdag=lambda m:s.kronecker_product(s.eye(m),s.Matrix([[p*p,-p*p]]))
D3=p*(1+p)*W(4)*D(z)*Wdag(4)
E3=s.diag(1,w+1,w-1,0,0,0,0,0)
D4=J(8)*D3*Pfx(8)+p*p*(1+p)*W(8)*E3*Wdag(8)
assert reduce_matrix(Pfx(8)*D4-D3*Pfx(8))==s.zeros(8,16)
assert reduce_matrix(Pfx(8)*(D4*D4)*J(8)-D3*D3)==s.zeros(8)

for N in range(1,7):
    finite=sum(p**(2*j) for j in range(1,N+1))
    assert relation.reduce(s.expand((1-p*p)*finite-p*p*(1-p**(2*N))))[1]==0

out={'verdict':'PASS','scope':'finite identities and hostile controls; proof in A4D_NATIVE_FINITE_PROBE_COMPLETION.md, Sections 13-15',
     'generic_response_difference':str(target),
     'generic_HS_square':'(z-w)^2*(2*(z+w)^2+8)',
     'response_separation':'operator norm >= 2*abs(z-w)',
     'attenuated_record_separation':'operator norm >= 2*p^(2j)*abs(delta z_j)',
     'depth_uniform_inverse':False,
     'rational_norm_controls':norm_controls,'prefix_controls':prefix_controls,
     'shifted_pulled_back_operator_scalar_identities':128+64,
     'golden_geometric_controls':6}
if args.output:
    args.output.write_text(json.dumps(out,indent=2)+'\n')
else:
    assert json.loads(args.expect.read_text())==out,'Pinned artifact mismatch'
print(json.dumps({'verdict':'PASS','norm_controls':len(norm_controls),
                 'prefix_controls':len(prefix_controls),'geometric_controls':6}))
