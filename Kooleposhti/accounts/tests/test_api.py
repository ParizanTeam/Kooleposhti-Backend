import json
from django.http import response
from rest_framework import status
from django.test import TestCase
from django import urls
from accounts import models


class UserAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_signup(self):
        '''
        testing normal signup process
        '''
        url = urls.reverse('accounts-signup')
        response = self.client.post(
            path=url,
            data={
                'username': 'test',
                'email': 'test@gmail.com',
                'password1': 'testAM12345678JL',
                'password2': 'testAM12345678JL',
                'is_instructor': False
            })
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        print(data)
