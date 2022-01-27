import pytest

from django import forms

from .. import form_faker


@pytest.mark.parametrize(
    "field_class,expected",
    [
        (forms.BooleanField, True),
        (forms.CharField, "RNvnAvOpyEVAoNGn"),
    ],
)
def test_random_generated_values(field_class, expected):
    class FormToTest(forms.Form):
        field_to_test = field_class()

    post_data = form_faker.get_data(FormToTest)

    assert post_data == {
        "field_to_test": expected,
    }


@pytest.mark.parametrize(
    "field_class,explicit_value",
    [
        (forms.BooleanField, False),
        (forms.CharField, "explicit value"),
    ],
)
def test_random_generated_values(field_class, explicit_value):
    class FormToTest(forms.Form):
        field_to_test = field_class()

    post_data = form_faker.get_data(FormToTest, field_to_test=explicit_value)

    assert post_data == {
        "field_to_test": explicit_value,
    }


@pytest.mark.parametrize(
    "field_class",
    [
        forms.BooleanField,
        forms.CharField,
    ],
)
def test_not_required(field_class):
    class FormToTest(forms.Form):
        field_to_test = field_class(required=False)

    post_data = form_faker.get_data(FormToTest)

    assert post_data == {}
