from django.db import models

from django.utils import timezone

# Create your models here.

class Worker(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False,unique=True)
    email = models.EmailField(max_length=50, null=False, blank=False,unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Attendance(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
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
    date_purchased = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name} {self.date_purchased}"
    
class MaterialUsage(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=10, null=False, blank=False)
    date_used = models.DateField(default=timezone.now)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f"{self.material.name}  {self.date_used}"
    
    @property
    def total_price(self):
        return self.quantity * self.price_per_unit

