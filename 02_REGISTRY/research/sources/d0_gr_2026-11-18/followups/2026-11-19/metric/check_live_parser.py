"""Four paid LC1 marks on reused heads: exact native gates and RAW/record checks."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json

from check_golden_record_race import gold, p
from check_extra_work import span
from check_source_price import load_control, need


def controller():
    # Wires 0,1 are Spin. 2 is a separate port. 3,4 are H,T. The six
    # new WORK wires 5..10 are D, tail D, C, tail C, tail X, tail T.
    ne, digest=load_control()
    import sympy as sp
    G=ne.Gate
    def xor(x,y):
        return G("CX",(x,y))
    def rot(y):
        return G("G",(y,))
    def encode(head,tail):
        return [xor(head,tail),rot(tail),xor(head,tail)]
    def swap(x,y):
        return [xor(x,y),xor(y,x),xor(x,y)]
    s=G("SourceI",(2,0,1))
    blank=swap(2,7)+[s,s,rot(2),s,s]+swap(2,7)
    word=[xor(4,5)]+encode(5,6)+blank+[xor(3,7),xor(5,7)]+encode(7,8)
    word+=[xor(4,5)]+encode(5,9)+[xor(4,5)]+encode(4,10)
    ex=ne.Execution(11,(),(),tuple(word),profile=ne.G_CX_SOURCE_I,
                    source_port=2,source_spin=(0,1),report_bits=(5,6,7,8,9,10))
    body=ne.execution_from_json(ne.canonical_json(ex),max_qubits=11,max_expanded_stages=28)
    need(body.gates==tuple(word) and Counter(g.op for g in word)==
         {"CX":19,"G":5,"SourceI":4},"whole native word, raw calls including all port routing")
    # The routed blank proof acts on all 16 Spin, port, and destination columns.
    sm=G("SourceI",(2,0,1))
    loc=swap(2,3)+[sm,sm,rot(2),sm,sm]+swap(2,3)
    unit=ne.Execution(4,(),(),tuple(loc),profile=ne.G_CX_SOURCE_I,source_port=2,source_spin=(0,1))
    uw=ne.word_matrix(unit,max_qubits=4,max_expanded_stages=11)
    need(ne.exact_matrix_equal(uw,sp.kronecker_product(sp.eye(8),ne.G_LOCAL.T)),
         "independently entangled dirty port and old Spin are restored")
    vv=sp.Matrix([ne.A,ne.P])
    for bit in (0,1):
        target=ne.G_LOCAL if bit==0 else ne.G_LOCAL.T
        e=ne.Execution(2,(),(),tuple(encode(0,1)))
        u=ne.word_matrix(e,max_qubits=2,max_expanded_stages=3)
        need(ne.exact_matrix_equal(u[2*bit:2*bit+2,2*bit:2*bit+2],target) and
             ne.exact_matrix_equal(u[2*bit:2*bit+2,2*(1-bit):2*(1-bit)+2],sp.zeros(2)),
             "NC1 on each dirty tail column")
        need(ne.exact_matrix_equal(vv.T*target*vv,sp.Matrix([ne.A])),"exact local cold scalar")
    return digest, [[g.op,*g.wires] for g in word]


def letter(head,tail):
    return "0" if not head else ("10" if not tail else "11")


def terminal(t,d,c,fd,fc,fx,ft):
    return (letter(d,fd),letter(c,fc),letter(t^d,fx),letter(t,ft))


def traces():
    weights=(p,p**2)
    invalid=0
    for h,t in product(range(2),repeat=2):
        rooted=Counter()
        raw=Counter()
        for d,c,fd,fc,fx,ft in product((0,1),repeat=6):
            row=terminal(t,d,c,fd,fc,fx,ft)
            born=gold(1)
            for bit in (d,c,fd,fc,fx,ft):
                born*=weights[bit]
            rooted[row]+=born
            # D is the incoming raw D bit XOR T; the routed blank gives C=H XOR D.
            mass=weights[d^t]
            if c!=(h^d):
                mass=gold(0)
            for head,tail in ((d,fd),(c,fc),(t^d,fx),(t,ft)):
                if head:
                    if tail:
                        mass=gold(0)
                else:
                    mass*= (4*p**3 if tail else p**6)
            raw[row]+=mass
        need(sum(rooted.values(),gold(0))==gold(1) and sum(raw.values(),gold(0))==gold(1),
             "all Born-rooted and actual sectors, including all rejected/failure results")
        invalid+=sum("11" in r for r in rooted)
        for row,born in rooted.items():
            d=(row[0]!="0")
            c=(row[1]!="0")
            if "11" in row or c!=(h^d):
                need(raw[row]==gold(0),"initialized dark, still present on the arena")
            else:
                need(raw[row]==weights[d^t],"joint deterministic code after actual binary D")
                if h:
                    x=t^d
                    need(born==p**(4+x+t),"same physical heads: guard only adds restricted fresh tails")
                    need(sum(map(len,row))==5+x+t,"four newly serialized LC1 words")
    return invalid


def prices():
    pp=(span(5).sqrt()-1)/2
    a=pp.sqrt()
    ell=(1/pp).log_positive()
    cold=a**5*pp*(a+pp)
    need((64*cold**2).lo>1,"honest parsed circuit also spectrally retains the common prefix")
    slopes=[]
    for t in (0,1):
        u=(p**2,p)[t]
        k=p**(4+t)
        z0=p**(5+t+(0!=t))
        z1=p**(5+t+(1!=t))
        need(z0+z1==k and z1==k*u,"printed code has true conditional Kraft calibration")
        bare=z0/(1-u)+z1/u
        derivative=z0/((1-u)**2)-z1/(u**2)
        need(bare==2*k and (-derivative)/bare==gold(F(1-2*t,2)),
             "unweighted counting at true intrinsic unequal noise")
        slopes.append(((1-2*t)/(2*ell)).fmt(14))
    # Any common symmetric pointer perturbation v, including non-central v.
    for v in (gold(F(3,8)),p**2,gold(F(2,5))):
        z0=p**5/(1-v)+p**6/v
        z1=p**7/v+p**6/(1-v)
        need(z1==p*z0,"shared-noise factorization for any previous ledger")
    return {"raw_guard_cold_on_all_heads":"p I","conditional_raw_whole_cold_H1":"a^5 p (a+p) I",
            "raw_whole_cold_at_H1":cold.fmt(14),"64_times_squared_cold":(64*cold**2).fmt(14),
            "per_sector_natural_pressure_slope_in_phi_units":slopes,
            "shared_pointer_slope":(1/(2*ell)).fmt(14),
            "paired_net_mean_per_copy":"4+T","native_cost_info_selection_proved":False}


if __name__=="__main__":
    digest,word=controller()
    print(json.dumps({"status":"PASS","source_sha256":digest,"births":6,"primitive_square_calls":28,
        "square_word":word,"raw_stages":34,"register_at_raw_ticks":[10,26,30,34],
        "wire_order":["Spin0","Spin1","port","H","T","D","tail_D","C","tail_C","tail_X","tail_T"],
        "all_input_space_dimension":2048,
        "verified_by":"native validation; factorization on all columns; exhaustive final joint sector enumeration",
        "distinct_dark_invalid_rows_summed_across_H_T":traces(),**prices()},indent=2))
