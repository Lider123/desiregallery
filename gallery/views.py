from django.http import Http404
from django.shortcuts import render
from .models import Post

# Create your views here.


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "index.html", {"posts": posts})


def post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, "post.html", {"post": post})
