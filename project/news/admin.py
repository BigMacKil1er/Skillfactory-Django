from django.contrib import admin
from .models import Post, Category, UserSubscriber
# Register your models here.
admin.site.register(Post)
from django.contrib.auth.models import Permission
admin.site.register(Permission)
admin.site.register(Category)
admin.site.register(UserSubscriber)