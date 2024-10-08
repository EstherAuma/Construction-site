from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
import uuid

from django.utils import timezone
def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')

# Create your models here.

class Worker(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False,unique=True)
    email = models.EmailField(max_length=50, null=False, blank=False,unique=True)
    password = models.CharField(max_length=128, null=False, blank=False,default='password')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def is_authenticated(self):
        return True
    
class WorkerToken(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE, related_name='auth_token')
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.key)
    
class Attendance(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, validators=[validate_not_future_date])
    time_in = models.TimeField(default=timezone.now)
    time_out = models.TimeField(default=timezone.now)
    daily_rate= models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f"{self.worker.first_name} {self.worker.last_name} {self.date}"
    
class Material(models.Model):
    UNIT_CHOICES = [
        ('m', 'Meters'),
        ('kg', 'Kilograms'),
        ('t', 'Tons'),
        ('L', 'Liters'),
        ('pcs', 'Pieces'),
    ]
    name = models.CharField(max_length=50, null=False, blank=False)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    quantity = models.PositiveIntegerField(default=0)
    date_purchased = models.DateField(default=timezone.now, validators=[validate_not_future_date])

    def __str__(self):
        return f"{self.name}"
    
class MaterialUsage(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0) 
    date_used = models.DateField(default=timezone.now, validators=[validate_not_future_date])
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f"{self.material.name}"
    
    @property
    def total_price(self):
        
        return self.quantity * self.price_per_unit
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            material = self.material
            if material.quantity < self.quantity:
                raise ValidationError("Insufficient material quantity")
            material.quantity -= self.quantity
            material.save()
        super().save(*args, **kwargs)
        
class AggregatedContent(models.Model):
    data = models.JSONField(null=False)
    def __str__(self):
        return str(self.id)
