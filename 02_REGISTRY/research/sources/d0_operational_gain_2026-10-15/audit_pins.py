#!/usr/bin/env python3
"""Read-only audit of the failed old receipt. Never rewrite a provenance hash."""
import argparse, hashlib, json
from pathlib import Path

def audit(root: Path):
    base=root/'02_REGISTRY/research/certificates/a4d_native_condensed_price_naturality_results.json'
    rec=json.loads(base.read_text())
    failures=[];checked=0
    for group in ('transitive_d0_source_sha256','primary_and_prior_input_sha256','toolchain_input_sha256'):
        for name,expected in rec[group].items():
            checked+=1;path=root/name
            actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            if actual!=expected:failures.append({'group':group,'path':name,'expected':expected,'actual':actual})
    return {'schema':'d0-readonly-pin-audit/1','checked':checked,'failures':failures,'files_modified':0}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('repository',type=Path);args=ap.parse_args()
    result=audit(args.repository.resolve());print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(1 if result['failures'] else 0)
if __name__=='__main__':main()
