"""An admitted stored-adjoint rotational wave and its v8 price Hessian.

The native legs have constant observer e0, identity links, and leg 2 depends
only on coordinates 0 and 1.  A homogeneous length acceleration repairs the
complete 128-dimensional occupied-shell matter second jet.  The FULL v8
H+J_program+R Hessian nevertheless excludes this first velocity from a C2
joint critical curve.  This is a statement about this wave, with first link
velocities zero; it is not a no-go for curved native critical points.

Only native creator definitions and the published v8 root rectangle are
consumed.  No earlier checker, root search, receipt writer, or large Fock
operator is run.  All 4096 thermal modes, sixteen Fock components, reference
128, finite record count, and heat normalization remain in the scalar sum.
"""
from __future__ import annotations

from collections import Counter
import ast
from decimal import Decimal, localcontext
from functools import lru_cache
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from types import SimpleNamespace

import mpmath as mp
import sympy as s


ROOT = Path(__file__).resolve().parents[4]
V8 = "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/"
RECEIPT_SHA = "da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9"
Q = (3, 3, 0, 0)
L = 8
ROUNDS = 8192
FOCK = 16
REFERENCE = 128
SHELL = tuple(tuple(sign if i == a else 0 for i in range(4))
              for a in range(4) for sign in (1, 7))
J23 = s.zeros(4)
J23[2, 3], J23[3, 2] = -1, 1


def require(condition, label):
    if not bool(condition):
        raise AssertionError(label)


def _zero(value):
    if isinstance(value, s.MatrixBase):
        return all(_zero(x) for x in value)
    x = s.expand(value)
    return x == 0 or s.cancel(x) == 0


def _matrix(value):
    return value.applyfunc(s.expand)


def gamma_second(d, o, rotated_norm_squared):
    """Positive -E2 on each of the two occupied +/-e2 blocks.

    A=|8(exp(3*pi*i/4)-1)|^2, B=2A(d+o), lambda1=|z(e2)|^2.
    X*X=(B lambda1 ||Jv2||^2/4) I16 on each of the two edges;
    the gaps are B and B+256o.  The other six shell blocks vanish.
    """
    A = 128+64*s.sqrt(2)
    B = 2*A*(d+o)
    lambda1 = 128-64*s.sqrt(2)
    return lambda1*rotated_norm_squared*(1+B/(B+256*o))/2


def native_row_family(F, parameter, phi, gamma=None):
    """Raw positive creator frame; native legs are eta times its rows.

    n=e0 and A_r=I.  Because phi is independent of x2, all exact stored
    parallel-leg conditions persist.  Optional gamma is the matter repair:
    scale=sqrt(1+gamma*t^2/(2*lambda1*d)), d=||F_2||^2.
    The full frame and all sixteen exterior components are retained.
    """
    R = s.eye(4)
    angle = parameter*phi
    R[2, 2] = R[3, 3] = s.cos(angle)
    R[2, 3], R[3, 2] = -s.sin(angle), s.sin(angle)
    d = (F.row(2)*F.row(2).T)[0]
    scale = (s.S.One if gamma is None else
             s.sqrt(1+gamma*parameter**2/(2*(128-64*s.sqrt(2))*d)))
    result = F.copy()
    result[2, :] = (scale*R*F.row(2).T).T
    return result


def qadd(a, b):
    return a[0]+b[0], a[1]+b[1]


def qsub(a, b):
    return a[0]-b[0], a[1]-b[1]


def qmul(a, b):
    return a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def qsum(values):
    result = (0, 0)
    for value in values:
        result = qadd(result, value)
    return result


RE = ((0, 0), (-8, 4), (-8, 0), (-8, -4), (-16, 0),
      (-8, -4), (-8, 0), (-8, 4))
IM = ((0, 0), (0, 4), (8, 0), (0, 4), (0, 0),
      (0, -4), (-8, 0), (0, -4))


def _z(mode):
    return tuple((RE[j], IM[j]) for j in mode)


def _real_inner(a, b):
    return qadd(qmul(a[0], b[0]), qmul(a[1], b[1]))


