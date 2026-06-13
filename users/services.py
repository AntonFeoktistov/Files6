import os

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from storages.backends.s3boto3 import S3Boto3Storage

from files.models import Folder


class UserFolderService:
    def get_user_folder_path(self, username: str) -> str:
        return f"{username}/"

    def create_user_folder(self, username: str) -> bool:
        try:
            if os.getenv("USE_S3", "False") != "True":
                print("ℹ️ MinIO не используется")
                return True

            bucket_name = os.getenv("MINIO_BUCKET_NAME")
            endpoint = os.getenv("MINIO_ENDPOINT")
            access_key = os.getenv("MINIO_ACCESS_KEY")
            secret_key = os.getenv("MINIO_SECRET_KEY")

            storage = S3Boto3Storage(
                bucket_name=bucket_name,
                endpoint_url=endpoint,
                access_key=access_key,
                secret_key=secret_key,
                use_ssl=False,
                file_overwrite=False,
            )

            folder_path = self.get_user_folder_path(username)
            marker_path = f"{folder_path}.folder_marker"

            user = get_object_or_404(User, username=username)
            Folder.objects.create(user=user, name=username, parent=None)

            if not storage.exists(marker_path):
                storage.save(marker_path, ContentFile(b""))
                print(f"✅ Папка для {username} создана: {folder_path}")
            else:
                print(f"ℹ️ Папка для {username} уже существует")

            return True

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback

            traceback.print_exc()
            return False
