from django.urls import path, include
from order.api import views


urlpatterns = [
    path('cart/', views.CartView.as_view(), name='card'),
    # path('checkout/', views.CheckoutAPIView.as_view(), name='checkoutapi'),
    path('cart-item/', views.CartItemView.as_view(), name='cart_item'),
    path('coupon/', views.CouponAPIVIew.as_view(), name='couponapi'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('wishlist/', views.WishlistAPIView.as_view(), name='wishlist'),

]

# urlpatterns += router.urls
