from django.contrib import admin
from .models import Post, Response


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'category']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content', 'status']


admin.site.register(Post, PostAdmin)
admin.site.register(Response, ReplyAdmin)