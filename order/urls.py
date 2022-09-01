from django.urls import path
from order.views import card

urlpatterns = [
    path('cart/', card, name='cart'),
]