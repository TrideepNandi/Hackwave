# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import user, crud
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
router.register('reward', crud.RewardViewSet)

urlpatterns = [
    path('user/signup/', user.SignupView.as_view(), name='signup'),
    path('user/login/', user.LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]