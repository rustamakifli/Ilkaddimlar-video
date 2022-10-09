from django.urls import path
from core import views as template_views

urlpatterns = [
    path('', template_views.HomeView.as_view(), name="home"),
    path('contact/', template_views.ContactView.as_view(), name="contact"),
]