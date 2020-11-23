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

from .helper import (validate_login_input,validate_password,validate_username, check_if_exist)

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
            'message': 'Welcome to Corpers Corner Booking System'
        }, status = status.HTTP_200_OK
    )

class RegisterUserView(generics.CreateAPIView):

    """ 
    post to register new user auth/register                                                                                                                                                                                                                         
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)


    def post(self, request, *args, **kwargs):
        data = request.data
        username = data['username']
        first_name = data['first_name'] 
        last_name = data['last_name']
        email = data['email']
        password = data['password']

        validate_username(username)
        validate_password(password)
        check_if_exist(email, username)
        
        new_user = User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email ,
            password = password
        )

        new_user_sure = UserSerializer(new_user).data

        return Response(
            data =  new_user_sure,
            status = status.HTTP_201_CREATED 
            
        )


class UserLoginView(generics.CreateAPIView):
    """  
    post login for new user   
     auth/login
    """        
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny , )

    def post(self, request , *args, **kwargs):
        user = validate_login_input(request , request.data)

        if user is not None:
            login(request ,user)
            token_serializer = TokenSerializer(
                data={
                    "token": jwt_encode_handler(
                        jwt_payload_handler(user)
                    )
                }
            )
            if token_serializer.is_valid():
                serializer = UserLoginSerializer(user)
                return Response(
                    data = {
                        'id': serializer.data.get('id'),
                        'username': serializer.data.get('username'),
                        'token': token_serializer.data
                    }, status = status.HTTP_200_OK
                )   
        return Response( 
            data = {
                'message': 'user does not exist'
            }, status = status.HTTP_401_UNAUTHORIZED
        )