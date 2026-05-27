from django import forms

from .. import form_faker


def test_float_field_min_and_max_value():
    class FloatFieldForm(forms.Form):
        float_field = forms.FloatField(min_value=10, max_value=20)

    post_data = form_faker.get_data(FloatFieldForm)
    assert post_data == {
        "float_field": 16.679215,
    }

    form = FloatFieldForm(post_data)
    assert form.is_valid()
