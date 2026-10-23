"""SHA256-pinned rational-decimal 42-center of new original FULL TWO-FLAG N1 CQ root.

Reproduction bytes only. The old original h0 three-node rational collar
comes UNCHANGED from d0_full42_interval_banach_2026-10-22/inputs.py.
Compressed to keep all 42 ~65-decimal strings in one small source.
"""
from __future__ import annotations
import base64, hashlib, json, zlib

_COMPRESSED = (
"eNqtl81uW0cMhfd5CkHr2Bj+DMnpsps+RFEUrq0GRhUr8A+Ktui796OTwJaWxQ0QQL66Q3LOOTyk/vmw2+3/dt3/sPuZj/wxrseac3pNk5jTxqjyOVI0aomOSBm53F0t04cP1TmU12XWTF/mUfuPX2NdEYx/RNNaI8TCcw3CmLjkEg8bObVk2Updob7W4LMtMlaFmq8ppd/jES6XustYkV5FSh9SReI+oclx17FKKsuCQJZWRmivoSbkyk1iScYofx9r6JpWOSPVpq0a5jplESjM51qT2/ASKA3xxmAqEaKT1vJhb6B1sCADh5cm0EaAoE1PgEvLYcA1Zko40KU5aUHfgLFMRTMh6X2wEVxbOJ4FqFw5qKbMdGaU9pWCq1Iq8HC8EiiGe6q6QVqYbRNtjtbPfAsWAagAXohBBQSVyMAXiGwKX65yhIU0uNyCPx4FDBFcYoylZ3WBroFqJDXPsFw5ZzS7AlhUs1qDGko+aqKkUdAoMgxsuQgp3+tWUfLoYsKCmEmdPsFWxCF5OBoeUVwLRXP3hKFm1wsFvEZ9X5ybRqgsLoGY3My5KK8iQFBRQSA15iCCgyt/mDrPKZAcMJ8bgOYrnVNrG9DoSkrHKGKje2IyKGUbBqq19lbZVxviOzpnUQynTbSwhEFLtz4pZAjVSyg2102n4Yp+pW2jKFbqnXBt0sPx+r+oy8kMwHSF22qf0Eari27f6NBNzMpSoMT2cpNIdPusczLTFn2BmGlF4MFyFA8XAMR3s81JmiOsA6RaId6ywPZM8EYg3SacAbGgy7d+yutVmct6lGCd+BskMDnS2/LxMdxWV2JfjnXAUfsLBpdwg7CR0uEqztoT+nsi6TA8ejVzbtRILICkMMSmbY0IBWcGPhhEnRTF7MoEyIs+WAEF3bs0HHLlg4J79dURBIOIkdWe1uItadeOBVPDSUyS5RvFyy4Wo8xz9RY3Xq2fnpUgKIabcgawmiBocMYJTtbyJgdTgkHD7KWne6RtFQ678PaF7+HqmkaG28COYBYV0PX0JdONtDQs0Wn+KYikBIpmbxFzFvwoaUNg9sLIxek7Gjns1ccwMqyMFUJBBrfGdUa3CR090OSEXrwEYvGciRzjnFrp6cjD2d1FS0m/DAFj0knhtBYmpK9ehJnwtBcfe+UGGYPOGXKYD1UNPLCYb5ST3RctAFmAxLQnBFdr28DYJo0cI3u6hJPhTSbfdiOEQmcBiIO8sVnQZFietawJhw2ICFXD1mxOcIXslmuXILOPS/BoDJYycjXugNifs8cC6sPvOIXZsCE0U91Bk+bBaaAFDSsFnA+I6LSR0Spi6eulBHS4LyeE9kUytKknmwKmgKqHgS0DGrNK4N2KWiyA1hlbkUGdONnaRihQt3rF2YYISmsEGGYbSYXWTtoPS7yYiP+b2zZZTPTCU5T2hwsjVC+8/Djg7qz9PSvYsBnnvDKp2XsNbECaYRZp+gzgfV7cF6tZvdJyHOvsmdDrLTWySlISLwiw9hICJ5TH4sIrXAhwMKlpe8L90jH3j4en+7uXm+OvDy+fD4/3tzdHfvDs85qFBL5JjVT6V0wPi+jfIjBch6tvNrd/uj19OfSJ0+P9p/uHm+Pu+c/T7vHwfHP/cLjb/XQ63h0edr/xzeNfu9+PN5+ePu4eTs+729PnLy/HpxNPfzyd/mAn/PDvf5w2sT0="
)
_SHA256 = "12d6272174485ec1fa1eeb0b09960c105de4cb44b31f7cf4a81beaad06d95aaf"
def get_center() -> list[str]:
    raw = zlib.decompress(base64.b64decode(_COMPRESSED))
    assert hashlib.sha256(raw).hexdigest() == _SHA256
    obj = json.loads(raw.decode("utf-8"))
    assert len(obj["z42"]) == 42
    return obj["z42"]

if __name__ == "__main__":
    print("PASS original full 42-field rational center, SHA256", _SHA256)
    print("first and last", get_center()[0], get_center()[-1])
