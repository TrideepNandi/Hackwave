# urls.py
from django.urls import path
from app.views import user

urlpatterns = [
    path('user/signup/', user.SignupView.as_view(), name='signup'),
    path('user/login/', user.LoginView.as_view(), name='login'),
]