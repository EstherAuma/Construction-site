from .models import Worker, Material
from rest_framework import serializers

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['first_name','last_name','phone_number']