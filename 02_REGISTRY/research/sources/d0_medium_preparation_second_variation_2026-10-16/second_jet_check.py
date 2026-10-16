#!/usr/bin/env python3
"""Candidate second jet of the pinned preparation envelope.

Analytic divided-difference identities are checked against an independent
finite difference. The four hostile controls must disagree with that jet.
No physical action, trace, norm, or claim row is changed.
"""

from __future__ import annotations

from mpmath import (
    mpc,
    mpf,
    mp,
    matrix,
    eye,
    sqrt,
    log,
    exp,
    conj,
    re,
    fabs,
    iv,
    nstr,
    acos,
    cos,
    pi,
)

mp.dps = 45

P = (sqrt(5) - 1) / 2
ELL = -log(P)
DELTA = P**3 / (2 * (1 + 2 * P**2))
P2 = P**2
I_LO = P2 * (1 - DELTA)
I_HI = P2 * (1 + DELTA)
N_LEVEL = 2


class Jet:
    """Second-order dual number. Value, first derivative, second derivative."""

    def __init__(self, value, first, second):
        self.v = value
        self.d = first
        self.h = second


def _is_interval(value):
    return hasattr(value, "_mpi_")


def _sqrt(value):
    return iv.sqrt(value) if _is_interval(value) else sqrt(value)


def _log(value):
    return iv.log(value) if _is_interval(value) else log(value)


def jet_const(value, like):
    if _is_interval(like):
        zero = iv.mpf(0)
        return Jet(iv.mpf(value) if not _is_interval(value) else value, zero, zero)
    zero = like * 0
    return Jet(value + zero, zero, zero)


def jet_var(value):
    if _is_interval(value):
        return Jet(value, iv.mpf(1), iv.mpf(0))
    return Jet(value, mpf(1), mpf(0))


def jet_add(left, right):
    return Jet(left.v + right.v, left.d + right.d, left.h + right.h)


def jet_sub(left, right):
    return Jet(left.v - right.v, left.d - right.d, left.h - right.h)


def jet_scale(factor, jet):
    if _is_interval(jet.v) and not _is_interval(factor):
        factor = iv.mpf(factor)
    return Jet(factor * jet.v, factor * jet.d, factor * jet.h)


def jet_mul(left, right):
    value = left.v * right.v
    first = left.d * right.v + left.v * right.d
    second = left.h * right.v + 2 * left.d * right.d + left.v * right.h
    return Jet(value, first, second)


def jet_sqrt(jet):
    root = _sqrt(jet.v)
    first = jet.d / (2 * root)
    second = jet.h / (2 * root) - jet.d**2 / (4 * root**3)
    return Jet(root, first, second)


def jet_log(jet):
    first = jet.d / jet.v
    second = jet.h / jet.v - jet.d**2 / jet.v**2
    return Jet(_log(jet.v), first, second)


def branch_counts(old_type: int):
    if old_type == 0:
        return P * sqrt(P), P**4, 3, 2
    if old_type == 1:
        return P, P**3, 2, 1
    raise ValueError("old type must be 0 or 1")


def conditional_price(old_type: int, effect: Jet) -> Jet:
    """Scalar f_j from the pinned conditional probabilities. Natural log."""
    weight, second_weight, first_copies, second_copies = branch_counts(old_type)
    one = jet_const(1, effect.v)
    root_gap = jet_sqrt(jet_sub(one, effect))
    root_effect = jet_sqrt(effect)
    half_root = jet_scale(1 / sqrt(2), root_effect)
    weighted_gap = jet_scale(weight, root_gap)
    plus = jet_add(weighted_gap, half_root)
    minus = jet_sub(weighted_gap, half_root)
    probabilities = [jet_mul(plus, plus), jet_mul(minus, minus)]
    plain = jet_mul(jet_const(weight**2, effect.v), jet_sub(one, effect))
    for _ in range(first_copies - 2):
        probabilities.append(plain)
    pending = jet_mul(jet_const(second_weight, effect.v), jet_sub(one, effect))
    for _ in range(second_copies):
        probabilities.append(pending)
    shift = jet_const(3 - old_type, effect.v)
    pending_mass = jet_scale(second_copies * second_weight, jet_sub(one, effect))
    total = jet_add(shift, pending_mass)
    for probability in probabilities:
        total = jet_add(total, jet_scale(1 / ELL, jet_mul(probability, jet_log(probability))))
    total.probabilities = probabilities
    return total


