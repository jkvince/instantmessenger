from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View

from django.http import HttpResponse

from . import models

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chat:home')
        else:
            return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('chat:home')
        
        else:
            return HttpResponse("Error")


class ForgotPassword(View):
    pass


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        models.UserModel.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('chat:home')