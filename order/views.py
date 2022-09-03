from pickle import TRUE
from statistics import mode
from urllib import request
from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView
import stripe
from django.http import JsonResponse
from datetime import datetime
from order.models import Cart,Cart_Item
# Create your views here.


def card(request):
    context = {
        'title': 'Card Sellshop'
    }
    return render(request, "cart.html",context=context)

class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

class CancelView(TemplateView):
    template_name = 'cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

def checkout(request):
    if request.method == "POST":
        arr = []
        courses = Cart_Item.objects.filter(
            cart=Cart.objects.get(user=request.user,is_ordered=False))

        for i in range(len(courses)):
            courses[i].price = f'{float(courses[i].price)}'
            courses[i].save()
            arr.append(Cart_Item.objects.filter(cart=Cart.objects.get(
                    user=request.user, is_ordered=False))[i])
        domain = 'http://127.0.0.1:8000/'
        stripe.api_key = 'sk_test_51LdsfuDNgtzlZOilAnigbnTQrdYzgZaMCvyDmsrpCXlmVpJfSoHc6bsKvFooCAMu3kSN5X3m3iv5E7lw5j2gPup700G9KKZOOT'
        line_items = []
        for i in range(len(arr)):
                print(arr[i].course.image)
                line_items.append(
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(float(arr[i].course.price)*100),
                            'product_data': {
                                'name': arr[i].course.title,
                                'images': [arr[i].course.image],
                            },
                        },
                        'quantity':1,
                    }
                )
        checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                payment_method_types=[
                    'card',
                ],
                mode='payment',
                success_url=domain + '/success/',
                cancel_url=domain + '/checkout/',
            )
        Cart.objects.filter(is_ordered=False).filter(user=request.user).update(is_ordered=True,
        ordered_at=datetime.now())

        Cart.objects.get_or_create(user=request.user, is_ordered=False)
        return JsonResponse(checkout_session.url, code=303)
    context = {
        'title': 'Checkout'
    }
    return render(request,'checkout.html',context=context)