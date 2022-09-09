from pickle import TRUE
from statistics import mode
from urllib import request
from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView
import stripe
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from order.models import Cart,Cart_Item
# Create your views here.


def card(request):

    context = {
        'title': 'Card Sellshop'
    }
    return render(request, "cart.html",context=context)

class CartPageView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        courses = Cart.objects.filter(is_ordered=False)
        context = super(CartPageView, self).get_context_data(**kwargs)
        context.update({
            "carts":courses
        })
        return context        


class CancelView(TemplateView):
    template_name = 'cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def checkout(request,pk,**kwargs):
    if request.method == "POST":
        cart_id = Cart.objects.get(pk=pk)
        arr = []
        try:
            discount = Cart.objects.get(
                    user=request.user, is_ordered=False).coupon.discount
            discount = float(discount)
        except:
            discount = 0
        courses = Cart_Item.objects.filter(
            cart=Cart.objects.get(user=request.user,is_ordered=False))

        for i in range(len(courses)):      
            courses[i].price = f'{(float(courses[i].price) * (100-discount))/100:.2f}'
            courses[i].save()
            arr.append(Cart_Item.objects.filter(cart=Cart.objects.get(
                    user=request.user, is_ordered=False))[i])
        domain = 'http://127.0.0.1:8000/'
        stripe.api_key = 'sk_test_51LdsfuDNgtzlZOilAnigbnTQrdYzgZaMCvyDmsrpCXlmVpJfSoHc6bsKvFooCAMu3kSN5X3m3iv5E7lw5j2gPup700G9KKZOOT'
        line_items = []
        for i in range(len(arr)):
                print("---------------------")
                print(arr[i].course.image)
                print("---------------------")
                line_items.append(
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(float(arr[i].course.price)*100*(100 - discount)/100),
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
                success_url=domain + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain + 'cancel/',
                client_reference_id = cart_id

            )
        print(checkout_session.client_reference_id)
       
            
            
        return redirect(checkout_session.url, code=303)
    context = {
        'title': 'Checkout'
    }
    return render(request,'checkout.html',context=context)


class SuccessView(TemplateView):
    template_name = 'success.html'

    def get(self,request,*args,**kwargs):
        if request.GET:
            if request.GET.get('session_id'):
                stripe.api_key = 'sk_test_51LdsfuDNgtzlZOilAnigbnTQrdYzgZaMCvyDmsrpCXlmVpJfSoHc6bsKvFooCAMu3kSN5X3m3iv5E7lw5j2gPup700G9KKZOOT'
                session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
                if session:
                        Cart.objects.filter(is_ordered=False).filter(user=request.user).update(is_ordered=True,
                        ordered_at=datetime.now())
                        user_cart = Cart.objects.filter(user=request.user).filter(
                                is_ordered=True).first()
                        Cart_Item.objects.filter(is_paid=False).filter(
                            cart=user_cart).update(is_paid=True)
                        Cart.objects.get_or_create(user=request.user, is_ordered=False)
                        print('success works')

                else :
                        print('cancel works')
                        Cart.objects.filter(is_ordered=False).filter(user=request.user).update(is_ordered=False)
        return render(request, 'success.html')
