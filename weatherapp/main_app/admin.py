from django.contrib import admin
from .models import *
# Register your models here.


class ForecastInline(admin.TabularInline):
    model = ForecastDate


class CityAdmin(admin.ModelAdmin):
    inlines = [
        ForecastInline
    ]


admin.site.register(City, CityAdmin)
admin.site.register(ForecastDate)
