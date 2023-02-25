from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    h1 = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL', default='')
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    time_created = models.DateField(default=now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField(default='')
    time_created = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return self.text
