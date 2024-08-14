from django.urls import path
from . import views
from .views import WorkerListAPIView, WorkerDetailAPIView

urlpatterns = [
    path("", views.workers, name="workers"),
    path("addworkers/", views.add_workers, name="addworkers"),
    path("addmaterials/", views.add_materials, name="addmaterials"),
    path("materials/", views.materials, name="materials"),
    path("api/workers/", WorkerListAPIView.as_view(), name="workers"),
    path("api/workers/<int:pk>/", WorkerDetailAPIView.as_view(), name="workers")
]