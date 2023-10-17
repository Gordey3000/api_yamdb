from .views import (TokenAPI, UserViewSet, SignUpApi,
                    GenreViewSet,
                    CategoryViewSet,
                    CommentViewSet,
                    ReviewViewSet,
                    TitleViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView
# )
router = DefaultRouter()
app_name = 'api'

router.register(
    'users',
    UserViewSet,
    basename='users'
)

router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [path('v1/', include(router.urls)),
               path('v1/auth/token/', TokenAPI.as_view(), name='get_token'),
               path('v1/auth/signup/', SignUpApi.as_view(), name='signup'),
               ]

# path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
# path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# path('v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
