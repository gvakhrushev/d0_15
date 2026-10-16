# Vacuum response control

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `560bf69300dcf8bb9c798cdd3f6e667cc9870729`.
Status: control, not a terminal. No source is assigned from a candidate.

## Control

On the flat background `eta`, the identity connection is an exact joint root of the vacuum equations `E_K=0` and `Xi=0`. Any other field in the same sitewise class satisfies `Xi=0` by membership. Therefore

```text
diam { Xi(K) : E_K(eta, K)=0 and Xi(K)=0 } = 0.
```

After `h^{-2}` the owner reconstruction is `0`, which is `-G[eta]/2`. The owned #232 family sits in this class: it is curved, nongauge, exactly connection stationary, and has `Xi=0`. It does not split the response class. Connection uniqueness fails; sitewise response uniqueness holds by the class definition.

The #227 family is outside the class. Its packed memory is nonzero, so it does not solve the vacuum metric equation. Using its response as a source after the fact is forbidden.

## What this does not close

The identity is a substitution. It does not construct a joint root for a nonzero prescribed smooth source, and it does not constrain a field whose metric equation is only the phase-erased subset. Existence of the designated root remains owned for small one-coordinate coframes and the warped family, not for a general four-dimensional `g`. Isolation outside the `c_g sqrt(h)` ball remains open.

Neither `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED` nor `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO` follows.

Verdict: vacuum sitewise diameter is a control. The lane stays `PARTIAL / OPEN` at prescribed-source existence on general `g`.
