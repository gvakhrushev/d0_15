#!/usr/bin/env python3
"""Mixed Y-current search; recorded candidates fail the necessary equations.

Recovered at publication after environment disconnection. Completed model
runs and flat controls predate that event; restored source needs independent
optional replay. This is not an exact joint-field certificate.
Optional dependencies: jax==0.4.35, jaxlib==0.4.35.
"""
import os
os.environ.setdefault("JAX_ENABLE_X64", "true")
os.environ.setdefault("XLA_FLAGS", "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import argparse
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.optimize import least_squares
import jax
import jax.numpy as j
from jax.scipy.linalg import expm
jax.config.update("jax_enable_x64", True)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "certificates"))
import a4d_y_curved_joint_rational_stencil as S
import a4d_y_curved_joint_center_gradient_module_check as C

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--period", type=int, default=4)
parser.add_argument("--amplitude", type=float, default=1.0)
parser.add_argument("--seed", choices=("zero", "singular"), default="zero")
parser.add_argument("--output-dir", type=Path, default=Path.cwd())
args = parser.parse_args()
N = args.period
if N < 4 or N % 4:
    parser.error("period must be a positive multiple of four")
h = 1/N
epsilon = args.amplitude*h*h
seed = args.seed
args.output_dir.mkdir(parents=True, exist_ok=True)

B, Cc, target = C.target()
B, Cc = np.array(B, float), np.array(Cc, float)
I = np.eye(4)
eta = np.diag([1, -1, -1, -1])
Y = np.array(S.Y, float)
Y2 = Y@Y
Pperp, Ppar = -Y2/3, I+Y2/3
gen = np.array(S.GEN, float)
pairs = S.PAIRS
k = np.array([0, 1, -1, 0])
sg = np.array(S.ETA_SIG)
star = np.zeros((6, 6))
for col, (row, sign) in enumerate(S.STAR_MAP):
    star[row, col] = sign
G2 = np.diag([sg[a]*sg[b] for a, b in pairs])
contract = G2@star


def wedge_np(u, v):
    return np.array([u[a]*v[b]-u[b]*v[a] for a, b in pairs])


f = 1+epsilon*np.cos(2*np.pi*np.arange(N)/N)
coframe = I+(f[:, None, None]-1)*Pperp
area = np.zeros((N, 6, 6))
darea = np.zeros((N, 6, 10, 6))
for x in range(N):
    lifts = []
    for a, b in S.SYM:
        q = np.zeros((4, 4))
        q[a, b] = q[b, a] = 1
        X = (Ppar@eta@q@Ppar/2
             + (Ppar@eta@q@Pperp+Pperp@eta@q@Ppar)/(1+f[x])
             + Pperp@eta@q@Pperp/(2*f[x]))
        assert np.max(abs(coframe[x]@X+X@coframe[x]-eta@q)) < 1e-14
        lifts.append(X)
    for face, (a, b) in enumerate(pairs):
        u, v = [z for z in range(4) if z not in (a, b)]
        area[x, face] = S.orient(a, b)*wedge_np(coframe[x, :, u], coframe[x, :, v])@contract
        for mi, X in enumerate(lifts):
            darea[x, face, mi] = S.orient(a, b)*(
                wedge_np(X[:, u], coframe[x, :, v])
                + wedge_np(coframe[x, :, u], X[:, v]))@contract
area, darea = j.array(area), j.array(darea)
eta, B, gen, Y, Y2, I = j.array(eta), j.array(B), j.array(gen), j.array(Y), j.array(Y2), j.eye(4)


def linv(M):
    return eta@j.swapaxes(M, -1, -2)@eta


