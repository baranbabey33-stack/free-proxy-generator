import tkinter as tk
from tkinter import ttk
import threading
import random
import time
import os

def generate_proxies(proxy_type, amount):
    proxies = []
    for _ in range(amount):
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        port = random.randint(1000, 9999)
        proxies.append(f"{proxy_type}://{ip}:{port}")
    return proxies

def save_proxies_to_file(proxies, filename="proxies.txt"):
    with open(filename, "w") as f:
        for proxy in proxies:
            f.write(proxy + "\n")

class ProxyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Generator")
        self.root.geometry("500x450")

        self.language_options = {"Türkçe": self.set_tr, "English": self.set_en}
        self.current_lang = "tr"

        self.amount_label = ttk.Label(root, text="Proxy Sayısı:")
        self.amount_label.pack(pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.pack(pady=5)
        self.amount_entry.insert(0, "1000")

        self.proxy_type_label = ttk.Label(root, text="Proxy Türü:")
        self.proxy_type_label.pack(pady=5)
        self.proxy_type = ttk.Combobox(root, values=["http", "https", "socks4", "socks5"], state="readonly")
        self.proxy_type.pack(pady=5)
        self.proxy_type.current(0)

        self.timeout_label = ttk.Label(root, text="Zaman Aşımı (sn):")
        self.timeout_label.pack(pady=5)
        self.timeout_entry = ttk.Entry(root)
        self.timeout_entry.pack(pady=5)
        self.timeout_entry.insert(0, "5")

        self.filename_label = ttk.Label(root, text="Dosya Adı:")
        self.filename_label.pack(pady=5)
        self.filename_entry = ttk.Entry(root)
        self.filename_entry.insert(0, "proxies.txt")
        self.filename_entry.pack(pady=5)

        self.generate_button = ttk.Button(root, text="Proxy Başlat", command=self.start_generation)
        self.generate_button.pack(pady=15)

        self.lang_label = ttk.Label(root, text="Dil Seçimi:")
        self.lang_label.pack(pady=5)
        self.lang_menu = ttk.Combobox(root, values=list(self.language_options.keys()), state="readonly")
        self.lang_menu.pack(pady=5)
        self.lang_menu.set("Türkçe")
        self.lang_menu.bind("<<ComboboxSelected>>", self.change_language)

        self.status_label = ttk.Label(root, text="Durum: Bekleniyor", wraplength=400)
        self.status_label.pack(pady=10)

    def set_tr(self):
        self.amount_label.config(text="Proxy Sayısı:")
        self.proxy_type_label.config(text="Proxy Türü:")
        self.timeout_label.config(text="Zaman Aşımı (sn):")
        self.filename_label.config(text="Dosya Adı:")
        self.generate_button.config(text="Proxy Başlat")
        self.lang_label.config(text="Dil Seçimi:")
        self.status_label.config(text="Durum: Bekleniyor")

    def set_en(self):
        self.amount_label.config(text="Proxy Count:")
        self.proxy_type_label.config(text="Proxy Type:")
        self.timeout_label.config(text="Timeout (sec):")
        self.filename_label.config(text="File Name:")
        self.generate_button.config(text="Start Proxy")
        self.lang_label.config(text="Language:")
        self.status_label.config(text="Status: Waiting")

    def change_language(self, event):
        lang = self.lang_menu.get()
        if lang in self.language_options:
            self.language_options[lang]()

    def start_generation(self):
        try:
            amount = int(self.amount_entry.get())
            timeout = int(self.timeout_entry.get())
            proxy_type = self.proxy_type.get()
            filename = self.filename_entry.get()
            self.status_label.config(text=f"Durum: {amount} proxy oluşturuluyor...")
            threading.Thread(target=self.run_generation, args=(proxy_type, amount, filename), daemon=True).start()
        except ValueError:
            self.status_label.config(text="Hata: Geçerli sayı girin!")

    def run_generation(self, proxy_type, amount, filename):
        proxies = generate_proxies(proxy_type, amount)
        save_proxies_to_file(proxies, filename)
        self.status_label.config(text=f"{len(proxies)} proxy oluşturuldu ve '{filename}' dosyasına kaydedildi.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyApp(root)
    root.mainloop()
