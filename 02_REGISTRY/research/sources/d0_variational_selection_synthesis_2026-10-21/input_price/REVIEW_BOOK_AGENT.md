# Independent scientific review: full128 all-input price separation

Reviewer: `/root/book_binding`, 21 October 2026. Read-only review requested
by the integrating agent. No input proof, checker, or expected result was changed.

## Reviewed immutable artifacts

| Artifact | SHA-256 |
|---|---|
| PROOF.md | d355322a2436ba3d2b0c1305050507e6cee5a1bbdc0915e9785fb74a6ea0ddae |
| check_input_obstruction.py | 4c0529877e803d2d76876fdecdf20cac6825d82e0e6ac223d12ad953b355c9c0 |
| RESULT.json | 0350d3348f25a945a4289ec9b20a4e2e9a8c1f5cf5cfa9d948b2261f02e7cc1e |

I independently read the literal pinned native_input.py, the port/channel
owner A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md, and the
preparation/retained-input source proofs. The checker was executed with
PYTHONPATH=/tmp/d0_synthesis_python against the current repository.
All 145 checks passed; stdout is byte-identical to the frozen RESULT.json.
The numerical Kraus checks are diagnostics, as the proof correctly states.

## Decision

**ACCEPT the exact n=4096 all-input inequality at its stated scope.**
No mathematical correction is needed for this core result. This is an
original DATA16 Fourier-block comparison of port code cost minus complete
coherent-record entropy, not a full spatial Einstein-field comparison or
a compulsory Book03 action theorem.

### 1. Native scalar effect and all-horizon charge

The actual phases have squared differences 2,2,4,2, totaling 10.
The signed original CAR therefore gives

    A^2 = (nu^2/16^2) sum_r |zeta_r-1|^2 I
        = (5nu^2/128)I.

Both nu=1/2 and nu=3/5 lie strictly within the original Julia domain:
the unscaled creators have norm one, and nu<1. No frozen-recycling
variation is introduced; the literal native function recomputes its Julia
defects and all128 Kraus maps at each nu.

The original full port1 sum is exactly E1=4p^3 A^2. This follows from the
actual paired Kraus maps and complete Walsh/Julia row identity, not from
the entropy choice. Thus G_port=(1+5p^3nu^2/32)I. Unitality of Phi* proves

    sum_(j=0)^(n-1)(Phi*)^j G_port
      =n(1+5p^3nu^2/32)I

at every integer n. Every normalized DATA input has the same expected
port charge. Initial DATA/RIGHT entanglement cannot change this scalar
expectation. The four-round numerical recurrence is a useful consistency
check, not the proof of the all-horizon identity.

### 2. Entropy cap and independence of the two inputs

For any pure initial DATA16/RIGHT128 purification C, the occupied RIGHT
subspace has dimension r=rank(CC*)<=16. Acting only on DATA leaves that
RIGHT support unchanged. The final DATA/RIGHT marginal is consequently
supported in dimension at most16r<=256. The whole DATA/RIGHT/fresh-record
state remains pure under the specified complete Stinespring execution.
Its two complementary marginals have equal nonzero Schmidt spectra, so

    0 <= S_phi(E) <= log_phi256.

The huge coherent record is not discarded to obtain this estimate. It is
a spectral bound on the full retained E marginal. It would not automatically
apply to newly introduced mixed fresh resources without their purifiers,
or to a physically measured pointer alphabet; those are different inputs
or information cuts and are not asserted here.

For any two independently chosen normalized purifications C1 and C2,
the difference is bounded below by the exact charge difference minus
log_phi256. Nothing requires their Schmidt spectra, RIGHT Grams, or
prepared DATA states to agree. Restricting both choices to a common fixed
RIGHT Gram only makes the comparison a smaller subclass, so the same
inequality holds there. Separate infima over any nonempty allowed input
classes also inherit it.

### 3. Exact positive lower bound

The exact charge difference per round is 11p^3/640. Since

    p^3=sqrt5-2>1/5,
    phi^12=144phi+89>144*(3/2)+89>256,

one obtains, strictly,

    4096*(11p^3/640)-log_phi256
       >4096*(11/640)*(1/5)-12=52/25.

The displayed approximately5.095824892684744 bound is only a numerical
display of the sharper exact expression; positivity does not depend on
floating-point logarithms, the Gibbs optimizer, mixing, or the n=2048
preparation diagnostic. The sharp conceptual conclusion is that optimizing
the initial density cannot reverse this finite same-horizon comparison.

### 4. General long-horizon corollary

