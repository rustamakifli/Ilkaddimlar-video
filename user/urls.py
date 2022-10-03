
from django.urls import path
from user import views as template_views

urlpatterns = [
    path('', template_views.UserLoginView.as_view(), name='login'),
    path('logout/', template_views.logout, name='logout'),
    path('account/<int:pk>', template_views.UpdatePersonalInfoView.as_view(), name='account'),
    path('register/', template_views.RegisterView.as_view(), name='register'),
    path('change_password/', template_views.ChangePasswordView.as_view(), name='change_password'),
    # path('password_change/done/', template_views.password_success, name="password_success"),


]