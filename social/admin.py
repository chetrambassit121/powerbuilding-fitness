from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from . import models
from .models import Comment, Notification, Post, PostTest, ThreadModel

admin.site.register(Notification)
admin.site.register(ThreadModel)
admin.site.register(PostTest)



class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ("comment", "created_on", "author")
    list_filter = ("comment", "created_on", "author")
    search_fields = ("comment", "created_on", "author")
admin.site.register(Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ("body", "created_on", "author")
    list_filter = ("body", "created_on", "author")
    search_fields = ("body", "created_on", "author")
admin.site.register(Post, PostAdmin)
