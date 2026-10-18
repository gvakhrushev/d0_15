#!/usr/bin/env python3
"""Replay the quantile-clock comparison. Assertions are not used.

python3 and python3 -O must both print PASS.
"""

from __future__ import annotations

import check_quantile_clock_execution as clock

PIN = "3e4330235b9cea8adae9bb58a2b3e045af89f5d2"


def _fail(name: str) -> None:
    raise SystemExit(name)


def main() -> None:
    try:
        clock.forged_engine_executes_map(True)
    except clock.RetypedClockForgery:
        rejected = True
    else:
        _fail("retyped CDF was accepted as engine execution")
    if not rejected:
        _fail("negative control did not raise")
    if clock.forged_engine_executes_map(False) is not False:
        _fail("forged checker changed a failed algebra replay into execution")
    algebra = clock.positive_control()
    if algebra["moving_mass"] != algebra["p"]:
        _fail("moving cell mass")
    result = clock.run()
    if result["engine_executes_map"] is not False:
        _fail("engine_executes_map")
    if result["sources_coincide"] is not False:
        _fail("sources_coincide")
    if result["gr_derived"] is not False:
        _fail("gr_derived")
    if result["qrho_identified_with_mu"] is not False:
        _fail("qrho")
    if result["residual"] != clock.RESIDUAL:
        _fail("residual")
    if result["residual"] in ("", "0", "exact zero", 0):
        _fail("residual collapsed")
    if result["positive_control"] is not True or result["forgery_rejected"] is not True:
        _fail("controls")
    if result["dt_tF"] != "sin(pi*sqrt(5))/(2*pi)":
        _fail("dt")
    if result["lapse_mass_error"] != "eps*sin(2*pi*p)/(2*pi)":
        _fail("lapse")
    if result["shear_wall_velocity"] != "x0*(sqrt(5)-2)/2":
        _fail("shear")
    if result["moving_cell_mass"] != "p":
        _fail("moving mass label")
    if result["owned_cocycle"] != "qρ(ω)=μ(ω) Tr(ρ Mω)":
        _fail("cocycle")
    if result["pin_sha"] != PIN:
        _fail("pin")
    if result["pin_at_least"] != clock.PIN_AT_LEAST:
        _fail("ancestor")
    if result["certificate_present_at_tip"] is not False:
        _fail("certificate tip")
    if result["certificate_present_at_cd077973"] is not False:
        _fail("certificate cd077973")
    if result["ci_ran_absent_certificate"] is not False:
        _fail("ci")
    if result["marker_hits"] != []:
        _fail("marker")
    if "no density argument" not in str(result["address_rule"]):
        _fail("address rule")
    print("PASS")


if __name__ == "__main__":
    main()
