import requests
from datetime import datetime, timedelta

start = datetime.utcnow()
end = start + timedelta(days=90)

url = f"https://api.tradingeconomics.com/calendar/country/united states/{start:%Y-%m-%d}/{end:%Y-%m-%d}?c=guest:guest"

events = requests.get(url).json()

lines = []
lines.append("BEGIN:VCALENDAR")
lines.append("VERSION:2.0")

for e in events:

    importance = int(e["Importance"])

    if importance < 2:
        continue

    date = e["Date"].replace("-", "").replace(":", "").replace("T","").split(".")[0]

    lines.append("BEGIN:VEVENT")
    lines.append(f"SUMMARY:{e['Event']} (USD)")
    lines.append(f"DTSTART:{date}")
    lines.append("END:VEVENT")

lines.append("END:VCALENDAR")

with open("usd_calendar.ics","w") as f:
    f.write("\n".join(lines))
