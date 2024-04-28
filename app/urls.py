# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import user, crud, reward_system
from app.views.get_yoga_recomm import YogaRecommendationsView

router = DefaultRouter()
router.register('user', crud.CustomUserViewSet)
router.register('elder', crud.ElderViewSet)
router.register('family-member', crud.FamilyMemberViewSet)
router.register('volunteer', crud.VolunteerViewSet)
router.register('doctor', crud.DoctorViewSet)
router.register('visit', crud.VisitViewSet)
router.register('medicine', crud.MedicineViewSet)
router.register('sos', crud.SOSViewSet)
router.register('exercise', crud.ExerciseViewSet)
# router.register('reward', crud.RewardViewSet)
router.register(r'achievements', reward_system.AchievementViewSet)
# router.register(r'volunteers', reward_system.VolunteerViewSet)
router.register(r'volunteer_achievements', reward_system.VolunteerAchievementViewSet)

urlpatterns = [
    path('user/signup/', user.SignupView.as_view(), name='signup'),
    path('user/login/', user.LoginView.as_view(), name='login'),
    path('yoga-recommendations/', YogaRecommendationsView.as_view(), name='yoga-recommendations'),
    path('', include(router.urls)),
]