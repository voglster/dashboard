import requests
from settings import config
from tempfile import TemporaryDirectory
from contextlib import contextmanager

assert config.weather_api_key, "No weather api key have you setup your environment?"


@contextmanager
def download_weather_icon(code):
    with TemporaryDirectory() as d:
        yield get_weather_icon(code, d)


def get_current():
    lat, lon = (32.942664, -97.191749)
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.weather_api_key}"
    return requests.get(url).json()


def get_forecast():
    lat, lon = (32.942664, -97.191749)
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={config.weather_api_key}"
    return requests.get(url).json()


def get_weather_icon(code, path="./"):
    import urllib.request

    url = f"http://openweathermap.org/img/wn/{code}@2x.png"
    urllib.request.urlretrieve(url, f"{path}weather_{code}.png")
    return f"{path}weather_{code}.png"


def k_to_f(val):
    return (val - 273.15) * 9 / 5 + 32


def get():
    f = get_current()
    temp = round(k_to_f(f["main"]["temp"]), 1)
    weather_icon_code = f["weather"][0]["icon"]
    return f"{ temp }f", f["weather"][0]["description"], weather_icon_code


if __name__ == "__main__":
    from pprint import pprint

    q = get_current()

    pprint(q)
