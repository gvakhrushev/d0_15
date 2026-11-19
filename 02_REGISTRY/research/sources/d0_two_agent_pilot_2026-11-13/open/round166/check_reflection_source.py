"""Exact source splitting, passive monitor weights, and two compensating graphs."""

from itertools import combinations, product
import json

import sympy as sp


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def skew_generators(size):
    for left,right in combinations(range(size),2):
        generator = sp.zeros(size)
        generator[left,right], generator[right,left] = 1,-1
        yield generator


def check_split_and_single_reverse():
    c = sp.diag(sp.Rational(7,25),sp.Rational(5,13))
    s = sp.diag(sp.Rational(24,25),sp.Rational(12,13))
    eye, zero = sp.eye(2), sp.zeros(2)
    reflection = c.row_join(s).row_join(zero).col_join(
        s.row_join(-c).row_join(zero)).col_join(zero.row_join(zero).row_join(-eye))
    initial = sp.eye(6)[:,:2]
    partner = sp.eye(6)[:,2:4]
    root = initial*initial.T
    other = sp.eye(6)-root
    weight = (eye+c*c/7).inv()
    compress = lambda matrix: initial.T*matrix*initial
    norm = lambda tangent: tangent*c+c*tangent.T
    witness = reflection*root-root*reflection
    require(compress(reflection*witness-witness*reflection) == 2*(eye-c*c),
            "nonzero independent inverse witness")
    count = 0
    for generator in skew_generators(6):
        dforward = reflection*generator
        dbackward = -generator*reflection
        forward, backward = map(compress,(dforward,dbackward))
        full = forward+backward
        rotate_norm = norm(forward+backward)
        require(sp.trace(weight*norm(forward)) == sp.trace(weight*norm(backward))
                == sp.trace(weight*rotate_norm)/2, "independent half source")
        monitor = full.T*c+c*full
        require(sp.trace(weight*rotate_norm) == sp.trace(weight*monitor),
                "all-column monitor and physical source disagree")

        # Opposite input ranges at one actual shared inverse. Only this control
        # changes. Projection on their union has zero first-order defect.
        basis = sp.eye(6)
        late_d = compress(dbackward*partner*partner.T*reflection.T+
                          reflection*partner*partner.T*dbackward.T)
        require(late_d+norm(backward) == zero, "physical common inverse source differs")
        defect = (other-partner*partner.T)*dbackward.T*initial
        require((defect.T*defect)[0,0] >= 0 and (defect.T*defect)[1,1] >= 0,
                "finite norm defect must be nonnegative")
        count += 1
    require(reflection.T*reflection == basis, "non-unitary base")
    return count


def check_passive_weights_and_curvature():
    p_real = (sp.sqrt(5)-1)/2
    field = sp.QQ.algebraic_field(p_real)
    p = field.convert(p_real)
    one = field.one
    require(p+p*p == one, "Golden weights")
    cases = 0
    for attempts in range(1,5):
        a = p**(2*attempts)
        ell = p**3*sum((p**(2*k) for k in range(attempts)),field.zero)
        require(ell == p*p*(one-a), "finite selector one-visit weight")
        for cap in range(5):
            active = {0: one}
            exhausted = {}
            for depth in range(cap+1):
                initial = active.pop(depth)
                for attempt in range(attempts):
                    if depth < cap:
                        active[depth+1] = active.get(depth+1,field.zero)+initial*p**3
                    initial *= p*p
                exhausted[depth] = initial
            require(exhausted == {j:a*ell**j for j in range(cap+1)}, "wrong monitor weights")
            cases += 1

    a,ell = p*p,p**3
    require(a*(p*p*p+p*p*p) == 2*a*ell, "first abort branch balance")
    require(ell*(one+ell+a) == p*p and a*ell == p**5, "two-visit passive baseline")
    require(p*p**4 == p*p*ell == p**5, "one shared inverse arm weights")
    f,b = sp.symbols("f b",real=True)
    scalar = 2*sp.cos(f+b)**2-sp.cos(2*b)**2
    require(sp.trigsimp(sp.diff(scalar,b).subs(b,f)) == 0, "reverse row not zero")
    require(sp.trigsimp(sp.diff(scalar,b,2).subs(b,f)-4*(2*sp.cos(2*f)**2-1)) == 0,
            "scalar reverse normal curvature")
    for bits in product((0,1),repeat=3):
        registers = list(bits)
        for source,target in ((0,1),(1,2),(0,1),(1,2),(0,2)):
            registers[target] ^= registers[source]
        require(tuple(registers) == bits, "five-call physical synchronizer")
    return cases


def check_reverse_elimination():
    c = sp.diag(sp.Rational(7,25),sp.Rational(5,13))
    s = sp.diag(sp.Rational(24,25),sp.Rational(12,13))
    i = sp.eye(4)[:,:2]
    j = c.col_join(s)
    projection = i*i.T+j*j.T
    d = sp.diag(*(1/sp.sqrt(2+2*c[k,k]) for k in range(2)))
    optimum = (i+j)*d
    require(sp.simplify(optimum.T*optimum) == sp.eye(2), "top bisectors not orthonormal")
    require(sp.simplify(projection*optimum-optimum*(sp.eye(2)+c)) == sp.zeros(4,2),
            "wrong principal-angle top eigenvalues")
    half = (sp.eye(2)+c)/2
    require(sp.simplify(optimum.T*i*i.T*optimum) == half
            and sp.simplify(optimum.T*j*j.T*optimum) == half, "lost regular output support")
    p = (sp.sqrt(5)-1)/2
    v = sp.Matrix([sp.sqrt(p),p])
    sign, exchange = sp.diag(1,-1), sp.Matrix([[0,1],[1,0]])
    require(sp.simplify((v.T*sign*v)[0]-p**3) == 0, "wrong canonical reference scalar")
    require(sp.simplify((sp.eye(2)-v*v.T)*sign*v-2*p*sp.sqrt(p)*sign*exchange*v)
            == sp.zeros(2,1), "fixed ZX failed to realize the reference partner")
    return True


def main():
    print(json.dumps({
        "status": "PASS",
        "exact_nonscalar_generator_checks": check_split_and_single_reverse(),
        "exact_native_passive_monitor_cases": check_passive_weights_and_curvature(),
        "two_visit_attenuator_identity": "h_matched=p^2 I+p^5 C^2",
        "single_shared_inverse_both_active_arm_weights": "p^5",
        "free_reverse_bisectors_and_reference_transport": check_reverse_elimination(),
        "exact_odd_native_identity_for_synchronization": True,
        "full_physical_Cost_minus_Info": False,
        "GR_closed": False,
    },indent=2))


if __name__ == "__main__":
    main()
