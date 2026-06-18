from django.shortcuts import render, redirect

from .forms import AddForm
from .models import Trip, TourGuid


# Create your views here.

def index(request):
    trips = Trip.objects.all()

    return render(request, 'index.html', {'trips': trips})


def add(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)

        if form.is_valid():
            trip = form.save(commit=False)
            trip.guide = TourGuid.objects.get(user=request.user)
            trip.save()

            return redirect('index')

    else:
        form = AddForm()

    return render(request, 'add.html', {'form': form})
