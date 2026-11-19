"""Literal native Z routes and full intermediate G-mark contrast.

The local work operators and terminal code-CQ functional here are conditional
models, not an identification with the original D0 Cost-Info source.
"""
import json
import math
import numpy as np
from check_source_price import load_control


def need(ok, message):
    if not ok:
        raise AssertionError(message)


def mul(a, b):
    return np.einsum('ij,jk->ik', a, b, optimize=False)


def one(matrix, wire):
    result = np.array([[1.]], dtype=complex)
    for j in range(3):
        result = np.kron(result, matrix if j == wire else np.eye(2))
    return result


def cx(control, target):
    result = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        bits = [(i >> (2-j)) & 1 for j in range(3)]
        bits[target] ^= bits[control]
        j = sum(bit << (2-k) for k, bit in enumerate(bits))
        result[j, i] = 1
    return result


def metric(mat):
    return float(np.max(np.abs(mat)))


def main():
    # Wires P,H,port.  The dirty port and any independent Spin/RIGHT remain
    # explicit in the input map; SourceI^2 = Z_port is its owned interface.
    p = (math.sqrt(5)-1)/2
    a = math.sqrt(p)
    theta = math.asin(p)
    ell = math.log(1/p)
    G = np.array([[a, -p], [p, a]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.diag([1., -1.]).astype(complex)
    I = np.eye(2, dtype=complex)
    ne, digest = load_control()
    source = ne.Gate('SourceI', (0, 1, 2))
    specification = ne.Execution(3, (), (), (source,), profile=ne.G_CX_SOURCE_I,
                                 source_port=0, source_spin=(1, 2))
    source_matrix = np.array(ne.gate_matrix(specification, source, max_qubits=3,
                                           max_expanded_stages=10), dtype=complex)
    need(metric(mul(source_matrix, source_matrix)-np.kron(Z, np.eye(4))) < 1e-14,
         'pinned literal SourceI squared is Z on dirty port and identity on Spin')
    gp = one(G, 1)
    c_hp, c_ph = cx(1, 2), cx(2, 1)
    route = [c_hp, c_ph, c_hp, one(Z, 2), c_hp, c_ph, c_hp]
    zphysical = np.eye(8, dtype=complex)
    for gate in route:
        zphysical = mul(gate, zphysical)
    need(metric(zphysical-one(Z,1)) < 1e-14, 'route implements Z on H and preserves dirty port')
    born = np.kron(np.eye(2), np.kron(np.array([[a], [p]]), np.eye(2))).astype(complex)
    initial = mul(cx(0, 1), born)
    basis = {'identity': I, 'x': X, 'y': Y, 'z': Z, 'positive_2P0': I+2*(I+Z)/2,
             'positive_2P1': I+2*(I-Z)/2}
    cuts = {name:one(mark,1) for name,mark in basis.items()}
    p1 = (I-Z)/2
    hproj = one(p1,1)
    tests = []
    for q, turns in [(19,2), (66,7), (613,65)]:
        epsilon = q*theta - 2*math.pi*turns
        dq = 2*a*p*math.sin(4*epsilon)
        def run(plus):
            v = initial.copy()
            paid = {name:np.zeros((4,4),dtype=complex) for name in basis}
            def zroute(vv):
                for gate in route:
                    vv = mul(gate, vv)
                return vv
            for _ in range(2):
                if not plus:
                    v = zroute(v)
                for _ in range(q):
                    v = mul(gp,v)
                    for name,mark in cuts.items():
                        paid[name] += mul(v.conj().T, mul(mark,v))
                v = zroute(v)
                if plus:
                    v = zroute(v)
            effect = mul(v.conj().T, mul(hproj, v))
            need(metric(mul(v.conj().T,v)-np.eye(4)) < 2e-12, 'full old input isometry')
            return paid,effect
        plus, ep = run(True)
        minus, em = run(False)
        need(metric(ep-em-dq*np.eye(4)) < 3e-12,'terminal H effect on all P,dirty port columns')
        analytical = {
            'identity':0.,
            'x':4*a*math.sin(2*epsilon)*math.cos(theta+2*epsilon),
            'y':0.,
            'z':-4*a*math.sin(2*epsilon)*math.sin(theta+2*epsilon),
        }
        maxerr=0.
        contrast={}
        for name in ('identity','x','y','z'):
            delta=plus[name]-minus[name]
            expected=analytical[name]
            err=metric(delta-expected*np.eye(4))
            maxerr=max(maxerr,err)
            need(err < 2e-9,'complete old input effect for '+name)
            contrast[name]=float(np.real(np.trace(delta)/4))
        work0 = float(np.real(np.trace(plus['positive_2P0']-minus['positive_2P0'])/4))/dq
        work1 = float(np.real(np.trace(plus['positive_2P1']-minus['positive_2P1'])/4))/dq
        predicted = math.sin(theta+2*epsilon)/(p*math.cos(2*epsilon))
        need(abs(work0+predicted)<1e-9,'positive mark P0 exact work secant')
        need(abs(work1-predicted)<1e-9,'positive mark P1 exact work secant')
        d = a*p*math.sin(4*epsilon)
        qplus=.5+d
        qminus=.5-d
        def h(t):
            return -t*math.log(t)-(1-t)*math.log(1-t)
        def f(t):
            return 1+t-h(t)/ell
        code=(f(qplus)-f(qminus))/dq
        need(abs(code-1)<1e-12,'true full registered pure-input code-CQ secant')
        residual=work0+code
        expected_residual=-(a/p)*math.tan(2*epsilon)
        need(abs(residual-expected_residual)<1e-9,'conditional cancellation residual')
        # Independent P preparation derivative of the same normalized CQ secant.
        # Vary the P=1 Born probability at the same input and all paid marks fixed.
        qprime=p**3*math.cos(4*epsilon)
        derivative=qprime*math.log(qplus/qminus)/(d*ell)
        need(derivative>0,'independent preparation row survives')
        tests.append({'q':q,'turns':turns,'epsilon':epsilon,'delta_q':dq,
          'g_stages_each':2*q,'g_mark_max_full_input_error':maxerr,
          'basis_work_contrasts':contrast,'K0_work_per_delta_q':work0,
          'K1_work_per_delta_q':work1,'code_CQ_per_delta_q':code,
          'K0_plus_code_per_delta_q':residual,
          'independent_P_derivative_of_code_secant':derivative})
    derivative_limit=4*p**3/ell
    need(abs(derivative_limit-1.9622791062588716)<1e-12,'independent-row analytic value')
    print(json.dumps({'status':'PASS','scope':'conditional local mean G-work and specified CQ code; not selected Book03 cost',
      'native_source_sha256':digest,'literal_SourceI_squared_verified_on_port_and_spin':True,
      'route':'3 CX, SourceI^2 on port, 3 CX',
      'all_added_G_marks_pulled_back_to_old_P_dirty_port_are_scalar_differences':True,
      'arbitrary_oldRIGHT_allowed_by_tensor_identity':True,
      'same_K0_and_K1_work_spectrum':[1,3],
      'limit_K0_work_per_delta_q':-1.0,
      'limit_K1_work_per_delta_q':1.0,
      'limit_independent_P_derivative_of_code_secant':derivative_limit,
      'book03_tariff_selected':False,'full_preparation_euler_rows_closed':False,
      'GR_closed':False,'examples':tests},indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
