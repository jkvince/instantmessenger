from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('user.urls')),
    path('chat/', include('chat.urls')),

    path('admin/', admin.site.urls),
]
