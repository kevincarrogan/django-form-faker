import pytest

from faker import Faker
from freezegun import freeze_time

import django
from django.conf import settings


@pytest.fixture(autouse=True)
def seed_faker():
    Faker.seed(0)


@pytest.fixture(autouse=True)
def froze_time():
    with freeze_time("2022-01-01"):
        yield


def pytest_configure():
    settings.configure(
        USE_L10N=False,
    )
    django.setup()
