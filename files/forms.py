from django import forms

from files.models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "folder", "file"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название файла"}
            ),
            "folder": forms.Select(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {"name": "Название файла", "folder": "Папка", "file": "Выберите файл"}
