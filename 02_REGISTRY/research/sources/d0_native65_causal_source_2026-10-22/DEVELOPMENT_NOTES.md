# Development audit

The first run reached the final diagnostic but failed an unjustified test expecting the two-tick predictive information to exceed 1e-8. Direct evaluation gave about 6.51254e-10 nats. The test was replaced with an independent direct joint-KL computation and cross-checked against the entropy difference and its derivative. No theorem asserted the rejected numerical threshold. Earlier identities had passed; the failed run is not counted as a passing run.

The executable native excerpt comes from connector-read original functions. It is not an independently fetched byte-for-byte full Git checkout.
