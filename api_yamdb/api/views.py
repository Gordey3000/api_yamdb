from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core import mail
from api_yamdb.settings import YAMDB_EMAIL
User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    """
    Отправление письма на почту с подтверждением и генерация токена
    """
    email = request.data.get('email')
    if email is None:
        message = 'Введите электронную почту'
    else:
        user = get_object_or_404(User, email=email)
        confirmation_code = default_token_generator.make_token(user)
        message_in_email = f'Ваш уникальный код для работы с YaMDb: {confirmation_code}'
        mail.send_mail(
            message_in_email,
            YAMDB_EMAIL, [email],
            fail_silently=False
        )
        user.confirmation_code = confirmation_code
        message = email
        user.save()
    return Response({'email': message})
