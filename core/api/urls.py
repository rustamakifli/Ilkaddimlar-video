from django.urls import path
from core.api import views as api_views


urlpatterns = [
    path('subscribers/', api_views.SubscriberCreateAPIView.as_view(), name="subscriber"),
]


