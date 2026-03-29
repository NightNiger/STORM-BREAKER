#!/usr/bin/env python
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.config import *
from modules.ui import banner
from modules.core import StormProBreaker

def main():
    # Создаем объект класса из core.py
    breaker = StormProBreaker()
    # Запускаем твой основной цикл
    breaker.run() 

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Stopping...{RE}")
        sys.exit()

