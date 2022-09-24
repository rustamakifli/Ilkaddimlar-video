from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from user.forms import  LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView as RegisterView

from user.forms import (
        LoginForm,
        )

USER = get_user_model()

  


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


@login_required
def logout(request):
    django_logout(request)
    return redirect('home')


@login_required
def account(request):
    return render(request, "my-account.html")


def register(request):
    return render(request, "register.html")