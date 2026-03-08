from ics import Calendar, Event
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
import os

rss = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
db_file = "events.json"

now = datetime.utcnow()
limit = now + timedelta(days=90)

# load database
if os.path.exists(db_file):
    with open(db_file) as f:
        db = json.load(f)
else:
    db = {}

# fetch weekly calendar
xml = requests.get(rss)
root = ET.fromstring(xml.content)

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

    uid = f"{title}-{dt.isoformat()}"

    db[uid] = {
        "title": title,
        "impact": impact,
        "time": dt.isoformat()
    }

# keep only upcoming 90 days
db = {
    k:v for k,v in db.items()
    if now <= datetime.fromisoformat(v["time"]) <= limit
}

with open(db_file,"w") as f:
    json.dump(db,f)

# group events
groups = {}

for e in db.values():

    dt = datetime.fromisoformat(e["time"])
    key = dt.strftime("%Y%m%dT%H%M")

    if key not in groups:
        groups[key] = {"time":dt,"high":[],"medium":[]}

    if e["impact"] == "High":
        groups[key]["high"].append(e["title"])
    else:
        groups[key]["medium"].append(e["title"])

high_calendar = Calendar()
medium_calendar = Calendar()

for g in groups.values():

    if g["high"]:
        ev = Event()
        ev.name = "🔴 " + " | ".join(sorted(set(g["high"]))) + " (USD)"
        ev.begin = g["time"]
        ev.duration = timedelta(minutes=30)
        high_calendar.events.add(ev)

    if g["medium"]:
        ev = Event()
        ev.name = "🟠 " + " | ".join(sorted(set(g["medium"]))) + " (USD)"
        ev.begin = g["time"]
        ev.duration = timedelta(minutes=30)
        medium_calendar.events.add(ev)

with open("usd_high.ics","w") as f:
    f.writelines(high_calendar)

with open("usd_medium.ics","w") as f:
    f.writelines(medium_calendar)
