import os, requests, time
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
DOMAIN = os.getenv('DOMAIN', 'vega-ex.ru')
INTERVAL = int(os.getenv('MONITOR_INTERVAL', 300))
GEOIP_PATH = "/app/geoip/GeoLite2-Country.mmdb"

# Переменные для слежения за состоянием
LAST_STATUS = "ONLINE" 
LAST_GEOIP_TIME = 0

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except: print("TG Error")

def check_system():
    global LAST_STATUS, LAST_GEOIP_TIME
    current_status = "ONLINE"
    geoip_msg = ""
    
    # 1. Проверка сайта
    try:
        r = requests.get(f"https://{DOMAIN}", timeout=10)
        if r.status_code != 200: current_status = "DOWN"
    except: current_status = "DOWN"

    # 2. Проверка базы GeoIP
    updated = False
    if os.path.exists(GEOIP_PATH):
        current_time = os.path.getmtime(GEOIP_PATH)
        if LAST_GEOIP_TIME == 0: LAST_GEOIP_TIME = current_time # Первый запуск
        if current_time > LAST_GEOIP_TIME:
            updated = True
            LAST_GEOIP_TIME = current_time
            geoip_msg = f"🌍 ✅ *GeoIP Base Updated!*\nDate: {datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M')}"
    else:
        current_status = "GEOIP_ERROR" # Если база пропала, это тоже повод для алерта

    # ЛОГИКА ОПОВЕЩЕНИЙ
    # Отправляем если: статус изменился ИЛИ обновилась база
    if current_status != LAST_STATUS:
        msg = f"🚨 *Status Changed!*\nNew Status: {current_status}\nDomain: {DOMAIN}"
        if current_status == "ONLINE": msg = f"✅ *Back Online!*\nProxy {DOMAIN} is up."
        send_telegram(msg)
        LAST_STATUS = current_status

    if updated:
        send_telegram(geoip_msg)

if __name__ == "__main__":
    send_telegram(f"🚀 *Monitor Started*\nWatching: {DOMAIN}\nAlerts only on changes.")
    while True:
        check_system()
        time.sleep(INTERVAL)
