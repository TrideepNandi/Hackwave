# views.crud.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from app.models import CustomUser, Elder, FamilyMember, Volunteer, Doctor, Visit, Medicine, SOS, Exercise, LiveLocation
from app.serializers import CustomUserSerializer, ElderSerializer, FamilyMemberSerializer, VolunteerSerializer, DoctorSerializer, VisitSerializer, MedicineSerializer, SOSSerializer, ExerciseSerializer, LiveLocationSerializer
from app.firebasemanager import send_sos_ring
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from pyfcm import FCMNotification
from datetime import timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from app.tasks import send_reminder
import json

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=['post'])
    def by_phone_number(self, request):
        phone_number = request.data.get('phone_number', None)
        if phone_number is not None:
            user = get_object_or_404(CustomUser, phone_number=phone_number)
            serializer = self.get_serializer(user)
            role_data = None
            try:
                if user.role == 'elder':
                    role_data = Elder.objects.get(user=user.id)
                    role_serializer = ElderSerializer(role_data)
                elif user.role == 'family_member':
                    role_data = FamilyMember.objects.get(user=user.id)
                    role_serializer = FamilyMemberSerializer(role_data)
                elif user.role == 'volunteer':
                    role_data = Volunteer.objects.get(user=user.id)
                    role_serializer = VolunteerSerializer(role_data)
                elif user.role == 'doctor':
                    role_data = Doctor.objects.get(user=user.id)
                    role_serializer = DoctorSerializer(role_data)
            except (Elder.DoesNotExist, FamilyMember.DoesNotExist, Volunteer.DoesNotExist, Doctor.DoesNotExist):
                raise NotFound('No role data found for this user.')
            if role_data is not None:
                return Response({
                    'user': serializer.data,
                    'role_data': role_serializer.data
                })
            else:
                return Response(serializer.data)
        else:
            return Response({'error': 'A phone number must be provided'}, status=status.HTTP_400_BAD_REQUEST)

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

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        medicine = serializer.save()

        # Get the reminder time
        reminder_time = medicine.reminder_time

        # Create a crontab schedule that runs at the reminder time every day
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=reminder_time.minute, 
            hour=reminder_time.hour, 
            day_of_week='*', 
            day_of_month='*', 
            month_of_year='*'
        )

        # Create a unique task name
        task_name = f"send_reminder_{medicine.id}"

        # Try to get the existing task
        try:
            task = PeriodicTask.objects.get(name=task_name)
            # If the task exists, update its schedule
            task.crontab = schedule
            task.save()
        except PeriodicTask.DoesNotExist:
            # If the task doesn't exist, create a new one
            PeriodicTask.objects.create(
                crontab=schedule, 
                name=task_name, 
                task='app.tasks.send_reminder', 
                args=json.dumps([medicine.id])
            )

        headers = self.get_success_headers(serializer.data)
        return Response({"medicine_data" : serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    

class SOSViewSet(viewsets.ModelViewSet):
    queryset = SOS.objects.all()
    serializer_class = SOSSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Get the elder who sent the SOS
        elder = Elder.objects.get(id=serializer.data['elder'])

        # Get the family members and volunteers associated with the elder
        family_members = FamilyMember.objects.filter(user__elder=elder)
        volunteers = Volunteer.objects.filter(user__elder=elder)
        
      # Prepare the list of device tokens
        device_tokens = []
        for family_member in family_members:
            device_tokens.append(family_member.user.device_token)
        for volunteer in volunteers:
            device_tokens.append(volunteer.user.device_token)

        # Prepare the data message
        data_message = {
            "title": "SOS Alert",
            "body": serializer.data['message'],
            "latitude": serializer.data['latitude'],
            "longitude": serializer.data['longitude'],
        }

        # Send an SOS ring to each family member and volunteer

        # Send the SOS ring to all devices
        push_service = FCMNotification(api_key="AAAA-N0VBwc:APA91bETlr8giC9S2mEw09zfzib1jdxAkICdPyQWj7XISCz_N-fkpuzf3dIrU5UtGKas2HQqGzYmFAJpfueTKOSyZaFEQbjyjrtT524-UOEiOygJuXyhrcF9CYBrZ8Ybnb33TtTInlZu")
        result = push_service.multiple_devices_data_message(registration_ids=device_tokens, data_message=data_message)

        # token = "eqlPrAHATiaAXmtM7hbhDK:APA91bHTDoiZAHVMYFg_z1Xy8oT6BNW7t4FR774bzom7VgLfvtVb9JuQf9LTSjajlCkYBykaqpDbbC_5EDO7__kt71hAdviIiCGYnBBFBKoWSa14RfDjrBwhZ7vDJt870ahxDC4S_aW5"
        token = "frAd-a4wQGuwpdr5txw6Ci:APA91bGOO7DIsWowFie2VGK2E71OwGzWIR_PT9o-LxdhKizjs2YxChkK1MWkI68FsAEiFg8UrpyUahU_VoetuPZwndEhYOZ4tc-aW6sHQhKZjZE4ub5exEn7R-DAN8nVZXxosh6--SSs"
        message_title = "SOS Alert"
        message_body = "I need help"
        result = send_sos_ring(token, message_title=message_title, message_body=message_body)

        # for family_member in family_members:
        #     send_sos_ring(family_member.user.device_token, message_title=message_title, message_body=message_body)
        # for volunteer in volunteers:
        #     send_sos_ring(volunteer.user.device_token, message_title=message_title, message_body=message_body)

        headers = self.get_success_headers(serializer.data)
        return Response({"result of notification": result, "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class LiveLocationViewSet(viewsets.ModelViewSet):
    serializer_class = LiveLocationSerializer
    queryset = LiveLocation.objects.all()  # Default queryset

def get_queryset(self):
    # Get the family_member id from the request
    family_member_id = self.request.query_params.get("family_member")
    print(family_member_id)

    # Get the FamilyMember object
    family_member = FamilyMember.objects.get(id=family_member_id)
    print(family_member)

    # Get all the elders associated with the family_member
    elders = family_member.elders.all()  # Change this line
    print(elders)

    # Get the live locations of these elders
    queryset = LiveLocation.objects.filter(elder__in=elders)

    return queryset

# class RewardViewSet(viewsets.ModelViewSet):
#     queryset = Reward.objects.all()
#     serializer_class = RewardSerializer