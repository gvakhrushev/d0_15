"""Reusable value, first jet and mixed second jet of the published stored-adjoint chart.

The nonlinear map and its Fourier tangent are the regular chart already built
in SOURCE 33267713b2e6d3e78af7789547b00f50cdceb43d. This module does not
rederive that chart, does not count its parameters, and does not classify the
kernel of the full Euler operator.

N07 interface, all on the tied carrier (h, q, observer and legs are not
independent inputs):

- ``homogeneous_frame``, ``edge_value``, ``edge_inverse``
- ``tied_constraints``, ``fourier_c1_action``
- ``kernel_coordinate_names``, ``kernel_tangent``, ``read_kernel_coordinates``
- ``fourier_mixed_second``, ``curve_constraint_jet``
- ``homogeneous_frame_curve``, ``row_rotation_curve``, ``observer_boost_curve``,
  ``edge_angle_curve``, ``endpoint_alignment_curve``
- ``c2_polynomial_jet``, ``conformal_edge``, ``so4_time_space_tangent``,
  ``native_assembly``, ``receipt_root_box``, ``flat_formal_jet``
- ``GENERATING_CURVES``, ``C2_COMPATIBILITY``,
  ``INTEGRABILITY_OUTSIDE_GENERATING_FAMILIES`` (``OPEN``)

Affine shifts are accepted only as a separate spectator argument. They do not
enter ``A``, ``v``, ``h``, ``q`` or ``F``.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from types import SimpleNamespace

import sympy as s


SOURCE_COMMIT = "33267713b2e6d3e78af7789547b00f50cdceb43d"
HISTORICAL_COMMIT = "74e62cdc716e10883accba9d34ccf0e21d58eb65"
LATTICE = 8
ETA = s.diag(1, -1, -1, -1)
E0 = s.Matrix([1, 0, 0, 0])
ROOT_CENTER = (
    "0.063635191594344535042829697433316630182693569761541",
    "0.0040167350432317252873844519148251220686807163526359",
)
ROOT_RADIUS = "1e-12"
CONTENT_SHA256 = {
    "02_REGISTRY/research/A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md":
        "b50614d5871377f0f70c2cffc9912b999eb95e162fccfe8fb3ebea1cf992a2f2",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/native_chart_check.py":
        "1cb2bd82796634b414b76a5396b629c98c3679aee3ce7aa63dfc34647ab84b65",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/kernel_check.py":
        "7c1a651f2b2130f1dbc721f3de1e36f0319bed52a6fd8b9d9ae259f716fef1da",
    "02_REGISTRY/research/A4D_NATIVE_JOINT_ADJOINT_SOURCE.md":
        "19b5062c1af8281c219de5c0ef6b70d7790922201c8f3c71b4472a18345c404d",
    "02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md":
        "10d30839a5a6b3cf5762ba0b3d7b846b1965363554bd3a971fdb7e8f249908e5",
    "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/receipt.json":
        "da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9",
}
# exp(2 pi i k / 8) for k = 0..7. The carrier is the owned L=8 lattice.
_EIGHTH = (
    s.Integer(1),
    (1 + s.I) / s.sqrt(2),
    s.I,
    (-1 + s.I) / s.sqrt(2),
    -s.Integer(1),
    (-1 - s.I) / s.sqrt(2),
    -s.I,
    (1 - s.I) / s.sqrt(2),
)
PURE_FRAME_COORDINATES = tuple(f"edge_angle[{role}]" for role in range(4))
GENERATING_CURVES = (
    "homogeneous_frame_curve",
    "row_rotation_curve",
    "observer_boost_curve",
    "edge_angle_curve",
    "endpoint_alignment_curve",
)
# Formal kernel vectors outside GENERATING_CURVES. Not a solved extension.
INTEGRABILITY_OUTSIDE_GENERATING_FAMILIES = "OPEN"
C2_COMPATIBILITY = "DC(eta) + D2C(xi, xi) = 0"
C2_SOLVABILITY = "not claimed"


class ChartSingular(ValueError):
    """Regular-chart hypothesis failed: vanishing leg length, antipodal leg, or a return outside diag(1, SO(3))."""


class InadmissibleCoordinate(ValueError):
    """A line coordinate was supplied on a Fourier mode that moves along its own role."""


def is_zero(value) -> bool:
    if isinstance(value, s.MatrixBase):
        return all(is_zero(entry) for entry in value)
    expr = s.cancel(s.expand_complex(s.expand(value)))
    if expr == 0:
        return True
    return s.simplify(expr) == 0


def column(entries) -> s.Matrix:
    return s.Matrix(len(entries), 1, list(entries))


def cross(vector) -> s.Matrix:
    v = column(vector)
    return s.Matrix([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])


def boost(nu) -> s.Matrix:
    nu = column(nu)
    return s.Matrix([
        [0, nu[0], nu[1], nu[2]],
        [nu[0], 0, 0, 0],
        [nu[1], 0, 0, 0],
        [nu[2], 0, 0, 0],
    ])


def phase_factor(index: int) -> s.Expr:
    return _EIGHTH[int(index) % LATTICE]


def kappa_of(phase, role: int) -> s.Expr:
    return s.simplify(1 - phase_factor(phase[role]))


def conjugate_phase(phase) -> tuple:
    return tuple((-int(index)) % LATTICE for index in phase)


def observer_vector(spatial) -> s.Matrix:
    svec = column(spatial)
    n0 = s.sqrt(1 + (svec.T * svec)[0])
    return column((n0, svec[0], svec[1], svec[2]))


def observer_form(n) -> s.Matrix:
    climbed = ETA * n
    return -ETA + 2 * climbed * climbed.T


def whitening(n) -> s.Matrix:
    """Positive Lorentz square root of h(n) on the future chart. L n = e0."""
    spatial = n[1:4, :]
    return s.BlockMatrix([
        [s.Matrix([[n[0]]]), -spatial.T],
        [-spatial, s.eye(3) + spatial * spatial.T / (1 + n[0])],
    ]).as_explicit()


def dh_at_rest(dn) -> s.Matrix:
    """Differential of h(n) at n=e0. The time-component row is the unit constraint, not a frozen observer."""
    delta = dn[0]
    nu = dn[1:4, :]
    return s.Matrix([[4 * delta]]).row_join((-2 * nu).T).col_join(
        (-2 * nu).row_join(s.zeros(3)))


def minimal_rotation(source, target) -> s.Matrix:
    """Proper rotation sending a non-antipodal unit vector ``source`` to ``target``."""
    denom = s.simplify(1 + (source.T * target)[0])
    if denom == 0:
        raise ChartSingular("antipodal leg directions are outside the declared chart")
    generator = target * source.T - source * target.T
    return s.eye(3) + generator + generator * generator / denom


def so3_about(axis, theta) -> s.Matrix:
    generator = cross(axis)
    return s.eye(3) + s.sin(theta) * generator + (1 - s.cos(theta)) * generator * generator


def transverse_frame(spatial) -> tuple:
    """Basis of the plane orthogonal to a nonzero spatial leg. Not an orthonormal gauge claim."""
    vector = column(spatial)
    pivots = (column((1, 0, 0)), column((0, 1, 0)), column((0, 0, 1)))
    first = None
    for pivot in pivots:
        candidate = s.simplify(vector.cross(pivot))
        if not is_zero(candidate):
            first = candidate
            break
    if first is None:
        raise ChartSingular("spatial leg vanished; flat frame is not the regular chart")
    second = s.simplify(vector.cross(first))
    if is_zero(second):
        raise ChartSingular("transverse frame collapsed")
    return first, second


def _leg_record(leg) -> tuple:
    spatial = column((leg[1], leg[2], leg[3]))
    rho2 = s.simplify((spatial.T * spatial)[0])
    if rho2 == 0:
        raise ChartSingular("spatial leg vanished; flat frame is not the regular chart")
    rho = s.sqrt(rho2)
    return leg[0], rho, s.simplify(spatial / rho), spatial, rho2


@dataclass
class HomogeneousFrame:
    """Spatially constant regular frame F=(a-b)I+b 11^T, n=e0, A=I. Not a new root."""
    a: object
    b: object
    F: s.Matrix
    v: tuple
    tau: tuple
    rho: tuple
    z: tuple
    w: tuple
    rho2: tuple

    @property
    def car_diagonal(self):
        return s.simplify(self.a ** 2 + 3 * self.b ** 2)

    @property
    def car_offdiagonal(self):
        return s.simplify(2 * self.a * self.b + 2 * self.b ** 2)


def homogeneous_frame(a, b) -> HomogeneousFrame:
    matrix = (a - b) * s.eye(4) + b * s.ones(4)
    legs = tuple(ETA * matrix.row(role).T for role in range(4))
    records = tuple(_leg_record(leg) for leg in legs)
    return HomogeneousFrame(
        a, b, matrix, legs,
        tuple(item[0] for item in records),
        tuple(item[1] for item in records),
        tuple(item[2] for item in records),
        tuple(item[3] for item in records),
        tuple(item[4] for item in records),
    )


def flat_legs():
    """Singular control F=eta. The time leg is parallel to the observer, so rho_0=0."""
    matrix = s.eye(4)
    legs = tuple(ETA * matrix.row(role).T for role in range(4))
    return matrix, legs


def tied_constraints(n_x, n_y, f_x, f_y, link, role: int) -> dict:
    """Original stored-adjoint rows. h and v are computed from n and F; they are not extra slots."""
    h_x = observer_form(n_x)
    h_y = observer_form(n_y)
    v_x = ETA * f_x.row(role).T
    v_y = ETA * f_y.row(role).T
    return {
        "observer_unit_x": (n_x.T * ETA * n_x)[0] - 1,
        "observer_unit_y": (n_y.T * ETA * n_y)[0] - 1,
        "lorentz": link.T * ETA * link - ETA,
        "pairing": link.T * h_x * link - h_y,
        "own_leg": link * v_y - v_x,
        "length": (v_x.T * h_x * v_x)[0] - (v_y.T * h_y * v_y)[0],
    }


def edge_value(s_x, s_y, tau, rho, z_x, z_y, theta):
    """Chart value on one edge. Affine data are not an argument."""
    z_x, z_y = column(z_x), column(z_y)
    for label, direction in (("x", z_x), ("y", z_y)):
        if not is_zero((direction.T * direction)[0] - 1):
            raise ChartSingular(f"leg direction {label} is not a unit vector")
    if is_zero(rho):
        raise ChartSingular("spatial leg vanished; flat frame is not the regular chart")
    gap = s.simplify(1 + (z_x.T * z_y)[0])
    if gap == 0:
        raise ChartSingular("antipodal leg directions are outside the declared chart")
    n_x = observer_vector(s_x)
    n_y = observer_vector(s_y)
    left = whitening(n_x)
    right = whitening(n_y)
    rotation = s.simplify(so3_about(z_x, theta) * minimal_rotation(z_y, z_x))
    orthogonal = s.diag(1, rotation)
    link = left.inv() * orthogonal * right
    u_x = column((tau, *((rho * z_x)[i] for i in range(3))))
    u_y = column((tau, *((rho * z_y)[i] for i in range(3))))
    return SimpleNamespace(
        n_x=n_x, n_y=n_y, h_x=left * left, h_y=right * right,
        L_x=left, L_y=right, u_x=u_x, u_y=u_y,
        v_x=left.inv() * u_x, v_y=right.inv() * u_y,
        A=link, O=orthogonal, R=rotation, s_x=column(s_x), s_y=column(s_y),
        tau=tau, rho=rho, z_x=z_x, z_y=z_y, theta=theta,
    )


def edge_inverse(n_x, n_y, v_x, v_y, link):
    """Inverse of the declared chart on one regular edge. Raises ChartSingular off that chart."""
    for label, n in (("x", n_x), ("y", n_y)):
        if not is_zero((n.T * ETA * n)[0] - 1) or s.simplify(n[0]) == 0:
            raise ChartSingular(f"observer {label} is not on the future unit chart")
    left, right = whitening(n_x), whitening(n_y)
    u_x, u_y = left * v_x, right * v_y
    records = []
    for label, leg in (("x", u_x), ("y", u_y)):
        try:
            records.append(_leg_record(leg))
        except ChartSingular as exc:
            raise ChartSingular(f"endpoint {label}: {exc}") from exc
    tau_x, rho_x, z_x, _, _ = records[0]
    tau_y, rho_y, z_y, _, _ = records[1]
    if not is_zero(tau_x - tau_y) or not is_zero(s.simplify(rho_x ** 2 - rho_y ** 2)):
        raise ChartSingular("tau or rho is not constant along the owned role line")
    orthogonal = s.simplify(left * link * right.inv())
    if (not is_zero(orthogonal[0, 0] - 1) or not is_zero(orthogonal[0, 1:4])
            or not is_zero(orthogonal[1:4, 0])):
        raise ChartSingular("whitened return is not diag(1, spatial block)")
    rotation = s.simplify(orthogonal[1:4, 1:4])
    if not is_zero(rotation.T * rotation - s.eye(3)) or not is_zero(rotation.det() - 1):
        raise ChartSingular("whitened return is not real SO(3)")
    alignment = minimal_rotation(z_y, z_x)
    stabilizer = s.simplify(rotation * alignment.inv())
    if not is_zero(stabilizer * z_x - z_x):
        raise ChartSingular("link rotation does not fix the owned leg")
    first, _ = transverse_frame(z_x)
    axis = z_x.cross(first)
    cosine = s.simplify((first.dot(stabilizer * first)) / (first.dot(first)))
    sine = s.simplify((axis.dot(stabilizer * first)) / (axis.dot(axis)))
    return SimpleNamespace(
        s_x=column((n_x[1], n_x[2], n_x[3])),
        s_y=column((n_y[1], n_y[2], n_y[3])),
        tau=s.simplify(tau_x), rho=s.simplify(rho_x),
        z_x=z_x, z_y=z_y, sin_theta=sine, cos_theta=cosine, stabilizer=stabilizer,
    )


def kernel_coordinate_names(phase) -> tuple:
    """Named chart coordinates of one Fourier symbol.

    Line coordinates exist only when that role's lattice frequency vanishes.
    Pure-frame angles are the four ``edge_angle`` names and are not the whole list.
    """
    names = [f"observer_nu[{i}]" for i in range(3)]
    for role in range(4):
        names.append(f"edge_angle[{role}]")
        names.append(f"leg_transverse[{role}][0]")
        names.append(f"leg_transverse[{role}][1]")
        if int(phase[role]) % LATTICE == 0:
            names.append(f"line_alpha[{role}]")
            names.append(f"line_radial[{role}]")
    return tuple(names)


def _coordinate(coordinates, name, default=0):
    if name not in coordinates:
        return default
    return coordinates[name]


def _role_beta(frame: HomogeneousFrame, role: int, phase, coordinates):
    first, second = transverse_frame(frame.w[role])
    beta = (_coordinate(coordinates, f"leg_transverse[{role}][0]") * first
            + _coordinate(coordinates, f"leg_transverse[{role}][1]") * second)
    line = int(phase[role]) % LATTICE == 0
    alpha_name = f"line_alpha[{role}]"
    radial_name = f"line_radial[{role}]"
    if not line and (alpha_name in coordinates or radial_name in coordinates):
        raise InadmissibleCoordinate(
            f"{alpha_name} and {radial_name} are absent unless phase[{role}] ≡ 0 mod {LATTICE}")
    alpha = _coordinate(coordinates, alpha_name) if line else 0
    if line:
        beta = beta + _coordinate(coordinates, radial_name) * frame.w[role] / frame.rho[role]
    return alpha, beta


def kernel_tangent(frame: HomogeneousFrame, phase, coordinates) -> SimpleNamespace:
    """First jet of the published chart at the homogeneous rest frame, one Fourier mode.

    ``du`` is the whitened-leg amplitude. ``dv`` differs from it by the observer boost.
    """
    unknown = set(coordinates) - set(kernel_coordinate_names(phase))
    if unknown:
        raise InadmissibleCoordinate(f"not chart coordinates of this phase: {sorted(unknown)}")
    nu = column(tuple(_coordinate(coordinates, f"observer_nu[{i}]") for i in range(3)))
    dn = column((0, nu[0], nu[1], nu[2]))
    dv, du, dA = [], [], []
    for role in range(4):
        alpha, beta = _role_beta(frame, role, phase, coordinates)
        leg_u = column((alpha, beta[0], beta[1], beta[2]))
        theta = _coordinate(coordinates, f"edge_angle[{role}]")
        kap = kappa_of(phase, role)
        skew = kap * (beta * frame.w[role].T - frame.w[role] * beta.T) / frame.rho2[role]
        spatial = skew + theta * cross(frame.z[role])
        link = boost(kap * nu)
        link[1:4, 1:4] += spatial
        du.append(leg_u)
        dv.append(s.simplify(leg_u + boost(nu) * frame.v[role]))
        dA.append(s.simplify(link))
    dF = s.zeros(4)
    for role, leg in enumerate(dv):
        dF[role, :] = (ETA * leg).T
    dq = s.simplify(dF * ETA * frame.F.T + frame.F * ETA * dF.T)
    return SimpleNamespace(
        phase=tuple(phase), coordinates=dict(coordinates), dn=dn, du=tuple(du),
        dv=tuple(dv), dA=tuple(dA), dF=dF, dh=dh_at_rest(dn), dq=dq,
    )


def read_kernel_coordinates(frame: HomogeneousFrame, phase, tangent) -> dict:
    """Inverse of ``kernel_tangent`` on its coordinate domain."""
    nu = column((tangent.dn[1], tangent.dn[2], tangent.dn[3]))
    found = {f"observer_nu[{i}]": s.simplify(nu[i]) for i in range(3)}
    for role in range(4):
        leg_u = s.simplify(tangent.dv[role] - boost(nu) * frame.v[role])
        beta = column((leg_u[1], leg_u[2], leg_u[3]))
        first, second = transverse_frame(frame.w[role])
        basis = s.Matrix.hstack(first, second, frame.w[role] / frame.rho[role])
        coeff = s.simplify(basis.inv() * beta)
        found[f"leg_transverse[{role}][0]"] = coeff[0]
        found[f"leg_transverse[{role}][1]"] = coeff[1]
        if int(phase[role]) % LATTICE == 0:
            found[f"line_alpha[{role}]"] = s.simplify(leg_u[0])
            found[f"line_radial[{role}]"] = coeff[2]
        kap = kappa_of(phase, role)
        removed = tangent.dA[role] - boost(kap * nu)
        angle_map = removed[1:4, 1:4] - kap * (
            beta * frame.w[role].T - frame.w[role] * beta.T) / frame.rho2[role]
        probe = first
        axis = frame.z[role].cross(probe)
        found[f"edge_angle[{role}]"] = s.simplify(
            (axis.dot(angle_map * probe)) / (axis.dot(axis)))
    return found


@dataclass
class C1Residual:
    observer_unit: object
    lorentz: tuple
    pairing: tuple
    own_leg: tuple

    def nonzero_rows(self) -> tuple:
        names = []
        if not is_zero(self.observer_unit):
            names.append("observer_unit")
        for role in range(4):
            if not is_zero(self.lorentz[role]):
                names.append(f"lorentz[{role}]")
            if not is_zero(self.pairing[role]):
                names.append(f"pairing[{role}]")
            if not is_zero(self.own_leg[role]):
                names.append(f"own_leg[{role}]")
        return tuple(names)


def fourier_c1_action(frame: HomogeneousFrame, phase, tangent) -> C1Residual:
    """Site-decoupled Fourier symbol of the tied constraint rows at n=e0, A=I.

    Own-leg row ``r`` uses only leg ``r`` and link ``r``. Observer velocity enters
    through ``dh`` and is not set to zero.
    """
    dh = tangent.dh if getattr(tangent, "dh", None) is not None else dh_at_rest(tangent.dn)
    lorentz, pairing, own = [], [], []
    for role in range(4):
        link = tangent.dA[role]
        kap = kappa_of(phase, role)
        lorentz.append(link.T * ETA + ETA * link)
        pairing.append(link + link.T + kap * dh)
        own.append(link * frame.v[role] - kap * tangent.dv[role])
    return C1Residual((2 * tangent.dn[0]), tuple(lorentz), tuple(pairing), tuple(own))


def _mode_displacement(frame: HomogeneousFrame, phase, coordinates, character):
    nu = column(tuple(_coordinate(coordinates, f"observer_nu[{i}]") for i in range(3)))
    spatial = character * nu
    legs = []
    for role in range(4):
        alpha, beta = _role_beta(frame, role, phase, coordinates)
        legs.append((character * alpha, character * beta))
    return spatial, tuple(legs)


def _deformed_endpoint(frame: HomogeneousFrame, spatial, legs):
    n = observer_vector(spatial)
    left = whitening(n)
    rows = []
    us = []
    for role in range(4):
        alpha, beta = legs[role]
        vector = frame.w[role] + beta
        rho = s.sqrt((vector.T * vector)[0])
        direction = vector / rho
        u = column((frame.tau[role] + alpha, *((rho * direction)[i] for i in range(3))))
        us.append(u)
        rows.append((ETA * (left.inv() * u)).T)
    matrix = s.Matrix.vstack(*rows)
    return SimpleNamespace(n=n, L=left, h=left * left, u=tuple(us), F=matrix,
                           q=matrix * ETA * matrix.T)


def fourier_chart_fields(frame: HomogeneousFrame, role: int, terms):
    """Nonlinear chart fields of one edge along a sum of Fourier coordinate modes.

    ``terms`` is a sequence ``(parameter, phase, coordinates)``. The source site
    carries character 1 and the target site character ``exp(2 pi i phase[role]/8)``.
    """
    source_s = column((0, 0, 0))
    target_s = column((0, 0, 0))
    source_legs = [(0, column((0, 0, 0))) for _ in range(4)]
    target_legs = [(0, column((0, 0, 0))) for _ in range(4)]
    theta = 0
    for parameter, phase, coordinates in terms:
        omega = phase_factor(phase[role])
        spatial, legs = _mode_displacement(frame, phase, coordinates, 1)
        spatial_y, legs_y = _mode_displacement(frame, phase, coordinates, omega)
        source_s = source_s + parameter * spatial
        target_s = target_s + parameter * spatial_y
        source_legs = tuple(
            (source_legs[i][0] + parameter * legs[i][0],
             source_legs[i][1] + parameter * legs[i][1])
            for i in range(4))
        target_legs = tuple(
            (target_legs[i][0] + parameter * legs_y[i][0],
             target_legs[i][1] + parameter * legs_y[i][1])
            for i in range(4))
        theta = theta + parameter * _coordinate(coordinates, f"edge_angle[{role}]")
    source = _deformed_endpoint(frame, source_s, source_legs)
    target = _deformed_endpoint(frame, target_s, target_legs)
    w_x = column((source.u[role][1], source.u[role][2], source.u[role][3]))
    w_y = column((target.u[role][1], target.u[role][2], target.u[role][3]))
    z_x = w_x / s.sqrt((w_x.T * w_x)[0])
    z_y = w_y / s.sqrt((w_y.T * w_y)[0])
    rotation = so3_about(z_x, theta) * minimal_rotation(z_y, z_x)
    orthogonal = s.diag(1, rotation)
    link = source.L.inv() * orthogonal * target.L
    return SimpleNamespace(
        n_x=source.n, n_y=target.n, F_x=source.F, F_y=target.F, A=link,
        h_x=source.h, h_y=target.h, q_x=source.q, O=orthogonal,
        v_x=ETA * source.F.row(role).T, v_y=ETA * target.F.row(role).T,
        u_x=source.u[role], u_y=target.u[role],
    )


def _jet_namespace(fields, parameters, orders) -> dict:
    out = {}
    for name in ("A", "v_x", "v_y", "n_x", "n_y", "h_x", "h_y", "q_x", "F_x", "O", "u_x", "u_y"):
        value = getattr(fields, name)
        for parameter, order in zip(parameters, orders):
            value = s.diff(value, parameter, order)
        out[name] = value.subs({parameter: 0 for parameter in parameters})
    return out


def fourier_first_jet(frame: HomogeneousFrame, role: int, phase, coordinates) -> dict:
    """Derivative of the nonlinear chart family, one Fourier mode, one edge."""
    t = s.symbols("first_t")
    fields = fourier_chart_fields(frame, role, ((t, phase, coordinates),))
    return {name: value for name, value in _jet_namespace(fields, (t,), (1,)).items()}


def fourier_mixed_second(frame: HomogeneousFrame, role: int, left, right) -> dict:
    """Mixed ambient second jet at the source of edge ``role``.

    ``left`` and ``right`` are ``(phase, coordinates)``. Coordinate accelerations
    are not included: this is the bilinear second derivative of the chart map.
    Solvability of a later C2 equation is not decided here.
    """
    t, u = s.symbols("mixed_t mixed_u")
    phase_t, coords_t = left
    phase_u, coords_u = right
    fields = fourier_chart_fields(
        frame, role,
        ((t, phase_t, coords_t), (u, phase_u, coords_u)))
    return _jet_namespace(fields, (t, u), (1, 1))


def curve_constraint_jet(builder, role: int, order: int) -> dict:
    t = s.symbols("curve_t")
    data = builder(t)
    rows = tied_constraints(data.n_x, data.n_y, data.F_x, data.F_y, data.A, role)
    out = {}
    for key, value in rows.items():
        jet = value if order == 0 else s.diff(value, t, order)
        out[key] = jet.subs(t, 0)
    return out


def field_taylor(builder):
    t = s.symbols("curve_t")
    data = builder(t)
    base, velocity, acceleration = {}, {}, {}
    for name in ("n_x", "n_y", "F_x", "F_y", "A"):
        value = getattr(data, name)
        base[name] = value.subs(t, 0)
        velocity[name] = s.diff(value, t).subs(t, 0)
        acceleration[name] = s.diff(value, t, 2).subs(t, 0)
    return base, velocity, acceleration


def polynomial_edge(base, velocity, acceleration):
    """Ambient path base + t velocity + t^2/2 acceleration. Not claimed to be integrable."""
    def builder(t):
        fields = {
            name: base[name] + t * velocity[name] + (t ** 2) * acceleration[name] / 2
            for name in base
        }
        return SimpleNamespace(**fields)
    return builder


def c2_polynomial_jet(base, velocity, acceleration, role: int) -> dict:
    """Necessary C2 condition DC(acceleration)+D2C(velocity, velocity)=0, evaluated on one edge.

    The returned rows are that combination. Vanishing is necessary for a C2 curve
    with those jets. It is not claimed to be solvable for every formal velocity.
    """
    return curve_constraint_jet(polynomial_edge(base, velocity, acceleration), role, 2)


def _rest(n=None):
    return E0 if n is None else n


def homogeneous_frame_curve(a, b):
    """Spatially constant path F(t)=(a+t-b)I+b 11^T, n=e0, A=I. The original homogeneous curve."""
    def builder(t):
        matrix = ((a + t) - b) * s.eye(4) + b * s.ones(4)
        n = E0
        link = s.eye(4)
        return SimpleNamespace(n_x=n, n_y=n, F_x=matrix, F_y=matrix, A=link)
    return builder


def _rotation_23(alpha):
    generator = s.zeros(4)
    generator[2, 3], generator[3, 2] = -1, 1
    plane = s.diag(0, 0, 1, 1)
    return (s.eye(4) - plane) + s.cos(alpha) * plane + s.sin(alpha) * generator, generator


def row_rotation_curve(a, b, x, role: int, c=0):
    """Owned row-2 rotation, wave (3,3,0,0). ``c`` is the optional length acceleration, invisible to C1."""
    frame = homogeneous_frame(a, b)
    y = tuple(int(x[i]) + (1 if i == role else 0) for i in range(4))

    def at(t, site):
        phi = s.cos(s.pi * (3 * site[0] + 3 * site[1]) / 4)
        rotation, _ = _rotation_23(t * phi)
        scale = s.sqrt(1 + c * t ** 2)
        matrix = frame.F.copy()
        moved = scale * rotation * frame.v[2]
        matrix[2, :] = (ETA * moved).T
        return matrix

    def builder(t):
        return SimpleNamespace(
            n_x=E0, n_y=E0, F_x=at(t, x), F_y=at(t, y), A=s.eye(4))
    return builder


def observer_boost_curve(a, b):
    """Spatially constant future observer with whitened legs held fixed. Velocity is not frozen."""
    frame = homogeneous_frame(a, b)

    def builder(t):
        n = observer_vector((t, 0, 0))
        left = whitening(n)
        rows = [(ETA * (left.inv() * frame.v[role])).T for role in range(4)]
        matrix = s.Matrix.vstack(*rows)
        return SimpleNamespace(n_x=n, n_y=n, F_x=matrix, F_y=matrix, A=s.eye(4))
    return builder


def edge_angle_curve(a, b, role: int):
    """Pure-frame SO(2) about the owned leg. One generating curve, not the whole kernel."""
    frame = homogeneous_frame(a, b)

    def builder(t):
        link = s.diag(1, so3_about(frame.z[role], t))
        return SimpleNamespace(n_x=E0, n_y=E0, F_x=frame.F, F_y=frame.F, A=link)
    return builder


def endpoint_alignment_curve(a, b):
    """Move only the target of role 0 and let R0 follow. A generating chart curve, not a linear ambient path."""
    frame = homogeneous_frame(a, b)
    z = frame.z[0]
    xi = column((1, -1, 0)) / s.sqrt(2)

    def builder(t):
        raw = z + t * xi
        zy = raw / s.sqrt((raw.T * raw)[0])
        link = s.diag(1, minimal_rotation(zy, z))
        target = frame.F.copy()
        moved = column((frame.tau[0], *((frame.rho[0] * zy)[i] for i in range(3))))
        target[0, :] = (ETA * moved).T
        return SimpleNamespace(n_x=E0, n_y=E0, F_x=frame.F, F_y=target, A=link)
    return builder


def conformal_edge(a, b, x, role: int):
    """Forbidden scaling F -> exp(t phi/2) F, phi=cos(2 pi (3x0+3x1)/8), frozen links and observer."""
    frame = homogeneous_frame(a, b)
    y = tuple(int(x[i]) + (1 if i == role else 0) for i in range(4))

    def at(t, site):
        phi = s.cos(s.pi * (3 * site[0] + 3 * site[1]) / 4)
        return s.exp(t * phi / 2) * frame.F

    def builder(t):
        return SimpleNamespace(n_x=E0, n_y=E0, F_x=at(t, x), F_y=at(t, y), A=s.eye(4))
    return builder


def conformal_symbol(frame: HomogeneousFrame, phase=(3, 3, 0, 0)):
    """Fourier amplitude of the forbidden curve: hat(dv_r)=v_r/4 at both nonzero cosine modes."""
    dn = column((0, 0, 0, 0))
    dv = tuple(leg / 4 for leg in frame.v)
    dA = tuple(s.zeros(4) for _ in range(4))
    dF = frame.F / 4
    tangent = SimpleNamespace(
        dn=dn, dv=dv, dA=dA, dF=dF, dh=dh_at_rest(dn),
        dq=s.simplify(dF * ETA * frame.F.T + frame.F * ETA * dF.T))
    return tangent, fourier_c1_action(frame, phase, tangent)


def so4_time_space_tangent(frame: HomogeneousFrame, phase) -> tuple:
    """Inadmissible time-space rotation. It is skew for h=I and is not a Lorentz tangent."""
    generator = s.zeros(4)
    generator[0, 1], generator[1, 0] = -1, 1
    dn = column((0, 0, 0, 0))
    tangent = SimpleNamespace(
        dn=dn, dv=tuple(column((0, 0, 0, 0)) for _ in range(4)),
        dA=tuple(generator if role == 0 else s.zeros(4) for role in range(4)),
        dF=s.zeros(4), dh=dh_at_rest(dn), dq=s.zeros(4))
    finite = s.eye(4)
    finite[:2, :2] = s.Matrix([[3, -4], [4, 3]]) / 5
    return tangent, fourier_c1_action(frame, phase, tangent), finite


def flat_formal_jet():
    """Owner's homogeneous formal jet at the singular control F=eta, not at the regular root.

    C1 can hold here while the regular chart refuses the point. Integrability of this
    jet is the owner's holonomy obstruction; it is not reopened and not re-proved.
    """
    matrix, legs = flat_legs()
    generator = s.zeros(4)
    generator[1, 2], generator[2, 1] = 1, -1
    dn = column((0, 0, 0, 0))
    dv = (column((0, 1, 0, 0)),) + tuple(column((0, 0, 0, 0)) for _ in range(3))
    tangent = SimpleNamespace(
        dn=dn, dv=dv,
        dA=(generator,) + tuple(s.zeros(4) for _ in range(3)),
        dF=s.zeros(4), dh=dh_at_rest(dn), dq=s.zeros(4))
    residual_legs = []
    for role in range(4):
        link = tangent.dA[role]
        residual_legs.append(link * legs[role])  # kappa = 0 on the zero mode
    lorentz = tuple(link.T * ETA + ETA * link for link in tangent.dA)
    return SimpleNamespace(
        F=matrix, v=legs, tangent=tangent, own_leg=tuple(residual_legs), lorentz=lorentz,
        rho0_squared=(column((legs[0][1], legs[0][2], legs[0][3])).T
                      * column((legs[0][1], legs[0][2], legs[0][3])))[0],
    )


def native_assembly(frame: HomogeneousFrame, affine_shifts=None):
    """Stored image. ``affine_shifts`` is retained only so callers can see it is not read."""
    del affine_shifts
    q = s.simplify(frame.F * ETA * frame.F.T)
    return SimpleNamespace(
        F=frame.F, q=q, v=frame.v, h=s.eye(4), n=E0, A=s.eye(4),
        affine_source_row=column((0, 0, 0, 0)),
    )


def receipt_root_box() -> dict:
    """Pinned v8 rectangle. It sits in a>b>0; the rational fixture and F=eta do not replace it."""
    with localcontext() as ctx:
        ctx.prec = 80
        d = Decimal(ROOT_CENTER[0])
        o = Decimal(ROOT_CENTER[1])
        radius = Decimal(ROOT_RADIUS)
        dl, du = d - radius, d + radius
        ol, ou = o - radius, o + radius
        regular = ol > 0 and ou < dl and du + 3 * ou < 1
        b_gap = (dl + 3 * ol).sqrt() - (du - ol).sqrt()
    return {
        "lower_d": str(dl), "upper_d": str(du), "lower_o": str(ol), "upper_o": str(ou),
        "rectangle_in_regular_component": bool(regular),
        "rho0_gap_numerator": str(b_gap),
        "rho0_positive_on_rectangle": bool(b_gap > 0),
        "physical_native_admission": False,
        "singular_flat_control": "F=eta, rho_0=0, not this rectangle",
    }


def reality_partner(frame: HomogeneousFrame, phase, coordinates):
    partner = conjugate_phase(phase)
    conjugated = {name: s.conjugate(value) for name, value in coordinates.items()}
    return partner, kernel_tangent(frame, partner, conjugated)


def zero_symbol_tangent(frame: HomogeneousFrame, coordinates):
    return kernel_tangent(frame, (0, 0, 0, 0), coordinates)
