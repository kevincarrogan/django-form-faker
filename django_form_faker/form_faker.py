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


def generate_date_time_field_value(field_instance):
    return fake.iso8601()


def generate_decimal_field_value(field_instance):
    kwargs = {}
    if field_instance.max_value:
        kwargs["max_value"] = field_instance.max_value
    if field_instance.min_value:
        kwargs["min_value"] = field_instance.min_value
    if field_instance.decimal_places:
        kwargs["right_digits"] = field_instance.decimal_places
    if field_instance.max_digits:
        kwargs["left_digits"] = (
            field_instance.max_digits - field_instance.decimal_places
        )
    return fake.pydecimal(**kwargs)


generators = {
    forms.BooleanField: generate_boolean_field_value,
    forms.CharField: generate_char_field_value,
    forms.ChoiceField: generate_choice_field_value,
    forms.DateField: generate_date_field_value,
    forms.DateTimeField: generate_date_time_field_value,
    forms.DecimalField: generate_decimal_field_value,
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