def price_derivatives(old_type: int, effect):
    jet = conditional_price(old_type, jet_var(effect))
    return jet.v, jet.d, jet.h, jet.probabilities


def dagger(array):
    out = matrix(array.cols, array.rows)
    for row in range(array.cols):
        for col in range(array.rows):
            out[row, col] = conj(array[col, row])
    return out


def trace_of(array):
    total = mpc(0)
    for index in range(array.rows):
        total += array[index, index]
    return total


def frobenius(array):
    total = mpf(0)
    for row in range(array.rows):
        for col in range(array.cols):
            total += fabs(array[row, col]) ** 2
    return sqrt(total)


def commutator(left, right):
    return left * right - right * left


def det3(array):
    a, b, c = array[0, 0], array[0, 1], array[0, 2]
    d, e, f = array[1, 0], array[1, 1], array[1, 2]
    g, h, i = array[2, 0], array[2, 1], array[2, 2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def eigenvalues_of(array):
    size = array.rows
    if size == 1:
        return [re(array[0, 0])]
    if size == 2:
        a = re(array[0, 0])
        b = re(array[1, 1])
        gap = array[0, 1]
        half = (a + b) / 2
        radius = sqrt(((a - b) / 2) ** 2 + fabs(gap) ** 2)
        return [half + radius, half - radius]
    if size != 3:
        raise ValueError("only blocks up to 3x3 are checked")
    diagonal_sum = re(trace_of(array))
    square_sum = re(trace_of(array * array))
    sigma = (diagonal_sum**2 - square_sum) / 2
    determinant = re(det3(array))
    # λ^3 - (tr)λ^2 + σλ - det = 0, depressed by Cardano's trigonometric case.
    linear = -diagonal_sum
    constant = -determinant
    shift = linear / 3
    p_coeff = sigma - linear**2 / 3
    q_coeff = 2 * linear**3 / 27 - linear * sigma / 3 + constant
    if fabs(p_coeff) < mpf("1e-28") and fabs(q_coeff) < mpf("1e-28"):
        return [-shift, -shift, -shift]
    discriminant = (q_coeff / 2) ** 2 + (p_coeff / 3) ** 3
    if discriminant > mpf("1e-18"):
        raise AssertionError("hermitian cubic left the three-real regime")
    radius = sqrt(-p_coeff / 3)
    cosine = (-q_coeff / 2) / radius**3
    cosine = max(mpf(-1), min(mpf(1), cosine))
    theta = acos(cosine)
    return [2 * radius * cos((theta - 2 * pi * index) / 3) - shift for index in range(3)]


def _pair_kernel(array, eigenvalue):
    rows = []
    for row in range(array.rows):
        rows.append([array[row, col] - (eigenvalue if row == col else 0) for col in range(array.cols)])
    if array.rows == 1:
        return [mpc(1)]
    if array.rows == 2:
        gap = array[0, 1]
        diagonal = array[0, 0] - eigenvalue
        if fabs(gap) >= fabs(diagonal):
            vector = [gap, -(array[0, 0] - eigenvalue)]
        else:
            vector = [-(array[1, 1] - eigenvalue), conj(gap)]
        if fabs(vector[0]) + fabs(vector[1]) < mpf("1e-18"):
            vector = [mpc(1), mpc(0)] if fabs(array[0, 1]) < mpf("1e-18") else vector
        norm = sqrt(fabs(vector[0]) ** 2 + fabs(vector[1]) ** 2)
        return [component / norm for component in vector]
    best = None
    best_norm = mpf(0)
    pairs = ((0, 1, 2), (0, 2, 1), (1, 2, 0))
    for first, second, _other in pairs:
        u, v = rows[first], rows[second]
        crossed = (
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0],
        )
        norm = sqrt(sum(fabs(component) ** 2 for component in crossed))
        if norm > best_norm:
            best_norm = norm
            best = crossed
    if best is None or best_norm < mpf("1e-18"):
        raise AssertionError("no 3x3 kernel vector")
    return [component / best_norm for component in best]


