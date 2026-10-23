# Complete-Povm information gain has zero action on the owned A9 blank family

15 October 2026. Exact KILL-FIRST comparison of the newly certified complete
information-gain functional with the actual level-nine AF/CAR state. This
rules out that functional as a nonzero source on this preparation family if
the whole A9 POVM algebra is taken as physically available. It does not select
the physical Info contract or close the native source/GR problem.

## The actual state at level nine

The owned level-three CAR weld and A3-to-A9 path frame send every normalized
blank \(B(x,y)\), \(x^2+y^2=1\), to a normalized vector \(u(x,y)\) in the
M89 summand of \(A_9=M_{89}\oplus M_{55}\). The resulting state on the
defining AF module is
\[
\sigma_9(x,y)=|u(x,y)\rangle\langle u(x,y)|\oplus0_{55}.
\]
It is pure for the whole family. At the golden source, its already checked
native-current readout is \((1,2ap,0,0)\), with nonzero spatial component
\(2ap\) and Lorentz norm squared \(p^6\).

The owned central Perron-Frobenius reference on this same finite algebra is
\[
\mu_9=p^{10}I_{89}\oplus p^{11}I_{55},\qquad
89p^{10}+55p^{11}=1.
\]
Its code-cost observable is \(-\log_\varphi\mu_9
=10I_{89}\oplus11I_{55}\). Therefore the expected cost of every state in
this normalized blank family is exactly 10.

## Exact value of the complete-maximal-gain contract

The new operational-gain theorem gives, when Info is the maximum over all
POVMs in the complete finite algebra,
\[
I_{\max}(\sigma_9;\mu_9)
 =\frac{D(\sigma_9\|\mu_9)}{\log\varphi}.
\]
Here \(S_{vN}(\sigma_9)=0\), and \(\mu_9\) is the scalar \(p^{10}) on the
support of \(\sigma_9\). Thus
\[
D(\sigma_9\|\mu_9)=-\log(p^{10})=10\log\varphi,
\qquad I_{\max}=10.
\]
This maximum is attained by the state projector
\(E_1=|u\rangle\langle u|\oplus0\) and its complement
\(E_2=(I_{89}-|u\rangle\langle u|)\oplus I_{55}\). Their process
probabilities are \(q=(1,0)\), and their reference probabilities are
\(r=(p^{10},1-p^{10})\), so the measured gain is also 10.

Consequently, for the complete-maximal-gain contract,
\[
\mathbb E[\mathrm{Cost}]-I_{\max}=10-10=0
\]
identically on the whole normalized \((x,y)\) blank family. Every tangent
within this family has zero derivative of this candidate action, while the
golden source state has a nonzero native-current readout. It therefore cannot
identify that current as a variation source along the blank-family tangents.
This says nothing about metric/connection tangents that leave this family.

## What this excludes

The exact boundary is the **complete maximum over all algebraic POVMs of A9**.
The state-projector test is mathematically admissible in that maximum; the
repository has not proved that the physical native history can execute this
test. The result does not reject the owned branch-outcome Info cocycle, whose
tests are tied to the actual direct/return instrument and whose physical
binding remains conditional. A restricted physical test algebra can have a
smaller gain and a different Cost−Info source.

This is not a no-go for all native information, all preparations, or all of
D0. It does sharpen the critical path: the full-A9 maximum is not the missing
nonzero stress for the existing golden blank. The next source test must use
the actual admitted branch/readout algebra, then pull its joint preparation
and instrument derivative into \((q,D,b,m)\). No new action, selector,
measurement postulate, or claim status is introduced.

## Reproduction

From the repository root:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_afcar_max_gain_action_check.py
```

The checker pins the replayed complete-gain theorem, its exact/interval and
hostile receipts, and the actual A9 source-state certificates. It reconstructs
the full blank family, proves its pure-state projector identity on
\(x^2+y^2=1\), and evaluates the attaining POVM and Cost−Info value using exact
golden relations. It does not promote physical POVM availability or a GR
source.
