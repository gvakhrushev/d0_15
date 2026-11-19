#!/usr/bin/env python3
"""Exact amplitude-jet norm budget on the complete native Fibonacci cost cut.

X=sum(v v*), W=sum(dv v*), Z=sum(dv dv*) are computational covariances,
not a replacement for the full coherent AF record. The original immutable
compact_step supplies X/Y. No entropy logarithm, numerical rank threshold,
physical Info law, or physical field-to-instrument map is introduced here.

C1 input means C1 Kraus amplitudes and a C1 purification L of FIXED width R
valid in a neighborhood. R need not equal rank(rho) at a rank-birth point.
Z measures the squared norm of the FIRST amplitude jet, not a second jet.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
OWNER_DIR = "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/"
ARCHIVE_SOURCE = "02_REGISTRY/research/sources/d0_native_archive_occupation_2026-10-15/archive_occupation.py"
SOURCE_PINS = {
    OWNER_DIR + "verify.py":
        "81a7b75b84ea23b8915eebaa054a08dbbc0573f0959a0c26661dcb775aeb4736",
    OWNER_DIR + "RESULT.md":
        "428bdda31e27ea6e7bf18ac93528fa4bc21c28677026341af2e86a36ac67ff52",
    OWNER_DIR + "receipt.json":
        "31ff9bd7d0547929bedea34e36beec680155ad1e7ac23e0ae8e879860edf5501",
    ARCHIVE_SOURCE:
        "0182e6ec3611ef61983c4380d613adc500a101beb532c75807955afd3435415b",
    "02_REGISTRY/research/A4D_NATIVE_AFCAR_MAX_GAIN_ACTION_BOUNDARY.md":
        "f1d629c3917dee2f1f1b59d3789da77000a9fb435be17cff437a55c8b0b439c3",
}


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def adj(M: s.MatrixBase) -> s.MatrixBase:
    return M.conjugate().T


def clean(M: s.MatrixBase) -> s.MatrixBase:
    return M.applyfunc(s.expand)


def vec(M: s.MatrixBase) -> s.Matrix:
    """Row-major vec, as in the pinned owner's K tensor I_R convention."""
    return s.Matrix(list(M))


@dataclass(frozen=True)
class BlockJet:
    X: s.MatrixBase
    W: s.MatrixBase
    Z: s.MatrixBase

    def __post_init__(self) -> None:
        if not all(isinstance(v, s.MatrixBase) for v in (self.X, self.W, self.Z)):
            raise TypeError("exact_SymPy_matrices_required")
        if self.X.rows != self.X.cols or self.W.shape != self.X.shape or self.Z.shape != self.X.shape:
            raise ValueError("same_square_covariance_shapes_required")

    @property
    def dX(self) -> s.MatrixBase:
        return clean(self.W + adj(self.W))


def _pin_sources(repo: Path) -> None:
    for path, expected in SOURCE_PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == expected,
                "source_pin:" + path)


