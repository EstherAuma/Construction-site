from django.forms import ModelForm
from .models import Worker, Attendance, Material, MaterialUsage

class WorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = ['first_name', 'last_name', 'phone_number', 'email']