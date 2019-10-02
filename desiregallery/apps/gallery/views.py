from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from .models import Post

# Create your views here.


def index(request):
    post_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(post_list, 16)

    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(request, "gallery/index.html", {"posts": posts})


def post(request, post_id):
    try:
        selected_post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, "gallery/post.html", {"post": selected_post})
