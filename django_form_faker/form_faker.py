from faker import Faker

from django import forms


fake = Faker()


def generate_char_field(field_instance):
    if field_instance.max_length:
        letters = fake.random_letters(field_instance.max_length)
    elif field_instance.min_length:
        letters = fake.random_letters(field_instance.min_length)
    else:
        letters = fake.random_letters()

    return "".join(letters)


generators = {
    forms.CharField: generate_char_field,
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
