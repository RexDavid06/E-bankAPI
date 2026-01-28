from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from .utils import get_jwt_tokens_for_user

User=get_user_model()

# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "user created"
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({
            "error": "incorrect credentials",
        }, status=status.HTTP_401_UNAUTHORIZED) 
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "date_of_birth": user.date_of_birth,
            "phone_number": user.phone_number,
            "id_number_type": user.id_number_type,
            "id_number": user.id_number,
        })
    
