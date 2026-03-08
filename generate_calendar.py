import requests
from datetime import datetime, timedelta

start = datetime.utcnow()
end = start + timedelta(days=90)

url = f"https://api.tradingeconomics.com/calendar/country/united states/{start:%Y-%m-%d}/{end:%Y-%m-%d}?c=guest:guest"

events = requests.get(url).json()

lines = []
lines.append("BEGIN:VCALENDAR")
lines.append("VERSION:2.0")
lines.append("PRODID:-//USD Economic Calendar//EN")

for e in events:

    try:
        importance = int(e["Importance"])
    except:
        continue

    if importance < 2:
        continue

    dt = datetime.fromisoformat(e["Date"].replace("Z",""))

    start_time = dt.strftime("%Y%m%dT%H%M%SZ")
    end_time = (dt + timedelta(minutes=30)).strftime("%Y%m%dT%H%M%SZ")

    uid = f"{e['Event']}-{start_time}"

    lines.append("BEGIN:VEVENT")
    lines.append(f"UID:{uid}")
    lines.append(f"DTSTAMP:{start_time}")
    lines.append(f"DTSTART:{start_time}")
    lines.append(f"DTEND:{end_time}")
    lines.append(f"SUMMARY:{e['Event']} (USD)")
    lines.append("END:VEVENT")

lines.append("END:VCALENDAR")

with open("usd_calendar.ics","w") as f:
    f.write("\n".join(lines))
