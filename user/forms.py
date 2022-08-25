from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _

USER = get_user_model()


class LoginForm(AuthenticationForm):
    class Meta:
        model = USER
        fields = (
            'username',
            'password',
        )
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 
        'class': 'form-control',
        'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

