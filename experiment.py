from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
from typing import Iterable

import numpy as np

from sac.config import V0Config, config_digest
from sac.mechanism import Mechanism
from sac.metrics import evaluate_frozen, frozen_digest, soft_accuracy
from sac.world import make_v0_world, reversal_histories, train_balanced_history


COMPONENTS: dict[str, set[str]] = {
    "S": {"S"},
    "A": {"A"},
    "C": {"C"},
    "S+A": {"S", "A"},
    "S+C": {"S", "C"},
    "A+C": {"A", "C"},
    "S+A+C": {"S", "A", "C"},
}


def _mean(records: list[dict], key: str) -> float:
    return float(np.mean([float(record[key]) for record in records]))


def run_seed(
    seed: int,
    rewarded_arm: str,
    shuffle_consequence: bool = False,
    config: V0Config | None = None,
) -> dict:
    config = config or V0Config()
    world = make_v0_world()
    mechanism = Mechanism(world.n_nodes, config)
    train_balanced_history(
        world,
        mechanism,
        rewarded_arm=rewarded_arm,
        seed=seed,
        shuffle_consequence=shuffle_consequence,
    )
    frozen = mechanism.freeze()
    before = frozen_digest(frozen)
    detailed = {
        name: evaluate_frozen(frozen, world, rewarded_arm, components)
        for name, components in COMPONENTS.items()
    }
    evaluations = {
        name: {
            "fork_accuracy": values["fork_accuracy"],
            "interior_direction_accuracy": values["interior_direction_accuracy"],
            "heldout_accuracy": values["heldout_accuracy"],
            "illegal_edge_choices": values["illegal_edge_choices"],
        }
        for name, values in detailed.items()
    }
    after = frozen_digest(frozen)
    return {
        "seed": int(seed),
        "rewarded_arm": rewarded_arm,
        "shuffle_consequence": bool(shuffle_consequence),
        "evaluations": evaluations,
        "freeze_integrity": before == after,
        "illegal_edge_choices": int(sum(e["illegal_edge_choices"] for e in evaluations.values())),
    }


def _gate_s(config: V0Config) -> dict:
    forward, reverse = reversal_histories()
    fwd_m = Mechanism(3, config)
    rev_m = Mechanism(3, config)
    for i, j in zip(forward, forward[1:]):
        fwd_m.observe(i, j)
    for i, j in zip(reverse, reverse[1:]):
        rev_m.observe(i, j)
    fwd = fwd_m.freeze()
    rev = rev_m.freeze()
    s_error = float(np.max(np.abs(fwd.S - rev.S)))
    a_flip_error = float(np.max(np.abs(fwd.A + rev.A)))
    middle = forward[1]
    s_accuracy = float(np.mean([
        soft_accuracy(fwd.choose_next(middle, {"S"}), forward[2]),
        soft_accuracy(rev.choose_next(middle, {"S"}), reverse[2]),
    ]))
    sa_accuracy = float(np.mean([
        soft_accuracy(fwd.choose_next(middle, {"S", "A"}), forward[2]),
        soft_accuracy(rev.choose_next(middle, {"S", "A"}), reverse[2]),
    ]))
    passed = (
        s_error <= config.atol
        and a_flip_error <= config.atol
        and s_accuracy == 0.5
        and sa_accuracy == 1.0
    )
    return {
        "pass": bool(passed),
        "structure_reversal_max_abs_error": s_error,
        "arrow_sign_flip_max_abs_error": a_flip_error,
        "s_only_direction_accuracy": s_accuracy,
        "s_plus_a_direction_accuracy": sa_accuracy,
    }


def _reward_reassignment_diagnostics(config: V0Config) -> dict:
    world = make_v0_world()
    s_errors: list[float] = []
    a_errors: list[float] = []
    c_distances: list[float] = []
    for seed in range(config.seeds):
        ma = Mechanism(world.n_nodes, config)
        mb = Mechanism(world.n_nodes, config)
        train_balanced_history(world, ma, "A", seed)
        train_balanced_history(world, mb, "B", seed)
        sa, sb = ma.snapshot(), mb.snapshot()
        s_errors.append(float(np.max(np.abs(sa["S"] - sb["S"]))))
        a_errors.append(float(np.max(np.abs(sa["A"] - sb["A"]))))
        c_distances.append(float(np.linalg.norm(sa["C"] - sb["C"])))
    return {
        "max_structure_error": max(s_errors),
        "max_arrow_error": max(a_errors),
        "min_consequence_distance": min(c_distances),
        "mean_consequence_distance": float(np.mean(c_distances)),
    }


def run_v0(config: V0Config = V0Config()) -> dict:
    correct: list[dict] = []
    shuffled: list[dict] = []
    for seed in range(config.seeds):
        rewarded_arm = "A" if seed % 2 == 0 else "B"
        correct.append(run_seed(seed, rewarded_arm, False, config))
        shuffled.append(run_seed(seed, rewarded_arm, True, config))

    component_summary: dict[str, dict[str, float]] = {}
    for name in COMPONENTS:
        evals = [record["evaluations"][name] for record in correct]
        component_summary[name] = {
            "fork_accuracy": _mean(evals, "fork_accuracy"),
            "interior_direction_accuracy": _mean(evals, "interior_direction_accuracy"),
            "heldout_accuracy": _mean(evals, "heldout_accuracy"),
        }

    shuffled_full = [record["evaluations"]["S+A+C"] for record in shuffled]
    shuffled_fork = _mean(shuffled_full, "fork_accuracy")
    gate_s = _gate_s(config)
    reassignment = _reward_reassignment_diagnostics(config)

    full_fork = component_summary["S+A+C"]["fork_accuracy"]
    sa_fork = component_summary["S+A"]["fork_accuracy"]
    gate_a_pass = (
        reassignment["max_structure_error"] <= config.atol
        and reassignment["max_arrow_error"] <= config.atol
        and reassignment["min_consequence_distance"] > config.atol
        and full_fork >= 0.90
        and sa_fork <= 0.625
        and shuffled_fork <= 0.625
    )

    full_heldout = component_summary["S+A+C"]["heldout_accuracy"]
    sc_interior = component_summary["S+C"]["interior_direction_accuracy"]
    gate_sac_pass = (
        full_heldout >= 0.90
        and sa_fork <= 0.625
        and sc_interior <= 0.625
        and shuffled_fork <= 0.625
    )

    freeze_integrity = all(r["freeze_integrity"] for r in [*correct, *shuffled])
    illegal_edge_choices = int(sum(r["illegal_edge_choices"] for r in [*correct, *shuffled]))

    return {
        "config": asdict(config),
        "config_digest": config_digest(config),
        "seeds": list(range(config.seeds)),
        "gates": {
            "S": gate_s,
            "A": {
                "pass": bool(gate_a_pass),
                **reassignment,
                "full_fork_accuracy": full_fork,
                "sa_fork_accuracy": sa_fork,
                "shuffled_fork_accuracy": shuffled_fork,
            },
            "SAC": {
                "pass": bool(gate_sac_pass),
                "full_heldout_accuracy": full_heldout,
                "sa_fork_accuracy": sa_fork,
                "sc_interior_direction_accuracy": sc_interior,
                "shuffled_fork_accuracy": shuffled_fork,
            },
        },
        "components": component_summary,
        "shuffled_full": {
            "fork_accuracy": shuffled_fork,
            "interior_direction_accuracy": _mean(shuffled_full, "interior_direction_accuracy"),
            "heldout_accuracy": _mean(shuffled_full, "heldout_accuracy"),
        },
        "freeze_integrity": bool(freeze_integrity),
        "illegal_edge_choices": illegal_edge_choices,
        "per_seed": [
            {
                "seed": r["seed"],
                "rewarded_arm": r["rewarded_arm"],
                "full_heldout_accuracy": r["evaluations"]["S+A+C"]["heldout_accuracy"],
                "full_fork_accuracy": r["evaluations"]["S+A+C"]["fork_accuracy"],
                "sa_fork_accuracy": r["evaluations"]["S+A"]["fork_accuracy"],
                "sc_interior_direction_accuracy": r["evaluations"]["S+C"]["interior_direction_accuracy"],
                "freeze_integrity": r["freeze_integrity"],
                "illegal_edge_choices": r["illegal_edge_choices"],
            }
            for r in correct
        ],
        "per_seed_shuffled": [
            {
                "seed": r["seed"],
                "rewarded_arm": r["rewarded_arm"],
                "full_fork_accuracy": r["evaluations"]["S+A+C"]["fork_accuracy"],
                "freeze_integrity": r["freeze_integrity"],
                "illegal_edge_choices": r["illegal_edge_choices"],
            }
            for r in shuffled
        ],
    }


def _canonical_json(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the frozen Structure/Arrow/Consequence v0 receipt")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-receipt", type=Path)
    args = parser.parse_args(list(argv) if argv is not None else None)

    receipt = run_v0()
    rendered = _canonical_json(receipt)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    if args.check_receipt:
        expected = args.check_receipt.read_text(encoding="utf-8")
        if expected != rendered:
            print("receipt drift")
            return 1
    if not args.output and not args.check_receipt:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
