from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from user.forms import  LoginForm
from django.contrib.auth.views import LoginView

from user.forms import (
        LoginForm,
        )

USER = get_user_model()

  


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    # success_url = reverse_lazy('courses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        print(' this works')
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print('why this fuckin function not works')
            return redirect('courses')
        return super().dispatch(request, *args, **kwargs)


@login_required
def logout(request):
    django_logout(request)
    return redirect('courses')
