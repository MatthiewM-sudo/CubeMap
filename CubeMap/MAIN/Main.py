import sys
import ctypes

if len(sys.argv) < 2:
    print("[!] Usage: python3 CubeMap.py <args> <ip>")
    sys.exit(1)

target_ip = sys.argv[-1]
options = []

for arg in sys.argv[1:-1]:
    options.append(arg)

if "-sS" in options:
    print("+" + "-"*45 + "+")
    print("|    ======  CubeMap Network Scanner  ======  |")
    print("|                Version 0.2.0                |")
    print("+---------------------------------------------+")
    print(f"\n[+] Launching scan on target: {target_ip}")
    print("[+] Scanning ports 1 to 1000...\n")
    print("PORT     STATE    SERVICE")

    try:
        scanner_engine = ctypes.CDLL('../FUN/SCANNER/libscanner.so')
    except OSError:
        print("[!] Error: Could not load 'libscanner.so'. Make sure it is compiled.")
        sys.exit(1)

    scanner_engine.scan_port_cpp.argtypes = [ctypes.c_char_p, ctypes.c_int]
    scanner_engine.scan_port_cpp.restype = ctypes.c_int

    ip_bytes = target_ip.encode('utf-8')
    open_ports_count = 0

    for port in range(1, 1001):
        is_open = scanner_engine.scan_port_cpp(ip_bytes, port)
        if is_open == 1:
            open_ports_count += 1
            service_name = "unknown"
            if port == 22: service_name = "ssh"
            elif port == 80: service_name = "http"
            elif port == 443: service_name = "https"
            
            print(f"{port}/tcp   open     {service_name}")

    print(f"\nCubeMap done: Scan finished. Found {open_ports_count} open ports.")
else:
    print(f"[-] Error: Missing or unknown scan flag (e.g. -sS).")
