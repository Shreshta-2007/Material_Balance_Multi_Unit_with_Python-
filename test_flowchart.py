import numpy as np
import pytest
from flowsheet import fresh_feed, solve_matrix, solve_iterative

FRESH = fresh_feed(100, 0.10, 50, 0.60)


def test_overall_balance_closes():
    s = solve_matrix(FRESH, 0.95, 0.80, 0.5)
    assert np.allclose(FRESH, s["s4"] + s["s7"])


def test_matrix_and_iteration_agree():
    a = solve_matrix(FRESH, 0.95, 0.80, 0.5)
    b, _ = solve_iterative(FRESH, 0.95, 0.80, 0.5)
    for k in a:
        assert np.allclose(a[k], b[k])


def test_no_recycle_means_mixer_sees_only_fresh_feed():
    s = solve_matrix(FRESH, 0.95, 0.80, 0.0)
    assert np.allclose(s["s3"], FRESH)
    assert np.allclose(s["s6"], 0)


def test_distillate_meets_specs():
    s = solve_matrix(FRESH, 0.95, 0.80, 0.5)
    assert s["s4"][0] / s["s3"][0] == pytest.approx(0.95)
    assert s["s4"][0] / s["s4"].sum() == pytest.approx(0.80)


def test_full_recycle_has_no_solution():
    with pytest.raises(ValueError):
        solve_matrix(FRESH, 0.95, 0.80, 1.0)
