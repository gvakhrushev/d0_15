#!/usr/bin/env python3
"""Audit active integration of the D0 neutron lifetime theorem."""
from __future__ import annotations
import json, math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_TEXT_FILES = {
    "book02_mechanism": "01_BOOKS/BOOK_02_MECHANISM_ACTION.md",
    "book03_spectrum": "01_BOOKS/BOOK_03_SPECTRUM_MATTER.md",
    "book04_verification": "01_BOOKS/BOOK_04_VERIFICATION.md",
    "book05_mathematics": "01_BOOKS/BOOK_05_MATHEMATICS.md",
    "theorem_registry": "00_INDEX/THEOREM_REGISTRY.md",
    "current_status": "00_INDEX/CURRENT_STATUS_ONLY.md",
    "master_index": "00_INDEX/MASTER_INDEX.md",
    "certificate_summary": "04_CERTS/CERTIFICATE_SUMMARY.md",
    "reproducibility_index": "04_CERTS/REPRODUCIBILITY_INDEX.md",
    "compiled_edition": "03_COMBINED/D0_COMPILED_SINGLE_EDITION.md",
}
REQUIRED_FILES = dict(ACTIVE_TEXT_FILES)
REQUIRED_FILES.update({
    "numeric_summary": "00_INDEX/NUMERIC_SUMMARY.json",
    "certificate_script": "04_CERTS/vp_neutron_lifetime_rate_closure.py",
    "certificate_results": "04_CERTS/D0_NEUTRON_LIFETIME_RATE_RESULTS.md",
    "certificate_numbers": "04_CERTS/D0_NEUTRON_LIFETIME_RATE_NUMBERS.json",
})
LATEX_BITS = ["sqrt{\\lambda_n^{D0}}-\\sqrt{\\lambda_p^{D0}}-\\frac1{38}", "0.04030449068822936", "877.8706191589381"]
NUMERIC_JSON_BITS = ['"formula_epsilon_beta": "sqrt(lambda_n_D0)-sqrt(lambda_p_D0)-1/38"','"formula_rate": "Gamma_n_D0*tau0 = epsilon_beta_D0^5 * delta0^19 * q_mass^14"','"tau_n_D0_seconds": 877.8706191589381']
FORBIDDEN_PATTERNS = [r"epsilon[^\n=]*=\s*lambda_n\s*-\s*lambda_p\s*-\s*1\s*/\s*38", r"ε[^\n=]*=\s*λ_n\s*-\s*λ_p", r"neutron channel remains beta/archive", r"neutron lifetime remains separate", r"neutron lifetime\s+(is\s+)?open", r"open\s+neutron lifetime"]

def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")

def compute_numbers() -> dict[str, float]:
    delta0 = (math.sqrt(5.0) - 2.0) / 2.0
    lambda_p = 2334.7985901288725
    lambda_n = 2341.241179437959
    Lambda_act_MeV = 19.417960126286623
    tau0_seconds = 2.129815732459607e-22
    q_mass = 1.0 / (1.0 + delta0**3)
    eps = math.sqrt(lambda_n)-math.sqrt(lambda_p)-1.0/38.0
    gamma_tau0 = eps**5 * delta0**19 * q_mass**14
    return {"epsilon_beta_D0": eps, "Q_beta_D0_MeV": Lambda_act_MeV*eps, "Gamma_n_D0_times_tau0": gamma_tau0, "tau_n_D0_seconds": tau0_seconds/gamma_tau0, "epsilon_beta_power_5": eps**5, "delta0_power_19": delta0**19, "q_mass_power_14": q_mass**14}

