"""Exact all-period cubic obstruction on a physical resonance circle.

Literal shared-link jets in the Boolean group algebra retain arbitrary
sign sequences. A finite Laurent left witness kills every normal linear
correction and sends the cubic source to a nonzero shift of the signs.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
import argparse
import numpy as np
import a4d_identity_quarter_nonlinear_response_check as N
import a4d_identity_physical_resonance_circles_check as P
import a4d_identity_circle_even_inverse_check as E
from a4d_warped_designated_normal_rescue_check import interpolate, inverse

class BP:
    OFFSET=32
    def __init__(self,d=None): self.d={k:F(v) for k,v in (d or {}).items() if v}
    @classmethod
    def of(cls,v):return v if isinstance(v,cls) else cls({0:v})
    @classmethod
    def eps(cls,n):return cls({1 << (n+cls.OFFSET):1})
    def __bool__(self):return bool(self.d)
    def __neg__(self):return BP({k:-v for k,v in self.d.items()})
    def __add__(self,o):
        if not o:return self
        d=self.d.copy()
        for k,v in self.of(o).d.items():d[k]=d.get(k,F(0))+v
        return BP(d)
    __radd__=__add__
    def __sub__(self,o):return self+-self.of(o)
    def __rsub__(self,o):return self.of(o)+-self
    def __mul__(self,o):
        if not self or not o:return BP()
        d={}
        for k,v in self.d.items():
            for l,w in self.of(o).d.items():d[k^l]=d.get(k^l,F(0))+v*w
        return BP(d)
    __rmul__=__mul__
    def __truediv__(self,o):return self*(1/F(o))
    def shift(self,j):
        if j<0:assert all(not (k & ((1<<(-j))-1)) for k in self.d)
        return BP({(k<<j if j>=0 else k>>(-j)):v for k,v in self.d.items()})
    def entries(self):return [[list(i-self.OFFSET for i in range(k.bit_length()) if (k>>i)&1),str(v)] for k,v in sorted(self.d.items())]
    def value(self,signs):
        z=F(0)
        for k,v in self.d.items():
            for i in range(k.bit_length()):
                if (k>>i)&1:v*=signs[i-self.OFFSET]
            z+=v
        return z

ZERO=np.zeros((4,4),dtype=object)
TAU=(1,1,0,0)

@lru_cache(None)
def leading(n,q,r):
    if r in (2,3):return N.T[r]*(BP.eps(n)*(1,0,-1,0)[q%4])
    return N.G[0]*((BP.eps(n+1)-BP.eps(n))*(1,1,-1,-1)[q%4]/2)

def source(q,degree,correction=None,read_degree=None):
    read_degree=degree if read_degree is None else read_degree
    ek=np.zeros(24,dtype=object);eq=np.zeros(10,dtype=object)
    @lru_cache(None)
    def link(n,p,r):
        logs=N.jconst(ZERO,degree);logs[1]=leading(n,p,r)
        if correction is not None:
            logs[2]=sum((N.G[j]*BP.of(correction[p%4,6*r+j]).shift(n) for j in range(6)),ZERO.copy())
        return N.jexp(logs)
    for face,(r,s) in enumerate(N.PAIRS):
        roles=(r,s,r,s);invs=(False,False,True,True)
        offsets=((0,0),(TAU[r],1),(TAU[s],1),(0,0))
        bases=list(dict.fromkeys((-n,-p) for n,p in offsets))
        for bn,bp in bases:
            locs=[(bn+dn,q+bp+dp) for dn,dp in offsets]
            fac=[N.jinv(link(n,p,rr)) if inv else link(n,p,rr) for (n,p),rr,inv in zip(locs,roles,invs)]
            prefix=[N.jconst(N.I,degree)]
            for f in fac:prefix.append(N.jmul(prefix[-1],f))
            suffix=[None]*5;suffix[4]=N.jconst(N.I,degree)
            for j in range(3,-1,-1):suffix[j]=N.jmul(fac[j],suffix[j+1])
            if (bn,bp)==(0,0):
                for m in range(10):eq[m]+=np.sum(N.DWEIGHT[face][m]*prefix[4][read_degree])
            for j,((n,p),rr,inv) in enumerate(zip(locs,roles,invs)):
                if (n,p)!=(0,q):continue
                co=N.jmul(suffix[j+1],N.WEIGHT[face].T@prefix[j])
                jet=-N.jmul(fac[j],co) if inv else N.jmul(co,fac[j])
                for g in range(6):ek[6*rr+g]+=np.sum(jet[read_degree].T*N.G[g])
    return np.array([BP.of(v) for v in ek],dtype=object),np.array([BP.of(v) for v in eq],dtype=object)

def common_inverse():
    vals=[]
    for z in (1,-1,P.Q):vals.append(np.array(P.flat_symbols([z,z,1,1])[0],dtype=object).T)
    zero=(vals[0]+vals[1])/2
    plus=(vals[0]-zero+(vals[2]-zero)/P.Q)/2
    minus=vals[0]-zero-plus
    assert all(not x.im for v in (minus,zero,plus) for row in v for x in row)
    h=np.array([[[x.re for x in row] for row in v] for v in (minus,zero,plus)],dtype=object)
    radius=4
    inv=np.array(interpolate([z**radius*inverse(sum(v*z**(j-1) for j,v in enumerate(h))) for z in map(F,range(1,2*radius+2))]))
    expected=np.zeros((2*radius+3,24,24),dtype=object);expected[radius+1]=np.eye(24,dtype=object)
    assert np.array_equal(E.compose(h,inv),expected)
    assert np.array_equal(E.compose(inv,h),expected)
    return h,inv

def correct(f0,f2):
    h0,b0=common_inverse();h2,b2=E.build_inverse()
    def apply(b,f,radius,phase=1):
        out=np.array([BP() for _ in range(24)],dtype=object)
        for k,block in enumerate(b):
            power=k-radius
            for r in range(24):
                for c in range(24):
                    if block[r,c]:out[r]-=f[c].shift(power)*block[r,c]*phase**power
        return out
    w0,w2=apply(b0,f0,4),apply(b2,f2,3,-1)
    return np.array([w0+(-1)**q*w2 for q in range(4)],dtype=object)

def dump(v):return [BP.of(x).entries() for x in v]

LEFT_WITNESS = [[0, 1, '1/8', '-1/8'], [0, 2, '1/8', '-1/8'], [0, 3, '1/8', '1/8'], [0, 4, '1/8', '1/8'], [0, 6, '-1/2', '0'], [0, 7, '1/8', '-1/8'], [0, 8, '1/8', '-1/8'], [0, 9, '1/8', '1/8'], [0, 10, '1/8', '1/8'], [0, 14, '0', '1/4'], [0, 16, '0', '-1/4'], [0, 19, '0', '1/4'], [0, 21, '0', '-1/4'], [0, 24, '1/2', '-1/2'], [0, 25, '1/2', '-1/2'], [0, 26, '-1/4', '-3/4'], [0, 27, '-1/4', '-3/4'], [0, 28, '0', '-1'], [0, 29, '-1/4', '-3/4'], [0, 30, '-1/4', '-3/4'], [0, 31, '-1/2', '-1/2'], [0, 32, '-1', '-1/2'], [0, 33, '-1/2', '-1/2'], [1, 0, '1/2', '-1/4'], [1, 1, '-5/8', '-3/8'], [1, 2, '-5/8', '-3/8'], [1, 3, '3/8', '-1/8'], [1, 4, '3/8', '-1/8'], [1, 6, '0', '-1/4'], [1, 7, '-3/8', '-1/8'], [1, 8, '-3/8', '-1/8'], [1, 9, '-3/8', '1/8'], [1, 10, '-3/8', '1/8'], [1, 13, '-1/4', '-1/2'], [1, 14, '1/4', '-5/4'], [1, 15, '1/2', '1/4'], [1, 19, '1/4', '-5/4'], [1, 20, '-1/4', '-1/2'], [1, 22, '1/2', '1/4'], [1, 24, '-1', '1/2'], [1, 26, '0', '1/2'], [1, 27, '0', '1/2'], [1, 28, '-1/2', '-1'], [1, 31, '0', '1/2'], [1, 33, '0', '1/2'], [2, 0, '-1/2', '-1/4'], [2, 1, '0', '-1/4'], [2, 2, '0', '-1/4'], [2, 3, '0', '-1/4'], [2, 4, '0', '-1/4'], [2, 6, '0', '1/4'], [2, 7, '0', '1/4'], [2, 8, '0', '1/4'], [2, 9, '0', '1/4'], [2, 10, '0', '1/4'], [2, 12, '-1/4', '-1/4'], [2, 18, '-1/4', '-1/4'], [2, 24, '1', '0']]

def sparse_complex(blocks, radius=0):
    return [[j-radius,r,str(x.re),str(x.im)] for j,b in enumerate(blocks)
            for r,x in enumerate(b) if x]


def run_checks():
    # EPS indices are independent: no lattice length or periodic aliasing
    # is used. Identifying EPS indices modulo any period preserves every
    # identity because it is a homomorphism of this Boolean group algebra.
    assert not BP.eps(0)*BP.eps(0)-1
    for q in range(4):
        k,v=source(q,1)
        assert not any(k) and not any(v)
    print('PASS_LITERAL_LINEAR_ALL_INDEPENDENT_SIGNS',flush=True)
    fk=[source(q,2)[0] for q in (0,1)]
    correction=correct((fk[0]+fk[1])/2,(fk[0]-fk[1])/2)
    expected=np.array([[BP() for _ in range(24)] for q in range(4)],dtype=object)
    for q in (0,2):
        expected[q,0]=expected[q,6]=BP.of(F(1,2))
    assert all(BP.of(x).d==y.d for x,y in zip(correction.flat,expected.flat))
    sources=[]
    for q in range(4):
        k,v=source(q,3,correction,read_degree=2)
        assert not any(k) and not any(v)
        k,v=source(q,3,correction)
        assert not any(v)
        sources.append(np.concatenate([k,v]))
    for q in (0,1):assert not any(sources[q]+sources[q+2])
    print('PASS_UNIQUE_EVEN_CORRECTION_ALL_QUADRATIC_ROWS_AND_CUBIC_PARITY',flush=True)
    # The full cubic source simplifies to a linear Laurent operator on
    # epsilon; this conclusion is derived, never loaded as an Euler oracle.
    want0=[BP() for _ in range(34)];want1=[BP() for _ in range(34)]
    for r in (13,15,20,22):
        want0[r]=(BP.eps(0)-BP.eps(-1))/8
        want1[r]=-(BP.eps(0)+BP.eps(-1))/8
    for r in (1,2,9,10):want1[r]=BP.eps(0)/4
    for actual,want in zip(sources[:2],(want0,want1)):
        assert all(BP.of(x).d==y.d for x,y in zip(actual,want))
    S=np.array([[P.QI() for _ in range(34)] for _ in range(2)],dtype=object)
    for r in range(34):
        for power in (-1,0):
            mask=1 << (power+BP.OFFSET)
            S[power+1,r]=P.QI(sources[0][r].d.get(mask,F(0))/2,
                                -sources[1][r].d.get(mask,F(0))/2)
    J,_,at=P.line_coefficients(1)
    J=np.array([block*phase for block,phase in zip(J,(-P.Q,1,P.Q))],dtype=object)
    for z in (1,-1,P.Q):assert np.array_equal(P.literal_joint([P.Q*z,P.Q*z,P.Q,P.Q]),at(P.Q*z))
    left=np.array([[P.QI() for _ in range(34)] for _ in range(3)],dtype=object)
    for power,row,re,im in LEFT_WITNESS:left[power,row]=P.QI(F(re),F(im))
    product=np.array([[P.QI() for _ in range(24)] for _ in range(5)],dtype=object)
    for j,row in enumerate(left):
        for k,block in enumerate(J):product[j+k]+=row@block
    assert not np.any(product)
    image=np.array([P.QI() for _ in range(4)],dtype=object)
    for j,row in enumerate(left):
        for k,vector in enumerate(S):image[j+k]+=row@vector
    # Product index 2 has Laurent power +1 because S starts at -1.
    assert list(image)==[P.QI(),P.QI(),P.QI(0,F(1,4)),P.QI()]
    cost=sum(abs(x.re)+abs(x.im) for row in left for x in row)
    assert cost==36
    print('PASS_COEFFICIENTWISE_LEFT_J_ZERO_LEFT_SOURCE_I_T_OVER4_COST36',flush=True)
    bad=left.copy();bad[0,1]=-bad[0,1]
    assert any(np.any(sum((row@J[k] for j,row in enumerate(bad) for k in range(3) if j+k==p),
                         np.array([P.QI() for _ in range(24)],dtype=object))) for p in range(5))
    wrong=np.array([np.concatenate([block[:24].T,block[24:]]) for block in J],dtype=object)
    assert any(np.any(sum((row@wrong[k] for j,row in enumerate(left) for k in range(3) if j+k==p),
                         np.array([P.QI() for _ in range(24)],dtype=object))) for p in range(5))
    print('PASS_LEFT_SIGN_AND_WRONG_EULER_PLACEMENT_NEGATIVE_CONTROLS',flush=True)
    H0,B0=common_inverse()
    bound=max(max(sum(abs(block[r,c]) for block in B0 for c in range(24)) for r in range(24)),
              max(sum(abs(block[r,c]) for block in B0 for r in range(24)) for c in range(24)))
    assert bound==F(9,2)
    return {'schema':'a4d-identity-circle-sign-cubic-gate-v1',
            'input_head':'909ad048d25de2def8875290c41bf9475e9180e6',
            'arithmetic':'Q/Q(i) Boolean group algebra, actual shared-link matrix jets, coefficientwise Laurent identities',
            'coordinates':'n=x0+x1; q=x0+x1+x2+x3 mod4; T shifts n by one at fixed q',
            'leading':{'role0_1':'(epsilon_(n+1)-epsilon_n)*(1,1,-1,-1)_q*K1/2',
                       'role2_3':'epsilon_n*(1,0,-1,0)_q*T_role',
                       'normalization':'Z_n=epsilon_n*i^n/2; the second quadratic cone is q translated by one'},
            'quadratic_correction':[dump(row) for row in correction],
            'full_joint_coefficients_through_degree2':'all zero, including common metric response',
            'cubic_source_q0':dump(sources[0]),'cubic_source_q1':dump(sources[1]),
            'cubic_metric':'identically zero in all ten rows; source is a connection compatibility obstruction',
            'positive_q_fourier_source_S':sparse_complex(S,1),
            'left_witness':sparse_complex(left),
            'identities':['L(z)J(i*z,i*z,i,i)=0 for every z in C*',
                          'L(z)S(z)=i*z/4 for every z in C*'],
            'left_finite_convolution_bound_all_p':'36',
            'common_even_inverse':{'identity':'H0(b)B0(b)=B0(b)H0(b)=I24 for every b in C*',
                                   'tested_radius':4,'actual_support':[j-4 for j,b in enumerate(B0) if np.any(b)],
                                   'row_column_coefficient_bounds':'9/2','B0':E.ledger(B0,4)},
            'all_period_cubic_bound':'for Z=t*epsilon*i^n, ||S3+J*w3||_p >= (t^3/18)||epsilon||_p, every 1<=p<=infinity, without period normalization',
            'analytic_consequence':'no nonzero third-order compatible tangent supported purely on this circle quadratic zero cone, including arbitrary signs; fixed-period pure-circle tangent accumulation excluded by finite-dimensional normal reduction',
            'nonclaims':['not a uniform radius of nonlinear isolation as L grows',
                         'additional quarter coordinates and coupled-circle tangents are not controlled',
                         'not an arbitrary curved-coframe exact continuation or unrestricted response theorem'],
            'verdict':'ALL_PERIOD_PURE_CIRCLE_SIGN_CUBIC_GATE_CERTIFIED; TASK_TERMINAL_OPEN'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--expect',type=Path)
    args=parser.parse_args()
    report=run_checks()
    expected=args.expect or (Path(__file__).with_name('a4d_identity_circle_sign_cubic_gate_results.json')
                            if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text())==report
        print('PASS_PINNED_LEDGER',flush=True)
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('VERDICT',report['verdict'])
