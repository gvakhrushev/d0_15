#!/usr/bin/env python3
import subprocess, sys, json, pathlib
root = pathlib.Path(__file__).resolve().parent
scripts = [
    "vp_v1134_lattice_ward_anomaly_hardening.py",
    "vp_v1134_alpha_scheme_passport.py",
]
rows = []
for s in scripts:
    p = subprocess.run([sys.executable, str(root/s)], cwd=str(root), text=True, capture_output=True)
    rows.append({"script": s, "returncode": p.returncode, "status": "PASS" if p.returncode == 0 else "FAIL", "stdout_tail": p.stdout[-1000:], "stderr_tail": p.stderr[-1000:]})
status = "PASS" if all(r["returncode"] == 0 for r in rows) else "FAIL"
result = {"cert": "run_all_v1134_external_hardening", "status": status, "rows": rows}
(root/"run_all_v1134_external_hardening_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
(root/"run_all_v1134_external_hardening.md").write_text("# v11.34 external hardening runner\n\n```json\n" + json.dumps(result, indent=2) + "\n```\n", encoding="utf-8")
print(json.dumps(result, indent=2))
sys.exit(0 if status == "PASS" else 1)
