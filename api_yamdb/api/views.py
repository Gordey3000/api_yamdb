from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from .filters import FilterTitleSet
from .mixins import CreateDeleteViewSet
from .permissions import (
    AuthorIsAuthenticatedModeratorAdminSuperuserOrReadOnly,
    IsAdminOnlyPermission, IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserTokenSerializer, GenreSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleReadSerializer,
                          UserMeSerializer, UsersSerializer)

User = get_user_model()


class TokenAPI(APIView):

    '''Отправляет и обновляет токен пользователю.'''

    def post(self, request):
        serializer = CustomUserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if str(user.confirmation_code) == confirmation_code:
            refresh = RefreshToken.for_user(user)
            token = {'token': str(refresh.access_token)}
            return Response(token, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):

    '''Получение и редактирование информации о пользователе.'''

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdminOnlyPermission,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH', ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_user(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserMeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(user,
                                          data=request.data,
                                          partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpApi(APIView):

    '''Получение confirmation_code на email при регистрации.'''

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        user = User.objects.filter(username=request.data.get('username'),
                                   email=request.data.get('email')).first()
        if user:
            serializer = RegistrationSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=request.data.get('username'))
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        send_mail(
            'Код подверждения для регистрации на платформе YaMDb',
            confirmation_code,
            settings.DEFAULT_EMAIL,
            (serializer.validated_data['email'], ),
            fail_silently=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(CreateDeleteViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class CategoryViewSet(CreateDeleteViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.order_by('id').annotate(
        rating=Avg('review__score')
    )
    serializer_class = TitleCreateSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    http_method_names = [
        'get', 'post', 'patch', 'delete'
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitleSet

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorIsAuthenticatedModeratorAdminSuperuserOrReadOnly,)
    http_method_names = [
        'get', 'post', 'patch', 'delete'
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user,
                        title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorIsAuthenticatedModeratorAdminSuperuserOrReadOnly,)
    http_method_names = [
        'get', 'post', 'patch', 'delete'
    ]

    def get_queryset(self):
        get_review = get_object_or_404(Review,
                                       id=self.kwargs.get('review_id'),
                                       title_id=self.kwargs.get('title_id'))
        return get_review.comments.all()

    def perform_create(self, serializer):
        get_review = get_object_or_404(Review,
                                       id=self.kwargs.get('review_id'),
                                       title_id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user,
                        review=get_review)
