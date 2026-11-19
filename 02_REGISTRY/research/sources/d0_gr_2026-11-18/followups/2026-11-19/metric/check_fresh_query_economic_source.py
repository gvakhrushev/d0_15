"""Fresh scalar-effect queries, one full thermal root, all old quantum memory.

The proof is conditional on a specified economic weighting. It does not infer
Book Cost-Info from Born statistics. The 34-stage LIVE cold is checked on all
old columns exactly. A separate literal two-query native word checks the CP
and absolute-thermal identities on an entangled input. Its heat is not
misreported as the heat of the much larger query-plus-LIVE programme.
"""
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path

import numpy as np

import check_complete_work_source as cw
from check_live_parser import controller
from check_local_gibbs_records import scene, scene_heat, halo, mm
from check_source_price import load_control, need


def close(x, y, message, tol=3e-11):
    need(float(np.max(np.abs(np.asarray(x)-np.asarray(y)))) < tol, message)


def exact_live_cold(ne):
    digest, listed = controller()
    local = {op: cw.native_local(ne, op) for op in ("G", "CX", "SourceI")}
    # Original wires: Spin0, Spin1, dirty port, H=1, coherent T.
    # Keep all 16 Spin x port x T columns, not one prepared mean.
    v = np.zeros((4, 32, 16), dtype=np.int64)
    for spin, port, t in product(range(4), range(2), range(2)):
        v[0, spin*8+port*4+2+t, spin*4+port*2+t] = 1
    for _ in range(6):
        v = cw.born(v)
    born = v.copy()
    for op, *wires in listed:
        v = cw.apply_local(v, local[op], 11, tuple(wires))
    cw.equal(cw.dot(v, v), cw.eye(16), "literal full LIVE remains isometric")
    c = cw.element(ne, ne.A**5*ne.P*(ne.A+ne.P))
    cw.equal(cw.dot(born, v), cw.scale(cw.eye(16), c),
             "all-column exact RAW LIVE cold, including coherent T and dirty port")
    cv = cw.scalar_value(c)
    need(0 < cv < 1, "strict true RAW contraction")
    return {"native_sha256": digest, "input_columns": 16,
            "output_dimension": 2048, "births": 6, "square_stages": 28,
            "cold_exact": cw.coefficient_text(c),
            "cold_decimal": format(cv, ".15g"),
            "cold_squared": format(cv*cv, ".15g"),
            "arithmetic": "exact Q(a), a^4+a^2-1=0"}, cv


def native_word(ne):
    g = ne.Gate
    swap = (g("CX", (2, 3)), g("CX", (3, 2)), g("CX", (2, 3)))
    # Both fresh ports are genuinely born. The one fixed SourceI port is 2;
    # the second query uses six real routing CX calls and restores port 2.
    word = (g("G", (2,)), g("SourceI", (2, 0, 1)),
            g("G", (3,)), g("G", (3,))) + swap + (
            g("SourceI", (2, 0, 1)),) + swap
    spec = ne.Execution(4, (), (), word, profile=ne.G_CX_SOURCE_I,
                        source_port=2, source_spin=(0, 1), report_bits=(2, 3))
    actual = ne.execution_from_json(ne.canonical_json(spec), max_qubits=4,
                                   max_expanded_stages=len(word))
    need(actual.gates == word, "literal routed original native word")
    mats = [np.array(ne.gate_matrix(actual, gate, max_qubits=4,
                                   max_expanded_stages=len(word)), dtype=float)
            for gate in word]
    return mats, [[gate.op, *gate.wires] for gate in word]


