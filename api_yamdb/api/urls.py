from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpApi, TitleViewSet, TokenAPI,
                    UserViewSet)

router = DefaultRouter()
app_name = 'api'

router.register('users', UserViewSet, basename='users')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_urls = [
    path('signup/', SignUpApi.as_view(), name='signup',),
    path('token/', TokenAPI.as_view(), name='get_token')
]

urlpatterns = [path('v1/', include(router.urls)),
               path('v1/auth/', include(auth_urls)),
               ]
