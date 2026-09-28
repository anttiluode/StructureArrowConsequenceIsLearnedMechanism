from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .config import V0Config


def _normalized(matrix: np.ndarray) -> np.ndarray:
    scale = float(np.max(np.abs(matrix))) if matrix.size else 0.0
    if scale == 0.0:
        return matrix.astype(float, copy=True)
    return matrix.astype(float, copy=True) / scale


@dataclass(frozen=True)
class FrozenMechanism:
    S: np.ndarray
    A: np.ndarray
    C: np.ndarray
    config: V0Config

    def choose_next(self, node: int, components: Iterable[str]) -> int | None:
        enabled = set(components)
        legal = np.flatnonzero(self.S[node] > self.config.atol)
        if legal.size == 0:
            return None

        scores = np.zeros(legal.size, dtype=float)
        if "S" in enabled:
            scores += self.S[node, legal]
        if "A" in enabled:
            scores += self.A[node, legal]
        if "C" in enabled:
            scores += self.C[node, legal]

        best = float(np.max(scores))
        winners = legal[np.isclose(scores, best, atol=self.config.atol, rtol=0.0)]
        if winners.size != 1:
            return None
        return int(winners[0])


class Mechanism:
    def __init__(self, n_nodes: int, config: V0Config):
        self.config = config
        self.S = np.zeros((n_nodes, n_nodes), dtype=float)
        self.A = np.zeros((n_nodes, n_nodes), dtype=float)
        self.E = np.zeros((n_nodes, n_nodes), dtype=float)
        self.C = np.zeros((n_nodes, n_nodes), dtype=float)

    def observe(self, i: int, j: int) -> None:
        self.S[i, j] += 1.0
        self.S[j, i] += 1.0
        self.A[i, j] += 1.0
        self.A[j, i] -= 1.0
        self.E *= self.config.rho
        self.E[i, j] += 1.0
        self.E[j, i] += 1.0

    def consequence(self, reward: float) -> None:
        self.C += self.config.eta * float(reward) * self.E

    def clear_eligibility(self) -> None:
        self.E.fill(0.0)

    def snapshot(self) -> dict[str, np.ndarray]:
        return {
            "S": self.S.copy(),
            "A": self.A.copy(),
            "E": self.E.copy(),
            "C": self.C.copy(),
        }

    def freeze(self) -> FrozenMechanism:
        return FrozenMechanism(
            S=_normalized(self.S),
            A=_normalized(self.A),
            C=_normalized(self.C),
            config=self.config,
        )