def _feature(vector):
    A = qsum(_real_inner(v, v) for v in vector)
    total = (qsum(v[0] for v in vector), qsum(v[1] for v in vector))
    return A, qsub(_real_inner(total, total), A)


@lru_cache(None)
def full_scalar_edges():
    """Exact Q(sqrt2) feature groups for ALL 4096*2 directed edges.

    Grouping only sums identical scalar terms.  Energies are declared equal
    solely when both exact (A,C) feature pairs agree, never by a tolerance.
    Reversing an edge preserves its contribution and is grouped explicitly.
    """
    modes = tuple(itertools.product(range(8), repeat=4))
    zs = {k: _z(k) for k in modes}
    features = {k: _feature(zs[k]) for k in modes}
    slopes = {}
    for k, z in zs.items():
        slopes[k] = (qadd(_real_inner(z[2], z[0]),
                          _real_inner(z[2], z[1])),
                     _real_inner(z[2], z[3]))
    groups = Counter()
    for k in modes:
        for sign in (-1, 1):
            l = tuple((k[i]+sign*Q[i]) % 8 for i in range(4))
            delta = tuple((qsub(zs[l][i][0], zs[k][i][0]),
                           qsub(zs[l][i][1], zs[k][i][1])) for i in range(4))
            common = (_real_inner(zs[k][2], zs[k][2]), _feature(delta))
            left, right = (features[k], slopes[k]), (features[l], slopes[l])
            groups[(min(left, right), max(left, right), common)] += 1
    return tuple(groups.items())


def _decimal_box(center, radius):
    with localcontext() as ctx:
        ctx.prec = 90
        return [str(Decimal(center)-Decimal(radius)),
                str(Decimal(center)+Decimal(radius))]


