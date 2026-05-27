from django import forms

from .. import form_faker


def test_multiple_choice_field_picks_subset_of_choices():
    class MultipleChoiceFieldForm(forms.Form):
        choice_field = forms.MultipleChoiceField(
            choices=[("a", "A"), ("b", "B"), ("c", "C"), ("d", "D"), ("e", "E")],
        )

    post_data = form_faker.get_data(MultipleChoiceFieldForm)
    assert post_data == {
        "choice_field": ["d", "a", "b", "c"],
    }

    form = MultipleChoiceFieldForm(post_data)
    assert form.is_valid()
