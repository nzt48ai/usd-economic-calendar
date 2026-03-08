from ics import Calendar, Event
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

rss = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

xml = requests.get(rss)
root = ET.fromstring(xml.content)

start = datetime.utcnow()
end = start + timedelta(days=90)

high_calendar = Calendar()
medium_calendar = Calendar()

groups = {}

for event in root.iter("event"):

    try:
        currency = event.find("country").text
        impact = event.find("impact").text
        title = event.find("title").text
        date = event.find("date").text
        time = event.find("time").text
    except:
        continue

    if currency != "USD":
        continue

    if impact not in ["High","Medium"]:
        continue

    if time == "All Day":
        continue

    try:
        dt = datetime.strptime(date + " " + time,"%m-%d-%Y %I:%M%p")
    except:
        continue

    if dt < start or dt > end:
        continue

    key = dt.strftime("%Y%m%dT%H%M")

    if key not in groups:
        groups[key] = {"time":dt,"high":[],"medium":[]}

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

with open("usd_high.ics","w") as f:
    f.writelines(high_calendar)

with open("usd_medium.ics","w") as f:
    f.writelines(medium_calendar)