def gram_columns(vectors):
    columns = []
    for vector in vectors:
        residual = [component for component in vector]
        for ready in columns:
            coefficient = sum(conj(ready[index]) * residual[index] for index in range(len(residual)))
            residual = [residual[index] - coefficient * ready[index] for index in range(len(residual))]
        norm = sqrt(sum(fabs(component) ** 2 for component in residual))
        if norm < mpf("1e-18"):
            raise AssertionError("eigenvector collapse")
        columns.append([component / norm for component in residual])
    out = matrix(len(columns[0]), len(columns))
    for col, vector in enumerate(columns):
        for row, component in enumerate(vector):
            out[row, col] = component
    return out


def eigh_hermitian(array):
    off_diagonal = mpf(0)
    for row in range(array.rows):
        for col in range(array.cols):
            if row != col:
                off_diagonal = max(off_diagonal, fabs(array[row, col]))
    if off_diagonal < mpf("1e-24"):
        values = [re(array[index, index]) for index in range(array.rows)]
        return values, eye(array.rows)
    values = eigenvalues_of(array)
    vectors = [_pair_kernel(array, value) for value in values]
    basis = gram_columns(vectors)
    rebuilt = basis * diagonal_matrix(values) * dagger(basis)
    if frobenius(rebuilt - array) > mpf("1e-18"):
        raise AssertionError("hermitian reconstruction failed")
    return values, basis


def apply_function(array, scalar_function):
    values, basis = eigh_hermitian(array)
    return basis * diagonal_matrix([scalar_function(value) for value in values]) * dagger(basis)


def positive_sqrt(array):
    return apply_function(array, sqrt)


def matrix_log(array):
    return apply_function(array, log)


def relative_entropy(state, reference):
    difference = matrix_log(state) - matrix_log(reference)
    return re(trace_of(state * difference))


def channel_factors(old_type: int, effect):
    weight, second_weight, first_copies, second_copies = branch_counts(old_type)
    gap = positive_sqrt(eye(effect.rows) - effect)
    amplitude = positive_sqrt(effect)
    half = amplitude / sqrt(2)
    factors = [(0, weight * gap + half), (0, weight * gap - half)]
    for _ in range(first_copies - 2):
        factors.append((0, weight * gap))
    pending_scale = sqrt(second_weight)
    for _ in range(second_copies):
        factors.append((1, pending_scale * gap))
    return factors


def channel_images(effects, states):
    images = []
    for old_type, (effect, state) in enumerate(zip(effects, states)):
        for block, factor in channel_factors(old_type, effect):
            images.append((block, factor * state * dagger(factor)))
    return images


def reference_states(effects, states):
    """Build the fine reference on each image corner, using the pinned weight."""
    references = []
    for old_type, (effect, state) in enumerate(zip(effects, states)):
        for block, factor in channel_factors(old_type, effect):
            weight = P ** (N_LEVEL + 4 + block)
            references.append((block, weight * eye(factor.rows)))
    return references


def entropy_against_reference(effects, states):
    total = mpf(0)
    images = channel_images(effects, states)
    references = reference_states(effects, states)
    if len(images) != len(references):
        raise AssertionError("corner count drifted")
    for (_block, image), (_ref_block, reference) in zip(images, references):
        total += relative_entropy(image, reference)
    return total


def partition(eigenvalues_by_block):
    total = mpf(0)
    weights = []
    for old_type, eigenvalues in enumerate(eigenvalues_by_block):
        mu = P ** (N_LEVEL + 1 + old_type)
        block_weights = []
        for eigenvalue in eigenvalues:
            value, _first, _second, _probabilities = price_derivatives(old_type, eigenvalue)
            raw = mu * exp(-ELL * value)
            block_weights.append(raw)
            total += raw
        weights.append(block_weights)
    return total, weights


def envelope_from_eigenvalues(eigenvalues_by_block):
    normalizer, _weights = partition(eigenvalues_by_block)
    return 6 - log(normalizer) / ELL, normalizer


def diagonal_matrix(values):
    out = matrix(len(values))
    for index, value in enumerate(values):
        out[index, index] = value
    return out


