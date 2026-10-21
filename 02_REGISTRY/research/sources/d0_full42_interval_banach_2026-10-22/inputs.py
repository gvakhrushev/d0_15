"""Exact rational decimal collar and 42-vector for the interval Banach proof.

Reproducibility transport only: these UTF-8 JSON files were zlib-compressed
and base64-encoded without changing their bytes. On extraction verify the
published SHA256 hashes; floats are NEVER used for these coordinates.
"""
from pathlib import Path
import base64, zlib, hashlib, json

_COLLAR = (
"eNrNVsluG1cQvOsrBjxJiiD39nrxL+SQQ5BTEBAjkY4HokmGZAALQf499caCwDjWzQRCidJwlurq7upq/nU1DIuPi/fDgu45NYmbmLfkKDN311L2koyMJm4m"
"jaxwmOyhZml4RMVJijWyBQvz4q6DrperafwdyL/i0/Dyd+hxIrkDlaiyNQRUZtcm4URUSskqag5gMGIRFtew4nR1KksqmgPPcWZMvpcoT2ugVMJqxOWtWjMX"
"MjLVVALrIBZLDaAR2KZKdCAl5uYU7OeQiJyZhJCSnVhQv9O4kCUeZu/MgzuvdEdOEtGUqCGtIFwPJKp6CcgZ8be7/xa2ubSeHrqU3lAlShTDGIXBL/BFPAWf"
"0VzNQgk8s6xluBMbNfS6fVVYNJ+VOkNREAX9bBbg1gI9qpYipEFdIeipVStkgKhQC3SBpuKC/QsSUSoJjzXkqIWepwdnEStybNKZpCECejZrAv0JMqkogCE+"
"mEReAvKbheV7+j6vc8YXgJT/L+SXul691HZx3I+nadwsH3a742n5dPyWS5zxgLIDYwOJYYrRSGgbIm5ooLgXzgrEFlIYDxGYgzij1WEQOuZG3WfRN6j/Iphv"
"TCN19WEeJN3gWtx1mU0qvTCU8D3qngUZYjC/GCnGBycNuDA6OBiTZJ37HEgTeSkupYCLQrX4weApbBO2IaCIkUsFW9gZXBne1/M0wvAqpI+RTAS4COYbhWBz"
"U+wHIAU8pxsxEkZ1MH2hsAx4kcAGMcGl3s2mosdCMRp8uoxwFu0454xVACftdTK4Fl6wJrzRMi1UUb05TN/gW1qh4IxNg4XifR+YdsNyh0XxRTC/Uvv+OPGr"
"ws+U3Q8ZT1BxGFx7tiIsMDg/wkAv2BZdPI5dhkY01Bk3cwuaWcLdBE6LdRmvwu6Q2suaUBvWN5Y56giVYYPC5qISQaSrHS22boXadwRVwabRRCSk6IMkVvvi"
"PAF5K4Hzw9cHxk/7/pWC3x3/OJyu5fZp3O/Hm5fvBZ/Hx9Pyw7TerJbT9rQ+7A/rE+xgt+2PHOajcTOs1o/TJ/x/3G024+F4N4ybzfDL8LD7c7saD8/DZto+"
"HXHXh2m7Xg0Pz8P68/764+3Tcrr9cTndDMfdMB7Wwxxt8zxM2+Hnn3645ju9WVz9/Q/ulM5b"
)
_CENTER = (
"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"
"i//9BlR+bMM="
)
_SHA = {
"rational_collar.json":"b86d94a59f5b0ecfec55af3a6c0db80eec257d41b09f3a03c59e367f56093fa1",
"rational_center.json":"0258a6bc84446dd8a506479acc59f4dbf503f3417c508444c516cce9c314f2f5",
}
def _recover(name, compressed):
    data=zlib.decompress(base64.b64decode(compressed))
    assert hashlib.sha256(data).hexdigest()==_SHA[name], name
    return json.loads(data.decode("utf-8"))
def get_inputs():
    collar=_recover("rational_collar.json",_COLLAR)
    center=_recover("rational_center.json",_CENTER)
    assert len(center["z42"])==42
    return collar,center

if __name__=="__main__":
    c,z=get_inputs()
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--export-dir",type=Path)
    args=p.parse_args()
    if args.export_dir:
        args.export_dir.mkdir(parents=True,exist_ok=True)
        for name,raw in (("rational_collar.json",_COLLAR),("rational_center.json",_CENTER)):
            (args.export_dir/name).write_bytes(zlib.decompress(base64.b64decode(raw)))
    print("PASS rational inputs 3 node collar, 42-dimensional center, both SHA256")
