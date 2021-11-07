import json
from django.http import response
from rest_framework import status
from django.test import TestCase
from django import urls
from accounts import models


class UserAPITests(TestCase):
    def setUp(self):
        self.url = urls.reverse('accounts-signup')
        return super().setUp()

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_signup(self):
        '''
        testing normal signup process
        '''
        email = 'test@gmail.com'
        username = 'test'
        response = self.client.post(
            path=self.url,
            data={
                'username': username,
                'email': email,
                'password1': 'testAM12345678JL',
                'password2': 'testAM12345678JL',
                'is_instructor': False
            })
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        print(f'normal signup {data} \n')
        self.assertEquals(data['username'], username)
        self.assertEquals(data['email'], email)

    def test_signup_wrong_username(self):
        '''
        sending request with no username
        '''
        response = self.client.post(
            path=self.url,
            data={
                # 'username': 'test',
                'email': 'test@gmail.com',
                'password1': 'testAM12345678JL',
                'password2': 'testAM12345678JL',
                'is_instructor': False
            })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        print(f'signup with no username {data} \n')
        assert 'username' in data
        assert len(data['username']) > 0

    def test_signup_wrong_email(self):
        '''
        sending email incorrect format
        '''
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test',
                'email': 'testgmail.com',
                'password1': 'testAM12345678JL',
                'password2': 'testAM12345678JL',
                'is_instructor': False
            })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        print(f'signup with no @ in email {data} \n')
        assert 'email' in data
        assert len(data['email']) > 0

    def test_signup_wrong_email2(self):
        '''
        sending email incorrect format
        '''
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test',
                'email': 'test@gmailcom',
                'password1': 'testAM12345678JL',
                'password2': 'testAM12345678JL',
                'is_instructor': False
            })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        print(f'sign up with no dot in email {data} \n')
        assert 'email' in data
        assert len(data['email']) > 0

    def test_signup_no_email(self):
        '''
        sending no email
        '''
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test',
                # 'email': 'test@gmail.com',
                'password1': 'testAM12345678JL',
                'password2': 'testAM12345678JL',
                'is_instructor': False
            })
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        print(f'sign up with no email {data} \n')
        assert 'email' in data
        assert len(data['email']) > 0

    def test_signup_bad_password(self):
        '''
        full numeric password
        '''
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test',
                'email': 'test@gmail.com',
                'password1': '77744488999999',
                'password2': '77744488999999',
                'is_instructor': False
            })
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        print(f'sign up with full numeric password {data} \n')
        assert 'password' in data
        assert len(data['password']) > 0

    def test_signup_bad_password2(self):
        '''
        full numeric password
        '''
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test',
                'email': 'test@gmail.com',
                'password1': 'm777222',
                'password2': 'm777222',
                'is_instructor': False
            })
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        print(f'password length less than 8 {data} \n')
        assert 'password' in data
        assert len(data['password']) > 0

    def test_signup_bad_password3(self):
        '''
        full numeric password
        '''
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test',
                'email': 'test@gmail.com',
                'password1': '777222',
                'password2': '777222',
                'is_instructor': False
            })
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        print(f'password length less than 8 and full numeric {data} \n')
        assert 'password' in data
        assert len(data['password']) > 1

    def test_signup_bad_password4(self):
        '''
        full numeric password
        '''
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test',
                'email': 'test@gmail.com',
                'password1': '777222',
                'password2': '777222',
                'is_instructor': False
            })
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        print(f'password length less than 8 and full numeric {data} \n')
        assert 'password' in data
        assert len(data['password']) > 1

    def test_signup_case_insensitive_username_email(self):
        '''
        full numeric password
        '''
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test',
                'email': 'test@gmail.com',
                'password1': '7772asjdkl22',
                'password2': '7772asjdkl22',
                'is_instructor': False
            })
        data1 = json.loads(response.content)
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        response = self.client.post(
            path=self.url,
            data={
                'username': 'Test',
                'email': 'Test@gmail.com',
                'password1': '7772asjdkl22',
                'password2': '7772asjdkl22',
                'is_instructor': False
            })
        data2 = json.loads(response.content)
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        print(
            f'first username is {data1["username"]} second username is {data2["username"]}')


'''
username case sensitive
'''
