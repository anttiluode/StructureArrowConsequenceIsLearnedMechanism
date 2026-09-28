from __future__ import annotations

import hashlib
from typing import Iterable

import numpy as np

from .config import config_digest
from .mechanism import FrozenMechanism
from .world import RouteWorld


def soft_accuracy(choice: int | None, target: int) -> float:
    if choice is None:
        return 0.5
    return float(choice == target)


def frozen_digest(frozen: FrozenMechanism) -> str:
    h = hashlib.sha256()
    for matrix in (frozen.S, frozen.A, frozen.C):
        h.update(np.ascontiguousarray(matrix).tobytes())
    h.update(config_digest(frozen.config).encode("ascii"))
    return h.hexdigest()


def evaluate_frozen(
    frozen: FrozenMechanism,
    world: RouteWorld,
    rewarded_arm: str,
    components: Iterable[str],
) -> dict[str, float | int | list[dict[str, int | str | None]]]:
    enabled = set(components)
    fork_target = world.paths[rewarded_arm][1]
    fork_choice = frozen.choose_next(world.start, enabled)
    fork_score = soft_accuracy(fork_choice, fork_target)

    records: list[dict[str, int | str | None]] = []
    interior_scores: list[float] = []
    illegal = 0
    if fork_choice is not None and frozen.S[world.start, fork_choice] <= frozen.config.atol:
        illegal += 1
    records.append({
        "role": "fork",
        "arm": rewarded_arm,
        "node": world.start,
        "choice": fork_choice,
        "target": fork_target,
    })

    for probe in world.direction_probes():
        choice = frozen.choose_next(probe.node, enabled)
        if choice is not None and frozen.S[probe.node, choice] <= frozen.config.atol:
            illegal += 1
        interior_scores.append(soft_accuracy(choice, probe.correct_next))
        records.append({
            "role": probe.role,
            "arm": probe.arm,
            "node": probe.node,
            "choice": choice,
            "target": probe.correct_next,
        })

    interior_accuracy = float(np.mean(interior_scores)) if interior_scores else 1.0
    heldout_accuracy = float(np.mean([fork_score, *interior_scores]))
    return {
        "fork_accuracy": float(fork_score),
        "interior_direction_accuracy": interior_accuracy,
        "heldout_accuracy": heldout_accuracy,
        "illegal_edge_choices": int(illegal),
        "probes": records,
    }
