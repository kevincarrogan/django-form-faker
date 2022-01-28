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
    return fake.random_element(field_instance.choices)[0]


def generate_date_field_value(field_instance):
    input_format = field_instance.input_formats[0]
    return fake.date(pattern=input_format)


generators = {
    forms.BooleanField: generate_boolean_field_value,
    forms.CharField: generate_char_field_value,
    forms.ChoiceField: generate_choice_field_value,
    forms.DateField: generate_date_field_value,
}


def get_data(form_class, _include_optional=False, **kwargs):
    fields = form_class.declared_fields

    post_data = {}
    for field_name, field in fields.items():
        if field_name in kwargs:
            post_data[field_name] = kwargs[field_name]
            continue

        if not _include_optional and not field.required:
            continue

        post_data[field_name] = generators[field.__class__](field)

    return post_data
