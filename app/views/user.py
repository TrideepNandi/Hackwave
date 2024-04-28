# views/user.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from app.serializers import CustomUserSerializer, LoginSerializer
from app.models import Elder, FamilyMember, Volunteer, Doctor


class SignupView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            if user:
                return Response({'message': "User Created Successfully", 'token': token.key, 'user': str(user.role), 'user_data': serializer.data}, status=status.HTTP_201_CREATED)        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate(phone_number=phone_number, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                # if user.role == 'Elder':
                #     user_data = Elder.objects.get(user=user)
                # elif user.role == 'FamilyMember':
                #     user_data = FamilyMember.objects.get(user=user)
                # elif user.role == 'Volunteer':
                #     user_data = Volunteer.objects.get(user=user)
                # elif user.role == 'Doctor':
                #     user_data = Doctor.objects.get(user=user)
                return Response({'token': token.key, 'user': str(user.role)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)