"""Check central regular-memory lift of literal NPS2 gates, sign sector and all repeats."""
import json
from fractions import Fraction as F

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from check_extra_work import span
from check_repeat_clock import proof_bounds
from check_source_price import load_control, need


def main():
    ne, digest = load_control()
    field = ne.GOLDEN_FIELD
    p, a, gate = ne.P, ne.A, ne.Gate
    v = sp.Matrix([a, p])

    def matrix(val):
        return DomainMatrix.from_Matrix(val).convert_to(field)

    def act(spec, inclusion):
        spec = ne.execution_from_json(ne.canonical_json(spec), max_qubits=spec.qubits,
                                       max_expanded_stages=len(spec.gates))
        even, odd = inclusion, inclusion
        for g in spec.gates:
            m = ne.gate_matrix(spec, g, max_qubits=spec.qubits, max_expanded_stages=len(spec.gates))
            even = matrix(m.applyfunc(abs))*even
            odd = matrix(m)*odd
        return even, odd

    l = 1+4*p**3
    def scalar(actual, value, n):
        need((actual-matrix(value*sp.eye(n))).is_zero_matrix, "true scalar operator")

    def cut(proj, image):
        return image.transpose()*proj*image

    sign = gate("SourceI",(2,0,1))
    enc = gate("CX",(4,5))
    for address,qbank in (((2,3),p**2),((3,2),2*p**3)):
        bank=gate("CX",address)
        body=ne.Execution(6,(),(),(bank,gate("CX",(2,4)),sign,sign,bank,enc,gate("G",(5,)),enc),
                          profile=ne.G_CX_SOURCE_I,source_port=2,source_spin=(0,1),report_bits=(4,5))
        born=matrix(sp.kronecker_product(sp.eye(4),v,v,v,v))
        even,odd=act(body,born)
        invalid=matrix(sp.kronecker_product(sp.eye(16),sp.diag(0,0,0,1)))
        r_one=matrix(sp.kronecker_product(sp.eye(16),sp.diag(0,0,1,1)))
        pi=p**2+p**3*qbank
        for image,norm,dark in ((even,l,4*p**3*pi),(odd,1,0)):
            scalar(image.transpose()*image,norm,4)
            scalar(cut(invalid,image),dark,4)
            scalar(cut(r_one,image),norm*pi,4)
    g=gate("CX",(1,2))
    repeat=ne.Execution(3,(),(),(gate("CX",(0,1)),g,gate("G",(2,)),g),report_bits=(1,2))
    j=matrix(sp.kronecker_product(sp.eye(2),v,v))
    even,odd=act(repeat,j)
    for image,factor in ((even,l),(odd,1)):
        scalar(image.transpose()*image,factor,2)
        for b in (0,1):
            proj=sp.diag(1-b,b)
            exact=cut(matrix(sp.kronecker_product(proj,sp.eye(4))),image)
            need((exact-matrix(factor*proj)).is_zero_matrix,"all sectors and old records transported")
    r=(span(5).sqrt()-1)/2
    L=1+4*r**3
    m=12
    n=m+1
    total=(1+L**n)/2
    dark_scale=L**n/(1+L**n)*(4*r**3)/L
    p0=r**2+r**5
    p1=r**2+2*r**6
    gap=proof_bounds()["M12_full_master_difference_interval"]
    need(F(gap[0])>0 and dark_scale.lo>0, "spectral gap against exactly equal regular total")
    print(json.dumps({"status":"PASS", "native_source_sha256":digest,
        "termwise_positive_lift":"pair sectors of central sign in the faithful real regular representation",
        "two_matched_words_and_two_unknown_spin_bits":"all protected columns checked",
        "formal_total_for_both":"(1+(1+4p^3)^(M+1))/2",
        "odd_sector_raw_invalid":"zero", "even_sector_NC1_norm_squared":"1+4p^3",
        "suffix_cuts":"full native isometry on the canonical two births, both old pointer projections",
        "M12":{"equal_formal_mass":total.fmt(13),
               "conditional_invalid_coefficient":dark_scale.fmt(13),
               "word0_invalid_probability":(dark_scale*p0).fmt(13),
               "word1_invalid_probability":(dark_scale*p1).fmt(13),
               "full_book_master_gap":gap},
        "role_assignment_required_by_book":False, "physical_full_price_identified":False},
        indent=2,sort_keys=True))


if __name__=="__main__":
    main()
