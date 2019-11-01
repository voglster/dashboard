from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

from os import getenv
from yaml import load, FullLoader

from config_generation import offline_and_missing_config

qboard_settings_path = Path(getenv("QBOARD_SETTINGS_PATH", "./settings.yml"))

registration_url = getenv("REGISTRATION_URL", r"https://qapi.cld.vogelcc.com/")

if not qboard_settings_path.is_file():
    config = offline_and_missing_config
else:
    with open(qboard_settings_path) as f:
        config = load(f, Loader=FullLoader)
