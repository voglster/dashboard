from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

from os import getenv
from yaml import load, FullLoader

# your config here
qboard_settings_path = Path(getenv("QBOARD_SETTINGS_PATH", "./settings.yml"))

if not qboard_settings_path.is_file():
    config = {}
else:
    with open(qboard_settings_path) as f:
        config = load(f, Loader=FullLoader)
