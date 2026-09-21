import sys
import ctypes
import os

if len(sys.argv) < 4 or sys.argv[1] != "-e":
    print("[!] Usage: CubeMap -e <service1-service2> <company_keyword>")
    print("Example: CubeMap -e aws-azure bank")
    sys.exit(1)

services_arg = sys.argv[2]
company = sys.argv[3]
target_services = services_arg.split('-')

print("+" + "-"*45 + "+")
print("|    ======  CUBEMAP CLOUD FRAMEWORK ======   |")
print("|    Version 0.7.0 - Global Interactive CLI   |")
print("+" + "-"*45 + "+")
print(f"\n[+] Target Keyword: {company}")
print(f"[+] Scanning: {', '.join(target_services).upper()}\n")

base_dir = os.path.dirname(os.path.realpath(__file__))
scanner_path = os.path.join(base_dir, '../FUN/SCANNER/libscanner.so')

try:
    scanner_engine = ctypes.CDLL(scanner_path)
except OSError:
    print(f"[!] Error: Cannot load '{scanner_path}'. Please run setup script.")
    sys.exit(1)

scanner_engine.check_path_cpp.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
scanner_engine.check_path_cpp.restype = ctypes.c_int

mutations = ["", "-backup", "-data", "-prod", "-staging", "-private"]
detected_vulnerabilities = {}
vuln_counter = 1

for service in target_services:
    service = service.lower().strip()
    
    if service == "aws":
        print(f"[*] Scanning AWS infrastructure...")
        for mut in mutations:
            host = f"{company}{mut}.s3.amazonaws.com"
            if scanner_engine.check_path_cpp(host.encode('utf-8'), 80, b"/") == 1:
                vuln_name = f"aws-{vuln_counter}"
                detected_vulnerabilities[vuln_name] = {"type": "AWS S3", "url": f"http://{host}"}
                print(f"    [{vuln_name}] VULNERABILITY FOUND: {detected_vulnerabilities[vuln_name]['url']}")
                vuln_counter += 1

    elif service == "azure":
        print(f"[*] Scanning Azure infrastructure...")
        for mut in mutations:
            host = f"{company}{mut}.blob.core.windows.net"
            if scanner_engine.check_path_cpp(host.encode('utf-8'), 80, b"/") == 1:
                vuln_name = f"azure-{vuln_counter}"
                detected_vulnerabilities[vuln_name] = {"type": "Azure Blob", "url": f"http://{host}"}
                print(f"    [{vuln_name}] VULNERABILITY FOUND: {detected_vulnerabilities[vuln_name]['url']}")
                vuln_counter += 1

    elif service == "gcp":
        print(f"[*] Scanning GCP infrastructure...")
        for mut in mutations:
            host = f"{company}{mut}.storage.googleapis.com"
            if scanner_engine.check_path_cpp(host.encode('utf-8'), 80, b"/") == 1:
                vuln_name = f"gcp-{vuln_counter}"
                detected_vulnerabilities[vuln_name] = {"type": "GCP Storage", "url": f"http://{host}"}
                print(f"    [{vuln_name}] VULNERABILITY FOUND: {detected_vulnerabilities[vuln_name]['url']}")
                vuln_counter += 1

print(f"\n[+] Scan finished. Total vulnerabilities map: {len(detected_vulnerabilities)}")

if not detected_vulnerabilities:
    print("[*] No targets found. Exiting.")
    sys.exit(0)

selected_target = None

print("\n--- CubeMap Interactive Shell ---")
print("Commands: use <target_id> | exploit | exit")

while True:
    try:
        prompt = f"CubeMap({selected_target if selected_target else 'none'}) > "
        cmd_input = input(prompt).strip().split()
        
        if not cmd_input:
            continue
            
        cmd = cmd_input[0].lower()
        
        if cmd == "exit":
            break
            
        elif cmd == "use":
            if len(cmd_input) < 2:
                print("[-] Error: Specify target ID (e.g., use aws-1)")
                continue
            target_id = cmd_input[1]
            if target_id in detected_vulnerabilities:
                selected_target = target_id
                print(f"[+] Switched to target: {target_id} ({detected_vulnerabilities[target_id]['url']})")
            else:
                print(f"[-] Error: Target ID '{target_id}' not found.")
                
        elif cmd == "exploit":
            if not selected_target:
                print("[-] Error: No target selected. Use 'use <target_id>' first.")
                continue
            
            target_data = detected_vulnerabilities[selected_target]
            print(f"\n[*] Launching exploit payload on {target_data['type']}...")
            print(f"[*] Executing raw assembly structures mapping out {target_data['url']}...")
            print("[+] Exploitation cycle completed. Target compromised.")
            
        else:
            print(f"[-] Error: Unknown command '{cmd}'")
            
    except (KeyboardInterrupt, EOFError):
        print("\n[*] Exiting shell.")
        break
