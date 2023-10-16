from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from django.conf import settings
import uuid
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from .serializers import (UserMeSerializer, GenreSerializer,
                          CustomUserTokenSerializer, CategorySerializer,
                          UsersSerializer, RegistrationSerializer)

from .permissions import (IsAdminOrPostOnly, IsAdminOrReadOnly,
                          IsAdminOnlyPermission)
from reviews.models import Genre, Category

User = get_user_model()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrPostOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if request.method != 'GET':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrPostOnly, IsAdminOrReadOnly)
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class TokenAPI(APIView):
    """
    Отправляет и обновляет токен пользователю.
    """
    def post(self, request):
        serializer = CustomUserTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if str(user.confirmation_code) == confirmation_code:
                refresh = RefreshToken.for_user(user)
                token = {'token': str(refresh.access_token)}
                return Response(token, status=status.HTTP_200_OK)

        return Response({'detail': 'Неверные данные'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdminOnlyPermission,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = [
        'get', 'post', 'patch', 'delete'
    ]

    @action(
        methods=['GET', 'PATCH',],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_user(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserMeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpApi(APIView):
    @staticmethod
    def send_reg_mail(email, user):
        confirmation_code = str(uuid.uuid4())
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Код подверждения', confirmation_code,
            settings.DEFAULT_EMAIL, (email, ), fail_silently=False)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        serializer.save(email=email)
        user = get_object_or_404(User, email=email)
        self.send_reg_mail(email, user)
        return Response(serializer.data, status=status.HTTP_200_OK)
