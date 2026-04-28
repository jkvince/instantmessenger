from django.db import models
import uuid

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32, null=False)
    admin = models.ForeignKey('user.UserModel', on_delete=models.CASCADE)
    datecreated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:detail-view', args=[str(self.id)])

    def get_members(self):
        return ChatMember.objects.filter(chat=self)

    def get_messages(self):
        return Message.objects.filter(chatmember__in=self.get_members()).order_by('datesent')

    def create_chat_complete(self, name, admin):
        chat = self.model(name=name, admin=admin)
        ChatMember.objects.create(user=admin, chat=chat)
        return chat

class ChatMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    datejoined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " in " + str(self.chat)

    def short_str(self):
        return self.user.username

    def get_user_model(self):
        return self.user

    def get_messages(self):
        return Message.objects.filter(chatmember=self).order_by('datesent')


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chatmember = models.ForeignKey(ChatMember, on_delete=models.CASCADE)
    datesent = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)

    def __str__(self):
        return str(self.id)

    def get_sender_model(self):
        return self.chatmember.get_user_model()

    def get_chat(self):
        return self.chatmember.chat