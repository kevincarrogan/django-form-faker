import pytest

from django import forms

from .. import form_faker


@pytest.mark.parametrize(
    "field_class,required_kwargs,expected",
    [
        (forms.BooleanField, {}, True),
        (forms.CharField, {}, "RNvnAvOpyEVAoNGn"),
        (forms.ChoiceField, {"choices": [("a", "A"), ("b", "B"), ("c", "C")]}, "b"),
        (forms.DateField, {}, "1996-03-20"),
    ],
)
def test_random_generated_values(field_class, required_kwargs, expected):
    class FormToTest(forms.Form):
        field_to_test = field_class(**required_kwargs)

    post_data = form_faker.get_data(FormToTest)

    assert post_data == {
        "field_to_test": expected,
    }

    form = FormToTest(data=post_data)
    assert form.is_valid()


@pytest.mark.parametrize(
    "field_class,required_kwargs,explicit_value",
    [
        (forms.BooleanField, {}, False),
        (forms.CharField, {}, "explicit value"),
        (forms.ChoiceField, {"choices": [("a", "A"), ("b", "B"), ("c", "C")]}, "a"),
        (forms.DateField, {}, "2000-01-01"),    ],
)
def test_explicit_values(field_class, required_kwargs, explicit_value):
    class FormToTest(forms.Form):
        field_to_test = field_class(**required_kwargs)

    post_data = form_faker.get_data(FormToTest, field_to_test=explicit_value)

    assert post_data == {
        "field_to_test": explicit_value,
    }


@pytest.mark.parametrize(
    "field_class,required_kwargs,explicit_value",
    [
        (forms.BooleanField, {}, False),
        (forms.CharField, {}, "explicit value"),
        (forms.ChoiceField, {"choices": [("a", "A"), ("b", "B"), ("c", "C")]}, "a"),
        (forms.DateField, {}, "2000-01-01"),
    ],
)
def test_explicit_values_on_optional_fields(
    field_class,
    required_kwargs,
    explicit_value,
):
    class FormToTest(forms.Form):
        field_to_test = field_class(required=False, **required_kwargs)

    post_data = form_faker.get_data(FormToTest, field_to_test=explicit_value)

    assert post_data == {
        "field_to_test": explicit_value,
    }


@pytest.mark.parametrize(
    "field_class,required_kwargs",
    [
        (forms.BooleanField, {}),
        (forms.CharField, {}),
        (forms.ChoiceField, {"choices": [("a", "A"), ("b", "B"), ("c", "C")]}),
        (forms.DateField, {}),
    ],
)
def test_not_required(field_class, required_kwargs):
    class FormToTest(forms.Form):
        field_to_test = field_class(required=False, **required_kwargs)

    post_data = form_faker.get_data(FormToTest)

    assert post_data == {}


@pytest.mark.parametrize(
    "field_class,required_kwargs,expected",
    [
        (forms.BooleanField, {}, True),
        (forms.CharField, {}, "RNvnAvOpyEVAoNGn"),
        (forms.ChoiceField, {"choices": [("a", "A"), ("b", "B"), ("c", "C")]}, "b"),
        (forms.DateField, {}, "1996-03-20"),
    ],
)
def test_optional_fields_with_include_optional_override(
    field_class,
    required_kwargs,
    expected,
):
    class FormToTest(forms.Form):
        field_to_test = field_class(required=False, **required_kwargs)

    post_data = form_faker.get_data(FormToTest, _include_optional=True)

    assert post_data == {
        "field_to_test": expected,
    }
