from pprint import pprint
from rest_framework.test import APIClient, force_authenticate
from rest_framework.test import RequestsClient
import json
from django.http import response
from rest_framework import status
from django.test import TestCase
from django import urls
from rest_framework.reverse import reverse
from accounts import models
from accounts.models import User, Instructor, Student, Tag
from rest_framework.test import RequestsClient


class InstructorAPITests(TestCase):
    def setUp(self):
        i = User.objects.create_user(
            username='insructor_test', password='1234567GG89MMM', email='instructortest@test.com')
        i = Instructor.objects.create(user=i)
        i.save()
        s = User.objects.create_user(
            username='student_test', password='1234567GG89MMM', email='studenttest@test.com')
        s = Student.objects.create(user=s)
        s.save()
        t1 = Tag.objects.create(name='python')
        t1.save()
        t2 = Tag.objects.create(name='JAVA')
        t2.save()
        t3 = Tag.objects.create(name='C')
        t3.save()
        t4 = Tag.objects.create(name='C++')
        t4.save()
        t5 = Tag.objects.create(name='C#')
        t5.save()
        i.tags.add(t1, t2, t3)
        i.save()
        self.my_client = APIClient()
        return super().setUp()

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def login(self, username, password):
        '''
        login
        '''
        response = self.client.post(
            path=reverse('accounts-jwt-create'),
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        return data['access']

    def test_change_instructor_profile(self):
        '''
            get instructor profile
        '''
        u = User.objects.get(username='insructor_test')
        i_tmp = u.instructor
        token = self.login(u.username, '1234567GG89MMM')
        self.my_client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.my_client.get(
            path=reverse('accounts-instructor-me'),
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        pprint(f'get Instructor profile {data} \n')
        self.assertEquals(data['username'], u.username)
        self.assertEquals(data['email'], u.email)
        self.assertEquals(data['id'], u.id)

    def test_change_instructor_profile(self):
        '''
            change instructor profile
        '''
        u = User.objects.get(username='insructor_test')
        i_tmp = u.instructor
        token = self.login(u.username, '1234567GG89MMM')
        self.my_client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        new_first_name = "ali"
        new_last_name = "rezayi"
        new_phone_no = "12309812398"
        new_birth_date = "2020-02-01"
        response = self.my_client.put(
            path=reverse('accounts-instructor-me'),
            data={
                'first_name': new_first_name,
                'last_name': new_last_name,
                'phone_no': new_phone_no,
                'birth_date': new_birth_date
            }
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        pprint(f'get Instructor profile {data} \n')
        self.assertEquals(data['first_name'], new_first_name)
        self.assertEquals(data['last_name'], new_last_name)
        self.assertEquals(data['phone_no'], new_phone_no)
        self.assertEquals(data['birth_date'], new_birth_date)
        pprint('instructor profile changed successfully')

    # def test_signup_wrong_username(self):
    #     '''
    #     sending request with no username
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             # 'username': 'test',
    #             'email': 'test@gmail.com',
    #             'password1': 'testAM12345678JL',
    #             'password2': 'testAM12345678JL',
    #             'is_instructor': False
    #         })
    #     self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     data = json.loads(response.content)
    #     print(f'signup with no username {data} \n')
    #     assert 'username' in data
    #     assert len(data['username']) > 0

    # def test_signup_wrong_email(self):
    #     '''
    #     sending email incorrect format
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'test',
    #             'email': 'testgmail.com',
    #             'password1': 'testAM12345678JL',
    #             'password2': 'testAM12345678JL',
    #             'is_instructor': False
    #         })
    #     self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     data = json.loads(response.content)
    #     print(f'signup with no @ in email {data} \n')
    #     assert 'email' in data
    #     assert len(data['email']) > 0

    # def test_signup_wrong_email2(self):
    #     '''
    #     sending email incorrect format
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'test',
    #             'email': 'test@gmailcom',
    #             'password1': 'testAM12345678JL',
    #             'password2': 'testAM12345678JL',
    #             'is_instructor': False
    #         })
    #     self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     data = json.loads(response.content)
    #     print(f'sign up with no dot in email {data} \n')
    #     assert 'email' in data
    #     assert len(data['email']) > 0

    # def test_signup_no_email(self):
    #     '''
    #     sending no email
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'test',
    #             # 'email': 'test@gmail.com',
    #             'password1': 'testAM12345678JL',
    #             'password2': 'testAM12345678JL',
    #             'is_instructor': False
    #         })
    #     self.assertEquals(response.status_code,
    #                       status.HTTP_400_BAD_REQUEST)
    #     data = json.loads(response.content)
    #     print(f'sign up with no email {data} \n')
    #     assert 'email' in data
    #     assert len(data['email']) > 0

    # def test_signup_bad_password(self):
    #     '''
    #     full numeric password
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'test',
    #             'email': 'test@gmail.com',
    #             'password1': '77744488999999',
    #             'password2': '77744488999999',
    #             'is_instructor': False
    #         })
    #     self.assertEquals(response.status_code,
    #                       status.HTTP_400_BAD_REQUEST)
    #     data = json.loads(response.content)
    #     print(f'sign up with full numeric password {data} \n')
    #     assert 'password' in data
    #     assert len(data['password']) > 0

    # def test_signup_bad_password2(self):
    #     '''
    #     full numeric password
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'test',
    #             'email': 'test@gmail.com',
    #             'password1': 'm777222',
    #             'password2': 'm777222',
    #             'is_instructor': False
    #         })
    #     self.assertEquals(response.status_code,
    #                       status.HTTP_400_BAD_REQUEST)
    #     data = json.loads(response.content)
    #     print(f'password length less than 8 {data} \n')
    #     assert 'password' in data
    #     assert len(data['password']) > 0

    # def test_signup_bad_password3(self):
    #     '''
    #     full numeric password
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'test',
    #             'email': 'test@gmail.com',
    #             'password1': '777222',
    #             'password2': '777222',
    #             'is_instructor': False
    #         })
    #     self.assertEquals(response.status_code,
    #                       status.HTTP_400_BAD_REQUEST)
    #     data = json.loads(response.content)
    #     print(f'password length less than 8 and full numeric {data} \n')
    #     assert 'password' in data
    #     assert len(data['password']) > 1

    # def test_signup_bad_password4(self):
    #     '''
    #     full numeric password
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'test',
    #             'email': 'test@gmail.com',
    #             'password1': '777222',
    #             'password2': '777222',
    #             'is_instructor': False
    #         })
    #     self.assertEquals(response.status_code,
    #                       status.HTTP_400_BAD_REQUEST)
    #     data = json.loads(response.content)
    #     print(f'password length less than 8 and full numeric {data} \n')
    #     assert 'password' in data
    #     assert len(data['password']) > 1

    # def test_signup_case_insensitive_username_email(self):
    #     '''
    #     full numeric password
    #     '''
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'test',
    #             'email': 'test@gmail.com',
    #             'password1': '777222',
    #             'password2': '777222',
    #             'is_instructor': False
    #         })
    #     data1 = json.loads(response.content)
    #     self.assertEquals(response.status_code,
    #                       status.HTTP_201_CREATED)
    #     response = self.client.post(
    #         path=self.url,
    #         data={
    #             'username': 'Test',
    #             'email': 'Test@gmail.com',
    #             'password1': '777222',
    #             'password2': '777222',
    #             'is_instructor': False
    #         })
    #     data2 = json.loads(response.content)
    #     self.assertEquals(response.status_code,
    #                       status.HTTP_201_CREATED)
    #     print(
    #         f'first username is {data1["username"]} second username is {data2["username"]}')
