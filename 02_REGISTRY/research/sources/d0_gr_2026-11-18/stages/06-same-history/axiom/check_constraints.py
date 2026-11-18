"""Read the actual pinned 128-label table. Prove rational constants for two proposed physical bindings."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

REV = "15f5b786ed912a0e91d660e337bf60a7c15c7cfa"
OWNER = "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"

def check(ok, message):
    if not ok:
        raise ValueError(message)

def load_table(repo):
    if repo is None:
        frozen = Path(__file__).resolve().parents[1] / "frozen/expected_actual_ledger_row.json"
        data = frozen.read_bytes()
        check(hashlib.sha256(data).hexdigest() == "7f1b07424839c688117bc9d4c30cf2411596e67ed74a57ce2f6be7d15bc89191",
              "frozen primary ledger row SHA-256")
        return json.loads(data)["fine_probability_rows"]
    src = subprocess.check_output(["git","-C",str(repo),"show",REV+":"+OWNER])
    check(hashlib.sha256(src).hexdigest()=="8e6bf36e80e4ef1693790e6702b204461ec768eaa2a86505e7e368ecaddff672", "primary SHA-256")
    start = b"<!-- BEGIN D0 20261118 CONTINUATION expected_actual_ledger_row.json -->"
    end = b"<!-- END D0 20261118 CONTINUATION expected_actual_ledger_row.json -->"
    segment = src.split(start,1)[1].split(end,1)[0]
    payload = re.search(rb"\x60{3}json\s*(\{.*\})\s*\x60{3}",segment,re.S)
    check(payload is not None,"embedded JSON table")
    return json.loads(payload[1])["fine_probability_rows"]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,default=None)
    args=parser.parse_args()
    rows=load_table(args.repo)
    by_j={i["j"]:(F(i["Tr_M"]),F(i["D_Tr_M"])) for i in rows}
    check(len(by_j)==13 and by_j[13][0]==F(1,25),"positive measured row 13")
    groups={}
    for j,(prob,deriv) in by_j.items():
        groups.setdefault(deriv/prob,[]).append(j)
    check(len(groups)==4 and sum(deriv for _,deriv in by_j.values())==0,"four distinct first scores")
    fisher=sum(deriv**2/prob for prob,deriv in by_j.values())
    g=F(9,2560)
    check(fisher==F(647,120) and g*fisher==F(1941,102400),"fine Fisher coefficient")
    tv=g*sum(abs(deriv) for _,deriv in by_j.values())/2
    check(tv==F(243,25600),"TV coefficient")
    # Bounds below use p^2<2/5, p>8/13, phi>8/5 and e>8/3.
    check(F(3,5)**2+F(3,5)<1 and F(8,13)**2+F(8,13)<1,"p>3/5, p>8/13")
    check(F(9,64000)<F(8,13)**18,"q26<p^22")
    eps=4*F(2,5)*F(9,640)
    check(eps==F(9,400) and 127/eps < F(8,3)**9,"entropy tail logarithm <9")
    lower_log_phi=2*(F(8,5)-1)/(F(8,5)+1)
    entropy_max=eps*10/lower_log_phi
    check(entropy_max<F(1,2),"entropy bound in golden units")
    print(json.dumps({
      "status":"PASS","p":"(sqrt(5)-1)/2","actual_score_groups":{str(k):v for k,v in groups.items()},
      "fine_grouped_fisher_over_p2":str(g*fisher),"first_order_tv_over_p2":str(tv),
      "q26":"9*p**4/64000","q26_threshold":"p**22",
      "upper_H_phi":str(entropy_max),
      "strict_upper_I26_port_only":str(-11+F(3,2)*entropy_max),
      "printed_looser_upper_bound":"-41/4",
      "integrity":"Pinned primary data plus exact rational inequalities; no new full-Book valuation."
    },indent=2))

if __name__=="__main__":
    main()
