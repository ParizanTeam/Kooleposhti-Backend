from django.dispatch import receiver
from .models import Student, Instructor
from django.db.models.signals import post_save


@receiver(post_save)
def create_student_for_new_user(sender, *args, **kwargs):
    if kwargs['created']:
        Student.objects.create(user=kwargs.get['instance'])