The bound from A_n=n cbar I+Y-(Phi*)^nY is correct: a unital positive map
contracts the operator norm on Hermitian Y, giving a boundary of at most
2||Y||. Together with the entropy cap this yields uniform O(1/n) value
convergence over pure input preparations. The derivative statement is
properly conditional on the stated uniform C1 mixing/source control and
a smooth interior minimum branch on a compact regular chart. It must not
be promoted to a uniform spatial-refinement bound, a universal finite
derivative threshold, or a statement near dark/singular modes.

## Optional measured-pointer entropy-rate section

**Mathematically acceptable with its explicit extra hypotheses; secondary
to the n=4096 result.** I do not find a false rate assertion, but it supplies
a conditional necessary target rather than an evaluated compensating source.

The stationary initial DATA density makes the repeated measured output
process stationary. Its conditional entropies decrease to an entropy rate.
For a general initial density, discarding the first k outcomes only for the
mathematical entropy chain rule leaves a tail generated from Phi^k(rho).
Trace-distance contraction under the whole tail instrument bounds its
classical total-variation distance from the stationary tail by delta_k.
The prefix conditional entropy lies in [0,k log_phi128] for both inputs;
its difference is bounded by that interval's width. Classical entropy
continuity then gives the displayed estimate. For the asymptotic use,
take k sufficiently large that delta_k<=1/2 and k proportional to log n.
This justifies uniform O(log n) differences and a common rate. It is
not a physical deletion or a chosen new price.

The ancillary port split is also exact: for each nonblank label the two
Kraus maps are positive scalar multiples of the same data map, with
conditional probabilities (p^2,p). Given the complete reduced past and
future labels, these port bits contribute independent entropy2-p each.
Both special blank-label ports stay distinguished. Hence

    H_full,n=H_red,n+(2-p) E N_nonblank-label.

On the scalar chart, the two blank Kraus squares directly give
E_nonblank-label=4p^2 lambda(1-lambda)I. Differentiation yields equation(6)
with the exact displayed coefficient and sign.

**Do not use equation(6) as an established physical mechanism or as a
computed derivative of h_red.** Neither C1 convergence of entropy rates,
the value of h_red', compulsory physical measurement, nor absence of other
complete price sources has been proved by this packet. The text retains
those premises. In the central synthesis I recommend reporting the exact
all-input obstruction as the result and treating equation(6), if mentioned,
as a separately conditional remaining calculation.

## Scope retained for integration

* One original homogeneous Fourier block, all16 CAR grades/all128 outcomes.
* Two original creation-column scales, one fixed horizon4096.
* Arbitrary purified inputs, including common fixed-RIGHT subclasses.
* Declared port-cost/coherent-E entropy valuation only.
* No collar-preserving all42 variation or same-initial physical writer is inferred.
* Every additional genuine writer, heat, work, label and Book charge retains
  its own difference. This inequality does not assign it zero.
* GR_closed remains false.

## Brief review of the clock-bracket packet, sections6–7

Reviewed /tmp/d0_clock_bracket_synthesis/PROOF.md, SHA-256
339ce4422f220d0dac6cc8617e540293fc6dd1bfb2f56515c4abaaa3826e2c0e.

**ACCEPT the heat third-order control as a scoped algebraic discriminator.**
For constant positive spatial q, D^2=-q^ij partial_i partial_j and
L_N={N,D^2}/2 has scalar principal symbol Nq^ij xi_i xi_j. Its commutator
has the displayed degree-three coefficient (up to the stated symbol i/sign).
An independent exact symbolic calculation with arbitrary N(x),M(x),f(x)
confirmed that the fourth derivative cancels and the coefficient of f''' is
exactly2(N M'-M N'). Thus the symmetrized heat candidate does not have the
first-order normal-normal deformation bracket for generic lapses. This
does not exclude every physical use of Book heat or nonlocal generators.

**The canonical-reconstruction boundary is correctly retained.** The proof
does not apply Hojman--Kuchar--Teitelboim to the external-spinor commutator.
It explicitly still requires a dynamical geometric phase/presymplectic
space, actual full-process constraint generators, moving-coframe terms,
the other normal/tangential brackets, and the reconstruction hypotheses.
A frozen Dirac background already satisfies the kinematic relation; hence
the identity cannot alone derive Einstein dynamics. The nonzero spin term
also cannot be dropped. I recommend retaining the clock calculation as
a new conditional native-operation test, not as closed GR or a canonical
constraint algebra already supplied by the CAR data.

This final paragraph reviews the algebra and scope stated in the packet;
it is not an independent literature/theorem audit of the cited HKT papers.
