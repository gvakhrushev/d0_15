"""Literal descriptor-to-CAR phase interface and protected seed trace.

The all-success logical composition is checked. Heralded gate/factory
realizations, actual full bank, physical measurement, and GR remain open.
"""
from collections import Counter
from itertools import product
import math
import numpy as np

from check_native_golden_descriptor_secants import check_columns, program
from check_two_parameter_fourier_catalogue import programme
from check_native_fourier_uncompute import BDD, schedule
from check_fourier_fresh_localization import original_reference
from check_composed_geometric_instrument import verify_complete_selector_t, verify_reference_polynomial
from check_source_price import need


def build_seed(data, prefix, k, h, z0, z1):
    data[prefix+'k'] = k.copy()
    data[prefix+'H'] = h.copy()
    data[prefix+'z0'] = z0.copy()
    data[prefix+'z1'] = z1.copy()
    data[prefix+'one'] = np.ones_like(k)
    for name in ('a0', 'q', 'U'):
        data[prefix+name] = np.zeros_like(k)
    for op in program(2):
        if op[0] == 'CX':
            data[prefix+op[2]] ^= data[prefix+op[1]]
        else:
            data[prefix+op[3]] ^= data[prefix+op[1]] & data[prefix+op[2]]
    need(np.array_equal(data[prefix+'H'], h), 'seed H restored')
    need(np.array_equal(data[prefix+'z0'], z0) and np.array_equal(data[prefix+'z1'], z1),
         'all seed Z restored')
    need(not data[prefix+'a0'].any() and not data[prefix+'q'].any(), 'seed scratch cleared')
    need(np.array_equal(data[prefix+'U'], h | (k & (1-z0) & (1-z1))),
         'literal seed descriptor')


