

from django.urls import path
from .consumer import MobileConsumer

ws_urlpatterns = [
    path('mobile/',MobileConsumer().as_asgi())
]