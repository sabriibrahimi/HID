from django.contrib import admin
from .models import Category, Manufacturer, Supplement

admin.site.register(Category)
admin.site.register(Manufacturer)

@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    exclude = ("created",)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created = request.user
        super().save_model(request, obj, form, change)
