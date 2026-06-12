# import storages.backends.s3boto3
# from django.conf import settings
# from django.core.management.base import BaseCommand


# class Command(BaseCommand):
#     help = "Ensure MinIO bucket exists"

#     def handle(self, *args, **options):
#         storage = storages.backends.s3boto3.S3Boto3Storage()
#         bucket_name = settings.AWS_STORAGE_BUCKET_NAME
#         if not storage.bucket_exists(bucket_name):
#             storage.create_bucket()
#             self.stdout.write(self.style.SUCCESS(f'Bucket "{bucket_name}" created'))
#         else:
#             self.stdout.write(f'Bucket "{bucket_name}" already exists')
