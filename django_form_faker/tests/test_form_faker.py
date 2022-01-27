import pytest

from django import forms

from .. import form_faker


@pytest.mark.parametrize(
    "field_class,required_kwargs,expected",
    [
        (forms.BooleanField, {}, True),
        (forms.CharField, {}, "RNvnAvOpyEVAoNGn"),
        (forms.ChoiceField, {"choices": ["a", "b", "c"]}, "b"),
    ],
)
def test_random_generated_values(field_class, required_kwargs, expected):
    class FormToTest(forms.Form):
        field_to_test = field_class(**required_kwargs)

    post_data = form_faker.get_data(FormToTest)

    assert post_data == {
        "field_to_test": expected,
    }


@pytest.mark.parametrize(
    "field_class,required_kwargs,explicit_value",
    [
        (forms.BooleanField, {}, False),
        (forms.CharField, {}, "explicit value"),
        (forms.ChoiceField, {"choices": ["a", "b", "c"]}, "a"),
    ],
)
def test_explicit_values(field_class, required_kwargs, explicit_value):
    class FormToTest(forms.Form):
        field_to_test = field_class(**required_kwargs)

    post_data = form_faker.get_data(FormToTest, field_to_test=explicit_value)

    assert post_data == {
        "field_to_test": explicit_value,
    }


@pytest.mark.parametrize(
    "field_class,required_kwargs",
    [
        (forms.BooleanField, {}),
        (forms.CharField, {}),
        (forms.ChoiceField, {"choices": ["a", "b", "c"]}),
    ],
)
def test_not_required(field_class, required_kwargs):
    class FormToTest(forms.Form):
        field_to_test = field_class(required=False, **required_kwargs)

    post_data = form_faker.get_data(FormToTest)

    assert post_data == {}
