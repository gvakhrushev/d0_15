"""Exact CAR completion, all-column program amplitudes, and a retained read."""

from fractions import Fraction
from itertools import product
import json
from math import isqrt, lcm
from pathlib import Path
import sys

import sympy as sp
import mpmath as mp

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "direct/round80/price"))
sys.path.insert(0, str(PILOT / "open/round181"))
from check_fixed_positive_reader import a, cx, nc1, ne, one, power, require
from check_parity_price import action, p

A = sp.Symbol("a")
P = A**2
RELATION = sp.Poly(A**4+A**2-1,A,domain=sp.QQ)
EVEN = tuple(i for i in range(16) if bin(i).count("1")%2 == 0)
SPARES = (2,4,8,11,13)


def reduce(value):
    return sp.Poly(value,A,domain=sp.QQ).rem(RELATION).as_expr()


def four_squares(value):
    pairs = {}
    for x in range(isqrt(value)+1):
        for y in range(x,isqrt(value-x*x)+1):
            pairs.setdefault(x*x+y*y,(x,y))
    for total, pair in pairs.items():
        if value-total in pairs:
            return pair + pairs[value-total]
    raise ArithmeticError("No four-square decomposition found")


def pack(psi, e14, extra, extra_grade, remaining):
    result = [sp.S.Zero]*16
    result[0],result[15] = (sp.Rational(q) for q in psi)
    result[1], result[14], result[extra_grade] = A,e14,extra
    other_grades = (grade for grade in SPARES if grade != extra_grade)
    for index,value in zip(other_grades,remaining):
        result[index] = value
    require(reduce(sum(y*y for y in result)) == 1, "Wrong field-completion normalization")
    require(all(index in (0,15) or result[index] == 0 for index in EVEN),
            "Even mask must be the original two field components")
    return sp.Matrix(result)


def fixed_car(psi):
    D = lcm(8,*(q.denominator for q in psi))
    budget = Fraction(3,8)-sum(q*q for q in psi)
    require(budget>=0 and (budget*D**2).denominator == 1, "Invalid rational field budget")
    numerators = four_squares(int(budget*D**2))
    c = (2*P-1)/4
    return pack(psi,c,c,11,[sp.Rational(q,D) for q in numerators])


def near_car(psi,v,scale):
    u = (v*v-1)/(2*v)
    D = scale*lcm(u.denominator,v.denominator,*(q.denominator for q in psi))
    budget = 1-u*u-v*v-sum(q*q for q in psi)
    units = budget*D*D
    require(units>0 and units.denominator==1, "No rational slack for the near completion")
    r = isqrt(int(units))
    nums = four_squares(int(units)-r*r)
    return pack(psi,sp.Rational(r,D),sp.Rational(u)+sp.Rational(v)*P,8,
                [sp.Rational(q,D) for q in nums]),D


def householder(m):
    root = sp.eye(16)[:,0]
    w = root-m
    T = (sp.eye(16)-w*w.T/(1-m[0])).applyfunc(reduce)
    require(T[:,0] == m.applyfunc(reduce), "Wrong loaded CAR on a clean column")
    require((T.T*T).applyfunc(reduce) == sp.eye(16), "New completion must be orthogonal on all columns")
    return T


def lcu_amplitudes(blocks,budget_power):
    coeffs = []
    for block in blocks:
        coeffs.append([[sp.Poly(x,A).nth(j) for j in range(4)] for x in block])
    D = int(lcm(*(int(sp.denom(c)) for table in coeffs for row in table for c in row)))
    R = 1 << ((budget_power*D-1).bit_length())
    raw_counts = []
    for T,table in zip(blocks,coeffs):
        counts = [[int(D*c) for c in row] for row in table]
        used = sum(sum(abs(c) for c in row) for row in counts)
        require(used <= budget_power*D <= R, "Selector capacity is exceeded")
        raw_counts.append(used)
        expected = T.applyfunc(lambda x:reduce(A**3*D*x/R))
        contracted = sp.Matrix(T.rows,T.cols,[
            reduce(sum(c*A**(3+j) for j,c in enumerate(row))/R) for row in counts
        ])
        require(contracted == expected, "Physical label contraction changes an old column")
    return {"common_coefficient_denominator":D,"coherent_label_bits":R.bit_length()-1,
            "M_terms_per_lookup":raw_counts,"logical_Kraus_scale":f"a^3 * {D}/{R}",
            "old_CAR_columns_each_SITE":blocks[0].cols}


