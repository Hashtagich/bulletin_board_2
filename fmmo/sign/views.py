# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView

from .models import BaseRegisterForm
from fan_forum.models import User


# Create your views here.


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self,  request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=True)
            else:
                return render(self.request, 'sing/invalid_code.html')
            return redirect('account_login')