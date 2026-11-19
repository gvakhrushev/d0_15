# Reproduce the original-full128 preparation/source packet

Run from any directory with Python, NumPy, SciPy and SymPy:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python check_native_preparation.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O check_native_preparation.py

Inside the repository the checker imports the existing pinned native source.
The downloadable ZIP also includes a byte-identical copy under inputs/ for
standalone use. The previous suite is not rerun. PROOF.md contains the analytic
all-length and all-size statements; RESULT.json contains the actual 69-group
finite replay with its tolerances and scope. VALIDATION.json records hashes,
ordinary/optimized equality and four rejected mutations. The delivered
validate_packet.py reproduces the mutation run.

This packet's title refers to closure of a dynamical fixed-state classification
and its source calculation, not physical GR closure. Keep all condition and
normalization distinctions in PROOF.md, especially sections 6 and 10.
