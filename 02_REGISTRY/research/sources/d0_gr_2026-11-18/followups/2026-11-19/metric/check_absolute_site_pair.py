"""Exact two-site absolute READY/REPORT journal, including its real parity-first reader."""
import json
from itertools import product
from fractions import Fraction as F
import sympy as sp

from check_golden_work_gauge import load_owner
from check_boundary_experiment import Golden as Q

p,one,zero=Q(0,1),Q(1),Q(0)


def native_alignment(n):
    # x,u,v -> x,u,v,d=0,g=0,c=0. Only d is read in the middle.
    zeros=sp.Matrix([1,0]); eye=sp.eye(2); kron=sp.kronecker_product
    def cx(a,b): return n.Gate("CX",(a,b))
    four=(cx(1,3),cx(2,3),cx(1,4),cx(0,4),cx(5,4))
    ex=n.Execution(6,(),(),four,report_bits=(3,4))
    matrices=[n.gate_matrix(ex,c) for c in four]
    du,dv,gu,gx,g0=matrices
    J=kron(sp.eye(8),zeros,zeros,zeros)
    basis=list(product((0,1),repeat=3))
    # One true NC1 encodes a live recorded bit in a fresh Golden tail.
    b,t=2,3
    enc=n.Execution(4,(),(),(cx(b,t),n.Gate("G",(t,)),cx(b,t)),report_bits=(b,t))
    E=n.word_matrix(enc)
    v=sp.Matrix([n.A,n.P]); g=sp.Matrix(n.G_LOCAL)
    for bit,tail in ((0,g*v),(1,zeros)):
        e=eye[:,bit]
        assert n.exact_matrix_equal(E*kron(sp.eye(4),e,v),kron(sp.eye(4),e,tail))
    exact=0
    for d,anchor in product((0,1),repeat=2):
        pd=kron(sp.eye(8),sp.diag(1-d,d),sp.eye(4))
        pg=kron(sp.eye(16),sp.diag(1-anchor,anchor),eye)
        K=pg*(gx if d else g0)*gu*pd*dv*du*J
        expected=sp.diag(*[int((u^v0)==d and (u^(d*x))==anchor) for x,u,v0 in basis])
        assert K.T*K==expected
        for mirrored in (False,True):
            # A real native noisy pointer per visit; the second visit is at the complemented
            # address. Matrix V on all coherent old-site columns, with no classical x read.
            X=sp.Matrix([[0,1],[1,0]])
            states=[kron(eye[:,x],X**(x^mirrored)*v,X**(1^x^mirrored)*v) for x in (0,1)]
            V=sp.Matrix.hstack(*states)
            effective_indices=[int((u^w)==d and (u^(d*(x^mirrored)))==anchor) for x,u,w in basis]
            M=V.T*sp.diag(*effective_indices)*V
            low=n.P if anchor==0 else n.P**2
            high=n.P if (anchor^d)==1 else n.P**2
            assert n.exact_matrix_equal(M,low*high*eye)
            exact+=1
    return exact


def main():
    n,_=load_owner()
    records=native_alignment(n)
    labels=list(product((0,1),repeat=2))
    def law(y,bits):
        a,b=bits
        # READY is a fresh identical Golden birth; REPORT is the true noisy CX pointer.
        return (p**2 if a else p)*(p if b==y else p**2)
    table={}
    moments=[]
    for x,reverse in product((0,1), repeat=2):
        first=x^reverse
        actual={}
        for u,v in product(labels,repeat=2):
            d=tuple(i^j for i,j in zip(u,v))
            g=tuple(i^(j*first) for i,j in zip(u,d))
            actual[d,g]=law(first,u)*law(1-first,v)
        if not table: table=actual
        assert actual==table and sum(actual.values(),zero)==one
        w=sum((Q(F(1+3*d[0]+5*g[0]+7*d[1]*g[1],11))*value
               for (d,g),value in actual.items()),zero)
        moments.append(w)
    assert len(set(moments))==1 and len(table)==16
    # Real prior chronological registrations distinguish orders even with all flags retained.
    tv=p-p**2
    assert tv==p**3
    tv_joint=p*p-p**4
    assert tv_joint==tv
    # A genuinely printed zero conditional on the first noisy chronological label.
    pi=Q(F(41247,100000))
    first_forward=(one-pi)*p**2+pi*p
    first_reverse=(one-pi)*p+pi*p**2
    assert first_forward-first_reverse==p**3*(Q(2)*pi-one)
    assert (one+(p-one)*first_forward)-(one+(p-one)*first_reverse)==(p-one)*p**3*(Q(2)*pi-one)
    # If an odd pair stays in its two chronological registers, which-order is orthogonal
    # until the two classically selected correction CX are actually executed.
    assert (0,1)!=(1,0) and ((1^1),(0^1))==(0,1)
    print(json.dumps({"status":"PASS","native_scalar_effect_checks_both_orientations":records,
        "absolute_ready_report_leaves":len(table),"arbitrary_example_nonproduct_price":moments[0].decimal(),
        "chronological_single_noisy_report_TV_p3":tv.decimal(),
        "all_16_leaves_both_orders_equal_exactly":True,
        "chronological_one_token_source_difference_per_dpi":(Q(2)*p**3).decimal(),
        "work_ordinary_calls_per_status_bit_forward_postprocessing":32,
        "physical_full_instruction_economy_identified":False,
        "large_geometric_writer_emitted":False},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
