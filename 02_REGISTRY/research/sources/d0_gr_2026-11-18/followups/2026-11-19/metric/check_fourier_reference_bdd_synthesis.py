"""Fresh Fourier128 for both exact k=89 CAR references (conditional gates)."""
from itertools import product
import json
import math
import numpy as np
from mpmath import iv

import check_dyadic_car_loader as car
from check_fourier_fresh_localization import original_reference
from check_native_fourier_uncompute import BDD, schedule


def main():
    pairs, _, S = original_reference()
    assert S == 256 and len(pairs) == 64
    diagram = BDD()
    roots = [diagram.compile([(k[r] >> b) & 1 for k in pairs])
             for r in range(4) for b in (0, 1)]
    assert len(diagram.nodes) == 105
    coords = list(product(range(4), repeat=4))
    # C_{(y,M),F}; the complete original Fourier reference basis F=(j,t).
    chi = np.zeros((S, 128), dtype=np.float64)
    for yi, y in enumerate(coords):
        for j, k in enumerate(pairs):
            b = sum(k[r] * y[r] for r in range(4)) % 4
            for t in (0, 1):
                out, sign = schedule(diagram, roots, j, y, t)
                out2, sign2 = schedule(diagram, roots, j, y, out)
                assert (out, sign) == (t ^ (b & 1), -1 if b & 2 else 1)
                assert out2 == t and sign * sign2 == 1
                if t == 0:
                    chi[yi, 2*j + out] = sign / 128.0
    assert np.all(np.sum(chi*chi, axis=1) == 1/256)
    assert np.array_equal(np.einsum('yi,yj->ij', chi, chi, optimize=False), np.eye(128)/128)

    p = (math.sqrt(5)-1)/2
    a = math.sqrt(p)
    theta = math.asin(p)
    amp, filler = p*math.sin(712*theta), -p*math.cos(712*theta)
    assert amp > 0 and filler > 0
    G = np.array([[a, -p], [p, a]])
    X = np.array([[0., 1.], [1., 0.]])
    mat = car.mat_one(0, G)
    for bit in (1, 2, 3):
        mat = car.mm(car.mat_one(bit, X), mat)
    for bit in (1, 2, 3):
        mat = car.mm(car.mat_cx(0, bit), mat)
    base = car.mm(car.rotation(14, 0, -712*theta), mat)
    matrices = [car.mm(car.rotation(0, 15, n*math.pi/2), base)
                for n in range(4)]
    max_col_error = 0.0
    for n, U in enumerate(matrices):
        assert np.linalg.norm(car.mm(U.T, U) - np.eye(16)) < 1e-12
        expected = np.zeros(16)
        expected[1], expected[14] = a, filler
        expected[0] = amp * (1, 0, -1, 0)[n]
        expected[15] = amp * (0, 1, 0, -1)[n]
        max_col_error = max(max_col_error, float(np.linalg.norm(U[:, 1]-expected)))
    assert max_col_error < 1e-12

    max_gram_error = 0.0
    max_site_formula_error = 0.0
    for mu in (0, 1):
        # True C on the full CAR16, with both original real components.
        matter = np.stack([matrices[y[mu]][:, 1] for y in coords])
        C = (chi[:, None, :] * matter[:, :, None]).reshape(S*16, 128)
        gram = np.einsum('yi,yj->ij', C, C, optimize=False)
        max_gram_error = max(max_gram_error, float(np.max(np.abs(gram - np.eye(128)/128))))
        for yi, y in enumerate(coords):
            sign = (1, 0, -1, 0)[y[mu]]
            sine = (0, 1, 0, -1)[y[mu]]
            max_site_formula_error = max(max_site_formula_error,
                abs(matter[yi, 0] - amp*sign), abs(matter[yi, 15] - amp*sine))
    assert max_gram_error < 1e-14 and max_site_formula_error < 1e-12

    # Actual finite repeated-factory success probabilities, assuming their
    # scalar success effects and independence exactly as in the owners.
    iv.dps = 130
    one = iv.mpf(1)
    pp = (iv.sqrt(5)-one)/2
    b2_64 = one-pp**384
    b3_64 = one-(one-16*pp**9)**64
    b0_16 = one-(one-2*pp**3)**16
    b2_32 = one-(one-4*pp**3)**32
    b3_32 = one-(one-16*pp**9)**32
    P_W = (one-pp**40)*(b2_64**6*b3_64)**456
    P_car = b0_16**86*(b2_32**4*b3_32)**43*b3_32**3
    # hW is prepared once; it is reused to prepare fourteen independent plus
    # by finite two-probe X-measurement, plus the fresh t=0 type wire.
    P_plus14 = b2_64**14
    gamma = P_W*P_car*P_plus14
    assert gamma > iv.mpf('0.9732214649') and gamma < iv.mpf('0.9732214652')
    theta_amp = iv.atan2(iv.sqrt(gamma/256), iv.sqrt(one-gamma/256))
    amp_prob = iv.sin(25*theta_amp)**2
    assert amp_prob > iv.mpf('0.9991947531') and amp_prob < iv.mpf('0.9991947534')
    print(json.dumps({
        'status':'PASS', 'L':4, 'actual_original_fourier_modes':64,
        'checked_yj_pairs':S*64, 'full_yjt_columns':S*64*2,
        'W_involution_on_all_prepared_type_columns':True,
        'W_commutes_with_SITE_controlled_CAR_on_success':True,
        'original_Fourier_gram_I128_over_128':True,
        'gram_max_float_error':max_gram_error,
        'CAR_full_columns_checked_per_site':16,
        'reference_directions':[0,1], 'CAR_site_labels_per_direction':4,
        'max_CAR_reference_float_error':max_col_error,
        'max_site_formula_float_error':max_site_formula_error,
        'factory_P_W':str(P_W), 'factory_P_CAR':str(P_car),
        'factory_P_fourteen_plus':str(P_plus14),
        'factory_P_one_full_reference':str(gamma),
        'factory_P_32_references':str(gamma**32),
        'factory_P_80_references':str(gamma**80),
        'conditional_raw_amplification_iterations':12,
        'conditional_raw_amplification_P_one':str(amp_prob),
        'conditional_raw_amplification_P_80':str(amp_prob**80),
        'known_one_separate_from_raw_inverse_required':True,
        'conditional_amplification_requires_unbuilt_coherent_raw_dilation':True,
        'general_current_fields_or_full_field_derivatives_compiled':False,
        'complete_source_Book03_and_GR_closed':False,
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
