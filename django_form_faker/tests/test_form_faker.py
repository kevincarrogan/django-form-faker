import datetime
import pytest

from decimal import Decimal

from django import forms

from .. import form_faker


@pytest.mark.parametrize(
    "field_class,required_kwargs,expected",
    [
        (forms.BooleanField, {}, True),
        (forms.CharField, {}, "RNvnAvOpyEVAoNGn"),
        (forms.ChoiceField, {"choices": [("a", "A"), ("b", "B"), ("c", "C")]}, "b"),
        (forms.DateField, {}, "1996-03-20"),
        (forms.DateTimeField, {}, "1996-03-20T07:46:39"),
        (
            forms.DecimalField,
            {},
            Decimal(
                "-6048764759382421948924115781565938778408016097535139332871158714841858398947196593423209471122018.684833969477515917953304135256012309891013991615109032173008691413145620870916345792302"
            ),
        ),
        (forms.DurationField, {}, datetime.timedelta(18, 34345)),
        (forms.EmailField, {}, "achang@example.org"),
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
        (forms.DateField, {}, "2000-01-01"),
        (forms.DateTimeField, {}, "2000-01-01T01:01:01"),
        (forms.DecimalField, {}, "1.200320"),
        (forms.DurationField, {}, "4 1:15:20"),
        (forms.EmailField, {}, "testing@example.com"),
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
    "field_class,required_kwargs,explicit_value",
    [
        (forms.BooleanField, {}, False),
        (forms.CharField, {}, "explicit value"),
        (forms.ChoiceField, {"choices": [("a", "A"), ("b", "B"), ("c", "C")]}, "a"),
        (forms.DateField, {}, "2000-01-01"),
        (forms.DateTimeField, {}, "2000-01-01T01:01:01"),
        (forms.DecimalField, {}, "1.200320"),
        (forms.DurationField, {}, "4 1:15:20"),
        (forms.EmailField, {}, "testing@example.com"),
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
        (forms.DateTimeField, {}),
        (forms.DecimalField, {}),
        (forms.DurationField, {}),
        (forms.EmailField, {}),
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
        (forms.DateTimeField, {}, "1996-03-20T07:46:39"),
        (
            forms.DecimalField,
            {},
            Decimal(
                "-6048764759382421948924115781565938778408016097535139332871158714841858398947196593423209471122018.684833969477515917953304135256012309891013991615109032173008691413145620870916345792302"
            ),
        ),
        (forms.DurationField, {}, datetime.timedelta(18, 34345)),
        (forms.EmailField, {}, "achang@example.org"),
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
