#!/usr/bin/env python3
"""Global 718=685+32+1 reconstruction of original positive scalar weights.

Consumes the exact 2/3-cycle P inverse. The supplied prior and Perron scalar
are mathematical inputs; neither is asserted physically selected by D0.
"""
import numpy as np
from check_global_closed_history_source import (
    N, SUPPORT, from_cost, perron, cycle_data, reconstructed_p
)


def reconstruct_all(k):
    rho, r, p = perron(k)
    b, tri = cycle_data(p)
    rho_markov, p_rec, _ = reconstructed_p(b, tri)
    assert abs(rho_markov - 1) < 2e-12
    old_prior = r/r.sum()
    rebuilt = rho*p_rec*(old_prior[:, None]/old_prior[None, :])
    return rho, old_prior, p_rec, rebuilt


def main():
    y0 = .19
    k, dlogk = from_cost(y0)
    rho, prior, p, built = reconstruct_all(k)
    error = max(abs(k[SUPPORT]-built[SUPPORT]))
    assert error < 2e-12
    assert max(abs(built[~SUPPORT])) == 0

    # All original edge-field first sources, not only conditioned Markov.
    dt = 1e-5
    kp = reconstruct_all(from_cost(y0+dt)[0])[3]
    km = reconstruct_all(from_cost(y0-dt)[0])[3]
    dbuilt = (np.log(kp[SUPPORT])-np.log(km[SUPPORT]))/(2*dt)
    derivative_error = max(abs(dbuilt-dlogk[SUPPORT]))
    assert derivative_error < 2e-8

    # Hostile control: even ALL conditioned 2/3-loop observations cannot see
    # the 32 independent old-prior parameters or one absolute price scale.
    different_prior = prior*np.exp(.11*np.sin(np.arange(N)))
    different_prior /= different_prior.sum()
    different_rho = rho*1.17
    different_k = different_rho*p*(different_prior[:, None]/different_prior[None, :])
    rho_new, prior_new, p_new, rebuilt_new = reconstruct_all(different_k)
    assert np.max(abs(p_new-p)) < 3e-12
    assert max(abs(prior_new-different_prior)) < 3e-12
    assert abs(rho_new/different_rho-1) < 2e-12
    assert np.max(abs(different_k-built)) > .1

    # A pure common scale shift is invisible even to the old prior, so one
    # absolute source is required. A pure endpoint tilt moves prior only.
    scaled = reconstruct_all(1.041*k)
    assert np.max(abs(scaled[2]-p)) < 3e-12
    assert np.max(abs(scaled[1]-prior)) < 3e-12
    assert abs(scaled[0]/rho-1.041) < 3e-12

    print('PASS all 718 unnormalized native scalar weights reconstructed =', f'{error:.3e}')
    print('PASS all 718 absolute log-first-sources reconstructed =', f'{derivative_error:.3e}')
    print('PASS exact 718=685 conditioned +32 preparation +1 Perron scale')
    print('PASS hostile prior+scale shift: identical whole Markov 2/3-history data')
    print('PASS independent common-scale shift: prior and P unchanged, rho changed')
    print('NOTE: these 718 scalars are mathematical Book-transfer inputs, not the full physical H+J+R')


if __name__ == '__main__':
    main()
