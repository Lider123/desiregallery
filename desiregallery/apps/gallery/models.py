from django.db import models
from django.utils.deconstruct import deconstructible
from sorl.thumbnail import ImageField
from uuid import uuid4
import os

# Create your models here.


@deconstructible
class UploadImage(object):

    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


class Post(models.Model):

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    image = ImageField(upload_to=UploadImage("content"), verbose_name="Изображение")
    timestamp = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        storage, name = self.image.storage, self.image.name
        super(Post, self).delete(*args, **kwargs)
        storage.delete(name)


class Comment(models.Model):

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    comment_text = models.CharField(max_length=200, verbose_name="Текст комментария")
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")


class Vote(models.Model):

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    value = models.IntegerField(verbose_name="Значение")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
