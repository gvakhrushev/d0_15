# The recorded A9 source has an all-level positive-state refinement

15 October 2026. Constructive continuation of the fixed-path AF/CAR state
test. This closes the positive-state/readout refinement step for the existing
recorded A9 state under the owned Jones maps. Physical execution, joint field
variation, source/Ward identity, curved roots, and GR remain open.

## The actual recorded state

The level-three CAR weld and right-module path frame give a normalized
20-component source row \(v\), with
\[
v_0=p,\qquad v_3=p-1,\qquad v_{15}=v_{18}=ap,
\]
and all other entries zero, where \(p^2+p=1\), \(a^2=p\), and both roots are
positive. Let \(S:\mathbb C^{20}\to\mathbb C^{89}\) be the owned A3-to-A9
path frame, \(y=Sv\), and let \(z\) be the first normalized column of the
owned A3-to-A9 Jones frame. In the regular A9 GNS space the recorded vector
is \(X=yz^*\), in the M89 block and zero in M55. The exact norm is
\(\|X\|_{2,\tau_9}^2=p^{10}\), and its induced state on the observable
algebra \(A_9=M_{89}\oplus M_{55}\) is
\[
\omega_9(A_+,A_-)
 =\frac{\tau_9(X^*(A_+,A_-)X)}{\tau_9(X^*X)}
 =y^*A_+y.
\]
It is positive and normalized. Its existing native current readout is
\((1,2ap,0,0)\), with Lorentz norm squared \(p^6\). It differs from the
canonical conditional Jones-vector state, whose spatial current is zero.
The construction below keeps the actual recorded state; it does not force
that mismatch away.

## The owned conditional expectation extends this state

At every AF level write
\(A_n=M_{d_n}\oplus M_{d_{n-1}}\), with the existing inclusion
\[
\alpha_n(A,B)=(\operatorname{diag}(A,B),A).
\]
The owned internal Jones transport is
\[
\widehat\alpha_n=\operatorname{Ad}_{R_n}\circ\alpha_n,
\qquad
\widehat C_n=C_n\circ\operatorname{Ad}_{R_n^*},
\]
where \(R_n\) is the already constructed full unitary and the actual
trace-adjoint conditional expectation is
\[
C_n\!\left(\begin{bmatrix}X&U\\V&Y\end{bmatrix},W\right)
       =(pX+p^2W,Y).
\]
The block sizes are \((d_n,d_{n-1})\) at level n and
\((d_n+d_{n-1},d_n)\) at level n+1. Since \(p,p^2>0\) and \(p+p^2=1\),
principal compression and positive averaging show that \(C_n\) is unital,
completely positive, and bimodular over the included algebra. The owned
identity \(C_n\alpha_n=I\) therefore gives
\(\widehat C_n\widehat\alpha_n=I\).

For any positive normalized state \(\omega_n\) on \(A_n\), set
\[
\omega_{n+1}=\omega_n\circ\widehat C_n.
\]
It is again a positive normalized state, and
\(\omega_{n+1}(\widehat\alpha_n(A))=\omega_n(A)\). Iterating this actual
trace-adjoint map gives a compatible state on the full AF inductive limit.
Because \(\widehat\alpha_n\) is a *-homomorphism, every polynomial readout
in the transported record, cuts, and CAR current is preserved, including
noncommuting products. This argument applies to the actual A9 source state
and does not require its vector to lie in the canonical Jones corner.

For the first step A9 to A10, the extension is explicit. Put
\(\rho_9=yy^*\oplus0_{55}\). The ordinary trace densities of
\(\omega_{10}=\omega_9\circ\widehat C_9\), in the A10 blocks M144 and M89,
are
\[
\begin{aligned}
\rho_{10,+}&=R_+\operatorname{diag}(p\,yy^*,0_{55})R_+^*,\\
\rho_{10,-}&=R_-(p^2yy^*)R_-^*.
\end{aligned}
\]
Each is a positive rank-one matrix; their traces are p and p squared, so
their total trace is one. The exact checker verifies both densities, their
normalization and spectral weights, and preservation of the current
*-algebra through all quadratic words.

## Scope boundary

This resolves one concrete obstruction in the state leg: failure to match
the canonical conditional vector does not prevent the actual recorded state
from having a positive, all-level, readout-preserving extension under the
already owned AF/Jones transition. The result uses no new state selector or
physical postulate.

The extension is a mathematical state on the inductive limit. It does not
prove that the internal unitary \(R_n\) is physically executable, derive a
physical clock or preparation law, map the current algebra to the joint
\((q,D,b,m)\) fields, produce their tangent, or establish the source,
stationarity, a curved solution, or Einstein dynamics. Those are the next
unsolved arrows toward the requested OTO/GR target.

## Reproduction

From the repository root:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_afcar_positive_state_refinement_check.py
```

The exact receipt pins the A9 weld and current owner, the whole-blank-family
test, the actual Fibonacci conditional expectation and the all-level Jones
transport. It checks the recorded vector and source moments at A9 and the
explicit positive density at A10. It does not upgrade the physical or GR
status of those owners.
