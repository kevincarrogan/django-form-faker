from django import forms

from .. import form_faker


def test_generic_ip_address_field_ipv6_protocol():
    class IPv6Form(forms.Form):
        ip_field = forms.GenericIPAddressField(protocol="IPv6")

    post_data = form_faker.get_data(IPv6Form)
    assert post_data == {
        "ip_field": "e3e7:682:c209:4cac:629f:6fbf:d82c:7cd",
    }

    form = IPv6Form(post_data)
    assert form.is_valid()
