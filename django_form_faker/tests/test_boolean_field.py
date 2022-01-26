import pytest

from faker import Faker
from django import forms

from .. import form_faker


@pytest.fixture(autouse=True)
def seed_faker():
    Faker.seed(0)


def test_boolean_field():
    class BooleanFieldForm(forms.Form):
        boolean_field = forms.BooleanField()

    post_data = form_faker.get_data(BooleanFieldForm)

    assert post_data == {
        "boolean_field": True,
    }


def test_boolean_field_explicit_value():
    class BooleanFieldForm(forms.Form):
        boolean_field = forms.BooleanField()

    post_data = form_faker.get_data(BooleanFieldForm, boolean_field=False)

    assert post_data == {
        "boolean_field": False,
    }


def test_boolean_field_not_required():
    class BooleanFieldForm(forms.Form):
        boolean_field = forms.BooleanField(required=False)

    post_data = form_faker.get_data(BooleanFieldForm)

    assert post_data == {}