def second_jet_pieces(eigenvalues_by_block, directions):
    """Divided-difference jet of A* in the eigenbasis of each block."""
    normalizer, raw_weights = partition(eigenvalues_by_block)
    alpha = mpf(0)
    local = mpf(0)
    collision = mpf(0)
    off_diagonal = mpf(0)
    populations = []
    slopes = []
    curvatures = []
    for old_type, eigenvalues in enumerate(eigenvalues_by_block):
        population = [raw / normalizer for raw in raw_weights[old_type]]
        slope = []
        curvature = []
        for eigenvalue in eigenvalues:
            _value, first, second, _probabilities = price_derivatives(old_type, eigenvalue)
            slope.append(first)
            curvature.append(second)
        populations.append(population)
        slopes.append(slope)
        curvatures.append(curvature)
        direction = directions[old_type]
        for row, left in enumerate(eigenvalues):
            alpha += population[row] * slope[row] * re(direction[row, row])
            for col, right in enumerate(eigenvalues):
                amplitude = fabs(direction[row, col]) ** 2
                if left == right:
                    kernel = population[row] * curvature[row] - ELL * population[row] * slope[row] ** 2
                    local += kernel * amplitude
                    if row != col:
                        collision += kernel * amplitude
                else:
                    kernel = (
                        population[row] * slope[row] - population[col] * slope[col]
                    ) / (left - right)
                    local += kernel * amplitude
                    off_diagonal += kernel * amplitude
    rank_one = ELL * alpha**2
    return {
        "alpha": alpha,
        "local": local,
        "collision": collision,
        "off_diagonal": off_diagonal,
        "rank_one": rank_one,
        "second": local + rank_one,
        "normalizer": normalizer,
        "populations": populations,
        "slopes": slopes,
        "curvatures": curvatures,
    }


def shifted_eigenvalues(effects, direction, step):
    output = []
    for effect, tangent in zip(effects, direction):
        output.append(eigenvalues_of(effect + step * tangent))
    return output


def finite_second(effects, direction, step):
    base, _normalizer = envelope_from_eigenvalues([eigenvalues_of(effect) for effect in effects])
    plus, _plus_normalizer = envelope_from_eigenvalues(shifted_eigenvalues(effects, direction, step))
    minus, _minus_normalizer = envelope_from_eigenvalues(shifted_eigenvalues(effects, direction, -step))
    return (plus + minus - 2 * base) / step**2


def density_from_populations(populations):
    return [diagonal_matrix(block) for block in populations]


def fill_state_derivative(pieces, eigenvalues_by_block, directions):
    blocks = []
    for old_type, population in enumerate(pieces["populations"]):
        size = len(population)
        derivative = matrix(size)
        direction = directions[old_type]
        eigenvalues = eigenvalues_by_block[old_type]
        for row in range(size):
            for col in range(size):
                if eigenvalues[row] == eigenvalues[col]:
                    slope = pieces["slopes"][old_type][row]
                    transport = -ELL * slope * population[row] * direction[row, col]
                else:
                    transport = (population[row] - population[col]) / (
                        eigenvalues[row] - eigenvalues[col]
                    ) * direction[row, col]
                if row == col:
                    transport += ELL * pieces["alpha"] * population[row]
                derivative[row, col] = transport
        blocks.append(derivative)
    return blocks


def omit_normalizer(derivative_blocks, pieces):
    stripped = []
    for population, derivative in zip(pieces["populations"], derivative_blocks):
        copy = matrix(derivative.rows)
        for row in range(derivative.rows):
            for col in range(derivative.cols):
                value = derivative[row, col]
                if row == col:
                    value -= ELL * pieces["alpha"] * population[row]
                copy[row, col] = value
        stripped.append(copy)
    return stripped


def _lower(interval):
    return mpf(interval._mpi_[0])


def _upper(interval):
    return mpf(interval._mpi_[1])


def _abs_upper(interval):
    return max(fabs(_lower(interval)), fabs(_upper(interval)))


