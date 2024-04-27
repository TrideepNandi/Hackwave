from django.contrib import admin
from .models import CustomUser, Elder, FamilyMember, Volunteer, Doctor, Visit, Medicine, SOS, Exercise, Reward

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'role', 'address', 'is_active', 'is_staff']

class ElderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'medical_history', 'emergency_contact']
    # list_display = all

class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'elder', 'relationship_to_elder']

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'badge_level', 'total_hours_volunteered']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'specialty']

class VisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'volunteer', 'elder', 'visit_date', 'visit_report', 'photos']

class MedicineAdmin(admin.ModelAdmin):
    list_display = ['id', 'elder', 'name', 'dosage', 'reminder_time']

class SOSAdmin(admin.ModelAdmin):
    list_display = ['id', 'elder', 'time', 'message']

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'elder', 'recommendation', 'frequency']

class RewardAdmin(admin.ModelAdmin):
    list_display = ['id', 'volunteer', 'badge', 'date_awarded']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Elder, ElderAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(SOS, SOSAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Reward, RewardAdmin)