from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpApi, TokenAPI, UserViewSet

router = DefaultRouter()

app_name = 'api'

router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [path('v1/', include(router.urls)),
               path('v1/auth/token/', TokenAPI.as_view(), name='get_token'),
               path('v1/auth/signup/', SignUpApi.as_view(), name='signup'),
               ]
