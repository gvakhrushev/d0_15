"""Golden comparator spliced with the owned role-cochain return.

The two owned primitives are
`D0.Representation.GoldenOrderInterferometer.gate` and
`D0.Geometry.cochainForwardShift`. Their composition is evaluated as a
term diagram on the literal site × 16-grade carrier, with the ACDB/ABCD
order sign, the grade complement, and both output ports retained.

This is not the v8 whitening intertwiner `I D I⁻¹`, and it does not
rebuild the creator conjugacy `orderSignMatrix * carAnnihilate * orderSignMatrix`.
Those stay consumed citations. No price and no dynamics are selected.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROBE_N = 1  # archiveFibers = N+2 = 3, so +step ≠ −step
L2_N = 0

# roleOrderIndex order A,B,C,D. Not the roleCode order.
A = (0, 0)
B = (1, 1)
C = (0, 1)
D = (1, 0)
ROLES = (A, B, C, D)
ROLE_NAME = {A: "A", B: "B", C: "C", D: "D"}


class MissingMorphism(Exception):
    def __init__(self, name: str, kind: str):
        self.morphism = name
        self.kind = kind
        super().__init__(f"{kind}:{name}")


def _reduce(raw: list[int]) -> tuple[int, int, int, int]:
    coeff = list(raw)
    while len(coeff) < 4:
        coeff.append(0)
    # a^4 = 1 - a^2, from a^2 = p and p^2 = 1 - p.
    for degree in range(len(coeff) - 1, 3, -1):
        high = coeff[degree]
        if high == 0:
            continue
        coeff[degree - 4] += high
        coeff[degree - 2] -= high
        coeff[degree] = 0
    return (coeff[0], coeff[1], coeff[2], coeff[3])


class Alg:
    """Element of Z[a]/(a^2 - p, p + p^2 - 1), stored as c0+c1 a+c2 a^2+c3 a^3."""

    __slots__ = ("c",)

    def __init__(self, c: tuple[int, int, int, int]):
        self.c = c

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Alg) and self.c == other.c

    def __hash__(self) -> int:
        return hash(self.c)

    def __repr__(self) -> str:
        return f"Alg{self.c}"

    def __add__(self, other: Alg) -> Alg:
        return Alg(tuple(x + y for x, y in zip(self.c, other.c)))  # type: ignore[return-value]

    def __sub__(self, other: Alg) -> Alg:
        return Alg(tuple(x - y for x, y in zip(self.c, other.c)))  # type: ignore[return-value]

    def __neg__(self) -> Alg:
        return Alg(tuple(-x for x in self.c))  # type: ignore[return-value]

    def __mul__(self, other: Alg) -> Alg:
        raw = [0] * 7
        for i, xi in enumerate(self.c):
            if xi == 0:
                continue
            for j, yj in enumerate(other.c):
                if yj:
                    raw[i + j] += xi * yj
        return Alg(_reduce(raw))


ZERO = Alg((0, 0, 0, 0))
ONE = Alg((1, 0, 0, 0))
GATE_A = Alg((0, 1, 0, 0))
P = Alg((0, 0, 1, 0))  # a^2 = p
AP = Alg((0, 0, 0, 1))  # a*p = a^3
NEG_ONE = Alg((-1, 0, 0, 0))


def alg_int(n: int) -> Alg:
    return Alg((n, 0, 0, 0))


Cochain = dict[tuple[tuple[int, int, int, int], tuple[int, int, int, int]], Alg]


def _keep(dest: Cochain, key, value: Alg) -> None:
    if value == ZERO:
        dest.pop(key, None)
    else:
        dest[key] = value


def add_cochain(left: Cochain, right: Cochain, scale: Alg = ONE) -> Cochain:
    out = dict(left)
    for key, value in right.items():
        term = scale * value
        _keep(out, key, out.get(key, ZERO) + term)
    return out


def scale_cochain(psi: Cochain, factor: Alg) -> Cochain:
    if factor == ZERO:
        return {}
    return {key: factor * value for key, value in psi.items() if factor * value != ZERO}


def sub_cochain(left: Cochain, right: Cochain) -> Cochain:
    return add_cochain(left, right, NEG_ONE)


def delta(site: tuple[int, int, int, int], grade: tuple[int, int, int, int]) -> Cochain:
    return {(site, grade): ONE}


def role_index(role: tuple[int, int]) -> int:
    return ROLES.index(role)


def role_order_index(role: tuple[int, int]) -> int:
    """`D0.Geometry.roleOrderIndex`: A,B,C,D → 0,1,2,3."""
    if role == A:
        return 0
    if role == B:
        return 1
    if role == C:
        return 2
    return 3


def role_code(role: tuple[int, int]) -> int:
    """`D0.Geometry.roleCode`: 2*r.1.val + r.2.val, so A,C,D,B → 0,1,2,3."""
    return 2 * role[0] + role[1]


def grades() -> tuple[tuple[int, int, int, int], ...]:
    out = []
    for mask in range(16):
        out.append(tuple((mask >> i) & 1 for i in range(4)))  # type: ignore[arg-type]
    return tuple(out)  # type: ignore[return-value]


def grade_bit(grade: tuple[int, int, int, int], role: tuple[int, int]) -> int:
    return grade[role_index(role)]


def published_order_phase(grade: tuple[int, int, int, int]) -> int:
    """Pin formula `orderPhaseInt`: (-1)^(s(B)*(s(C)+s(D)))."""
    exponent = grade_bit(grade, B) * (grade_bit(grade, C) + grade_bit(grade, D))
    return -1 if exponent % 2 else 1


def inversion_phase(grade: tuple[int, int, int, int]) -> int:
    """Parity of occupied pairs whose ABCD order and ACDB code order disagree."""
    inversions = 0
    for i, left in enumerate(ROLES):
        if grade_bit(grade, left) == 0:
            continue
        for right in ROLES[i + 1 :]:
            if grade_bit(grade, right) == 0:
                continue
            if role_order_index(left) < role_order_index(right) and role_code(right) < role_code(left):
                inversions += 1
    return -1 if inversions % 2 else 1


def phase_alg(grade: tuple[int, int, int, int]) -> Alg:
    return ONE if published_order_phase(grade) == 1 else NEG_ONE


def sign_bridge(psi: Cochain) -> Cochain:
    out: Cochain = {}
    for (site, grade), value in psi.items():
        _keep(out, (site, grade), phase_alg(grade) * value)
    return out


def fibers(n: int) -> int:
    """`archiveFibers n = n + 2`."""
    return n + 2


def sites(length: int) -> tuple[tuple[int, int, int, int], ...]:
    out = []
    for a in range(length):
        for b in range(length):
            for c in range(length):
                for d in range(length):
                    out.append((a, b, c, d))
    return tuple(out)


def basis(length: int):
    for site in sites(length):
        for grade in grades():
            yield site, grade


def move_site(site: tuple[int, int, int, int], role: tuple[int, int], step: int, length: int):
    slot = role_index(role)
    moved = list(site)
    moved[slot] = (moved[slot] + step) % length
    return tuple(moved)


def pull(psi: Cochain, role: tuple[int, int], step: int, length: int) -> Cochain:
    """Lean pullback `(T ψ)(x) = ψ(x + step·e_r)`.

    `cochainForwardShift` is this operator at step = +1. The value sitting at
    `x` is written to `x - step·e_r`.
    """
    out: Cochain = {}
    for (site, grade), value in psi.items():
        dest = (move_site(site, role, -step, length), grade)
        _keep(out, dest, out.get(dest, ZERO) + value)
    return out


def cochain_forward_shift(psi: Cochain, role: tuple[int, int], length: int) -> Cochain:
    return pull(psi, role, +1, length)


def cochain_multiply(field, psi: Cochain, length: int) -> Cochain:
    """`cochainMultiply`: `(M_m ψ)(x,S) = m(x) ψ(x,S)`."""
    out: Cochain = {}
    for (site, grade), value in psi.items():
        _keep(out, (site, grade), alg_int(field(site)) * value)
    return out


def pointwise_pull(psi: Cochain, role: tuple[int, int], step: int, length: int) -> Cochain:
    """Same pullback, read off the whole grid. Used to check the sparse push."""
    out: Cochain = {}
    index = {(site, grade): value for (site, grade), value in psi.items()}
    for site, grade in basis(length):
        value = index.get((move_site(site, role, step, length), grade), ZERO)
        if value != ZERO:
            out[(site, grade)] = value
    return out


def comparison_from_blank(apply_u, psi: Cochain) -> tuple[Cochain, Cochain]:
    """Term diagram of `Gᵀ diag(I,U) G` on the blank first port.

    Gate `G = [[a,-p],[p,a]]` acts by scalars. `U` is applied only on port 1.
    Returns the two retained output ports, not their effects.
    """
    after_gate_0 = scale_cochain(psi, GATE_A)
    after_gate_1 = scale_cochain(psi, P)
    controlled_0 = after_gate_0
    controlled_1 = scale_cochain(apply_u(psi), P)
    # Gᵀ = [[a,p],[-p,a]]
    port_0 = add_cochain(scale_cochain(controlled_0, GATE_A), scale_cochain(controlled_1, P))
    port_1 = add_cochain(
        scale_cochain(controlled_0, -P),
        scale_cochain(controlled_1, GATE_A),
    )
    return port_0, port_1


def scalar_return(factor: Alg):
    def apply(psi: Cochain) -> Cochain:
        return scale_cochain(psi, factor)

    return apply


def output_polynomial(sign: Alg) -> tuple[Alg, Alg]:
    """`GoldenOrderInterferometer.output_formula`: ![a^2 + s p^2, (s-1) a p]."""
    p2 = P * P
    return (P + sign * p2, (sign - ONE) * AP)


def shift_return(role: tuple[int, int], step: int, length: int):
    def apply(psi: Cochain) -> Cochain:
        return pull(psi, role, step, length)

    return apply


def record_of_delta(role, step, length, site, grade) -> tuple[Cochain, Cochain]:
    return comparison_from_blank(shift_return(role, step, length), delta(site, grade))


def conjugate_return(apply_u):
    """`S U S` on functions. `S` is the diagonal grade sign, and `S² = I`."""

    def apply(psi: Cochain) -> Cochain:
        return sign_bridge(apply_u(sign_bridge(psi)))

    return apply


def effect(apply_u, apply_adj, psi: Cochain) -> Cochain:
    """`(U - I)ᵀ (U - I) ψ`, with the adjoint supplied by the caller."""
    difference = sub_cochain(apply_u(psi), psi)
    return sub_cochain(apply_adj(difference), difference)


def quadratic_effects(apply_u, apply_adj, psi: Cochain) -> tuple[Cochain, Cochain]:
    k0, k1 = comparison_from_blank(apply_u, psi)
    # K0 = p I + p² U, so K0ᵀ = p I + p² Uᵀ.
    # K1 = a p (U - I), so K1ᵀ = a p (Uᵀ - I).
    def k0_adj(value: Cochain) -> Cochain:
        return add_cochain(scale_cochain(value, P), scale_cochain(apply_adj(value), P * P))

    def k1_adj(value: Cochain) -> Cochain:
        return scale_cochain(sub_cochain(apply_adj(value), value), AP)

    return k0_adj(k0), k1_adj(k1)


def supports(psi: Cochain):
    return set(psi)


def forget_grade(psi: Cochain) -> dict[tuple[int, int, int, int], Alg]:
    """Erasure of the 16-grade label. Coefficients on one site add."""
    out: dict[tuple[int, int, int, int], Alg] = {}
    for (site, _grade), value in psi.items():
        total = out.get(site, ZERO) + value
        if total == ZERO:
            out.pop(site, None)
        else:
            out[site] = total
    return out


def trivial_sign(psi: Cochain) -> Cochain:
    return dict(psi)


def shell_reference_index():
    """8 signed role axes × 16 grades. This index is not a state and not `pi0`."""
    return tuple((sign, role, grade) for sign in (1, -1) for role in ROLES for grade in grades())


def v8_select_words():
    """The 32 signed words of v8 RESULT §2. Duplicate `-beta` is part of that list.

    No Lean declaration sends one of these words to a cochain operator.
    """
    words = []
    for role in ROLES:
        words.append(("beta", ROLE_NAME[role], "T", +1))
        words.append(("zeta", ROLE_NAME[role], "T", +1))
        words.append(("beta", ROLE_NAME[role], "T_adj", +1))
        words.append(("zeta", ROLE_NAME[role], "T_adj", -1))
        words.append(("beta", ROLE_NAME[role], "I", -1))
        words.append(("beta", ROLE_NAME[role], "I", -1))
    words.extend(("one", None, "I", +1) for _ in range(4))
    words.extend(("one", None, "I", -1) for _ in range(4))
    return tuple(words)


def spatial_sites(length: int):
    """Sites of `SpatialRole = {r : Role // r ≠ A}`, coordinates (B,C,D)."""
    return tuple((b, c, d) for b in range(length) for c in range(length) for d in range(length))


def history_spatial_reading(tick: int, spatial: tuple[int, int, int]):
    """`historySpatialReading`: tick is `tickIndex`, spatial coordinate is kept, grade is not an input."""
    if tick < 0:
        raise ValueError("HistoryIndex is a natural number")
    return (tick, spatial)


def unpriced_history_packet(tick, spatial, grade, ports):
    """Product of the owned history reading with one retained golden record.

    The product does not evaluate H, J_program, or R.
    """
    return {
        "history": history_spatial_reading(tick, spatial),
        "grade": grade,
        "ports": ports,
        "price": None,
    }


def read_complete_price(_packet):
    raise MissingMorphism("MORPH_HISTORY_WINDOW_TO_COMPLETE_PRICE", "missing-engineering")


def coefficient_dilation_before_shift(*_args):
    raise MissingMorphism("MORPH_COEFF_DILATION_BEFORE_SHIFT", "missing-engineering")


def retained_select32(*_args):
    raise MissingMorphism("MORPH_RETAINED_SELECT32", "missing-engineering")


def pi0_to_shell_reference(*_args):
    raise MissingMorphism("MORPH_PI0_TO_SHELL_REFERENCE128", "missing-engineering")


def select_program(*_args):
    raise MissingMorphism("LAW_SELECT_V8_PROGRAM_AND_PRICE", "unproved-selection-law")


DECLARATIONS = (
    {
        "name": "D0.Representation.GoldenOrderInterferometer.gate",
        "file": "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean",
        "needle": "def gate (a p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ",
        "blob": "7b59090312c610e1e19f426d7ed8f4a982ebf296",
    },
    {
        "name": "D0.Representation.GoldenOrderInterferometer.controlledSign",
        "file": "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean",
        "needle": "def controlledSign (s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ",
        "blob": "7b59090312c610e1e19f426d7ed8f4a982ebf296",
    },
    {
        "name": "D0.Representation.GoldenOrderInterferometer.output",
        "file": "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean",
        "needle": "def output (a p s : ℝ) : Fin 2 → ℝ",
        "blob": "7b59090312c610e1e19f426d7ed8f4a982ebf296",
    },
    {
        "name": "D0.Representation.GoldenOrderInterferometer.output_formula",
        "file": "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean",
        "needle": "theorem output_formula (a p s : ℝ)",
        "blob": "7b59090312c610e1e19f426d7ed8f4a982ebf296",
    },
    {
        "name": "D0.primitiveRoot",
        "file": "03_FORMALIZATION/D0/Core/Phi.lean",
        "needle": "noncomputable def primitiveRoot : ℝ",
        "blob": "09d678ef8fbef7fd5b5ead6b854fda96ca07c813",
    },
    {
        "name": "D0.primitive_root_satisfies",
        "file": "03_FORMALIZATION/D0/Core/Phi.lean",
        "needle": "theorem primitive_root_satisfies : primitiveRoot + primitiveRoot^2 = 1",
        "blob": "09d678ef8fbef7fd5b5ead6b854fda96ca07c813",
    },
    {
        "name": "D0.Geometry.ArchiveCochainBasis",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveCubicalDifferential.lean",
        "needle": "abbrev ArchiveCochainBasis (N : ℕ) : Type :=",
        "blob": "ac5abb195286676382dfac48d9ec5737ef63dc3d",
    },
    {
        "name": "D0.Geometry.cochainForwardShift",
        "file": "03_FORMALIZATION/D0/Geometry/A4DDiscreteEnergyKernel.lean",
        "needle": "def cochainForwardShift (N : ℕ) (r : Role) (ψ : ArchiveCochain N)",
        "blob": "68acc7276031dd512e3dd4b03adff6dc82cd477b",
    },
    {
        "name": "D0.Geometry.cochainMultiply",
        "file": "03_FORMALIZATION/D0/Geometry/A4DDiscreteEnergyKernel.lean",
        "needle": "def cochainMultiply (N : ℕ) (m : ArchiveRolePhaseGroup N → ℝ)",
        "blob": "68acc7276031dd512e3dd4b03adff6dc82cd477b",
    },
    {
        "name": "D0.Geometry.ArchiveFockState",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean",
        "needle": "abbrev ArchiveFockState : Type := Role → Bool",
        "blob": "1acfaec4d7a41b50f50dd55cced7613b80852514",
    },
    {
        "name": "D0.Geometry.card_archive_fock_state",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean",
        "needle": "theorem card_archive_fock_state :",
        "blob": "1acfaec4d7a41b50f50dd55cced7613b80852514",
    },
    {
        "name": "D0.Geometry.roleOrderIndex",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean",
        "needle": "def roleOrderIndex (r : Role) : ℕ :=",
        "blob": "8ff68576d92ff67532733a0ca2646de9d50105e2",
    },
    {
        "name": "D0.Geometry.roleCode",
        "file": "03_FORMALIZATION/D0/Geometry/A4DRolePairMetricCarrier.lean",
        "needle": "def roleCode (r : Role) : Fin 4 :=",
        "blob": "1ad21724f68b2d2c951a847cf6a3e7549ceed22d",
    },
    {
        "name": "D0.Geometry.archiveExteriorCreator",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean",
        "needle": "def archiveExteriorCreator (v : RoleSpace)",
        "blob": "087afdd443ffc02701376e00728193c020da259d",
    },
    {
        "name": "D0.Geometry.archiveExteriorContraction",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean",
        "needle": "def archiveExteriorContraction (α : Module.Dual ℝ RoleSpace)",
        "blob": "087afdd443ffc02701376e00728193c020da259d",
    },
    {
        "name": "D0.Geometry.createAction",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveCubicalDifferential.lean",
        "needle": "def createAction (N : ℕ) (r : Role)",
        "blob": "ac5abb195286676382dfac48d9ec5737ef63dc3d",
    },
    {
        "name": "D0.Geometry.annihilateAction",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveCubicalCartan.lean",
        "needle": "def annihilateAction (N : ℕ) (r : Role)",
        "blob": "2b0d487d2493e3ebae25b79d475c57f4b8f44624",
    },
    {
        "name": "D0.Geometry.HistoryIndex",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveSpatialHistorySplit.lean",
        "needle": "abbrev HistoryIndex := ℕ",
        "blob": "e019851589ad7e750e183ff1098c24283a093d19",
    },
    {
        "name": "D0.Geometry.historySpatialReading",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveSpatialHistorySplit.lean",
        "needle": "def historySpatialReading (N : ℕ)",
        "blob": "e019851589ad7e750e183ff1098c24283a093d19",
    },
    {
        "name": "D0.Evolution.FeshbachSchurTimeDelayOwner.tickIndex",
        "file": "03_FORMALIZATION/D0/Evolution/FeshbachSchurTimeDelayOwner.lean",
        "needle": "def tickIndex (t : ArchivePathTerm) : Nat := t.k",
        "blob": "bf3699925e35a290e54536c47b5a916832deecfc",
    },
    {
        "name": "D0.Evolution.FeshbachSchurTimeDelayOwner.ArchivePathTerm",
        "file": "03_FORMALIZATION/D0/Evolution/FeshbachSchurTimeDelayOwner.lean",
        "needle": "structure ArchivePathTerm where",
        "blob": "bf3699925e35a290e54536c47b5a916832deecfc",
    },
    {
        "name": "D0.Foundation.VerifiabilityNecessity.VerificationProtocol.record",
        "file": "03_FORMALIZATION/D0/Foundation/VerifiabilityNecessity.lean",
        "needle": "record : State → Record",
        "blob": "f0dbfcf6e99a24346fa1d9407b4ed49cc784a2e1",
    },
    {
        "name": "D0.Geometry.LabelledPositiveFamily",
        "file": "03_FORMALIZATION/D0/Geometry/A4DLabelledPathHolonomyDescent.lean",
        "needle": "abbrev LabelledPositiveFamily (N : ℕ) (K V : Type*)",
        "blob": "a34ab5dfb7d75f0736e48cd4f47168a346b81dde",
    },
    {
        "name": "D0.Geometry.pi0",
        "file": "03_FORMALIZATION/D0/Geometry/Pi0DiscreteAngle.lean",
        "needle": "noncomputable def pi0 : ℝ := (6 / 5) * phi ^ 2",
        "blob": "be10e6470f8a1fcf2ed1d5ebab8f09d302453ba0",
    },
    {
        "name": "D0.A",
        "file": "03_FORMALIZATION/D0/Core/DyadABCD.lean",
        "needle": "def A : Role := (0, 0)",
        "blob": "a1d55541e869c1c549e9d629becd424d71816355",
    },
    {
        "name": "D0.Geometry.archiveFibers",
        "file": "03_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean",
        "needle": "def archiveFibers (n : Nat) : Nat := n + 2",
        "blob": "312f7483dfa95cba67676e8afbf6a94b175575d0",
    },
)

PIN_DECLARATIONS = (
    {
        "commit": "74e62cdc716e10883accba9d34ccf0e21d58eb65",
        "file": "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.lean",
        "blob": "48dea1af391a2169ec95980007a77e62e6360b53",
        "name": "D0.Research.CurvedSolderedHeat.orderPhaseInt",
        "needle": "def orderPhaseInt (s : ArchiveFockState) : ℤ :=",
        "consumed_not_rerun": "actual_real_order_conjugacy",
    },
    {
        "commit": "76a3210c322706132048131f02389633caf6711e",
        "file": "02_REGISTRY/research/certificates/a4d_moving_preparation_golden_interferometer.lean",
        "blob": "1dc68d2f6e488496be0a431d11c7404f9706ce26",
        "name": "D0.Research.MovingPreparationGoldenBridge.comparisonOutput",
        "needle": "def comparisonOutput (a p : ℝ) (U : Matrix ι ι ℝ)",
        "consumed_not_rerun": "nativeRoleFailureEffect_formula",
    },
)


def resolve_declarations(root: Path = ROOT):
    found = []
    for item in DECLARATIONS:
        path = root / item["file"]
        text = path.read_text(encoding="utf-8")
        line_no = None
        for number, line in enumerate(text.splitlines(), 1):
            if item["needle"] in line:
                line_no = number
                break
        if line_no is None:
            raise AssertionError(f"unresolved declaration {item['name']}")
        blob = subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{item['file']}"], cwd=root, text=True
        ).strip()
        if blob != item["blob"]:
            raise AssertionError(f"blob changed for {item['name']}: {blob}")
        found.append({**item, "line": line_no})
    return tuple(found)


def typed_gaps():
    return (
        {
            "family": "creator/contraction coefficient gates",
            "owners": (
                "D0.Geometry.archiveExteriorCreator",
                "D0.Geometry.archiveExteriorContraction",
                "D0.Geometry.createAction",
                "D0.Geometry.annihilateAction",
                "D0.Geometry.cochainMultiply",
                "D0.Geometry.cochainForwardShift",
            ),
            "input": "Role × (ArchiveRolePhaseGroup N → ℤ) with a nonconstant value",
            "output_if_admitted": "End(Fin 2 × ArchiveCochainBasis N) whose zero-qubit compression is multiply-then-shift",
            "completed_fragment": "cochainMultiply and cochainForwardShift do not commute, and neither order equals the integer sandwich",
            "missing_morphism": "MORPH_COEFF_DILATION_BEFORE_SHIFT",
            "kind": "missing-engineering",
        },
        {
            "family": "retained label/control operations",
            "owners": (
                "D0.Representation.GoldenOrderInterferometer.controlledSign",
                "D0.Geometry.LabelledPositiveFamily",
            ),
            "input": "Fin 32 word from the v8 six-per-role list plus four I and four -I",
            "output_if_admitted": "word index × ArchiveCochain, label retained",
            "completed_fragment": "the 32-word input type is finite; the golden splice retains only Fin 2 ports",
            "missing_morphism": "MORPH_RETAINED_SELECT32",
            "kind": "missing-engineering",
            "not_the_same_owner": "LabelledPositiveFamily is List ChainStep, not the 32-word register",
        },
        {
            "family": "full matter/reference preparation",
            "owners": (
                "D0.Geometry.ArchiveFockState",
                "D0.Geometry.card_archive_fock_state",
                "D0.Geometry.pi0",
            ),
            "input": "a record, not the scalar D0.Geometry.pi0",
            "output_if_admitted": "a state on {±} × Role × ArchiveFockState, cardinality 128",
            "completed_fragment": "the 128-index exists as a product; pi0 resolves as ℝ and does not inhabit it",
            "missing_morphism": "MORPH_PI0_TO_SHELL_REFERENCE128",
            "kind": "missing-engineering",
        },
        {
            "family": "history/window and complete-price reading",
            "owners": (
                "D0.Geometry.HistoryIndex",
                "D0.Geometry.historySpatialReading",
                "D0.Evolution.FeshbachSchurTimeDelayOwner.tickIndex",
                "D0.Foundation.VerifiabilityNecessity.VerificationProtocol.record",
            ),
            "input": "HistoryIndex × SpatialArchivePhaseGroup N × ArchiveFockState × two golden ports",
            "output_if_admitted": "a price triple; not selected here",
            "completed_fragment": "historySpatialReading keeps tick and spatial data and does not read the grade; the unpriced product stores the golden ports beside it",
            "missing_morphism": "MORPH_HISTORY_WINDOW_TO_COMPLETE_PRICE",
            "kind": "missing-engineering",
        },
    )


def algebra_relations() -> None:
    if not (P + P * P == ONE):
        raise AssertionError("p + p^2 = 1")
    if not (GATE_A * GATE_A == P):
        raise AssertionError("a^2 = p")
    # p^3 = p - p^2 = 2p - 1
    if not (P * P * P == Alg((-1, 0, 2, 0))):
        raise AssertionError("p^3 = 2p - 1")
    if not (AP * AP == P * P * P):
        raise AssertionError("(a p)^2 = p^3")
    if role_code(A) != 0 or role_code(C) != 1 or role_code(D) != 2 or role_code(B) != 3:
        raise AssertionError("roleCode is not ACDB")
    if [role_order_index(role) for role in ROLES] != [0, 1, 2, 3]:
        raise AssertionError("roleOrderIndex is not ABCD")
    negative = [grade for grade in grades() if published_order_phase(grade) == -1]
    if len(grades()) != 16 or len(negative) != 4:
        raise AssertionError("sign bridge must be nontrivial on exactly four of sixteen grades")
    for grade in grades():
        if published_order_phase(grade) != inversion_phase(grade):
            raise AssertionError(f"order phase disagrees with inversion parity at {grade}")
        if published_order_phase(grade) ** 2 != 1:
            raise AssertionError("phase is not a sign")


def scalar_gate_matches_owner() -> None:
    probe = delta((0, 0, 0, 0), (0, 0, 0, 0))
    for raw in (1, -1, 0, 3):
        sign = alg_int(raw)
        port0, port1 = comparison_from_blank(scalar_return(sign), probe)
        expected0, expected1 = output_polynomial(sign)
        if port0 != {( (0, 0, 0, 0), (0, 0, 0, 0) ): expected0}:
            raise AssertionError(f"port 0 disagrees with output_formula at s={raw}")
        if expected1 == ZERO:
            if port1:
                raise AssertionError(f"port 1 should be dark at s={raw}")
        elif port1 != {((0, 0, 0, 0), (0, 0, 0, 0)): expected1}:
            raise AssertionError(f"port 1 disagrees with output_formula at s={raw}")
    plus0, plus1 = output_polynomial(ONE)
    if plus0 != ONE or plus1 != ZERO:
        raise AssertionError("s=+1 does not return the blank port")
    minus0, minus1 = output_polynomial(NEG_ONE)
    if minus0 != P * P * P or minus1 != alg_int(-2) * AP:
        raise AssertionError("s=-1 does not match minus_path_output")


def _expected_shift_record(role, step, length, site, grade):
    image = move_site(site, role, -step, length)
    port0 = {
        (site, grade): P,
        (image, grade): P * P,
    }
    port1 = {
        (site, grade): -AP,
        (image, grade): AP,
    }
    return port0, port1


def full_basis_term_diagram(n: int = PROBE_N) -> int:
    length = fibers(n)
    checked = 0
    for role in ROLES:
        for site, grade in basis(length):
            got0, got1 = record_of_delta(role, +1, length, site, grade)
            exp0, exp1 = _expected_shift_record(role, +1, length, site, grade)
            if got0 != exp0 or got1 != exp1:
                raise AssertionError(f"term diagram failed at {role} {site} {grade}")
            sparse = cochain_forward_shift(delta(site, grade), role, length)
            dense = pointwise_pull(delta(site, grade), role, +1, length)
            if sparse != dense:
                raise AssertionError("sparse push disagrees with pointwise pullback")
            checked += 1
    if checked != 4 * (length ** 4) * 16:
        raise AssertionError(f"basis was not exhaustive: {checked}")
    return checked


def sign_and_complement(n: int = PROBE_N) -> int:
    length = fibers(n)
    checked = 0
    for role in ROLES:
        forward = shift_return(role, +1, length)
        conjugated = conjugate_return(forward)
        for site, grade in basis(length):
            psi = delta(site, grade)
            port0, port1 = comparison_from_blank(forward, psi)
            signed0, signed1 = comparison_from_blank(forward, sign_bridge(psi))
            if signed0 != sign_bridge(port0) or signed1 != sign_bridge(port1):
                raise AssertionError("sign bridge does not commute with the golden record")
            conj0, conj1 = comparison_from_blank(conjugated, psi)
            if conj0 != port0 or conj1 != port1:
                raise AssertionError("S U S is not the same return")
            phase = published_order_phase(grade)
            if phase == -1 and (trivial_sign(port0) == sign_bridge(port0)):
                raise AssertionError("trivial sign was accepted on a negative grade")
            allowed = {(site, grade), (move_site(site, role, -1, length), grade)}
            if supports(port0) | supports(port1) != allowed:
                raise AssertionError("record leaked out of the grade or the two-site plane")
            checked += 1
    return checked


def substitution_and_erasure(n: int = PROBE_N) -> dict:
    length = fibers(n)
    labels_rejected = 0
    effects_agree = 0
    grade_erasure_collisions = 0
    sign_erasure_rejected = 0
    for role in ROLES:
        forward = shift_return(role, +1, length)
        backward = shift_return(role, -1, length)
        forward_adj = backward
        backward_adj = forward
        for site, grade in basis(length):
            psi = delta(site, grade)
            f0, f1 = comparison_from_blank(forward, psi)
            b0, b1 = comparison_from_blank(backward, psi)
            if (f0, f1) == (b0, b1):
                raise AssertionError("L=3 forward and backward records coincided")
            labels_rejected += 1
            fe = effect(forward, forward_adj, psi)
            be = effect(backward, backward_adj, psi)
            if fe != be:
                raise AssertionError("orthogonal returns were expected to share the quadratic effect")
            effects_agree += 1
            fq = quadratic_effects(forward, forward_adj, psi)
            bq = quadratic_effects(backward, backward_adj, psi)
            if fq != bq:
                raise AssertionError("port effects distinguished an erasure that should be blind")
            total = add_cochain(fq[0], fq[1])
            if total != psi:
                raise AssertionError("sum of port effects is not the identity")
            other = grades()[(grades().index(grade) + 1) % 16]
            g0, g1 = comparison_from_blank(forward, delta(site, other))
            if forget_grade(f0) == forget_grade(g0) and forget_grade(f1) == forget_grade(g1):
                if (f0, f1) == (g0, g1):
                    raise AssertionError("distinct grades were already equal")
                grade_erasure_collisions += 1
            if published_order_phase(grade) == -1:
                if sign_bridge(f0) == trivial_sign(f0):
                    raise AssertionError("negative grade had a trivial sign")
                sign_erasure_rejected += 1
    # Same summed effect, different role labels.
    relabel_rejected = 0
    for site, grade in basis(length):
        psi = delta(site, grade)
        labelled = {}
        swapped = {}
        sum_effect = {}
        sum_swapped = {}
        swap = {A: B, B: A, C: C, D: D}
        for role in ROLES:
            labelled[role] = comparison_from_blank(shift_return(role, +1, length), psi)
            swapped[role] = comparison_from_blank(shift_return(swap[role], +1, length), psi)
            sum_effect = add_cochain(
                sum_effect, effect(shift_return(role, +1, length), shift_return(role, -1, length), psi)
            )
            sum_swapped = add_cochain(
                sum_swapped,
                effect(shift_return(swap[role], +1, length), shift_return(swap[role], -1, length), psi),
            )
        if sum_effect != sum_swapped:
            raise AssertionError("role relabel changed the summed effect")
        if labelled[A] == swapped[A]:
            raise AssertionError("role A record survived a swap with role B")
        relabel_rejected += 1
    if sign_erasure_rejected == 0 or grade_erasure_collisions == 0:
        raise AssertionError("erasure probe did not see a collision")
    return {
        "labels_rejected": labels_rejected,
        "effects_agree": effects_agree,
        "grade_erasure_collisions": grade_erasure_collisions,
        "sign_erasure_rejected": sign_erasure_rejected,
        "relabel_rejected": relabel_rejected,
        "basis": (length ** 4) * 16,
    }


def l2_involution_is_not_separating() -> None:
    length = fibers(L2_N)
    site = (0, 0, 0, 0)
    grade = (0, 0, 0, 0)
    forward = comparison_from_blank(shift_return(A, +1, length), delta(site, grade))
    backward = comparison_from_blank(shift_return(A, -1, length), delta(site, grade))
    if forward != backward:
        raise AssertionError("L=2 translation is not an involution")


def coefficient_orders_disagree() -> None:
    length = fibers(PROBE_N)
    source = (0, 0, 0, 0)
    image = (0, 2, 0, 0)  # forward pullback moves the peak by -e_B
    values = {source: 1, image: 4}

    def field(site):
        return values.get(site, 9)

    psi = delta(source, (0, 0, 0, 0))
    multiply_then_shift = cochain_forward_shift(cochain_multiply(field, psi, length), B, length)
    shift_then_multiply = cochain_multiply(field, cochain_forward_shift(psi, B, length), length)
    if multiply_then_shift == shift_then_multiply:
        raise AssertionError("nonconstant coefficient commuted with the shift")
    grade = (0, 0, 0, 0)
    if multiply_then_shift[(image, grade)] != alg_int(1):
        raise AssertionError("multiply-then-shift did not keep the source coefficient")
    if shift_then_multiply[(image, grade)] != alg_int(4):
        raise AssertionError("shift-then-multiply did not read the image coefficient")
    # The rejected symmetric sandwich sqrt(u(x)) T sqrt(u(x+e)) has coefficient
    # sqrt(u(image)) sqrt(u(source)) = 2 at that same peak. It is neither order.
    sandwich = 2
    if len({sandwich, 1, 4}) != 3:
        raise AssertionError("sandwich failed to separate from both orders")
    try:
        coefficient_dilation_before_shift(B, field)
    except MissingMorphism as exc:
        if exc.morphism != "MORPH_COEFF_DILATION_BEFORE_SHIFT" or exc.kind != "missing-engineering":
            raise
    else:
        raise AssertionError("coefficient dilation was treated as implemented")


def interface_refusals() -> None:
    words = v8_select_words()
    if len(words) != 32 or words.count(("beta", "A", "I", -1)) != 2:
        raise AssertionError("32-word list does not keep the duplicate -beta")
    if len(shell_reference_index()) != 128:
        raise AssertionError("reference index is not 128")
    try:
        retained_select32(words[0])
    except MissingMorphism as exc:
        if exc.kind != "missing-engineering":
            raise
    else:
        raise AssertionError("SELECT was treated as implemented")
    try:
        pi0_to_shell_reference(shell_reference_index()[0])
    except MissingMorphism as exc:
        if exc.morphism != "MORPH_PI0_TO_SHELL_REFERENCE128":
            raise
    else:
        raise AssertionError("pi0 was treated as a shell state")
    length = fibers(L2_N)
    for tick in (0, 1, 2):
        for spatial in spatial_sites(length):
            reading = history_spatial_reading(tick, spatial)
            if reading != (tick, spatial):
                raise AssertionError("history reading changed its tick or spatial coordinate")
    packet = unpriced_history_packet(
        1,
        (0, 0, 0),
        (1, 0, 0, 0),
        comparison_from_blank(shift_return(A, +1, fibers(PROBE_N)), delta((0, 0, 0, 0), (1, 0, 0, 0))),
    )
    if packet["price"] is not None or packet["history"][0] != 1 or packet["grade"] != (1, 0, 0, 0):
        raise AssertionError("unpriced packet dropped tick or grade")
    try:
        read_complete_price(packet)
    except MissingMorphism as exc:
        if exc.kind != "missing-engineering":
            raise
    else:
        raise AssertionError("complete price was selected")
    try:
        select_program(packet)
    except MissingMorphism as exc:
        if exc.kind != "unproved-selection-law":
            raise
    else:
        raise AssertionError("program selection was treated as proved")
    gaps = typed_gaps()
    if len(gaps) != 4:
        raise AssertionError("expected four typed gaps")
    names = {gap["missing_morphism"] for gap in gaps}
    if names != {
        "MORPH_COEFF_DILATION_BEFORE_SHIFT",
        "MORPH_RETAINED_SELECT32",
        "MORPH_PI0_TO_SHELL_REFERENCE128",
        "MORPH_HISTORY_WINDOW_TO_COMPLETE_PRICE",
    }:
        raise AssertionError(names)


def run_all(root: Path = ROOT) -> dict:
    algebra_relations()
    resolved = resolve_declarations(root)
    scalar_gate_matches_owner()
    basis_count = full_basis_term_diagram()
    sign_count = sign_and_complement()
    probe = substitution_and_erasure()
    l2_involution_is_not_separating()
    coefficient_orders_disagree()
    interface_refusals()
    return {
        "resolved_declarations": len(resolved),
        "full_basis_records": basis_count,
        "sign_bridge_records": sign_count,
        **probe,
    }


if __name__ == "__main__":
    result = run_all()
    for key in sorted(result):
        print(f"PASS {key}={result[key]}")
