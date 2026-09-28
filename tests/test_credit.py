import numpy as np

from sac.config import V0Config
from sac.mechanism import Mechanism
from sac.world import make_v0_world, train_balanced_history


def _arm_mass(matrix, path):
    return sum(matrix[i, j] for i, j in zip(path, path[1:]))


def _tie_as_chance(choice, target):
    return 0.5 if choice is None else float(choice == target)


def test_reward_reassignment_changes_consequence_not_structure_or_arrow():
    config = V0Config()
    world = make_v0_world()

    mech_a = Mechanism(world.n_nodes, config)
    mech_b = Mechanism(world.n_nodes, config)
    train_balanced_history(world, mech_a, rewarded_arm="A", seed=7)
    train_balanced_history(world, mech_b, rewarded_arm="B", seed=7)

    snap_a = mech_a.snapshot()
    snap_b = mech_b.snapshot()
    np.testing.assert_allclose(snap_a["S"], snap_b["S"], atol=config.atol)
    np.testing.assert_allclose(snap_a["A"], snap_b["A"], atol=config.atol)
    assert not np.allclose(snap_a["C"], snap_b["C"], atol=config.atol)

    a_path = world.paths["A"]
    b_path = world.paths["B"]
    assert _arm_mass(snap_a["C"], a_path) > _arm_mass(snap_a["C"], b_path)
    assert _arm_mass(snap_b["C"], b_path) > _arm_mass(snap_b["C"], a_path)


def test_direction_only_cannot_choose_value_but_full_sac_can():
    config = V0Config()
    world = make_v0_world()
    for rewarded_arm in ("A", "B"):
        mech = Mechanism(world.n_nodes, config)
        train_balanced_history(world, mech, rewarded_arm=rewarded_arm, seed=3)
        frozen = mech.freeze()
        target = world.paths[rewarded_arm][1]
        assert _tie_as_chance(frozen.choose_next(world.start, {"S", "A"}), target) == 0.5
        assert _tie_as_chance(frozen.choose_next(world.start, {"S", "A", "C"}), target) == 1.0


def test_shuffled_consequence_destroys_reliable_route_value():
    config = V0Config()
    world = make_v0_world()
    correct = []
    shuffled = []
    for seed in range(config.seeds):
        rewarded_arm = "A" if seed % 2 == 0 else "B"
        target = world.paths[rewarded_arm][1]

        mech = Mechanism(world.n_nodes, config)
        train_balanced_history(world, mech, rewarded_arm, seed, shuffle_consequence=False)
        correct.append(_tie_as_chance(mech.freeze().choose_next(0, {"S", "A", "C"}), target))

        control = Mechanism(world.n_nodes, config)
        train_balanced_history(world, control, rewarded_arm, seed, shuffle_consequence=True)
        shuffled.append(_tie_as_chance(control.freeze().choose_next(0, {"S", "A", "C"}), target))

    assert np.mean(correct) >= 0.90
    assert np.mean(shuffled) <= 0.625
