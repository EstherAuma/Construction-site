from django.shortcuts import render,redirect
from .forms import WorkerForm, MaterialForm
from .models import Worker, Material


# For API
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WorkerSerializer
from rest_framework import status
from django.http import Http404
from rest_framework import status



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


# Template Views
def workers(request):
    workers = Worker.objects.all()
    return render(request, "pages/workers.html", {"workers": workers})

def add_workers(request):
    form = WorkerForm(request.POST)
    if request.method == "POST":
        
        if form.is_valid():
            form.save()
    return render(request, "pages/addworkers.html", {"form": form})

def add_materials(request):
    form = MaterialForm(request.POST)
    if request.method == "POST":   
        if form.is_valid():
            form.save()
    return render(request, "pages/addmaterials.html", {"rice": form})

def materials(request):
    materials = Material.objects.all()
    return render(request, "pages/materials.html", {"cars": materials})


def worker_detail(request, pk):
    worker = Worker.objects.get(pk=pk)
    return render(request, "pages/worker-details.html", {"worker": worker})


def edit_workers(request, pk):
    worker = Worker.objects.get(pk=pk)
    form = WorkerForm(request.POST or None, instance=worker)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/', kwargs={'pk': pk})
    return render(request, "pages/edit-worker.html", {"form": form})
