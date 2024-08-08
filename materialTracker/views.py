from django.shortcuts import render
from .forms import WorkerForm
from .models import Worker

# Create your views here.

def workers(request):
    workers = Worker.objects.all()
    return render(request, "workers.html", {"workers": workers})