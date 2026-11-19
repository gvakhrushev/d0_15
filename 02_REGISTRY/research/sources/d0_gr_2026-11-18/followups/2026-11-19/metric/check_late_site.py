"""Chronological marks and a late real SITE read: exact native erasure law and mixed CQ spectra."""
import json
from itertools import product
from fractions import Fraction as F
import numpy as np
from check_boundary_experiment import Golden as G
from check_full_site_sort import q_report
from check_golden_work_gauge import load_owner

one,zero,p=G(1),G(0),G(0,1)
def gd(q): return float(q.decimal())


def entropy(A):
    s=np.linalg.eigvalsh(A)
    assert min(s)>-1e-13
    s=s[s>1e-14]
    return -sum(s*np.log(s))


def scalar_h(q):
    return -q*np.log(q)-(1-q)*np.log(1-q)


def exact_native_site_read():
    n,_=load_owner()
    import sympy as sp
    gate=lambda a,b:n.Gate("CX",(a,b))
    route=(gate(2,3),n.Gate("G",(3,)),gate(2,3))
    ex=n.Execution(4,(),(),route,profile=n.G_CX_SOURCE_I,source_port=2,source_spin=(0,1),report_bits=(2,3))
    V=n.word_matrix(ex)*sp.kronecker_product(sp.eye(8),sp.Matrix([n.A,n.P]))
    for x in (0,1):
        E=sp.kronecker_product(sp.eye(4),sp.diag(1-x,x),sp.eye(2))
        mirror=sp.kronecker_product(sp.eye(4),sp.diag(1-x,x))
        assert n.exact_matrix_equal(V.T*E*V,mirror)
    return len(route)


def native_channel():
    # z0,z1 are independent genuine Golden records. Their early copies are
    # attached to visit times; after reading x the remaining order is recoverable.
    rows=({}, {})
    for x in (0,1):
        for a,b in product((0,1),repeat=2):
            z=(a,b)
            weight=(p**2 if a else p)*(p**2 if b else p)
            rows[x][(z[x],z[1-x],a,b)]=weight
    keys=tuple(sorted(set(rows[0])|set(rows[1])))
    reveal=sum((rows[0].get(k,zero) for k in keys if k not in rows[1]),zero)
    assert reveal==G(2)*p**3
    return np.array([[gd(r.get(k,zero)) for k in keys] for r in rows]),reveal


def entropic_tests():
    P,reveal=native_channel()
    # Noncommuting mixed density on SITE x retained RIGHT; also test a genuinely
    # classical old address with the same diagonal and pure native empty-history input.
    T=np.array([[1.,0,1,0],[0,2,0,1],[1,1,0,1],[0,0,1,2]])
    mixed=T@T.T/np.trace(T@T.T)
    diag=mixed.copy()
    diag[:2,2:]=0;diag[2:,:2]=0
    born=np.array([np.sqrt(gd(p)),0,gd(p),0])
    records=[]
    for rho in (mixed,diag,np.outer(born,born)):
        dephased=rho.copy();dephased[:2,2:]=0;dephased[2:,:2]=0
        C=entropy(dephased)-entropy(rho)
        base=2*scalar_h(gd(p**2))
        for k in (1,2,3):
            pre,post=0.,0.
            for z in product(range(P.shape[1]), repeat=k):
                m=np.prod(P[:,z],axis=1)
                if not m.any():continue
                R=np.diag(np.repeat(np.sqrt(m),2))
                B=R@rho@R
                pre+=entropy(B)
                for a in (0,1):post+=entropy(B[2*a:2*a+2,2*a:2*a+2])
            eta=pre-entropy(rho)-k*base
            assert abs(eta-(1-(1-gd(reveal))**k)*C)<1e-11
            assert abs(post-entropy(rho)-k*base-C)<1e-11
            records.append({"K":k,"old_coherence_nats":round(C,13),"early_entropy_excess_nats":round(eta,13)})
    return records


def physical_average():
    # Literal periodic matter grid F1. The old prior is moving and is used
    # directly: on each branch, pick the actual first visited outcome.
    H=F(1,4)
    psi=(F(0),H/4,F(0),H/2)
    mom=[((psi[(i+1)%4]-psi[i])/H)**2 for i in range(4)]
    priors=[(F(1,4),)*4,(F(1,3),F(1,3),F(1,6),F(1,6))]
    qs=[q_report(zero,G(-m/64)) for m in mom]
    means=[sum((G(mu)*q for mu,q in zip(weights,qs)),zero) for weights in priors]
    assert means[1]-means[0]==G(F(1,6))*(qs[0]-qs[2])!=zero
    matched=[sum((G(w)*q_report(zero,G(-m/(64*4*w))) for w,m in zip(weights,mom)),zero) for weights in priors]
    assert matched[0]==means[0] and matched[1]!=means[1]
    return {"fixed_report_table_old_only":[q.decimal() for q in means],
            "regenerated_PF_and_inverse_PF_inputs":[q.decimal() for q in matched]}


if __name__=="__main__":
    print(json.dumps({"status":"PASS","native_terminal_SITE_read_square_calls_per_bit":exact_native_site_read(),
          "grid_4power4_last_only":{"bits":8,"births":8,"square_calls":24},
          "golden_pair_reveal_probability":(G(2)*p**3).decimal(),
          "mixed_right_and_native_input_CQ_checks":entropic_tests(),
          "actual_F1_SC1_first_visit_two_old_PF_means":physical_average(),
          "large_geometric_words_emitted":False,"full_book_valuation_identified":False},sort_keys=True,indent=2))
