from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import Department

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('accounts:create')
TOKEN_URL = reverse('accounts:token')
ME_URL = reverse('accounts:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test uses API(public)"""

    def setUp(self):
        self.client = APIClient()
         
    # def test_create_valid_user_success(self):
    #     """Test craating user with valid payload succssful"""
    #     dept = Department.objects.create(name='elect')
    #     email = 'hello@gmail.com'
    #     password = 'passwod123'

    #     payload = {
    #         'email': email,
    #         'password': password,
    #         'first_name':'Chase',
    #         'last_name':'Conner',
    #         'department':dept,
    #     }
    #     res = self.client.post(CREATE_USER_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     user = get_user_model().objects.get(**res.data)
    #     self.assertTrue(user.check_password(payload['password']))
    #     self.assertNotIn('password',res.data)

    def test_user_created_already(self):
        """Test creating a user that already exists fails"""
        dept = Department.objects.create(name='elect')
        payload = {
            'email': 'hello@btw.com',
            'password': 'password123',
            'first_name':'Chase',
            'last_name':'Conner',
            'department':dept,
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 8 characters"""

        dept = Department.objects.create(name='elect')
        payload = {
            'email': 'hello@btw.com',
            'password': 'pass',
            'first_name':'Chase',
            'last_name':'Conner',
            'department':dept,
        }
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for user"""
        dept = Department.objects.create(name='elect')
        payload = {
            'email': 'hello@btw.com',
            'password': 'password123',
            'first_name':'Chase',
            'last_name':'Conner',
            'department':dept,
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        dept = Department.objects.create(name='elect')
        create_user(
            email = 'hello@btw.com',
            password ='password123',
            first_name = 'Chase',
            last_name = 'Conner',
            department = dept,
        )
        payload = {'email':'hello@btw.com', 'password': 'pass'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not createdif user doesn't exist"""
        dept = Department.objects.create(name='elect')
        payload = {
            'email': 'hello@btw.com',
            'password': 'password123',
            'first_name':'Chase',
            'last_name':'Conner',
            'department':dept,
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Tests that email and password are required"""
        res = self.client.post(TOKEN_URL,{
            'email':'one@btw.com',
            'password': '',
        })

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Tests that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class  PrivateUserApiTests(TestCase):
    """Tests API requests that require authentication"""

    def setUp(self):
        dept = Department.objects.create(name='elect')
        self.user = create_user(
            email = 'hello@btw.com',
            password ='password123',
            first_name = 'Chase',
            last_name = 'Conner',
            department = dept,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'first_name':self.user.first_name,
            'last_name': self.user.last_name,
            'email':self.user.email,
            'department': self.user.department
        })
    
    def test_post_me_not_allowed(self):
        """Tests that POST not allowed on ME url"""
        res = self.client.post(ME_URL,{})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating the user profile for authenticated user
        """
        dept = Department.objects.create(name='econs')
        payload = {
            'password': 'password123456',
            'first_name':'Omari',
            'department':dept,
        } 

        res = self.client.patch(ME_URL,payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.department, payload['department'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)