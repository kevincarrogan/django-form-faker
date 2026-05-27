from django import forms

from .. import form_faker


def test_time_field_input_formats():
    class TimeFieldForm(forms.Form):
        time_field = forms.TimeField(input_formats=["%I:%M %p", "%H:%M"])

    post_data = form_faker.get_data(TimeFieldForm)

    assert post_data == {
        "time_field": "07:46 AM",
    }

    form = TimeFieldForm(post_data)
    assert form.is_valid()
