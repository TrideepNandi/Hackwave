# views.crud.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from app.models import CustomUser, Elder, FamilyMember, Volunteer, Doctor, Visit, Medicine, SOS, Exercise
from app.serializers import CustomUserSerializer, ElderSerializer, FamilyMemberSerializer, VolunteerSerializer, DoctorSerializer, VisitSerializer, MedicineSerializer, SOSSerializer, ExerciseSerializer
from app.firebasemanager import send_sos_ring
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from pyfcm import FCMNotification


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
        push_service = FCMNotification(api_key="YOUR_SERVER_KEY")
        result = push_service.multiple_devices_data_message(registration_ids=device_tokens, data_message=data_message)

        token = "eEB6IeaYSdCYq8VgNrh-n1:APA91bHIVmTqLzKjo7vfTdtzelayOFGGFgsdV8PafLYnvm4E5MeF61pa37Gybn4rtg2LkiS1KusbBXmMCUChsQlQ1paxkFRvK0sIemuulxRujdm6Vt6Pz8j5BVPEOK8E0llhdGBPOQw1"
        message_title = "SOS Alert"
        message_body = "I need help"
        # result = send_sos_ring(token, message_title=message_title, message_body=message_body)

        for family_member in family_members:
            send_sos_ring(family_member.user.device_token, message_title=message_title, message_body=message_body)
        for volunteer in volunteers:
            send_sos_ring(volunteer.user.device_token, message_title=message_title, message_body=message_body)

        headers = self.get_success_headers(serializer.data)
        return Response({"result of notification": result, "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

# class RewardViewSet(viewsets.ModelViewSet):
#     queryset = Reward.objects.all()
#     serializer_class = RewardSerializer