# views.crud.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from app.models import CustomUser, Elder, FamilyMember, Volunteer, Doctor, Visit, Medicine, SOS, Exercise, Reward
from app.serializers import CustomUserSerializer, ElderSerializer, FamilyMemberSerializer, VolunteerSerializer, DoctorSerializer, VisitSerializer, MedicineSerializer, SOSSerializer, ExerciseSerializer, RewardSerializer
from app.firebasemanager import send_sos_ring
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=['post'])
    def by_phone_number(self, request):
        phone_number = request.data.get('phone_number', None)
        if phone_number is not None:
            user = get_object_or_404(CustomUser, phone_number=phone_number)
            serializer = self.get_serializer(user)
            role_data = None
            if user.role == 'elder':
                role_data = Elder.objects.get(user=user.id)
                role_serializer = ElderSerializer(role_data)
            elif user.role == 'familymember':
                role_data = FamilyMember.objects.get(user=user.id)
                role_serializer = FamilyMemberSerializer(role_data)
            elif user.role == 'volunteer':
                role_data = Volunteer.objects.get(user=user.id)
                role_serializer = VolunteerSerializer(role_data)
            elif user.role == 'doctor':
                role_data = Doctor.objects.get(user=user.id)
                role_serializer = DoctorSerializer(role_data)
            if role_data is not None:
                return Response({
                    'user': serializer.data,
                    'role_data': role_serializer.data
                })
            else:
                return Response(serializer.data)
        else:
            return Response({'error': 'A phone number must be provided'}, status=status.HTTP_400_BAD_REQUEST)

class ElderViewSet(viewsets.ModelViewSet):
    queryset = Elder.objects.all()
    serializer_class = ElderSerializer

class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class SOSViewSet(viewsets.ModelViewSet):
    queryset = SOS.objects.all()
    serializer_class = SOSSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Get the elder who sent the SOS
        elder = serializer.instance.elder

        # Get the family members and volunteers associated with the elder
        family_members = FamilyMember.objects.filter(elder=elder)
        volunteers = Volunteer.objects.filter(elder=elder)

        # Send an SOS ring to each family member and volunteer
        for family_member in family_members:
            send_sos_ring(family_member.user.device_token)
        for volunteer in volunteers:
            send_sos_ring(volunteer.user.device_token)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer