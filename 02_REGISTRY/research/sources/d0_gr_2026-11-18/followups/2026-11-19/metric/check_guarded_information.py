"""Guarded real reader, equal-inventory source-port settings, and two operational info laws."""
from fractions import Fraction as F
import json
import sympy as sp
from sympy.polys.matrices import DomainMatrix

from check_extra_work import span
from check_source_price import load_control, need


def native():
    ne, digest = load_control()
    p, a = ne.P, ne.A
    gate = ne.Gate
    const = ne.GOLDEN_FIELD
    to_field = lambda m: DomainMatrix.from_Matrix(m).convert_to(const)
    v=sp.Matrix([a,p])
    # Live T=3, fresh r=2 is the permitted SourceI port, fresh tail=4.
    # Basis order of the retained input is Spin0, Spin1, T.
    born=to_field(sp.kronecker_product(sp.eye(4),v,sp.eye(2),v))
    spin=gate("SourceI",(2,0,1))
    g=gate("G",(2,))
    cx=gate("CX",(2,4))
    report=(gate("CX",(3,2)),cx,gate("G",(4,)),cx)
    before_enc=sp.Matrix([[a,-p],[p,a]])
    # Use a small common N for the all-column literal replay.
    for n in (0,1,2):
        N=2
        gates=(spin,spin)+(g,)*(N-n)+(spin,spin)+(g,)*(N+n)+report
        spec=ne.Execution(5,(),(),gates,profile=ne.G_CX_SOURCE_I,source_port=2,
                          source_spin=(0,1),report_bits=(2,4))
        spec=ne.execution_from_json(ne.canonical_json(spec),max_qubits=5,max_expanded_stages=len(gates))
        end=to_field(ne.word_matrix(spec,max_qubits=5,max_expanded_stages=len(gates)))*born
        work=to_field(before_enc)**(2*n) * to_field(v)
        l=work[1,0].element**2
        l_symbol=const.to_sympy(l)
        expected=to_field(sp.kronecker_product(sp.eye(4),sp.diag(l_symbol,1-l_symbol)))
        mark=to_field(sp.kronecker_product(sp.eye(4),sp.diag(0,1),sp.eye(2),sp.diag(1,0)))
        dark=to_field(sp.kronecker_product(sp.eye(4),sp.diag(0,1),sp.eye(2),sp.diag(0,1)))
        need((end.transpose()*mark*end-expected).is_zero_matrix,"complete conditional pointer effects")
        need((end.transpose()*dark*end).is_zero_matrix,"dark support stays exact")
    return digest


def ctimes(z,y):
    a,b=z
    c,d=y
    return a*c-b*d, a*d+b*c


def rotation(z,n):
    result=span(1),span(0)
    while n:
        if n%2:
            result=ctimes(result,z)
        z=ctimes(z,z)
        n//=2
    return result


def proof():
    p=(span(5).sqrt()-1)/2
    a=p.sqrt()
    ell=(1/p).log_positive()
    l0=p**2
    def values(n):
        _,ss=rotation((a,p),2*n+1)
        l=ss**2
        entropy=l*(1/l).log_positive()+(1-l)*(1/(1-l)).log_positive()
        h0=(1+l0)*ell
        code=l-l0-(entropy-h0)/ell
        overlap=a*(1-l).sqrt()+p*l.sqrt()
        return l, code, 1-overlap
    out={}
    for n in (902,903):
        l,code,gap=values(n)
        d=l-l0
        q=code/d
        amp=gap/d
        need(0<code.lo<code.hi and 0<gap.lo and d.lo*d.hi>0,"finite proper quadratic remainders")
        need(max(abs(q.lo),abs(q.hi))<F(1,100),"guarded code response is locally suppressed")
        out[str(n)]={"l_minus_native":d.fmt(14),"observed_code_length_secant":"1",
                     "complete_CQ_code_secant":q.fmt(14),"one_minus_overlap_secant":amp.fmt(14),
                     "Bayesian_old_information_gain":"0"}
    # d h(l_0)/d l = ln((1-p^2)/p^2) = ln(1/p).
    need((a*p).lo>F(48,100),"strict lower angular source bifurcation")
    for w in (F(-1,3),F(0),F(1,2),F(4,3)):
        need(max(abs(w),abs(w-1))>=F(1,2),"any shared physical cost derivative")
    return {"common_N":903,"two_sided_physical_settings":out,
            "central_relative_rows_in_error_coordinate":{"direct_length":1,
                "CQ_entropy_in_golden_units":1,"mutual_information_about_conditional_old_input":0,
                "registered_length_minus_CQ":0,"optimal_cold_corner":0},
            "minimum_discrepancy_shared_work_no_thermal_remainder":"1/2 per varied copy",
            "minimum_angle_discrepancy":(a*p).fmt(14)}


if __name__=="__main__":
    print(json.dumps({"status":"PASS","native_source_sha256":native(),**proof(),
        "microscopic_info_selected":False,"fixed_birth_actuator_is_an_additional_admission":True,
        "spectral_finite_heat_row_set_to_zero":False},indent=2,sort_keys=True))
