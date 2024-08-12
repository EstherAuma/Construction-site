from django.urls import path
from . import views

urlpatterns = [
    path("", views.workers, name="workers"),
    path("addworkers/", views.add_workers, name="addworkers"),
    path("addmaterials/", views.add_materials, name="addmaterials"),
]