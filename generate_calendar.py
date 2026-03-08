from ics import Calendar, Event
import requests
from datetime import datetime, timedelta

API_KEY = "YOUR_FINNHUB_KEY"

start = datetime.utcnow()
end = start + timedelta(days=90)

url = f"https://finnhub.io/api/v1/calendar/economic?token={API_KEY}"

response = requests.get(url)
data = response.json().get("economicCalendar", [])

high_calendar = Calendar()
medium_calendar = Calendar()

groups = {}

for item in data:

    currency = item.get("currency")
    impact = item.get("impact")
    title = item.get("event")
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
        groups[key]["high"].append(title)

    if impact == "Medium":
        groups[key]["medium"].append(title)

for g in groups.values():

    if g["high"]:
        e = Event()
        e.name = "🔴 " + " | ".join(g["high"]) + " (USD)"
        e.begin = g["time"]
        e.duration = timedelta(minutes=30)
        high_calendar.events.add(e)

    if g["medium"]:
        e = Event()
        e.name = "🟠 " + " | ".join(g["medium"]) + " (USD)"
        e.begin = g["time"]
        e.duration = timedelta(minutes=30)
        medium_calendar.events.add(e)

with open("usd_high.ics", "w") as f:
    f.writelines(high_calendar)

with open("usd_medium.ics", "w") as f:
    f.writelines(medium_calendar)
