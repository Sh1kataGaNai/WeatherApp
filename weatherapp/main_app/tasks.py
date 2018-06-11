from .celery_app import app
import requests
from .models import City, ForecastDate
from .serializers import ForecastsSerializer, CitySerializer
from django.db import IntegrityError


@app.task(bind=True, max_retries=5, time_limit=20)
def request_weather(self, api_key, city_name, iso_country_code, required_date_search):

    try:

        self.track_started = True
        weather_call = requests.get('https://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}&units=metric'
                                    .format(city_name,
                                            iso_country_code,
                                            api_key)).json()

        if weather_call['cod'] == '200':
            city = City.objects.filter(city_id=weather_call['city']['id']).first()
            if not city:
                city = City.objects.create(
                    city_id=weather_call['city']['id'],
                    city_name=weather_call['city']['name'],
                    iso_country_code=weather_call['city']['country'],
                    lat=weather_call['city']['coord']['lat'],
                    lon=weather_call['city']['coord']['lon']
                )
            forecast = ForecastDate.objects.filter(city__city_id=weather_call['city']['id'],
                                                   datetime_forecast__date=required_date_search
                                                   ).first()

            if not forecast:
                for forecast_datetime in weather_call['list']:
                    ForecastDate.objects.create(
                        city=city,
                        datetime_forecast=forecast_datetime['dt_txt'],
                        weather_main=forecast_datetime['weather'][0]['main'],
                        weather_description=forecast_datetime['weather'][0]['description'],
                        weather_icon=forecast_datetime['weather'][0]['icon'],
                        clouds_percent=forecast_datetime['clouds']['all'],
                        wind_speed=forecast_datetime['wind']['speed'],
                        wind_degree=forecast_datetime['wind']['deg'],
                        rain_volume=forecast_datetime['rain']['3h'] if 'rain' in forecast_datetime and '3h'
                                                                       in forecast_datetime['rain'] else 0,
                        temperature=forecast_datetime['main']['temp'],
                        pressure_sea_level=forecast_datetime['main']['sea_level'],
                        pressure_grnd_level=forecast_datetime['main']['grnd_level'],
                        snow_volume=forecast_datetime['snow']['3h'] if 'snow' in forecast_datetime and '3h'
                                                                       in forecast_datetime['snow'] else 0,
                        pressure=forecast_datetime['main']['pressure']
                     )

                required_forecasts = ForecastDate.objects.filter(city=city,
                                                                 datetime_forecast__date=required_date_search
                                                                 )
                ser_city = CitySerializer(city)
                ser_forecast = ForecastsSerializer(required_forecasts, many=True)
                return {
                     'requested_date': required_date_search,
                     'city': ser_city.data,
                     'forecast': ser_forecast.data
                        }

            else:
                required_forecasts = ForecastDate.objects.filter(city=city,
                                                                 datetime_forecast__date=required_date_search
                                                                )
                if required_forecasts.first() is not None:
                    ser_city = CitySerializer(city)
                    ser_forecast = ForecastsSerializer(required_forecasts, many=True)
                    return {
                        'requested_date': required_date_search,
                        'city': ser_city.data,
                        'forecast': ser_forecast.data
                    }

        elif weather_call['cod'] == '404':
            return weather_call['message']

        else:
            self.retry(countdown=2 ** self.request.retries)

    except requests.exceptions.RequestException as ex:
        self.update_state(
            state='RETRY',
            meta={
                'detailed': 'OpenWeatherMap API not respond'
            }
        )
        self.retry(countdown=2 ** self.request.retries, exc=ex)

    except IntegrityError as ex:
        self.update_state(
            state='FAILED',
            meta={
                'detailed': 'Server side error, please contact admin cite.'
            }
        )

    except Exception as ex:
        self.update_state(
            state='FAILED',
            meta={
                'detailed': 'Unknown exception'
            }
        )




