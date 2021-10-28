from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage
from .models import Verification
# from djoser import utils
# from djoser.conf import settings
from django.http import HttpRequest
from validate_email import validate_email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from datetime import timedelta
from django import conf


def remove_expired_tokens():
    Verification.objects.filter(create_time__gte=timedelta(
        days=conf.settings.TOKEN_EXPIRATION_TIME)).delete()


class ActivationEmail(APIView):
    def post(self, request: HttpRequest):
        # remove_expired_tokens()
        user_email = request.data['email']
        user_username = request.data['username']

        if validate_email(user_email):
            rnd_tok = random.randrange(100000, 1000000)
            template = render_to_string('myemail/activation.html',
                                        {
                                            'username': user_username,
                                            'code': rnd_tok
                                        })

            email = EmailMessage('تایید حساب کاربری در کوله پشتی',
                                 template,
                                 'Kooleposhti',
                                 [user_email]
                                 )

            email.content_subtype = "html"
            email.fail_silently = False
            email.send()

            try:
                # email resent
                verification_obj = Verification.objects.get(email=user_email)
                verification_obj.token = str(rnd_tok)
                verification_obj.save()

            except Verification.DoesNotExist:
                # email sent
                verification_obj = Verification.objects.create(
                    email=user_email,
                    token=str(rnd_tok))
                verification_obj.save()

            return Response(status=status.HTTP_200_OK, data='Email sent successfully')
            # return Response({"code": random_code}, status= status.HTTP_200_OK)

        else:
            return Response(f"'{user_email}' doesn't exist", status=status.HTTP_404_NOT_FOUND)


# class ActivationEmail(BaseEmailMessage):
#     template_name = "email/activation.html"

#     def get_context_data(self):
#         # ActivationEmail can be deleted
#         context = super().get_context_data()

#         user = context.get("user")
#         context["uid"] = utils.encode_uid(user.pk)
#         context["token"] = default_token_generator.make_token(user)
#         context["url"] = settings.ACTIVATION_URL.format(**context)
#         return context


# class ConfirmationEmail(BaseEmailMessage):
#     template_name = "email/confirmation.html"


# class PasswordResetEmail(BaseEmailMessage):
#     template_name = "email/password_reset.html"

#     def get_context_data(self):
#         # PasswordResetEmail can be deleted
#         context = super().get_context_data()

#         user = context.get("user")
#         context["uid"] = utils.encode_uid(user.pk)
#         context["token"] = default_token_generator.make_token(user)
#         context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
#         return context


# class PasswordChangedConfirmationEmail(BaseEmailMessage):
#     template_name = "email/password_changed_confirmation.html"


# class UsernameChangedConfirmationEmail(BaseEmailMessage):
#     template_name = "email/username_changed_confirmation.html"


# class UsernameResetEmail(BaseEmailMessage):
#     template_name = "email/username_reset.html"

#     def get_context_data(self):
#         context = super().get_context_data()

#         user = context.get("user")
#         context["uid"] = utils.encode_uid(user.pk)
#         context["token"] = default_token_generator.make_token(user)
#         context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)
#         return context
