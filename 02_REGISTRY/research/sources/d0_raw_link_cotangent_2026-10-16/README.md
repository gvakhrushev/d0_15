# Raw-link cotangent coefficient conversion

[Proof and scope](../../A4D_RAW_LINK_COTANGENT_JET.md) · [Exact checker](check_raw_link_cotangent.py) · [Scientific stdout](RESULTS.json) · [Execution metadata](VALIDATION.json)

The bounded calculation checks a nonconstant, noncommuting proper Lorentz
parallel path through h³ and its actual raw-link variation. It retains all 16
exterior components, both invariant-trace and positive Hilbert–Schmidt
cotangent pairings, nonconstant density and moving-background corrections.
The inverse coefficient is 1/12. Frozen endpoints, reversed trivialization,
omitted density and the wrong boost adjoint are rejected.

The completed normal and optimized runs passed 47 exact checks with
byte-identical stdout. Normal stdout is preserved as RESULTS.json;
optimized stdout was captured and compared in memory. No separate optimized
stdout file exists. Its measured runtime was 3.045s; the normal runtime was
not recorded. VALIDATION.json records these facts without another execution.

API: `run(repo=None)` returns the deterministic result; running the checker
prints it. No old check entrypoint is executed. The result is a smooth jet
conversion, not a uniform all-grid C⁰ inverse or a continuum/source theorem.
No native connection, preparation, action or physical admission is selected.
