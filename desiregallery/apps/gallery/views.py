from collections import namedtuple
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import redirect, render, reverse
from django.utils import timezone
from .forms import CommentForm
from .models import Post


VotedPost = namedtuple("VotedPost", ["post", "avg_vote"])

# Create your views here.


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    votes = list(map(lambda p: p.votes.aggregate(Avg("value")), posts))
    data = list(map(lambda z: VotedPost(z[0], z[1]["value__avg"] or 0.), zip(posts, votes)))

    paginator = Paginator(data, 16)
    page = request.GET.get("page")
    data = paginator.get_page(page)
    return render(request, "gallery/index.html", {
        "data_page": data,
    })


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
