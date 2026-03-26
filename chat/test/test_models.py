from django.test import TestCase

from chat import models
from user import models

class ChatModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = models.UserModel.objects.filter(username='vin')
        models.Chat.objects.create(name='Test', admin=user)

    def test_get_members(self):
        self.assertTrue(True)
