from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.html import strip_tags


# Create your models here.
class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscriber = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author
    title = models.CharField(max_length=255, default='Заголовок')
    text = RichTextUploadingField()
    datetime_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')  # связь «многие ко многим» с моделью Category

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def preview(self):
        result = strip_tags(self.text)
        return f'{result[:40]}...'

    def get_absolute_url(self):
        return f'/posts/{self.id}'


class Response(models.Model):
    text = models.TextField()
    datetime_response = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author
    accept = models.BooleanField(default=False)

    def preview(self):
        if len(self.text) > 20:
            result = f'{self.text[:20]}...'
        else:
            result = self.text
        return result

    def get_absolute_url(self):
        return f'/response/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Category
