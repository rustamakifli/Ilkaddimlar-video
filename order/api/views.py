from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from order.api.serializers import CartItemSerializer, CartSerializer
from order.models import Cart, Cart_Item
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
        print('course',course_id)
        template = request.data.get('template')
        print('template',template)
        course = Course.objects.get(pk=course_id)
        cart, created = Cart.objects.get_or_create(
            user=request.user, is_ordered=False)
        if course:
            cart_item, created = Cart_Item.objects.get_or_create(
                cart=cart, course=course)
            if template == "cart.html":
                print('cart.html wokrs')
                Cart_Item.objects.filter(cart=cart, course=course).update(
                     price=course.price)
                Cart.objects.get(user=request.user,
                                 is_ordered=False).course.add(course)
            elif template == "course-list.html":
                print('course-list.html works')
                Cart_Item.objects.filter(cart=cart, course=course).update(
                   price=course.price)
                Cart.objects.get(user=request.user,
                                 is_ordered=False).course.add(course)
            elif template == "remove_from_cart":
                print('remove from cart works')
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
