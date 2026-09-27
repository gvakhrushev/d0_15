import numpy as np, sympy as sp
exec(compile(open('a4d_fugu_p1p2_check.py').read(),'base','exec'))
print("symbol built; HAB",HAB.shape,"HAQ",HAQ.shape, flush=True)
zs_=[z[0],z[1],z[2],z[3]]
np.savez('sym_symbolic.npy.npz')  # placeholder
# numeric substitution per orbit
HAB_l = sp.lambdify(zs_, HAB, 'numpy')
HAQ_l = sp.lambdify(zs_, HAQ, 'numpy')
np.save('orbits_ids.npy', np.array(ORBITS))
for n,ids in enumerate(ORBITS):
    vals=[rt(ids[j]) for j in range(4)]
    A=np.array(HAB_l(*[complex(v) for v in vals]), dtype=complex)
    C=np.array(HAQ_l(*[complex(v) for v in vals]), dtype=complex)
    np.savez(f'num_{n}.npz', A=A, C=C, ids=np.array(ids))
    print("saved orbit",n,ids, flush=True)
print("DONE")
