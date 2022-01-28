from django import forms

from decimal import Decimal

from .. import form_faker


def test_decimal_field_input_formats():
    class DecimalFieldForm(forms.Form):
        decimal_field = forms.DecimalField(
            min_value=5,
            max_value=500,
            max_digits=7,
            decimal_places=4,
        )

    post_data = form_faker.get_data(DecimalFieldForm)
    assert post_data == {
        "decimal_field": Decimal("437.6604"),
    }

    form = DecimalFieldForm(post_data)
    assert form.is_valid()
