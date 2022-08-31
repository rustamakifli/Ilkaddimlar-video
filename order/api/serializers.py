from rest_framework import serializers
from order.models import Cart,Cart_Item
from django.db.models import fields
from django.contrib.auth import get_user_model
from courses.api.serializers import CourseSerializer
User = get_user_model()

class CartSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "courses")

    def get_courses(self, obj):
        qs = obj.course.all()
        return CourseSerializer(qs, many=True).data


class CartItemSerializer(serializers.ModelSerializer):
    courses = CourseSerializer()
    is_ordered = serializers.SerializerMethodField()

    class Meta:
        model = Cart_Item
        fields = ("course", "is_ordered")

    def get_is_ordered(self, obj):
        qs = obj.cart.is_ordered
        return qs
