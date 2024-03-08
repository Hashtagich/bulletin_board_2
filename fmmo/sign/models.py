from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms

from fan_forum.models import User


class BaseRegisterForm(UserCreationForm, SignupForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    def save(self, request):
        user = super(BaseRegisterForm, self).save(request)
        basic_group = Group.objects.get(name='authors')
        basic_group.user_set.add(user)
        return user

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)