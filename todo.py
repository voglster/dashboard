from dateutil.parser import parse
from datetime import datetime
import todoist
import pytz
from settings import config

tz = pytz.timezone("US/Central")

fields = ["content", "priority", "day_order"]

assert config.todoist_api_key, "No todoist api key have you setup your environment?"


def get_next_tasks(count=3):
    api = todoist.TodoistAPI(config.todoist_api_key)
    api.sync()

    today = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz).date()

    todays_items = [
        x
        for x in api.state["items"]
        if x["due"] and parse(x["due"]["date"]).date() <= today and x["checked"] == 0
    ]

    todays_items = sorted(
        todays_items, key=lambda x: x["day_order"] + (4 - x["priority"] * 1000)
    )[:count]

    todays_items = [{field: x[field] for field in fields} for x in todays_items]
    return todays_items
