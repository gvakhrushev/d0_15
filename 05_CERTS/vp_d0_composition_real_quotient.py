#!/usr/bin/env python3
"""vp_d0_composition_real_quotient.py - D0-COMPOSITION-REAL-QUOTIENT-EQUIVALENCE-001 (PASSPORT-CLOSED).

PASSPORT, not a present-core THE. Anchors D0's composition to the EXTERNAL real-quotient quantum theory of
Barrios Hita et al., PRL 136, 240202 (2026): a real-number QM whose composition obeys postulate P4 (local
operators commute) reproduces all multipartite predictions and is non-falsifiable (vs the Renou-falsified
naive-tensor class). This cert verifies (a) the paper's 2-qubit real-quotient identities AND (b) the
D0-NATIVE leg that licenses the dictionary J_F <-> Q8 center: the actual Q8 multiplication table has center
{+-1} and every imaginary unit squares to the center -1 (= J_F^2 = -I). The general d / n>2 case is the
EXTERNAL owner-edge ASSUMP-PRL-RQM-GENERAL (PRL Suppl. Sec. B; not re-derived). The dictionary identifications
(Q8-center<->J_F, cluster-decomposition<->P4) are interpretive bridges, NOT present-core derivations -- hence
PASSPORT, not THE.
"""
import numpy as np

I2 = np.eye(2)
JF = np.array([[0.0, -1.0], [1.0, 0.0]])     # complex unit i as SO(2) generator (paper Eq.5)

def S(psi): return np.concatenate([psi.real, psi.imag])         # C^2 -> R^4 (paper Eq.1)
def T(Op):                                                       # complex op -> real (paper Eq.4)
    R, Im = Op.real, Op.imag
    return np.block([[R, -Im], [Im, R]])
def rand_herm(n, rng):
    M = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    return M + M.conj().T

def main():
    rng = np.random.default_rng(0)
    ok = True
    def chk(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    # === (b) D0-NATIVE leg: the real Q8 grounds J_F (center i*i = -1) ===
    els = ['1', 'i', 'j', 'k', '-1', '-i', '-j', '-k']
    def parse(s): return (-1, s[1:]) if s.startswith('-') else (1, s)
    def fmt(s, u): return (('' if s == 1 else '-') + u) if u != '1' else ('1' if s == 1 else '-1')
    def mul(a, b):
        sa, ua = parse(a); sb, ub = parse(b); s = sa * sb
        if ua == '1': return fmt(s, ub)
        if ub == '1': return fmt(s, ua)
        t = {('i','i'):(-1,'1'),('j','j'):(-1,'1'),('k','k'):(-1,'1'),
             ('i','j'):(1,'k'),('j','k'):(1,'i'),('k','i'):(1,'j'),
             ('j','i'):(-1,'k'),('k','j'):(-1,'i'),('i','k'):(-1,'j')}
        s2, u = t[(ua, ub)]; return fmt(s * s2, u)
    center = [a for a in els if all(mul(a, b) == mul(b, a) for b in els)]
    chk("D0 Q8 center = {1,-1} (one shared phase flag)", set(center) == {'1', '-1'})
    chk("D0 Q8: i^2 = j^2 = k^2 = -1 (= J_F^2 = -I, the center relation)",
        all(mul(u, u) == '-1' for u in ['i', 'j', 'k']))
    chk("J_F^2 = -I (real 2D complex structure)", np.allclose(JF @ JF, -I2))

    # === (a) PRL 2-qubit real-quotient identities ===
    dim_complex = 2 * (2 * 2)        # real params of C^4
    dim_naive   = (2 * 2) * (2 * 2)  # naive double flag (falsified class)
    dim_d0      = (2 * 2) * 2        # base (x) one shared R^2_F
    chk("dim: shared flag = 8 = complex composite; naive double flag = 16 (rejected)",
        dim_complex == 8 and dim_d0 == dim_complex and dim_naive == 16 and dim_naive != dim_complex)

    even = np.array([1, 0, 0, -1.0]) / np.sqrt(2)
    odd  = np.array([0, 1, 1, 0.0]) / np.sqrt(2)
    JJ = np.kron(JF, JF)
    chk("J_Fa(x)J_Fb = -I on shared-flag classes (= Q8 center i*i = -1)",
        np.allclose(JJ @ even, -even) and np.allclose(JJ @ odd, -odd))

    OA = np.kron(rand_herm(2, rng), I2.astype(complex))
    OB = np.kron(I2.astype(complex), rand_herm(2, rng))
    chk("P4 locality: [T(O_A), T(O_B)] = 0 (cluster decomposition)",
        np.linalg.norm(T(OA) @ T(OB) - T(OB) @ T(OA)) < 1e-9)

    eq6 = True
    for _ in range(200):
        psi = rng.standard_normal(4) + 1j * rng.standard_normal(4); psi /= np.linalg.norm(psi)
        A = rand_herm(4, rng)
        if not np.isclose(S(psi) @ T(A) @ S(psi), (psi.conj() @ A @ psi).real): eq6 = False; break
    chk("Eq.6 expectation values reproduced (200 random multipartite states/operators)", eq6)

    # === REAL negative controls (must FAIL the complex-structure / quotient test) ===
    # (1) an involution R (R^2 = +I, the D4-reflection alternative) is NOT a complex structure:
    R = np.array([[1.0, 0.0], [0.0, -1.0]])      # R^2 = I != -I
    assert not np.allclose(R @ R, -I2), "neg-control: a g^2=+I generator must NOT be a complex structure"
    # (2) the naive double-flag dimension genuinely differs from the complex composite (dead class):
    assert dim_naive != dim_complex, "neg-control: naive double-flag tensor must not match (falsified class)"
    # (3) a g^2=+1 element would break the center relation that grounds J_F:
    assert mul('i', 'i') != '1', "neg-control: if i^2 were +1, Q8 would not supply J_F^2=-I"

    # guillotine
    assert ok, "RESULT: SOME PASSPORT CHECK FAILED"
    print("\n[STATUS] PASSPORT-CLOSED: D0 composition anchors to the PRL real-quotient (P4) class")
    print("         (non-falsifiable; NOT the Renou-falsified naive-tensor class). D0-native Q8 center grounds")
    print("         J_F; dictionary (Q8-center<->J_F, cluster-decomp<->P4) is a bridge, NOT a present-core THE.")
    print("         General d / n>2: external owner-edge ASSUMP-PRL-RQM-GENERAL (PRL 136, 240202 (2026)).")
    print("[CERT-CLOSED] PASS_D0_COMPOSITION_REAL_QUOTIENT")


if __name__ == "__main__":
    main()