def build_graph(ne, mats, delta=0.0):
    """The same two births and eleven stages in a genuine growing clock."""
    gates = [u.copy() for u in mats]
    # A smooth matrix diagnostic at one actual native point. This checks a
    # derivative identity, not physical admission of intermediate angle gates.
    rot = np.array([[math.cos(delta), -math.sin(delta)],
                    [math.sin(delta), math.cos(delta)]])
    gates[0] = mm(np.kron(np.kron(np.eye(4), rot), np.eye(2)), gates[0])
    v = np.array([[float(ne.A)], [float(ne.P)]])
    births = [np.kron(np.eye(4), v), np.kron(np.eye(8), v)]
    stages = births+gates[:-1]
    passive = births+[np.eye(16) for _ in gates[:-1]]
    dims = [4]+[u.shape[0] for u in stages]
    edges = np.cumsum([0]+dims)
    cuts = [slice(edges[j], edges[j+1]) for j in range(len(dims))]
    d = int(edges[-1])
    clock = np.zeros((d, d))
    for j, u in enumerate(stages):
        clock[cuts[j+1], cuts[j]] = u
    for j, dim in enumerate(dims):
        emb = np.eye(dim)
        for u in passive[j:]:
            emb = mm(u, emb)
        extra = np.eye(dim) if j == 0 else np.eye(dim)-mm(passive[j-1], passive[j-1].T)
        clock[cuts[j], cuts[-1]] += mm(extra, emb.T, gates[-1])
    close(mm(clock.T, clock), np.eye(d), "genuine complete growing clock including complements")
    born = mm(births[1], births[0])
    end = born.copy()
    for u in gates:
        end = mm(u, end)
    close(mm(end.T, end), np.eye(4), "every old Spin column retained")
    cold = mm(born.T, end)
    z = 2**-20
    j = -float(np.linalg.slogdet((1-z)*np.eye(4)+z*mm(cold.T, cold))[1])
    b, c = scene()
    beta = 2*float(ne.P)**2
    vals, vecs = np.linalg.eigh(clock+clock.T)
    heats = [scene_heat(b, c, val, beta) for val in vals]
    zh = 359*d+2*sum(float(h.trace()) for h in heats)
    local = mm(vecs*np.array([h[32, 32] for h in heats])[None, :], vecs.T)
    k = mm(gates[-1], local[cuts[-1], cuts[-1]], gates[-1].T)
    need(np.linalg.eigvalsh(k).min() >= math.exp(-2*beta)-2e-12,
         "true localized heat remains strictly positive")
    return end, k, zh, j, d, len(gates), clock


def old_state():
    # A full-rank entangled Spin4 x untouched RIGHT4 input, not a product.
    psi = np.zeros(16)
    for i, weight in enumerate((.4, .3, .2, .1)):
        psi[4*i+i] = math.sqrt(weight)
    rho = .83*np.outer(psi, psi)+.17*np.eye(16)/16
    partial_transpose = rho.reshape(4, 4, 4, 4).transpose(0, 3, 2, 1).reshape(16, 16)
    need(np.linalg.eigvalsh(partial_transpose).min() < -.1, "old input is genuinely entangled")
    close(rho.trace(), 1, "normalized old density")
    return rho


def blocks(end, rho):
    full = mm(np.kron(end, np.eye(4)), rho, np.kron(end.T, np.eye(4)))
    out = {}
    effects = {}
    for t in product(range(2), repeat=2):
        diagonal = np.array([((i >> 1) & 1) == t[0] and (i & 1) == t[1]
                             for i in range(16)], dtype=float)
        proj = np.diag(np.repeat(diagonal, 4))
        out[t] = mm(proj, full, proj)
        effects[t] = mm(end.T, np.diag(diagonal), end)
        close(effects[t], np.eye(4)*np.trace(effects[t])/4,
              "complete joint native effect is scalar on all old Spin inputs")
    close(sum(out.values()).trace(), 1, "all recorded sectors retained")
    q = [sum(float(b.trace()) for t, b in out.items() if t[i]) for i in range(2)]
    for t, b in out.items():
        expected = math.prod(q[i] if t[i] else 1-q[i] for i in range(2))
        close(b.trace(), expected, "fresh conditional laws, no quantum product assumption")
    return out, q


