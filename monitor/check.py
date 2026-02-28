import os
import requests
import time
from datetime import datetime

# Берем настройки из .env (теперь они точно подгрузятся)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
DOMAIN = os.getenv('DOMAIN', 'vega-ex.ru')
INTERVAL = int(os.getenv('MONITOR_INTERVAL', 300))
GEOIP_PATH = "/app/geoip/GeoLite2-Country.mmdb"

def send_telegram(message):
    if not TOKEN or not CHAT_ID:
        print("Telegram settings missing")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error sending TG: {e}")

def get_geoip_status():
    if os.path.exists(GEOIP_PATH):
        mtime = os.path.getmtime(GEOIP_PATH)
        dt = datetime.fromtimestamp(mtime)
        return f"✅ Base updated: {dt.strftime('%Y-%m-%d %H:%M')}"
    return "❌ GeoIP Base NOT FOUND"

def check_system():
    status_msg = f"🔍 *System Health Report ({datetime.now().strftime('%H:%M')})*\n\n"
    
    # Проверка доступности твоего нового домена
    try:
        # Проверяем именно vega-ex.ru
        r = requests.get(f"https://{DOMAIN}", timeout=10)
        if r.status_code == 200:
            status_msg += f"🌐 Proxy {DOMAIN}: *ONLINE* ✅\n"
        else:
            status_msg += f"🌐 Proxy {DOMAIN}: *STATUS {r.status_code}* ⚠️\n"
    except Exception as e:
        status_msg += f"🌐 Proxy {DOMAIN}: *DOWN* 🚨\n_{str(e)[:50]}_"

    # Проверка GeoIP
    status_msg += f"🌍 {get_geoip_status()}\n"
    
    send_telegram(status_msg)
    print(f"Check completed at {datetime.now()}. Alert sent: {bool(TOKEN)}")

if __name__ == "__main__":
    print(f"Monitor started for {DOMAIN}...")
    check_system() # Первый запуск сразу
    while True:
        time.sleep(INTERVAL)
        check_system()
