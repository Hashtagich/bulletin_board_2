from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# Create your models here.
class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author
    title = models.CharField(max_length=255, default='Заголовок')
    # text = models.TextField(default='Текст объявления')
    text = RichTextUploadingField(default='Текст объявления',
                                  config_name='special',
                                  external_plugin_resources=[(
                                      'youtube',
                                      'staticc/ckeditor/ckeditor/plugins/youtube',
                                      'plugin.js',
                                  )],
                                  )
    datetime_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')  # связь «многие ко многим» с моделью Category

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'


class Response(models.Model):
    text = models.TextField()
    datetime_response = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author
    accept = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text[:20]}...'

    def get_absolute_url(self):
        return f'/response/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Category