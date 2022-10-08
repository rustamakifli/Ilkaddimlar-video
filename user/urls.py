
from django.urls import path,re_path
from user import views as template_views

urlpatterns = [
    path('', template_views.UserLoginView.as_view(), name='login'),
    path('logout/', template_views.logout, name='logout'),
    path('account/<int:pk>', template_views.UpdatePersonalInfoView.as_view(), name='account'),
    path('register/', template_views.RegisterView.as_view(), name='register'),
    path('forgot/', template_views.ResetPasswordView.as_view(), name='password_reset'),
    path('change_password/', template_views.ChangePasswordView.as_view(), name='change_password'),

    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,33})/$',
        template_views.Activate.as_view(), name='activate'),
    re_path(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,33})/$',
        template_views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_change/done/', template_views.password_success, name="password_success"),

]