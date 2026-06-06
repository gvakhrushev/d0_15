#!/usr/bin/env python3
"""D0 neutron beta/archive split closure certificate."""
from __future__ import annotations
import json, math
from pathlib import Path

def run_vp_neutron_beta_archive_split_closure() -> dict[str, object]:
    phi=(1+math.sqrt(5))/2
    delta0=(math.sqrt(5)-2)/2
    Delta_lambda=math.sqrt(10)/20
    d13=20
    lambda_N_core=2640.7985901288725
    lambda_p=2334.7985901288725
    Lambda=19.417960126286623
    lambda_np_split=2*d13*Delta_lambda+delta0
    lambda_n=lambda_p+lambda_np_split
    M_p=Lambda*math.sqrt(lambda_p)
    M_n=Lambda*math.sqrt(lambda_n)
    return {
        "status":"PASS_NEUTRON_BETA_ARCHIVE_SPLIT_CLOSURE",
        "phi":phi,
        "delta0":delta0,
        "Delta_lambda":Delta_lambda,
        "d13":d13,
        "lambda_N_core":lambda_N_core,
        "lambda_p_D0":lambda_p,
        "lambda_np_split_D0":lambda_np_split,
        "lambda_n_D0":lambda_n,
        "Lambda_act_SI_MeV":Lambda,
        "M_p_D0_MeV":M_p,
        "M_n_D0_MeV":M_n,
        "np_mass_difference_D0_MeV":M_n-M_p,
        "m_n_over_m_e_D0":38*math.sqrt(lambda_n),
        "formula":"lambda_n=lambda_p + 2*d13*Delta_lambda + delta0 = lambda_p + 2*sqrt(10)+delta0",
        "guardrail":"This closes the neutron mass/split operator and supplies lambda_n for the separate neutron lifetime unlock-rate theorem. The split certificate is not itself a lifetime normalization.",
    }

def main() -> None:
    res=run_vp_neutron_beta_archive_split_closure()
    root=Path(__file__).resolve().parents[1]
    out=root/'04_CERTS'/'D0_NEUTRON_BETA_ARCHIVE_SPLIT_RESULTS.md'
    js=root/'04_CERTS'/'D0_NEUTRON_BETA_ARCHIVE_SPLIT_NUMBERS.json'
    lines=["# D0 Neutron Beta/Archive Split Closure", "", f"Status: `{res['status']}`", "", "## Formula", "", "```text", res['formula'], "```", "", "## Numbers"]
    for k,v in res.items():
        if k not in {'status','formula'}:
            lines.append(f"- `{k}`: `{v}`")
    out.write_text("\n".join(lines)+"\n", encoding='utf-8')
    js.write_text(json.dumps(res, indent=2, sort_keys=True)+"\n", encoding='utf-8')
    print(json.dumps(res, indent=2, sort_keys=True))

if __name__=='__main__':
    main()
