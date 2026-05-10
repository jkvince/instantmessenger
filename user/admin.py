from django.contrib import admin
from . import models

@admin.register(models.UserModel)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_superuser', 'is_online', 'last_login']

@admin.register(models.UserChannel)
class AdminChannel(admin.ModelAdmin):
    list_display = ['id', 'user', 'websocketid', 'dateopened', 'dateclosed']