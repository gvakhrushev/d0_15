from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import time


@dataclass
class Check:
    id: str
    status: str  # "PASS" / "FAIL" / "SKIP"
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CertReport:
    cert_id: str
    protocol_id: str
    created_unix: float = field(default_factory=lambda: time.time())
    checks: List[Check] = field(default_factory=list)
    artifacts: Dict[str, str] = field(default_factory=dict)  # name -> relative path

    def add(self, check_id: str, passed: bool, **details: Any) -> None:
        self.checks.append(Check(check_id, "PASS" if passed else "FAIL", details))

    def add_skip(self, check_id: str, reason: str) -> None:
        self.checks.append(Check(check_id, "SKIP", {"reason": reason}))

    def skip(self, check_id: str, reason: str) -> None:
        self.add_skip(check_id, reason)

    def ok(self) -> bool:
        return all(c.status != "FAIL" for c in self.checks)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cert_id": self.cert_id,
            "protocol_id": self.protocol_id,
            "created_unix": self.created_unix,
            "ok": self.ok(),
            "checks": [{"id": c.id, "status": c.status, "details": c.details} for c in self.checks],
            "artifacts": dict(self.artifacts),
        }
