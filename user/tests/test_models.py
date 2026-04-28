from django.test import TestCase

from user.models import UserModel
from chat.models import Chat, ChatMember

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            "john1", 
            "john@john.com", 
            "password123"
        )
        cls.chat1 = Chat.objects.create(name='TestChat1', admin=cls.user)
        cls.chat2 = Chat.objects.create(name='TestChat2', admin=cls.user)

        cls.chat1member = ChatMember.objects.create(user=cls.user, chat=cls.chat1)
        cls.chat2member = ChatMember.objects.create(user=cls.user, chat=cls.chat2)

    def test_customcreate_username(self):
        self.assertEqual(self.user.username, "john1")

    def test_customcreate_email(self):
        self.assertEqual(self.user.email, "john@john.com")

    def test_customcreate_password(self):
        self.assertTrue(self.user.check_password("password123"))

    def test_get_all_chat_members(self):
        query = self.user.get_all_chat_members()
        self.assertIn(self.chat1member, query)
        self.assertIn(self.chat2member, query)

    def test_get_chats(self):
        query = self.user.get_chats()
        self.assertIn(self.chat1, query)
        self.assertIn(self.chat2, query)

    def test_get_member_from_chat(self):
        query1 = self.user.get_member_from_chat(self.chat1)
        query2 = self.user.get_member_from_chat(self.chat2)
        self.assertEqual(self.chat1member, query1)
        self.assertEqual(self.chat2member, query2)
