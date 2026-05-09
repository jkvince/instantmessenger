from django.test import TestCase
from django.urls import reverse

from user.models import UserModel

class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            "john1", 
            "john@john.com", 
            "password123"
        )
    
    def test_get_no_user(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)

    def test_get_loggedin(self):
        login = self.client.login(username="john1", password="password123")
        response = self.client.get(reverse('user:login'))
        self.assertRedirects(response, reverse('chat:home'))

    def test_post_login(self):
        login_info = {
            'username': 'john1',
            'password': 'password123'
        }

        response = self.client.post(
            reverse('user:login'),     
            login_info
        )
        self.assertRedirects(response, reverse('chat:home'))
        

class SignupViewTest(TestCase):
    
    def test_get_exists(self):
        response = self.client.get(reverse('user:signup'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        new_user = {
            'username': 'john1',
            'email': 'john@john.com',
            'password': 'password123'
        }

        response = self.client.post(
            reverse('user:signup'),
            new_user
        )
        query = UserModel.objects.filter(username='john1')
        self.assertRedirects(response, reverse('chat:home'))
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0].email, 'john@john.com')
        self.assertTrue(query[0].check_password("password123"))
