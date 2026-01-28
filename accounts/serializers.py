from rest_framework import serializers
from django.contrib.auth import get_user_model


User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['email', 'phone_number', 'password', 'username']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'id_number_type', 'id_number']
    

    
