from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review')
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router_v1.urls)),
]
