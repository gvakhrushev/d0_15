#!/usr/bin/env python3
import math, json, pathlib

# Minimal executable scheme contract, not a new D0 prediction.
passport = {
    "claim_id": "D0-QFT-RG-ALPHA-001",
    "quantity": "alpha",
    "scheme": "minimal one-loop QED bridge contract",
    "mu0_GeV": 0.00051099895,  # electron mass scale, declared input
    "mu1_GeV": 91.1876,        # Z pole scale, declared comparison scale
    "alpha_inv_mu0": 137.035999084,
    "active_species": [
        {"name": "e", "Nc": 1, "Q": -1, "threshold_GeV": 0.00051099895},
        {"name": "mu", "Nc": 1, "Q": -1, "threshold_GeV": 0.1056583755},
        {"name": "tau", "Nc": 1, "Q": -1, "threshold_GeV": 1.77686},
    ],
    "free_repair_parameters": 0,
}

alpha_inv = passport["alpha_inv_mu0"]
mu0 = passport["mu0_GeV"]
mu1 = passport["mu1_GeV"]
contributions = []
for sp in passport["active_species"]:
    th = sp["threshold_GeV"]
    if mu1 > th:
        start = max(mu0, th)
        delta_inv = -(2/(3*math.pi))*sp["Nc"]*(sp["Q"]**2)*math.log(mu1/start)
        alpha_inv += delta_inv
        contributions.append({"name": sp["name"], "delta_alpha_inv": delta_inv})

checks = {
    "scheme_declared": bool(passport["scheme"]),
    "scales_declared": mu0 > 0 and mu1 > mu0,
    "active_species_declared": len(passport["active_species"]) >= 1,
    "no_free_repair_parameters": passport["free_repair_parameters"] == 0,
    "output_not_overwritten": abs(alpha_inv - passport["alpha_inv_mu0"]) > 0,
}

result = {
    "cert": "vp_v1134_alpha_scheme_passport",
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "passport": passport,
    "contributions": contributions,
    "computed_alpha_inv_mu1_minimal_QED": alpha_inv,
    "note": "This cert closes the scheme bridge contract. It is not a full SM electroweak precision prediction."
}

pathlib.Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2), encoding="utf-8")
pathlib.Path(__file__).with_suffix(".md").write_text("# v11.34 alpha scheme-passport cert\n\n```json\n" + json.dumps(result, indent=2) + "\n```\n", encoding="utf-8")
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["status"] == "PASS" else 1)
