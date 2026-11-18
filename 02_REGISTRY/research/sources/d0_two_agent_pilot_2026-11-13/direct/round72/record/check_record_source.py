"""Verify native Golden pair preparation and the two-copy H.1 determinant reporter."""
from itertools import product
from math import sqrt, log
from pathlib import Path
from hashlib import sha256
import sys
import sympy as sp
import mpmath as mp


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def criterion(bits, epsilon):
    x, y, old, ready_r, r, ready_f, f, ready_u, u, coin_a, coin_b = bits
    if not (ready_r and ready_f and ready_u):
        return 0
    value = 0
    if old:
        if x == y == 0:
            value = int((coin_a, coin_b) == (0, 1))
        elif x == y == 1:
            value = int((coin_a, coin_b) == (1, 1))
        elif coin_a == 1 and f == 0:
            value = epsilon * (2*r-1)
    return int(value == 1 or (value == 0 and u == 1))


def walsh(entries):
    row = list(entries)
    half = 1
    while half < len(row):
        for start in range(0, len(row), 2*half):
            for j in range(start, start+half):
                lo, hi = row[j], row[j+half]
                row[j], row[j+half] = lo+hi, lo-hi
        half *= 2
    return row


def probability(value, p1):
    return p1 if value else 1-p1


def main():
    root = Path(__file__).resolve().parents[7]
    source = root / '02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
    require(sha256(source.read_bytes()).hexdigest() == '222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c', 'native gate source')
    sys.path.insert(0, str(source.parent))
    import native_execution as native
    cx = native.Execution(2, (), (), (native.Gate('CX',(0,1)),))
    pair = sp.kronecker_product(sp.Matrix([native.A,native.P]), sp.Matrix([native.A,native.P]))
    after = native.word_matrix(cx, max_qubits=2) * pair
    # Native address 0 is the most significant bit. The last bit is herald=1.
    herald = sp.Matrix([after[1], after[3]])
    require(sp.simplify(herald[0]-native.A*native.P)==0 and herald[0]==herald[1], 'actual coherent fair pair')
    g = sp.Matrix([[native.A,-native.P],[native.P,native.A]])
    read = g @ herald
    require(sp.simplify(read[1]**2-read[0]**2 - 4*(native.A*native.P)**3)==0, 'conditional signed bias 2ap')
    p = (sqrt(5)-1)/2
    a = sqrt(p)
    h = 2*p**3
    gamma = h**3
    require(0 < gamma < .11, 'Golden herald gain')
    mp.mp.dps = 60
    golden = (mp.sqrt(5)-1)/2
    theta = mp.asin(golden)
    m_probe = next(i for i in range(1,100) if mp.sin(i*2**11*theta)**2 > mp.mpf('.51'))
    nu = float(mp.sin(m_probe*2**11*theta)**2)
    all_bits = list(product((0,1), repeat=11))
    # The actually prepared raw basis probabilities, also including each failed herald.
    def bank(ready, value, signed):
        if not signed:
            return (h/2 if ready else (p**2 if value==0 else p**4))
        pair_slice = [a*p, a*p] if ready else [a*a,p*p]
        t0, t1 = pair_slice
        return ((a*t0-p*t1) if value==0 else (p*t0+a*t1))**2

    q_grid = (.12, .137, .2, .72)
    for epsilon in (-1,1):
        selectors = [criterion(b,epsilon) for b in all_bits]
        require(walsh(walsh(selectors)) == [len(selectors)*x for x in selectors], 'integer all-column Gray rotation exponents')
        lifted = []
        for raw in product((0,1), repeat=12):
            old_success = int(raw[2:4] == (0,0))
            row = (*raw[:2], old_success, *raw[4:])
            lifted.append(criterion(row,epsilon))
        require(walsh(walsh(lifted)) == [len(lifted)*x for x in lifted], 'actual two-wire return predicate inside the same flag')
        for q in q_grid:
            for old in (0,.37,.81,1):
                total = 0.
                selected = 0.
                for bits, take in zip(all_bits, selectors):
                    x,y,c,hr,r,hf,f,hu,u,ca,cb = bits
                    mass = (probability(x,q)*probability(y,q)*probability(c,old)
                            * bank(hr,r,True)*bank(hf,f,False)*bank(hu,u,False)
                            * probability(ca,p*p)*probability(cb,p*p))
                    total += mass
                    selected += take*mass
                w = (p*a*(1-q)+epsilon*p*p*q)**2
                require(abs(total-1)<1e-13 and abs(selected-gamma*(1+old*w)/2)<2e-14,
                        'full raw law and predicate')
                u = nu*selected
                eigenvalues = (.17,.23,.6)
                retained = [branch*v for branch in (u,1-u) for v in eigenvalues]
                entropy_gain = -sum(v*log(v) for v in retained)+sum(v*log(v) for v in eigenvalues)
                require(abs(entropy_gain + u*log(u)+(1-u)*log(1-u))<2e-14, 'full conditional spectra')
                zeta = 2**-20
                partition = 1-zeta + zeta*old*w
                for b in (-1,0,1):
                    k = nu*gamma*partition*(log((1-u)/u)/log(1/p)-b)/(8*zeta)
                    require(k>0, 'positive field gain')
    # Joint analytic row, allowing both previous preparation and the present report to vary.
    q,s,pa,aa,sign,zeta,nugamma,rank = sp.symbols('q s p a epsilon z k r', positive=True)
    w=(pa*aa*(1-q)+sign*pa**2*q)**2
    g0=1-zeta+zeta*s*w
    u=nugamma*(1+s*w)/2
    for var in (q,s):
        require(sp.simplify(sp.diff(-rank*sp.log(g0),var)
                            +2*rank*zeta*sp.diff(u,var)/(g0*nugamma))==0,
                'absolute first variation with moving past')
    print('PASS native paired coins, both SER signs, full coherent selector, conditional entropy and old-source row')


if __name__ == '__main__':
    main()
