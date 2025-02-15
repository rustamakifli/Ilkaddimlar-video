from pickle import TRUE
from statistics import mode
from urllib import request
from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView
import stripe
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from order.models import Cart,Cart_Item,Wishlist
from courses.models import Course,Category,Tag,Author
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


def card(request):

    context = {
        'title': 'Card Sellshop',
        'categories': Category.objects.annotate(number_of_courses = Count("category_courses")).all(),
        'discounted_courses':Course.objects.filter(discount__isnull=False),
        'all_courses':Course.objects.filter(is_active=True),
        'popularcourses':Course.objects.all()[0:3],
        'tags':Tag.objects.all(),
        'authors':Author.objects.annotate(number_of_courses = Count("author_courses")).all()[0:6]
    }
    return render(request, "cart.html",context=context)

class CartPageView(LoginRequiredMixin,TemplateView):
    template_name = "cart.html"
    context_object_name = 'cart'
    
    def dispatch(self, request, *args, **kwargs) :
        if not request.user.is_authenticated:
            return render(request,'404.html')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        courses = Cart.objects.filter(is_ordered=False)
        context = super(CartPageView, self).get_context_data(**kwargs)
        context.update({
            "cart":courses.first(),
            'popularcourses':Course.objects.all()[0:3],
            'categories': Category.objects.annotate(number_of_courses = Count("category_courses")).all(),
            'discounted_courses':Course.objects.filter(discount__isnull=False),
            'all_courses':Course.objects.filter(is_active=True),
            'tags':Tag.objects.all(),
            'authors':Author.objects.annotate(number_of_courses = Count("author_courses")).all()[0:6],
            
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
        if arr[i].course.discounted_price != 0.00:
            domain = 'http://127.0.0.1:8000/'
            stripe.api_key = 'sk_test_51LdsfuDNgtzlZOilAnigbnTQrdYzgZaMCvyDmsrpCXlmVpJfSoHc6bsKvFooCAMu3kSN5X3m3iv5E7lw5j2gPup700G9KKZOOT'
            line_items = []
            for i in range(len(arr)):
                    
                    line_items.append(
                        {
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount': int(float(arr[i].course.discounted_price)*100*(100 - discount)/100),
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
        
                
                
            return redirect(checkout_session.url, code=303)
        else:
            Cart.objects.filter(is_ordered=False).filter(user=request.user).update(is_ordered=True,
                        ordered_at=datetime.now())
            user_cart = Cart.objects.filter(user=request.user).filter(
                                is_ordered=True).last()
            Cart_Item.objects.filter(is_paid=False).filter(
                            cart=user_cart).update(is_paid=True)
            return render(request,'success.html')
    context = {
        'title': 'Checkout'
    }
    return render(request,'checkout.html',context=context)


class SuccessView(LoginRequiredMixin,TemplateView):
    template_name = 'success.html'

    def dispatch(self, request, *args, **kwargs) :
        if not request.user.is_authenticated:
            return render(request,'404.html')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
        if request.GET:
            if request.GET.get('session_id'):
                stripe.api_key = 'sk_test_51LdsfuDNgtzlZOilAnigbnTQrdYzgZaMCvyDmsrpCXlmVpJfSoHc6bsKvFooCAMu3kSN5X3m3iv5E7lw5j2gPup700G9KKZOOT'
                session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
                if session:
                        Cart.objects.filter(is_ordered=False).filter(user=request.user).update(is_ordered=True,
                        ordered_at=datetime.now())
                        user_cart = Cart.objects.filter(user=request.user).filter(
                                is_ordered=True).last()
                        Cart_Item.objects.filter(is_paid=False).filter(
                            cart=user_cart).update(is_paid=True)
                        # Cart.objects.get_or_create(user=request.user, is_ordered=False)

                else :
                        Cart.objects.filter(is_ordered=False).filter(user=request.user).update(is_ordered=False)
        context = super(SuccessView, self).get_context_data(**kwargs)
        context.update({
            'popularcourses':Course.objects.all()[0:3],
            'categories': Category.objects.annotate(number_of_courses = Count("category_courses")).all(),
            'discounted_courses':Course.objects.filter(discount__isnull=False),
            'all_courses':Course.objects.filter(is_active=True),
            'tags':Tag.objects.all(),
            'authors':Author.objects.annotate(number_of_courses = Count("author_courses")).all()[0:6],
            
        })
        return render(request, 'success.html',context=context)

def wishlist(request):
    wishlist_courses = Wishlist.objects.filter(user=request.user)

    context = {
        'title': 'Wishlist Sellshop',
        'wishlist':wishlist_courses
    }
    if request.user.is_authenticated:
        return render(request, "wishlist.html", context=context)
    return render(request, "404.html", context=context)