def enclose_scalar_bounds(pieces=512):
    """Outward enclosures of f, f', f'' and branch probabilities on I_safe."""
    width = (I_HI - I_LO) / pieces
    bounds = {
        "f_min": None,
        "f_max": None,
        "abs_fp": mpf(0),
        "abs_fpp": mpf(0),
        "abs_shape": mpf(0),
        "p_min": None,
        "p_plus_min": None,
    }
    for old_type in (0, 1):
        for index in range(pieces):
            left = I_LO + index * width
            right = I_LO + (index + 1) * width
            segment = iv.mpf([left, right])
            jet = conditional_price(old_type, jet_var(segment))
            lower_f = _lower(jet.v)
            upper_f = _upper(jet.v)
            bounds["f_min"] = lower_f if bounds["f_min"] is None else min(bounds["f_min"], lower_f)
            bounds["f_max"] = upper_f if bounds["f_max"] is None else max(bounds["f_max"], upper_f)
            bounds["abs_fp"] = max(bounds["abs_fp"], _abs_upper(jet.d))
            bounds["abs_fpp"] = max(bounds["abs_fpp"], _abs_upper(jet.h))
            shape = jet.h - iv.mpf(ELL) * jet.d * jet.d
            bounds["abs_shape"] = max(bounds["abs_shape"], _abs_upper(shape))
            for branch_index, probability in enumerate(jet.probabilities):
                lower = _lower(probability.v)
                bounds["p_min"] = lower if bounds["p_min"] is None else min(bounds["p_min"], lower)
                if branch_index == 0:
                    bounds["p_plus_min"] = (
                        lower if bounds["p_plus_min"] is None else min(bounds["p_plus_min"], lower)
                    )
    return bounds


