from ics import Calendar, Event
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

rss = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

response = requests.get(rss)

root = ET.fromstring(response.content)

calendar = Calendar()

now = datetime.utcnow()
limit = now + timedelta(days=90)

for event in root.iter("event"):

    country = event.find("country").text
    impact = event.find("impact").text

    if country != "USD":
        continue

    if impact not in ["Medium", "High"]:
        continue

    date = event.find("date").text
    time = event.find("time").text

    if time == "All Day":
        continue

    try:
        dt = datetime.strptime(date + " " + time, "%m-%d-%Y %I:%M%p")
    except:
        continue

    if dt < now or dt > limit:
        continue

    title = event.find("title").text

    if impact == "High":
        title = "🔴 " + title
    elif impact == "Medium":
        title = "🟠 " + title

    e = Event()
    e.name = title + " (USD)"
    e.begin = dt
    e.duration = timedelta(minutes=30)

    calendar.events.add(e)

with open("usd_calendar.ics","w") as f:
    f.writelines(calendar)
