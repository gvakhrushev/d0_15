"""Run the frozen B121 constructor using the matching bundled Git blobs."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parents[1] / "primary"
source = base / "B121" / "check_book03_identity_pair.py"
pins = json.loads((base / "SOURCES.json").read_text())["primary_files"]
assert hashlib.sha256(source.read_bytes()).hexdigest() == pins["B121/" + source.name]["sha256"]
original = source.read_text()
start = original.index("REPO = ")
end = original.index("ARCHIVE = ", start)
header = """REPO = Path(_bundle_root)
NATIVE = REPO / 'native_execution.py'
BOOK03 = REPO / 'B121' / 'BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md'
"""
script = original[:start] + header + original[end:]
start = script.index("    spec = f", script.index("def archive_pin"))
end = script.index("    return ", start)
# Compute each real Git blob identity directly. The original semantic
# constructor, expected blob constants, and returned hashes stay unchanged.
reader = """    data = (REPO / 'B121' / path).read_bytes()
    frame = b'blob ' + str(len(data)).encode() + b'\\0' + data
    blob = __import__('hashlib').sha1(frame).hexdigest()
    require(blob == expected_blob, f'Archive blob changed: {path}')
"""
script = script[:start] + reader + script[end:]
exec(compile(script, str(source), "exec"),
     {"__name__":"__main__", "__file__":str(source), "_bundle_root":str(base)})
