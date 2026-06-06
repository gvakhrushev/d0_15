#!/usr/bin/env python3
"""Compatibility wrapper for the closed CKM mass-basis theorem."""
from __future__ import annotations

from vp_ckm_mass_basis_terminal_return_closure import run_vp_ckm_mass_basis_terminal_return_closure


def run_vp_final_ckm_mass_basis() -> dict[str, object]:
    result = run_vp_ckm_mass_basis_terminal_return_closure()
    result = dict(result)
    result['compatibility_note'] = 'This replaces the old bridge-open diagnostic: quark up/down mass operators are now registered in Book 03 and certified by vp_ckm_mass_basis_terminal_return_closure.py.'
    return result


def main() -> None:
    result = run_vp_final_ckm_mass_basis()
    print(f"VP final CKM mass basis: [{result['status']}]")
    for key, value in result.items():
        if key != 'status':
            print(f"{key}= {value}")


if __name__ == '__main__':
    main()
