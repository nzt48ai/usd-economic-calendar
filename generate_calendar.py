import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

rss_url = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

response = requests.get(rss_url)

root = ET.fromstring(response.content)

now = datetime.utcnow()
limit = now + timedelta(days=90)

lines = []
lines.append("BEGIN:VCALENDAR")
lines.append("VERSION:2.0")
lines.append("PRODID:-//USD Economic Calendar//EN")

for item in root.iter("event"):

    country = item.find("country").text
    impact = item.find("impact").text

    if country != "USD":
        continue

    if impact not in ["Medium", "High"]:
        continue

    date = item.find("date").text
    time = item.find("time").text

    if time == "All Day":
        continue

    try:
        dt = datetime.strptime(date + " " + time, "%m-%d-%Y %I:%M%p")
    except:
        continue

    if dt < now or dt > limit:
        continue

    start = dt.strftime("%Y%m%dT%H%M%SZ")
    end = (dt + timedelta(minutes=30)).strftime("%Y%m%dT%H%M%SZ")

    title = item.find("title").text

    lines.append("BEGIN:VEVENT")
    lines.append(f"UID:{title}-{start}")
    lines.append(f"DTSTAMP:{start}")
    lines.append(f"DTSTART:{start}")
    lines.append(f"DTEND:{end}")
    lines.append(f"SUMMARY:{title} (USD)")
    lines.append("END:VEVENT")

lines.append("END:VCALENDAR")

with open("usd_calendar.ics","w") as f:
    f.write("\n".join(lines))