def require(condition, name, checks):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def main():
    checks = []
    require(fabs((3 * (2 * P - 1) + 2 * (2 - 3 * P)) - 1) < mpf("1e-30"), "fibonacci_mass_one_n2", checks)
    require(I_LO > mpf("0.3") and I_HI < mpf("0.45"), "safe_interval_inside_open_unit", checks)
    root0 = 2 * P**3 / (1 + 2 * P**3)
    root1 = 2 * P**2 / (1 + 2 * P**2)
    gap = min(I_LO - 0, 1 - I_HI, abs(I_LO - root0), abs(I_HI - root0), abs(I_LO - root1), abs(I_HI - root1))
    require(I_HI < root1 and I_LO > root0 and gap > mpf("1e-3"), "safe_interval_separated_from_branch_roots", checks)

    for old_type in (0, 1):
        value, first, second, probabilities = price_derivatives(old_type, P2)
        probability_sum = sum(item.v for item in probabilities)
        require(fabs(probability_sum - 1) < mpf("1e-30"), f"probabilities_sum_one_type_{old_type}", checks)
        require(fabs(sum(item.d for item in probabilities)) < mpf("1e-24"), f"probability_derivative_sum_zero_{old_type}", checks)
        step = mpf("1e-6")
        right, _r1, _r2, _rp = price_derivatives(old_type, P2 + step)
        left, _l1, _l2, _lp = price_derivatives(old_type, P2 - step)
        require(fabs((right - left) / (2 * step) - first) < mpf("1e-10"), f"jet_first_matches_difference_{old_type}", checks)
        require(fabs((right + left - 2 * value) / step**2 - second) < mpf("1e-8"), f"jet_second_matches_difference_{old_type}", checks)

    _f0, f0_prime, _f0_second, _p0 = price_derivatives(0, P2)
    _f1, f1_prime, _f1_second, _p1 = price_derivatives(1, P2)
    require(f0_prime > mpf("0.58484") and f0_prime < mpf("0.58485"), "pinned_f0_prime_window", checks)
    require(f1_prime > mpf("1.7812") and f1_prime < mpf("1.7813"), "pinned_f1_prime_window", checks)

    import sympy as sp

    ell, z0, weight = sp.symbols("ell z0 w", positive=True)
    psi0, psi1, psi2 = sp.symbols("psi0 psi1 psi2", real=True)
    coordinate_u, coordinate_v = sp.symbols("u v", real=True)
    psi = lambda coordinate: psi0 + psi1 * coordinate + psi2 * coordinate**2 / 2
    def addressed(parameters):
        blank = sp.exp(-ell * psi0)
        normalizer = z0 + weight * sum(sp.exp(-ell * psi(item)) - blank for item in parameters)
        return 6 - sp.log(normalizer) / ell, normalizer
    action, _normalizer_symbol = addressed((coordinate_u, coordinate_v))
    a0 = weight * sp.exp(-ell * psi0) / z0
    diagonal = sp.diff(action, coordinate_u, 2).subs({coordinate_u: 0, coordinate_v: 0})
    mixed = sp.diff(action, coordinate_u, coordinate_v).subs({coordinate_u: 0, coordinate_v: 0})
    published_diagonal = a0 * psi2 - ell * (a0 - a0 * a0) * psi1**2
    published_mixed = ell * a0 * a0 * psi1**2
    require(sp.simplify(diagonal - published_diagonal) == 0, "scalar_hessian_matches_published_14", checks)
    require(sp.simplify(mixed - published_mixed) == 0, "scalar_mixed_matches_published_14", checks)
    kernel = a0 * psi2 - ell * a0 * psi1**2
    alpha_symbol = a0 * psi1
    reconstructed = sp.simplify(kernel + ell * alpha_symbol**2)
    require(sp.simplify(reconstructed - published_diagonal) == 0, "divided_difference_rebuilds_scalar_hessian", checks)
    ignored = sp.simplify(published_diagonal - kernel)
    require(sp.simplify(ignored - ell * a0**2 * psi1**2) == 0, "ignoring_Z_drops_rank_one_term", checks)

    bounds = enclose_scalar_bounds()
    f_span = bounds["f_max"] - bounds["f_min"]
    population_factor = exp(ELL * f_span)
    c1 = bounds["abs_fp"]
    shape = bounds["abs_shape"]
    kernel_bound = population_factor * shape
    require(bounds["p_min"] > mpf("5e-4"), "branch_probabilities_bounded_away_from_zero", checks)
    require(c1 < mpf("2.12"), "C1_outward_decimal", checks)
    require(bounds["abs_fpp"] < mpf("19.52"), "C2_outward_decimal", checks)
    require(shape < mpf("20.41"), "shape_outward_decimal", checks)
    require(population_factor < mpf("1.104"), "population_factor_outward_decimal", checks)
    require(kernel_bound < mpf("22.53"), "kernel_bound_outward_decimal", checks)
    require(bounds["p_min"] > mpf("5.912e-4"), "P_min_outward_decimal", checks)
    require(bounds["p_plus_min"] > mpf("0.659"), "plus_branch_outward_decimal", checks)
    require(gap > mpf("0.02555"), "root_gap_outward_decimal", checks)

    lam = P2
    mu = P2 * (1 + DELTA / 2)
    nu = P2 * (1 - DELTA / 2)
    eigenvalues = ([lam, lam, mu], [nu, P2])
    effects = [diagonal_matrix(block) for block in eigenvalues]
    direction = [
        matrix(
            [
                [mpf("1") / 2, mpc(1), mpc("1", "0.3")],
                [mpc(1), -mpf("1") / 2, mpc(0)],
                [mpc("1", "-0.3"), mpc(0), mpf("1") / 3],
            ]
        ),
        matrix([[mpf("1") / 4, mpc("0.5", "-0.2")], [mpc("0.5", "0.2"), -mpf("1") / 5]]),
    ]
    require(frobenius(commutator(effects[0], direction[0])) > mpf("1e-6"), "example_block_is_noncommuting", checks)
    require(eigenvalues[0][0] == eigenvalues[0][1], "example_has_exact_eigenvalue_collision", checks)
    pieces = second_jet_pieces(eigenvalues, direction)
    require(fabs(pieces["second"] - re(pieces["second"])) < mpf("1e-20"), "second_jet_is_real", checks)
    require(fabs(pieces["alpha"]) > mpf("1e-6"), "example_has_nonzero_normalizer_slope", checks)
    require(fabs(pieces["off_diagonal"]) > mpf("1e-6"), "off_diagonal_divided_difference_nonzero", checks)
    require(fabs(pieces["collision"]) > mpf("1e-6"), "collision_pair_contribution_nonzero", checks)
    require(fabs(pieces["rank_one"]) > mpf("1e-8"), "normalizer_rank_one_nonzero", checks)

    step = mpf("1e-4")
    coarse = finite_second(effects, direction, step)
    fine = finite_second(effects, direction, step / 2)
    richardson = (4 * fine - coarse) / 3
    require(fabs(richardson - pieces["second"]) < mpf("1e-9"), "finite_difference_matches_divided_difference", checks)
    commuting = pieces["second"] - pieces["off_diagonal"] - pieces["collision"]
    require(fabs(commuting - richardson) > mpf("1e-4"), "commuting_shortcut_disagrees", checks)
    without_normalizer = pieces["second"] - pieces["rank_one"]
    require(fabs(without_normalizer - richardson) > mpf("1e-5"), "ignoring_Z_disagrees", checks)
    without_collision = pieces["second"] - pieces["collision"]
    require(fabs(without_collision - richardson) > mpf("1e-4"), "dropping_collision_pairs_disagrees", checks)

    try:
        _boom = (pieces["populations"][0][0] - pieces["populations"][0][1]) / (
            eigenvalues[0][0] - eigenvalues[0][1]
        )
        singular = True
    except ZeroDivisionError:
        singular = False
    require(not singular, "naive_collision_quotient_does_not_define_a_value", checks)
    probe_gaps = [mpf("1e-3"), mpf("1e-6"), mpf("1e-9")]
    collision_values = []
    second_at_collision = price_derivatives(0, lam)[2]
    for gap_probe in probe_gaps:
        _left_value, left_slope, _left_curve, _left_probabilities = price_derivatives(0, lam)
        _right_value, right_slope, _right_curve, _right_probabilities = price_derivatives(0, lam + gap_probe)
        collision_values.append((right_slope - left_slope) / gap_probe)
    require(fabs(collision_values[-1] - second_at_collision) < mpf("1e-6"), "collision_limit_of_f_prime_is_f_second", checks)
    require(max(fabs(item) for item in collision_values) < 5 * (1 + fabs(second_at_collision)), "divided_difference_stays_bounded", checks)
    require(min(1 / gap_probe for gap_probe in probe_gaps) > 100 * (1 + c1), "reciprocal_gap_is_not_the_hessian", checks)

    state_tangent = fill_state_derivative(pieces, eigenvalues, direction)
    tangent_trace = sum(re(trace_of(block)) for block in state_tangent)
    require(fabs(tangent_trace) < mpf("1e-18"), "state_derivative_preserves_trace", checks)
    stripped = omit_normalizer(state_tangent, pieces)
    stripped_trace = sum(re(trace_of(block)) for block in stripped)
    require(fabs(stripped_trace) > mpf("1e-6"), "ignoring_Z_leaves_the_state_simplex", checks)

    populations = pieces["populations"]
    states = density_from_populations(populations)
    base_entropy = entropy_against_reference(effects, states)
    identity_gap = base_entropy + log(pieces["normalizer"])
    require(fabs(identity_gap) < mpf("1e-18"), "channel_relative_entropy_matches_normalizer", checks)
    unital_defect = mpf(0)
    for old_type, effect in enumerate(effects):
        total = eye(effect.rows) * 0
        for _block, factor in channel_factors(old_type, effect):
            total += dagger(factor) * factor
        unital_defect += frobenius(total - eye(effect.rows))
    require(unital_defect < mpf("1e-18"), "channel_factors_are_unital", checks)

    def frozen_price(step_value):
        moved = [effect + step_value * tangent for effect, tangent in zip(effects, direction)]
        entropy = entropy_against_reference(moved, states)
        return 6 + entropy / ELL

    def remainder_at(step_value):
        moved_states = [state + step_value * tangent for state, tangent in zip(states, state_tangent)]
        return relative_entropy_pair(effects, moved_states, states)

    def schur_at(step_value):
        frozen_second = (
            frozen_price(step_value) + frozen_price(-step_value) - 2 * frozen_price(0)
        ) / step_value**2
        remainder_second = (
            remainder_at(step_value) + remainder_at(-step_value) - 2 * remainder_at(0)
        ) / step_value**2
        return frozen_second - remainder_second / ELL, frozen_second, remainder_second

    price_step = mpf("4e-4")
    schur_coarse, frozen_coarse, remainder_coarse = schur_at(price_step)
    schur_fine, frozen_fine, remainder_fine = schur_at(price_step / 2)
    schur = (4 * schur_fine - schur_coarse) / 3
    frozen_second = (4 * frozen_fine - frozen_coarse) / 3
    remainder_second = (4 * remainder_fine - remainder_coarse) / 3
    require(fabs(schur - pieces["second"]) < mpf("1e-8"), "schur_envelope_matches_partition_jet", checks)
    require(fabs(frozen_second - pieces["second"]) > mpf("1e-2"), "frozen_preparation_partial_is_not_the_envelope", checks)

    op_norms = []
    hs_squares = []
    for tangent in direction:
        op_norms.append(max(fabs(value) for value in eigenvalues_of(tangent)))
        hs_squares.append(frobenius(tangent) ** 2)
    safe_majorant = kernel_bound * sum(hs_squares) + ELL * c1**2 * max(op_norms) ** 2
    require(fabs(pieces["second"]) <= safe_majorant, "example_obeys_safe_majorant", checks)

    smallest_population = min(value for block in populations for value in block)
    output_floor = smallest_population * bounds["p_min"]
    eta_squares = [frobenius(block) ** 2 for block in state_tangent]
    remainder_ceiling = (5 * eta_squares[0] + 3 * eta_squares[1]) / output_floor
    require(output_floor > 0, "example_output_floor_positive", checks)
    require(remainder_second > 0, "remainder_hessian_positive_on_example", checks)
    require(remainder_second < remainder_ceiling, "remainder_hessian_obeys_output_margin", checks)

    # Amplitude rank birth is not a quadratic Hessian. eps = t^2.
    birth_constant = mpf("1.7")
    ratios = []
    for exponent in (4, 8, 12):
        eps = mpf(10) ** (-exponent)
        delta = ((1 - eps) * log(1 - eps) + eps * log(eps) + eps * birth_constant) / ELL
        ratios.append(delta / eps)
    require(ratios[0] > ratios[1] > ratios[2] and ratios[2] < -20, "rank_birth_ratio_diverges", checks)
    smooth_prediction = ratios[0]
    require(fabs(ratios[2] - smooth_prediction) > 10, "one_finite_hessian_cannot_fit_rank_birth", checks)

    report = {
        "checks": len(checks),
        "I_lo": nstr(I_LO, 25),
        "I_hi": nstr(I_HI, 25),
        "delta": nstr(DELTA, 25),
        "gap": nstr(gap, 20),
        "root0": nstr(root0, 20),
        "root1": nstr(root1, 20),
        "f0_prime": nstr(f0_prime, 20),
        "f1_prime": nstr(f1_prime, 20),
        "f_min": nstr(bounds["f_min"], 20),
        "f_max": nstr(bounds["f_max"], 20),
        "C1": nstr(c1, 20),
        "C2": nstr(bounds["abs_fpp"], 20),
        "shape": nstr(shape, 20),
        "population_factor": nstr(population_factor, 20),
        "kernel_bound": nstr(kernel_bound, 20),
        "P_min": nstr(bounds["p_min"], 20),
        "P_plus_min": nstr(bounds["p_plus_min"], 20),
        "alpha": nstr(pieces["alpha"], 20),
        "second": nstr(pieces["second"], 20),
        "off_diagonal": nstr(pieces["off_diagonal"], 20),
        "collision": nstr(pieces["collision"], 20),
        "rank_one": nstr(pieces["rank_one"], 20),
        "richardson": nstr(richardson, 20),
        "fd_gap": nstr(richardson - pieces["second"], 12),
        "schur": nstr(schur, 20),
        "schur_gap": nstr(schur - pieces["second"], 12),
        "majorant": nstr(safe_majorant, 20),
        "population_min": nstr(smallest_population, 20),
        "output_floor": nstr(output_floor, 20),
        "birth_ratios": [nstr(item, 12) for item in ratios],
        "normalizer": nstr(pieces["normalizer"], 20),
        "identity_gap": nstr(identity_gap, 12),
    }
    for key, value in report.items():
        print(f"{key}: {value}")
    print("PASS second_jet_check")


def relative_entropy_pair(effects, states, references):
    total = mpf(0)
    for old_type, (effect, state, reference) in enumerate(zip(effects, states, references)):
        for _block, factor in channel_factors(old_type, effect):
            image = factor * state * dagger(factor)
            reference_image = factor * reference * dagger(factor)
            total += relative_entropy(image, reference_image)
    return total


if __name__ == "__main__":
    main()
