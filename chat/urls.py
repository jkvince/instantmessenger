from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'chat'


urlpatterns = [
    path('', views.Main.as_view(), name='home'),

    path('loadchat/<uuid:pk>/', views.LoadChat.as_view(), name='loadchat'),
    path('createchat/', views.CreateChat.as_view(), name='createchat'),
    path('createmessage/', views.CreateMessage.as_view(), name='createmessage'),

    path('logout/', views.Logout.as_view(), name='logout')
]
