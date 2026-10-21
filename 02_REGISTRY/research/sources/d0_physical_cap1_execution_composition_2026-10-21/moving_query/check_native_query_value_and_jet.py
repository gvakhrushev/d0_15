#!/usr/bin/env python3
"""Exact bounded application to the original full8D query; no repo writes."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import sympy as s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    start = time.perf_counter()
    a, z, eta2, df, dq, sigma = s.symbols('a z eta2 df dq sigma')
    p = a**2
    modulus = s.Poly(a**4+a**2-1, a)
    def red(x):
        return s.rem(s.Poly(s.expand(x), a), modulus).as_expr().expand()
    def zero(x):
        if isinstance(x, s.MatrixBase):
            return all(red(v) == 0 for v in x)
        return red(x) == 0
    passed = []
    def require(ok, label):
        if not bool(ok):
            raise RuntimeError(label)
        passed.append(label)

    I2 = s.eye(2)
    J = s.Matrix([[0,-1],[1,0]])
    G = s.Matrix([[a,-p],[p,a]])
    CX = s.eye(4)
    CX[2,2] = CX[3,3] = 0
    CX[2,3] = CX[3,2] = 1
    T = CX*s.kronecker_product(G,I2)
    owned_T = s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
    require(T == owned_T, 'literal T_star = CX (G tensor I), all16 entries')
    require(zero(G.T*G-I2) and zero(T.T*T-s.eye(4)), 'native Golden and four-tail orthogonality')
    U = s.kronecker_product(T*T,G*G)
    require(zero(U.T*U-s.eye(8)), 'full8D six-letter baseline is orthogonal')

    # Required original angle jets, with no moving field set to zero.
    dthetaE = a*eta2*df/2
    dthetab = sigma*a**3*eta2*dq
    dT = dthetaE*CX*s.kronecker_product(J*G,I2)
    dG = dthetab*J*G
    dU = s.kronecker_product(dT*T+T*dT,G*G)+s.kronecker_product(T*T,dG*G+G*dG)
    require(zero(dU.T*U+U.T*dU), 'required complete query jet is orthogonal tangent')
    require(zero(s.trace(dU)+8*p**5*eta2*df+32*sigma*p**4*eta2*dq), 'full trace distinguishes required jet from moving unitary compression')
    require(not zero(dU), 'fixed native word zero jet does not equal original query jet')

    P = s.zeros(8,2)
    P[0,0] = P[2,1] = 1
    W = P.T*U*P
    dW = P.T*dU*P
    F = I2-W.T*W
    dF = -dW.T*W-W.T*dW
    plus, minus = s.Matrix([1,1]), s.Matrix([1,-1])
    L, M = 4*p**3, 4*p**3*(1+p**6)
    A = (plus.T*F*plus)[0]/2
    B = (minus.T*F*minus)[0]/2
    dA = (plus.T*dF*plus)[0]/2
    dB = (minus.T*dF*minus)[0]/2
    require(zero(A-M) and zero(B-L), 'actual retained plus/minus feedback eigenvalues')
    require(zero(dA-eta2*(4*p**11*df+8*sigma*p**12*dq)), 'upper-band full geometric and matter jet')
    require(zero(dB-8*sigma*p**6*eta2*dq), 'lower-band real matter jet')
    Q, R = 1-z*L, 1-z*M
    dr = z*(Q*dA+R*dB)
    target = z*eta2*(4*Q*p**11*df+8*sigma*p**6*(R+Q*p**6)*dq)
    require(zero(dr-target), 'complete two-query click jet including both bands')
    require(not zero(s.diff(dr,dq)), 'freezing live matter changes actual report source')

    # A fixed larger W and same moving isometric input/output cut.
    k, l00, l01, l10, l11 = s.symbols('k l00 l01 l10 l11')
    Uc = s.diag(1,-1)
    Wc = s.diag(Uc,J)
    i = s.eye(4)[:,:2]
    K = s.Matrix([[0,-k],[k,0]])
    di = K.col_join(s.Matrix([[l00,l01],[l10,l11]]))
    require(i.T*di+di.T*i == s.zeros(2), 'general isometric first tangent including normal motion')
    da = di.T*Wc*i+i.T*Wc*di
    require(s.simplify(da-(Uc*K-K*Uc)) == s.zeros(2), 'unitary compression first derivative is conjugacy')
    require(s.trace(da) == 0, 'unitary compression trace source zero')
    # The lemma does not exclude genuinely leaky moving-cut readout.
    ii = s.Matrix([s.Rational(3,5),s.Rational(4,5)])
    dii = s.Matrix([-s.Rational(4,5),s.Rational(3,5)])
    aa = (ii.T*Uc*ii)[0]
    daa = (dii.T*Uc*ii+ii.T*Uc*dii)[0]
    require(aa == -s.Rational(7,25) and daa == -s.Rational(48,25), 'leaky moving-cut countercontrol')
    require(-2*aa*daa == -s.Rational(672,625), 'leaky Book complement has real encoding source')
    # A distinct moving output decoder is not same-cut compression.
    rot = s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
    require(s.trace(-J*rot) == s.Rational(8,5), 'different moving decoder escapes only with its own source')

    result = {'status':'PASS', 'scope':'exact six-letter baseline and original full8D first jet; same-cut lemma controls only',
              'checks':passed,'word_inventory':{'G':4,'CNOT':2},
              'trace_DU':'-8 p^5 eta^2 df - 32 sigma p^4 eta^2 dq',
              'sympy_version':s.__version__,'elapsed_seconds':time.perf_counter()-start,
              'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    payload = json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(payload)
        print(json.dumps({'status':result['status'],'output':str(args.output),'elapsed_seconds':result['elapsed_seconds']}))
    else:
        print(payload,end='')


if __name__ == '__main__':
    main()
