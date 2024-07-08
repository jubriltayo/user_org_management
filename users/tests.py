from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from organization.models import Organisation
User = get_user_model()

class TokenGenerationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
            phone="1234567890"
        )
        self.organisation = Organisation.objects.create(
            name="John's Organisation",
            description="Default organisation for John"
        )
        self.user.organisations.add(self.organisation)

    def test_token_generation(self):
        refresh = RefreshToken.for_user(self.user)
        self.assertIn('access', refresh.access_token['token_type'])
        self.assertIn('refresh', refresh["token_type"])
        self.assertEqual(refresh['userId'], self.user.userId)

    def test_token_expiry(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token

        # Ensure the token is valid before expiry
        response = self.client.get(reverse('user-detail', args=[self.user.userId]), HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Mock the token expiration by setting the expiration time in the past
        from datetime import timedelta
        access_token.set_exp(lifetime=timedelta(seconds=0))
        response = self.client.get(reverse('user-detail', args=[self.user.userId]), HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        
        url = reverse('register')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['first_name'], "John")
        self.assertEqual(response.data['data']['user']['last_name'], "Doe")

    def test_user_registration_missing_fields(self):
        url = reverse('register')
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "john.doe@example.com",
            "password": "",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_user_registration_duplicate_email(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
            phone="1234567890"
        )
        self.organisation = Organisation.objects.create(
            name="John's Organisation",
            description="Default organisation for John"
        )
        self.user.organisations.add(self.organisation)

    def test_user_login(self):
        url = reverse('login')
        data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], "john.doe@example.com")

    def test_user_login_invalid_credentials(self):
        url = reverse('login')
        data = {
            "email": "john.doe@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], "Authentication failed")