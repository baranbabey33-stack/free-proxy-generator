import tkinter as tk
from tkinter import ttk
import threading
import requests

proxy_counters = {
    "http": 0,
    "https": 0,
    "socks4": 0,
    "socks5": 0
}

country_codes = {
    "Tümü (Varsayılan)": "",
    "Türkiye": "TR",
    "ABD": "US",
    "Almanya": "DE",
    "Fransa": "FR",
    "Hollanda": "NL",
    "İngiltere": "GB",
    "Rusya": "RU",
    "Japonya": "JP",
    "Kanada": "CA",
    "Avustralya": "AU"
}

def fetch_real_proxies(proxy_type, country_code):
    url = f"https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&proxy_format=ipport&format=text&protocol={proxy_type}"
    if country_code:
        url += f"&country={country_code}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        proxies = response.text.strip().split('\n')
        return [proxy.strip() for proxy in proxies if proxy.strip()]
    except:
        return []

def save_proxies(proxy_type, proxies):
    proxy_counters[proxy_type] += 1
    filename = f"{proxy_type}_proxy_{proxy_counters[proxy_type]}.txt"
    with open(filename, "w") as f:
        for proxy in proxies:
            f.write(proxy + "\n")
    return filename

class ProxyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Generator")
        self.root.geometry("500x430")
        self.root.configure(bg="#0f1117")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#0f1117", foreground="#ffffff", font=("Segoe UI", 11))
        style.configure("TButton", background="#1f6feb", foreground="#ffffff", font=("Segoe UI", 11), padding=6)
        style.map("TButton", background=[("active", "#2e8bff")])
        style.configure("TEntry", padding=5)
        style.configure("TCombobox", padding=5)

        ttk.Label(root, text="Proxy Generator", font=("Segoe UI", 16, "bold")).pack(pady=10)

        ttk.Label(root, text="Proxy Türü:").pack()
        self.proxy_type = ttk.Combobox(root, values=["http", "https", "socks4", "socks5"], state="readonly")
        self.proxy_type.pack()
        self.proxy_type.current(0)

        ttk.Label(root, text="Proxy Sayısı:").pack()
        self.count_entry = ttk.Entry(root)
        self.count_entry.pack()
        self.count_entry.insert(0, "100")

        ttk.Label(root, text="Ülke Seçimi:").pack()
        self.country_combo = ttk.Combobox(root, values=list(country_codes.keys()), state="readonly")
        self.country_combo.pack()
        self.country_combo.set("Tümü (Varsayılan)")

        ttk.Button(root, text="Proxy Oluştur", command=self.start_generation).pack(pady=15)

        self.status_label = ttk.Label(root, text="Durum: Bekleniyor", font=("Segoe UI", 10))
        self.status_label.pack(pady=10)

    def start_generation(self):
        try:
            count = int(self.count_entry.get())
            proxy_type = self.proxy_type.get()
            country_name = self.country_combo.get()
            country_code = country_codes.get(country_name, "")
            self.status_label.config(text=f"{proxy_type} proxy alınıyor...")
            threading.Thread(target=self.generate_proxies, args=(proxy_type, count, country_code), daemon=True).start()
        except:
            self.status_label.config(text="Geçerli sayı girin.")

    def generate_proxies(self, proxy_type, count, country_code):
        proxies = fetch_real_proxies(proxy_type, country_code)
        if proxies:
            selected = proxies[:count]
            filename = save_proxies(proxy_type, selected)
            self.status_label.config(text=f"{len(selected)} proxy kaydedildi → {filename}")
        else:
            self.status_label.config(text="Proxy alınamadı.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyApp(root)
    root.mainloop()
