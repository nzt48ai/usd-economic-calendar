import requests
from datetime import datetime, timedelta

url = "https://api.tradingeconomics.com/calendar/country/united%20states"

data = requests.get(url).json()

now = datetime.utcnow()
limit = now + timedelta(days=90)

lines = []
lines.append("BEGIN:VCALENDAR")
lines.append("VERSION:2.0")
lines.append("PRODID:-//USD Economic Calendar//EN")

for e in data:

    try:
        importance = int(e["Importance"])
    except:
        continue

    if importance < 2:
        continue

    date_string = e.get("Date")

    if not date_string:
        continue

    dt = datetime.fromisoformat(date_string.replace("Z",""))

    if dt > limit:
        continue

    start = dt.strftime("%Y%m%dT%H%M%SZ")
    end = (dt + timedelta(minutes=30)).strftime("%Y%m%dT%H%M%SZ")

    uid = f"{e['Event']}-{start}"

    lines.append("BEGIN:VEVENT")
    lines.append(f"UID:{uid}")
    lines.append(f"DTSTAMP:{start}")
    lines.append(f"DTSTART:{start}")
    lines.append(f"DTEND:{end}")
    lines.append(f"SUMMARY:{e['Event']} (USD)")
    lines.append("END:VEVENT")

lines.append("END:VCALENDAR")

with open("usd_calendar.ics","w") as f:
    f.write("\n".join(lines))
