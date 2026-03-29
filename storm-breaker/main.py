#!/usr/bin/env python3
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.ui import banner
from modules.core import StormProBreaker

def main():
    try:
        breaker = StormProBreaker()
        breaker.run()
    except KeyboardInterrupt:
        print(f"\n Stopping...")
        sys.exit()

if __name__ == "__main__":
    main()

