#!/usr/bin/env python3
"""Narrow new controls: two-effect source projection and native full128 parity.

Imports only functions from the pinned original normalization owner. Does not
run that owner's main/exact_checks/primary_application or any historical suite.
The original full128 source is numerical; the independent small controls use
exact Fraction arithmetic and explicit noncommuting two-block effects.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

import numpy as np


NAMES: list[str] = []
HERE = Path(__file__).resolve().parent
PROOF = "BOOK_SOURCE_SUFFICIENCY_AND_NATIVE_PARITY.md"
OWNER = "02_REGISTRY/research/sources/d0_full128_normalization_closure_2026-10-21/check_normalization.py"


def require(ok: bool, label: str) -> None:
    if not bool(ok):
        raise ArithmeticError(label)
    NAMES.append(label)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(s, a):
    return [[F(s) * x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n)), F(0))
             for j in range(n)] for i in range(n)]


def tr(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def inv(a):
    n = len(a)
    aug = [row[:] + eye for row, eye in zip(a, ident(n))]
    for j in range(n):
        pivot = next(k for k in range(j, n) if aug[k][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        div = aug[j][j]
        aug[j] = [x / div for x in aug[j]]
        for i in range(n):
            if i != j:
                fac = aug[i][j]
                aug[i] = [x - fac * y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def block(a, b):
    out = zero(4)
    for i in range(2):
        for j in range(2):
            out[i][j], out[i+2][j+2] = a[i][j], b[i][j]
    return out


def expectation(a, size=2):
    return [[x if i // size == j // size else F(0)
             for j, x in enumerate(row)] for i, row in enumerate(a)]


def quadratic(inverse, jet):
    return tr(mul(mul(mul(inverse, jet), inverse), jet))


def exact_controls() -> dict:
    n = block(mat([[F(3,5), F(1,10)], [F(1,10), F(4,5)]]),
              mat([[F(4,5), F(-1,10)], [F(-1,10), F(3,5)]]))
    b = block(mat([[F(1,5), 0], [0, F(3,10)]]),
              mat([[F(3,10), F(1,20)], [F(1,20), F(1,5)]]))
    dn = mat([[F(1,7), F(1,11), F(2,9), F(1,5)],
              [F(1,11), F(-2,7), F(-1,6), F(3,10)],
              [F(2,9), F(-1,6), F(1,8), F(1,13)],
              [F(1,5), F(3,10), F(1,13), F(-1,8)]])
    db = mat([[F(2,9), F(-1,12), F(1,7), F(-1,8)],
              [F(-1,12), F(1,6), F(1,4), F(1,9)],
              [F(1,7), F(1,4), F(-1,6), F(1,10)],
              [F(-1,8), F(1,9), F(1,10), F(1,5)]])
    z, dz = F(1,3), F(2,7)
    q = add(scale(1-z, n), scale(z, b))
    ni, qi = inv(n), inv(q)
    require(mul(n, b) != mul(b, n), "exact source control has noncommuting anchor effects")
    for label, x in (("N", n), ("B", b), ("N-B", sub(n,b))):
        require(all(x[j][j] > 0 and x[j][j]*x[j+1][j+1] > x[j][j+1]**2
                    for j in (0,2)), f"exact {label} is strictly positive")
    require(expectation(n) == n and expectation(b) == b,
            "exact anchor lies in the two-block algebra")
    dn_e, db_e = expectation(dn), expectation(db)
    def qjet(nn, bb):
        return add(add(scale(1-z,nn),scale(z,bb)),scale(dz,sub(b,n)))
    dq, dq_e = qjet(dn,db), qjet(dn_e,db_e)
    source = tr(mul(ni,dn))-tr(mul(qi,dq))
    reduced = tr(mul(ni,dn_e))-tr(mul(qi,dq_e))
    require(source == reduced and source != 0,
            "exact nonzero first source survives projection including moving z")
    kn, kb = sub(ni,scale(1-z,qi)), scale(z,qi)
    require(expectation(kn) == kn and expectation(kb) == kb,
            "exact source-gradient matrices remain in the retained algebra")
    require(scale(z,inv(kb)) == q and
            inv(add(kn,scale((1-z)/z,kb))) == n,
            "exact gradients reconstruct the original effects")
    # N(s),B(s),z(s) affine; Q has its genuine nonzero acceleration.
    ddq = scale(2*dz,sub(db,dn))
    ddq_e = scale(2*dz,sub(db_e,dn_e))
    hess = -quadratic(ni,dn)+quadratic(qi,dq)-tr(mul(qi,ddq))
    hess_e = -quadratic(ni,dn_e)+quadratic(qi,dq_e)-tr(mul(qi,ddq_e))
    defect = quadratic(qi,sub(dq,dq_e))-quadratic(ni,sub(dn,dn_e))
    require(hess-hess_e == defect and defect != 0,
            "exact Hessian defect includes every moving-z acceleration term")
    x = mat([[0,1],[1,0]])
    pos = quadratic(scale(F(4,3),ident(2)),scale(F(1,2),x))
    neg = -quadratic(scale(2,ident(2)),x)
    require(pos == F(8,9), "unmarked off-algebra Hessian defect is exactly 8/9")
    require(neg == -8, "marked off-algebra Hessian defect can be exactly -8")
    require(expectation(x,1) == zero(2), "Hessian controls discard only off-diagonal jets")
    return {"noncommuting_source":str(source), "noncommuting_hessian_defect":str(defect),
            "positive_hessian_defect":str(pos), "negative_hessian_defect":str(neg)}


def verify_pins(repo: Path) -> dict:
    pins = json.loads((HERE / "SOURCE_PINS.json").read_text())
    ref = pins["source_ref"]
    for item in pins["sources"]:
        data = subprocess.run(["git","-C",str(repo),"show",f"{ref}:{item['path']}"],
                              check=True, capture_output=True).stdout
        require(sha(data) == item["sha256"], "historical source pin: " + item["path"])
    owner_pin = next(x["sha256"] for x in pins["sources"] if x["path"] == OWNER)
    require(sha((repo/OWNER).read_bytes()) == owner_pin,
            "imported current owner bytes match the historical scientific pin")
    return pins


def native_application(repo: Path) -> dict:
    spec = importlib.util.spec_from_file_location("pinned_native_normalization", repo / OWNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the pinned owner")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    require(m.CHECKS == [], "import did not run the historical test suite")
    theta, t, z, right = .08, .7, m.Z, m.RIGHT
    k, dk, _, _ = m.native(theta)
    parity = np.diag([(-1)**j.bit_count() for j in range(16)])
    sectors = [np.array([j for j in range(16) if (-1)**j.bit_count() == sign])
               for sign in (1,-1)]
    require(all(len(s) == 8 for s in sectors), "actual CAR parity sectors have ranks 8 and 8")
    for r,c in enumerate(m.creators()):
        require(np.array_equal(parity@c@parity,-c), f"integer original creator {r} is odd")
    defects = [m.hs(parity@k[h]@parity-(-1)**((h//2)%2)*k[h]) for h in range(128)]
    jet_defects = [m.hs(parity@dk[h]@parity-(-1)**((h//2)%2)*dk[h]) for h in range(128)]
    require(max(defects) < 2e-12, "all128 actual Golden Kraus operators have their declared parity")
    require(max(jet_defects) < 2e-12, "all128 original analytic defect and field jets have the same parity")
    zeros = np.zeros_like(m.I)
    cost = np.tile([1.,2.],64)
    weights = np.exp(-t*cost)
    n1,dn1 = m.transfer(k,dk,m.I,zeros,weights)
    n,dn = m.transfer(k,dk,n1,dn1,weights)
    a = np.exp(-t)*k[0]@k[0]
    da = np.exp(-t)*(dk[0]@k[0]+k[0]@dk[0])
    b = m.adj(a)@a
    db = m.adj(da)@a+m.adj(a)@da
    def expect(x):
        return (x+parity@x@parity)/2
    for label,x in (("N",n),("B",b),("DN",dn),("DB",db)):
        require(m.hs(x-expect(x)) < 2e-12, "actual original " + label + " is parity even")
    eig = np.linalg.eigvalsh(n)
    require(eig[-1]-eig[0] > 1e-5, "original two-round cost normalizer is genuinely nonscalar")
    require(eig[0] >= np.exp(-4*t)-2e-12 and eig[-1] <= np.exp(-2*t)+2e-12,
            "original finite all-history cost bounds hold")
    require(np.linalg.eigvalsh(b).min() > 0 and np.linalg.eigvalsh(n-b).min() > 0,
            "original two effects are inside the strict positive ambient chart")
    q = (1-z)*n+z*b
    ni,qi = np.linalg.inv(n),np.linalg.inv(q)
    kn,kb = ni-(1-z)*qi,z*qi
    require(np.linalg.eigvalsh(kn).min() > -2e-12 and np.linalg.eigvalsh(kb).min() > 0,
            "actual original source weights have the proved signs")
    def source(nn,bb,zz=0.0):
        return right*m.real_trace(kn@nn-kb@bb+zz*qi@(n-b))
    def block_sources(nn,bb,zz=0.0):
        out=[]
        for ss in sectors:
            ix=np.ix_(ss,ss)
            dq=(1-z)*nn[ix]+z*bb[ix]+zz*(b[ix]-n[ix])
            out.append(right*(m.real_trace(np.linalg.solve(n[ix],nn[ix]))
                              -m.real_trace(np.linalg.solve(q[ix],dq))))
        return out
    dj = source(dn,db)
    block_dj = block_sources(dn,db)
    owned = m.normalized_complement(n,dn,a,da)
    require(abs(dj-owned["dj"]) < 2e-12,
            "new source-gradient formula matches original polar complement")
    require(abs(sum(block_dj)-dj) < 2e-12,
            "both actual parity blocks reconstruct the complete original field source")
    require(abs(dj) > 1e-6, "actual source-sufficiency application has a nonzero field source")
    jblocks=[right*(m.logdet(n[np.ix_(ss,ss)])-m.logdet(q[np.ix_(ss,ss)]))
             for ss in sectors]
    require(abs(sum(jblocks)-owned["j"]) < 2e-11,
            "ordinary full trace equals both block traces with oldRIGHT128")
    require(abs(sum(jblocks)-jblocks[0]) > 1e-7,
            "dropping the second parity block changes the Book price")
    require(abs(dj+right*m.real_trace(kb@db)) > 1e-9,
            "freezing the actual nonscalar normalizer changes the first source")
    # General ambient odd-parity directions are not asserted to be native gates.
    odd_n=np.zeros_like(m.I); odd_n[0,1]=odd_n[1,0]=F(1,5)
    odd_b=np.zeros_like(m.I); odd_b[0,2]=.13j; odd_b[2,0]=-.13j
    require(m.hs(expect(odd_n))+m.hs(expect(odd_b)) == 0,
            "ambient controls are exactly off the parity algebra")
    require(abs(source(dn+odd_n,db+odd_b)-dj) < 2e-12,
            "off-algebra ambient effect jets do not alter the first source")
    moving_z=1/7
    require(abs(source(dn+odd_n,db+odd_b,moving_z)
                -sum(block_sources(dn+odd_n,db+odd_b,moving_z))) < 2e-11,
            "moving-z source retains the same exact two-block interface")
    # Genuine mark derivative, using its recurrence and every original outcome.
    zero_k=np.zeros_like(k)
    dw=-cost*weights
    n1t=m.transfer(k,zero_k,m.I,zeros,dw)[0]
    nt=(m.transfer(k,zero_k,n1,zeros,dw)[0]
        +m.transfer(k,zero_k,n1t,zeros,weights)[0])
    bt=-2*b
    require(m.hs(expect(nt)-nt) < 2e-12,
            "actual moving-cost-mark normalizer derivative is parity even")
    marker_source=source(nt,bt)
    require(abs(marker_source-sum(block_sources(nt,bt))) < 2e-11,
            "cost-mark source is reconstructed without dropping its normalization jet")
    qperp=z*odd_b
    actual_hessian_defect=right*m.real_trace(qi@qperp@qi@qperp)
    require(actual_hessian_defect > 1e-12,
            "actual anchor has a positive missing Hessian for a pure off-parity B jet")
    # Same Kraus data also evaluate the genuine unmarked execution; no new map.
    unmarked_a=k[0]@k[0]
    unmarked_da=dk[0]@k[0]+k[0]@dk[0]
    unmarked_b=m.adj(unmarked_a)@unmarked_a
    unmarked_db=m.adj(unmarked_da)@unmarked_a+m.adj(unmarked_a)@unmarked_da
    unmarked_q=(1-z)*m.I+z*unmarked_b
    unmarked_source=-right*z*m.real_trace(np.linalg.solve(unmarked_q,unmarked_db))
    unmarked_blocks=[-right*z*m.real_trace(np.linalg.solve(
        unmarked_q[np.ix_(ss,ss)],unmarked_db[np.ix_(ss,ss)])) for ss in sectors]
    require(abs(unmarked_source-sum(unmarked_blocks)) < 2e-12
            and abs(unmarked_source) > 1e-6,
            "unchanged unmarked native execution has the same nonzero block-source interface")
    require(m.CHECKS == [], "no imported historical checker or primary replay was invoked")
    return {"theta":theta,"cost_marker_t":t,"rounds":2,
            "outcomes_per_round":128,"retained_word_count":128**2,
            "input_dimension":16,"parity_ranks":[8,8],"oldRIGHT_trace_multiplicity":right,
            "native_kraus_parity_error":max(defects),"native_jet_parity_error":max(jet_defects),
            "normalizer_eigenvalue_spread":float(eig[-1]-eig[0]),
            "full_feedback":float(owned["j"]),"parity_feedbacks":list(map(float,jblocks)),
            "full_field_source":float(dj),"parity_field_sources":list(map(float,block_dj)),
            "cost_marker_source":float(marker_source),
            "unmarked_field_source":float(unmarked_source),
            "unmarked_parity_sources":list(map(float,unmarked_blocks)),
            "ambient_off_parity_hessian_defect":float(actual_hessian_defect),
            "scope":"original full128 Fourier fixture, exact supplied cut; numerical source control, not a new physical Info/cut or forgetting operation"}


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    pins=verify_pins(args.repo.resolve())
    exact=exact_controls()
    native=native_application(args.repo.resolve())
    result={"status":"PASS","checks":len(NAMES),"names":NAMES,
            "source_ref":pins["source_ref"],"source_pins_sha256":sha((HERE/"SOURCE_PINS.json").read_bytes()),
            "proof_sha256":sha((HERE/PROOF).read_bytes()),"checker_sha256":sha(Path(__file__).read_bytes()),
            "exact_controls":exact,"native_application":native,
            "not_claimed":["Book Info or full Cost-Info equality","physical conditional-expectation instrument",
                           "same-controller selection","full HJR/GR closure","ambient Hessian preservation"]}
    out=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(out)
    else:
        print(out,end="")


if __name__ == "__main__":
    main()
