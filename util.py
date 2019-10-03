import os


def running_on_rpi():
    return os.uname()[4].startswith("arm")
