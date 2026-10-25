#!/usr/bin/env python3
"""Bounded exact native adjugate-return and one-closing-prefix checks.

No full256-word, large native root, generic SK or Lean suite is replayed.
Actual rank8 columns, full middle permutations and local all-column inverse
cells have separate, explicit scopes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import sympy as sp
import mpmath as mp
import paired_return as pr

CHECKS = []
SOURCES = Path(__file__).resolve().parent.parent
REPO = SOURCES.parents[2]


def check(name, statement):
    if not statement:
        raise AssertionError(name)
    CHECKS.append(name)


def kron(a, b):
    return mp.matrix([[a[i//b.rows, j//b.cols]*b[i % b.rows, j % b.cols]
                       for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])


def norm(a):
    if a.cols == 1:
        return mp.sqrt(mp.re((a.H*a)[0]))
    return max(abs(v) for v in mp.eighe((a+a.H)/2, eigvals_only=True))


def c_original(p, x, y):
    E, b = p*p*(1+x), (p-p*p*y)**2
    return (1-2*b)*((1-E)*mp.eye(2)-E*mp.matrix([[0, 1], [1, 0]]))


def raw_moment_score(kernel, state, zeta):
    c = (state.H*kernel*state)[0]
    score = -16*zeta*c*kernel/(1-zeta+zeta*c*c)
    return score, 2*(score*state-state*(state.H*score*state)[0])


def run():
    mp.mp.dps = 100
    tol = mp.mpf("1e-75")
    ne, p, zeta = pr.ne, (mp.sqrt(5)-1)/2, mp.mpf(2)**-20
    q1 = 1-zeta+zeta*p**18
    a1 = 32*zeta*p**17/q1
    b1 = -128*zeta*p**18/q1
    x2, z2 = sp.Matrix([[0, 1], [1, 0]]), sp.diag(1, -1)
    alpha, beta = sp.symbols("alpha beta", real=True)
    arbitrary = alpha*sp.eye(2)-beta*x2
    check("arbitrary internally joint DATA-blind corner paired with its band flip is exactly its determinant times I",
          arbitrary*z2*arbitrary*z2 == (alpha*alpha-beta*beta)*sp.eye(2))

    rows = []
    for helper in (False, True):
        spec = pr.specification(helper)
        middle = pr.execution(spec, pr.middle_word(spec))
        images = pr.signed_word(middle)
        e1, bE, e2, bB = spec["programmes"]
        bits = lambda col, q: (col >> (spec["qubits"]-1-q)) & 1
        expected = []
        for col in range(1 << spec["qubits"]):
            flip = bits(col, e1)^bits(col, e2)
            row = col ^ (flip << (spec["qubits"]-1-spec["data"]))
            sign = (-1)**(bits(col, e1)+bits(col, bE)+bits(col, bB))
            expected.append((row, sign))
        mi = ne.inventory(middle, **pr.bounds(spec))
        trace = sum(sign for col, (row, sign) in enumerate(images) if col == row)
        check("fixed middle is the exact signed permutation on ALL columns helper"+str(helper),
              images == expected and mi.g_count == 0 and mi.source_i_count == 6
              and mi.cx_count == (20 if helper else 14)
              and all(images[row][0] == col and sign*images[row][1] == 1
                      for col, (row, sign) in enumerate(images)) and trace == 0)
        for correlated in (False, True):
            stages = 74 if helper else 62
            spec, exe = pr.pair_execution(helper, correlated, stages=stages)
            inv = ne.inventory(exe, **pr.bounds(spec))
            corner, columns = pr.exact_columns(exe)
            scalar = ne.P**(3 if correlated else 9)
            check("actual rank8 raw columns give the exact scalar corner helper"+str(helper)+" correlated"+str(correlated),
                  ne.exact_matrix_equal(corner, scalar*sp.eye(8))
                  and ne.exact_matrix_equal(columns.T*columns, sp.eye(8)))
            desired = ((8, 22, 44) if helper else (8, 22, 32)) if not correlated else (
                (4, 14, 56) if helper else (4, 14, 44))
            check("every forward inverse phase and real common padding stage is counted helper"+str(helper)+" correlated"+str(correlated),
                  inv.gate_count == stages and inv.cut_rank == 8
                  and inv.full_dimension == (256 if helper else 128)
                  and (inv.g_count, inv.source_i_count, inv.cx_count) == desired)
            j = -8*mp.log(1-zeta+zeta*p**(6 if correlated else 18))
            rows.append({"dedicated_helper": helper, "correlated_each_copy": correlated,
                         "N": inv.gate_count, "full_dimension": inv.full_dimension, "input_rank": 8,
                         "G": inv.g_count, "CX": inv.cx_count, "SourceI": inv.source_i_count,
                         "return_scalar_power_of_p": 3 if correlated else 9, "J": mp.nstr(j, 35)})
        check("same-marginal correlated programmes remain a genuine different paired-return task helper"+str(helper),
              mp.mpf(rows[-1]["J"]) < mp.mpf(rows[-2]["J"]))

    # One exact local off-port inverse check, independent of initialized
    # columns, supports the full-factorization argument used for prefixes.
    local = dict(qubits=5, programmes=(0, 1), data=2, spin=(3, 4), helper=None, keys=())
    inverse = pr.inv_g(2, local)
    iw = ne.word_matrix(pr.execution(local, inverse), max_qubits=5, max_expanded_stages=100000)
    target_inverse = ne.gate_matrix(pr.execution(local), ne.Gate("G", (2,)),
                                    max_qubits=5, max_expanded_stages=100000).T
    check("off-port raw G inverse restores every dirty helper-spin column exactly",
          len(inverse) == 11 and ne.exact_matrix_equal(iw, target_inverse))
    probe = dict(local, programmes=())
    probe_word = (ne.Gate("G", (2,)), ne.Gate("CX", (1, 2)),
                  ne.Gate("SourceI", (0, 3, 4)), ne.Gate("G", (0,)))
    probe_execution = pr.execution(probe, probe_word)
    _, propagated = pr.exact_columns(probe_execution)
    check("protected-column propagation agrees with the owned gate-matrix engine on all32 columns of a mixed primitive word",
          ne.exact_matrix_equal(propagated, ne.word_matrix(probe_execution,
                                     max_qubits=5, max_expanded_stages=100000)))

    # The finite request graph has a genuinely fixed primitive controller.
    # Its local D cells are checked all-column; graph512/1024 matrices are
    # not emitted. Protected keys have a different true input rank.
    key_rows = []
    for port_cell in (True, False):
        q = 0 if port_cell else 2
        fwd = pr.request_cell(q, 1, local)
        backward = pr.request_cell(q, 1, local, inverse=True)
        wf = ne.word_matrix(pr.execution(local, fwd), max_qubits=5, max_expanded_stages=100000)
        wb = ne.word_matrix(pr.execution(local, backward), max_qubits=5, max_expanded_stages=100000)
        expected = sp.zeros(32)
        for column in range(32):
            key = (column >> 3) & 1
            power = ne.G_LOCAL**(1+2*key)
            old_bit = (column >> (4-q)) & 1
            base = column & ~(1 << (4-q))
            for new_bit in (0, 1):
                expected[base | (new_bit << (4-q)), column] = power[new_bit, old_bit]
        check("actual native request cell has control0 G control1 G cubed and exact all-column inverse port"+str(port_cell),
              len(fwd) == (9 if port_cell else 15) and len(backward) == (13 if port_cell else 25)
              and ne.exact_matrix_equal(wf, expected)
              and ne.exact_matrix_equal(wb*wf, sp.eye(32)))
    for helper in (False, True):
        for protected in (False, True):
            spec, exe, forward_length, inverse_length = pr.request_execution(helper, protected_keys=protected)
            inv = ne.inventory(exe, **pr.bounds(spec))
            check("request graph retains actual inventory and true key input rank helper"+str(helper)+" protected"+str(protected),
                  inv.gate_count == (186 if helper else 162)
                  and forward_length == (60 if helper else 54)
                  and inverse_length == (100 if helper else 88)
                  and (inv.g_count, inv.cx_count, inv.source_i_count) == (24, 108 if helper else 84, 54)
                  and inv.full_dimension == (1024 if helper else 512)
                  and inv.cut_rank == (32 if protected else 8))
            key_rows.append({"dedicated_helper": helper, "protected_quantum_keys": protected,
                             "N": inv.gate_count, "full_dimension": inv.full_dimension,
                             "input_rank": inv.cut_rank})

    # Literal native endpoints have scalar compression. These continuous
    # comparisons differentiate the original x/y operands, not word strings.
    def sxy(x, y):
        return pr.scalar(p*p*(1+x), (p-p*p*y)**2)

    check("single exact comparison has positive actual gain and lambda_pair minus4p without readiness dilution",
          a1 > 0 and abs(mp.diff(lambda x: -8*mp.log(1-zeta+zeta*sxy(x, 0)**2), 0)-a1) < tol
          and abs(mp.diff(lambda y: -8*mp.log(1-zeta+zeta*sxy(0, y)**2), 0)-b1) < tol
          and abs(b1/a1+4*p) < tol and abs(sxy(0, 0)-p**9) < tol)
    prefix_rows = []
    for length in (1, 2, 3):
        exe, private_sets = pr.native_prefix(length)
        inv = ne.inventory(exe, max_qubits=exe.qubits, max_expanded_stages=100000)
        future_excludes_past = all(
            not (set(g.wires) & set.union(*private_sets[:j]))
            for j in range(1, length) for g in exe.gates[74*j:74*(j+1)])
        check("literal private prefix counts one helper-spin and never reads a sealed old private block M"+str(length),
              inv.gate_count == 74*length and inv.cut_rank == 4*2**length
              and inv.full_dimension == 2**(5*length+3)
              and (inv.g_count, inv.cx_count, inv.source_i_count) == (8*length, 44*length, 22*length)
              and future_excludes_past)
        def literal_price(x, y):
            scalar = sxy(x, y)*p**(9*(length-1))
            returned = scalar*mp.eye(2**length)
            return -4*mp.log(mp.det((1-zeta)*mp.eye(2**length)+zeta*returned.T*returned))
        gx = mp.diff(lambda x: literal_price(x, 0), 0)
        gy = mp.diff(lambda y: literal_price(0, y), 0)
        gain = pr.prefix_gain(p, zeta, length)
        value = literal_price(0, 0)
        check("one literal cumulative returned-matrix logdet has the true positive gain and invariant coupling M"+str(length),
              gain > 0 and abs(gx-gain) < tol and abs(gy/gx+4*p) < tol
              and abs(value-pr.prefix_price([p**9]*length, zeta)) < tol
              and (length == 1 or abs(value-length*pr.prefix_price([p**9], zeta)) > mp.mpf("1e-12")))
        prefix_rows.append({"M": length, "actual_N": inv.gate_count, "input_rank": inv.cut_rank,
                            "J": mp.nstr(value, 35), "Gamma_old_block": mp.nstr(gain, 35),
                            "lambda": mp.nstr(gy/gx, 35)})

    # All-column private factorization, not initialized-column equality,
    # gives old-channel partial-trace compatibility for correlated inputs.
    u = mp.diag([1, 1, -1, -1])
    angle = mp.mpf(".37")
    v = mp.matrix([[mp.cos(angle), -mp.sin(angle)], [mp.sin(angle), mp.cos(angle)]])
    vector = mp.matrix([mp.mpf(j+1) for j in range(8)])
    vector /= norm(vector)
    rho = vector*vector.H
    evolved = kron(u, v)*rho*kron(u, v).H
    pt = lambda a: mp.matrix([[mp.fsum(a[2*i+j, 2*k+j] for j in range(2))
                               for k in range(4)] for i in range(4)])
    check("private all-column tensor action preserves the old reduced channel even on a correlated input",
          norm(pt(evolved)-u*pt(rho)*u.H) < tol)

    normal_rows = []
    normal_kernel = normal_state = None
    for n in (2, 3):
        dimension, weight = 1 << (2*n), sp.Rational(1, n*n)
        h = sp.zeros(dimension)
        for col in range(dimension):
            for i in range(n):
                for j in range(n):
                    row = col ^ (1 << (2*n-1-i)) ^ (1 << (n-1-j))
                    h[row, col] += weight
        state = sp.zeros(dimension, 1)
        state[0] = 1
        image = h*state
        tangent = n*image
        one_slots_zero = all(h.extract([0, 1 << q], [0, 1 << q]) == sp.zeros(2)
                             for q in range(2*n))
        check("two-group k2 padded kernel has zero one-slot conditionals but nonzero cross-group excitation n"+str(n),
              h.T == h and all(sum(abs(h[i, j]) for j in range(dimension)) == 1 for i in range(dimension))
              and one_slots_zero and (image.T*image)[0] == sp.Rational(1, n*n)
              and (tangent.T*tangent)[0] == 1 and (state.T*tangent)[0] == 0)
        epsilon = p**9/4
        ell = -16*zeta*p**9*epsilon/q1
        exact_norm = 2*abs(ell)/n
        upper = 2*mp.sqrt(2)*abs(ell)*4/mp.sqrt(n*(n-1))
        def normal_price(t):
            c = p**9+epsilon*mp.sin(2*t)/n
            return -8*mp.log(1-zeta+zeta*c*c)
        check("full logdet source sees the cross-group correlated tangent and obeys the joint overlap norm n"+str(n),
              exact_norm > 0 and abs(abs(mp.diff(normal_price, 0))-exact_norm) < tol
              and exact_norm <= upper)
        normal_rows.append({"n_each_group": n, "k_each_group_with_idle_padding": 2,
                            "first_conditionals_zero": True, "full_gradient_norm": mp.nstr(exact_norm, 35),
                            "joint_overlap_bound": mp.nstr(upper, 35)})
        if n == 2:
            normal_state = mp.matrix([1]+[0]*(dimension-1))
            normal_kernel = p**9*mp.eye(dimension)+epsilon*mp.matrix(h.tolist())
    # Perturb the WHOLE two-group kernel. The compared object is its full
    # pure-state score gradient, not a sum of separate marginal norms.
    rotation = mp.eye(normal_state.rows)
    angle = mp.mpf(".007")
    rotation[0, 0] = rotation[5, 5] = mp.cos(angle)
    rotation[0, 5], rotation[5, 0] = -mp.sin(angle), mp.sin(angle)
    changed = rotation.T*normal_kernel*rotation
    epsilon_kernel = norm(changed-normal_kernel)
    old_score, old_gradient = raw_moment_score(normal_kernel, normal_state, zeta)
    new_score, new_gradient = raw_moment_score(changed, normal_state, zeta)
    check("whole two-group matrix-kernel error controls the actual pure-gradient source without summing marginal norms",
          epsilon_kernel > 0
          and norm(new_score-old_score) <= 32*zeta*epsilon_kernel/(1-zeta)**2
          and norm(new_gradient-old_gradient) <= 64*zeta*epsilon_kernel/(1-zeta)**2)

    return {"checks": CHECKS, "checks_passed": len(CHECKS), "native_pair_rows": rows,
            "request_graph_rows": key_rows, "prefix_rows": prefix_rows, "two_group_norm_diagnostic": normal_rows,
            "single_comparison": {"readiness": "1", "a1": mp.nstr(a1, 40),
                "b1": mp.nstr(b1, 40), "lambda_pair": mp.nstr(b1/a1, 40)},
            "matrix_scope": "actual rank8 protected columns only for62/74 words; middle signed permutations ALL128/256; local inverse/request cells ALL32",
            "request_graph_full512_or1024_replayed": False,
            "private_prefix_full_large_unitaries_replayed": False,
            "compiled_DATA_blind_identical_copies_have_exact_scalar_corner": True,
            "arbitrary_cross_copy_correlated_inputs_claimed_scalar": False,
            "protected_keys_have_one_scalar_Book_corner_claimed": False,
            "sum_of_local_prefix_prices_claimed": False,
            "two_group_toy_is_native42_example": False,
            "continuous_native_word_selector_proved": False,
            "physical_request_or_all_XN_admission_proved": False,
            "full_native_joint_stationarity_proved": False, "GR_closed": False,
            "numeric_arithmetic": "100-digit mpmath non-interval; exact Q(sqrt(p)) native columns and local cells; exact rational joint overlap diagnostic"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result.update(schema="d0.native-adjugate-pair-prefix-check/1", status="PASS")
    paths = [Path(__file__).resolve(), Path(pr.__file__).resolve(), Path(__file__).with_name("PROOF.md"),
             SOURCES/"d0_native_bilinear_return_echo_2026-10-25/PROOF.md",
             SOURCES/"d0_native_bilinear_return_echo_2026-10-25/native_echo.py",
             SOURCES/"d0_native_execution_domain_2026-10-24/native_execution.py",
             SOURCES/"d0_native_matrix_collective_return_2026-10-25/PROOF.md"]
    result["inputs_sha256"] = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    primary = REPO/"02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
    text_primary = primary.read_text()
    result["consumed_sections_sha256"] = {}
    for section in ("7ab", "7ac", "7ae"):
        start = text_primary.index("## "+section+".")
        end = text_primary.find("\n## ", start+4)
        body = text_primary[start:end if end >= 0 else len(text_primary)]
        result["consumed_sections_sha256"][section] = hashlib.sha256(body.encode()).hexdigest()
    result["runtime"] = {"python": sys.version.split()[0], "mpmath": mp.__version__, "sympy": sp.__version__}
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
