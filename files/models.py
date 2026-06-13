from django.contrib.auth.models import User
from django.db import models


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subfolders",
    )

    full_path = models.CharField(max_length=1024, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.parent:
            self.full_path = f"{self.parent.full_path}/{self.name}"
        else:
            self.full_path = f"{self.name}"
        super().save(*args, **kwargs)

    def get_minio_path(self):
        return self.full_path

    def __str__(self):
        return self.full_path

    def get_ancestors(self):
        """Возвращает список родительских папок от корня до текущей"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)
            current = current.parent
        return ancestors


class File(models.Model):
    def get_file_upload_path(instance, filename):
        return f"{instance.user.username}/{instance.folder.get_full_path()}/{instance.name}"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="files"
    )
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")
    full_path = models.CharField(max_length=1024, unique=True, db_index=True)
    file = models.FileField(upload_to=get_file_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.full_path = f"{self.folder.full_path}/{self.name}"
        if not self.file.name or self.file.name != self.full_path:
            self.file.name = self.full_path

        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_path
