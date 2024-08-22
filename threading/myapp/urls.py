from django.urls import path
from .views import FetchWeatherData

urlpatterns = [
    path('fetch-weather/<str:city_name>/', FetchWeatherData.as_view())
]
