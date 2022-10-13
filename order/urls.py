from django.urls import path
from order.views import card,checkout,SuccessView,CancelView,CartPageView,wishlist
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('cart/', CartPageView.as_view(), name='cart'),
    path('checkout/<pk>/',checkout,name='checkout'),
    path('success/',SuccessView.as_view(),name='success'),
    path('cancel/',CancelView.as_view(),name='cancel'),
    path("wishlist/", wishlist, name="wishlist"),


]