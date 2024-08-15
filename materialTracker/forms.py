from django.forms import ModelForm
from django import forms
from .models import Worker, Attendance, Material, MaterialUsage

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['first_name', 'last_name', 'phone_number', 'email']
   
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'quantity','unit',  'date_purchased']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['worker', 'date', 'time_in', 'time_out', 'daily_rate']