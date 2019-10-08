import os
import platform


def running_on_rpi():
    if platform.system() != "Linux":
        return False
    return os.uname()[4].startswith("arm")
