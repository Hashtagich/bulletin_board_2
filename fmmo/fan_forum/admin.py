from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Response

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Response)