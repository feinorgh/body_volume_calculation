"""Shared fixtures for the body-volume-calculation test suite."""

import numpy as np
import pytest


@pytest.fixture()
def normal_person():
    """A representative normal-BMI adult male."""
    return {"height": 1.75, "weight": 70, "gender": "male", "age": 30}


@pytest.fixture()
def test_weights():
    """Small weight array for fast integration tests."""
    return np.array([50, 70, 90])


@pytest.fixture()
def test_heights():
    """Small height array for fast integration tests."""
    return np.array([1.60, 1.75, 1.90])
