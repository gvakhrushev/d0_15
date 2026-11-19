"""Exact field obstruction for a coherent L=16 reference-loader column."""
import json
import math
import sympy as sp
import mpmath as mp
from sympy.polys.matrices import DomainMatrix
from sympy.polys.polyerrors import CoercionFailed

from check_source_price import load_control, need


def main():
    ne,digest=load_control()
    sqrt2,sqrt5=sp.sqrt(2),sp.sqrt(5)
    p=(sqrt5-1)/2
    a=sp.sqrt(p)
    K=sp.QQ.algebraic_field(a,sqrt2)
    need(K.mod.degree()==8,'actual Golden-Hadamard number field degree')
    # Full local native alphabet and every canonical fresh resource entry.
    H=sp.Matrix([[1,1],[1,-1]])/sqrt2
    v=sp.Matrix([a,p])
    matrices=(ne.G_LOCAL,ne.SOURCE_I_LOCAL,H,v)
    checked=0
    for M in matrices:
        for x in M:
            K.from_sympy(x)
            checked+=1
    need(checked==74,'all native and fresh matrix entries in K')

    # The parent note uses A'=p sin(712 theta), a matrix element in Q(a).
    native=DomainMatrix.from_Matrix(ne.G_LOCAL).convert_to(ne.GOLDEN_FIELD)
    power=native**712
    need(power.transpose().matmul(power)==DomainMatrix.eye((2,2),ne.GOLDEN_FIELD),
         'exact finite-word Golden power')
    mp.mp.dps=280
    pp=(mp.sqrt(5)-1)/2;theta=mp.asin(pp)
    iv=mp.iv;iv.dps=60
    ip=(iv.sqrt(5)-1)/2; itheta=iv.atan2(ip,iv.sqrt(ip))
    sine=iv.sin(712*itheta)
    need(sine.a>iv.mpf('0.01801378') and sine.b<iv.mpf('0.01801379'),
         'A prime is strictly nonzero')
    amplitude=pp*mp.sin(712*theta)

    # The formal independent number-field checker agrees with the norm proof
    # in the note.  The norm proof itself is not delegated to this exception.
    cosine=sp.sqrt(2+sqrt2)/2
    try:
        K.from_sympy(cosine)
        member=True
    except CoercionFailed:
        member=False
    need(not member,'exact cos(pi/8) is outside actual gate field')
    s=2+sqrt2
    need(sp.simplify(s*(2-sqrt2))==2, 'N_Qsqrt2/Q(s)=2')
    need(sp.simplify((s/5)*((2-sqrt2)/5))==sp.Rational(2,25),
         'N_Qsqrt2/Q(s/5)=2/25')
    need(sp.simplify(p*((-sqrt5-1)/2))==-1, 'N_Qsqrt5/Q(p)=-1')
    need(sp.simplify(-s**2).is_negative is True, 'other norm is strictly negative')
    x=sp.Symbol('x')
    need(sp.minpoly(cosine,x)==8*x**4-8*x**2+1, 'exact phase polynomial')

    # A restricted address set n=0,8 uses only ±1 and is not excluded.
    restricted=[sp.cos(2*sp.pi*n/16) for n in (0,8)]
    need(restricted==[1,-1] and all(K.from_sympy(q) is not None for q in restricted),
         'selected-address subset remains available')

    # Check the cyclic edge-error estimate on a deliberately nonuniform set
    # of four phase errors, including 15 -> 0; this is a conditional analytic
    # bound, not a claim that these approximated phases were physically built.
    L=16;h=1/L; err=[1e-6,-2e-6,3e-6,-1e-6]
    E=sum(abs(x) for x in err)
    A=float(amplitude)
    angles=[2*math.pi*n/L+sum(((n>>j)&1)*err[j] for j in range(4))
            for n in range(L)]
    base=4*A*A*math.sin(math.pi/L)**2/h**2
    worst=0.
    for n in range(L):
        delta=angles[(n+1)%L]-angles[n]
        value=4*A*A*math.sin(delta/2)**2/h**2
        worst=max(worst,abs(value-base))
    bound=A*A/h**2*(2*abs(math.sin(2*math.pi/L))*E+E**2)
    need(worst <= bound*(1+1e-10), 'all-site and periodic-boundary phase error')
    print(json.dumps({
      'status':'PASS','native_source_sha256':digest,
      'field':'Q(sqrt(phi^-1),sqrt(2))','field_degree':int(K.mod.degree()),
      'primitive_and_resource_entries_checked':checked,
      'norm_2_plus_sqrt2':'2','norm_divided_by_five':'2/25',
      'norm_golden_p':'-1','negative_norm_obstruction':True,
      'cos_pi_over_8_in_field':False,
      'one_common_success_column_obstructed':True,
      'requires_nonzero_reference_and_coherent_common_success':True,
      'selected_site_n0_n8_excluded':False,
      'finite_approximation_excluded':False,
      'alternative_primitive_alphabet_excluded':False,
      'example_A_prime':mp.nstr(amplitude,24),
      'periodic_site_edges_checked':L,
      'example_phase_error_max':worst,'example_phase_error_upper_bound':bound,
      'genuine_kappa_phase_sequence_compiled':False,
      'full_book_cost_info_identified':False,'GR_closed':False,
    },sort_keys=True,indent=2))


if __name__=='__main__':
    main()
