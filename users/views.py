from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from organisation.models import Organisation
from .serializers import UserSerializer



class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            org_name = f"{user.firstName}'s Organisation"
            organisation = Organisation.objects.create(name=org_name)
            organisation.users.set([user])
            organisation.save()
            token = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "status_code": 201,
                "message": "Registration successful",
                "data": {
                    "accessToken": str(token.access_token),
                    "user": serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "Bad request",
            "status_code": 400,
            "message": "Registration unsuccessful",
            "errors": [{ "field": key, "message": value[0]} for key, value in serializer.errors.items()]
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post (self, request):
        from django.contrib.auth import authenticate
        from rest_framework_simplejwt.tokens import RefreshToken
        
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(token.access_token),
                    "user": serializer.data
                }
            }, status=status.HTTP_200_OK)
        return Response(
            {
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            }, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, userId):
        user = User.objects.filter(userId=userId).first()
        if user and (user == request.user or request.user in user.organisations.all()):
            serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "message": "User retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "Unauthorized",
            "message": "Access denied",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)
