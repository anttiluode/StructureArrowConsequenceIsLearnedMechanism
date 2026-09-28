from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Probe:
    node: int
    correct_next: int
    arm: str
    role: str


@dataclass(frozen=True)
class RouteWorld:
    paths: dict[str, tuple[int, ...]]
    start: int = 0

    @property
    def n_nodes(self) -> int:
        return 1 + max(node for path in self.paths.values() for node in path)

    def train_episode(self, arm: str, reversed: bool = False) -> list[tuple[int, int]]:
        path = self.paths[arm]
        if reversed:
            path = path[::-1]
        return list(zip(path, path[1:]))

    def direction_probes(self) -> list[Probe]:
        probes: list[Probe] = []
        for arm, path in self.paths.items():
            for node, nxt in zip(path[1:-1], path[2:]):
                probes.append(Probe(node=node, correct_next=nxt, arm=arm, role="interior"))
        return probes


def make_v0_world() -> RouteWorld:
    return RouteWorld(paths={"A": (0, 1, 2, 3), "B": (0, 4, 5, 6)})


def reversal_histories() -> tuple[list[int], list[int]]:
    forward = [0, 1, 2]
    return forward, list(reversed(forward))


def train_balanced_history(
    world: RouteWorld,
    mechanism,
    rewarded_arm: str,
    seed: int,
    shuffle_consequence: bool = False,
) -> list[tuple[str, float]]:
    """Present equal A/B histories; deliver one delayed outcome at each terminal."""
    import numpy as np

    arms = ["A"] * mechanism.config.episodes_per_arm + ["B"] * mechanism.config.episodes_per_arm
    rng = np.random.default_rng(seed)
    rng.shuffle(arms)
    rewards = np.asarray([1.0 if arm == rewarded_arm else -1.0 for arm in arms], dtype=float)
    if shuffle_consequence:
        rewards = rng.permutation(rewards)

    ledger: list[tuple[str, float]] = []
    for arm, reward in zip(arms, rewards.tolist()):
        mechanism.clear_eligibility()
        for i, j in world.train_episode(arm):
            mechanism.observe(i, j)
        mechanism.consequence(reward)
        ledger.append((arm, reward))
    return ledger
