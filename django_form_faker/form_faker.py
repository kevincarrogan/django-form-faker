from faker import Faker

from django import forms


fake = Faker()


def generate_boolean_field_value(field_instance):
    return fake.boolean()


def generate_char_field_value(field_instance):
    if field_instance.max_length:
        letters = fake.random_letters(field_instance.max_length)
    elif field_instance.min_length:
        letters = fake.random_letters(field_instance.min_length)
    else:
        letters = fake.random_letters()

    return "".join(letters)


def generate_choice_field_value(field_instance):
    return fake.random_element(field_instance.choices)


generators = {
    forms.BooleanField: generate_boolean_field_value,
    forms.CharField: generate_char_field_value,
    forms.ChoiceField: generate_choice_field_value,
}


def get_data(form_class, **kwargs):
    fields = form_class.declared_fields

    post_data = {}
    for field_name, field in fields.items():
        if not field.required:
            continue

        if field_name in kwargs:
            value = kwargs[field_name]
        else:
            value = generators[field.__class__](field)

        post_data[field_name] = value

    return post_data
