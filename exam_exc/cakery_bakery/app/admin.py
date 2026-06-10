from django.contrib import admin
from django.db.models import Count

from .models import *


# Register your models here.
class BakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname']

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj = None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj = None):
        return request.user.is_superuser

    #Bakeries with less than 5 cakes
    # are shown to superuser in the Admin panel.
    def get_queryset(self, request):
        qs = super(BakerAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs.annotate(cakes_count=Count('cakes')).filter(cakes_count__lt=5)
        return qs

class CakeAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True

        return obj and request.user == obj.baker.user

    #A baker can have a maximum of 10 cakes at a given time.
    def save_model(self, request, obj, form, change):
        baker = Baker.objects.filter(user=request.user).first()

        if not change:
            obj.baker = baker

        cakes = Cake.objects.filter(baker=baker)

        if not change and cakes.count() >= 10:
            return

        #The total price of the cakes of one baker must not exceed 10,000.
        total_price = 0

        for cake in cakes:
            total_price += cake.price

        if not change and total_price + obj.price > 10000:
            return

        if change:
            old_cake = Cake.objects.get(id=obj.id)

            if total_price + obj.price - old_cake.price > 10000:
                return

        if Cake.objects.exclude(pk=obj.pk).filter(name=obj.name).exists():
            return

        super(CakeAdmin, self).save_model(request, obj, form, change)

admin.site.register(Cake, CakeAdmin)
admin.site.register(Baker, BakerAdmin)



