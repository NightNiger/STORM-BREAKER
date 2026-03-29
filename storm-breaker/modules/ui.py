import os
import time
from modules.config import *

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear_screen()
    # ы
    banner_text = f"""
{C}{BOLD}┌────────────────────────────────────────────────────────┐
│          🚀 {PROJECT_NAME} 🚀          │
│  Author: {PROJECT_AUTHOR} | Studio: {PROJECT_STUDIO}  │
│  TG: {TELEGRAM_LINK}                                   │
│  GH: {GITHUB_LINK}                                   │
└────────────────────────────────────────────────────────┘{RE}"""
    print(banner_text)

def draw_progress_bar(current, total, bar_length=40, title=""):
    if total == 0: percentage = 0
    else: percentage = min(100, (current / total) * 100)
    filled = int((percentage / 100) * bar_length)
    bar = '█' * filled + '░' * (bar_length - filled)
    color = R if percentage < 50 else (Y if percentage < 80 else G)
    print(f"\r{DIM}{title:<25}{RE} {color}[{bar}]{RE} {BOLD}{percentage:.0f}%{RE}", end='', flush=True)

