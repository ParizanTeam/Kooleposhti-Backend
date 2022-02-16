from django.db import models
import os
import uuid
from django.conf import settings
from django.core.files.storage import Storage, default_storage

# Create your models here.


def image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    extension = filename.split('.')[-1]  # returns extension of the filename
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('uploads/images/', filename)


class MyImage(models.Model):
    image = models.ImageField(
        verbose_name="profile image", upload_to='uploads/images/', null=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='image')

    def __str__(self):
        return self.name

    @classmethod
    def get_image_id(cls, image_url):
        return cls.objects.exclude(image__isnull=True) \
            .filter(image__contains=image_url) \
            .first()

    # @staticmethod
    # def image_upload_url()
