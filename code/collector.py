from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import time
import os

ow_api_key = os.environ['OW_API_KEY']
ow_location = os.environ['OW_LOCATION']

url = "http://api.openweathermap.org/data/2.5/weather?q=" + ow_location + "&APPID=" + ow_api_key

class JsonCollector(object):
  def collect(self):
    # Fetch the JSON
    response = json.loads(requests.get(url).content.decode('UTF-8'))

    # Grab labels
    station_id = str(response['sys']['id'])
    country = response['sys']['country']
    name = response['name']

    # Visibility
    metric = Metric('openweathermap_visibility', 'Visibility', 'gauge')
    metric.add_sample('openweathermap_visibility',
                      value=response['visibility'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

    # Sunrise and Sunset
    metric = Metric('openweathermap_sunrise', 'Sunrise', 'counter')
    metric.add_sample('openweathermap_sunrise',
                      value=response['sys']['sunrise'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric
    metric = Metric('openweathermap_sunset', 'Sunset', 'counter')
    metric.add_sample('openweathermap_sunset',
                      value=response['sys']['sunset'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

    # Temp
    #metric = Metric('openweathermap_main', 'Main', 'gauge')
    #for k, v in response['main'].items():
    #  metric.add_sample('openweathermap_main', value=v, labels={'feature': k})
    #yield metric

    # Temp
    metric = Metric('openweathermap_temp', 'Temperature', 'gauge')
    metric.add_sample('openweathermap_temp',
                      value=response['main']['temp'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

    # Pressure
    metric = Metric('openweathermap_pressure', 'Pressure', 'gauge')
    metric.add_sample('openweathermap_pressure',
                      value=response['main']['pressure'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

    # Humidity
    metric = Metric('openweathermap_humidity', 'Humidity', 'gauge')
    metric.add_sample('openweathermap_humidity',
                      value=response['main']['humidity'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

    # Clouds
    metric = Metric('openweathermap_clouds_all', 'Cloud Cover', 'gauge')
    metric.add_sample('openweathermap_clouds_all',
                      value=response['clouds']['all'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

    # Wind
    metric = Metric('openweathermap_wind_speed', 'Wind Speed', 'gauge')
    metric.add_sample('openweathermap_wind_speed',
                      value=response['wind']['speed'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

    metric = Metric('openweathermap_wind_deg', 'Wind Direction', 'gauge' )
    metric.add_sample('openweathermap_wind_deg',
                      value=response['wind']['deg'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

    metric = Metric('openweathermap_wind_gust', 'Wind Gust', 'gauge' )
    metric.add_sample('openweathermap_wind_gust',
                      value=response['wind']['gust'],
                      labels={'name': name, 'country': country, 'station_id': station_id})
    yield metric

if __name__ == '__main__':
  start_http_server(8000)
  REGISTRY.register(JsonCollector())
  while True:
      time.sleep(1)