from .models import Worker, Material
from rest_framework import serializers
from django.contrib.auth.models import User

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user