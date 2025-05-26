from datetime import datetime
from typing import Any
import ntplib

def get_synced_date() -> str:
    try:
        ntp_client: Any = ntplib.NTPClient() # type: ignore
        ntp_response: Any = ntp_client.request(host="pool.ntp.org", version=3) # type: ignore
        return str(datetime.fromtimestamp(ntp_response.tx_time).date()) # type: ignore
    except Exception as e:
        print("Error obtaining NTP data:", e)
        return datetime.now().strftime("%Y-%m-%d")

