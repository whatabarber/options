import csv
from datetime import datetime

def log_alerts(alerts):
    with open("alert_history.csv", "a", newline="") as f:
        writer = csv.writer(f)
        for alert in alerts:
            writer.writerow([
                datetime.now(),
                alert["ticker"],
                alert["type"],
                alert["strike"],
                alert["expiration"],
                alert["volume"],
                alert["openInterest"],
                alert["lastPrice"],
                round(alert["impliedVolatility"]*100, 2),
                alert["score"]
            ])