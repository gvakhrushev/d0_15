# The fixed record engine has no uniform finite-resolution memory

**Exact scoped consequence, 16 October 2026.** The existing closed record
engine has infinitely many pairwise distinct exact states, but their mutual
separation has infimum zero. Every finite level of the constructed isometric
hereditary refinement, conditional on its declared child pairing, preserves
that arbitrarily close pair structure. Therefore exact coefficient growth
in this fixed-carrier engine does not by itself establish robustly readable
memory or physical expansion.

This is a limit on the current 16-slot engine plus its existing inheritance
map. It does not rule out a state-dependent refinement mechanism that creates
new child distinctions; deriving such a mechanism and its detector remains a
separate native obligation.

Consumed owner pins: engine `7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9`,
checker `7d4cd83521729b780758c8559b9168668f6aac8437f89c9b8652b1141f2692f8`,
certificate `2c6060cc856083c4dc60ee67b8b2bfca1a9a4967f4992bcfdc3b5ef6c604d5ce`,
and proof `36eaeb8617630acaeace297fa64e7b8c33b92fc4824133a2b8e3515c4c79520a`.

## Proof on the actual seed orbit

Consume the actual blank seed, all-time domain, and exact rotation formula in
[`A4D_NATIVE_CLOSED_RECORD_ENGINE.md`](A4D_NATIVE_CLOSED_RECORD_ENGINE.md),
whose checker pins the engine and its inputs. At every even return after the
second tick, the lower state is the same pair `A`, while the only nonzero
higher pair is
\[
u_k=R^k e_2,\qquad
R=\begin{pmatrix}r&-s\\s&r\end{pmatrix}\in SO(2),\qquad
r=2p-1,\quad s=2ap.
\]
The existing owner proves `R` has infinite order and that the complete
seed-orbit states are pairwise distinct.

Because `SO(2)` is compact, the sequence of powers `R^n` has a convergent
subsequence `R^(n_j) -> L`. Set `d_j = n_(j+1) - n_j > 0`. Then
\[
R^{d_j}=(R^{n_j})^{-1}R^{n_{j+1}}\longrightarrow I.
\]
The gaps `d_j` tend to infinity after passing to this subsequence: if
infinitely many gaps were bounded, some fixed positive gap `d` would repeat
infinitely often and force `R^d = I`, contradicting infinite order. Hence
\[
0<\|m_{2+2d_j}-m_2\|
 =\|(R^{d_j}-I)e_2\|\longrightarrow0.
\]
Strict positivity follows because a planar rotation fixing a nonzero vector
is the identity. Thus the orbit has pairwise distinct exact vectors, but no
positive lower bound separates all of its histories.
The same conclusion holds for the normalized seed; normalization only
multiplies these distances by a fixed positive constant.

More generally, for any `L`-Lipschitz current-state readout `F`,
\[
\|F(m_{2+2d_j})-F(m_2)\|
 \le L\|m_{2+2d_j}-m_2\|\longrightarrow0.
\]
Such a detector cannot assign a uniform positive readout margin to every
distinct tick of this orbit.

## What the current archive refinement does

The owned adjacent pullback `J_n` maps a field to its pullback along `pi_n`,
injecting a coarse field into the fine carrier by copying each parent value
to its children. The closed
record owner constructs a normalized map `J_n^iso` that is an
isometry under its declared child weights and commutes with the local engine;
its physical pairing remains conditional. For any finite tower composition
`J^iso`,
\[
\|J^{\rm iso}m_{2+2d_j}-J^{\rm iso}m_2\|
 =\|m_{2+2d_j}-m_2\|\longrightarrow0.
\]
It also remains in the inherited subspace: for one scalar component,
\[
\dim\operatorname{im}J_n=|X_n|<|X_{n+1}|
 =\dim\mathbb R^{X_{n+1}}.
\]
Thus copying increases the number of carrier sites but neither creates new
independent child values nor improves the separation of the recurrent record
states in the owned pairing. The unnormalized counting pullback is not an
isometry; its level-dependent norm factor is not an owned bit-capacity or
detector law.

This separates two facts that must not be conflated:

- The exact algebraic coefficient codec can require unboundedly many bits as
  the orbit advances.
- The actual Fock vectors stay on a bounded sphere and recur arbitrarily
  close. An exact symbolic distinction is not a uniform finite-resolution
  distinction.

The result does not say that the current deterministic update loses its
mathematical state: the states remain distinct and the local observer sign
continues to have the all-time margin proved by the owner. It says that a
fixed-resolution current-state readout cannot robustly decode every past
tick from this 16-slot carrier with a uniform margin within the stated
Lipschitz readout class. A detector that itself
gains resolution could change that conclusion only if a native rule couples
the record to newly distinguishable child degrees and carries the complete
action, metric/link variations, and refinement equations. No such trigger or
new cell state is introduced here.

## Consumer in the gravity route

For Front A, the common preparation must explain how retained distinctions
become detector/readout data on the `(q,D,b,m)` carrier and how refinement
adds admissible independent directions. The existing local engine and
hereditary pullback do not supply that transition. This narrows the next
question to the already-owned action/preparation interface: what term makes
the child-complement modes physical and resolves the exact recurrence without
an externally scheduled depth, a fitted source, or a new memory postulate?

The result is not a global no-go: it applies to the fixed-carrier orbit and
the existing isometric inheritance, not to every possible native refinement
or every state-dependent matter/link law. It adds no Lean declaration and
does not close a source, Ward identity, curved root, recovery theorem, or GR.
