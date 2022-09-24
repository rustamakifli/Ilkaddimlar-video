
from django.urls import path,re_path
from user import views as template_views

urlpatterns = [
    path('', template_views.UserLoginView.as_view(), name='login'),
    path('logout/', template_views.logout, name='logout'),
    path('account/', template_views.account, name='account'),
    path('register/', template_views.register, name='register'),
    # path('detail/<int:pk>', template_views.UserDetailView.as_view(), name='user_detail'),
]