from django.dispatch import receiver
from accounts.models import Student, Instructor
from django.db.models.signals import post_save
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_for_new_user(sender, *args, **kwargs):
    pass
    # if kwargs['created']:
    #     Student.objects.create(user=kwargs.get['instance'])


# def create_instructor_for_new_user
