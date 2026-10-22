#!/usr/bin/env python3
"""Tiny rational integration control for the finite quantum price reduction.

This is NOT new native full128 evidence. Only 2(K+1) binary stopped words are
enumerated. Exact rational controls accompany positive two-dimensional matrix
logarithms and a finite-difference Poisson source test. No clipping or historic
suite is used. Default execution compares an immutable receipt and never
writes it. All explicit checks survive python -O.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import numpy as np

ELL = float(np.log((1+np.sqrt(5.0))/2))
I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)
CHECKS = []
PRICE_TOL = 2e-11
SOURCE_TOL = 2e-7
FD_STEP = 1e-4
RECEIPT_ATOL, RECEIPT_RTOL = 3e-8, 2e-7


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError(label)
    CHECKS.append(label)


def adj(x):
    return x.conj().T


def herm(x):
    return (x+adj(x))/2


def vec(x):
    return x.reshape(4)


def mat(x):
    return x.reshape(2, 2)


def tr(x):
    z = np.trace(mat(x))
    if abs(z.imag) > 1e-10:
        raise ArithmeticError("non-real trace")
    return float(z.real)


def norm1(x):
    return float(np.linalg.svd(mat(x), compute_uv=False).sum())


def positive_log(x):
    ev, u = np.linalg.eigh(herm(x))
    if ev.min() <= 0:
        raise ArithmeticError("strictly positive leaf spectrum required; no clipping")
    return (u*np.log(ev))@adj(u), float(ev.min())


def entropy(x):
    logs, gap = positive_log(x)
    return -tr(x@logs), gap


def words(cap):
    out = []
    for a in (0, 1):
        other = 1-a
        out.extend(((a,)+(other,)*j+(a,), False) for j in range(cap))
        out.append(((a,)+(other,)*cap, True))
    return out


def chart(t):
    a, b = .6+t, .8-.3*t
    u, v = 1-a*a, 1-b*b
    if min(u, v, a, b) <= 0:
        raise ArithmeticError("control left faithful invertible-Kraus chart")
    k = [np.diag([a, b]).astype(complex),
         np.array([[0, np.sqrt(v)], [np.sqrt(u), 0]], complex)]
    dk = [np.diag([1, -.3]).astype(complex),
          np.array([[0, .3*b/np.sqrt(v)], [-a/np.sqrt(u), 0]], complex)]
    cost, dcost = np.array([1+.2*t, 2-.1*t]), np.array([.2, -.1])
    density = np.diag([v/(u+v), u/(u+v)]).astype(complex)
    du, dv = -2*a, .6*b
    dfirst = (dv*(u+v)-v*(du+dv))/(u+v)**2
    ddensity = np.diag([dfirst, -dfirst]).astype(complex)
    return k, dk, cost, dcost, density, ddensity


def evaluate(t, rho, cap):
    k, dk, cost, dcost, stationary, dstate = chart(t)
    maps = [np.kron(kb, kb.conj()) for kb in k]
    phi = sum(maps)
    jets = [np.kron(db, kb.conj())+np.kron(kb, db.conj()) for kb, db in zip(k, dk)]
    effects = [adj(kb)@kb for kb in k]
    q = np.array([tr(e@rho) for e in effects])
    logrho, rho_gap = positive_log(rho)
    initial_s = -tr(rho@logrho)
    leaves = []
    terminal = np.zeros_like(rho)
    counts = np.zeros(2)
    cost_mean = pointer_s = cq_s = drelative = 0.0
    abort = mass = reference_mass = 0.0
    leaf_gap = 1.0
    for word, is_abort in words(cap):
        product = I2.copy()
        for z in word:
            product = k[z]@product
        x = product@rho@adj(product)
        p = tr(x)
        if p <= 0:
            raise ArithmeticError("positive stopped leaf mass required")
        sigma = herm(x/p)
        logsigma, gap = positive_log(sigma)
        leaf_gap = min(leaf_gap, gap)
        cost_word = float(sum(cost[z] for z in word))
        log_reference = float(sum(np.log(q[z]) for z in word))
        ref = float(np.exp(log_reference))
        relative_quantum = tr(x@(logsigma-logrho))
        drelative += p*(np.log(p)-log_reference)+relative_quantum
        cq_s -= p*np.log(p)+tr(x@logsigma)
        pointer_s -= p*np.log(p)
        terminal += x
        mass += p
        reference_mass += ref
        abort += p*is_abort
        counts += p*np.bincount(word, minlength=2)
        cost_mean += p*cost_word
        leaves.append((p, cost_word, relative_quantum))
    price = cost_mean-(cq_s-initial_s)/ELL
    # Scalar code Gibbs law on exactly this capped language.
    raw = np.exp([-ELL*c for p, c, quant in leaves])
    partition = float(raw.sum())
    logz = float(np.log(partition))
    gibbs_kl = sum(p*(np.log(p)+ELL*c+logz) for p, c, quant in leaves)
    gibbs_cq_d = gibbs_kl+sum(quant for p, c, quant in leaves)
    terminal_log = tr((terminal-rho)@logrho)
    classical_gibbs = (gibbs_kl-logz)/ELL
    quantum_gibbs = (gibbs_cq_d-logz+terminal_log)/ELL
    # The separately assembled finite-dimensional operator reduction.
    rv = vec(rho)
    delta = (phi-I4)@rv
    resolvents = [np.linalg.inv(I4-maps[1-a]) for a in (0, 1)]
    powers = [np.linalg.matrix_power(maps[1-a], cap) for a in (0, 1)]
    vcap = sum((pw@rv for pw in powers), np.zeros(4, complex))
    wcap = sum((pw@ra@aa@rv for pw, ra, aa in zip(powers, resolvents, maps)),
               np.zeros(4, complex))
    rd = sum((ra@delta for ra in resolvents), np.zeros(4, complex))
    g = np.array([tr(aa@rd) for aa in maps])
    e = delta+sum((aa@ra@delta for aa, ra in zip(maps, resolvents)), np.zeros(4, complex))
    predicted_counts = 3*q+g-np.array([tr(aa@wcap) for aa in maps])
    predicted_terminal = rv+e+(I4-phi)@wcap
    f = sum(((cost[z]+np.log(q[z])/ELL)*effects[z] for z in (0, 1)), np.zeros_like(I2))
    logv = vec(logrho)
    bv = sum((adj(ra)@vec(f) for ra in resolvents), np.zeros(4, complex))
    bv += (logv+sum((adj(ra)@adj(aa)@logv for ra, aa in zip(resolvents, maps)),
                    np.zeros(4, complex)))/ELL
    gv = vec(f)+(adj(phi)-I4)@logv/ELL
    bhat = bv-sum((adj(ra)@adj(pw)@gv for ra, pw in zip(resolvents, powers)), np.zeros(4, complex))
    s1 = float(q@cost+q@np.log(q)/ELL)
    cap_term = tr(mat(gv)@mat(vcap))
    reduced = 3*s1+drelative/ELL-cap_term
    preparation = tr(mat(bhat)@mat(delta))
    return {
        "price": float(price), "reduced": float(reduced), "preparation": preparation,
        "cap_term": cap_term, "D_K": float(drelative), "S1": s1,
        "cost_mean": float(cost_mean), "pointer_entropy": float(pointer_s),
        "CQ_entropy": float(cq_s), "initial_entropy": initial_s,
        "terminal_log_defect": terminal_log, "mass": mass, "reference_mass": reference_mass,
        "abort_mass": float(abort), "counts": counts, "terminal": terminal,
        "predicted_counts": predicted_counts, "predicted_terminal": mat(predicted_terminal),
        "q": q, "rho_gap": rho_gap, "normalized_leaf_gap": leaf_gap,
        "partition": partition, "gibbs_classical_KL": float(gibbs_kl),
        "gibbs_CQ_D": float(gibbs_cq_d), "classical_gibbs_price": float(classical_gibbs),
        "quantum_gibbs_price": float(quantum_gibbs),
        "phi": phi, "dphi": sum(jets), "bhat": mat(bhat), "delta": mat(delta),
        "stationary": stationary, "stationary_jet": dstate, "leaf_count": len(leaves),
    }


def exact_control(rho, cap):
    """Exact rational matrices, leaf masses, counts, and capped reference."""
    k = [np.array([[Q(3, 5), Q(0)], [Q(0), Q(4, 5)]], object),
         np.array([[Q(0), Q(3, 5)], [Q(4, 5), Q(0)]], object)]
    eye = np.array([[Q(1), Q(0)], [Q(0), Q(1)]], object)
    require(np.array_equal(sum((a.T@a for a in k)), eye), "exact rational Kraus completeness")
    require(np.count_nonzero(k[0]@k[1]-k[1]@k[0]) == 2,
            "exact control Kraus operators do not commute")
    q = [np.trace(a@rho@a.T) for a in k]
    mass, refmass = Q(0), Q(0)
    counts = np.array([Q(0), Q(0)], object)
    terminal = np.full((2, 2), Q(0), object)
    for word, is_abort in words(cap):
        product, ref = eye.copy(), Q(1)
        for z in word:
            product = k[z]@product
            ref *= q[z]
        x = product@rho@product.T
        p = np.trace(x)
        require(p > 0 and x[0, 0]*x[1, 1]-x[0, 1]*x[1, 0] > 0,
                f"exact positive-mass invertible control leaf {word}, abort={is_abort}")
        mass += p
        refmass += ref
        terminal += x
        for z in word:
            counts[z] += p
    require(mass == refmass == 1, f"exact capped actual/reference mass at K={cap}")
    return terminal, counts, q


def value_checks(t, rho, cap, label, exact=None):
    x = evaluate(t, rho, cap)
    require(x["leaf_count"] == 2*(cap+1), label+": exactly2(K+1) match/abort words")
    require(abs(x["mass"]-1) < PRICE_TOL and abs(x["reference_mass"]-1) < PRICE_TOL,
            label+": both states normalized on the same capped language")
    require(x["abort_mass"] > 0 and x["normalized_leaf_gap"] > 0,
            label+": positive aborts and every positive quantum mode retained")
    require(norm1(x["terminal"]-x["predicted_terminal"]) < PRICE_TOL and
            np.linalg.norm(x["counts"]-x["predicted_counts"]) < PRICE_TOL,
            label+": full terminal/count resolvent formulas agree with independent words")
    require(abs(x["price"]-x["reduced"]-x["preparation"]) < PRICE_TOL,
            label+": direct full CQ-gain price equals reduced price plus Bhat delta")
    require(abs(x["classical_gibbs_price"]-(x["cost_mean"]-x["pointer_entropy"]/ELL)) < PRICE_TOL,
            label+": scalar code partition and classical Gibbs identity")
    require(abs(x["quantum_gibbs_price"]-x["price"]) < PRICE_TOL,
            label+": complete quantum Gibbs identity retains terminal log-rho boundary")
    require(x["D_K"] > 0 and x["gibbs_CQ_D"] > 0,
            label+": actual capped relative entropies positive")
    require(norm1(x["bhat"]-adj(x["bhat"])) < PRICE_TOL,
            label+": complete noncommuting adjoint correction is Hermitian")
    if exact is not None:
        terminal, counts, q = exact
        require(norm1(x["terminal"]-np.asarray(terminal, complex)) < PRICE_TOL and
                np.linalg.norm(x["counts"]-np.asarray(counts, float)) < PRICE_TOL and
                np.linalg.norm(x["q"]-np.asarray(q, float)) < PRICE_TOL,
                label+": full leaf probabilities/counts/terminal match exact rational evaluation")
    return {
        "field_parameter": t, "cap": cap, "leaf_count": x["leaf_count"],
        "abort_mass": x["abort_mass"], "input_min_eigenvalue": x["rho_gap"],
        "minimum_normalized_leaf_eigenvalue": x["normalized_leaf_gap"],
        "q": x["q"].tolist(), "expected_fine_counts": x["counts"].tolist(),
        "expected_charge": x["cost_mean"], "initial_entropy": x["initial_entropy"],
        "full_CQ_entropy": x["CQ_entropy"], "pointer_entropy": x["pointer_entropy"],
        "actual_gain_price": x["price"], "iid_capped_quantum_D": x["D_K"],
        "reduced_price": x["reduced"], "Bhat_delta_correction": x["preparation"],
        "cap_term_Tr_G_V": x["cap_term"],
        "price_reduction_error": abs(x["price"]-x["reduced"]-x["preparation"]),
        "terminal_count_formula_error":
            max(norm1(x["terminal"]-x["predicted_terminal"]),
                float(np.linalg.norm(x["counts"]-x["predicted_counts"]))),
        "terminal_DATA_defect_trace_norm": norm1(x["terminal"]-rho),
        "terminal_log_rho_defect": x["terminal_log_defect"],
        "scalar_Gibbs_partition": x["partition"],
        "Gibbs_classical_KL": x["gibbs_classical_KL"], "Gibbs_quantum_D": x["gibbs_CQ_D"],
        "Gibbs_quantum_price_error": abs(x["quantum_gibbs_price"]-x["price"]),
        "deleting_cap_term_price_error": abs(x["cap_term"]),
        "deleting_preparation_defect_price_error": abs(x["preparation"]),
        "deleting_Gibbs_terminal_boundary_price_error": abs(x["terminal_log_defect"]/ELL),
    }


def derivative(function, step=FD_STEP):
    return float((-function(2*step)+8*function(step)-8*function(-step)+function(-2*step))/(12*step))


def poisson_control(cap=3):
    _, _, _, _, rho, drho = chart(0.0)
    base = evaluate(0.0, rho, cap)
    phi, dphi, bhat = base["phi"], base["dphi"], base["bhat"]
    eigenvalues = np.linalg.eigvals(phi)
    nonstationary = [z for z in eigenvalues if abs(z-1) > 1e-10]
    require(len(nonstationary) == 3 and max(abs(z) for z in nonstationary) < .99,
            "Poisson: faithful generated input lies on a simple stationary-eigenvalue chart")
    require(norm1(adj(dphi)@vec(I2)) < PRICE_TOL,
            "Poisson: actual moving complementary-square-root channel has trace-preserving jet")
    # A full Hermitian trace-free basis; no diagonal-only DATA assumption.
    pauli = [np.array([[0, 1], [1, 0]], complex),
             np.array([[0, -1j], [1j, 0]], complex),
             np.diag([1, -1]).astype(complex)]
    cotangents, data_sources = {}, {}
    for name, scalar in (("full", "price"), ("red", "reduced")):
        source = [derivative(lambda s, direction=e: evaluate(0.0, rho+s*direction, cap)[scalar])
                  for e in pauli]
        cotangents[name] = sum((g*e/2 for g, e in zip(source, pauli)), np.zeros_like(I2))
        data_sources[name] = source
    def centered(m):
        return m-tr(rho@m)*I2
    mfull, mred = cotangents["full"], cotangents["red"]
    cotangent_defect = centered(mfull)-centered(mred)-mat((adj(phi)-I4)@vec(bhat))
    require(norm1(cotangent_defect) < SOURCE_TOL,
            "Poisson: independently differenced full DATA cotangents have the exact Bhat correction")
    require(norm1((I4-phi)@vec(drho)-dphi@vec(rho)) < PRICE_TOL,
            "Poisson: actual moving stationary density satisfies differentiated fixed-point equation")
    projection = np.outer(vec(I2), vec(rho).conj())
    operator = I4-adj(phi)+projection
    yfull = mat(np.linalg.solve(operator, vec(centered(mfull))))
    yred = mat(np.linalg.solve(operator, vec(centered(mred))))
    for name, y, m in (("full", yfull, mfull), ("red", yred, mred)):
        require(norm1((I4-adj(phi))@vec(y)-vec(centered(m))) < PRICE_TOL and
                abs(tr(rho@y)) < PRICE_TOL, "Poisson: centered "+name+" adjoint equation and gauge")
    shift = yfull-yred+bhat-tr(rho@bhat)*I2
    require(norm1(shift) < SOURCE_TOL,
            "Poisson: Y_full=Y_red-Bhat+Tr(rho Bhat)I")
    ffull = derivative(lambda t: evaluate(t, rho, cap)["price"])
    fred = derivative(lambda t: evaluate(t, rho, cap)["reduced"])
    dphi_rho = mat(dphi@vec(rho))
    explicit = tr(bhat@dphi_rho)
    require(abs(ffull-fred-explicit) < SOURCE_TOL,
            "Poisson: independent fixed-DATA field sources retain Tr Bhat(dPhi)rho")
    transported_full = ffull+tr(yfull@dphi_rho)
    transported_red = fred+tr(yred@dphi_rho)
    curve_full = derivative(lambda t: evaluate(t, chart(t)[4], cap)["price"])
    curve_red = derivative(lambda t: evaluate(t, chart(t)[4], cap)["reduced"])
    require(max(abs(transported_full-transported_red), abs(transported_full-curve_full),
                abs(transported_red-curve_red)) < SOURCE_TOL,
            "Poisson: both corrected sources equal independent total stationary-curve derivatives")
    chain_full = ffull+tr(mfull@drho)
    require(abs(chain_full-curve_full) < SOURCE_TOL,
            "Poisson: independent DATA chain rule agrees with adjoint elimination")
    stale = fred+tr(yfull@dphi_rho)
    require(abs(stale-curve_full) > 1e-3,
            "negative control: retaining the old adjoint in the reduced source fails")
    return {
        "cap": cap, "five_point_step": FD_STEP,
        "largest_nonstationary_eigenvalue_modulus": float(max(abs(z) for z in nonstationary)),
        "stationary_density": np.diag(rho).real.tolist(),
        "stationary_density_source": np.diag(drho).real.tolist(),
        "Pauli_DATA_directional_sources": data_sources,
        "centered_DATA_cotangent_identity_error": norm1(cotangent_defect),
        "adjoint_shift_trace_norm_error": norm1(shift),
        "fixed_DATA_field_source_full": ffull, "fixed_DATA_field_source_reduced": fred,
        "explicit_Bhat_dPhi_rho_correction": explicit,
        "field_correction_identity_error": abs(ffull-fred-explicit),
        "transported_full_source": transported_full, "transported_reduced_source": transported_red,
        "independent_total_stationary_full_source": curve_full,
        "independent_total_stationary_reduced_source": curve_red,
        "independent_chain_rule_full_source": chain_full,
        "stale_adjoint_reduced_source": stale,
        "stale_adjoint_negative_control_error": abs(stale-curve_full),
    }


def compare_receipt(actual, expected, where="result"):
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or actual.keys() != expected.keys():
            raise ArithmeticError("receipt structure changed at "+where)
        for key in expected:
            compare_receipt(actual[key], expected[key], where+"."+key)
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise ArithmeticError("receipt list changed at "+where)
        for index, (a, e) in enumerate(zip(actual, expected)):
            compare_receipt(a, e, where+f"[{index}]")
    elif isinstance(expected, float):
        if not np.isfinite(actual) or abs(actual-expected) > RECEIPT_ATOL+RECEIPT_RTOL*abs(expected):
            raise ArithmeticError("receipt numerical difference at "+where)
    elif type(actual) is not type(expected) or actual != expected:
        raise ArithmeticError("receipt exact value changed at "+where)


def run():
    stationary = np.array([[Q(9, 25), Q(0)], [Q(0), Q(16, 25)]], object)
    independent = np.array([[Q(3, 7), Q(1, 11)], [Q(1, 11), Q(4, 7)]], object)
    rational_k = [np.array([[Q(3, 5), Q(0)], [Q(0), Q(4, 5)]], object),
                  np.array([[Q(0), Q(3, 5)], [Q(4, 5), Q(0)]], object)]
    require(np.array_equal(sum((k@stationary@k.T for k in rational_k)), stationary),
            "exact rational stationary density is diag(9/25,16/25)")
    require(not np.array_equal(sum((k@independent@k.T for k in rational_k)), independent),
            "exact faithful offstationary control keeps its independent input defect")
    cases = {}
    for name, rational_rho in (("stationary", stationary), ("offstationary", independent)):
        require(np.trace(rational_rho) == 1 and
                rational_rho[0, 0]*rational_rho[1, 1]-rational_rho[0, 1]*rational_rho[1, 0] > 0,
                name+": exact rational faithful normalized input")
        cases[name] = []
        for cap in (1, 3, 7):
            exact = exact_control(rational_rho, cap)
            case = value_checks(0.0, np.asarray(rational_rho, complex), cap, name+f" K={cap}", exact)
            require(abs(case["scalar_Gibbs_partition"]-1) < PRICE_TOL,
                    name+f" K={cap}: complete Golden 0/10 code has normalized scalar partition")
            cases[name].append(case)
    require(max(c["deleting_cap_term_price_error"] for c in cases["stationary"]) > 1e-3,
            "negative control: deleting the finite cap correction changes the stationary full price")
    require(max(c["deleting_preparation_defect_price_error"] for c in cases["offstationary"]) > 1e-3,
            "negative control: deleting Bhat delta changes the faithful independent-input price")
    require(max(c["deleting_Gibbs_terminal_boundary_price_error"] for c in cases["offstationary"]) > 1e-3,
            "negative control: deleting terminal quantum defect changes the complete Gibbs price")
    shifted_t = .04
    shifted = value_checks(shifted_t, chart(shifted_t)[4], 3, "moving gates and paid charges")
    require(abs(shifted["scalar_Gibbs_partition"]-1) > 1e-3,
            "nontrivial scalar normalizer: actual changing paid code has Z_K different from one")
    sources = poisson_control()
    return {
        "status": "FINITE_QUANTUM_PRICE_REDUCTION_CONTROL_PASS",
        "kind": "tiny rational integration control, not new native evidence",
        "consumer": "STATIONARY_SOURCE_CONSUMER.md Sections3-4",
        "control": {"K0": [["3/5", "0"], ["0", "4/5"]],
                    "K1": [["0", "3/5"], ["4/5", "0"]],
                    "stationary_rho": [["9/25", "0"], ["0", "16/25"]],
                    "independent_rho": [["3/7", "1/11"], ["1/11", "4/7"]],
                    "field_curve": "a=.6+t,b=.8-.3t; K1 offdiagonal sqrt(1-b^2),sqrt(1-a^2)",
                    "paid_charge_curve": "c0=1+.2t,c1=2-.1t",
                    "ell": ELL},
        "complete_capped_cases": cases,
        "nontrivial_partition_case": shifted,
        "full_Poisson_source_control": sources,
        "verification": {"exact_arithmetic": "rational input, noncommuting Kraus, all leaf masses/counts/terminal",
                         "numerical_arithmetic": "full positive2x2 logarithms; five-point DATA/field derivatives",
                         "price_identity_absolute_tolerance": PRICE_TOL,
                         "source_identity_absolute_tolerance": SOURCE_TOL,
                         "receipt_absolute_tolerance": RECEIPT_ATOL,
                         "receipt_relative_tolerance": RECEIPT_RTOL,
                         "spectral_clipping": False, "discarded_abort_leaves": False,
                         "old_suites_replayed": False, "interval_certificate": False,
                         "native_checker_modified": False},
        "scope": {"new_native_full128_evidence": False, "complete_uncapped_source_computed": False,
                  "physical_Book03_Info_selected": False, "all42_source_transport_proved": False,
                  "GR_closed": False},
        "checks_passed": len(CHECKS), "checks": CHECKS,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="explicitly author the new immutable receipt")
    parser.add_argument("--print-only", action="store_true", help="diagnose without writing or comparing")
    args = parser.parse_args()
    if args.write_result and args.print_only:
        parser.error("choose one author/diagnostic mode")
    result = run()
    encoded = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n"
    target = Path(__file__).with_name("FINITE_PRICE_REDUCTION_RESULT.json")
    if args.write_result:
        target.write_text(encoded)
    elif not args.print_only:
        compare_receipt(result, json.loads(target.read_text()))
    print(encoded, end="")


if __name__ == "__main__":
    main()
