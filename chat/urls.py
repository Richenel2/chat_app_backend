from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'messages', views.MessageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('login', views.Login.as_view()),
    path('post_message', views.PostMessage.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]