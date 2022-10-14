from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField,PasswordResetForm,SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _

USER = get_user_model()

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
                                    widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'New Password'
            }))
    new_password2 = forms.CharField(
                                    widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm New Password'
            }))
            
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


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }))

    class Meta:
        model = USER
        fields = (
            "first_name",
            "last_name",
            'username',
            'email',
            'password',
            'confirm_password',
        )

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username here'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name here'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name here'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),
        }

    def clean(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError("Please make sure your passwords match")
        return super().clean()


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = USER
        fields = (
            "first_name",
            "last_name",
            'email',
            'image',
            'mobile',
            'birthday',
            'gender',
        )
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name here'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name here'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image'
            }),
            'mobile': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile'
            }),
            'birthday': forms.DateInput(attrs={
                'placeholder':'Birth Date', 
                'class': 'form-control',
                'type': 'date',                                                                 
            }),
            'gender': forms.Select(attrs={
                'placeholder':'MR or MRs', 
                'class': 'form-control', 
            }),
        }

class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }), max_length=255)

