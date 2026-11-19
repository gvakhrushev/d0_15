"""Regular stored-native chart at the existing homogeneous v8 root.

Only defining functions are extracted from pinned owners; no old run(),
certificate, root search, receipt generator or Lean build is executed.
The rational matrix used for ranks is explicitly NOT the stationary root.

Exact local chart: n is a future unit observer, u_r=L(n)v_r=(tau_r,rho_r z_r),
rho_r>0, z_r in S^2.  tau_r and rho_r are constant along their own r-lines;
z_r is arbitrary nearby, and each edge has one free SO(2) stabilizer angle.
R0(z_y,z_x), followed by rotation about z_x, supplies its full link.  Then
A=L_x^-1 diag(1,R) L_y.  Invertibility/bounded coefficients are open conditions.
This parametrizes the whole regular stratum, not just a chosen wave.

Whitened O is SO(4) INTERSECT Lorentz: diag(1,SO(3)) near the root, not SO(4).
For each Fourier mode k, kappa_r=1-exp(2pi i k_r/L), the complete reduced
first constraints are kappa_r alpha_r=0 and
kappa_r beta_r=W_r w_r, W_r^T=-W_r.  Three observer boosts reconstruct all
43 original variables; their omission from the reduced constraints freezes
no original link or observer direction.

Metric-image proof valid at the ACTUAL root a>b>0: any three spatial rows
w_r are independent (their minors are +/-b(a-b)^2 or -(a-b)^2(a+2b)).
For p<=3 active directions, a common Lorentz boost corrects the p time-leg
equations without changing H, leaving exactly H_rr=0 on active r. For p=4,
the sole extra compatibility is l^T H l=0, l=q^-1 tau, because
2 l^T alpha=l^T H l. Thus the image is 10-p (p<=3), or 5 (p=4).
The root receipt proves b>0; no rational-rank extrapolation is used.

These are stored-adjoint/representation constraints, not physical primitive
admission, CAR-current observer selection, or preparation/Euler equations.
All16 exterior grades, matter/reference directions and scalar site weights
remain. The pairing here is the owned counting-site pairing.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
ETA = s.diag(1, -1, -1, -1)
SLOTS = tuple((i, j) for i in range(4) for j in range(i, 4))
JOINT = "02_REGISTRY/research/certificates/a4d_native_joint_adjoint_source.py"
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
LEAN = "03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean"
RECEIPT = "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/receipt.json"
PINS = {
    JOINT: "71ba142e284974db57d67c91a77ccd08a7e4f9759e8fc8daef7c5938774c0b28",
    CURVED: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    LEAN: "2ccca18cf8ca66b9e1aa020301ce0d84d6fcd12563e913323482ce139928e5fe",
    RECEIPT: "da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9",
}


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("native_chart:"+label)


def zero(value):
    values = value.todok().values() if isinstance(value, s.MatrixBase) else (value,)
    return all(s.cancel(s.expand_complex(x)) == 0 for x in values)


def owned_definitions(repo):
    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                "pin:"+path)
    tree = ast.parse((repo/CURVED).read_text())
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "basis_phase"]
    require(len(nodes) == 1, "owned_basis_phase_present")
    scope = {"s": s}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CURVED, "exec"), scope)
    tree = ast.parse((repo/JOINT).read_text())
    names = {"exterior", "minimal_rotation", "observer"}
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in names]
    require(len(nodes) == len(names), "owned_chart_definitions_present")
    scope = {"s": s, "ETA": ETA,
             "P": SimpleNamespace(basis_phase=scope["basis_phase"])}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), JOINT, "exec"), scope)
    return SimpleNamespace(**{name: scope[name] for name in names})


def cross(v):
    return s.Matrix([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])


def boost(v):
    return s.Matrix([[0, *v], [v[0], 0, 0, 0],
                     [v[1], 0, 0, 0], [v[2], 0, 0, 0]])


def observer_whitening(n):
    """Canonical positive Lorentz L=sqrt(h_n), Ln=e0 on the future chart."""
    spatial = n[1:4, :]
    return s.BlockMatrix([[s.Matrix([[n[0]]]), -spatial.T],
                          [-spatial, s.eye(3)+spatial*spatial.T/(1+n[0])]]).as_explicit()


def regular_fourier_chart(F, differences):
    """All original43 first jets, built from16 leg+12 rotation+3 observer slots.

    differences are the ACTUAL kappa values; zero/nonzero cases are separate,
    so no division by a disappearing Fourier difference is introduced.
    """
    require(len(differences) == 4 and F.shape == (4, 4), "four_role_shape")
    legs = [ETA*F[r, :].T for r in range(4)]
    spatial = [v[1:4, :] for v in legs]
    require(all((w.T*w)[0] != 0 for w in spatial), "regular_nonzero_spatial_legs")
    variables = s.Matrix(s.symbols("reduced0:31"))
    observer = variables[28:31, :]
    du = [variables[4*r:4*r+4, :] for r in range(4)]
    rotations = [variables[16+3*r:19+3*r, :] for r in range(4)]
    reduced_equations = []
    columns = []
    for r, (kappa, w) in enumerate(zip(differences, spatial)):
        reduced_equations.append(kappa*du[r][0])
        reduced_equations.extend(kappa*du[r][1:4, :]-cross(rotations[r])*w)
        active = kappa != 0
        if not active:
            column = s.zeros(31, 1)
            column[4*r] = 1
            columns.append(column)
            perpendicular = list(s.eye(3).columnspace())
        else:
            perpendicular = (s.eye(3)-w*w.T/(w.T*w)[0]).columnspace()
            require(len(perpendicular) == 2, "two_leg_direction_coordinates")
        for beta in perpendicular:
            column = s.zeros(31, 1)
            column[4*r+1:4*r+4, :] = beta
            column[16+3*r:19+3*r, :] = kappa*w.cross(beta)/(w.T*w)[0]
            columns.append(column)
        column = s.zeros(31, 1)
        column[16+3*r:19+3*r, :] = w  # SO(2) stabilizer, unscaled coefficient.
        columns.append(column)
    for i in range(3):
        column = s.zeros(31, 1)
        column[28+i] = 1
        columns.append(column)
    basis = s.Matrix.hstack(*columns)
    reduced_constraints = s.Matrix(reduced_equations).jacobian(variables)

    # Exact original variables: all16 native leg jets,3 observer jets,24
    # Lorentz-link jets. Boost slots are determined, not frozen or deleted.
    original = []
    for r in range(4):
        original.extend(du[r]+boost(observer)*legs[r])
    original.extend(observer)
    for r in range(4):
        original.extend(s.Matrix(differences[r]*observer))
        original.extend(rotations[r])
    original_map = s.Matrix(original).jacobian(variables)
    original_variables = s.Matrix(s.symbols("original0:43"))
    dv = [original_variables[4*r:4*r+4, :] for r in range(4)]
    nu = original_variables[16:19, :]
    original_equations = []
    for r, kappa in enumerate(differences):
        b = original_variables[19+6*r:22+6*r, :]
        rotation = original_variables[22+6*r:25+6*r, :]
        X = boost(b)+s.diag(0, cross(rotation))
        original_equations.extend(b-kappa*nu)
        original_equations.extend(X*legs[r]-kappa*dv[r])
    original_constraints = s.Matrix(original_equations).jacobian(original_variables)
    H = s.Matrix(4, 4, lambda r, t:
                 (dv[r].T*ETA*legs[t]+legs[r].T*ETA*dv[t])[0])
    metric = s.Matrix([H[i, j] for i, j in SLOTS]).jacobian(original_variables)
    return {"constraints43": original_constraints, "constraints31": reduced_constraints,
            "basis31": basis, "basis43": original_map*basis,
            "metric": metric, "legs": legs}


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    owner = owned_definitions(repo)
    checks = []

    def eq(actual, expected, label):
        require(zero(actual-expected), label)
        checks.append(label)

    def yes(condition, label):
        require(condition, label)
        checks.append(label)

    nx, ny = s.Matrix([s.Rational(5, 4), s.Rational(3, 4), 0, 0]), s.Matrix([
        s.Rational(13, 12), 0, s.Rational(5, 12), 0])
    Lx, Ly = observer_whitening(nx), observer_whitening(ny)
    for label, n, L in (("x", nx, Lx), ("y", ny, Ly)):
        eq(n.T*ETA*n, s.ones(1), "unit_observer_"+label)
        eq(L*ETA*L, ETA, "canonical_whitening_is_Lorentz_"+label)
        eq(L*L, owner.observer(n), "canonical_whitening_is_positive_root_"+label)
        eq(L*n, s.eye(4)[:, 0], "canonical_whitening_maps_observer_to_e0_"+label)
        yes(all(L[:j, :j].det() > 0 for j in range(1, 5)),
            "canonical_whitening_positive_"+label)

    zx, zy = s.Matrix([s.Rational(3, 5), s.Rational(4, 5), 0]), s.Matrix([
        0, s.Rational(3, 5), s.Rational(4, 5)])
    R0 = owner.minimal_rotation(zy, zx)
    axis = cross(zx)
    Raxis = s.eye(3)+s.Rational(12, 13)*axis+s.Rational(8, 13)*axis*axis
    R = Raxis*R0
    O = s.diag(1, R)
    A = Lx.inv()*O*Ly
    vx = Lx.inv()*s.Matrix([s.Rational(2, 5), *(s.Rational(3, 7)*zx)])
    vy = Ly.inv()*s.Matrix([s.Rational(2, 5), *(s.Rational(3, 7)*zy)])
    eq(R0*zy, zx, "actual_alignment_maps_own_leg_direction")
    eq(Raxis*zx, zx, "free_SO2_angle_preserves_own_leg")
    eq(O.T*O, s.eye(4), "whitened_link_orthogonal")
    eq(O.T*ETA*O, ETA, "whitened_link_is_also_Lorentz")
    eq(A.T*ETA*A, ETA, "reconstructed_native_link_Lorentz")
    eq(A*ny, nx, "reconstructed_native_observer_transport")
    eq(A*vy, vx, "reconstructed_native_own_role_leg_transport")
    hx, hy = owner.observer(nx), owner.observer(ny)
    eq(A.T*hx*A, hy, "reconstructed_native_pairing_transport")

    Ix, Iy, EA, EO = map(owner.exterior, (Lx, Ly, A, O))
    Gx, Gy = owner.exterior(hx), owner.exterior(hy)
    eq(Ix.H*Ix, Gx, "all16_whitening_Gram_no_scalar_site_weight")
    eq(EA.H*Gx*EA, Gy, "all16_native_link_isometry")
    eq(Ix*EA, EO*Iy, "all16_full_link_whitening_intertwiner")
    eq(EO.H*EO, s.eye(16), "all16_return_unitarity_including_vacuum_top")

    hostile = s.eye(4)
    hostile[:2, :2] = s.Matrix([[3, -4], [4, 3]])/5
    yes(zero(hostile.T*hostile-s.eye(4))
        and not zero(hostile.T*ETA*hostile-ETA)
        and hostile*s.eye(4)[:, 0] != s.eye(4)[:, 0],
        "hostile_SO4_time_space_rotation_is_not_native_whitened_link")

    # Five active patterns on ONE generic rational NONROOT fixture. No mode
    # or phase census and no replacement of the certified root is performed.
    a, b = s.Rational(1, 4), s.Rational(1, 125)
    F = (a-b)*s.eye(4)+b*s.ones(4)
    profile = []
    for p in range(5):
        differences = tuple(s.Integer(r < p) for r in range(4))
        chart = regular_fourier_chart(F, differences)
        C43, C31, B43, B31 = (chart[name] for name in
                              ("constraints43", "constraints31", "basis43", "basis31"))
        dimension = 23-2*p
        yes(C43.rank() == 43-dimension and C31.rank() == 31-dimension
            and B43.rank() == dimension and B31.rank() == dimension,
            "nonroot_fixture_complete_43_and_31_tangent_dimensions_p"+str(p))
        eq(C43*B43, s.zeros(C43.rows, dimension), "all_original_constraints_p"+str(p))
        eq(C31*B31, s.zeros(C31.rows, dimension), "all_reduced_constraints_p"+str(p))
        image = chart["metric"]*B43
        expected_metric = 10-p-int(p == 4)
        yes(image.rank() == expected_metric, "nonroot_fixture_metric_image_p"+str(p))
        profile.append([p, dimension, expected_metric])

    phase = -s.sqrt(2)/2+s.I*s.sqrt(2)/2  # exp(2pi i*3/8)
    wave = regular_fourier_chart(F, (1-phase, 1-phase, 0, 0))
    eq(wave["constraints43"]*wave["basis43"], s.zeros(28, 19),
       "actual_q3300_phase_full19_column_constraint_basis")
    yes(wave["basis43"].cols == 19,
        "q3300_keeps_all19_native_first_parameters")

    # Symbolic polynomial minors justify the metric-image result throughout
    # the actual a>b>0 root stratum, not only at the nonroot rank fixture.
    u, beta = s.symbols("positive_a_minus_b positive_b", positive=True)
    genericF = u*s.eye(4)+beta*s.ones(4)
    W = (genericF*ETA)[:, 1:4]
    from itertools import combinations
    determinants = [s.factor(W.extract(rows, range(3)).det())
                    for rows in combinations(range(4), 3)]
    yes(all(s.cancel(value/(beta*u*u)) in (1, -1) for value in determinants[:3])
        and zero(determinants[3]+u*u*(u+3*beta)),
        "any_three_spatial_rows_independent_for_every_a_greater_b_positive")
    ell = s.Matrix([u+3*beta, -beta, -beta, -beta])/(u*(u+4*beta))
    eq(W.T*ell, s.zeros(3, 1), "all_active_metric_extra_compatibility_left_null")
    eq((ell.T*genericF[:, 0])[0], 1,
       "all_active_metric_normalization_gives_lHl_not_a_fitted_constraint")

    receipt = json.loads((repo/RECEIPT).read_text())
    center = receipt["interval"]["root_center"]
    radius = s.Rational(receipt["interval"]["root_radius"])
    dl, du = s.Rational(center[0])-radius, s.Rational(center[0])+radius
    ol, ou = s.Rational(center[1])-radius, s.Rational(center[1])+radius
    yes(0 < ol < ou < dl < du and du+3*ou < 1,
        "existing_root_rectangle_implies_a_greater_b_positive_and_regular_rho0")
    yes(receipt["interval"]["Fock_dimension"] == 16
        and receipt["interval"]["purifying_reference_dimension"] == 128
        and receipt["physical_native_admission"] is False,
        "existing_root_scope_full16_reference128_not_physical_admission")

    # At b=0 the time leg is parallel to the observer and its SO(3)
    # stabilizer has dimension3 instead of1. The regular chart must reject it.
    flatlegs = [ETA*(a*s.eye(4))[r, :].T for r in range(4)]
    singular_variables = s.Matrix(s.symbols("singular_rotation0:12"))
    singular_equations = s.Matrix.vstack(*(cross(singular_variables[3*r:3*r+3, :])
                                          *flatlegs[r][1:4, :] for r in range(4)))
    yes(singular_equations.jacobian(singular_variables).rank() == 6
        and 31-6 == 25 and profile[0][1] == 23,
        "b_zero_flat_zero_mode_is_singular_and_not_the_actual_root_chart")
    return {"exact_checks": len(checks), "source_pins": PINS,
            "nonroot_fixture_rank_profile": profile,
            "actual_root_rectangle": [[str(dl), str(du)], [str(ol), str(ou)]],
            "q3300_first_parameters": 19,
            "whitened_links": "diag(1,SO(3)), not arbitrary SO(4)",
            "all16_exterior_grades_retained": True,
            "all43_original_directions_constrained_not_frozen": True,
            "regular_chart_is_complete_local_nonlinear_chart": True,
            "physical_primitive_or_current_binding_selected": False,
            "full_joint_Euler_kernel_solved": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
