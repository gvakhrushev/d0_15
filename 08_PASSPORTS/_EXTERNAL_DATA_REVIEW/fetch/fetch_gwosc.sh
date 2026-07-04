#!/bin/bash
set -e; DEST="$(dirname "$0")/../cache/gwosc"; mkdir -p "$DEST"
curl -sSL -m 90 -o "$DEST/allevents.json" "https://gwosc.org/eventapi/json/allevents/"; echo "fetched allevents.json"
