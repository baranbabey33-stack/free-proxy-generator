import threading
import requests
import queue
import time

proxy_file = input("Test edilecek proxy dosyası (örnek: http_proxy_1.txt): ").strip()

try:
    with open(proxy_file, "r") as f:
        proxy_list = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("Dosya bulunamadı!")
    exit()

proxy_type = proxy_file.split("_")[0].lower()
q = queue.Queue()
valid_proxies = []
lock = threading.Lock()

def check_proxy():
    while not q.empty():
        proxy = q.get()
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }
        try:
            response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
            if response.status_code == 200:
                with lock:
                    valid_proxies.append(proxy)
                    print(f"[✓] {proxy}")
        except:
            pass
        q.task_done()

for p in proxy_list:
    q.put(p)

thread_list = []
start = time.time()

for _ in range(50):
    t = threading.Thread(target=check_proxy)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()

if valid_proxies:
    with open("working_proxies.txt", "w") as f:
        for proxy in valid_proxies:
            f.write(proxy + "\n")
    print(f"\nToplam geçerli proxy: {len(valid_proxies)} → working_proxies.txt")
else:
    print("\nGeçerli proxy bulunamadı.")

print(f"Süre: {round(time.time() - start, 2)} sn")