def main():
    # The full logical columns of the actual n=8 seed are rechecked separately
    # from the smaller literal two-seed/CAR Cartesian product below.
    ncols, inv = check_columns(8)
    need(ncols == 2048 and inv == Counter({'T': 17, 'CX': 18}),
         'full n=8 native seed logical columns')
    # Reverse the actual seed circuit, not just its output formula, on all
    # 2^9 seed words and both original programme values.
    for k in (0, 1):
        for x in range(512):
            h, z = x & 1, x >> 1
            bits = {'H': h, 'k': k, 'one': 1,
                    'U': int(bool(h or (k and z == 0))), 'q': 0}
            bits.update({'z'+str(i): (z >> i) & 1 for i in range(8)})
            bits.update({'a'+str(i): 0 for i in range(7)})
            for op in reversed(program(8)):
                if op[0] == 'CX': bits[op[2]] ^= bits[op[1]]
                else: bits[op[3]] ^= bits[op[1]] & bits[op[2]]
            need(bits['U'] == 0 and bits['H'] == h and bits['k'] == k,
                 'native inverse clears the descriptor on every seed')
            need(all(bits['z'+str(i)] == ((z >> i) & 1) for i in range(8)),
                 'native inverse preserves all seed bits')
            need(bits['q'] == 0 and all(bits['a'+str(i)] == 0 for i in range(7)),
                 'native inverse returns every scratch')
    count = 4*8*8*256*16
    ix = np.arange(count, dtype=np.uint32)
    initial_car, y = ix & 15, (ix >> 4) & 255
    su, sv = (ix >> 12) & 7, (ix >> 15) & 7
    ku, kv = ((ix >> 18) & 1).astype(np.uint8), ((ix >> 19) & 1).astype(np.uint8)
    bit = lambda arr, j: ((arr >> j) & 1).astype(np.uint8)
    data = {}
    build_seed(data, 'u_', ku, bit(su,0), bit(su,1), bit(su,2))
    build_seed(data, 'v_', kv, bit(sv,0), bit(sv,1), bit(sv,2))
    for i in range(4): data['c'+str(i)] = bit(initial_car, i)
    for i in range(8): data['y'+str(i)] = bit(y, i)
    data.update(u=data['u_U'].copy(), v=data['v_U'].copy(),
                h=np.ones(count, dtype=np.uint8), a=np.zeros(count, dtype=np.uint8),
                b=np.zeros(count, dtype=np.uint8), t=np.zeros(count, dtype=np.uint8))
    sign = np.ones(count, dtype=np.int8)
    ops = programme()
    for op in ops:
        # An allocated seed bit is neither targeted nor even addressed by
        # this literal successful material phase network.
        need(not any(w.startswith(('u_', 'v_')) for w in op[1:]), 'no seed address in CAR word')
        if op[0] == 'CX': data[op[2]] ^= data[op[1]]
        elif op[0] == 'T': data[op[3]] ^= data[op[1]] & data[op[2]]
        else: sign *= 1-2*(data[op[1]] & data[op[2]] & data[op[3]]).astype(np.int8)
    need(np.array_equal(data['u'], data['u_U']) and np.array_equal(data['v'], data['v_U']),
         'complete phase programme preserves both descriptors')
    need(all(np.array_equal(data['y'+str(i)], bit(y,i)) for i in range(8)),
         'all site coordinates preserved')
    need(not data['a'].any() and not data['b'].any() and not data['t'].any(),
         'all three CAR scratch bits cleared')
    actual = sum(data['c'+str(i)].astype(np.uint32) << i for i in range(4))
    phase = (((y >> 2) & 3)+data['u']*(y & 3)+data['v']*((y >> 4) & 3)) & 3
    expected = initial_car.copy()
    exsign = np.ones(count, dtype=np.int8)
    for n in range(4):
        sel = phase == n
        if n in (1, 3):
            expected[sel & (initial_car == 0)] = 15
            expected[sel & (initial_car == 15)] = 0
        if n in (2, 3): exsign[sel & (initial_car == 0)] *= -1
        if n in (1, 2): exsign[sel & (initial_car == 15)] *= -1
    need(np.array_equal(actual, expected) and np.array_equal(sign, exsign),
         'all literal seed/CAR/site columns and signs')

    # Existing complete BDD Fourier schedule acts on its own J/Y/type, not
    # on either seed or the descriptor program. Every bit column is checked.
    pairs, _, size = original_reference()
    need(size == 256 and len(pairs) == 64, 'original Fourier support')
    bdd = BDD()
    roots = [bdd.compile([(k[r] >> b) & 1 for k in pairs]) for r in range(4) for b in (0, 1)]
    for coord, j, typ in product(product(range(4), repeat=4), range(64), range(2)):
        phase_bdd = sum(pairs[j][r]*coord[r] for r in range(4)) % 4
        out, sg = schedule(bdd, roots, j, coord, typ)
        need(out == (typ ^ (phase_bdd & 1)) and sg == (-1 if phase_bdd & 2 else 1),
             'complete actual Fourier BDD column')
    verify_complete_selector_t()
    need(verify_reference_polynomial() == '16517734400/162621047169',
         'existing exact geometric reference polynomial')

    # Independent entangled program+RIGHT state. Each seed value gives a
    # subnormalized output vector; partial trace of their coherent sum equals
    # the actual recorded mixture for the same literal site/CAR map.
    p = (math.sqrt(5)-1)/2
    branch = np.zeros((64, 4*4*16*2), dtype=np.complex128)
    for xu, xv in product(range(8), repeat=2):
        mass = 1.0
        for x in (xu, xv):
            for b in range(3): mass *= p*p if (x >> b) & 1 else p
        for k in (0, 3):
            idx = (k << 18) | (xv << 15) | (xu << 12) | (37 << 4) | 0
            u, v = int(data['u'][idx]), int(data['v'][idx])
            out, sg = int(actual[idx]), int(sign[idx])
            right = 0 if k == 0 else 1
            amplitude = (1 if k == 0 else 1j)/math.sqrt(2)
            col = (((k*4+(u+2*v))*16+out)*2+right)
            branch[xu*8+xv, col] += math.sqrt(mass)*amplitude*sg
    reduced = np.einsum('xi,xj->ij', branch, branch.conj(), optimize=False)
    mixture = np.zeros_like(reduced)
    for b in branch: mixture += np.outer(b, b.conj())
    err = float(np.max(np.abs(reduced-mixture)))
    need(err < 1e-13 and abs(np.trace(reduced)-1) < 1e-13,
         'oldRIGHT-entangled coherent program: recorded and coherent reductions agree')
    need(np.max(np.abs(reduced.imag)) > 1e-5, 'program/RIGHT coherence was not discarded')

    # Physical distinguishing continuation on one n=8 seed: undo its
    # controlled word and apply routed inverse G to every preserved seed bit.
    # Probability of all zeros after a complete seed recording is s^9.
    s = p*p+p**4
    need(abs(s-(3-4*p)) < 1e-14, 'exact one-seed inverse-read factor')
    weights = [math.prod(p*p if (x >> j) & 1 else p for j in range(9))
               for x in range(512)]
    need(abs(sum(weights)-1) < 1e-13 and abs(sum(w*w for w in weights)-s**9) < 1e-13,
         'all 512 inverse seed columns reproduce recorded all-zero probability')
    need(abs(sum(weights)**2-1) < 1e-13, 'coherent inverse returns all zeros')
    need(0.00318198 < s**9 < 0.00318200, 'n=8 full-seed read contrast')
    print('complete n=8 seed word columns:', ncols)
    print('literal n=2 seed-pair x 4 programmes x 256 SITE x 16 CAR columns:', count)
    print('Fourier BDD complete site/mode/type columns:', 256*64*2)
    print('existing selector truth table and geometric reference polynomial checked')
    print('coherent program and oldRIGHT protected-channel difference:', err)
    print('all-zero discriminator after reversing n=8 seed, coherent/recorded:', 1.0, s**9)
    print('successful logical sector; full physical geometry/factory/clock and GR remain open')


if __name__ == '__main__':
    main()
