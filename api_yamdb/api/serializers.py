from reviews.models import User, Genre, Category
from rest_framework import serializers
from django.core.exceptions import ValidationError


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class CustomUserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать me в качестве поля username нельзя!')
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


'''class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        '''


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate(self, attrs):
        # Проверка на наличие обязательных полей и их правильность
        if attrs.get('name') is None or attrs.get('slug') is None:
            raise ValidationError("Некорректные данные")
        return attrs
