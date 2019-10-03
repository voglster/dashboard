import requests
from settings import config

assert config.weather_api_key, "No weather api key have you setup your environment?"


def get_current():
    lat, lon = (32.942664, -97.191749)
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.weather_api_key}"
    return requests.get(url).json()


def get_forecast():
    lat, lon = (32.942664, -97.191749)
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={config.weather_api_key}"
    return requests.get(url).json()


def get_weather_icon(code):
    import urllib.request

    url = f"http://openweathermap.org/img/wn/{code}@2x.png"
    urllib.request.urlretrieve(url, "weather_ico.png")
    return "./weather_ico.png"


def k_to_f(val):
    return (val - 273.15) * 9 / 5 + 32


def get():
    f = get_current()
    temp = round(k_to_f(f["main"]["temp"]), 1)
    ico_num = f["weather"][0]["icon"]
    get_weather_icon(ico_num)
    return f"{ temp }f", f["weather"][0]["description"]


if __name__ == "__main__":
    from pprint import pprint

    q = get_current()

    pprint(q)

    # print(round(k_to_f(q["main"]["temp"]), 1))