def main() -> None:
    missing=[rel for rel in REQUIRED_FILES.values() if not (ROOT/rel).exists()]
    absent=[]
    for name, rel in ACTIVE_TEXT_FILES.items():
        text=read(rel)
        if name in {"certificate_summary", "reproducibility_index"}:
            checks=["vp_neutron_lifetime_rate_closure.py", "PASS_NEUTRON_LIFETIME_BETA_ARCHIVE_UNLOCK_RATE_CLOSURE", "877.8706191589381"]
        elif name in {"current_status", "master_index"}:
            checks=["neutron", "free-neutron beta/archive rate theorem"]
        else:
            checks=LATEX_BITS + ["2.4261157464184423e-25"]
            if name != "book04_verification":
                checks.append("(\\epsilon_\\beta^{D0})^5\\delta_0^{19}q_{mass}^{14}")
        for bit in checks:
            if bit not in text:
                absent.append((name, bit))
    numeric_text=read("00_INDEX/NUMERIC_SUMMARY.json")
    for bit in NUMERIC_JSON_BITS:
        if bit not in numeric_text:
            absent.append(("numeric_summary", bit))
    forbidden=[]
    for name,rel in list(ACTIVE_TEXT_FILES.items())+[("numeric_summary","00_INDEX/NUMERIC_SUMMARY.json")]:
        text=read(rel)
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, text, flags=re.IGNORECASE):
                forbidden.append((rel, pat))
    nums=compute_numbers()
    expected={"epsilon_beta_D0":0.04030449068822936,"Q_beta_D0_MeV":0.7826309930943283,"Gamma_n_D0_times_tau0":2.4261157464184423e-25,"tau_n_D0_seconds":877.8706191589381}
    numeric_errors={k: abs(nums[k]-v) for k,v in expected.items()}
    numeric_ok=all(err <= max(1e-30, abs(expected[k])*1e-14) for k,err in numeric_errors.items())
    status="PASS_NEUTRON_LIFETIME_FULL_INTEGRATION_AUDIT" if not missing and not absent and not forbidden and numeric_ok else "FAIL_NEUTRON_LIFETIME_FULL_INTEGRATION_AUDIT"
    res={"status":status,"missing_required_files":missing,"missing_active_presence":absent,"forbidden_active_patterns":forbidden,"numeric_values":nums,"numeric_errors":numeric_errors,"active_books_checked":["BOOK_02_MECHANISM_ACTION","BOOK_03_SPECTRUM_MATTER","BOOK_04_VERIFICATION","BOOK_05_MATHEMATICS"],"active_indices_checked":["THEOREM_REGISTRY","CURRENT_STATUS_ONLY","MASTER_INDEX","NUMERIC_SUMMARY","CERTIFICATE_SUMMARY","REPRODUCIBILITY_INDEX","D0_COMPILED_SINGLE_EDITION"],"historical_snapshots_policy":"D0_ALL_BOOKS_* files are historical snapshots and are not used for active-status assertions.","guardrail":"The beta window is sqrt(lambda_n)-sqrt(lambda_p)-1/38, never raw lambda_n-lambda_p-1/38; measured neutron lifetime is benchmark only, not input."}
    (ROOT/'04_CERTS'/'D0_NEUTRON_LIFETIME_FULL_INTEGRATION_AUDIT_RESULTS.json').write_text(json.dumps(res, indent=2, sort_keys=True)+"\n", encoding='utf-8')
    md=["# D0 Neutron Lifetime Full Integration Audit","",f"Status: `{status}`","","## Checked active books","","- Book 02 — mechanism/action block.","- Book 03 — spectrum/matter block.","- Book 04 — verification block.","- Book 05 — mathematical theorem block.","","## Canonical theorem","","```math",r"\epsilon_\beta^{D0}=\sqrt{\lambda_n^{D0}}-\sqrt{\lambda_p^{D0}}-\frac1{38}=0.04030449068822936","```","","```math",r"\Gamma_n^{D0}\tau_0=(\epsilon_\beta^{D0})^5\delta_0^{19}q_{mass}^{14}=2.4261157464184423\times 10^{-25}","```","","```math",r"\tau_n^{D0}=877.8706191589381\;\mathrm{s}","```","","## Result","",f"- Missing active presence: `{absent}`",f"- Forbidden active patterns: `{forbidden}`",f"- Numeric errors: `{numeric_errors}`","","Historical `D0_ALL_BOOKS_*` snapshots are not active-status books and were not used for this pass/fail criterion.",""]
    (ROOT/'04_CERTS'/'D0_NEUTRON_LIFETIME_FULL_INTEGRATION_AUDIT_RESULTS.md').write_text("\n".join(md), encoding='utf-8')
    print(json.dumps(res, indent=2, sort_keys=True))
    if status.startswith('FAIL'):
        raise SystemExit(1)
if __name__ == '__main__':
    main()
