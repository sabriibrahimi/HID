from django.shortcuts import render, redirect
from .models import *
from .forms import *


# Create your views here.


def index(request):
    properties = Property.objects.filter(sold=False,area__gt=100)

    prop_list = []

    for p in properties:
        features = PropertyFeature.objects.filter(property=p)

        price = 0

        for f in features:
            price += f.feature.value

        prop_list.append({
            'id': p.id,
            'name': p.name,
            'url': p.image.url if p.image else None,
            'area': p.area,
            'price': price,
        })

    return render(  request,'index.html',{'properties': prop_list}
    )

def edit(request, id):
    instance = Property.objects.filter(id=id).first()
    if request.method == 'POST':
        form = EditForm(request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('index')
    form = EditForm(instance=instance)

    return render(request, 'edit.html',{'form': form, 'property': instance})