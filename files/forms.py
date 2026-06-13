from django import forms

from .models import File, Folder


class FileUploadForm(forms.ModelForm):
    file = forms.FileField(
        label="Выберите файл", widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = File
        fields = ["file"]


class CreateFolderForm(forms.ModelForm):
    name = forms.CharField(
        label="Название папки",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите название папки"}
        ),
    )

    class Meta:
        model = Folder
        fields = ["name"]