def links(x):
    x = x.reshape(N, 96)
    coefficients = (x[:, :94]@B.T).reshape(N, 4, 4, 6)
    W = j.einsum("xpra,aij->xprij", coefficients, gen)
    K = expm(W)
    a = 1+x[:, 94:]
    cy = (I+(4*a/(4+3*a*a))[:, :, None, None]
          * j.array([1.0, -1.0])[None, :, None, None]*Y
          + (2*a*a/(4+3*a*a))[:, :, None, None]*Y2)
    K = K.at[:, 0, 0].set(cy[:, 0]@K[:, 0, 0])
    K = K.at[:, 2, 0].set(cy[:, 1]@K[:, 2, 0])
    return K


def curvatures(K):
    out = []
    for a, b in pairs:
        right = j.roll(j.roll(K, -int(k[a]), axis=0), -1, axis=1)[:, :, b]
        top = linv(j.roll(j.roll(K, -int(k[b]), axis=0), -1, axis=1)[:, :, a])
        P = K[:, :, a]@right@top@linv(K[:, :, b])
        F = (P-linv(P))/2
        out.append(j.stack([F[:, :, aa, bb]*sg[bb] for aa, bb in pairs], axis=-1))
    return j.stack(out, axis=2)


def action(x):
    return j.sum(curvatures(links(x))*area[:, None, :, :])


grad = jax.grad(action)


def metric(x):
    return j.einsum("xpfb,xfmb->xpm", curvatures(links(x)), darea)


def physical_coordinates(x):
    x = j.asarray(x).reshape(N, 96)
    return x.at[:, 94:].add(-j.mean(x[:, 94:])).reshape(-1)


def residual(x):
    x = physical_coordinates(x) if args.amplitude else x
    E = metric(x)
    c = x.reshape(N, 96)[:, 94:]
    scale = epsilon if epsilon else 1.0
    # Full physical chart gradient: pin the parameters, not the Euler rows.
    return j.concatenate([
        grad(x)/scale,
        ((E[:, 1:]-E[:, :1])/scale).reshape(-1),
        j.array([j.mean(c)]),
    ])


funjax = jax.jit(residual)
jacjax = jax.jit(jax.jacfwd(residual))
mj, gj = jax.jit(metric), jax.jit(grad)
x0 = np.zeros(96*N)
if seed == "singular":
    theta = np.array([0, 2*np.pi/N, -2*np.pi/N, 0])
    Hq, Mq = np.zeros((96, 96), complex), np.zeros((40, 96), complex)
    for terms, owner in ((S.ATERMS, Hq), (S.QTERMS, Mq)):
        for d, entries in terms.items():
            factor = np.exp(1j*np.dot(d, theta))
            for (r, c), value in entries.items():
                owner[r, c] += float(value)*factor
    erase = np.concatenate([np.tile(-np.eye(10), (3, 1)), np.eye(30)], axis=1)
    Qq = np.concatenate([Hq, erase@Mq])
    center = Cc@np.ones(2)
    wseed = np.linalg.lstsq(Qq@np.array(B), -Qq@center, rcond=None)[0]*h
    phase = np.exp(2j*np.pi*np.arange(N)/N)
    xx = x0.reshape(N, 96)
    xx[:, :94] = np.real(phase[:, None]*wseed[None, :])
    xx[:, 94:] = h*np.real(phase[:, None])
    assert np.max(abs(x0)) < 0.15

t = time.monotonic()
y0 = np.array(funjax(x0))
J0 = np.array(jacjax(x0))
print("INITIAL", N, "EPSILON", epsilon, "RAW_RESID",
      np.max(abs(y0[:-1]))*epsilon, "COMPILE_SECONDS", time.monotonic()-t, flush=True)
