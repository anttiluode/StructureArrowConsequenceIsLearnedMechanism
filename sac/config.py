from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json


@dataclass(frozen=True)
class V0Config:
    rho: float = 0.8
    eta: float = 1.0
    seeds: int = 32
    episodes_per_arm: int = 8
    atol: float = 1e-12


def config_digest(config: V0Config) -> str:
    payload = json.dumps(asdict(config), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
