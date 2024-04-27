from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20)  # Admin, Elder, Family Member, Volunteer, Doctor
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

class Elder(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    medical_history = models.TextField()
    emergency_contact = models.CharField(max_length=15)

class FamilyMember(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE)
    relationship_to_elder = models.CharField(max_length=50)

class Volunteer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    badge_level = models.CharField(max_length=20)  # Bronze, Silver, Gold, Platinum, etc.
    total_hours_volunteered = models.IntegerField()

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)

class Visit(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE)
    visit_date = models.DateTimeField()
    visit_report = models.TextField()
    photos = models.ImageField(upload_to='visit_photos/')

class Medicine(models.Model):
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    reminder_time = models.TimeField()

class SOS(models.Model):
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

class Exercise(models.Model):
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE)
    recommendation = models.TextField()
    frequency = models.CharField(max_length=50)

class Reward(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    badge = models.CharField(max_length=50)  # Bronze, Silver, Gold, Platinum, etc.
    date_awarded = models.DateTimeField(auto_now_add=True)