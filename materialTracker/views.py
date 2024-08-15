from django.shortcuts import render,redirect,get_object_or_404
from .forms import WorkerForm, MaterialForm
from .models import Worker, Material


# For API
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WorkerSerializer,UserSerializer
from rest_framework import status
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny



# API Views
class WorkerListAPIView(APIView):
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


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'username': user.username,
                'email': user.email,
                'token': token.key
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
        form = MaterialForm()  # Only create a new form when the method is not POST

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
    material = Material.objects.get(pk=pk)
    form = MaterialForm(request.POST or None, instance=material)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/materials')
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