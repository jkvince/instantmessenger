from django.test import TestCase

from user.models import UserModel
from user.models import Chat

class ChatTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            "john1", 
            "john@john.com", 
            "password123"
        )

        cls.chat = Chat.objects.create_chat_complete("TestChat", cls.user)

    def test(self):
        self.assertTrue(True)



