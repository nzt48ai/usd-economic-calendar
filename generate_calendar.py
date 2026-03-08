from ics import Calendar, Event
import requests
from datetime import datetime, timedelta

API_KEY = "d6mq2dpr01qir35i1fu0d6mq2dpr01qir35i1fug"

start = datetime.utcnow()
end = start + timedelta(days=90)

url = f"https://finnhub.io/api/v1/calendar/economic?token={API_KEY}"

response = requests.get(url, timeout=30)
data = response.json().get("economicCalendar", [])

calendar = Calendar()

groups = {}

for item in data:

    currency = item.get("currency")
    impact = item.get("impact")
    event_name = item.get("event")
    timestamp = item.get("time")

    if currency != "USD":
        continue

    if impact not in ["High", "Medium"]:
        continue

    try:
        dt = datetime.fromtimestamp(timestamp)
    except:
        continue

    if dt < start or dt > end:
        continue

    key = dt.strftime("%Y%m%dT%H%M")

    if key not in groups:
        groups[key] = {"time": dt, "high": [], "medium": []}

    if impact == "High":
        groups[key]["high"].append(event_name)
    else:
        groups[key]["medium"].append(event_name)

for g in groups.values():

    parts = []

    if g["high"]:
        parts.append("🔴 " + " | ".join(g["high"]))

    if g["medium"]:
        parts.append("🟠 " + " | ".join(g["medium"]))

    title = " | ".join(parts)

    e = Event()
    e.name = title + " (USD)"
    e.begin = g["time"]
    e.duration = timedelta(minutes=30)

    calendar.events.add(e)

with open("usd_calendar.ics", "w") as f:
    f.writelines(calendar)
