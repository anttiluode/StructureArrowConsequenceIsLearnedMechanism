import numpy as np

from sac.config import V0Config
from sac.mechanism import Mechanism


def _train(path, repeats=1):
    mech = Mechanism(3, V0Config())
    for _ in range(repeats):
        for i, j in zip(path, path[1:]):
            mech.observe(i, j)
    return mech


def test_component_algebraic_invariants():
    mech = Mechanism(4, V0Config())
    for i, j in [(0, 1), (1, 2), (2, 1), (1, 3)]:
        mech.observe(i, j)
    mech.consequence(1.0)
    snap = mech.snapshot()

    np.testing.assert_allclose(snap["S"], snap["S"].T, atol=1e-12)
    np.testing.assert_allclose(snap["E"], snap["E"].T, atol=1e-12)
    np.testing.assert_allclose(snap["C"], snap["C"].T, atol=1e-12)
    np.testing.assert_allclose(snap["A"], -snap["A"].T, atol=1e-12)
    np.testing.assert_allclose(np.diag(snap["A"]), 0.0, atol=1e-12)


def test_reversal_preserves_structure_and_flips_arrow():
    fwd = _train([0, 1, 2]).freeze()
    rev = _train([2, 1, 0]).freeze()

    np.testing.assert_allclose(fwd.S, rev.S, atol=1e-12)
    np.testing.assert_allclose(fwd.A, -rev.A, atol=1e-12)


def test_repeated_traversal_preserves_normalized_arrow_semantics():
    once = _train([0, 1, 2], repeats=1).freeze()
    triple = _train([0, 1, 2], repeats=3).freeze()

    np.testing.assert_array_equal(np.sign(once.A), np.sign(triple.A))
    np.testing.assert_allclose(once.A, triple.A, atol=1e-12)
    assert once.choose_next(1, {"S", "A"}) == 2
    assert triple.choose_next(1, {"S", "A"}) == 2
