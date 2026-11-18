"""Cold-Doob correction on scalar-return sections and deterministic Golden gates."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import runpy
import sympy as sp


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


previous=Path(__file__).with_name("check_extra_work.py")
require(hashlib.sha256(previous.read_bytes()).hexdigest()=="93d93b4923062bc2aa831afbcfda84b0c2cbab1baeeca49b43538ac5090acc45",
        "pinned rational enclosures")
tools=runpy.run_path(str(previous))
span,centre=tools["span"],tools["centre"]


def zero(expr):
    if isinstance(expr,sp.MatrixBase):
        return all(sp.simplify(x)==0 for x in expr)
    return sp.simplify(expr)==0


def plane_and_rounds():
    m,s,t=sp.symbols("m s t",positive=True)
    h=s*s+(t*t-s*s)*m
    cnum=s+(t-s)*m
    fnum=(t-s)**2*m*(1-m)
    require(sp.expand(h-cnum**2-fnum)==0,"exact squared components of B")
    r=2*m*(1-m)
    require(zero((fnum/h)/r-(t-s)**2/(2*h)),"expected extra cycles")
    # Use the actual projectors in the exact principal-plane example.
    # R is range(V), P is the proper canonical born test.
    R=sp.diag(1,0); I=sp.eye(2); original=sp.Matrix([1,0]); other=sp.Matrix([0,1])
    mm=sp.Rational(3,5); ss=sp.Rational(7,8); tt=sp.Integer(1)
    j=sp.Matrix([sp.sqrt(mm),sp.sqrt(1-mm)]); P=j*j.T
    H=ss**2+(tt**2-ss**2)*mm
    A=ss*I+(tt-ss)*P; B=sp.simplify(A*original/sp.sqrt(H))
    require(zero((B.T*B)[0]-1),"normalized transformed input")
    # Orientation preserving rotation sending B to original; tensor by
    # identity on the unknown input to cover external passive references.
    rotate=sp.Matrix([[B[0],B[1]],[-B[1],B[0]]])
    require(zero(rotate*B-original) and zero(rotate.T*rotate-I) and zero(rotate.det()-1),"direct rotation")
    trial_success=0
    for proj in (P,I-P):
        after_good=R*proj*other
        after_bad=(I-R)*proj*other
        require(zero(after_good[1]) and zero(after_bad[0]),"complete outcome maps reset the current plane")
        trial_success+=(after_good.T*after_good)[0]
    require(zero(trial_success-2*mm*(1-mm)),"actual full two-measurement retry probability")
    init_fail=(B.T*(I-R)*B)[0]
    require(zero(init_fail/trial_success-(tt-ss)**2/(2*H)),"complete mean including zero rounds")
    return {"exact_fixture_m":str(mm),"first_failure":str(sp.factor(init_fail)),
            "two_test_cycle_success":str(sp.factor(trial_success)),
            "mean_additional_rounds":str(sp.factor(init_fail/trial_success))}


def native_field():
    x=sp.Symbol("x")
    require(sp.Poly(x**4+x**2-1,x,domain=sp.QQ).is_irreducible,"quartic for a=sqrt(p)")
    factors=sp.factorint(2**20-1)
    require(factors=={3:1,5:2,11:1,31:1,41:1},"radical of feedback filter")
    sf=sp.prod(prime for prime,k in factors.items() if k%2)
    require(sf==41943 and sf!=5,"quadratic field differs from Q(sqrt(5))")
    # The other real conjugate of p=(sqrt(5)-1)/2 is negative, so K has
    # a nonreal embedding. Two different real quadratic subfields in this
    # quartic field would make it totally real biquadratic.
    require(((-sp.sqrt(5)-1)/2).is_negative,"quartic not totally real")
    # For any genuine native K-isometry, the kinematic factor in the
    # off-diagonal block of B B* has squared HS norm as below.
    U=sp.Matrix([[3,-4],[4,3]])/5
    vals=[sp.Rational(1,4),sp.Rational(3,4)]
    root=U*sp.diag(*map(sp.sqrt,vals))*U.T
    comp=U*sp.diag(*[sp.sqrt(1-m) for m in vals])*U.T
    V=root.col_join(comp)
    P=sp.diag(1,1,0,0); Q=sp.eye(4)-P; M=V.T*P*V
    z=sp.Rational(1,2**20)
    H=(1-z)*sp.eye(2)+z*M
    block=P*V*H.inv()*V.T*Q
    hs=sp.simplify(sp.trace(block.T*block))
    theory=sum(m*(1-m)/(1-z+z*m)**2 for m in vals)
    require(hs>0 and zero(hs-theory),"strict spectral HS norm")
    # Directly evaluate the true eight-letter word at the mutable 16-column
    # cut.  The same word below also checks all four original Spin columns.
    owner = Path(__file__).with_name("check_forbidden_code.py")
    require(hashlib.sha256(owner.read_bytes()).hexdigest() ==
            "b2d82cdd88c61eb307edf8878e7939dab6267ad9cbfb27a6fb90328159bccc3a",
            "pinned eight-letter operations")
    native = runpy.run_path(str(owner))
    open_counts = {}
    for rank in (4, 16):
        born = native["births"](rank)
        executed = [native["apply_word"](col) for col in born]
        contraction = [[native["dot"](left, right) for right in executed] for left in born]
        require(all(contraction[i][j] == native["O"] for i in range(rank)
                    for j in range(rank) if i != j), "native proper return is diagonal")
        interior = 0
        for i in range(rank):
            eigenvalue = native["K"].to_sympy(contraction[i][i]**2)
            require(eigenvalue.is_positive and (1-eigenvalue).is_positive,
                    "native return eigenvalue strictly between zero and one")
            interior += 1
        open_counts[rank] = interior
    return {"degree":4,"only_quadratic_subfield":"Q(sqrt(5))",
            "sqrt_one_minus_z":"5 sqrt(41943)/1024","positive_offblock_fixture":str(hs),
            "actual_eight_call_interior_eigenvalues_by_input_rank":open_counts}


def literal_centre():
    p=(span(5).sqrt()-1)/2
    q,ell=centre(); z=F(1,2**20)
    s=(1-span(z)).sqrt(); d=span(z)/(1+s)
    v0,v1=(1-q).sqrt(),q.sqrt()
    j0,j1=p.sqrt(),p**3
    j1=j1.sqrt()
    f=j0*v0+j1*v1
    m=f*f; h=1-z+z*m
    cosine=(s+d*m)/h.sqrt()
    sine=d*(m*(1-m)).sqrt()/h.sqrt()
    error=sine*(2/(1+cosine)).sqrt()
    stability_factor = 1 + 1/s + z/s**3
    positive_radius = error/stability_factor
    representative_accuracy = F(88,10**9)
    stable_gap = error-stability_factor*representative_accuracy
    require(stable_gap.lo > 0, "positive finite-word LC10 residual at 8.8e-8")
    # All three branch amplitudes positive for t>=s. LC1-commuting
    # unitaries cannot increase any branch overlap; identity saturates.
    transformed=[(s*v0+d*f*j0)/h.sqrt(),(s*v1+d*f*j1)/h.sqrt(),d*f*p**2/h.sqrt()]
    require(all(b.lo>0 for b in transformed),"co-oriented LC4 branches")
    overlap=v0*transformed[0]+v1*transformed[1]
    require(overlap.lo<=cosine.hi and overlap.hi>=cosine.lo,"LC10 saturating identity")
    require(error.lo>transformed[2].hi,"strictly sharper than forbidden-code amplitude")
    fail=sine*sine
    retry=2*m*(1-m)
    extra=d*d/(2*h)
    ratio=fail/retry
    require(ratio.lo<=extra.hi and extra.lo<=ratio.hi,"mean vs geometrical flux")
    require(1/h.lo>1 and extra.lo>0,"positive cold gain and expected rounds")
    return {"report_q":q.fmt(14),"return_m":m.fmt(15),
            "optimal_LC10_operator_norm_error":error.fmt(21),
            "finite_representative_stability_radius":positive_radius.fmt(21),
            "residual_lower_bound_at_epsilon_8_8e_minus_8":stable_gap.fmt(21),
            "forbidden_only_amplitude_bound":transformed[2].fmt(21),
            "first_range_failure_probability":fail.fmt(28),
            "retry_cycle_success_probability":retry.fmt(15),
            "mean_additional_rounds":extra.fmt(28),
            "closed_form_feedback_logged_count":"-ln(h)/ln(phi)=[ln E(L)-ln((t-s)^2/2)]/ln(phi)"}


if __name__=="__main__":
    result={"status":"PASS","scope":"specified normalized tilted input B and proper P/R instruments; implementation of B and full Book-price binding are separate",
            "exact_tests":plane_and_rounds(),"native_deterministic_field":native_field(),
            "single_recovered_block_at_original_q":literal_centre(),
            "all_prior_and_service_records_retained":True,"original_cost_info_identified":False,"GR_closed":False}
    print(json.dumps(result,indent=2))
