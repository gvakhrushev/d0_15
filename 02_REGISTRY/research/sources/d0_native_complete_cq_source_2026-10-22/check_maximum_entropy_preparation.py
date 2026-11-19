#!/usr/bin/env python3
"""Narrow maximum-entropy consumer of exact original CAR16 spectral data.

Uses only Python's standard library. No old suite is replayed. The proof
is analytical; Decimal log/exp controls are not interval certificates.
Every check executes under python -O. This program never writes evidence.
"""
from __future__ import annotations

from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
import json


CHECKS: list[str] = []


def require(condition: bool, name: str) -> None:
    if not condition:
        raise ArithmeticError(name)
    CHECKS.append(name)


def dec(q: Q | int) -> D:
    if isinstance(q, Q):
        return D(q.numerator) / D(q.denominator)
    return D(q)


def entropy(weights: list[D]) -> D:
    return -sum((p * p.ln() for p in weights if p), D(0))


def inverse_state(lambdas: list[D]) -> tuple[list[D], D]:
    inv = [1 / lam for lam in lambdas]
    z = sum(inv, D(0))
    return [x / z for x in inv], D(len(inv)) / z


def gibbs(lambdas: list[D], beta: D) -> tuple[list[D], D]:
    # Subtracting min(lambda) only stabilizes normalized Gibbs weights.
    lo = min(lambdas)
    vals = [(-beta * (lam - lo)).exp() for lam in lambdas]
    z = sum(vals, D(0))
    weights = [x / z for x in vals]
    return weights, sum((p * lam for p, lam in zip(weights, lambdas)), D(0))


def maxent(lambdas: list[D], energy: D) -> tuple[list[D], D]:
    if max(lambdas) == min(lambdas):
        raise ValueError('scalar constraint has no unique Gibbs multiplier')
    left, right = D(0), D(1)
    while gibbs(lambdas, right)[1] > energy:
        right *= 2
    # 280 bisections put the root well beyond the 65-digit check tolerance.
    for _ in range(280):
        mid = (left + right) / 2
        if gibbs(lambdas, mid)[1] > energy:
            left = mid
        else:
            right = mid
    beta = (left + right) / 2
    return gibbs(lambdas, beta)[0], beta


def relative(weights: list[D], reference: list[D]) -> D:
    return sum((p * (p / q).ln() for p, q in zip(weights, reference)), D(0))


def spectral_gap(lambdas: list[D]) -> tuple[D, D, D]:
    rho, energy = inverse_state(lambdas)
    sigma, beta = maxent(lambdas, energy)
    gap = entropy(sigma) - entropy(rho)
    rel = relative(rho, sigma)
    return gap, rel, beta


def text(x: D) -> str:
    return format(x, '.55g')


