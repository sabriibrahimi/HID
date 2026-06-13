from datetime import datetime

from django.contrib import admin
from .models import *
from datetime import date


# Register your models here.
class AgentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'linked_in_profile']

    def has_add_permission(self, request):
        return request.user.is_superuser

class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

    def has_add_permission(self, request):
        return request.user.is_superuser

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'description']

    def has_add_permission(self, request):
        return Agent.objects.filter(user=request.user).exists()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            agent = Agent.objects.filter(user=request.user).first()
            if agent:
                PropertyAgent.objects.create(property=obj,agent=agent)

    def has_delete_permission(self, request, obj = None):
        return obj and not PropertyFeature.objects.filter(property=obj).exists()

    def has_change_permission(self, request, obj = None):
        if obj:
            agent = (PropertyAgent.objects.filter
                     (property=obj).first())
            if agent:
                agent = agent.agent
                return request.user == agent.user
        return False

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Property.objects.filter(date=date.today())
        return Property.objects.all()

admin.site.register(Property, PropertyAdmin)
admin.site.register(Agent, AgentsAdmin)
admin.site.register(Feature, FeatureAdmin)