def thermal_identity(ne, mats, delta=0.0):
    end, k, zh, j, d, length, clock = build_graph(ne, mats, delta)
    rho = old_state()
    cells, q = blocks(end, rho)
    p = float(ne.P)
    tilted = sum(p**sum(t)*block for t, block in cells.items())
    unweighted = sum(cells.values())
    prodz = math.prod(1-p*p*x for x in q)
    normalized = tilted/prodz
    close(normalized.trace(), 1, "exact positive scalar-effect normalization")
    kref = np.kron(k, np.eye(4))
    s0 = float(np.trace(mm(kref, unweighted)))
    sw = float(np.trace(mm(kref, normalized)))
    root = math.exp(j)*zh
    # These are the ABSOLUTE normalized full-graph weights.
    raw = {t:root*float(np.trace(mm(kref, block)))/s0 for t, block in cells.items()}
    close(sum(raw.values()), root, "full heat+feedback root kept exactly", tol=2e-8)
    direct = sum(p**(8+sum(t))*mass for t, mass in raw.items())
    factored = root*p**8*prodz*sw/s0
    close(direct, factored, "one full thermal root times normalized CP product", tol=2e-9)
    # Missing Z_H/s0 is a material normalization error, not an ignored constant.
    wrong = math.exp(j)*float(np.trace(mm(kref, tilted)))*p**8
    need(abs(wrong/direct-1) > .99, "hostile omitted absolute root normalization")
    # One marginal for the untouched RIGHT is retained at every branch.
    right = np.trace(normalized.reshape(16,4,16,4), axis1=0, axis2=2)
    old_right = np.trace(rho.reshape(4,4,4,4), axis1=0, axis2=2)
    close(right, old_right, "complete scalar weighting preserves every old RIGHT marginal")
    ell = -math.log(p)
    action = -math.log(direct)/ell
    terms = (-math.log(root)/ell, -sum(math.log(1-p*p*x) for x in q)/ell,
             -math.log(sw/s0)/ell)
    close(action, 8+sum(terms), "absolute action identity with all root and local terms")
    beta = 2*p*p
    b, c = scene()
    sinf = sum(scene_heat(b,c,2*math.cos(2*math.pi*n/128),beta) for n in range(128))/128
    s = float(sinf[32,32]); e = float(np.linalg.norm(k-s*np.eye(16), ord=2))
    shortest = length
    analytic = 2*halo(beta/11, shortest)
    need(e < analytic+3e-12, "actual single-graph local thermal scalar approximation")
    return {"action":action,"terms":terms,"q":q,"prodz":prodz,
            "s0":s0,"sw":sw,"root":root,"dimension":d,"shortest":shortest,
            "e":e,"e_bound":analytic,"normalized":normalized,"unweighted":unweighted,
            "k":k,"clock":clock}


def anisotropy_control(p):
    q = .42
    rho = old_state()
    h = np.diag((.3, -.2, .1, -.2))
    trace_old = np.trace(rho.reshape(4,4,4,4), axis1=1, axis2=3)
    z = 1-p*p*q
    zeta = -p*p*float(np.trace(mm(h, trace_old)))/z
    need(abs(zeta) > 1e-3, "scalar centre alone leaves a real independent row")
    def mass(t):
        e1 = q*np.eye(4)+t*h
        e0 = np.eye(4)-e1
        need(np.linalg.eigvalsh(e1).min()>0 and np.linalg.eigvalsh(e0).min()>0,
             "actual positive instrument perturbation")
        return float(np.trace(mm(e0+p*e1, trace_old)))/z
    step = 1e-6
    derivative = (math.log(mass(step))-math.log(mass(-step)))/(2*step)
    close(derivative, zeta, "FQ12 source persists when K is exactly scalar", tol=2e-10)
    return {"center_q":q,"independent_trace_source":format(zeta,".13g"),
            "finite_difference_error":format(abs(derivative-zeta),".4g"),
            "thermal_error":0,"scalar_effect_family_required":True}


def feedback_bounds(p, cold):
    z = 2**-20; r = 4
    a = np.diag((.8,.6,.4,.2))
    da = np.array([[.1,.02,0,0],[.02,-.1,0,0],[0,0,.03,0],[0,0,0,-.04]])
    b = np.array([[0,.06,.03,0],[.01,0,0,0],[0,0,.04,0],[0,0,0,-.02]])
    results = []
    for m in (1,2,4,8):
        c = cold**m*a
        dc = cold**m*da+cold**(m-1)*b
        denominator = (1-z)*np.eye(r)+z*mm(c.T,c)
        dj = -z*float(np.trace(np.linalg.solve(denominator,mm(dc.T,c)+mm(c.T,dc))))
        bound = 2*r*z/(1-z)*(cold**(2*m)*np.linalg.norm(da,ord=2)
                            +cold**(2*m-1)*np.linalg.norm(b,ord=2))
        all_bound = 2*r*z/(1-z)*cold**m*np.linalg.norm(dc,ord=2)
        need(abs(dj)<=bound+1e-30 and abs(dj)<=all_bound+1e-30,
             "full matrix RAW resolvent source bounds")
        results.append({"M":m,"actual_matrix_derivative":format(dj,".11g"),
                        "structured_upper":format(bound,".11g"),
                        "full_tangent_upper":format(all_bound,".11g")})
    return results