def test_golden_exponents():
    # Input word uses three genuine Golden births before the classical signs.
    birth = {}
    for digits in product((0,1),repeat=3):
        idx = 8+4*digits[0]+2*digits[1]+digits[2]
        amp = one
        for bit in digits:
            amp *= p if bit else a
        birth[idx]=amp
    for j in range(4):
        terminal = birth
        for wire in range(1,j+1):
            terminal = action(terminal,cx(0,wire),4)
        require(terminal[8] == power(a,3+j), "Wrong amplitude of the three actual born flags")
    return {"births":3,"successful_flag":"000","amplitudes":["a^3","a^4","a^5","a^6"]}


def literal_phase_meter():
    # 4 data bits, followed by 2 real NC1 tails. The published mark is (b0,b3)=(1,1).
    pivot_word = tuple(cx(0,i) for i in (1,2,3))+(ne.Gate("G",(0,)),)
    word = pivot_word+nc1(0,4)+nc1(3,5)
    tails = (a*a,a*p,p*a,p*p)
    amp_f = (2*p-one)*one
    # Compare 4*state to keep integer Golden coefficients in the exact executor.
    def click(f_sign):
        root = {}
        for index,v in ((1,4*a),(14,f_sign*amp_f),(2,one),(8,a)):
            for t,coeff in enumerate(tails):
                root[4*index+t]=v*coeff
        for g in word:
            root=action(root,g,6)
        return sum((v*v for index,v in root.items() if (index & 32) and (index & 4)),one*0)
    require(click(1)-click(-1) == 16*power(p,5),
            "The same-diagonal signed filler must be distinguishable on literal heads")
    return {"retained_heads":2,"CX":7,"G":3,"additional_births":2,
            "click_difference_at_filling_plus_vs_minus":"p^5"}


def literal_parity_filler_rotation():
    # CAR bits 0..3, old PORT=4, old Spin=5,6. Rotations act on the
    # routed old port rather than assuming any blank in the old carrier.
    target, ctl1, ctl0, port = 0,2,3,4
    swap = (cx(target,port),cx(port,target),cx(target,port))
    source = ne.Gate("SourceI",(4,5,6))
    g = ne.Gate("G",(port,))
    inverse_g = (source,source,g,source,source)
    word_b = (g,cx(ctl1,port))+inverse_g+(cx(ctl1,port),)
    middle = (cx(ctl0,port),)+word_b+(cx(ctl0,port),)+word_b
    move_odd_pair = cx(0,1)
    word = (move_odd_pair,)+swap+middle+swap+(move_odd_pair,)
    execution = ne.Execution(7,(),(),word,ne.G_CX_SOURCE_I,4,(5,6))
    ne.validate_execution(execution,max_qubits=7,max_expanded_stages=26)
    C=9*one-16*p
    S=8*a-12*a*p
    expected_pairs = {(2,14),(6,10)}
    active = {i for pair in expected_pairs for i in pair}
    require(C*C+S*S==one,"Golden pair rotation normalization")
    for col in range(128):
        state={col:one}
        for gate in word:
            state=action(state,gate,7)
        data=col>>3
        if data not in active:
            expected={col:one}
        else:
            low,high=next(pair for pair in expected_pairs if data in pair)
            other=(high if data==low else low)*8+(col&7)
            expected={col:C,other:(S if data==low else -S)}
        require(state==expected, "Filler rotation must leave the actual old PORT/Spin and useful grades unchanged")
    return {"stages":len(word),"all_old_columns":128,
            "pairs":[[2,14],[6,10]],"cosine":"9-16p","sine":"8a-12ap"}


