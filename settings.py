from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

from os import getenv
from yaml import load, FullLoader

qboard_settings_path = Path(getenv("QBOARD_SETTINGS_PATH", "./settings.yml"))

registration_url = getenv("REGISTRATION_URL", r"https://qapi.cld.vogelcc.com/")

if not qboard_settings_path.is_file():
    config = {
        "qboard": {"load_remote": True},
        "modules": [
            {"name": "color_bg", "id": "bg1"},
            {
                "name": "static_text",
                "id": "unreg",
                "color": "dark_grey",
                "font_size": "extra_small",
                "text": "Not connected",
                "position": {
                    "anchor_point": "midtop",
                    "anchor_to": {"id": "screen", "point": "midtop"},
                },
            },
            {
                "name": "static_text",
                "id": "unreg2",
                "font_size": "extra_small",
                "color": "dark_grey",
                "text": "Not connected",
                "position": {
                    "anchor_point": "midbottom",
                    "anchor_to": {"id": "screen", "point": "midbottom"},
                },
            },
            {
                "name": "static_text",
                "id": "default_config",
                "color": "red",
                "font_size": "extra_small",
                "text": "error: default config, cannot connect to server or missing settings.yml",
                "position": {
                    "anchor_point": "center",
                    "anchor_to": {"id": "screen", "point": "center"},
                },
            },
        ],
    }
else:
    with open(qboard_settings_path) as f:
        config = load(f, Loader=FullLoader)
