# Exact scalar ports and adaptive stopped-price extension

20 October 2026. Read-only extension of the stopped Golden result at `f22c1864`, consuming the whole-J2 three-query cleanup at `4867b6d4`. No new physical task, action, primitive admission or Book information cut is selected. The fixed-k stopped minimum for `5<=T0<=50` is an input proved in the existing owner.

## 1. Exact scalar port effects hold off the null stratum

Use the existing complete output

```
VJ = f0 |0>J + f1 |1>J - 2t^2 |1>QWJ,
f0=1-2t^2,     f1=2t(1-t^2),
J*QWJ=0,      (QWJ)*(QWJ)=(1-t^2)I.
```

After a fixed Golden postrotation `G^k=[[c,-s],[s,c]]`, the two full port maps are exactly

```
K0=(c f0-s f1)J + 2s t^2 QWJ,
K1=(s f0+c f1)J - 2c t^2 QWJ.
```

Consequently, on the entire real compression chart,

```
K_b*K_b=q_b(t)I,
q1=[s f0+c f1]^2+4c^2 t^4(1-t^2),
q0+q1=1.
```

The joint effects of `(port,clean/nonclean)` are scalar as well. Total nonclean probability is exactly `r(t)=4t^4(1-t^2)`, independent of k and of the normalized incoming logical state, including arbitrary entanglement with oldRIGHT and all preceding work.

Thus fresh-work repetitions with one fixed k have an EXACT geometric coarse port stop law off Sigma. Conditional logical states need not be IID or restored after nonclean outcomes: scalar effects make the next port probability independent of those states. Fine work-address labels need not be independent or identically distributed. No previous computational workspace or protected record is reversed or erased.

This strengthens the earlier first-jet justification without assuming free input preparation. The supplied clean embedding, moving field query, fixed paid prefix and original preparation/admission hypotheses remain in force.

## 2. Complete fine-pointer entropy has a uniform per-attempt bound

At each live node of the retained history, let the complete recorded trial outcome be `(b,w)`, where b is the port and w is the finite fresh-work address. The conditional input can be arbitrary. There is one clean address and at most `N_g` nonclean addresses. Since nonclean probability is always r,

```
0 <= beta_h := H_phi(w | b, full previous history=h)
   <= H_phi(w | full previous history=h)
   <= B(t):=h_phi(r(t))+r(t)log_phi N_g.
```

Here `B(t)=O(t^4 |log|t||)` at zero, uniformly in history, logical preparation and postrotation k. The report word and clock are deterministic functions of the actual trial choices and outcomes, and add no independent conditional Shannon entropy.

The same bound includes the retained quantum oldRIGHT R when the declared information is the classical-quantum pointer tape together with R. Subtract its common fixed initial entropy baseline `S(R)/ln(phi)`. Scalar port effects imply that b is independent of conditional R at each history, so `H_phi(b|h,R)=H_phi(Bern(q_k))`. The remaining increment is then `beta_h=H_phi(w|b,h,R)`. Since w is classical, `0<=beta_h<=H_phi(w|b,h)<=B(t)`. The ordinary classical-pointer case is obtained by omitting R. No replacement of an arbitrary coherent work entropy by a Shannon entropy is made.

For one fixed k, the exact port stop law has expected attempts `1/q_k(t)`. The variable-length entropy chain rule therefore gives

```
H_phi(complete stopped pointer tape)
 = H_phi(geometric stopped port tape) + H_extra,
0 <= H_extra <= B(t)/q_k(t).
```

All failures and all work outcomes remain. In a neighborhood where `q_k(0)>0`, this difference has zero first derivative at zero. The entropy difference is understood relative to the fixed oldRIGHT baseline if it is included. A different coherent information cut, a moving oldRIGHT marginal, a paid work label, or another independently charged ledger requires its actual term.

## 3. Exact admissible adaptive family

The declared task remains: stop at the first recorded port1. Before each nonhalted trial, a deterministic policy chooses an integer `k(h)>=0` using only the already retained history h. It may read previous fine-work labels; it cannot use unrecorded randomness or assume an external value of t.

The actual trial consists of the same supplied fresh-work query/cleanup, k original Golden rotations, and the literal 0/10 reporter. Unit G cost is fixed here. The pre-report charge is `T0+k` on every executed trial. The policy must halt almost surely and have finite expected total execution cost on the parameter point being compared. The policy chooses only k: no other field or logical measurement, altered query/reference, abort rule, reset of previous work, or outcome postselection is admitted.

Deterministically calculated scheduling labels are functions of the retained history and add no independent pointer entropy. Any additional actual scheduler execution cost is included and assumed nonnegative; setting it to zero gives a lower bound. The fixed k=2 controller is assumed already included in its stated T0. Additional field-dependent costs or correlated information rebates are outside this theorem.

Let `s_h` be the probability of reaching live node h, let `q_h=q_{k(h)}(t)`, and write

```
D(q)=D_phi((1-q,q)||(p,p^2)),
a_k(t)=T0+k+D(q_k(t)).
```

All following prices omit only the same fixed oldRIGHT entropy baseline, if included. The actual per-node expected reporter length is `1+q_h`. The identity
`1+q-H_phi(Bern(q))=D(q)` gives the exact total pointer-price ledger

```
S_policy = sum_h s_h [a_{k(h)}(t)-beta_h] + C_scheduler.       (1)
```

Finite expected cost implies finite expected attempt count and finite full pointer entropy, so the chain rule involves no subtraction of divergent quantities. Histories of differing lengths are included in the tree sum.

## 4. On Sigma: no deterministic adaptive policy beats fixed G²

