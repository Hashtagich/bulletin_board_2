from random import sample
from string import hexdigits

from allauth.account.forms import SignupForm
from django.core.mail import send_mail
from django.forms import ModelForm
from django.conf import settings

from .models import Post, Response


# Создаём модельную форму
class PostForm(ModelForm):
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


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject='Код активации',
            message=f'Ваш код активации {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user