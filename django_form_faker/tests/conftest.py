import pytest

from django.conf import settings

from faker import Faker


@pytest.fixture(autouse=True)
def seed_faker():
    Faker.seed(0)


def pytest_configure():
    settings.configure(
        USE_L10N=False,
    )
