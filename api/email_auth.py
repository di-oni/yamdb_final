import logging

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Code
from .serializers import (
    CheckEmailCodeSerializer,
    CodeSerializer,
    EmailSerializer,
    UserTokenSerializer,
)
from .utils import generate_code, get_tokens_for_user, send_message


User = get_user_model()

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


@api_view(['POST'])
def get_code(request):
    """Get a confirmation code when the email received during registration."""
    email = EmailSerializer(data=request.data)
    email.is_valid(raise_exception=True)
    has_code = Code.objects.filter(email=email)
    if has_code.exists():
        has_code.delete()

    confirmation_code = generate_code()
    data = {
        'email': request.data['email'],
        'confirmation_code': confirmation_code,
    }
    code_serializer = CodeSerializer(data=data)
    code_serializer.is_valid(raise_exception=True)
    code_serializer.save()

    message = send_message(request.data['email'], confirmation_code)
    response = Response(message, status=status.HTTP_200_OK)
    return response


@api_view(['POST'])
def get_token(request):
    """Get tokens for data user's request."""
    incoming_data = CheckEmailCodeSerializer(data=request.data)
    incoming_data.is_valid(raise_exception=True)

    user_serializer = UserTokenSerializer(data=request.data)
    user_serializer.is_valid(raise_exception=True)
    user = user_serializer.save()
    token = get_tokens_for_user(user)
    return Response(token, status=status.HTTP_200_OK)
