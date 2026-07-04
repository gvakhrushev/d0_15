#!/bin/bash
set -e
BASE="https://cdsarc.cds.unistra.fr/ftp/J/AJ/152/157"
DEST="$(dirname "$0")/../cache/sparc"; mkdir -p "$DEST"
for f in ReadMe table2.dat; do curl -sSL -m 60 -o "$DEST/$f" "$BASE/$f"; echo "fetched $f"; done
