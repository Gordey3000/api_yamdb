from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Comment, Review, User

from .serializers import (CommentSerializer,
                          ReviewSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title_id(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title_id().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.get_title_id().id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_title_id(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review_id(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return Comment.objects.filter(title=self.get_title_id().id,
                                      review=self.get_review_id().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.get_title_id().id,
                        review_id=self.get_review_id().id)
