#!/usr/bin/env python3
"""Generation-overlap response origin certificate.

This is the public v14 cert name for the torus-sourced generation overlap
certificate.  It reuses the deterministic shell-operator certificate and emits
the overlap-origin token expected by the global operator-geometry gate.
"""

from __future__ import annotations

from vp_generation_selector_origin import run_certificate


if __name__ == "__main__":
    run_certificate()
    print("[CERT-CLOSED] PASS_GENERATION_OVERLAP_RESPONSE_ORIGIN")
