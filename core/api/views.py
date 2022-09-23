from rest_framework import generics
from rest_framework.response import Response
from core.api.serializers import SubscriberSerializer
from core.models import Subscriber


class SubscriberCreateAPIView(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer