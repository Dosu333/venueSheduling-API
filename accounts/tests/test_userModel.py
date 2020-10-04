from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Department

# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        """Test for creating user with email successful"""
        email = 'hello@GMAIL.com'
        password = 'testPass123'
        dept = Department.objects.create(name='econs')

        user = get_user_model().objects.create_user(
            email = email,  
            password = password,
            department = dept,
            first_name = 'Dosu',
            last_name = 'Chase',
        )
        print(user)

    def test_user_create(self):
        email = 'hello@gmail.com'
        password = 'testPass123'

        checkuser = get_user_model().objects.get(email=email)
        self.assertEqual(checkuser.email,email)
        self.assertTrue(checkuser.check_password(password))


    def test_email_normalize(self):
        """Test email for new user is normalized"""
        email = 'hello@gmail.com'
        user = get_user_model().objects.get(email=email)

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email and raises exceptions"""
        password = 'testPass123'
        dept = Department.objects.create(name='econs')

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password = password,
                department = dept,
                first_name = 'Dosu',
                last_name = 'Chase',
            )