def fresh_guard_composition(ne):
    # Consume the independently exact all-branch table. Its full 35-stage
    # native-column verification lives in its owner; it is not replaced by
    # this small matrix/product diagnostic.
    from check_fresh_guard_reader import golden_tables, gf
    from check_golden_record_race import gold, p as exact_p
    rows, means, factors, counting, nchecks = golden_tables()
    # An average conditional factor does NOT preserve the old conditional
    # state. Retain all actual H,E rows in the economically weighted CP map.
    h_sensitive=[]
    for t in (0,1):
        h_weight=gold(0); whole_weight=gold(0)
        for row in rows:
            if row["T"] != t:
                continue
            born=exact_p**(2+row["H"]+row["E"])
            weighted=born*exact_p**row["declared_net_price"]
            whole_weight+=weighted
            if row["H"]:
                h_weight+=weighted
        need(whole_weight==factors[t],"all fine physical guard rows summed once")
        expected_h=gold(1)/(1+2*exact_p) if t==0 else gold(1)/2
        need(h_weight/whole_weight==expected_h,
             "true tilted H marginal, not the original p^2 marginal")
        need(expected_h!=exact_p**2,"conditional quantum state really changes under the tilt")
        # K=(I+P_H=1)/2 is positive, <=I, and sees the missing state change.
        actual_numerator=(whole_weight+h_weight)/2
        wrongly_scaled_original=whole_weight*(1+exact_p**2)/2
        need(actual_numerator!=wrongly_scaled_original,
             "positive H-sensitive K kills coarse factor times original state shortcut")
        h_sensitive.append({"T":t,"actual_tilted_H1":gf(expected_h),
                            "original_H1":gf(exact_p**2),
                            "positive_K_difference":gf(actual_numerator-wrongly_scaled_original)})
    p=float(ne.P); ell=-math.log(p); a=float(ne.A)
    a0=p**3+p**5; a1=2*p**5; kappa=(a0-a1)/a0
    close(kappa,1/math.sqrt(5),"exact guard factors consumed with the proper ratio")
    c1=p**4*(1+a); c0=c1+p**6*(a-p)
    need(0<c1<c0<75125/262144<1/3,"true nonscalar guard is a strict contraction")
    cold=np.diag((c0,c1))
    generator=np.array([[0.,-1.],[1.,0.]])
    theta=.37
    query=np.array([[math.cos(theta),-math.sin(theta)],
                    [math.sin(theta),math.cos(theta)]])
    dquery=mm(generator,query)
    contractions=[]
    for m in (1,2,4,8):
        full=np.eye(2)
        for _ in range(m):
            full=mm(cold,query,full)
        derivative=mm(cold,dquery)
        for _ in range(m-1):
            derivative=mm(cold,query,derivative)
        need(np.linalg.norm(full,ord=2)<=c0**m*(1+1e-12),
             "nonscalar cold factors need not commute with the fresh query")
        need(np.linalg.norm(derivative,ord=2)<=c0**m*(1+1e-12),
             "true norm product keeps a current query derivative")
        contractions.append({"M":m,"actual_norm":format(np.linalg.norm(full,ord=2),".11g"),
                             "upper_c0_power":format(c0**m,".11g")})
    # Explicit retained-bit dependence is in the full code, including +T.
    for q0,q1 in ((.4,.46),(.2,.8)):
        direct=sum((a1 if t0 else a0)*(a1 if t1 else a0)
                   *(q0 if t0 else 1-q0)*(q1 if t1 else 1-q1)
                   for t0,t1 in product(range(2),repeat=2))
        close(direct,a0*a0*(1-kappa*q0)*(1-kappa*q1),"all four fresh guard products")
    # Crucial negative control: the whole query-only endpoint derivative
    # can cancel, while interleaved nonscalar cold keeps a real source.
    # FQ17 must use insertion norms, not ||D(Q2 Q1)|| from scalar FQ10.
    query_only_derivative=-generator+generator
    inserted_derivative=mm(cold,mm(cold,generator)-mm(generator,cold))
    close(query_only_derivative,np.zeros((2,2)),"query-only derivative cancels exactly")
    need(np.linalg.norm(inserted_derivative,ord=2)>1e-3,
         "nonscalar cold prevents cancellation of the query insertions")
    need(np.linalg.norm(inserted_derivative,ord=2)<=2*c0*c0,
         "sum of actual insertion derivatives gives a valid bound")
    step=1e-6
    def mixed(t):
        rot=np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])
        return mm(cold,rot.T,cold,rot)
    close((mixed(step)-mixed(-step))/(2*step),inserted_derivative,
          "noncommuting cancellation control matches actual matrix differentiation",tol=1e-10)
    return {"known_H1_not_required":True,"conditional_factors_Qp":[gf(x) for x in factors],
            "kappa":"1/sqrt(5)","positive_per_query_minimum_gain":format(kappa/ell,".13g"),
            "raw_cold_not_scalar":True,"raw_c0":format(c0,".15g"),
            "raw_c1":format(c1,".15g"),"nonscalar_interleaving_controls":contractions,
            "fine_tilted_state_negative_control":{"operator":"(I+P_H1)/2",
                "arithmetic":"exact Q(p)","rows":h_sensitive,
                "required_map":"sum over actual t,h,e Kraus branches with each p^s; preserve original unweighted Gamma and full Z_N"},
            "query_cancellation_control":{"query_only_derivative_norm":0,
                "interleaved_derivative_norm":format(np.linalg.norm(inserted_derivative,ord=2),".13g"),
                "required_norm":"sum of actual query-insertion derivative norms"},
            "all_branch_owner":"check_fresh_guard_reader.py",
            "remaining_scope":"economic weighting is conditional; full 35-stage thermal graph must be built for its actual geometry"}


