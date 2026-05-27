from faker import Faker

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import validate_ipv6_address


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


def generate_duration_field_value(field_instance):
    return fake.time_delta(fake.future_datetime())


def generate_email_field_value(field_instance):
    return fake.email()


def generate_float_field_value(field_instance):
    kwargs = {}
    if field_instance.max_value is not None:
        kwargs["max_value"] = field_instance.max_value
    if field_instance.min_value is not None:
        kwargs["min_value"] = field_instance.min_value
    return fake.pyfloat(**kwargs)


def generate_generic_ip_address_field_value(field_instance):
    if validate_ipv6_address in field_instance.default_validators:
        return fake.ipv6()
    return fake.ipv4()


def generate_integer_field_value(field_instance):
    kwargs = {}
    if field_instance.max_value is not None:
        kwargs["max_value"] = field_instance.max_value
    if field_instance.min_value is not None:
        kwargs["min_value"] = field_instance.min_value
    return fake.pyint(**kwargs)


def generate_json_field_value(field_instance):
    return fake.json()


def generate_multiple_choice_field_value(field_instance):
    choices = tuple(value for value, label in field_instance.choices)
    return fake.random_elements(elements=choices, unique=True)


def generate_null_boolean_field_value(field_instance):
    return fake.random_element([True, False, None])


def generate_slug_field_value(field_instance):
    return fake.slug()


def generate_time_field_value(field_instance):
    input_format = field_instance.input_formats[0]
    return fake.time(pattern=input_format)


def generate_url_field_value(field_instance):
    return fake.url()


def generate_uuid_field_value(field_instance):
    return fake.uuid4()


generators = {
    forms.BooleanField: generate_boolean_field_value,
    forms.CharField: generate_char_field_value,
    forms.ChoiceField: generate_choice_field_value,
    forms.DateField: generate_date_field_value,
    forms.DateTimeField: generate_date_time_field_value,
    forms.DecimalField: generate_decimal_field_value,
    forms.DurationField: generate_duration_field_value,
    forms.EmailField: generate_email_field_value,
    forms.FloatField: generate_float_field_value,
    forms.GenericIPAddressField: generate_generic_ip_address_field_value,
    forms.IntegerField: generate_integer_field_value,
    forms.JSONField: generate_json_field_value,
    forms.MultipleChoiceField: generate_multiple_choice_field_value,
    forms.NullBooleanField: generate_null_boolean_field_value,
    forms.SlugField: generate_slug_field_value,
    forms.TimeField: generate_time_field_value,
    forms.URLField: generate_url_field_value,
    forms.UUIDField: generate_uuid_field_value,
}


def generate_file(field_instance):
    return fake.binary()


file_field_generators = {
    forms.FileField: generate_file,
}


def get_data(form_class, _include_optional=False, **kwargs):
    fields = form_class.declared_fields

    post_data = {}
    for field_name, field in fields.items():
        field_class = field.__class__
        if field_class in file_field_generators:
            continue

        if field_name in kwargs:
            post_data[field_name] = kwargs[field_name]
            continue

        if not _include_optional and not field.required:
            continue

        post_data[field_name] = generators[field_class](field)

    return post_data


def get_files(form_class):
    fields = form_class.declared_fields

    file_data = {}
    for field_name, field in fields.items():
        field_class = field.__class__
        if field_class not in file_field_generators:
            continue

        file_data[field_name] = SimpleUploadedFile(
            "test_file",
            file_field_generators[field_class](field),
        )

    return file_data
