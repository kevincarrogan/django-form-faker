import datetime
import pytest

from decimal import Decimal
from pathlib import Path

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
        (forms.FloatField, {}, -6.36438676418356),
        (forms.GenericIPAddressField, {}, "171.174.170.81"),
        (forms.IntegerField, {}, 6311),
        (
            forms.JSONField,
            {},
            '[{"name": "Norma Fisher", "residency": "4759 William Haven Apt. 194\\nWest Corey, TX 43780"}, {"name": "Brian Hamilton", "residency": "778 Brown Plaza\\nNorth Jenniferfurt, WY 88077"}, {"name": "Lisa Clayton", "residency": "139 John Divide Suite 115\\nRodriguezside, VT 16860"}, {"name": "Robin Fernandez", "residency": "USNV Wallace\\nFPO AP 50950"}, {"name": "David White", "residency": "471 Erika Curve\\nNorth Megan, UT 71358"}, {"name": "Sara Warren", "residency": "96947 Keller Squares\\nChristopherville, OR 83095"}, {"name": "Connor Smith", "residency": "2560 Krista Walk\\nNorth Lisa, ND 79428"}, {"name": "Alyssa Reid", "residency": "1510 James Ferry\\nSouth Jasonton, AK 71835"}, {"name": "Brian Green", "residency": "6208 Williams Courts Suite 345\\nMasseyshire, UT 88665"}, {"name": "Randall Kramer", "residency": "8419 Wade Bridge\\nMaldonadoshire, NY 41322"}]',
        ),
        (
            forms.MultipleChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
            ["b", "a"],
        ),
        (forms.NullBooleanField, {}, False),
        (forms.SlugField, {}, "three-image-son"),
        (forms.TimeField, {}, "07:46:39"),
        (
            forms.TypedChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
            "b",
        ),
        (forms.URLField, {}, "https://green.info/"),
        (forms.UUIDField, {}, "e3e70682-c209-4cac-a29f-6fbed82c07cd"),
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
    assert form.is_valid(), f"Invalid with {form.errors}"


@pytest.mark.parametrize(
    "field_class",
    [
        forms.FileField,
    ],
)
def test_random_generated_files(field_class):
    class FormToTest(forms.Form):
        non_file_field = forms.CharField()
        file_field = field_class()

    post_data = form_faker.get_data(FormToTest)
    assert "file_field" not in post_data

    files_data = form_faker.get_files(FormToTest)
    assert "non_file_field" not in files_data

    file_data = files_data["file_field"]
    current_path = Path(__file__).parent
    test_data_path = current_path / "data" / "random_binary_file"
    with open(test_data_path, "rb") as test_data_file:
        assert file_data.read() == test_data_file.read()
    assert file_data.name == "test_file"

    form = FormToTest(data=post_data, files=files_data)
    assert form.is_valid(), f"Invalid with {form.errors}"


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
        (forms.FloatField, {}, 1.5),
        (forms.GenericIPAddressField, {}, "192.0.2.1"),
        (forms.IntegerField, {}, 42),
        (forms.JSONField, {}, '{"explicit": true}'),
        (
            forms.MultipleChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
            ["a", "c"],
        ),
        (forms.NullBooleanField, {}, None),
        (forms.SlugField, {}, "explicit-slug"),
        (forms.TimeField, {}, "12:34:56"),
        (
            forms.TypedChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
            "a",
        ),
        (forms.URLField, {}, "https://example.com/"),
        (forms.UUIDField, {}, "12345678-1234-5678-1234-567812345678"),
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
        (forms.FloatField, {}, 1.5),
        (forms.GenericIPAddressField, {}, "192.0.2.1"),
        (forms.IntegerField, {}, 42),
        (forms.JSONField, {}, '{"explicit": true}'),
        (
            forms.MultipleChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
            ["a", "c"],
        ),
        (forms.NullBooleanField, {}, None),
        (forms.SlugField, {}, "explicit-slug"),
        (forms.TimeField, {}, "12:34:56"),
        (
            forms.TypedChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
            "a",
        ),
        (forms.URLField, {}, "https://example.com/"),
        (forms.UUIDField, {}, "12345678-1234-5678-1234-567812345678"),
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
        (forms.FloatField, {}),
        (forms.GenericIPAddressField, {}),
        (forms.IntegerField, {}),
        (forms.JSONField, {}),
        (
            forms.MultipleChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
        ),
        (forms.NullBooleanField, {}),
        (forms.SlugField, {}),
        (forms.TimeField, {}),
        (
            forms.TypedChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
        ),
        (forms.URLField, {}),
        (forms.UUIDField, {}),
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
        (forms.FloatField, {}, -6.36438676418356),
        (forms.GenericIPAddressField, {}, "171.174.170.81"),
        (forms.IntegerField, {}, 6311),
        (
            forms.JSONField,
            {},
            '[{"name": "Norma Fisher", "residency": "4759 William Haven Apt. 194\\nWest Corey, TX 43780"}, {"name": "Brian Hamilton", "residency": "778 Brown Plaza\\nNorth Jenniferfurt, WY 88077"}, {"name": "Lisa Clayton", "residency": "139 John Divide Suite 115\\nRodriguezside, VT 16860"}, {"name": "Robin Fernandez", "residency": "USNV Wallace\\nFPO AP 50950"}, {"name": "David White", "residency": "471 Erika Curve\\nNorth Megan, UT 71358"}, {"name": "Sara Warren", "residency": "96947 Keller Squares\\nChristopherville, OR 83095"}, {"name": "Connor Smith", "residency": "2560 Krista Walk\\nNorth Lisa, ND 79428"}, {"name": "Alyssa Reid", "residency": "1510 James Ferry\\nSouth Jasonton, AK 71835"}, {"name": "Brian Green", "residency": "6208 Williams Courts Suite 345\\nMasseyshire, UT 88665"}, {"name": "Randall Kramer", "residency": "8419 Wade Bridge\\nMaldonadoshire, NY 41322"}]',
        ),
        (
            forms.MultipleChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
            ["b", "a"],
        ),
        (forms.NullBooleanField, {}, False),
        (forms.SlugField, {}, "three-image-son"),
        (forms.TimeField, {}, "07:46:39"),
        (
            forms.TypedChoiceField,
            {"choices": [("a", "A"), ("b", "B"), ("c", "C")]},
            "b",
        ),
        (forms.URLField, {}, "https://green.info/"),
        (forms.UUIDField, {}, "e3e70682-c209-4cac-a29f-6fbed82c07cd"),
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
