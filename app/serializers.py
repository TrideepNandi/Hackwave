from rest_framework import serializers
from .models import CustomUser, Elder, FamilyMember, Volunteer, Doctor, Visit, Medicine, SOS, Exercise, Reward
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)


    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'), phone_number=phone_number, password=password)

            if user is None:
                raise serializers.ValidationError('Invalid phone number or password.')
            if not user.is_active:
                raise serializers.ValidationError('User is deactivated.')
        else:
            raise serializers.ValidationError('Must include "phone number" and "password".')
        return data

class ElderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = '__all__'

class FamilyMemberSerializer(serializers.ModelSerializer):
    elders = serializers.PrimaryKeyRelatedField(many=True, queryset=Elder.objects.all())

    class Meta:
        model = FamilyMember
        fields = '__all__'

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class SOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOS
        fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'