def main():
    ne, digest = load_control()
    live, cold = exact_live_cold(ne)
    need(live["native_sha256"] == digest, "one pinned native alphabet")
    mats, word = native_word(ne)
    center = thermal_identity(ne,mats)
    h = 2e-5
    plus = thermal_identity(ne,mats,h)
    minus = thermal_identity(ne,mats,-h)
    direct_derivative = (plus["action"]-minus["action"])/(2*h)
    term_derivative = sum((x-y)/(2*h) for x,y in zip(plus["terms"],minus["terms"]))
    close(direct_derivative,term_derivative,"full absolute source includes moving K, root and old output",tol=4e-9)
    p = float(ne.P); ell = -math.log(p)
    b = [(plus["q"][i]-minus["q"][i])/(2*h) for i in range(2)]
    expected_code = sum(p*p*x/(ell*(1-p*p*q)) for x,q in zip(b,center["q"]))
    code_difference=(plus["terms"][1]-minus["terms"][1])/(2*h)
    close(code_difference, expected_code, "positive economic code source on actual fresh effects",tol=4e-9)
    bnorm=np.linalg.norm((plus["unweighted"]-minus["unweighted"])/(2*h),ord="nuc")
    wnorm=np.linalg.norm((plus["normalized"]-minus["normalized"])/(2*h),ord="nuc")
    rnorm=np.linalg.norm((plus["k"]-minus["k"])/(2*h),ord=2)
    local_difference=(plus["terms"][2]-minus["terms"][2])/(2*h)*ell
    estimate=(2*rnorm+center["e_bound"]*(bnorm+wnorm))/math.exp(-4*p*p)
    need(abs(local_difference)<=estimate+3e-10,"normalized thermal derivative has no inverse product mass")
    # Even when product masses are tiny, the normalized-map estimate uses
    # only per-copy z>=p. This scalar arithmetic is not a larger native build.
    masses=[{"M":m,"born_weighted_mass":format((1-p*p*.42)**m,".10g"),
             "positive_code_gain_on_diagonal":format(m*p*p/(ell*(1-p*p*.42)),".12g")}
            for m in (1,8,64,256)]
    sources=("check_fresh_query_economic_source.py","check_complete_work_source.py",
             "check_live_parser.py","check_local_gibbs_records.py","check_fresh_guard_reader.py")
    print(json.dumps({"status":"PASS",
        "scientific_status":{"physical_economic_weight_selected":False,
                             "whole_Einstein_bank_built":False,"obligation_C_discharged":False,
                             "GR_closed":False},
        "source_sha256":{name:sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in sources},
        "exact_raw_live":live,
        "native_entangled_cp_and_thermal_fixture":{"word":word,"births":2,
            "input_Spin_dimension":4,"untouched_RIGHT_dimension":4,
            "clock_dimension":center["dimension"],"full_two_grade_modes":425*center["dimension"],
            "actual_report_probabilities":[format(x,".14g") for x in center["q"]],
            "actual_root_partition":format(center["root"],".14g"),
            "local_unweighted_mass":format(center["s0"],".14g"),
            "local_tilted_normalized_mass":format(center["sw"],".14g"),
            "product_weight":format(center["prodz"],".14g"),
            "full_source_identity_error":format(abs(direct_derivative-term_derivative),".4g"),
            "scope":"literal two-query native graph, not the full query-plus-LIVE clock; smooth matrix derivative is a mathematical diagnostic, not an admission theorem"},
        "anisotropy_negative_control":anisotropy_control(p),
        "feedback_matrix_controls":feedback_bounds(p,cold),
        "fresh_guard_35_stage_composition":fresh_guard_composition(ne),
        "fresh_scalar_product_arithmetic":masses,
        "conditional_parent_result":"one full absolute graph root; positive fresh-query source; no old-memory independence or inverse rare-product penalty",
        "remaining_physical_operand":"true same-history economic weights, field-bank admission, and actual full source/gain/lift budgets"},ensure_ascii=False,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
