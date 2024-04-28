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
    first_name = models.CharField(max_length=255, default="Default_First_Name")
    last_name = models.CharField(max_length=255, default="Default_Last_Name")
    gender = models.CharField(max_length=255, default="Default_Gender")
    device_token = models.CharField(max_length=255, blank=True, null=True)

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
    age = models.PositiveIntegerField(default=60)
    emergency_contact = models.ManyToManyField('FamilyMember', related_name='related_elders', blank=True)

class FamilyMember(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    elders = models.ManyToManyField(Elder, related_name='family_members', blank=True)

class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    points_required = models.IntegerField()
    badge = models.ImageField(upload_to='badges/')


class VolunteerAchievement(models.Model):
    volunteer = models.ForeignKey('Volunteer', on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(null=True, blank=True)
    progress = models.IntegerField()
    unlocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.progress >= self.achievement.points_required:
            self.unlocked = True
        super().save(*args, **kwargs)

class Volunteer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    skills = models.TextField(null=True, blank=True)  # Skills the volunteer has
    interests = models.TextField(null=True, blank=True)  # Interests of the volunteer
    availability = models.TextField(null=True, blank=True)  # When the volunteer is available
    date_joined = models.DateField(auto_now_add=True)  # When the volunteer joined
    badges = models.CharField(max_length=20)  # Bronze, Silver, Gold, Platinum, etc.
    achievements = models.ManyToManyField(Achievement, through='VolunteerAchievement')
    total_points = models.IntegerField()

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
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default="0")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default="0")    
class Exercise(models.Model):
    elder = models.ForeignKey(Elder, on_delete=models.CASCADE)
    recommendation = models.TextField()
    frequency = models.CharField(max_length=50)

# class Reward(models.Model):
#     volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
#     badge = models.CharField(max_length=50)  # Bronze, Silver, Gold, Platinum, etc.
#     date_awarded = models.DateTimeField(auto_now_add=True)
