from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import *


User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Perfectly singed up', status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully activated', status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Perfectly logout out', status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        print(request.auth)
        print(dir(request))
        email = request.user.email
        User = get_user_model()
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_email(
            email=email, activation_code=user.activation_code, is_password=True)
        return Response('Activation code has been sent to your email', status=status.HTTP_200_OK)


class ForgotPasswordComplete(APIView):
    def post(self, request, activation_code):
        data = request.data
        data["activation_code"] = activation_code
        serializer = CreateNewPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('You have successfully reset your password', status=status.HTTP_200_OK)