def main() -> None:
    with localcontext() as ctx:
        ctx.prec = 80
        mu_q = Q(141489, 10240000)
        h_q = Q(69399, 5030720)
        dmu_q = -Q(328779, 204800000)
        dh_q = -Q(20040939, 9885993640)
        eps_sq = mu_q * (mu_q - h_q)
        require(Q(55, 100000) ** 2 < eps_sq < Q(56, 100000) ** 2,
                'exact original native spectral-splitting brackets')
        require(mu_q > h_q > 0,
                'exact original nonscalar regular harmonic-energy chart')
        mu, h, dmu, dh = map(dec, (mu_q, h_q, dmu_q, dh_q))
        eps = dec(eps_sq).sqrt()
        deps = ((2 * mu - h) * dmu - mu * dh) / (2 * eps)
        lm, lp = mu - eps, mu + eps
        lambdas = [lm] * 8 + [lp] * 8
        dlambdas = [dmu - deps] * 8 + [dmu + deps] * 8
        rho, energy = inverse_state(lambdas)
        sigma, beta = maxent(lambdas, energy)
        beta_secant = (lp / lm).ln() / (lp - lm)
        tol = D('1e-65')
        require(abs(energy - h) < tol,
                'native mean energy equals full16 harmonic moment')
        require(abs(beta - beta_secant) < tol,
                'generated constraint multiplier equals owned two-band secant')
        require(max(abs(x-y) for x,y in zip(rho,sigma)) < tol,
                'native invariant preparation is exact marginal maximum entropy')
        require(abs(entropy(sigma)-entropy(rho)) < tol,
                'native marginal entropy gain vanishes')
        require(1 / lp < beta < 1 / lm,
                'dual multiplier lies between true reciprocal energy levels')
        p = (D(5).sqrt()-1) / 2
        beta0 = 2 * p * p
        require(beta > 66 and beta0 < D('0.8'),
                'generated dual multiplier is not actual Golden inverse temperature')
        golden_sigma = gibbs(lambdas, beta0)[0]
        fixed_temp_gap = sum((abs(x-y) for x,y in zip(rho,golden_sigma)),D(0))
        require(fixed_temp_gap > D('0.0388'),
                'original fixed-temperature Gibbs mismatch preserved')

        # Differentiate the true normalized inverse state directly.
        zinv = sum((1/lam for lam in lambdas),D(0))
        dzinv = -sum((dl/lam**2 for dl,lam in zip(dlambdas,lambdas)),D(0))
        drho = [(-dl/lam**2)/zinv - (1/lam)*dzinv/zinv**2
                for dl,lam in zip(dlambdas,lambdas)]
        d_entropy = -sum((dp*pr.ln() for dp,pr in zip(drho,rho)),D(0))
        moving_test = sum((pr*dl for pr,dl in zip(rho,dlambdas)),D(0))
        envelope = beta*(dh-moving_test)
        frozen_test = beta*dh
        require(abs(sum(drho,D(0))) < tol,
                'complete native preparation derivative has zero trace')
        require(abs(d_entropy-envelope) < tol,
                'direct native entropy derivative equals moving-test envelope')
        require(abs(envelope-frozen_test) > D('0.1'),
                'freezing actual port observable loses a nonzero first source')
        require(D('-0.01537') < d_entropy < D('-0.01536'),
                'original proper-boost entropy source retained')
        vdmu = dmu-mu*dh/h
        vdeps = (2*mu-h)*vdmu/(2*eps)
        vtest = vdmu-(eps/mu)*vdeps
        vsource = -beta*vtest
        require(vdmu > 0 and vsource < D('-0.015'),
                'fixed measured port mean still has moving-test entropy source')

        # Genuine three-band control at the SAME harmonic mean constraint.
        three = [D(1),D(2),D(4)]
        gap3, rel3, beta3 = spectral_gap(three)
        require(abs(gap3-rel3) < tol,
                'three-band entropy gap equals exact relative-entropy identity')
        require(gap3 > D('0.001'),
                'three distinct energies have strictly positive marginal gain')
        require(D(2).ln() != (D(4).ln()-D(2).ln())/2,
                'three-band logarithmic secants disagree')

        # Split two vectors within the ACTUAL native lower band. Energy and
        # maximizing state both move; we do not hold the test fixed.
        split = D('1e-11')
        plus = lambdas.copy()
        minus = lambdas.copy()
        plus[0] += split
        plus[1] -= split
        minus[0] -= split
        minus[1] += split
        gap_p, rel_p, _ = spectral_gap(plus)
        gap_m, rel_m, _ = spectral_gap(minus)
        require(abs(gap_p-rel_p) < tol and abs(gap_m-rel_m) < tol,
                'transverse split retains moving-constraint KL identity')
        require(gap_p > 0 and gap_m > 0,
                'genuine native eightfold-band splitting creates positive gain')
        first_split = (gap_p-gap_m)/(2*split)
        hessian_numeric = (gap_p+gap_m)/split**2
        hessian_exact = 2*rho[0]*(beta-1/lm)**2
        require(abs(first_split) < D('1e-55'),
                'transverse first marginal-gain source is zero')
        require(abs(hessian_numeric-hessian_exact) < D('1e-13'),
                'positive transverse Hessian equals analytical block formula')

        # Scalar degeneracy is represented honestly: equality of states,
        # but no unique temperature is asserted or silently returned.
        scalar = [D(2)]*4
        srho, sh = inverse_state(scalar)
        require(srho == [D(1)/4]*4 and sh == D(2),
                'scalar state equals the unconstrained entropy maximizer')
        try:
            maxent(scalar,sh)
        except ValueError:
            rejected = True
        else:
            rejected = False
        require(rejected, 'scalar degeneracy does not claim a unique multiplier')

        out = {
            'status':'PASS',
            'scope':'Analytical theorem with 80-digit Decimal finite controls; no interval claim',
            'input_checkpoint':'cd7595b0808e47c38147f25e2cabe476ecb508f8',
            'checks':CHECKS,
            'check_count':len(CHECKS),
            'native':{
                'dimension':16,'multiplicities':[8,8],
                'mu':str(mu_q),'h':str(h_q),
                'd_mu':str(dmu_q),'d_h':str(dh_q),
                'beta_dual':text(beta),
                'beta_Golden_actual':text(beta0),
                'actual_temperature_trace_norm_gap':text(fixed_temp_gap),
                'entropy':text(entropy(rho)),
                'proper_boost_entropy_source':text(d_entropy),
                'wrong_frozen_test_source':text(frozen_test),
                'one_port_neutral_entropy_source':text(vsource),
                'marginal_gain':'0 (analytical)',
                'all_smooth_first_gain_sources':'0 (analytical; nonscalar regular point)',
                'transverse_gain_hessian':text(hessian_exact),
                'transverse_hessian_numeric_error':text(abs(hessian_numeric-hessian_exact))
            },
            'three_band_control':{
                'energies':[1,2,4],
                'beta_dual':text(beta3),
                'strict_entropy_gain':text(gap3)
            },
            'GR_closed':False,
            'physical_Book03_Info_selected':False,
            'full_history_replaced_by_DATA_marginal':False
        }
        print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
