# files/models.py
from django.contrib.auth.models import User
from django.db import models


class Folder(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="folders",
        verbose_name="Пользователь",
    )
    name = models.CharField(max_length=255, verbose_name="Название папки")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subfolders",
        verbose_name="Родительская папка",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name


class File(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="files"
    )
    name = models.CharField(max_length=255, verbose_name="Название файла")
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="files", verbose_name="Папка"
    )
    file = models.FileField(upload_to="")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.file.field.upload_to = f"{self.user.username}/"
        super().save(*args, **kwargs)

    def __str__(self):
        folder_path = self.folder.get_full_path() if self.folder else ""
        return f"{folder_path}/{self.name}" if folder_path else self.name
