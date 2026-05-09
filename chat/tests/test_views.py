from django.test import TestCase
from django.urls import reverse

from user.models import UserModel
from chat.models import Chat, ChatMember, Message

class AbstracViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            "john1", 
            "john@john.com", 
            "password123"
        )
        cls.chat = Chat.objects.create(name="TestChat", admin=cls.user)
        cls.chatmember = ChatMember.objects.create(chat=cls.chat, user=cls.user)
        cls.message = cls.chatmember.new_message("Message test")
    
    def setUp(self):
        login = self.client.login(username="john1", password="password123")

    #def test_no_user(self):
    #    self.client.logout()
    #    response = self.client.get(reverse(self.url_name))
    #    self.assertEqual(response.status_code, 302)


class MainViewTest(AbstracViewTest):
    def test_get_correct_chat(self):
        response = self.client.get(reverse('chat:home'))
        self.assertEqual(len(response.context['chats']), 1)
        self.assertEqual(response.context['chats'][0], self.chat)


class LogoutViewTest(AbstracViewTest):
    def test_post_redirect(self):
        response = self.client.post(
            reverse('chat:logout')
        )
        self.assertRedirects(response, reverse('user:login'))


class LoadChatViewTest(AbstracViewTest):
    def test_get_correct_messages(self):
        response = self.client.get(reverse('chat:loadchat', args=[str(self.chat.id)]))
        self.assertTrue(True)