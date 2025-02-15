from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from order.api.serializers import CartItemSerializer, CartSerializer,CouponSerializer,SuccessSerializer,WishlistSerializer
from order.models import Cart, Cart_Item,Coupon,Wishlist
from user.models import User
from courses.models import Course

User = get_user_model()

class CartView(APIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        obj = Cart.objects.get(user=request.user)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        template = request.data.get('template')
        course = Course.objects.get(pk=course_id)
        cart, created = Cart.objects.get_or_create(
            user=request.user, is_ordered=False)
        if course:
            cart_item, created = Cart_Item.objects.get_or_create(
                cart=cart, course=course)
            if template == "cart.html":
                Cart_Item.objects.filter(cart=cart, course=course).update(
                     price=course.price)
                Cart.objects.get(user=request.user,
                                 is_ordered=False).course.add(course)
            elif template == "course-list.html":
                Cart_Item.objects.filter(cart=cart, course=course).update(
                   price=course.price)
                Cart.objects.get(user=request.user,
                                 is_ordered=False).course.add(course)
            elif template == "remove_from_cart":
                Cart_Item.objects.filter(cart=cart, course=course).delete()
                Cart.objects.get(user=request.user,
                                 is_ordered=False).course.remove(course)
            message = {'success': True,
                       'message': 'Course added to your card.'}
            return Response(message, status=status.HTTP_201_CREATED)
        message = {'success': False, 'message': 'Course not found.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class CartItemView(APIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        Cart.objects.get_or_create(user=request.user, is_ordered=False)
        obj = Cart_Item.objects.filter(
            cart=Cart.objects.get(user=request.user, is_ordered=False)).order_by('created_at')
        serializer_context = {
            'request': request,
        }
        serializer = self.serializer_class(obj, many=True,context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SuccessView(APIView):
    serializer_class = SuccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_cart=Cart.objects.filter(user=request.user, is_ordered=True).last()
        obj = Cart_Item.objects.filter(cart=user_cart).order_by('created_at').filter(is_paid=True)
        serializer_context = {
            'request': request,
        }
        serializer = self.serializer_class(obj, many=True,context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CouponAPIVIew(APIView):
    serializer_class = CouponSerializer

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        if code and Coupon.objects.filter(code=code,is_active=True).exists():
            if Cart.objects.filter(user=request.user, is_ordered=False, coupon=Coupon.objects.get(code=code)).count() == 0:
                if Cart.objects.filter(user=request.user, is_ordered=False, coupon=None).exists():
                    obj, created = Cart.objects.get_or_create(
                        user=request.user, is_ordered=False)
                    obj.coupon = Coupon.objects.get(code=code)
                    for i in range(len(Coupon.objects.filter(code=obj.coupon))):
                        print(Cart.objects.filter(user=request.user, is_ordered=False, coupon=Coupon.objects.get(code=code)).count())
                        
                        other_quantity =Coupon.objects.filter(code=obj.coupon)[
                            i].used + 1
                        quantity = Coupon.objects.filter(code=obj.coupon)[
                            i].is_available - 1
                        if quantity == 0:
                            Coupon.objects.filter(code=obj.coupon).update(is_available=quantity,used=other_quantity,is_active=False)
                        else:
                            Coupon.objects.filter(code=obj.coupon).update(is_available=quantity,used=other_quantity)
                    
                    obj.save()
                    message = {'success': True,
                               'message': 'Coupon applied.'}
                    return Response(message, status=status.HTTP_201_CREATED)
                message = {'success': False,
                           'message': 'Coupon already applied to this cart.'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            message = {'success': False,
                       'message': 'You can apply coupon only once.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'success': False, 'message': 'Coupon not found.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class WishlistAPIView(APIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        obj, created = Wishlist.objects.get_or_create(user=request.user)
        serializer_context = {
            'request': None,
        }
        serializer = self.serializer_class(obj,context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        course = Course.objects.get(pk=course_id)
        Wishlist.objects.get_or_create(user=request.user)
        wishlist = Wishlist.objects.get(user=request.user)
        if course and course not in wishlist.course.all():
            wishlist.course.add(course)
        else:
            wishlist.course.remove(course)
        message = {'success': True,
                   'message': 'Course added to your wishlist.'}
        return Response(message, status=status.HTTP_201_CREATED)

