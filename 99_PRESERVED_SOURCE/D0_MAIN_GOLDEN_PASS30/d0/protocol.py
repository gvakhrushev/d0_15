from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Protocol:
    protocol_id: str
    params: Dict[str, Any]


def load_protocol(path: str | Path) -> Protocol:
    p = Path(path)
    obj = json.loads(p.read_text(encoding="utf-8"))
    if "protocol_id" not in obj or "params" not in obj:
        raise ValueError("Protocol json must contain keys: protocol_id, params")
    return Protocol(protocol_id=obj["protocol_id"], params=obj["params"])


def get(obj: Protocol, key: str, default: Optional[Any] = None) -> Any:
    return obj.params.get(key, default)


def P(prot: Protocol, key: str, default: Optional[Any] = None) -> Any:
    return prot.params.get(key, default)
