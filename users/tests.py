from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
import json
import uuid


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-register')
        self.token_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')
        
        # Create test user
        self.test_user = CustomUser.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Data for new user registration
        self.valid_user_data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '+380991234567'
        }

    def test_user_registration(self):
        """Test new user registration"""
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())
        
        self.assertNotIn('password', response.data)
        
        # Check that username is set as email
        user = CustomUser.objects.get(email='newuser@example.com')
        self.assertEqual(user.username, 'newuser@example.com')

    def test_user_registration_invalid_data(self):
        """Test registration with incomplete data"""
        invalid_data = {
            'email': 'invalid@example.com',
            # Password is missing
        }
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(CustomUser.objects.filter(email='invalid@example.com').exists())

    def test_user_login(self):
        """Test token obtaining during login"""
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        
        response = self.client.post(
            self.token_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(
            self.token_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_refresh(self):
        """Test token refresh"""
        # First get the tokens
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        
        login_response = self.client.post(
            self.token_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        refresh_token = login_response.data['refresh']
        
        refresh_data = {
            'refresh': refresh_token
        }
        
        response = self.client.post(
            self.token_refresh_url,
            data=json.dumps(refresh_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_detail_get(self):
        """Test getting user data"""
        # Get token for authorization
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        
        login_response = self.client.post(
            self.token_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        access_token = login_response.data['access']
        
        # Set token for authorization
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Get user data
        user_detail_url = reverse('user-detail', kwargs={'pk': self.test_user.id})
        response = self.client.get(user_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')

    def test_user_update(self):
        """Test updating user data"""
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        
        login_response = self.client.post(
            self.token_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        access_token = login_response.data['access']
        
        # Set token for authorization
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Update user data
        update_data = {
            'email': 'testuser@example.com',
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone_number': '+380991234567'
        }
        
        user_detail_url = reverse('user-detail', kwargs={'pk': self.test_user.id})
        response = self.client.put(
            user_detail_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # Add debug information
        print("\nResponse status:", response.status_code)
        print("Response data:", response.data)
        
        if response.status_code != status.HTTP_200_OK:
            print("Error details:", response.data)
            
        # Check current user state in database
        current_user = CustomUser.objects.get(id=self.test_user.id)
        print("Current user state:", {
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'phone_number': current_user.phone_number
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that data is updated
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.first_name, 'Updated')
        self.assertEqual(self.test_user.last_name, 'Name')
        self.assertEqual(self.test_user.phone_number, '+380991234567')

    def test_unauthorized_access(self):
        """Test access without authorization"""
        user_detail_url = reverse('user-detail', kwargs={'pk': self.test_user.id})
        response = self.client.get(user_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 