"""Bounded actual128 entropy checks and finite Golden-clock source controls."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import platform
import numpy as np
import scipy
import sympy as S


def run():
    root = Path(__file__).resolve()
    while not (root / "AGENTS.md").is_file():
        if root.parent == root:
            raise RuntimeError("repository root not found")
        root = root.parent
    pins = {
        "02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md":
            "2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79",
        "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/PROOF.md":
            "09d7c1cebffcb70df03b8e9f3ea274cc554f8ad4e26dfaa87ad0eacdde822be3",
        "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py":
            "1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9",
        "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/RESULT.md":
            "d1c3cff174b2e4d03481ca6b3d18a1da2d3b65baba1f2dbf886324d8ce7f607d",
        "02_REGISTRY/research/A4D_TWO_LETTER_GOLDEN_COST_HERALD_SOURCE_2026_10_21.md":
            "d2fbf6e2daec763dc8aaf1a32a1b654e51156e16fc8daf272ea9f49990cfc907",
    }
    checks = []

    def ok(condition, label):
        if not bool(condition):
            raise RuntimeError(label)
        checks.append(label)

    def eq(left, right, label):
        ok(S.simplify(left-right) == 0, label)

    for path, sha in pins.items():
        ok(hashlib.sha256((root/path).read_bytes()).hexdigest() == sha, "pin "+path)
    ps = (S.sqrt(5)-1)/2
    ss, aa, rr = S.symbols("s a r", positive=True)
    den = 1-2*ps**2*ss
    ut = (2*ps*ss-ss**2)/den
    rt, rc = 2*ps**3*ss/den, 2*ps**2*ss+ps*ss**2
    eq(S.diff(ut, ss), 2*(ps-ss+ps**2*ss**2)/den**2,
       "exact marked-event derivative with its scalar normalizer retained")
    eq(S.limit(ut/ss, ss, 0), 2*ps, "Golden target has event-time factor p")
    eq(S.limit(rt/ss, ss, 0), ps*S.limit(rc/ss, ss, 0),
       "target and padded shorter candidate have the same limiting port count")
    ell = (2-rr)/(aa**2*(1-rr)*(2-ss))-4/(aa**2*(2-ss)**2)
    eq(ell, (2*rr-(2-rr)*ss)/(aa**2*(1-rr)*(2-ss)**2),
       "exact normalized-jump first-source invariant at physical nu=h*a")
    eq(-S.log(ps)/S.log(1/ps), 1, "Golden timestamp Jacobian is one phi-unit per event")
    vv = S.Symbol("v", positive=True)
    remainder = -(1-vv)*S.log(1-vv)-vv
    eq(S.diff(remainder, vv), S.log(1-vv), "exact Bernoulli-entropy remainder derivative")
    eq(remainder.subs(vv, 0), 0, "Bernoulli-entropy remainder has zero base value")
    eq(S.diff(rt, ss), 2*ps**3/den**2, "exact complete marked port-source coefficient")

    source = root/"02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
    spec = importlib.util.spec_from_file_location("d0_owned_uniform_for_entropy", source)
    owner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owner)  # Imports definitions; does not run the owned 115-control main.
    p = owner.P
    logphi = np.log(1/p)
    initial_a = .7

    def entropy(q):
        q = np.asarray(q).ravel()
        if np.any(q < 0):
            raise RuntimeError("negative probability")
        bright = q > 0  # Exact 0 log 0 convention, no probability floor.
        return float(-np.sum(q[bright]*np.log(q[bright]))/logphi)

    def bernoulli(u):
        return float(-(u*np.log(u)+(1-u)*np.log1p(-u))/logphi)

    fixture_rows = []
    for L in (4, 8):
        h = 1/L
        w = 4*np.sin(np.pi*h)**2
        phases = (np.exp(2j*np.pi*h), 1, 1, 1)

        def kraus(a):
            return owner.native(0., nu=h*a, phases=phases)[0]

        a = initial_a
        k = kraus(a)
        s = p*p*h*h*a*a*w/128
        u = 2*s-s*s
        du = 4*s*(1-s)/a
        ok(np.linalg.norm(k[0]-(1-s)*np.eye(16)) < 1e-12,
           f"actual scalar blank on fullCAR16 first-shell fixture L{L}")
        q1 = np.sum(abs(k)**2, axis=(1, 2))/16
        ok(abs(np.sum(q1)-1) < 1e-12, f"all128 one-round probabilities retained L{L}")
        ok(abs(np.sum(q1[1:])-u) < 1e-12, f"actual full nonblank effect matches physical event probability L{L}")
        products = np.einsum("aij,bjk->abik", k, k, optimize=True)
        q2 = np.sum(abs(products)**2, axis=(2, 3))/16
        ok(q2.size == 16384 and abs(np.sum(q2)-1) < 1e-12,
           f"all16384 original two-round records normalized L{L}")
        ok(np.max(abs(q2[0, 1:]-(1-u)*q1[1:])) < 1e-12
           and np.max(abs(q2[1:, 0]-(1-u)*q1[1:])) < 1e-12,
           f"time positions factor while actual quantum marks remain L{L}")
        mark1, mark2 = q1[1:]/u, q2[1:, 1:]/u**2
        ok(abs(np.sum(mark1)-1) < 1e-9 and abs(np.sum(mark2)-1) < 1e-9,
           f"complete normalized one- and two-event mark laws L{L}")
        hfull = entropy(q2)
        decomposition = 2*bernoulli(u)+2*u*(1-u)*entropy(mark1)+u*u*entropy(mark2)
        ok(abs(hfull-decomposition) < 5e-11,
           f"full original-record entropy equals exact event-time/mark chain L{L}")
        step = 1e-4
        dk = (-kraus(a+2*step)+8*kraus(a+step)-8*kraus(a-step)+kraus(a-2*step))/(12*step)
        qa = p*p*h*h*w*(2-h*h*a*a)/(128*(1-h*h*a*a))
        qnorm = np.einsum("aji,ajk->ik", dk.conj(), dk)
        ok(np.linalg.norm(qnorm-qa*np.eye(16)) < 1e-10,
           f"physical scaled all128 derivative agrees with owned exact cross L{L}")
        dj = dk[1:]/np.sqrt(u)-k[1:]*du/(2*u**1.5)
        jnorm = np.einsum("aji,ajk->ik", dj.conj(), dj)
        ell_num = qa/u-(2*s/a)**2/u**2
        ok(ell_num >= 0 and np.linalg.norm(jnorm-ell_num*np.eye(16)) < 1e-8,
           f"actual normalized jump source stays controlled as nu approaches zero L{L}")
        fixture_rows.append({"L":L,"all_record_entropy":hfull,
                             "chain_residual":abs(hfull-decomposition),
                             "normalized_jump_source_square":ell_num})
        del products

    rows = []
    for L in (8, 16, 32, 64, 128):
        h = 1/L
        a = initial_a
        n = 128*L**4
        m = int(S.floor(ps*n))
        w = 4*np.sin(np.pi*h)**2
        s = p*p*h*h*a*a*w/128
        ds = 2*s/a
        u, du = 2*s-s*s, 2*(1-s)*ds
        den = 1-2*p*p*s
        ut = (2*p*s-s*s)/den
        dut = 2*(p-s+p*p*s*s)*ds/den**2
        lt, lc, dlt, dlc = n*ut, m*u, n*dut, m*du
        timediff = n*bernoulli(ut)-m*bernoulli(u)
        dtimediff = dlt*np.log((1-ut)/ut)/logphi-dlc*np.log((1-u)/u)/logphi
        lr = np.log(n/m)/logphi
        maxlog = max(abs(np.log(lt)), abs(np.log(lc)))
        value_bound = (abs(lt-lc)*(np.log(n)+maxlog)
                       +n*ut**2/(2*(1-ut))+m*u**2/(2*(1-u)))/logphi
        source_bound = (abs(dlt-dlc)*(np.log(n)+maxlog)
                        +abs(dlc)*abs(np.log(lt/lc))
                        +abs(dlt)*ut/(1-ut)+abs(dlc)*u/(1-u))/logphi
        ok(abs(timediff-lc*lr) <= value_bound+1e-8,
           f"finite timestamp value obeys explicit Bernoulli remainder bound L{L}")
        ok(abs(dtimediff-dlc*lr) <= source_bound+1e-7,
           f"finite timestamp first source obeys explicit remainder bound L{L}")
        rt, rc = 2*p**3*s/den, 2*p*p*s+p*s*s
        drt, drc = 2*p**3*ds/den**2, (2*p*p+2*p*s)*ds
        portdiff, dportdiff = m*rc-n*rt, m*drc-n*drt
        tau, dtau = 8*np.pi**2*p*p*a*a, 16*np.pi**2*p*p*a
        mu, dmu = p*tau, p*dtau
        logxt = n*(2*np.log1p(-s)-np.log1p(-2*p*p*s))
        logxc = 2*m*np.log1p(-s)
        dlogxt = n*(-2*ds/(1-s)+2*p*p*ds/den)
        dlogxc = -2*m*ds/(1-s)
        log_bound = 2*s+(n-m)*s*s/(1-s)+2*n*p**4*s*s/den
        dlog_bound = 2*ds+2*(n-m)*s*ds/(1-s)+4*n*p**4*s*ds/den
        ok(abs(logxt-logxc) <= log_bound+1e-12 and abs(dlogxt-dlogxc) <= dlog_bound+1e-11,
           f"finite normalized Book corners have the proved common C1 limit L{L}")
        z = 2.**-20
        xt, xc = np.exp(logxt), np.exp(logxc)
        dj_t = -16384*z*xt*dlogxt/(1-z+z*xt)
        dj_c = -16384*z*xc*dlogxc/(1-z+z*xc)
        ok(timediff > 0 and dtimediff > 0,
           f"Gold-clock timestamp defect is not erased as a constant L{L}")
        rows.append({"L":L,"n":n,"m":m,
                     "timestamp_entropy_difference":timediff,
                     "timestamp_source_difference":dtimediff,
                     "known_port_defect_after_baseline":portdiff,
                     "known_port_source_defect":dportdiff,
                     "mu_limit":mu,"mu_source_limit":dmu,
                     "Book_source_difference":dj_t-dj_c})
    ok(abs(rows[-1]["Book_source_difference"]) < 1e-8
       and rows[-1]["timestamp_source_difference"] > 1,
       "matching Book source does not imply matching timestamp price source")
    return {"status":"PASS","input_snapshot":"42649a5f575c2c72f6d63de5a8708e8100002972",
            "source_pins":pins,"checks":checks,"check_count":len(checks),
            "native_bounded_fixtures":fixture_rows,"physical_horizon_formula_checks":rows,
            "environment":{"python":platform.python_version(),"sympy":S.__version__,
                           "numpy":np.__version__,"scipy":scipy.__version__},
            "scope":{"literal_native128_outcomes_in_bounded_fixture":True,
                     "fixture_CAR_dimension":16,"fixture_is_one_Fourier_block":True,
                     "fixture_preparation_rank":16,"all_eight_modes_replayed":False,
                     "large_horizon_paths_simulated":False,"all_horizon_C1_claim_is_analytic":True,
                     "finite_formula_data_are_timing_and_known_port_components":True,
                     "actual_native_padding_controller_constructed":False,
                     "Book03_Info_selected":False,"full42_source_claimed":False,"GR_closed":False}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2)+"\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
