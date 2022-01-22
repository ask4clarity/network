from django.contrib import admin
from .models import Follow, User, Post 

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)