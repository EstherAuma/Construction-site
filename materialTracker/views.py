from django.shortcuts import render
from .forms import WorkerForm
from .models import Worker

# Create your views here.

def workers(request):
    workers = Worker.objects.all()
    return render(request, "workers.html", {"workers": workers})

def add_workers(request):
    form = WorkerForm(request.POST)
    if request.method == "POST":
        
        if form.is_valid():
            form.save()
    return render(request, "addworkers.html", {"form": form})