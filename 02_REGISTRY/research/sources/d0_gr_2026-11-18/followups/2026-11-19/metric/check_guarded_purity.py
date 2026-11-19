"""Test the paid full-column purity witness and the pre-read information bound."""
from fractions import Fraction as F
import json
import sympy as sp
from sympy.polys.matrices import DomainMatrix

from check_extra_work import span
from check_source_price import load_control, need


def native_witness():
    ne, digest = load_control()
    field = ne.GOLDEN_FIELD
    dm = lambda m: DomainMatrix.from_Matrix(m).convert_to(field)
    a, p, gate = ne.A, ne.P, ne.Gate
    v, w = sp.Matrix([a,p]), sp.Matrix([-p,a])
    zero, one = sp.eye(2)[:,0], sp.eye(2)[:,1]
    k = sp.kronecker_product
    g=gate("G",(2,))
    z=(gate("SourceI",(2,0,1)),)*2
    inv=z+(g,)+z
    c23,c32=gate("CX",(2,3)),gate("CX",(3,2))
    swap=(c23,c32,c23)
    encoder=gate("CX",(3,4))
    # s=3 is born v and prepared in zero. The live r=2 returns from its temporary routing.
    gates=swap+inv+swap+inv+(c23,g,encoder,gate("G",(4,)),encoder)
    spec=ne.Execution(5,(),(),gates,profile=ne.G_CX_SOURCE_I,source_port=2,
                      source_spin=(0,1),report_bits=(3,4))
    spec=ne.execution_from_json(ne.canonical_json(spec),max_qubits=5,max_expanded_stages=len(gates))
    word=dm(ne.word_matrix(spec,max_qubits=5,max_expanded_stages=len(gates)))
    image=word*dm(k(sp.eye(8),v,v))
    target=dm(k(sp.eye(4),v*v.T,zero,ne.G_LOCAL*v)+k(sp.eye(4),w*w.T,one,zero))
    need((image-target).is_zero_matrix,"full old Spin and arbitrary input pointer")
    valid=dm(k(sp.eye(8),sp.diag(1,1,1,0)))
    pass0=dm(k(sp.eye(8),sp.diag(1,1,0,0)))
    need((valid*image-image).is_zero_matrix,"no invalid outcome on complete input")
    need((image.transpose()*pass0*image-dm(k(sp.eye(4),v*v.T))).is_zero_matrix,
         "true Born test for target state")
    return digest,len(gates)


def quantitative():
    p=(span(5).sqrt()-1)/2
    l=p**2
    w=l*(1-l)
    rho=l**2+(1-l)**2
    def h(x):
        if x.hi==0:
            return span(0)
        return x*(1/x).log_positive()+(1-x)*(1/(1-x)).log_positive()
    rows={}
    # Pure dilations that realize every indicated coherence and saturate the quantum Holevo bound.
    for u in (F(0),F(1,4),F(1,2),F(3,4)):
        err=2*w*(1-u)
        eigen=(1-(1-4*w*(1-u*u)).sqrt())/2
        bound=h(err)
        ent=h(eigen)
        need(ent.hi<bound.lo,"qbit entropy vs pure-return binary entropy")
        rows[str(u)]={"echo_failure":err.fmt(12),"full_memory_Holevo_nats":ent.fmt(12),
                      "purity_test_upper_nats":bound.fmt(12)}
    for m in (1,2,12):
        # Product dephasing yields a physically constructible perfectly informative copy.
        # Principal return after its generating measurement equals the collision probability.
        total=span(1)
        for _ in range(m):
            total*=rho
        need(total.hi<1 and total.lo>0,"full which-record causes nonzero echo loss")
    return {"golden_single_full_prediction_echo_survival":rho.fmt(13),
            "golden_12_full_prediction_echo_survival":(rho**12).fmt(13),
            "partial_preexisting_marker_examples":rows}


if __name__=="__main__":
    digest,ticks=native_witness()
    print(json.dumps({"status":"PASS","native_source_sha256":digest,
        "native_square_calls_excluding_births":ticks,"unknown_input_columns":8,
        "matched_input_hypothesis_information":"exactly zero including arbitrary additional WORK/reference",
        "spectral_and_native_friction_identification":False,**quantitative()},
        indent=2,sort_keys=True))
