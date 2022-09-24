
from django.urls import path
from user import views as template_views

urlpatterns = [
    path('', template_views.UserLoginView.as_view(), name='login'),
    path('logout/', template_views.logout, name='logout'),
    path('account/', template_views.account, name='account'),
    path('register/', template_views.RegisterView.as_view(), name='register'),
]