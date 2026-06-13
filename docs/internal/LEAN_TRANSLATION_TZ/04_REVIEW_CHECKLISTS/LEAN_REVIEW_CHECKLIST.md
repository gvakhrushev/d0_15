# Lean review checklist

For every Lean PR:

1. Does it compile with `lake build`?
2. Does it introduce `axiom`, `sorry`, `admit`, or `unsafe`?
3. Does it use `Float` in theorem-bearing code?
4. Is the theorem in the correct layer: core / bridge / cert / passport?
5. If bridge, are assumptions explicit structures?
6. If physical claim, is there a claim-id mapping?
7. If numerical result, is it exact arithmetic or delegated to cert with hash/log?
8. Does the active book text need an update?
9. Does theorem/status database need an update?
10. Are negative controls represented as formal predicates or cert tests?
