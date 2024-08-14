from django.urls import path
from . import views
from .views import WorkerListAPIView, WorkerDetailAPIView

urlpatterns = [
    path("", views.workers, name="worker"),
    path("addworkers/", views.add_workers, name="addworkers"),
    path("addmaterials/", views.add_materials, name="addmaterials"),
    path("materials/", views.materials, name="materials"),
    path("workers/<int:pk>/", views.worker_detail, name="worker-detail"),
    path("api/workers/", WorkerListAPIView.as_view(), name="workers"),
    path("api/workers/<int:pk>/", WorkerDetailAPIView.as_view(), name="workers")
]