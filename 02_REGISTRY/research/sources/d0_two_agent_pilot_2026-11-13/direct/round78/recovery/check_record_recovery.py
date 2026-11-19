"""Two real archived runs lower-bound the failure to restore the original blank DATA/RIGHT."""
import hashlib
import json
import os
import sys
from fractions import Fraction as Q
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.dont_write_bytecode = True
import numpy as np

direct = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(direct / "round75/work"))
import check_pointer_weyl as W

O, I, spectral = W.O, W.I, W.spectral


def diag(a):
    return I(np.diag(a.lo), np.diag(a.hi))


def distance(target, branch):
    delta = branch - target
    # A concrete projective test on each of the original 128 labels.
    exact = diag(delta)
    abs_lo = np.maximum(np.maximum(exact.lo, -exact.hi), 0.)
    abs_hi = np.maximum(np.abs(exact.lo), np.abs(exact.hi))
    tv = O.reduce_sum(I(abs_lo, abs_hi))*Q(1,2)
    # For the squared fidelity of the complete target, a fixed measurement gives
    # F <= (sum sqrt(s_i*t_i))^2. Use its stable Hellinger representation.
    rt, rb = diag(target).sqrt(), diag(branch).sqrt()
    hell2 = O.reduce_sum((rt-rb).square())*Q(1,2)
    loss = hell2*(I(2.)-hell2)
    O.require(tv.lo>0 and loss.lo>0, "native RIGHT labels distinguish this branch")
    return tv, loss


def purity(m):
    # Density matrices here are real symmetric.
    return O.reduce_sum(m.square())


def main():
    for path, digest in O.PINS.items():
        O.require(hashlib.sha256((W.ROOT/path).read_bytes()).hexdigest()==digest, path)
    p, C, w, _, fw, bw, _, _, _ = W.site_vector()
    kcs = [C]
    for n in range(3):
        a=C if n==0 else kcs[-1]
        for j in range(1,5):
            a=W.dirac(a,w,fw,bw)
            if j==2:
                a2=a
        kcs.append(4*p*p*(a2-p*p*a))
    ct=spectral.transpose(W.flatten(C))
    K=[I(np.eye(128)/128)] + [spectral.matmul(ct,W.flatten(a)) for a in kcs[1:]]
    O.require(spectral.matmul(ct,W.flatten(C)).contains(np.eye(128)/128),"original prior")
    G1=K[0]-K[1]
    G2=K[0]-2*K[1]+K[2]
    G2f=K[1]-2*K[2]+K[3]     # C*X^2(I-X)C, no cancellation of near-unit matrices
    P1,P2,P2f=(O.reduce_sum(diag(m)) for m in (G1,G2,G2f))
    sigma=G1/P1
    tr0=G2/P2
    tr1=G2f/P2f
    Gn=K[1]-K[2]               # zero/nonzero single retained paid bit
    Pn=O.reduce_sum(diag(Gn))
    trn=Gn/Pn
    tv0,loss0=distance(sigma,tr0)
    tv1,loss1=distance(sigma,tr1)
    tvn,lossn=distance(sigma,trn)
    w0,w10,w01=P2/P1,p*P2f/P1,p*p*P2f/P1
    first_two=w0*loss0+w10*loss1
    both_orders=first_two+w01*loss1
    one_bit=w0*loss0+(Pn/P1)*lossn
    ps, pb = purity(sigma),purity(tr1)
    O.require(pb.lo > ps.hi, "distinct conditional DATA spectra for a clean reversible return")
    data_tv = (pb-ps)/(2*(pb.sqrt()+ps.sqrt()))
    O.require(first_two.lo > 0.00007415895 and both_orders.lo > 0.0001198279,
              "positive uniform floor on DATA-side entanglement recovery")
    O.require(one_bit.lo > 0.00012065974397 and data_tv.lo > 0.0037637160,
              "one-bit archive and clean reversible DATA bounds")
    O.require((w0+w10+w01).hi < 1, "other accepted records remain")
    print(json.dumps({name:O.bounds(value) for name,value in [
        ("P1",P1),("P2",P2),("P2_minus_P3",P2f),("conditional_zero",w0),
        ("conditional_first_one",w10),("conditional_second_one",w01),
        ("TV_RIGHT_zero",tv0),("TV_RIGHT_one",tv1),
        ("conditional_infidelity_zero",loss0),("conditional_infidelity_one",loss1),
        ("infidelity_floor_first_two",first_two),("infidelity_floor_both_orders",both_orders),
        ("infidelity_floor_zero_nonzero_fee",one_bit),("TV_RIGHT_nonzero",tvn),
        ("target_purity",ps),("one_flip_purity",pb),("one_flip_clean_DATA_TV_floor",data_tv)]},
        sort_keys=True,indent=2))


if __name__=="__main__":
    main()
