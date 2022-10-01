from rest_framework import serializers
from order.models import Cart,Cart_Item,Coupon,Wishlist
from django.db.models import fields
from django.contrib.auth import get_user_model
from courses.api.serializers import CourseSerializer
User = get_user_model()

class CartSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "course")

    def get_course(self, obj):
        qs = obj.course.all()
        return CourseSerializer(qs, many=True).data


class CartItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    is_ordered = serializers.SerializerMethodField()   
    coupon_discount = serializers.SerializerMethodField()

    class Meta:
        model = Cart_Item
        fields = ("course", "is_ordered","coupon_discount")

    def get_is_ordered(self, obj):
        qs = obj.cart.is_ordered
        return qs

    def get_coupon_discount(self, obj):
        if obj.cart.coupon:
            qs = obj.cart.coupon.discount
            return qs
        return 0

class SuccessSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    is_ordered = serializers.SerializerMethodField()   
    coupon_discount = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart_Item
        fields = ("course", "is_ordered","coupon_discount","is_paid")

    def get_is_ordered(self, obj):
        qs = obj.cart.is_ordered
        return qs
    def get_coupon_discount(self, obj):
        if obj.cart.coupon:
            qs = obj.cart.coupon.discount
            return qs
        return 0

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = '__all__'

    def get_course(self, obj):
        qs = obj.course.all()
        return CourseSerializer(qs, many=True).data