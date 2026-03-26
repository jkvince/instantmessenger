from django.urls import path, include

from . import views

app_name = 'user'


urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup')
]
