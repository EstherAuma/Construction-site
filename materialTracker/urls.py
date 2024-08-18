from django.urls import path
from . import views
from .views import WorkerListAPIView, WorkerDetailAPIView, WorkerUpdateAPIView, WorkerCreateAPIView, UserRegistrationAPIView

urlpatterns = [
    # Template URLS
    path("", views.workers, name="worker"),
    path("addworkers/", views.add_workers, name="addworkers"),
    path("addmaterials/", views.add_materials, name="addmaterials"),
    path("materials/", views.materials, name="materials"),
    path("workers/<int:pk>/", views.worker_detail, name="worker-detail"),
    path("editworkers/<int:pk>/", views.edit_workers, name="editworkers"),
    path("editmaterials/<int:pk>/", views.edit_materials, name="edit-materials"),
    path('delete/worker/<int:pk>/', views.delete_worker, name='delete-worker'),
    path('delete/material/<int:pk>/', views.delete_material, name='delete-material'),
    path("materials/<int:pk>/", views.material_details, name="material-details"),
    path("attendance/", views.add_attendance, name="attendance"),
    path("attendance-list/", views.attendance_list, name="attendance-list"),
    path("material-usage/", views.material_usage, name="material-usage"),
    
    # API URLS
    path("api/workers/", WorkerListAPIView.as_view(), name="workers"),
    path("api/workers/<int:pk>/", WorkerDetailAPIView.as_view(), name="workers"),
    path("api/workers/<int:pk>/update/",WorkerUpdateAPIView.as_view(), name="worker-update"),
    path("api/workers/create/", WorkerCreateAPIView.as_view(), name="worker-create"),
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-register'),
]

