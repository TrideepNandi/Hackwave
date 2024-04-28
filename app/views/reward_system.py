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

    @action(detail=True, methods=['post'])
    def reward(self, request, pk=None):
        volunteer = self.get_object()
        achievement_id = request.data.get('achievement_id')
        try:
            achievement = Achievement.objects.get(id=achievement_id)
        except Achievement.DoesNotExist:
            return Response({'error': 'Achievement does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        volunteer_achievement, created = VolunteerAchievement.objects.get_or_create(
            volunteer=volunteer, 
            achievement=achievement, 
            defaults={'progress': achievement.points_required}
        )
        if created:
            volunteer_achievement.unlocked = True
            volunteer_achievement.save()
            return Response({'status': 'Achievement rewarded.'})
        else:
            return Response({'status': 'Achievement already rewarded.'})

class VolunteerAchievementViewSet(viewsets.ModelViewSet):
    queryset = VolunteerAchievement.objects.all()
    serializer_class = VolunteerAchievementSerializer