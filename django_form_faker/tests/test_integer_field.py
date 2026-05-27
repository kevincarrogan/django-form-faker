from django import forms

from .. import form_faker


def test_integer_field_min_and_max_value():
    class IntegerFieldForm(forms.Form):
        integer_field = forms.IntegerField(min_value=10, max_value=20)

    post_data = form_faker.get_data(IntegerFieldForm)
    assert post_data == {
        "integer_field": 16,
    }

    form = IntegerFieldForm(post_data)
    assert form.is_valid()