if not args.amplitude:
    H, MC = np.zeros((96*N, 96*N)), np.zeros((40*N, 96*N))
    E = np.concatenate([np.array(B), Cc], axis=1)
    for terms, owner in ((S.ATERMS, H), (S.QTERMS, MC)):
        nr = 96 if owner is H else 40
        for d, entries in terms.items():
            shift = int(np.dot(d, k))
            for (r, c), value in entries.items():
                for site in range(N):
                    owner[nr*site+r, 96*((site+shift) % N)+c] += float(value)
    EB = np.kron(np.eye(N), E)
    dh = float(np.max(abs(J0[:96*N]-EB.T@H@EB)))
    actual_m = np.array(jax.jacfwd(metric)(x0)).reshape(40*N, 96*N)
    dm = float(np.max(abs(actual_m-MC@EB)))
    print("FLAT_OWNER_MATCH", dh, dm, "VACUUM", float(np.max(abs(y0))), flush=True)
    assert dh < 1e-12 and dm < 1e-12 and np.max(abs(y0)) < 1e-12
    raise SystemExit(0)

result = least_squares(
    lambda x: np.array(funjax(x)), x0,
    jac=lambda x: np.array(jacjax(x)),
    bounds=(-0.15, 0.15), max_nfev=40,
    ftol=1e-12, xtol=1e-12, gtol=1e-12,
)
x = np.array(physical_coordinates(result.x)).reshape(N, 96)
c, w = x[:, 94:], x[:, :94]
DG = []
for phase in (0, 1):
    for s in (1, 2, 3):
        DG.append(np.roll(c[:, phase], -int(k[s]))-c[:, phase])
        DG.append(np.roll(c[:, 1-phase], -int(k[s]))-c[:, phase])
DG = np.array(DG).T
conn = np.array(gj(x.reshape(-1)))
metric_values = np.array(mj(x.reshape(-1)))
erasure = metric_values[:, 1:]-metric_values[:, :1]
w_inf = float(np.max(np.sum(abs(w), axis=1)))
g_inf = float(np.max(np.sum(abs(DG), axis=1)))
repeat = N**3/4
standard = [col for col in range(96) if col not in {3, 4, 5, 51, 52, 53}]
w_phases = np.array([col//24 for col in standard]+[0, 0, 2, 2])
wp = max(float(np.max(np.sum(abs(w[:, w_phases == phase]), axis=1))) for phase in range(4))
gp = float(np.max(abs(DG)))
ws = repeat*float(np.sum(abs(w)))
gs = repeat*max(float(np.sum(abs(DG[:, move]))+np.sum(abs(DG[:, move+6]))) for move in range(6))
record = {
    "N": N, "h": h, "epsilon": epsilon, "seed": seed,
    "status": int(result.status), "nfev": result.nfev, "cost": float(result.cost),
    "scaled_residual_max": float(np.max(abs(result.fun[:-1]))),
    "connection_chart_residual_max": float(np.max(abs(conn))),
    "metric_phase_erasure_max": float(np.max(abs(erasure))),
    "mean_center": float(np.mean(c)), "center_sup": float(np.max(abs(c))),
    "w_all_phase_fibre_sup": w_inf, "graph_all_move_fibre_sup": g_inf,
    "X_fibre_aggregate_sup": w_inf+g_inf,
    "X_fibre_aggregate_sup_over_h2": (w_inf+g_inf)/h**2,
    "X_sum_over_all_graph_moves": repeat*(float(np.sum(abs(w)))+float(np.sum(abs(DG)))),
    "X_physical_component_sup": wp+gp,
    "X_physical_component_sup_over_h2": (wp+gp)/h**2,
    "X_physical_component_sum": ws+gs,
    "X_physical_component_sum_over_h2": (ws+gs)/h**2,
    "necessary_equations_pass_at_1e-10": bool(np.max(abs(conn)) < 1e-10 and np.max(abs(erasure)) < 1e-10),
    "note": "necessary EK+phase-erasure probe; no prescribed source; not an exact joint solution",
}
print("RESULT", json.dumps(record), flush=True)
suffix = str(N)+("-"+seed if seed != "zero" else "")
np.savez(args.output_dir/("mixed-rescue-"+suffix+".npz"), x=x, metric=metric_values, residual=result.fun)
with open(args.output_dir/("mixed-rescue-"+suffix+".json"), "w") as ff:
    json.dump(record, ff, indent=2)
