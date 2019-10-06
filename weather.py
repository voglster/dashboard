from settings import config
from tempfile import TemporaryDirectory
from contextlib import contextmanager
import urllib.request
import pyowm

assert config.weather_api_key, "No weather api key have you setup your environment?"
owm = pyowm.OWM(config.weather_api_key)


@contextmanager
def downloaded_weather_icon(code):
    with TemporaryDirectory() as d:
        yield get_weather_icon(code, d)


def get_weather_icon(code, path="./"):
    url = f"http://openweathermap.org/img/wn/{code}@2x.png"
    urllib.request.urlretrieve(url, f"{path}weather_{code}.png")
    return f"{path}weather_{code}.png"


def get(coords=(32.942664, -97.191749)):
    w = owm.weather_at_coords(*coords).get_weather()
    temp = round(w.get_temperature("fahrenheit")["temp"], 1)
    desc = w.get_detailed_status()
    icon = w.get_weather_icon_name()
    return f"{ temp }f", desc, icon


if __name__ == "__main__":
    from pprint import pprint

    pprint(get())
