from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserInputCitySerializer, ForecastsSerializer, CitySerializer
from .models import City, ForecastDate
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
from .tasks import request_weather
from celery.result import AsyncResult
from .celery_app import app
# Create your views here.


@api_view(['GET'])
def weather_forecast(request, iso_country_code, city_name, required_date_search):
    if request.method == 'GET':
        WEATHER_APIKEY = getattr(settings, "WEATHER_APIKEY", None)
        data = {
            'iso_country_code': str(iso_country_code),
            'city_name': str(city_name),
            'required_date_search': str(required_date_search)
        }
        print(data)
        serializer = UserInputCitySerializer(data=data)
        if serializer.is_valid():
            city = City.objects.filter(city_name__iexact=data['city_name'],
                                       iso_country_code__iexact=data['iso_country_code']).first()

            if not city:
                request_task = request_weather.delay(WEATHER_APIKEY,
                                                     data['city_name'],
                                                     data['iso_country_code'],
                                                     data['required_date_search']
                                                     )

                return Response({'message': 'Success',
                                 'db_exists_forecast': False,
                                 'db_exists_city_data': False,
                                 'task_track_id': request_task.id
                                 })
            else:
                forecast = ForecastDate.objects.filter(city__city_name__iexact=data['city_name'],
                                                       city__iso_country_code__iexact=data['iso_country_code'],
                                                       datetime_forecast__date=data['required_date_search']
                                                       )
                if not forecast.exists():

                    request_task = request_weather.delay(WEATHER_APIKEY,
                                                         data['city_name'],
                                                         data['iso_country_code'],
                                                         data['required_date_search']
                                                         )
                    return Response({'message': 'Success',
                                     'db_exists_forecast': False,
                                     'db_exists_city': True,
                                     'task_track_id': request_task.id
                                     })
                else:
                    ser_city_forecast = CitySerializer(city)
                    ser_forecast = ForecastsSerializer(forecast, many=True)

                    return Response({'message': 'Success',
                                     'city': ser_city_forecast.data,
                                     'forecast': ser_forecast.data,
                                     'db_exists_forecast': True,
                                     'db_exists_city': True})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_status(request, task_track_id):
    try:

        task = AsyncResult(task_track_id, app=app)
        if task.state == 'SUCCESS':
            return Response({
                'task_track_id': task.id,
                'task_status': task.state,
                'task_result': task.get()
            })
        else:
            return Response({
                'task_track_id': task.id,
                'task_status': task.state,
                'task_meta': task.meta
            })

    except Exception as ex:
        return Response({
            'message': str(ex)
        })