At t=0, r=B=beta_h=0. All fine-work records are clean, so reachable adaptive histories reduce to the number of previous failures. For k>=1 the existing Golden irrationality argument gives `0<q_k(0)<1`. Set

```
R_k=(T0+k+D(q_k))/q_k.
```

The probability of halting at a live node is `w_h=s_h q_h`; almost-sure stopping gives `sum_h w_h=1`. Nodes using k=0 have q=0 and contribute strictly positive cost without any halting probability. Therefore

```
S_policy
 = sum_{h:q_h>0} w_h R_{k(h)}
   + sum_{h:q_h=0} s_h a_0
   + C_scheduler
 >= min_{k>=1} R_k.                                      (2)
```

The existing fixed-k theorem proves the unique minimizer is k=2 for `5<=T0<=50`. Equation (2) therefore extends that minimum to **every deterministic history-adaptive policy in the stated family**, including unbounded schedules with finite expected cost.

Equality requires k=2 at every reached positive-probability node and no extra scheduler cost. Since every finite failure history under G² has positive probability, a schedule that changes k after any finite number of failures is strictly more expensive. Policies can differ on zero-probability fine-work histories at Sigma.

There is no uniform positive gap separating all alternative policies: one can postpone a different action to an arbitrarily unlikely late failure. Accordingly a uniform policy-gap argument must not be used to differentiate the optimized value.

## 5. The complete optimized value nevertheless has the same first source

Let `V(y,rho)` be the infimum of the complete prices (1) over this adaptive family, where y contains the original field/query variables, `t=t(y)`, and rho is the normalized logical/reference preparation with the prescribed fixed oldRIGHT marginal. Off Sigma, fine-work adaptation and entropy may depend on more than t and may change the exact best policy. We do not claim scalarization of the full value; we need only a uniform bound.

Let

```
R(t)=min_{k:q_k(t)>0} a_k(t)/q_k(t).
```

For any admissible policy, the same terminal-node weighting as (2), now allowing arbitrary fine-work histories, gives

```
sum_h s_h a_{k(h)}(t) >= R(t).
```

As `D>=0`, every `a_k>=T0`. For sufficiently small t with `B(t)<T0`, (1) therefore implies

```
S_policy
 >= (1-B(t)/T0) sum_h s_h a_{k(h)}(t)
 >= (1-B(t)/T0) R(t).                                  (3)
```

This bound remains valid with nonnegative additional scheduler costs. It does not assume a uniform bound on each policy's possible running time or a policy gap.

The fixed-action minimum is locally stable. Indeed `a_k/q_k>=T0+k`, whereas the fixed k=2 value is bounded near zero. Only finitely many k can compete. Their strict gaps at t=0 persist by continuity; k=0 has `q_0(t)->0` and its ratio diverges. Thus in a neighborhood of zero,

```
R(t)=R_2(t).
```

The admitted fixed k=2 policy, with its complete controller already included in T0 and no extra unknown price, supplies `V(y,rho)<=R_2(t(y))`, because its extra fine-pointer entropy is nonnegative. Combining with (3),

```
(1-B(t(y))/T0) R_2(t(y)) <= V(y,rho) <= R_2(t(y)),
V(y,rho)=R_2(t(y))+O(t(y)^4 |log|t(y)||).                (4)
```

The estimate is uniform over normalized logical preparations on the fixed finite carrier and over the supplied local query chart. Since `t(y0)=0` and `t(y)=O(||y-y0||)` for the smooth original query, the remainder in (4) has zero full Fréchet first derivative at `(y0,rho0)`. Thus the optimized complete value has exactly the fixed G² first source at every point of Sigma, including all vertical query and normalized preparation directions, even if different policies become favorable on rare nonclean histories away from it:

```
dV|Sigma
 = -(T0-3)/(2p^(3/2)) dt
 = -(T0-3)/(2p^(3/2)) gamma_h dJ2.
```

The statement transports all original 16+24+2 first-source rows and their coupling under the existing whole-J2 and remaining-ledger hypotheses. It does not identify field Hessians or establish a field minimum. The value infimum need not be attained off Sigma for this first-jet conclusion.

## 6. Review of the latest stopped owner

The stopped probability law, Golden Kraft identity, `D(q)/q` code identity and derivative formula are correct. At T0=5, the correct coefficient is `-p^(-3/2)`, agreeing with the document.

The original checker at f22c1864 has a factor-two typo in its final expected target: it evaluates `T2=7` but compares against `-2/p^(3/2)`. The correct independent target is `-(5-3)/(2p^(3/2))=-1/p^(3/2)`. This is a checker expected-value defect, not a failure of the document's source theorem.

The real full prefix T0 and the primitive price of G are still unbound. The window `5<=T0<=50` is not certified for the supplied 46-coin/address/reference/query compilation. Its actual paid word can be much longer; neither three query calls nor a compound-oracle count supplies T0. The stopped task itself is explicitly prospective and is not yet derived as compulsory from M1.

The earlier finite bit-continuation theorem in `PROSPECTIVE_SELECTION_4867.md` is an alternative task/ledger. It must not be added to this stopped price or used to replace its random cumulative prefix. The stopped continuation is state-dependent and generally infinite-horizon; its actual expected prefix cost already generates the derivative in the displayed formula.

## 7. Verification boundary

`check_adaptive_stopping.py` checks exact symbolic port-effect normalization and scalar coarse probabilities, the Golden derivative coefficient, and finite adaptive schedules with an infinite fixed tail whose value is summed analytically. It checks the Bellman identity and terminal-node weighted ratio identity without discarding the tail. It prints a read-only result by default; optional `--output PATH` writes only that requested file. The infinite-policy theorem and optimized-value estimate are proved above; finite schedules alone do not certify them.
