"""Paired NC1 commitments, complement priors, exact joint receiver-state cancellation."""
from decimal import Decimal as D, localcontext
from itertools import product
import json

from check_paired_readers import (A, P, ONE, ZERO, INV, LAMBDA, birth, turn,
                                  cx, add, clean, partial, final_law, dec)


def polarization(rows):
    out = {}
    for key, values in rows.items():
        for pos,z in values.items():
            add(out,pos,z if key[0]==key[1] else -z)
    return clean(out)  # Twice the normalized contrast.


def receiver_timeline(psi, i, j):
    snapshots = [psi]
    masks = [[]]
    live = []
    for control, target in ((i,4),(4,5),(j,6),(6,7)):
        psi = birth(psi,target)
        live = live+[target]
        snapshots.append(psi)
        masks.append(live)
        for cmd in ('C','G','C'):
            psi = cx(psi,control,target) if cmd=='C' else turn(psi,target)
            snapshots.append(psi)
            masks.append(live)
    return list(zip(snapshots,masks))


def binary_proof(b,l,ell):
    y=b*l
    joint=b*l*l
    m=(1-2*y+joint,y-joint,y-joint,joint)
    q=((1-y)**2,y*(1-y),y*(1-y),y*y)
    if b==0 or b==1:
        return D(0)
    return sum(v*(v/w).ln() for v,w in zip(m,q) if v)/ell


def check():
    for t in (0,1):
        answers = []
        for complement in (0,1):
            psi = {0:ONE}
            for h in (0,1):
                psi = birth(psi,h)
                if t: psi = {x^(1<<h):z for x,z in psi.items()}
                psi = turn(psi,h)
                if t: psi = {x^(1<<h):z for x,z in psi.items()}
                # This is the CX column selected by an already actually committed
                # helper, e.g. the one or zero from two different NC1 receipts.
                if complement: psi = {x^(1<<h):z for x,z in psi.items()}
            for h,shadow in ((0,2),(1,3)):
                psi = turn(birth(psi,shadow),shadow,INV)
                psi = cx(psi,h,shadow)
            programs = {(i,j):receiver_timeline(psi,i,j) for i,j in product(range(2),repeat=2)}
            signatures = []
            b=ONE-LAMBDA if t==0 else ONE
            if complement: b=ONE-b
            y=b*LAMBDA
            for key,seq in programs.items():
                joint=b*LAMBDA**2 if key[0]==key[1] else y**2
                assert final_law(seq[-1][0])==(ONE-y-y+joint,y-joint,y-joint,joint)
            for age in range(17):
                signatures.append(polarization({k:partial(*v[age]) for k,v in programs.items()}))
            answers.append(signatures)
        assert answers[0]==answers[1]
        assert bool(answers[0][-1])==(t==0)
    with localcontext() as ctx:
        ctx.prec=50
        phi=(1+D(5).sqrt())/2
        ell=phi.ln()
        a=(1/phi).sqrt()
        l=dec(LAMBDA,a)
        small=binary_proof(1-l,l,ell)
        large=binary_proof(l,l,ell)
        gain=small-large
        assert D('.20448')<gain<D('.20450')
        return dict(exact_joint_receiver_state_cancellation=True,snapshot_count=17,
                    conditional_old_T_values=[0,1],methods=8,
                    small_prior_gain=str(+small),large_prior_gain=str(+large),gain=str(+gain),
                    two_native_unequal_herald_mass=str(+(2/phi**3)),
                    unconditioned_gain_if_this_herald_is_needed=str(+(2/phi**3*gain)),
                    price_can_include="both receiver instruments and old reference for an affine common valuation",
                    outside="new hidden sources and shadows, protocol-selector access, nonlinear state tariffs, unverified routes",
                    full_CD13=False)


if __name__ == '__main__':
    print(json.dumps(check(),sort_keys=True,indent=2))
