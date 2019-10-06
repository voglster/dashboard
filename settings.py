from dotenv import load_dotenv

load_dotenv()

from os import getenv
from yaml import load, FullLoader

# your config here
qboard_settings_path = getenv("QBOARD_SETTINGS_PATH", "./settings.yml")
with open(qboard_settings_path) as f:
    config = load(f, Loader=FullLoader)
