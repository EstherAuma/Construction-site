from .models import Worker, Material
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"


class WorkerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Worker
        fields = ('first_name', 'last_name','email','phone_number','password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        worker = Worker.objects.create(**validated_data)
        return worker