from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login

from rest_framework import generics, permissions, exceptions

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from rest_framework.views import status, APIView

from rest_framework_jwt.settings import api_settings

from rest_framework.parsers import MultiPartParser, FormParser

from .models import User

from .helper import *

from .serializer import (UserLoginSerializer, UserSerializer, TokenSerializer)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# payload = jwt_payload_handler(user)
# token = jwt_encode_handler(payload)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def index(request):
    return Response(
        data = {
            'message': 'Welcome to Corpers Corner'
        }, status = status.HTTP_200_OK
    )


