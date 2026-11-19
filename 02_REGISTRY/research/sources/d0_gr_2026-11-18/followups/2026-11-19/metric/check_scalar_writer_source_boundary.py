"""Scalar complemented writer: input-only source and fixed-heat boundary.

The physical local blocks and readiness are consumed from their owners;
the numerical quantum channel below is a deterministic finite control for
the general scalar-effect theorem, not a simulation of the full factory.
"""
import json
import math
import numpy as np


def need(ok, message):
    if not ok:
        raise AssertionError(message)


def main():
    p = (math.sqrt(5.0) - 1.0) / 2.0
    ell = math.log(1.0 / p)
    beta = 2.0 * p * p
    eye = np.eye(2)
    d = [np.diag([math.sqrt(p), p]), np.diag([p, math.sqrt(p)])]
    effects = [x.T @ x for x in d]
    need(np.linalg.norm(sum(effects) - eye) < 1e-14, 'writer instrument TP')
    z = sum(p ** (h + (1 - h)) * effects[h] for h in range(2))
    need(np.linalg.norm(z - p * eye) < 1e-14, 'paid complementary effect')
    qloc = [255.0 / 256.0, 1.0 / 256.0]
    loc_z = qloc[0] + p * qloc[1]
    full_effect = sum(p * p ** t * qloc[t] * effects[h]
                      for h in range(2) for t in range(2))
    need(np.linalg.norm(full_effect - p * loc_z * eye) < 1e-14,
         'complemented writer plus scalar locator')
    # Old RIGHT is a nontrivial qubit; h,t outcomes are explicitly retained.
    # h-dependent rotations are a finite algebraic control, not the CAR device.
    xgate = np.array([[0., 1.], [1., 0.]])
    rgate = np.array([[0.8, -0.6], [0.6, 0.8]])
    unitaries = {(h, t): np.kron((rgate if h else eye) @ (xgate if t else eye), eye)
                 for h in range(2) for t in range(2)}

    def channel(rho, weighted):
        blocks = []
        for h in range(2):
            k = np.kron(d[h], eye)
            for t in range(2):
                u = unitaries[h, t]
                weight = qloc[t] * (p ** t / loc_z if weighted else 1.0)
                blocks.append(weight * u @ k @ rho @ k.conj().T @ u.conj().T)
        out = np.zeros((16, 16), dtype=complex)
        for i, block in enumerate(blocks):
            out[4*i:4*i+4, 4*i:4*i+4] = block
        return out

    right = np.array([[0.63, 0.11j], [-0.11j, 0.37]], dtype=complex)
    rho = np.kron(np.diag([0.5, 0.5]), right)
    tangent = np.kron(np.diag([-1.0, 1.0]), right)
    dq_dt = p ** 3
    h1_effect = np.kron(effects[1], eye)
    need(abs(np.trace(h1_effect @ rho).real - 0.5) < 1e-14, 'central descriptor')
    need(abs(np.trace(h1_effect @ tangent).real - dq_dt) < 1e-14, 'physical gain')
    g0, gw = channel(rho, False), channel(rho, True)
    x0, xw = channel(tangent, False), channel(tangent, True)
    need(abs(np.trace(g0) - 1) < 1e-14 and abs(np.trace(gw) - 1) < 1e-14,
         'both complete retained instruments normalized')
    need(abs(np.trace(x0)) < 1e-14 and abs(np.trace(xw)) < 1e-14,
         'scalar partition has zero input derivative')
    need(np.linalg.norm(g0 - gw) > 1e-4,
         'scalar effect does not equate conditional quantum outputs')
    rng = np.random.default_rng(1729)
    aa = rng.standard_normal((16, 16)) + 1j * rng.standard_normal((16, 16))
    aa = (aa + aa.conj().T) / 2.0
    aa /= np.max(np.abs(np.linalg.eigvalsh(aa)))
    scalar, err = 0.65, 0.03
    kheat = scalar * np.eye(16) + err * aa
    def pairing(left, right):
        return np.einsum('ij,ji->', left, right, optimize=False).real
    uw = pairing(kheat, gw)
    u0 = pairing(kheat, g0)
    slope = -(pairing(kheat, xw) / uw - pairing(kheat, x0) / u0) / ell / dq_dt
    lower = scalar - err
    slope_bound = 4.0 * err / (lower * ell * p ** 3)
    need(abs(slope) <= slope_bound + 1e-12, 'fixed heat source bound')
    # Two independently regenerated descriptors: existing exact target Q(s,t).
    def B(t):
        return (1-t)**2 + t*t
    def Q(s, t):
        return -(B(s)-s*s)*B(t) - t*t*B(s)
    step = 1e-5
    ds = (Q(.5+step, .5) - Q(.5-step, .5))/(2*step)
    dt = (Q(.5, .5+step) - Q(.5, .5-step))/(2*step)
    need(abs(ds-.5) < 1e-9 and abs(dt+.5) < 1e-9, 'two-copy target contrast')
    lmin = 12
    x = beta/11.0
    e12 = 2*x**lmin/(math.factorial(lmin)*(1-x/(lmin+1)))
    physical_bound = 4*math.exp(2*beta)*e12/(ell*p**3)
    out = {
      'status': 'PASS; fixed scalar-effect input-only source boundary',
      'writer_and_locator_effect_without_hardware_ready': p*loc_z,
      'direct_writer_q_at_half': .5,
      'direct_writer_dq_dt': dq_dt,
      'normalized_partition_input_source': 0.0,
      'same_scalar_effect_does_not_mean_same_full_output': True,
      'finite_control_heat_source_per_dq': slope,
      'finite_control_heat_bound_per_dq': slope_bound,
      'owner_heat_tail_L12_upper': e12,
      'owner_heat_source_per_dq_upper_L12': physical_bound,
      'two_copy_target_dQ_ds': ds,
      'two_copy_target_dQ_dt': dt,
      'FQ_weight_is_selected_Book03_price': False,
      'whole_factory_all_failures_and_full_GR_proved': False,
      'GR_closed': False,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
