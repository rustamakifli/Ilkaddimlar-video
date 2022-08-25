
from django.urls import path,re_path
from user.views import (
    logout,
    UserLoginView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    
]