from rest_framework import serializers
from .models import WeatherData


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['city', 'temperature', 'description']

    def validate_temperature(self, value):
        if value < -100 or value > 100:
            raise serializers.ValidationError("Invalid temperature value.")
        return value
