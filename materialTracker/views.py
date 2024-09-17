from django.shortcuts import render,redirect,get_object_or_404
from .forms import WorkerForm, MaterialForm, AttendanceForm, MaterialUsageForm
from .models import Worker, Material, Attendance, MaterialUsage, WorkerToken
from decimal import Decimal


# For API
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WorkerSerializer,WorkerRegistrationSerializer
from rest_framework import status
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import WorkerToken
from rest_framework.permissions import IsAuthenticated





# API Views

class WorkerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token_key = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed('Invalid token header. No token provided.')

        try:
            token = WorkerToken.objects.get(key=token_key)
        except WorkerToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        return (token.worker, None)
    
class WorkerListAPIView(APIView):
    authentication_classes = [WorkerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class WorkerDetailAPIView(APIView):
    def get(self,request, pk):
        try:
            worker = Worker.objects.get(pk=pk)
        except Worker.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WorkerSerializer(worker)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WorkerCreateAPIView(APIView):
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WorkerUpdateAPIView(APIView):
    def get_object(self, pk):
        try:
            return Worker.objects.get(pk=pk)
        except Worker.DoesNotExist:
            return None

    def put(self, request, pk):
        worker = self.get_object(pk)
        if not worker:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WorkerSerializer(worker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        worker = self.get_object(pk)
        if not worker:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WorkerSerializer(worker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        worker = self.get_object(pk)
        if not worker:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        worker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkerRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WorkerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            worker = serializer.save()

            
            token, created = WorkerToken.objects.get_or_create(worker=worker)

            return Response({
                'first_name': worker.first_name,
                'email': worker.email,
                'token': str(token.key)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Template Views
def workers(request):
    workers = Worker.objects.all()
    return render(request, "pages/workers.html", {"workers": workers})

def add_workers(request):
    form = WorkerForm(request.POST)
    if request.method == "POST":
        
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, "pages/addworkers.html", {"form": form})

def add_materials(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/materials')
    else:
        form = MaterialForm()  

    return render(request, "pages/addmaterials.html", {"form": form})

def materials(request):
    materials = Material.objects.all()
    return render(request, "pages/materials.html", {"cars": materials})


def worker_detail(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    return render(request, "pages/worker-details.html", {"worker": worker})


def edit_workers(request, pk):
    worker = Worker.objects.get(pk=pk)
    form = WorkerForm(request.POST or None, instance=worker)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, "pages/edit-worker.html", {"form": form})


def edit_materials(request, pk):
    
    material = get_object_or_404(Material, pk=pk)
    
    
    form = MaterialForm(request.POST or None, instance=material)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/materials') 
        else:
            print("Form errors:", form.errors)  
    
    return render(request, "pages/edit-material.html", {"form": form})
def delete_worker(request, pk):
    worker = Worker.objects.get(pk=pk)
    worker.delete()
    return redirect('/')

def delete_material(request, pk):
    material = Material.objects.get(pk=pk)
    material.delete()
    return redirect('/materials')

def material_details(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, "pages/material-details.html", {"material": material})

def add_attendance(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance-list')  
    else:
        form = AttendanceForm()
    
    return render(request, 'pages/attendance.html', {'form': form})

def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'pages/attendance-list.html', {'attendances': attendances})

def material_usage(request):
    if request.method == "POST":
        form = MaterialUsageForm(request.POST)
        if form.is_valid():
           
            material_usage = form.save()
            
            return redirect('/')
    else:
        form = MaterialUsageForm()
    
    return render(request, 'pages/material-usage.html', {'form': form})


def material_usage_list(request):
    material_usages = MaterialUsage.objects.all()
    return render(request, 'pages/material-usage-list.html', {'usage': material_usages})


def index(request):
    return render(request, 'pages/index.html')

def edit_attendance(request, pk):
    attendance = Attendance.objects.get(pk=pk)
    form = AttendanceForm(request.POST or None, instance=attendance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('attendance-list')
    return render(request, "pages/edit-attendance.html", {"form": form})

