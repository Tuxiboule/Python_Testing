import pytest
from app import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app.config['TESTING'] = False
    client = app.test_client()
    yield client


@pytest.fixture
def clubs():
    clubs = loadClubs()
    return clubs


@pytest.fixture
def competitions():
    competitions = loadCompetitions()
    return competitions
