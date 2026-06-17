from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


def repairs(request):
    rep = Repair.objects.filter(car__car_type='Sedan')
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('index')
        else:
            # Stay on the page and show errors instead of redirecting
            print(form.errors.as_json())
            messages.error(request, "Please log in!")
    else:
        form = AddForm()

    return render(request, 'repairs.html', {'form': form, 'repairs': rep})
