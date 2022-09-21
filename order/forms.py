from django import forms
from order.models import Coupon


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = (
            'code',
        )
        widgets = {
            'code': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Apply coupon',
                'class': 'form-control',
            })
        }