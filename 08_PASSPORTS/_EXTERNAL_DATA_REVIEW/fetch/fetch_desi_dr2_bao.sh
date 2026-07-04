#!/bin/bash
# Fetch DESI DR2 BAO combined measurements (git-safe: data -> cache/, only this script + manifest committed).
set -e
BASE="https://raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2"
DEST="$(dirname "$0")/../cache/desi_dr2_bao"
mkdir -p "$DEST"
for f in desi_gaussian_bao_ALL_GCcomb_mean.txt desi_gaussian_bao_ALL_GCcomb_cov.txt; do
  curl -sSL -m 60 -o "$DEST/$f" "$BASE/$f"
  echo "fetched $f"
done
