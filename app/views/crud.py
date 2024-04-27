# views.crud.py
from rest_framework import viewsets
from app.models import CustomUser, Elder, FamilyMember, Volunteer, Doctor, Visit, Medicine, SOS, Exercise, Reward
from app.serializers import CustomUserSerializer, ElderSerializer, FamilyMemberSerializer, VolunteerSerializer, DoctorSerializer, VisitSerializer, MedicineSerializer, SOSSerializer, ExerciseSerializer, RewardSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer