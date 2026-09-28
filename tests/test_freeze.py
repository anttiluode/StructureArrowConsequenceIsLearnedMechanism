from sac.config import V0Config
from sac.mechanism import Mechanism
from sac.metrics import evaluate_frozen, frozen_digest
from sac.world import make_v0_world, train_balanced_history
from experiment import run_v0


COMPONENT_SETS = [
    {"S"}, {"A"}, {"C"}, {"S", "A"}, {"S", "C"}, {"A", "C"}, {"S", "A", "C"}
]


def _trained(rewarded_arm="A", seed=0):
    config = V0Config()
    world = make_v0_world()
    mechanism = Mechanism(world.n_nodes, config)
    train_balanced_history(world, mechanism, rewarded_arm, seed)
    return world, mechanism.freeze()


def test_full_sac_executes_frozen_fork_and_direction_without_mutation():
    world, frozen = _trained("A", seed=11)
    before = frozen_digest(frozen)
    scores = evaluate_frozen(frozen, world, rewarded_arm="A", components={"S", "A", "C"})
    after = frozen_digest(frozen)

    assert scores["fork_accuracy"] == 1.0
    assert scores["interior_direction_accuracy"] == 1.0
    assert scores["heldout_accuracy"] == 1.0
    assert before == after


def test_matched_ablations_isolate_value_and_direction():
    world, frozen = _trained("A", seed=5)
    sa = evaluate_frozen(frozen, world, "A", {"S", "A"})
    sc = evaluate_frozen(frozen, world, "A", {"S", "C"})
    full = evaluate_frozen(frozen, world, "A", {"S", "A", "C"})

    assert sa["fork_accuracy"] == 0.5
    assert sc["interior_direction_accuracy"] == 0.5
    assert full["heldout_accuracy"] == 1.0


def test_executor_never_chooses_an_edge_absent_from_structure():
    world, frozen = _trained("B", seed=2)
    terminals = {world.paths["A"][-1], world.paths["B"][-1]}
    for components in COMPONENT_SETS:
        for node in range(world.n_nodes):
            if node in terminals:
                continue
            choice = frozen.choose_next(node, components)
            if choice is not None:
                assert frozen.S[node, choice] > frozen.config.atol


def test_v0_aggregate_meets_predeclared_gate_thresholds():
    receipt = run_v0(V0Config())

    assert receipt["gates"]["S"]["pass"] is True
    assert receipt["gates"]["A"]["pass"] is True
    assert receipt["gates"]["SAC"]["pass"] is True
    assert receipt["gates"]["SAC"]["full_heldout_accuracy"] >= 0.90
    assert receipt["gates"]["SAC"]["sa_fork_accuracy"] <= 0.625
    assert receipt["gates"]["SAC"]["sc_interior_direction_accuracy"] <= 0.625
    assert receipt["gates"]["SAC"]["shuffled_fork_accuracy"] <= 0.625
    assert receipt["freeze_integrity"] is True
    assert receipt["illegal_edge_choices"] == 0


def test_frozen_matrices_reject_external_mutation():
    import pytest

    _, frozen = _trained("A", seed=0)
    for matrix in (frozen.S, frozen.A, frozen.C):
        assert matrix.flags.writeable is False
        with pytest.raises(ValueError):
            matrix[0, 0] = 123.0
