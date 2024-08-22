import threading
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WeatherData
from .serializers import WeatherDataSerializer


class FetchWeatherData(APIView):
    def get(self, request, city_name):
        # Start a new thread to fetch the weather data and save it
        thread = threading.Thread(target=self.fetch_and_save_weather_data, args=(city_name,))
        thread.start()

        # Return an immediate response to the client while the thread processes in the background
        return Response({"message": "Data fetching initiated, check back later to see results."},
                        status=status.HTTP_202_ACCEPTED)

    def fetch_and_save_weather_data(self, city_name):
        """ This method runs in a separate thread to fetch weather data and save it """
        latitude, longitude = self.get_lat_long(city_name)
        if not latitude or not longitude:
            print("Could not fetch latitude/longitude for the city.")
            return

        external_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

        # Fetch data from the external API
        response = requests.get(external_api_url)

        if response.status_code != 200:
            print("Could not fetch data from external API")
            return

        # Parse the JSON response
        data = response.json()

        weather_data = {
            'city': city_name,
            'temperature': data['current_weather']['temperature'],
            'description': data['current_weather']['weathercode']
        }
        # Validate and save the data
        serializer = WeatherDataSerializer(data=weather_data)

        if serializer.is_valid():
            serializer.save()
            print(f"Weather data for {city_name} saved successfully.")
        else:
            print(f"Error in saving data for {city_name}: {serializer.errors}")

    def get_lat_long(self, city_name):
        """ Use OpenStreetMap API to get the latitude and longitude for a city """
        geocode_url = f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json"
        response = requests.get(geocode_url)

        if response.status_code == 200 and len(response.json()) > 0:
            city_data = response.json()[0]
            return city_data['lat'], city_data['lon']
        return None, None
