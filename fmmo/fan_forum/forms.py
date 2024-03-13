from random import sample
from string import hexdigits

from allauth.account.forms import SignupForm
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.forms import ModelForm

from .models import Post, Response
from .models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Создаём модельную форму
class PostForm(ModelForm):
    # text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', ]
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'category': 'Категория',
        }


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        labels = {
            'text': 'Текст',
        }


class CommonSignupForm(UserCreationForm, SignupForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(sample(hexdigits, 5))
        user.code = code

        basic_group = Group.objects.get(name='authors')
        basic_group.user_set.add(user)

        user.save()
        send_mail(
            subject='Код активации',
            message=f'Ваш код активации {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)
