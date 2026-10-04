import socket
import sys
import threading
import time

BANNER = r"""
==================================================
        ___            _     ____                                      
       / _ \___  _____| |_  / ___|  ___ __ _ _ __  _ __   ___ _ __ 
      / /_)/ _ \/ ___/| __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
     / ___/ (_) | |   | |_   ___) | (_| (_| | | | | | | |  __/ |   
     \/    \___/|_|    \__| |____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                                   
==================================================
"""

print(BANNER)

try:
    target_input = input("Enter Target Host/IP : ").strip()
    start_port = int(input("Enter Start Port    : ").strip())
    end_port = int(input("Enter End Port      : ").strip())
except ValueError:
    print("\n[-] Invalid port number! Please enter integers only.")
    sys.exit()

try:
    target = socket.gethostbyname(target_input)
except socket.gaierror:
    print("\n[-] Name resolution error")
    sys.exit()

print("\n" + "-" * 50)
print(f" Target Host : {target_input} ({target})")
print(f" Port Range  : {start_port} to {end_port}")
print("-" * 50 + "\n")


def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    con = s.connect_ex((target, port))
    if not con:
        print(f"[+] Port {port:<5} is open")
    s.close()


threads = []
for port in range(start_port, end_port + 1):
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("\n" + "-" * 50)
print("Scan complete.")
print("-" * 50)