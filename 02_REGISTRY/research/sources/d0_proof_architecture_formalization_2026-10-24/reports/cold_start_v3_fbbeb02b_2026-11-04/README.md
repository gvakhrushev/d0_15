# Cold-start v3: producer overview, 4 November 2026

A full producer replay completed with exit code 0 on clean snapshot
`fbbeb02bb1cb36da0f173adc614400dbe81154e9`: 50 search cases, 414 queries,
and an additional change-impact case. The complete original report is held
locally because it contains local absolute paths; it is not published here.
Its operator-recorded byte length is 468947808 and SHA-256 is
`adf9b4549f50aea8f56f03511abd3bcf0e5ad84367366fea4fc0c80834f7c059`.
Without the original bytes a reader cannot independently verify this hash or
replay evidence from this overview. This hash does not authenticate the producer.

The accompanying JSON is a minimal producer-asserted summary, not the output
of the independent evidence compactor. Discovery is unattested and the top-level
success count is null. The 50 false case flags follow from unattested discovery;
they do not show 50 failed searches. Status counts are self-reported and do not
independently establish source attribution, verified discovery, or mathematical
scope. The exact-source-vs-unrelated-prose control is a producer assertion.

Independent compaction of original evidence failed (exit 1): source pages did
not reproduce from locator bytes and pins. The cause remains under investigation.
No redacted raw report is included, and no result here establishes C0 acceptance
or physical GR selection. Earlier 44/50 and 36/50 strict replays used different
snapshots and must not be numerically compared as if inputs were identical.
