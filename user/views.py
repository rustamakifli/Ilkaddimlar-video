from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView 
# PasswordResetView, PasswordResetConfirmView
from django.views.generic import CreateView,TemplateView, UpdateView,View

from user.forms import RegisterForm, LoginForm, PersonalInfoForm,ResetPasswordForm,CustomSetPasswordForm
# CustomSetPasswordForm, ResetPasswordForm 
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from user.utils import account_activation_token

from user.tasks import send_email_confirmation


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


class UpdatePersonalInfoView(LoginRequiredMixin, UpdateView):
    form_class = PersonalInfoForm
    model = USER
    template_name = 'account.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(UpdatePersonalInfoView, self).get_object()
        if not obj.id == self.request.user.id:
            raise Http404
        return obj

    def form_valid(self, form):
        form.instance.first_name = self.request.POST.get('first_name')
        form.instance.last_name = self.request.POST.get('last_name')
        form.instance.email = self.request.POST.get('email')
        form.instance.mobile = self.request.POST.get('mobile')
        form.instance.birthday = self.request.POST.get('birthday')
        form.instance.gender = self.request.POST.get('gender')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.instance
        form.instance.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()
        current_site = self.request.META['HTTP_HOST']
        send_email_confirmation(user, current_site)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'change-password.html'
    success_url = reverse_lazy('login')

class Activate(View):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = USER.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, USER.DoesNotExist):
            user = None
        if user.is_active:
            messages.add_message(request, messages.SUCCESS, 'EMail has been confirm')
            return redirect(reverse_lazy('login'))
        elif user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Email confirmed')
            return redirect(reverse_lazy('login'))
        else:
            messages.add_message(request, messages.SUCCESS, 'Email didnot confirm')
            return redirect(reverse_lazy('/'))

class ResetPasswordView(PasswordResetView):
    template_name = 'forgot-password.html'
    form_class = ResetPasswordForm
    email_template_name = 'email/reset-password-mail.html'
    success_url = reverse_lazy('forget-done')

    def get_success_url(self):
        return super().get_success_url()   

class ForgetPasswordDoneView(views.PasswordResetDoneView):
    """
        Forget password view
    """

    template_name = "forget-done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ForgetPasswordResetConfirmView( views.PasswordResetConfirmView):
    """
        Forget password view
    """

    template_name = "forget-confirm.html"
    post_reset_login = True
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'change-forgot-password.html'
#     form_class = CustomSetPasswordForm
#     success_url = reverse_lazy('login')

#     def get_success_url(self):
#         messages.add_message(self.request, messages.SUCCESS, 'Sizin yeni sifreniz teyin edildi')
#         return super().get_success_url()