from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Person)
admin.site.register(models.FriendRequest)
admin.site.register(models.Notification)
admin.site.register(models.Groups)
admin.site.register(models.Message)
admin.site.register(models.Post)
