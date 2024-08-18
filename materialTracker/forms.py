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
        widgets = {
            'date_purchased': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'unit': forms.Select(choices=Material.UNIT_CHOICES, attrs={'class': 'form-control'})
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['worker', 'date', 'time_in', 'time_out', 'daily_rate']

class MaterialUsageForm(forms.ModelForm):
    class Meta:
        model = MaterialUsage
        fields = ['material', 'quantity', 'date_used', 'price_per_unit']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example'}),
        }