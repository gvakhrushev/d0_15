#!/usr/bin/env python3
"""Narrow controls for the new adapter; no historical checker is imported.

The state test uses the OWNED cap-one H instrument: CZ failure I, subsequent
X-cycle failure after CZ, and both corrected H success signs, followed by ALL
four Bell labels. Its actual probabilities use s=4p^3. Quantum abort work,
original RIGHT and the downstream coherent two-outcome channel are retained.
Only reported prefix/Bell labels acquire the additional output-DATA tag.
This is a finite diagnostic of the proved arbitrary-d composition, not a
new verification of every literal Golden letter or of physical cut admission.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
from fractions import Fraction as F

import numpy as np

HERE = Path(__file__).resolve().parent
CHECKS = []


def require(name, truth, detail=None):
    if not bool(truth):
        raise RuntimeError(f"FAILED {name}: {detail}")
    CHECKS.append(name)


def close(name, lhs, rhs, tol=3e-12):
    err = float(np.max(np.abs(np.asarray(lhs) - np.asarray(rhs))))
    require(name, err <= tol, err)


def entropy(rho, ell):
    vals = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    require("entropy density positive", float(vals.min()) >= -2e-12)
    vals = vals[vals > 1e-13]
    return float(-np.dot(vals, np.log(vals)) / ell)


def right_gram(matrix):
    return matrix.conj().T @ matrix


def bell_blocks(U, C):
    # Axes are D,A,O,R. Actual basis change: CNOT(D,A), then H(D).
    omega = U.T / math.sqrt(2)
    init = np.einsum("dr,ao->daor", C, omega)
    after_cnot = np.zeros_like(init)
    for d in range(2):
        for a in range(2):
            after_cnot[d, a ^ d] = init[d, a]
    H = np.array([[1, 1], [1, -1]], float) / math.sqrt(2)
    after_h = np.einsum("ed,daor->eaor", H, after_cnot)
    return after_cnot, after_h


def adapter_state(U, C, s, channel):
    # E = T(10) D(2) A(2) old-H-work(2) original-record(2).
    # Untraced complement before the explicit tag is O(2) R(2).
    mat = np.zeros((10 * 16, 4), complex)
    after_cnot, bell = bell_blocks(U, C)
    plus = np.array([1, 1]) / math.sqrt(2)
    minus = np.array([1, -1]) / math.sqrt(2)
    weights = [1-s, s*(1-s)] + [s*s/8] * 8

    def put(t, d, a, h, j, block, scale):
        e = t*16 + d*8 + a*4 + h*2 + j
        mat[e, :] += scale * block.reshape(-1)

    for d in range(2):
        for a in range(2):
            for h in range(2):
                # CZ cap-abort: its failure map is scalar identity.
                put(0, d, a, h, 0, after_cnot[d, a],
                    math.sqrt(1-s)*plus[h])
                # CZ ready but X-cycle cap-abort: retain the full CZ state.
                put(1, d, a, h, 0, after_cnot[d, a],
                    math.sqrt(s*(1-s))*plus[h]*((-1)**(d*h)))

    for sign, work in enumerate((plus, minus)):
        for d in range(2):
            for a in range(2):
                label = 2*d+a
                t = 2 + 4*sign + label
                output = 2*bell[d, a]  # normalized U P C
                outputs = [K @ output for K in channel] if label == 0 else [output]
                for j, block in enumerate(outputs):
                    for h in range(2):
                        put(t, d, a, h, j, block,
                            math.sqrt(weights[t])*work[h])

    # An actual CNOT copy of T to Q: columns become (O,R,Q).
    tagged = np.zeros((160, 40), complex)
    for t in range(10):
        tagged[t*16:(t+1)*16, t*4:(t+1)*4] = mat[t*16:(t+1)*16]
    return mat, tagged, np.array(weights)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    repo = Path(args.repo)
    pins = json.loads((HERE / "SOURCE_PINS.json").read_text())
    for entry in pins["sources"]:
        data = subprocess.check_output(
            ["git", "-C", str(repo), "show", f'{pins["source_ref"]}:{entry["path"]}'])
        require("historical source " + entry["path"],
                hashlib.sha256(data).hexdigest() == entry["sha256"])

    # Exact real rational targets and literal whole-row permutation inventory.
    Q = [[F(3,5), -F(4,5)], [F(4,5), F(3,5)]]
    for i in range(2):
        for j in range(2):
            require("exact rational orthogonal entry", sum(Q[k][i]*Q[k][j]
                    for k in range(2)) == (1 if i == j else 0))
    inventory = []
    for order in ((0,1,2), (1,2,0), (2,0,1)):
        slots = ["row0", "row1", "row2", "blank"]
        calls = []
        for row in order:
            # Each whole pair has two qubits, each SWAP three directed CNOTs.
            slots[row], slots[3] = slots[3], slots[row]
            for bit in range(2):
                calls.extend([(3,row,bit), (row,3,bit), (3,row,bit)])
        require("last row is active", slots[3] == f"row{order[-1]}")
        require("no row or blank erased", sorted(slots) == ["blank","row0","row1","row2"])
        inventory.append(sorted(calls))
    require("same addressed CNOT inventory", inventory[0] == inventory[1] == inventory[2])

    phi = (1+math.sqrt(5))/2
    p = 1/phi
    ell = math.log(phi)
    s = 4*p**3
    close("actual Golden cap-one failure", 1-s, p**6)
    close("actual H cap-one readiness", s*s, (1-p**6)**2)
    gamma = s*s/4
    require("Bell readiness includes paid H", 0 < gamma < F(1,4))

    # Fundamental false-mixture control and its paid-tag repair.
    bare = np.array([[1],[1]], complex)/math.sqrt(2)
    copied = np.eye(2)/math.sqrt(2)
    close("untagged coherent flag entropy", entropy(bare@bare.conj().T, ell), 0)
    close("tagged entropy", entropy(copied@copied.T, ell), math.log(2)/ell)
    require("untagged mixture formula is false", math.log(2)/ell > 1)

    C = np.diag([math.sqrt(F(3,4)), math.sqrt(F(1,4))])
    G = right_gram(C)
    I = np.eye(2)
    X = np.array([[0,1],[1,0]], float)
    Z = np.diag([1,-1])
    targets = [I, np.array(Q, float)]
    channel = [math.sqrt(F(3,4))*I, math.sqrt(F(1,4))*Z]
    cost = [1., 3.]
    A = sum(c*K.T@K for c,K in zip(cost,channel))
    # Literal OWNED G/CNOT inventory; actual common bank/controller/reading/
    # storage charges are additional, not declared zero. They cancel from the
    # comparison exactly and are kept as an additive symbol in the proof.
    # Five raw bits (CZ1, X2, Bell2), with unused slots zero, are all copied to Q.
    known_branch_costs = np.array([27.,37.]+[42.]*4+[43.]*4)
    known_prefix_mean_cost = 27+10*s+5.5*s*s
    all_results = []

    for row, U in enumerate(targets):
        # All four Bell effects, full input columns, and reference preservation.
        _, bell = bell_blocks(U, C)
        for d in range(2):
            for a in range(2):
                P = np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,d)
                close("full Bell operator action", 2*bell[d,a], U@P@C)
                close("every Bell label preserves full RIGHT", right_gram(2*bell[d,a]), G)
                close("every Bell effect", (U@P/2).T@(U@P/2), I/4)

        raw, tagged, w = adapter_state(U, C, s, channel)
        close("complete actual H/Bell branch law", w.sum(), 1)
        close("literal paid G/CNOT mean includes five tag copies",
              float(np.dot(w,known_branch_costs)), known_prefix_mean_cost)
        close("full untagged state normalized", np.vdot(raw, raw), 1)
        close("full tagged state normalized", np.vdot(tagged, tagged), 1)
        rho_raw = raw@raw.conj().T
        rho_tag = tagged@tagged.conj().T
        S_raw, S_tag = entropy(rho_raw, ell), entropy(rho_tag, ell)
        H_w = -float(np.dot(w,np.log(w)))/ell
        branch_entropies = []
        for t in range(10):
            v = raw[t*16:(t+1)*16]/math.sqrt(w[t])
            branch_entropies.append(entropy(v@v.conj().T,ell))
            # Trace all branch quantum work except original RIGHT.
            tensor = v.reshape(16,2,2)
            reduced_R = np.einsum("eor,eos->rs", tensor.conj(), tensor)
            close("actual coarse branch RIGHT unchanged", reduced_R, G)

        Ck = U@C
        env = np.stack([(K@Ck).reshape(-1) for K in channel])
        S_original = entropy(env@env.conj().T,ell)
        original_charge = float(np.trace(Ck@Ck.T@A))
        F_original = original_charge-S_original
        abort_entropy = sum(w[t]*branch_entropies[t] for t in (0,1))
        baseline = known_prefix_mean_cost-H_w-abort_entropy
        exact_price = known_prefix_mean_cost+gamma*original_charge-S_tag
        close("tagged full mixture identity", S_tag, H_w+float(np.dot(w,branch_entropies)))
        close("original downstream coherent entropy retained", S_tag,
              H_w+abort_entropy+gamma*S_original)
        close("known-gate ledger affine orbit-price identity", exact_price,
              baseline+gamma*F_original)
        require("unmodified coherent cut does not have tagged price", abs(S_raw-S_tag)>1e-4)
        all_results.append(dict(row=row, baseline=baseline, price=exact_price,
                                original_price=F_original, tagged_entropy=S_tag,
                                untagged_entropy=S_raw,
                                abort_entropies=branch_entropies[:2]))

    close("both real abort entropies row independent",
          all_results[0]["abort_entropies"], all_results[1]["abort_entropies"])
    require("abort entropy not discarded", max(all_results[0]["abort_entropies"])>0.1)
    close("whole prefix baseline row independent", all_results[0]["baseline"],
          all_results[1]["baseline"])
    close("actual full contrast is Gamma times old input contrast",
          all_results[1]["price"]-all_results[0]["price"],
          gamma*(all_results[1]["original_price"]-all_results[0]["original_price"]))
    require("nontrivial old input contrast", abs(all_results[1]["original_price"]-
            all_results[0]["original_price"])>0.01)

    receipt = {
        "status":"PASS", "checks":len(CHECKS),
        "source_ref":pins["source_ref"],
        "proof_sha256":hashlib.sha256((HERE/"TAGGED_PAID_ORBIT_INPUT.md").read_bytes()).hexdigest(),
        "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_pins_sha256":hashlib.sha256((HERE/"SOURCE_PINS.json").read_bytes()).hexdigest(),
        "actual_cap_one_H_readiness":s*s, "actual_Bell_zero_gain":gamma,
        "known_G_CNOT_branch_counts":known_branch_costs.tolist(),
        "known_G_CNOT_prefix_mean_cost":known_prefix_mean_cost,
        "additional_actual_prefix_charges":"Common bank/controller/reading/storage charges are retained symbolically in the proof, not assigned zero by the diagnostic.",
        "fixture_rows":all_results,
        "scope":"Narrow cap-one paid H/Bell, literal known G/CNOT ledger including five tag copies, all reported labels, original RIGHT and coherent downstream record. Extra common actual prefix charges remain symbolic. Historical gate/GR suites not replayed; no physical cut or controller admission claimed."
    }
    Path(args.output).write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS", "checks":len(CHECKS), "output":args.output}))


if __name__ == "__main__":
    main()
