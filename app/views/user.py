# views/user.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from app.serializers import CustomUserSerializer, LoginSerializer, ElderSerializer, FamilyMemberSerializer, VolunteerSerializer, DoctorSerializer
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
                user_serializer = CustomUserSerializer(user)  # Serialize the CustomUser instance
                if user.role == 'elder':
                    user_data = Elder.objects.get(user=user)
                    role_serializer = ElderSerializer(user_data)
                elif user.role == 'familymember':
                    user_data = FamilyMember.objects.get(user=user)
                    role_serializer = FamilyMemberSerializer(user_data)
                elif user.role == 'volunteer':
                    user_data = Volunteer.objects.get(user=user)
                    role_serializer = VolunteerSerializer(user_data)
                elif user.role == 'doctor':
                    user_data = Doctor.objects.get(user=user)
                    role_serializer = DoctorSerializer(user_data)
                print(user_data)
                if user_data is not None: 
                    return Response({
                        'token': token.key, 
                        'user': user_serializer.data,  # Include the serialized CustomUser data
                        'role_data': role_serializer.data  # Include the serialized role-specific data
                    }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)