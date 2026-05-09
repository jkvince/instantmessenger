from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from django.http import HttpResponse

from . import models


class AbstractView(LoginRequiredMixin, View):
    permission_required = 'user.UserModel'


class Main(AbstractView):
    def get(self, request):
        context = {
            'chats' : request.user.get_chats()
        }
        return render(request, 'main.html', context)


class Logout(AbstractView):
    def post(self, request):
        logout(request)
        return redirect('user:login')


class LoadChat(AbstractView):
    def get(self, request, pk):
        # TODO add check if pk is eligible for user
        chat = models.Chat.objects.get(id=pk)
        messages = chat.get_messages()
        member = request.user.get_member_from_chat(chat)
        context = {
            'messages': messages,
            'chat': chat,
            'member': member
        }
        return render(request, 'loadchat.html', context)


class CreateChat(AbstractView):
    def get(self, request):
        return render(request, 'createchat-modal.html')

    def post(self, request):
        name = request.POST.get('chatname')
        new_chat = models.Chat.objects.create(name=name, admin=request.user)
        models.ChatMember.objects.create(user=request.user, chat=new_chat)
        return HttpResponse(status=204)


class CreateMessage(AbstractView):
    def post(self, request):
        content = request.POST.get('content')
        if len(content) == 0: return HttpResponse()

        chatmemberid = request.POST.get('chatmember')
        chatmember = models.ChatMember.objects.get(id=chatmemberid)

        # check if correct user
        if request.user != chatmember.get_user_model(): 
            print("User does not match memberid when creating message")
            print(request.user, "&", chatmember.get_user_model())
            return HttpResponse()

        models.Message.objects.create(chatmember=chatmember, content=content)

        string = f"<p>{chatmember} -> {content}</p>"
        return HttpResponse(string)


