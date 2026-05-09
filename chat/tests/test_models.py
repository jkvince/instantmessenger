from django.test import TestCase

from user.models import UserModel
from chat.models import Chat, ChatMember, Message

class ChatModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            "john1", 
            "john@john.com", 
            "password123"
        )

        cls.chat = Chat.objects.create(name="TestChat", admin=cls.user)
        cls.chatmember = ChatMember.objects.create(user=cls.user, chat=cls.chat)
        cls.message = Message.objects.create(chatmember=cls.chatmember, content="test")

    def test_custom_create(self):
        full_chat = Chat.objects.create_chat_complete("FullTestChat", self.user)
        m = full_chat.get_members()
        self.assertEqual(len(m), 1)

    def test_get_absolute_url(self):
        self.assertEqual(self.chat.get_absolute_url(), f'/chat/loadchat/{self.chat.id}/')

    def test_get_members(self):
        query = self.chat.get_members()
        self.assertEqual(len(query), 1)
        self.assertEqual(self.chatmember, query[0])

    def test_get_messages(self):
        query = self.chat.get_messages()
        self.assertEqual(len(query), 1)
        self.assertEqual(self.message, query[0])


class ChatMemberModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            "john1", 
            "john@john.com", 
            "password123"
        )

        cls.chat = Chat.objects.create(name="TestChat", admin=cls.user)
        cls.chatmember = ChatMember.objects.create(user=cls.user, chat=cls.chat)
        cls.message = Message.objects.create(chatmember=cls.chatmember, content="test")

    def test_short_str(self):
        self.assertEqual(self.chatmember.short_str(), "john1")

    def test_get_user_model(self):
        self.assertEqual(self.chatmember.get_user_model(), self.user)

    def test_get_messages(self):
        query = self.chatmember.get_messages()
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], self.message)

    def test_new_message(self):
        message = self.chatmember.new_message("New Message")
        query = self.chatmember.get_messages()
        self.assertEqual(len(query), 2)
        self.assertEqual(query[0], self.message)



class MessageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            "john1", 
            "john@john.com", 
            "password123"
        )

        cls.chat = Chat.objects.create(name="TestChat", admin=cls.user)
        cls.chatmember = ChatMember.objects.create(user=cls.user, chat=cls.chat)
        cls.message = Message.objects.create(chatmember=cls.chatmember, content="test")

    def test_get_sender_model(self):
        self.assertEqual(self.message.get_sender_model(), self.user)

    def test_get_chat(self):
        self.assertEqual(self.message.get_chat(), self.chat)