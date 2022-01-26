# Django Form Faker

Django Form Faker creates test data for Django Forms.

This loosely resembles libraries that provide fixtures for Django models.

## Install

```bash
pip install django_form_faker
```

## Usage and Info

### Basic usage

```python
# forms.py

class UserDetailsForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
    title = forms.CharField(
        choices=(
            "mr", "Mr.",
            "mrs", "Mrs.",
            "ms", "Ms.",
        ),
    )
    email = forms.EmailField()


# test_forms.py

from django.test import TestCase
from django_form_faker import form_faker

from .forms import UserDetailsForm

class TestUserDetailForm(TestCase):
    def test_post_is_valid(self):
        post_data = form_faker.get_post_data(UserDetailsForm)
        form = UserDetailsForm(data=post_data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid(self):
        form = form_faker.make(UserDetailsForm)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = form_faker.make(
            UserDetailsForm,
            email="notanemail",
        )
        self.assertFalse(form.is_valid())
```
