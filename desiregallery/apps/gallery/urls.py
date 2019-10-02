from django.urls import path, re_path

from . import views

app_name = "gallery"
urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^post/(?P<post_id>\d+)/$", views.post, name="post"),
    path("post/<int:post_id>/comment/", views.comment, name='comment'),
]
