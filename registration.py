import os
import uuid
import util
from pathlib import Path
from settings import registration_url
import requests
import json
import yaml

os.makedirs(".cache", exist_ok=True)
id_file = Path(".cache/id")
status_file = Path(".cache/device_status")


def get_unique_id():
    if id_file.is_file():
        with open(id_file) as f:
            return f.read()
    new_id = str(uuid.uuid4())
    with open(id_file, "w") as f:
        f.write(new_id)
    return new_id


def get_config(width, height):
    response = requests.post(
        registration_url,
        json={"unique_id": get_unique_id(), "width": width, "height": height},
    )

    remote_config = response.json()

    with open(".cache/remote_config.yml", "w") as f:
        f.write(yaml.dump(remote_config))

    return remote_config


if __name__ == "__main__":
    resp = get_config(200, 200)
    print(resp)