@lru_cache(maxsize=4)
def _owner(repo: Path):
    _pin_sources(repo)
    spec = importlib.util.spec_from_file_location(
        "amplitude_jet_original_compact_owner", repo/(OWNER_DIR + "verify.py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("original_compact_definition_import_failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _feature(v: s.MatrixBase, dv: s.MatrixBase) -> BlockJet:
    return BlockJet(clean(v*adj(v)), clean(dv*adj(v)), clean(dv*adj(dv)))


def seed_jet(K0: s.MatrixBase, K1: s.MatrixBase, L: s.MatrixBase,
             dK0: s.MatrixBase, dK1: s.MatrixBase,
             dL: s.MatrixBase) -> tuple[BlockJet, BlockJet]:
    """Complete cost-cut N=0, including all preparation-amplitude derivatives."""
    if dL.shape != L.shape or K0.rows != K0.cols or K1.shape != K0.shape:
        raise ValueError("compatible_working_carrier_and_fixed_purification_width_required")
    if L.rows != K0.rows or dK0.shape != K0.shape or dK1.shape != K1.shape:
        raise ValueError("compatible_amplitude_tangents_required")
    return tuple(_feature(vec(K*L), vec(dK*L+K*dL))
                 for K, dK in ((K0, dK0), (K1, dK1)))


def advance(pair: tuple[BlockJet, BlockJet], K0: s.MatrixBase,
            K1: s.MatrixBase, dK0: s.MatrixBase, dK1: s.MatrixBase,
            repo: Path | None = None) -> tuple[BlockJet, BlockJet]:
    """One native COST level. Pending features are carried exactly once."""
    A, B = pair
    repo = ROOT if repo is None else Path(repo).resolve()
    if A.X.shape != B.X.shape or K0.rows != K0.cols or K1.shape != K0.shape:
        raise ValueError("same_fixed_working_carrier_required")
    if A.X.rows % K0.rows or dK0.shape != K0.shape or dK1.shape != K1.shape:
        raise ValueError("compatible_fixed_purification_width_required")
    R = A.X.rows//K0.rows
    B0, B1 = (s.kronecker_product(K, s.eye(R)) for K in (K0, K1))
    D0, D1 = (s.kronecker_product(K, s.eye(R)) for K in (dK0, dK1))
    # Consume the immutable owner's actual value recurrence; do not copy it.
    new_X, new_Y = _owner(repo).compact_step(A.X, B.X, K0, K1)

    def branch(Xnext, op, dop, carried: BlockJet | None) -> BlockJet:
        W = dop*A.X*adj(op) + op*A.W*adj(op)
        Z = (dop*A.X*adj(dop) + dop*adj(A.W)*adj(op)
             + op*A.W*adj(dop) + op*A.Z*adj(op))
        if carried is not None:
            W += carried.W
            Z += carried.Z
        return BlockJet(clean(Xnext), clean(W), clean(Z))

    return branch(new_X, B0, D0, B), branch(new_Y, B1, D1, None)


def norm_budget(pair: tuple[BlockJet, BlockJet]) -> dict[str, s.Expr]:
    """Squared norm of the raw and normalized FIRST feature tangent.

    Requires tau>0. The normalized budget includes any phase/purification
    gauge motion, so it is a valid norm bound rather than a gauge minimum.
    """
    tau = s.simplify(sum(s.trace(v.X) for v in pair))
    if tau == 0 or tau.is_nonpositive is True or tau.is_real is False:
        raise ValueError("positive_raw_feature_norm_required")
    overlap = s.simplify(sum(s.trace(v.W) for v in pair))
    dtau = s.simplify(overlap+s.conjugate(overlap))
    raw_energy = s.simplify(sum(s.trace(v.Z) for v in pair))
    energy = s.simplify(raw_energy/tau - dtau**2/(4*tau**2))
    return {"raw_norm": tau, "raw_norm_jet": dtau,
            "raw_jet_energy": raw_energy, "normalized_jet_energy": energy}


def normalize_jet(pair: tuple[BlockJet, BlockJet]) -> tuple[tuple[BlockJet, BlockJet], dict]:
    """Apply v/sqrt(tau), dv/sqrt(tau)-v*dtau/(2*tau^(3/2))."""
    budget = norm_budget(pair)
    tau, dtau = budget["raw_norm"], budget["raw_norm_jet"]
    alpha = dtau/(2*tau)
    normalized = tuple(BlockJet(
        clean(v.X/tau),
        clean((v.W-alpha*v.X)/tau),
        clean((v.Z-alpha*(v.W+adj(v.W))+alpha**2*v.X)/tau),
    ) for v in pair)
    return normalized, budget


def recorded_support_spectrum(level: int, p: s.Expr) -> dict:
    """Exact spectral data of the owned positive-state lift from A9.

    The analytic owner identity is h_N=hat_alpha(h_9)=p^(-10)P_N.
    Conjugation preserves ranks; each literal inclusion sends (rA,rB) to
    (rA+rB,rA), starting at (1,0). Thus ranks are (F_(k+1),F_k), k=N-9,
    and sigma_N has eigenvalues p^k,p^(k+1) on those support sectors.
    This is the defining-AF density, not the full-GNS heat operator trace.
    """
    if not isinstance(level, int) or level < 9:
        raise ValueError("recorded_state_level_at_least_nine_required")
    k = level-9
    rA, rB = 1, 0
    for _ in range(k):
        rA, rB = rA+rB, rA
    masses = (rA*p**k, rB*p**(k+1))
    return {"level": level, "depth": k, "support_ranks": (rA, rB),
            "eigenvalue_exponents": (k, k+1), "sector_masses": masses,
            "normalization": sum(masses),
            "cost": (level+1)*masses[0]+(level+2)*masses[1],
            "entropy_phi_units": k*masses[0]+(k+1)*masses[1]}


def run_checks(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    _pin_sources(repo)
    original = _owner(repo)

    def eq(actual, expected, name: str) -> None:
        delta = actual-expected
        values = list(delta) if isinstance(delta, s.MatrixBase) else [delta]
        require(all(s.simplify(v) == 0 for v in values), name)

    # The exact noncommuting d=2 fixture and its actual K/L tangents are copied
    # literally from the pinned owner's exact() definitions, not its test run.
    r, I = s.Rational, s.I
    K0 = s.diag(r(3, 5), r(5, 13))
    U = s.Matrix([[r(3, 5), I*r(4, 5)], [I*r(4, 5), r(3, 5)]])
    K1 = U*s.diag(r(4, 5), r(12, 13))
    L = s.diag(r(3, 5), r(4, 5))
    dK0 = I*s.Matrix([[1, 1], [1, 0]])*K0
    dK1 = I*s.Matrix([[0, -I], [I, 2]])*K1
    dL = I*s.Matrix([[0, 1], [1, 0]])*L
    eq(adj(K0)*K0+adj(K1)*K1, s.eye(2), "actual_complete_instrument")
    require(K0*K1 != K1*K0, "actual_instrument_noncommutes")
    eq(adj(dK0)*K0+adj(K0)*dK0+adj(dK1)*K1+adj(K1)*dK1,
       s.zeros(2), "actual_tangent_completeness")
    require(dL*adj(L)+L*adj(dL) != s.zeros(2), "actual_preparation_moves")

    def enumerate_block(words, dots, seed, dseed):
        vs = [vec(A*seed) for A in words]
        dvs = [vec(dA*seed+A*dseed) for A, dA in zip(words, dots)]
        return BlockJet(*(clean(sum((f(v, dv) for v, dv in zip(vs, dvs)), s.zeros(4)))
                          for f in (lambda v, dv: v*adj(v),
                                    lambda v, dv: dv*adj(v),
                                    lambda v, dv: dv*adj(dv))))

    pair = seed_jet(K0, K1, L, dK0, dK1, dL)
    # Same normalized state direction, represented with a moving raw norm.
    scale = r(2, 7)
    raw_pair = seed_jet(K0, K1, L, dK0, dK1, dL+scale*L)
    A, B, dA, dB = [K0], [K1], [dK0], [dK1]
    counts = []
    final_budget = None
    for N in range(5):
        counts.append([len(A), len(B)])
        words_pair = (enumerate_block(A, dA, L, dL), enumerate_block(B, dB, L, dL))
        raw_words = (enumerate_block(A, dA, L, dL+scale*L),
                     enumerate_block(B, dB, L, dL+scale*L))
        for tag, got, want in (("normalized", pair, words_pair), ("raw", raw_pair, raw_words)):
            for block, reference in zip(got, want):
                for name in ("X", "W", "Z"):
                    eq(getattr(block, name), getattr(reference, name), f"word_{tag}_{name}_{N}")
        normalized, budget = normalize_jet(raw_pair)
        for got, want in zip(normalized, pair):
            for name in ("X", "W", "Z"):
                eq(getattr(got, name), getattr(want, name), f"moving_normalizer_{name}_{N}")
        eq(sum(s.trace(v.dX) for v in pair), 0, f"complete_cut_trace_jet_zero_{N}")
        eq(sum(s.trace(v.dX) for v in normalized), 0, f"normalized_raw_trace_jet_zero_{N}")
        eq(budget["raw_norm"], 1, f"complete_cut_raw_norm_{N}")
        eq(budget["raw_norm_jet"], 2*scale, f"moving_raw_norm_jet_{N}")
        eq(sum(s.trace(v.Z) for v in normalized), budget["normalized_jet_energy"],
           f"normalized_energy_trace_{N}")
        eq(budget["raw_jet_energy"]-budget["normalized_jet_energy"], scale**2,
           f"moving_norm_energy_correction_{N}")
        final_budget = budget
        if N < 4:
            pair = advance(pair, K0, K1, dK0, dK1, repo)
            raw_pair = advance(raw_pair, K0, K1, dK0, dK1, repo)
            A1 = [K0*T for T in A]+B
            B1 = [K1*T for T in A]
            dA1 = [dK0*T+K0*dT for T, dT in zip(A, dA)]+dB
            dB1 = [dK1*T+K1*dT for T, dT in zip(A, dA)]
            A, B, dA, dB = A1, B1, dA1, dB1
    require(counts == [[1, 1], [2, 1], [3, 2], [5, 3], [8, 5]], "actual_native_cost_cuts")

    # Hostile controls act on this new capsule only, not immutable owners.
    initial = seed_jet(K0, K1, L, dK0, dK1, dL)
    frozen_L = seed_jet(K0, K1, L, dK0, dK1, s.zeros(2))
    frozen_K = seed_jet(K0, K1, L, s.zeros(2), s.zeros(2), dL)
    require(any(g.W != w.W for g, w in zip(initial, frozen_L)), "reject_frozen_L")
    require(any(g.W != w.W for g, w in zip(initial, frozen_K)), "reject_frozen_K")
    following = advance(initial, K0, K1, dK0, dK1, repo)
    B0 = s.kronecker_product(K0, s.eye(2))
    D0 = s.kronecker_product(dK0, s.eye(2))
    wrong_pending = clean(D0*initial[0].X*adj(B0)+B0*initial[0].W*adj(B0)
                          +B0*initial[1].W*adj(B0))
    require(following[0].W != wrong_pending, "reject_reexecuted_pending_jet")
    missing_cross = clean(D0*initial[0].X*adj(D0)+B0*initial[0].Z*adj(B0)+initial[1].Z)
    require(following[0].Z != missing_cross, "reject_missing_Z_cross_terms")
    require(final_budget["raw_jet_energy"] != final_budget["normalized_jet_energy"],
            "reject_frozen_normalizer")
    try:
        zero = BlockJet(s.zeros(4), s.zeros(4), s.zeros(4))
        normalize_jet((zero, zero))
    except ValueError:
        pass
    else:
        raise AssertionError("zero_normalizer_not_rejected")

    # Normalization removes the REAL radial derivative, not the phase jet.
    # Replacing (Re Tr W)^2 by |Tr W|^2 would incorrectly erase this budget.
    phase = seed_jet(K0, K1, L, s.zeros(2), s.zeros(2), I*L)
    phase_normalized, phase_budget = normalize_jet(phase)
    eq(phase_budget["raw_norm"], 1, "pure_phase_raw_norm")
    eq(phase_budget["raw_norm_jet"], 0, "pure_phase_norm_jet_zero")
    eq(phase_budget["normalized_jet_energy"], 1, "pure_phase_amplitude_budget_retained")
    for block in phase_normalized:
        eq(block.W, I*block.X, "pure_phase_W_is_iX")
        eq(block.Z, block.X, "pure_phase_Z_is_X")
        eq(block.dX, s.zeros(4), "pure_phase_each_sector_density_jet_zero")
    phase_overlap = sum(s.trace(v.W) for v in phase)
    wrong_phase_budget = (sum(s.trace(v.Z) for v in phase)
                          - phase_overlap*s.conjugate(phase_overlap))
    eq(wrong_phase_budget, 0, "wrong_modulus_overlap_erases_phase_budget")
    require(wrong_phase_budget != phase_budget["normalized_jet_energy"],
            "reject_modulus_instead_of_real_overlap")

    # C1 fixed-width rank-birth example: L(t)=diag(1,t), rho(t) normalized.
    # Its base density jet is zero, but the amplitude jet energy is one.
    Lbirth, dLbirth = s.diag(1, 0), s.diag(0, 1)
    birth = seed_jet(K0, K1, Lbirth, s.zeros(2), s.zeros(2), dLbirth)
    for _ in range(3):
        birth = advance(birth, K0, K1, s.zeros(2), s.zeros(2), repo)
    birth_normalized, birth_budget = normalize_jet(birth)
    eq(birth_budget["normalized_jet_energy"], 1, "C1_rank_birth_jet_energy_retained")
    eq(birth_budget["raw_norm_jet"], 0, "C1_rank_birth_norm_first_jet")
    require(any(v.W != s.zeros(4) for v in birth_normalized), "C1_birth_amplitude_not_frozen")
    # Ready words at N=3, built independently of the covariance recurrence.
    Aw, Bw = [K0], [K1]
    for _ in range(3):
        Aw, Bw = [K0*T for T in Aw]+Bw, [K1*T for T in Aw]
    def history_gram(words, seed):
        return s.Matrix(len(words), len(words), lambda i, j:
                        s.trace(words[i]*seed*adj(seed)*adj(words[j])))
    gram0, gram1 = history_gram(Aw, Lbirth), history_gram(Aw, s.eye(2))
    require((gram0.rank(), gram1.rank()) == (2, 4), "actual_ready_rank_birth_two_to_four")
    eq(dLbirth*adj(Lbirth)+Lbirth*adj(dLbirth), s.zeros(2), "birth_density_first_jet_zero")
    # gram(t)=gram0+t^2*(gram1-gram0), a PSD sum. Its rank is four for every
    # t!=0, while all newborn eigenvalues are O(t^2); no log threshold is used.

    # Concrete consumer: the ACTUAL recorded defining-AF state at A9, distinct
    # from the full-GNS archive density/operator trace. Only reconstruct its
    # source definitions; never call the archive capsule's run_checks().
    archive_spec = importlib.util.spec_from_file_location(
        "amplitude_actual_recorded_archive_definitions", repo/ARCHIVE_SOURCE)
    if archive_spec is None or archive_spec.loader is None:
        raise RuntimeError("actual_archive_definition_import_failed")
    archive = importlib.util.module_from_spec(archive_spec)
    sys.modules[archive_spec.name] = archive
    archive_spec.loader.exec_module(archive)
    actual = archive.recorded_archive(repo)
    AF, y, p = actual["AF"], actual["y"], actual["p"]
    require(y.shape == (89, 1) and AF.counts(9) == (89, 55), "actual_A9_defining_blocks")
    norm_y = AF.red((adj(y)*y)[0])
    require(norm_y == 1, "actual_A9_recorded_y_normalized")
    L_B = s.zeros(55, 1)
    require(AF.zero(L_B), "actual_A9_B_sector_zero")
    # sigma_A=y y*. Its complete projector defect factors as
    # y*(y*y-1)*y*. Certify the middle factor and its action, avoiding 144^2
    # (and even 89^2) arrays. This is a normalized rank-one projector.
    require(AF.red(norm_y-1) == 0 and AF.zero(y*(norm_y-1)), "actual_A9_sigma_projector")
    require(AF.red(89*p**10+55*p**11-1) == 0, "actual_A9_fixed_PF_reference_normalized")
    expected_cost = AF.red(10*norm_y+11*(adj(L_B)*L_B)[0])
    require(expected_cost == 10, "actual_A9_central_cost_ten")
    centered_cost_L = ((10-expected_cost)*y, (11-expected_cost)*L_B)
    require(all(AF.zero(v) for v in centered_cost_L), "actual_A9_centered_cost_kills_L")
    # log(sigma) acts by log(1)=0 on its support; a new C1 amplitude direction
    # in its kernel contributes only O(t^2 log|t|). Hence BOTH Info contracts'
    # normalized first-source feature coefficients vanish at this state.
    log_on_L = (s.log(norm_y)*y, L_B)
    require(all(AF.zero(v) for v in log_on_L), "actual_A9_entropy_first_source_coefficient_zero")
    require(all(AF.zero(c+v) and AF.zero(-v)
                for c, v in zip(centered_cost_L, log_on_L)),
            "actual_A9_both_Info_action_first_source_coefficients_zero")

    # Finite checks bind INDEXING to the analytic all-N transport identity;
    # they are not an extrapolation proof. Each sigma/mu ratio on support is
    # p^(-10), so log(sigma)-log(mu)=10 log(phi) on the entire support.
    support_rows = []
    for N in range(9, 13):
        spectrum = recorded_support_spectrum(N, p)
        k = spectrum["depth"]
        rA, rB = spectrum["support_ranks"]
        exponents = spectrum["eigenvalue_exponents"]
        require((exponents[0]-(N+1), exponents[1]-(N+2)) == (-10, -10),
                "transported_likelihood_common_support_exponent")
        require(AF.red(spectrum["normalization"]-1) == 0,
                "transported_state_Fibonacci_spectral_normalization")
        require(AF.red(spectrum["cost"]-spectrum["entropy_phi_units"]-10) == 0,
                "transported_old_contract_relative_entropy_ten")
        require((N+1-k-10, N+2-(k+1)-10) == (0, 0),
                "transported_old_contract_centered_source_coefficients_zero")
        support_rows.append({"level": N, "support_ranks": [rA, rB],
                             "eigenvalue_exponents": list(exponents),
                             "old_relative_entropy_phi_units": "10"})
    require([v["support_ranks"] for v in support_rows] == [[1, 0], [1, 1], [2, 1], [3, 2]],
            "actual_transported_support_Fibonacci_indexing")

    # Actual A10 has one support eigenvector in EACH sector. The fine germ
    # masses (p-t,p^2+t) is positive on a real neighborhood, admits a C1
    # square-root purification, and changes sector masses. It is therefore
    # outside the zero-source conclusion restricted to transported seed germs.
    # Work with exact log eigenvalues (-g,-2g), rather than numerical logs.
    g = s.Symbol("log_phi", positive=True)
    dmass = (-s.S.One, s.S.One)
    log_eigenvalues = (-g, -2*g)
    fine_entropy_jet = s.simplify(-sum(dm*le for dm, le in zip(dmass, log_eigenvalues))/g)
    fine_cost_jet = 11*dmass[0]+12*dmass[1]
    require(sum(dmass) == 0 and fine_entropy_jet == 1 and fine_cost_jet == 1,
            "actual_A10_fine_mass_germ_entropy_and_cost_jets_one")
    require(fine_cost_jet-fine_entropy_jet == 0,
            "actual_A10_old_relative_entropy_fine_first_source_zero")
    require(fine_entropy_jet != 0,
            "reject_gain_entropy_zero_for_all_fine_preparation_germs")

    require(original.CHECKS == [], "original_owner_suite_not_executed")
    _pin_sources(repo)
    return {
        "status": "PASS_AMPLITUDE_SOURCE_REGULARITY",
        "fixture": {"working_dimension": 2, "purification_width": 2,
                    "compact_matrix_size": 4, "cost_levels": [0, 1, 2, 3, 4],
                    "ready_pending_counts": counts},
        "N4_raw_norm_jet": str(final_budget["raw_norm_jet"]),
        "N4_normalized_jet_energy": str(final_budget["normalized_jet_energy"]),
        "pure_phase_normalized_jet_energy": str(phase_budget["normalized_jet_energy"]),
        "rank_birth": {"ready_level": 3, "base_rank": 2, "nearby_rank": 4,
                       "seed_base_rank": 1, "seed_nearby_rank": 2,
                       "normalized_jet_energy": str(birth_budget["normalized_jet_energy"])},
        "actual_recorded_A9": {
            "state": "sigma=y y* in M89, zero in M55; defining AF density",
            "mu": "p^10 I89 (+) p^11 I55", "cost": "10 I89 (+) 11 I55",
            "norm": str(norm_y), "entropy": "0", "expected_cost": str(expected_cost),
            "entropy_Info_action_value": "10", "complete_max_gain_Info_action_value": "0",
            "both_preparation_first_sources": "0",
            "structural_inputs_for_C1_corollary": True,
            "scope": "all C1 fixed-width amplitude preparation germs through this state; fixed mu and cost",
            "full_GNS_heat_or_metric_link_operator_variation_covered": False,
        },
        "actual_positive_state_refinement": {
            "analytic_all_N_input": "h_N=hat_alpha(h9)=p^(-10)P_N; N>=9",
            "support_ranks": "(F_(k+1),F_k), k=N-9",
            "support_eigenvalues": "p^k and p^(k+1), with those multiplicities",
            "finite_index_checks": support_rows,
            "all_N_old_relative_entropy_phi_units": "10",
            "all_N_old_action_C1_fine_preparation_first_source": "0",
            "all_N_gain_entropy_first_source_zero_on_transported_seed_germs": True,
            "gain_entropy_zero_for_all_fine_preparation_germs": False,
            "A10_fine_mass_germ": {"masses": "(p-t,p^2+t)", "d_entropy_phi": "1",
                                   "d_cost": "1", "d_old_action": "0", "d_gain_action": "1"},
            "all_N_scope_basis": "analytic transport and C1 amplitude corollary, not finite-fixture extrapolation",
            "fixed_reference_and_cost_only": True,
        },
        "scope": {"full_cut_W_Z_exact": True, "moving_raw_normalizer": True,
                  "C1_fixed_width_amplitudes_allow_rank_birth": True,
                  "arbitrary_C1_density_alone_suffices": False,
                  "amplitude_jet_energy_is_physical_energy": False,
                  "actual_A9_preparation_first_source_vanishes_for_both_Info_contracts": True,
                  "all_N_old_action_C1_fine_preparation_first_source_zero": True,
                  "all_N_gain_action_C1_fine_preparation_first_source_zero": False,
                  "entropy_log_threshold_used": False,
                  "new_physical_Info_or_field_map": False,
                  "physical_carrier_replaced_by_covariances": False},
        "source_pins": SOURCE_PINS,
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), sort_keys=True))
