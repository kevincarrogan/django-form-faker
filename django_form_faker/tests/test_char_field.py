import pytest

from faker import Faker
from django import forms

from .. import form_faker


@pytest.fixture(autouse=True)
def seed_faker():
    Faker.seed(0)


def test_char_field_max_length():
    class CharFieldForm(forms.Form):
        char_field = forms.CharField(max_length=2)

    post_data = form_faker.get_data(CharFieldForm)

    assert post_data == {
        "char_field": "RN",
    }


def test_char_field_min_length():
    class CharFieldForm(forms.Form):
        char_field = forms.CharField(min_length=50)

    post_data = form_faker.get_data(CharFieldForm)

    assert post_data == {
        "char_field": "RNvnAvOpyEVAoNGnVZQUqLUJyfwFVYySnPCaLuQIazTmqTjDmY",
    }


def test_char_field_min_and_max_length():
    class CharFieldForm(forms.Form):
        char_field = forms.CharField(min_length=2, max_length=50)

    post_data = form_faker.get_data(CharFieldForm)

    assert post_data == {
        "char_field": "RNvnAvOpyEVAoNGnVZQUqLUJyfwFVYySnPCaLuQIazTmqTjDmY",
    }
