#!/usr/bin/env python3
import sys
import re
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_ROOT = ROOT / "09_LEAN_FORMALIZATION"

def main() -> int:
    claim_map_path = LEAN_ROOT / "D0" / "TheoremLedger" / "ClaimMap.lean"
    active_index_path = LEAN_ROOT / "D0" / "TheoremLedger" / "ActiveClosureIndex.lean"
    claim_csv_path = LEAN_ROOT / "docs" / "CLAIM_TO_LEAN_MAP.csv"
    targets_csv_path = LEAN_ROOT / "docs" / "HARD_CLOSURE_TARGETS.csv"
    books_dir = ROOT / "01_BOOKS"
    theory_map_dir = ROOT / "03_THEORY_MAP"

    failures = []

    # 1. Read active targets from ActiveClosureIndex.lean
    if not active_index_path.exists():
        print(f"FAIL: ActiveClosureIndex.lean not found at {active_index_path}")
        return 1
    active_content = active_index_path.read_text(encoding="utf-8")
    active_theorems = [
        item.split(".")[-1]
        for item in re.findall(r'#check\s+@?D0\.([A-Za-z0-9_.]+)', active_content)
    ]
    if not active_theorems:
        print("FAIL: No active theorems found in ActiveClosureIndex.lean")
        return 1

    # 2. Read CLAIM_TO_LEAN_MAP.csv to find corresponding claim IDs for active theorems
    if not claim_csv_path.exists():
        print(f"FAIL: CLAIM_TO_LEAN_MAP.csv not found at {claim_csv_path}")
        return 1
    
    with claim_csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        csv_rows = list(reader)

    active_claim_ids = []
    for row in csv_rows:
        lean_th = row.get("lean_theorem", "")
        # A claim row might contain multiple theorems separated by semicolons
        th_names = [t.strip().split(".")[-1] for t in lean_th.replace(";", ",").split(",") if t.strip()]
        for ath in active_theorems:
            if ath in th_names:
                active_claim_ids.append(row.get("claim_id"))

    # Remove duplicates
    active_claim_ids = list(set(active_claim_ids))

    # Check that CLAIM_TO_LEAN_MAP.csv contains entries for all active theorems
    for ath in active_theorems:
        found = False
        for row in csv_rows:
            lean_th = row.get("lean_theorem", "")
            th_names = [t.strip().split(".")[-1] for t in lean_th.replace(";", ",").split(",") if t.strip()]
            if ath in th_names:
                found = True
                break
        if not found:
            failures.append(f"Active target theorem '{ath}' has no entry in CLAIM_TO_LEAN_MAP.csv")

    # Check that HARD_CLOSURE_TARGETS.csv contains entries for all active theorems
    if not targets_csv_path.exists():
        print(f"FAIL: HARD_CLOSURE_TARGETS.csv not found at {targets_csv_path}")
        return 1
    with targets_csv_path.open("r", encoding="utf-8", newline="") as f:
        t_reader = csv.DictReader(f)
        t_rows = list(t_reader)
    for ath in active_theorems:
        found = False
        for row in t_rows:
            if row.get("theorem_name").split(".")[-1] == ath:
                found = True
                break
        if not found:
            failures.append(f"Active target theorem '{ath}' is missing from HARD_CLOSURE_TARGETS.csv")

    # 3. Read ClaimMap.lean to check that it contains the active claim IDs
    if not claim_map_path.exists():
        print(f"FAIL: ClaimMap.lean not found at {claim_map_path}")
        return 1
    claim_map_content = claim_map_path.read_text(encoding="utf-8")
    for cid in active_claim_ids:
        if cid not in claim_map_content:
            failures.append(f"Claim ID '{cid}' is missing from ClaimMap.lean")

    # 4. Gather text from all books and theory map files to check for mentions of active claims/theorems
    book_texts = ""
    for path in books_dir.rglob("*.md"):
        book_texts += path.read_text(encoding="utf-8") + "\n"
    if theory_map_dir.exists():
        for path in theory_map_dir.rglob("*"):
            if path.is_file():
                book_texts += path.read_text(encoding="utf-8", errors="ignore") + "\n"

    # Check that active claim IDs and active theorem names are referenced in the books / theory map
    for cid in active_claim_ids:
        if cid not in book_texts:
            failures.append(f"Active claim ID '{cid}' is not referenced in any book in 01_BOOKS/ or theory map in 03_THEORY_MAP/")

    for tname in active_theorems:
        if tname not in book_texts:
            failures.append(f"Active target theorem '{tname}' is not mentioned in any book in 01_BOOKS/ or theory map in 03_THEORY_MAP/")

    if failures:
        print("FAIL: Text sync issues found:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("PASS: Text synchronization check succeeded.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
