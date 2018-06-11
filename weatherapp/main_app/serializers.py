from rest_framework import serializers
from .models import City, ForecastDate
import datetime


class UserInputCitySerializer(serializers.Serializer):
    city_name = serializers.CharField(max_length=200, default='')
    iso_country_code = serializers.CharField(max_length=2, default='')
    required_date_search = serializers.DateField()

    def validate_required_date_search(self, value):
        required = value
        today = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
        after_five = today + datetime.timedelta(days=4)
        if after_five.date() < required or today.date() > required:
            raise serializers.ValidationError('Forecast available only for 5 days since today')
        return value


class ForecastsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForecastDate
        exclude = ('city', )


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'



