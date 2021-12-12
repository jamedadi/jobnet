from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class RegistrationViewTest(APITestCase):
    def setUp(self):
        self.registration_urls = {
            'job-seeker': reverse('accounts:registration', kwargs={'user_type': 'job-seeker'}),
            'employer': reverse('accounts:registration', kwargs={'user_type': 'employer'}),
            'incorrect-parameter': reverse('accounts:registration', kwargs={'user_type': 'incorrect-parameter'}),
        }
        self.user_data = dict(
            username='mohammad', email='mohammad@gmail.com', password='QWEasd9876', confirm_password='QWEasd9876'
        )
        self.week_password_user_data = dict(
            username='mohammad', email='mohammad@gmail.com', password='123qwe123', confirm_password='123qwe123'
        )

        self.password_not_equal_user_data = dict(
            username='mohammad', email='mohammad@gmail.com', password='QWEasd9876', confirm_password='QWEasd9874'
        )

    def test_job_seeker_registration(self):
        response = self.client.post(self.registration_urls['job-seeker'], data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=self.user_data['username'])
        self.assertFalse(user.email_verified)
        self.assertFalse(user.is_employer)
        self.assertTrue(user.is_job_seeker)

    def test_employer_registration(self):
        response = self.client.post(self.registration_urls['employer'], data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=self.user_data['username'])
        self.assertFalse(user.email_verified)
        self.assertFalse(user.is_job_seeker)
        self.assertTrue(user.is_employer)

    def test_incorrect_user_type(self):
        response = self.client.post(self.registration_urls['incorrect-parameter'], data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_job_seeker_registration_with_week_password(self):
        response = self.client.post(self.registration_urls['job-seeker'], data=self.week_password_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employer_registration_with_week_password(self):
        response = self.client.post(self.registration_urls['employer'], data=self.week_password_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_seeker_registration_with_not_equal_password(self):
        response = self.client.post(self.registration_urls['job-seeker'], data=self.password_not_equal_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employer_registration_with_not_equal_password(self):
        response = self.client.post(self.registration_urls['employer'], data=self.password_not_equal_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_seeker_duplicate_username_registration(self):
        user_data = self.user_data
        for i in range(2):
            response = self.client.post(self.registration_urls['job-seeker'], data=user_data)
            user_data['email'] = 'ali@gmail.com'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employer_duplicate_username_registration(self):
        user_data = self.user_data
        for i in range(2):
            response = self.client.post(self.registration_urls['employer'], data=user_data)
            user_data['email'] = 'ali@gmail.com'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_seeker_duplicate_email_registration(self):
        user_data = self.user_data
        for i in range(2):
            response = self.client.post(self.registration_urls['job-seeker'], data=user_data)
            user_data['username'] = 'ali'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employer_duplicate_email_registration(self):
        user_data = self.user_data
        for i in range(2):
            response = self.client.post(self.registration_urls['employer'], data=user_data)
            user_data['username'] = 'ali'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
