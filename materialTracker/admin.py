from django.contrib import admin
from .models import Worker, Attendance, Material, MaterialUsage
# Register your models here.

admin.site.register(Worker)
admin.site.register(Attendance)
admin.site.register(Material)
admin.site.register(MaterialUsage)