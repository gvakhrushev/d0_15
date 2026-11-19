# Book03 J from alternating native P/Q tests: eliminate the artificial sqrt(F) instrument

22 Oct 2026. Existing scientific Draft PR #334. **Exact operational algebra** consuming original F=P U†Q U P (Q=I-P), original U and its inverse, original Golden p and zeta=2^-20. Does not modify Book03 action, choose vertex Info, or prove G0 physical permission for controlled projection/clock/reset.

## Exact operator compiler

Let A=Q U P on original Hilbert space and A†=P U† Q; F=A†A, 0≤F≤I_P. Start on P with arbitrary density σ, Tr σ=1. Run a chronological alternating *successful* step:
P→Q: apply U, measure {Q,P}, keep if Q; Q→P: apply U†, measure {P,Q}, keep if P; repeat. After n individual successful projections the full Kraus chain is
K_(2m)=F^m on P, K_(2m+1)=A F^m from P to Q.
Consequently K_n†K_n=F^n **for EVERY n**, including parity, all input states, and every zero return mode. **Do not** count the whole two-test cycle as one success: that would incorrectly give F^(2n), not F^n. A failed projection is permanently logged and ends the current attempt; no projection failure is erased, no reprepare of old data is needed. The register resides alternatively on P/Q and remains in its true projected state after every keep.

Before EACH alternating test, generate a fresh independent fair bit using the ORIGINAL Golden Bernoulli p and p²: sample two old Golden letters, restart on equal pair, select 0 or 1 by AB/BA order; each unequal pair has probability p³ and the expected number of original letters per fair bit is 1/p³=2+sqrt5. Keep all tied-pair outcomes in the recorded work tape. Generate 20 such bits and continue only if ALL are 1; this implements EXACT zeta=2^-20. A rejected controller bit is a terminal STOP outcome with an append-only known flag, BEFORE invoking U or U†. A selected U/projection then keeps only on its appropriate Q/P result and logs the complementary measurement on failure. This controller is stochastic and almost surely terminating with unbounded max clock; a capped physical version retains a nonzero unresolved flag and requires explicit convergence/source bounds.

The effect for survival of n COMPLETE gated alternating tests is
S_n = zeta^n K_n†K_n = (zeta F)^n.
The two mutually exclusive stopping categories at the next step, controller failure and tested-projection failure, have aggregate effect
S_n - S_(n+1) = (zeta F)^n(I_P-zeta F).
Hence the number N of genuinely successful P/Q projection tests before terminal stop satisfies for ANY initial density σ on P:
Prσ(N=n)=Tr σ(zeta F)^n(I_P-zeta F),
Prσ(N≥n)=Tr σ(zeta F)^n.
They sum to 1 exactly; all controllers, projection failures, final alternatives and parity/timing are retained, with no postselected normalization. On the physically supplied maximally mixed P/d (purified using a real oldRIGHT register if prepared), the exact original Book03 feedback is
**J=-Tr_P ln(I_P-zeta F)=d E_[P/d] H_N.**
This is the SAME complete stopped-harmonic Book J of the preceding result, NOW without implementing sqrt(F) or sqrt(I-zeta F) as native field-dependent operators. All genuine parameter derivatives of J follow by differentiating this fixed compiled history sum, if actual U(y),P(y),clock/controller and input are physically admitted as one differentiable execution.

**Exact native paid-clock accounting (not optional).** For fixed native expected cost c_fb of generating one fair bit (including all old Golden ties/attempts) and tests of one U/projection pair with actual variable clock cost c_test(n), the expected number of generated fairness bits is 20 E(N+1), with E(N+1)=Tr σ (I-zeta F)^-1≤1/(1-zeta). Thus mean original Golden primitive letters for 20 bits/test are 20/p³ *Tr σ (I-zeta F)^-1 ≤ 20/[p³(1-zeta)]. The expected number of U or U† calls is **not** E(N+1), since the Golden controller may STOP first: it equals sum_{n≥0} zeta Tr σ(zeta F)^n = zeta Tr σ(I-zeta F)^-1. The expected number of actual P/Q measured tests is identical. All code flags/clock stages/oldRIGHT/controller record and a genuinely physical independent fair-bit compiler remain paid. This is a valid finite-mean infinite-cut diagnostic, not proof G0 selects its cost or any output Info.

**Important categorical limit:** Real original U† availability and P/Q projective readout, plus physical feed-forward to alternate the two, are REQUIRED; the BOOK algebra alone defines these matrices but does not supply an M1-admitted executable word with phase/order-memory/oldRIGHT preservation. Even if U† has a known finite inverse decomposition for a specific Q8 circuit, the general curved coframe/CAR U(y) inverse and its stage control are not thereby constructed. The controller's fair Golden process also requires fresh independent draws and bounded memory/clock/source analysis; no free coin is introduced. Moreover the stopped score E H_N reconstructs J, not automatically the selected total Book03 H+J+R Cost−Info and its independent preparation Euler. Those remain GR_closed=false.

**Concrete source:** On the already owned ORIGINAL two-tick scene J₂, the RETURN block F has 528 A(x,y) modes and 528 B(x,y) modes, yielding J₂=-528 log[(1-zeta A)(1-zeta B)]=-528 log(1-r(x,y)), with the ACTUAL original N1 Golden click r=zeta(A+B)-zeta²AB. Alternating the ACTUAL U/P/Q for this fixed scene is the precise remaining physical source realization, rather than inventing a generic sqrt(F) spectral gate. The full all42 nonlinear N1/Book source-direction bridge and certified nonnull 42 solutions remain previously owned distinct mathematical results.