def two_real_filler_obstruction():
    # The two odd grades that meet both old selector types are 8 and 14.
    choices = ((32,211),(64,139))
    rows = []
    for M,prime in choices:
        residue = (1-pow(M*M,-1,prime))%prime
        numerator = M**4-3*M**2+1
        root = next(a for a in range(prime) if (a*a-residue)%prime == 0)
        require(prime%4==3 and sp.isprime(prime) and numerator%prime==0
                and numerator%(prime*prime)!=0,"Need an odd local valuation")
        require((root**4+root*root-1)%prime==0 and (4*root**3+2*root)%prime!=0,
                "Hensel embedding must be on a simple root")
        require((-1-residue)**2*pow(M,2,prime)%prime!=1,
                "Conjugate root also vanishes, contradicting simple valuation")
        rows.append({"M":M,"prime":prime,"a_residue":root,"valuation":1})
    return rows


def a89_work_control():
    # Two real ordered settings in A89 JOINT_BOOTSTRAP.
    with mp.workdps(65):
        base=(mp.sqrt(5)-1)/2
        theta=mp.asin(base)
        t=1160*theta-246*mp.pi
        # First CX of the second parity chain: one unit of switched odd mass.
        before_plus = mp.sin(mp.pi/2 + 65*theta+t)**2
        before_minus = mp.sin(mp.pi/2 + 65*theta-t)**2
        secant = base**2*((1-2*before_plus)-(1-2*before_minus))/(2*t)
        formula = base**2*mp.sin(130*theta)*mp.sin(2*t)/t
        require(abs(secant-formula)<mp.mpf("1e-58") and
                mp.mpf("-.745945")<formula<mp.mpf("-.745944"),
                "Wrong actual local CW1 mixed contrast")
    return {"ready":"p^2","changed_CAR_lsb_mass":"at least (p^3/4)^2",
            "work_contrast_per_moved_mass_interval":["-.745945","-.745944"]}


def main():
    profiles = [(Fraction(k,64),Fraction(0)) for k in (0,1,2)] + [
                (Fraction(1,64),Fraction(1,64))]
    fixed = [fixed_car(psi) for psi in profiles]
    nearby = [near_car(psi,Fraction(2,3),4) for psi in profiles]
    a_real = sp.sqrt((sp.sqrt(5)-1)/2)
    near_certificate = []
    for psi,(new,D) in zip(profiles,nearby):
        old = sp.sqrt((sp.sqrt(5)-1)**2/4-sum(sp.Rational(q)**2 for q in psi))
        err2 = 2*old*(old-new[14])
        eps = new[8].subs(A,a_real)
        bound = 2*eps**2+2*a_real**2/D
        require(float((bound-err2).evalf(40))>=0,"Near completion violates the uniform estimate")
        near_certificate.append({"D":D,"state_error_bound":float(sp.sqrt(bound).evalf(15))})
    result = {
        "all_column_householder":lcu_amplitudes([householder(m) for m in fixed],256),
        "clean_car_preparation":lcu_amplitudes(fixed,4),
        "declared_near_car_preparation":lcu_amplitudes([m for m,_ in nearby],8),
        "near_completion_bounds":near_certificate,
        "three_canonical_birth_flags":test_golden_exponents(),
        "literal_phase_meter":literal_phase_meter(),
        "literal_parity_filler_rotation":literal_parity_filler_rotation(),
        "two_real_filler_local_obstructions":two_real_filler_obstruction(),
        "A89_intermediate_work_contrast":a89_work_control(),
        "full_original_Cost_Info_equivalence_proved":False,
        "GR_closed":False
    }
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
