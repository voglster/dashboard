from dotenv import load_dotenv

load_dotenv()

from os import getenv
from dotmap import DotMap


config = DotMap()

# your config here
config.weather_api_key = getenv("WEATHER_API_KEY")
config.todoist_api_key = getenv("TODOIST_API_KEY")

if __name__ == "__main__":
    with open(".env", "w") as f:
        for key, value in config.items():
            f.write(f"{str(key).upper()}={value}\n")
