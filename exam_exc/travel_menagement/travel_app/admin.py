from xml.dom import ValidationErr

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Count

from .models import Trip, TourGuid


# Register your models here.


# Tour guides can be added, edited, and deleted only by superusers.
class TourGuideAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # In the Django Admin panel, superusers should only see tour guides who have fewer than 3 destinations assigned to them.
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs.annotate(total_destinations=Count('guide_tour')).filter(total_destinations__lt=3)

        return qs


class TripAdmin(admin.ModelAdmin):

    # Destinations can only be edited by the tour guide responsible
    # for that destination.
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.guide.user == request.user

    # Other tour guides may only view those destinations.
    def has_view_permission(self, request, obj=None):
        return True

    # A tour guide can manage a maximum of 5 destinations at any given time.
    def save_model(self, request, obj, form, change):
        guide = obj.guide

        count = Trip.objects.filter(guide=guide).count()

        if change:
            count -= 1

        if count >= 5:
            raise ValidationError("A tour guide cannot have more than 5 destinations.")

        # The total price of all destinations assigned
        # to a single tour guide must not exceed 50,000.
        total_price = 0

        for trip in Trip.objects.filter(guide=guide):
            total_price += trip.price

        if change:
            total_price -= obj.price

        if total_price + obj.price > 50000:
            raise ValidationError("The total price of all destinations cannot exceed 50000.")

        # A tour guide cannot add a destination if another
        # destination with the same name already exists.
        if Trip.objects.filter(place=obj.place).exists():
            raise ValidationError("A destination with this name already exists")

        super().save_model(request, obj, form, change)

        # Destinations can only be edited by the tour guide responsible
        # for that destination.
        # Other tour guides may only view those destinations.

admin.site.register(Trip, TripAdmin)
admin.site.register(TourGuid, TourGuideAdmin)