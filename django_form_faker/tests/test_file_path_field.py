from pathlib import Path

from django import forms

from .. import form_faker


def test_file_path_field_picks_from_directory():
    data_path = str(Path(__file__).parent / "data")

    class FilePathFieldForm(forms.Form):
        file_path_field = forms.FilePathField(path=data_path)

    post_data = form_faker.get_data(FilePathFieldForm)
    assert post_data == {
        "file_path_field": f"{data_path}/random_binary_file",
    }

    form = FilePathFieldForm(post_data)
    assert form.is_valid()
