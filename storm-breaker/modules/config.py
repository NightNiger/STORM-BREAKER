import os

# Цвета
G, R, C, Y, B, W, M, BG_R, RE = (
    '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[94m', '\033[97m', '\033[95m',
    '\033[41m', '\033[0m'
)
BOLD, DIM = '\033[1m', '\033[2m'

# Порты
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
    'python-httpx/0.25.0'
]

WAF_PATHS = ['/', '/api/', '/admin/', '/login']

PROFILES = {
    '1': {'name': 'Light', 'concurrent': 10, 'timeout': 10},
    '2': {'name': 'Medium', 'concurrent': 50, 'timeout': 5},
    '3': {'name': 'Heavy', 'concurrent': 200, 'timeout': 3},
    '4': {'name': 'Extreme', 'concurrent': 500, 'timeout': 2},
    '5': {'name': 'Nuclear', 'concurrent': 2000, 'timeout': 1}
}

PROJECT_NAME = "STORM-BREAKER PRO v5.0 ULTRA"
PROJECT_AUTHOR = "@Rrupv"
PROJECT_STUDIO = "NightNiger"
TELEGRAM_LINK = "https://t.me/Rrupv"
GITHUB_LINK = "https://github.com/NightNiger/STORM-BREAKER"

