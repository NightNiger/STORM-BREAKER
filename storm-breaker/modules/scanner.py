import socket

def run_scan(target):
    print(f"\n[!] СКАНИРОВАНИЕ ЦЕЛИ: {target}")
    # Самые интересные порты
    ports = [21, 22, 80, 443, 8080, 3306]
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"  [+] ПОРТ {port} ОТКРЫТ")
        sock.close()
    print("[*] Проверка завершена.\n")

