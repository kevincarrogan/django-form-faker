from django import forms

from .. import form_faker


def test_date_field_input_formats():
    class DateFieldForm(forms.Form):
        date_field = forms.DateField(input_formats=["%d %B %Y", "%d %B, %"])

    post_data = form_faker.get_data(DateFieldForm)

    assert post_data == {
        "date_field": "20 March 1996",
    }


def test_date_field_settings_input_formats(settings):
    settings.DATE_INPUT_FORMATS = ["%d %B %Y", "%d %B, %"]

    class DateFieldForm(forms.Form):
        date_field = forms.DateField()

    post_data = form_faker.get_data(DateFieldForm)

    assert post_data == {
        "date_field": "20 March 1996",
    }


def test_date_field_settings_input_formats(settings):
    settings.USE_L10N = True
    settings.DATE_INPUT_FORMATS = ["%d %B %Y", "%d %B, %"]

    class DateFieldForm(forms.Form):
        date_field = forms.DateField()

    post_data = form_faker.get_data(DateFieldForm)

    assert post_data == {
        "date_field": "1996-03-20",
    }
