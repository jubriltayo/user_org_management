from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Organisation

User = get_user_model()


class UserRegistrationTests(APITestCase):

    def test_register_user_successfully(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.data['status'], 'success')
        # self.assertEqual(response.data['data']['user']['email'], data['email'])
        # self.assertTrue('accessToken' in response.data['data'])
        
        # Verify default organisation creation
        org_name = f"{data['firstName']}'s Organisation"
        self.assertTrue(Organisation.objects.filter(name=org_name).exists())

    def test_register_user_missing_fields(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['status'], 'error')
        self.assertTrue('errors' in response.data)

    def test_register_user_duplicate_email(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.client.post(url, data, format='json')
        
        # Attempt to register again with the same email
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['status'], 'error')
        self.assertTrue('errors' in response.data)


class UserLoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="john.doe@example.com",
            firstName="John",
            lastName="Doe",
            password="password123",
            phone="1234567890"
        )

    def test_login_user_successfully(self):
        url = reverse('login')
        data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['user']['email'], data['email'])
        self.assertTrue('accessToken' in response.data['data'])

    def test_login_user_invalid_credentials(self):
        url = reverse('login')
        data = {
            "email": "john.doe@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'Authentication failed')


class UserDetailTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            userId="testuserid",
            email="john.doe@example.com",
            firstName="John",
            lastName="Doe",
            password="password123",
            phone="1234567890"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_own_details(self):
        url = reverse('user-detail', kwargs={'userId': self.user.userId})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['status'], 'success')
        # self.assertEqual(response.data['data']['email'], self.user.email)


class AddUserToOrganisationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="john.doe@example.com",
            firstName="John",
            lastName="Doe",
            password="password123",
            phone="1234567890"
        )
        self.organisation = Organisation.objects.create(
            name="John's Organisation",
            orgId="123456",
            # created_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_add_user_to_organisation(self):
        url = reverse('add-user-to-organisation', kwargs={'orgId': self.organisation.orgId})
        data = {"userId": self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'User added to organisation successfully')



