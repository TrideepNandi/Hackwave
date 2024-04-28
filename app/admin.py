from django.contrib import admin
from .models import CustomUser, Elder, FamilyMember, Volunteer, Doctor, Visit, Medicine, SOS, Exercise

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'role', 'address', 'is_active', 'is_staff']

class ElderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'medical_history', 'display_emergency_contact']

    def display_emergency_contact(self, obj):
        return ", ".join([family_member.user.phone_number for family_member in obj.emergency_contact.all()])
    display_emergency_contact.short_description = 'Emergency Contact'

class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'display_elders']

    def display_elders(self, obj):
        return ", ".join([elder.user.phone_number for elder in obj.elders.all()])
    display_elders.short_description = 'Elders'

# class VolunteerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'badge_level', 'total_hours_volunteered']

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

# class RewardAdmin(admin.ModelAdmin):
#     list_display = ['id', 'volunteer', 'badge', 'date_awarded']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Elder, ElderAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)
# admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(SOS, SOSAdmin)
admin.site.register(Exercise, ExerciseAdmin)
# admin.site.register(Reward, RewardAdmin)