from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render, reverse
from django.utils import timezone
from .forms import CommentForm
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
        selected_post.comments.order_by("-timestamp")
        comment_form = CommentForm()
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, "gallery/post.html", {"post": selected_post, "comment_form": comment_form})


def comment(request, post_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = Post.objects.get(pk=post_id)
            new_comment.timestamp = timezone.now()
            new_comment.save()
    return redirect(reverse('gallery:post', args=[post_id]))
