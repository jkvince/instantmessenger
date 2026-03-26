from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
import uuid

from chat.models import Chat, ChatMember, Message

class UserModel(AbstractUser):
    is_online = models.BooleanField(null=False, default=False)

    # Excluded
    first_name = None
    last_name = None

    def create_user(self, username, email, password):
        if not email or not username or not password:
            raise ValueError("Parameter required is missing")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def get_all_chat_members(self):
        return ChatMember.objects.filter(user=self)

    def get_chats(self):
        return Chat.objects.filter(chatmember__in=self.get_all_chat_members())

    def get_member_from_chat(self, chat):
        try:
            return ChatMember.objects.get(user=self, chat=chat)
        except ChatMember.DoesNotExist:
            return ChatMember.DoesNotExist
        except ChatMember.MultipleObjectsReturned:
            return ChatMember.MultipleObjectsReturned


class UserChannel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user.UserModel', on_delete=models.PROTECT, editable=False)
    websocketid = models.CharField(max_length=64, editable=False)
    dateopened = models.DateTimeField(auto_now=True)
    dateclosed = models.DateTimeField()

    def close(self):
        self.dateclosed = timezone.now()