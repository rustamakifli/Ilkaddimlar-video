from django.urls import path
from order.views import card,checkout,SuccessView,CancelView

urlpatterns = [
    path('cart/', card, name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('success/',SuccessView.as_view(),name='success'),
    path('cancel/',CancelView.as_view(),name='cancel')

]