def full_hessian_interval(root_data, digits=60):
    """Outward evaluation on the OWNED v8 root box, without finding a root.

    kappa=-B^(2n-1)/Z+128 beta z B^(2n-1)/(1-z+zB^(2n)).
    At the root, the entire direct Y contraction vanishes by the ten metric
    equations.  Delta Z'=0 because this wave has no diagonal Fourier block.
    Hence S''=16 sum_edges kappa^[1] c_kl - gamma/4, with
    c_kl=||u_l-u_k||^2 ||V_k||^2/4+b_k b_l and
    b_k=Re(u_k* V_k), V_k=z2(k) Jv2.  The factor 16 and Z_full=16 sumB^(2n)
    are essential; the reference factor 128 remains in kappa.
    """
    iv = mp.iv
    previous_digits = iv.dps
    iv.dps = digits
    try:
        d = iv.mpf(_decimal_box(root_data["root_center"][0], root_data["root_radius"]))
        o = iv.mpf(_decimal_box(root_data["root_center"][1], root_data["root_radius"]))
        sqrt2 = iv.sqrt(2)
        p = (iv.sqrt(5)-1)/2
        alpha, beta, fugacity = p*p/ROUNDS, 2*p*p, iv.mpf(1)/2**20
        cross = iv.sqrt((d-o)*(d+3*o))
        rotated_norm = (3*d-o+cross)/4
        slope_B, slope_C = (cross-(d-o))/4, ((d-o)+cross)/2
        qcache = {}

        def qiv(value):
            if value not in qcache:
                qcache[value] = value[0]+value[1]*sqrt2
            return qcache[value]

        def energy(feature):
            return d*qiv(feature[0])+o*qiv(feature[1])

        counts = Counter(_feature(_z(k)) for k in itertools.product(range(8), repeat=4))
        require(sum(counts.values()) == 4096, "complete_thermal_mode_count")
        energies = {f: energy(f) for f in counts}
        bs = {f: 1-alpha*energies[f] for f in counts}
        require(all(b.a > 0 for b in bs.values()), "positive_survival_on_root_box")
        powers = {f: bs[f]**(2*ROUNDS) for f in counts}
        Z = FOCK*sum(counts[f]*powers[f] for f in counts)
        heat, feedback, heat_prime, feedback_prime = {}, {}, {}, {}
        m = 2*ROUNDS-1
        for f in counts:
            b, e = bs[f], powers[f]
            h = 1-fugacity+fugacity*e
            heat[f] = -e/(Z*b)
            feedback[f] = REFERENCE*beta*fugacity*e/(h*b)
            heat_prime[f] = m*alpha*e/(Z*b*b)
            feedback_prime[f] = (REFERENCE*beta*fugacity*alpha*e/(h*b*b)
                                  *(-m+2*ROUNDS*fugacity*e/h))
        thermal_H, thermal_J = iv.mpf(0), iv.mpf(0)
        equal_edges, nonzero_edges = 0, 0
        groups = full_scalar_edges()
        require(sum(mult for _, mult in groups) == 8192, "complete_directed_edge_count")
        for (left, right, common), multiplicity in groups:
            fk, sk = left
            fl, sl = right
            vfactor, wfeature = common
            norm_V = qiv(vfactor)*rotated_norm
            norm_W = energy(wfeature)
            bk = slope_B*qiv(sk[0])+slope_C*qiv(sk[1])
            bl = slope_B*qiv(sl[0])+slope_C*qiv(sl[1])
            norm_X = norm_W*norm_V/4+bk*bl
            if fk == fl:
                dH, dJ = heat_prime[fk], feedback_prime[fk]
                equal_edges += multiplicity
            else:
                gap = energies[fl]-energies[fk]
                # Exact feature inequality must also have a signed interval.
                # This box satisfies it; a crossing is rejected, not divided.
                require(gap.a > 0 or gap.b < 0, "distinct_energy_gap_excludes_zero")
                dH = (heat[fl]-heat[fk])/gap
                dJ = (feedback[fl]-feedback[fk])/gap
                nonzero_edges += multiplicity
            thermal_H += FOCK*multiplicity*dH*norm_X
            thermal_J += FOCK*multiplicity*dJ*norm_X
        A = 128+64*sqrt2
        B = 2*A*(d+o)
        gamma = (128-64*sqrt2)*rotated_norm*(1+B/(B+256*o))/2
        matter = -gamma/4
        total = thermal_H+thermal_J+matter
        require(total.a > iv.mpf("0.089") and total.b < iv.mpf("0.091"),
                "strict_full_price_Hessian_positive_on_owned_root_box")
        return {"full_Hessian_interval": str(total),
                "certified_rational_enclosure": ["0.089", "0.091"],
                "heat_Hessian_interval": str(thermal_H),
                "feedback_Hessian_interval": str(thermal_J),
                "matter_Schur_interval": str(matter),
                "full_Z_interval": str(Z), "scalar_edge_groups": len(groups),
                "directed_edges": equal_edges+nonzero_edges,
                "exact_equal_energy_edges": equal_edges,
                "nonzero_energy_edges": nonzero_edges, "interval_digits": digits}
    finally:
        iv.dps = previous_digits


