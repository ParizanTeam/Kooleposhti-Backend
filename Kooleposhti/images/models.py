from django.db import models
import os
import uuid
from django import conf

# Create your models here.


def image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    extension = filename.split('.')[-1]  # returns extension of the filename
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('uploads/images/', filename)


class MyImage(models.Model):
    image = models.ImageField(
        verbose_name="profile image", upload_to=image_file_path)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # @staticmethod
    # def image_upload_url()
