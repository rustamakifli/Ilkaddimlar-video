from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView 
# PasswordResetView, PasswordResetConfirmView
from django.views.generic import CreateView,TemplateView
from user.forms import RegisterForm, LoginForm
# CustomSetPasswordForm, ResetPasswordForm 
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
USER = get_user_model()
  
  
class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'change-password.html'
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'password_success.html', {})

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'forgot-password.html'
#     # form_class = CustomSetPasswordForm
#     success_url = reverse_lazy('login')

#     def get_success_url(self):
#         return super().get_success_url()
   

# class ResetPasswordView(PasswordResetView):
#     template_name = 'forgot-password.html'
#     # form_class = ResetPasswordForm
#     email_template_name = 'email/reset-password-mail.html'
#     success_url = reverse_lazy('login')

#     def get_success_url(self):
#         return super().get_success_url()   

class SetttingsView(TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
