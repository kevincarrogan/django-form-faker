from io import BytesIO

from PIL import Image

from django import forms

from .. import form_faker


def test_random_generated_image_is_valid_png():
    class ImageForm(forms.Form):
        image_field = forms.ImageField()

    post_data = form_faker.get_data(ImageForm)
    assert "image_field" not in post_data

    files_data = form_faker.get_files(ImageForm)
    image_upload = files_data["image_field"]
    assert image_upload.name == "test_file.png"

    image = Image.open(BytesIO(image_upload.read()))
    assert image.format == "PNG"
    assert image.size == (1, 1)

    image_upload.seek(0)
    form = ImageForm(data=post_data, files=files_data)
    assert form.is_valid(), f"Invalid with {form.errors}"
