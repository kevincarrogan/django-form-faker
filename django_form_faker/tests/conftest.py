import pytest

from faker import Faker


@pytest.fixture(autouse=True)
def seed_faker():
    Faker.seed(0)
