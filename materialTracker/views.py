from django.shortcuts import render
from .forms import WorkerForm, MaterialForm
from .models import Worker, Material

# Create your views here.

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