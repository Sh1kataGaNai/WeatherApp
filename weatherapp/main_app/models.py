from django.db import models


class City(models.Model):
    city_id = models.IntegerField(unique=True)
    city_name = models.CharField(max_length=200, default='')
    iso_country_code = models.CharField(max_length=2, default='')
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return '{}:{}:{}'.format(self.city_name, self.iso_country_code, self.city_id)

    class Meta:
        verbose_name_plural = 'cities'


class ForecastDate(models.Model):
    # city section
    city = models.ForeignKey(City, related_name='forecasts', on_delete=models.CASCADE, null=True)
    # datetime forecast section
    datetime_forecast = models.DateTimeField()
    # weather section
    weather_main = models.CharField(max_length=50, default='')
    weather_description = models.CharField(max_length=50, default='')
    weather_icon = models.CharField(max_length=5, default='')
    # snow section
    snow_volume = models.FloatField(blank=True, default=0.0)
    # clouds section
    clouds_percent = models.IntegerField(default=0)
    # rain section
    rain_volume = models.FloatField(blank=True, default=0.0)
    # wind section
    wind_speed = models.FloatField(default=0.0)
    wind_degree = models.FloatField(default=0.0)
    # other section
    temperature = models.FloatField(default=0.0)
    pressure = models.FloatField(default=0.0)
    pressure_sea_level = models.FloatField(default=0.0)
    pressure_grnd_level = models.FloatField(default=0.0)

    class Meta:
        ordering = ['datetime_forecast']

    def __str__(self):
        return '{}:{}:{}'.format(self.datetime_forecast, self.weather_main, self.weather_description)
