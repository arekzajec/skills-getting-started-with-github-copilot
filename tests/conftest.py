import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Restore the in-memory `activities` dict after each test so tests are isolated.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))
