"""Check the sharp two-sector bound with the canonical native controlled quarter turn."""
import json
import math
import numpy as np


def entropy(state):
    values = np.linalg.eigvalsh((state+state.conj().T)/2)
    assert values.min() > -1e-11
    positive = values[values > 1e-13]
    return float(-np.sum(positive*np.log(positive)))


def h(x):
    return -x*math.log(x)-(1-x)*math.log1p(-x)


def main():
    p=(math.sqrt(5)-1)/2
    v=np.array([math.sqrt(p),p])
    spin=np.kron(np.eye(2),np.array([[0,-1],[1,0]]))
    assert np.array_equal(spin@spin,-np.eye(4))
    # Equal occupation in two opposite sectors, entangled with a two-state old reference.
    plus=np.array([1,-1j,0,0])/math.sqrt(2)
    minus=plus.conj()
    assert np.allclose(spin@plus,1j*plus) and np.allclose(spin@minus,-1j*minus)
    base=np.column_stack([plus,minus])/math.sqrt(2)  # indices Spin, R
    data0=base@base.conj().T
    bank=[base]
    output={}
    for n in range(1,7):
        bank=[v[b]*(spin@old if b else old) for old in bank for b in (0,1)]
        vec=np.stack(bank,axis=0)
        data=np.einsum("asr,atr->st",vec,vec.conj(),optimize=False)
        closed=np.einsum("asr,atu->srtu",vec,vec.conj(),optimize=False).reshape(8,8)
        hidden=entropy(closed)-(entropy(data)-entropy(data0))
        target=h((1-p**(3*n))/2)
        assert abs(hidden-target)<1e-12 and hidden<math.log(2)
        # If each new control actually is read and the remaining full quantum block kept,
        # conditionally the evolution of the old input is unitary/isometric.
        probs=np.einsum("asr,asr->a",vec,vec.conj(),optimize=False).real
        hwords=float(-np.sum(probs*np.log(probs)))
        joint_report=hwords
        data_report=hwords + sum(prob*entropy(old@old.conj().T/prob) for prob,old in zip(probs,vec))-entropy(data0)
        assert abs(data_report-joint_report)<1e-12 and abs(hwords-n*h(p*p))<1e-12
        output[n]=dict(hidden_work_reference_gap=round(hidden,11),
                       full_read_reference_gap=round(abs(data_report-joint_report),11))
    return dict(status="PASS",source="native controlled L_i, canonical birth",
                analytic_hidden_work_gap="h((1-p^(3M))/2)",data=output,
                proves_full_physical_binding=False)


if __name__=="__main__":
    print(json.dumps(main(),indent=2))
