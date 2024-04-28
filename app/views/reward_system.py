from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from app.models import Achievement, Volunteer, VolunteerAchievement
from app.serializers import AchievementSerializer, VolunteerSerializer, VolunteerAchievementSerializer

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer


class VolunteerAchievementViewSet(viewsets.ModelViewSet):
    queryset = VolunteerAchievement.objects.all()
    serializer_class = VolunteerAchievementSerializer