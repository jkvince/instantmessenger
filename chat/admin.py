from django.contrib import admin
from django.utils.html import format_html

from . import models

class ChatMemberInline(admin.TabularInline):
    model = models.ChatMember
    extra = 0

class MessagesInline(admin.TabularInline):
    model = models.Message
    extra = 0

@admin.register(models.Chat)
class AdminChat(admin.ModelAdmin):
    list_display = ['name', 'id', 'admin', 'datecreated']
    search_fields = ['id', 'name']
    inlines = [ChatMemberInline]

    readonly_fields = ['chat_transcript']

    def chat_transcript(self, obj):
        messages = obj.get_messages().order_by('-datesent')

        html_content = ""
        for msg in messages:
            sender = msg.get_sender_model()
            html_content += f"<strong>{sender}: </strong>{msg.content}<br>"
        return format_html(html_content)

    chat_transcript.short_description = "Messages"


@admin.register(models.ChatMember)
class AdminChatMember(admin.ModelAdmin):
    list_display = ['id', 'user', 'chat', 'datejoined']
    inlines = [MessagesInline]


@admin.register(models.Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ['id', 'chatmember', 'content', 'datesent']