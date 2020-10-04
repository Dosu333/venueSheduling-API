from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Department

class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        dept = Department.objects.create(name='econs')

        self.admin_user =  get_user_model().objects.create_superuser(
            email = 'hello@gmail.com',
            password = 'password123', 
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@gmail.com',  
            password = 'password134',
            department = dept,
            first_name = 'Dosu',
            last_name = 'Chase',
        )
    
    def test_users_listed(self):
        """Test that user are listed on user page"""
        url = reverse('admin:accounts_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)

    def test_user_change_page(self):
        """Tests user edit page"""
        url = reverse('admin:accounts_user_change', args=[self.user.id,])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page works"""
        url = reverse('admin:accounts_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)