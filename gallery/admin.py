from django.contrib import admin

from .models import Comment, Post, Vote

# Register your models here.


class CommentInline(admin.StackedInline):
    model = Comment


class VoteInline(admin.StackedInline):
    model = Vote


class PostsAdmin(admin.ModelAdmin):
    inlines = (CommentInline, VoteInline, )
    ordering = ("-timestamp", )


admin.site.register(Post, PostsAdmin)
