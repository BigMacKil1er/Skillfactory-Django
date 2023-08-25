from django.contrib import admin
from .models import Post
# Register your models here.
admin.site.register(Post)
from django.contrib.auth.models import Permission
admin.site.register(Permission)