from django.shortcuts import render, redirect
from .forms import *
from .models import *
# Create your views here.

def index(request):
    cakes = Cake.objects.all()

    return render(request,'index.html', {'cakes': cakes})

def add(request):

    if request.method=='POST':
        form = CakeForm(request.POST, request.FILES)

        if request.user.is_authenticated and form.is_valid():
            cake = form.save(commit=False)
            cake.baker = Baker.objects.filter(user=request.user).first()
            cake.save()

        return redirect('index')

    form = CakeForm()

    return render(request, 'add.html', {'form': form})