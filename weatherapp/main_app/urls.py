from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('weather_forecast/<iso_country_code>/<city_name>/<required_date_search>',
         views.weather_forecast),
    path('task_status/<task_track_id>', views.task_status)
]