def run(repo=None):
    repo = ROOT if repo is None else Path(repo)
    checks = []

    def group(condition, label):
        require(condition, label)
        checks.append(label)

    receipt_path = repo/(V8+"receipt.json")
    group(hashlib.sha256(receipt_path.read_bytes()).hexdigest() == RECEIPT_SHA,
          "owned_v8_root_receipt_pin")
    root_data = json.loads(receipt_path.read_text())["interval"]
    group((root_data["L"], root_data["rounds"], root_data["Fock_dimension"],
           root_data["purifying_reference_dimension"], root_data["fugacity"])
          == (8, 8192, 16, 128, "2^-20"), "actual_v8_complete_program_parameters")
    source = Path(__file__).with_name("record_heat_continuation.py")
    spec = importlib.util.spec_from_file_location("stored_wave_native_definitions", source)
    owner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owner)
    basis, native_creator = owner._definitions(repo)
    phase = basis["basis_phase"]()
    creators = tuple(phase*native_creator(s.eye(4)[:, i])*phase for i in range(4))
    group(all(_zero(creators[i]*creators[j].H+creators[j].H*creators[i]
                    -int(i == j)*s.eye(16)) for i in range(4) for j in range(4)),
          "actual_native_all16_CAR_pairing")
    eta = s.diag(1, -1, -1, -1)
    # Definition-only consumption of the actual full exterior lift.  This
    # two-endpoint witness supports the general identity, not its universal
    # proof: hat A=Lx A Ly^-1 is orthogonal whenever A*hx A=hy.
    tree = ast.parse((repo/owner.JOINT).read_text())
    selected = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == "exterior"]
    require(len(selected) == 1, "actual_full_exterior_definition")
    scope = {"s": s, "P": SimpleNamespace(basis_phase=basis["basis_phase"])}
    exec(compile(ast.Module(body=selected, type_ignores=[]), owner.JOINT, "exec"), scope)
    exterior = scope["exterior"]
    Lx, Ly = s.eye(4), s.eye(4)
    for Lend, i in ((Lx, 1), (Ly, 2)):
        Lend[0, 0] = Lend[i, i] = s.Rational(5, 4)
        Lend[0, i] = Lend[i, 0] = -s.Rational(3, 4)
    O = s.eye(4)
    O[2, 2] = O[3, 3] = s.Rational(3, 5)
    O[2, 3], O[3, 2] = -s.Rational(4, 5), s.Rational(4, 5)
    hx, hy = Lx**2, Ly**2
    A = Lx.inv()*O*Ly
    nx, ny = Lx.inv()[:, 0], Ly.inv()[:, 0]
    u = s.Matrix([s.Rational(1, 7), s.Rational(2, 7),
                  s.Rational(1, 5), s.Rational(1, 6)])
    vx, vy = Lx.inv()*u, Ly.inv()*O.T*u
    Bx, By, UA = exterior(Lx), exterior(Ly), exterior(A)
    forward = native_creator(vx)*UA
    stored = native_creator(hy*vy).T*exterior(A.inv())
    group(_zero(Lx**2-(-eta+2*eta*nx*nx.T*eta))
          and _zero(Ly**2-(-eta+2*eta*ny*ny.T*eta))
          and _zero(A.T*eta*A-eta) and _zero(A.T*hx*A-hy)
          and _zero(A*ny-nx) and _zero(A*vy-vx)
          and _zero(Bx*UA*By.inv()-exterior(O))
          and _zero(exterior(O).T*exterior(O)-s.eye(16))
          and _zero(By*stored*Bx.inv()-(Bx*forward*By.inv()).T),
          "whole_stored_adjoint_class_positive_full16_similarity_bridge")
    x0, x1, x2, t = s.symbols("x0 x1 x2 t", real=True)
    phi = s.cos(2*s.pi*(3*x0+3*x1)/8)
    group(_zero(J23.T+J23) and _zero(J23.T*eta+eta*J23)
          and _zero(J23*s.eye(4)[:, 0]) and _zero(s.diff(phi, x2)),
          "exact_fixed_observer_identity_link_parallel_leg_conditions")
    a, b = s.Rational(1, 4), s.Rational(1, 125)
    F, G, _ = owner.shell_metric_family(a, b)
    d, o = G[0, 0], G[0, 1]
    v = F.row(2).T
    w, tt = J23*v, J23**2*v
    w2 = (w.T*w)[0]
    gamma = gamma_second(d, o, w2)
    family = native_row_family(F, t, phi, gamma)
    radial = gamma/(2*(128-64*s.sqrt(2))*d)
    group(_zero(family.subs(t, 0)-F)
          and _zero(s.diff(family, t).subs(t, 0).row(2).T-phi*w)
          and _zero(s.diff(family, t, 2).subs(t, 0).row(2).T-phi**2*tt-radial*v)
          and _zero((v.T*tt)[0]+w2), "actual_native_rotation_and_length_second_jets")
    c = tuple(sum((F[r, i]*creators[i] for i in range(4)), s.zeros(16))
              for r in range(4))
    Cw = sum((w[i]*creators[i] for i in range(4)), s.zeros(16))
    Ct = sum((tt[i]*creators[i] for i in range(4)), s.zeros(16))
    repaired, first_residuals, normalization, scalar_blocks = [], [], s.S.Zero, []
    lambda1 = 128-64*s.sqrt(2)
    for k in SHELL:
        bk = owner.mode_blocks(c, G, k)
        z2 = bk["z"][2]
        W = _matrix(z2*Cw+s.conjugate(z2)*Cw.H)
        T = _matrix(z2*Ct+s.conjugate(z2)*Ct.H)
        D1 = W/2
        Y = _matrix((bk["D"]*T+T*bk["D"])/2+W*W)
        schur = s.zeros(16)
        for sign in (-1, 1):
            l = owner.add_mode(k, Q, sign)
            bl = owner.mode_blocks(c, G, l)
            X = _matrix(bl["D"]*D1+D1*bk["D"])
            gap = s.expand(bl["energy"]-bk["energy"])
            norm_V = s.expand(z2*s.conjugate(z2)*w2)
            delta_D = _matrix(bl["D"]-bk["D"])
            norm_W = s.expand(s.trace(delta_D*delta_D)/16)
            scalar_blocks.append(_zero(X.H*X-norm_V*norm_W*s.eye(16)/4))
            schur += 2*X.H*X/gap
            eta_jet = -X/(s.sqrt(128)*gap)
            first_residuals.append(_zero(gap*eta_jet+X/s.sqrt(128)))
            normalization += s.trace(X.H*X)/(128*gap**2)
        E2 = _matrix(Y-schur)
        active = k[2] in (1, 7)
        repaired.append(_zero(E2+(gamma if active else 0)*s.eye(16)))
        correction = _matrix(2*radial*s.re((bk["z"].H*G[:, 2])[0]*z2)*s.eye(16))
        repaired.append(_zero(E2+correction))
        scalar_blocks.append(_zero(Y))
    group(all(scalar_blocks), "all128_shell_full16_X_square_scalar_and_Y_zero")
    group(all(first_residuals) and normalization != 0,
          "nonzero_normalized_full_shell_offshell_matter_first_response")
    group(all(repaired), "homogeneous_native_length_acceleration_repairs_all128_matter_second_rows")
    group(d > o > 0 and w2 > 0 and gamma > 0,
          "strict_gamma_positive_nontrivial_native_wave")
    # One nonoccupied block tests the scalar reduction used on ALL thermal edges.
    k = (1, 2, 3, 4)
    l = owner.add_mode(k, Q)
    bk, bl = owner.mode_blocks(c, G, k), owner.mode_blocks(c, G, l)
    V = bk["z"][2]*w
    Vgamma = sum((V[i]*creators[i]+s.conjugate(V[i])*creators[i].H
                  for i in range(4)), s.zeros(16))
    X = _matrix((bl["D"]*Vgamma+Vgamma*bk["D"])/2)
    u, ul = F.T*bk["z"], F.T*bl["z"]
    norm_V = s.expand((V.H*V)[0])
    norm_W = s.expand(((ul-u).H*(ul-u))[0])
    bs0 = s.expand(s.re((u.H*V)[0]))
    bs1 = s.expand(s.re((ul.H*V)[0]))
    group(_zero(X.H*X-(norm_W*norm_V/4+bs0*bs1)*s.eye(16)),
          "nonoccupied_full16_block_validates_complete_scalar_edge_formula")
    group(Q[2] == 0 and Q != (0, 0, 0, 0)
          and all(owner.add_mode(k, Q, sign) not in SHELL
                  for k in SHELL for sign in (-1, 1)),
          "no_diagonal_first_jet_full_heat_normalizer_first_derivative_zero")
    interval = full_hessian_interval(root_data)
    group(interval["directed_edges"] == 8192,
          "all4096_thermal_modes_and_all8192_edges_retained")
    group(interval["certified_rational_enclosure"] == ["0.089", "0.091"],
          "actual_full_v8_Hessian_excludes_this_joint_critical_first_velocity")
    return {"exact_checks": len(checks), "checks": checks, **interval,
            "native_candidate": "n=e0, identity links; row2 rotates in spatial23 with wave(3,3,0,0)",
            "matter_second_jet": "all128 rows repaired by homogeneous leg2 length acceleration",
            "whole_class_bridge": "For exact stored-adjoint links A*hx A=hy and parallel legs, I_x=exterior(sqrt(hx)) gives unitary returns and Dstored'=d'+d'^dagger; the literal bounded v8 instrument applies conditionally to this entire class",
            "full_price_conclusion": "no C2 joint critical curve with this first velocity and zero first link jets",
            "scope": "same v8 price, native stored-adjoint wave; not a no-go for other curved roots or joint link velocities"}
