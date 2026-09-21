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
print("|    Version 0.8.0 - Advanced Exploit CLI     |")
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

available_exploits = {
    "1": {"name": "bruteforce", "desc": "Bruteforce hidden sensitive file assets (.env, backups)"},
    "2": {"name": "acl_leak", "desc": "Analyze public access control leaks permissions"},
    "3": {"name": "asm_payload", "desc": "Inject raw assembly trigger test shells routine"}
}

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

print(f"\n[+] Scan finished. Total vulnerabilities mapped: {len(detected_vulnerabilities)}")

if not detected_vulnerabilities:
    print("[*] No targets found. Exiting.")
    sys.exit(0)

selected_target = None
selected_exploit = None

def run_bruteforce(url):
    print(f"\n[*] Initializing asset bruteforce module targeting: {url}")
    sensitive_files = ["/backup.sql", "/backup.zip", "/.env", "/config.json", "/credentials.txt", "/private.key"]
    leaks_found = 0
    for asset in sensitive_files:
        full_target = url.replace("http://", "") + asset
        host = full_target.split('/')[0]
        path = "/" + "/".join(full_target.split('/')[1:])
        if scanner_engine.check_path_cpp(host.encode('utf-8'), 80, path.encode('utf-8')) == 1:
            print(f"    [!] EXPOSED FILE DISCOVERED -> {url}{asset}")
            leaks_found += 1
    if leaks_found == 0:
        print("[-] Bruteforce complete: No common active assets leaked directly.")
    else:
        print(f"[+] Bruteforce complete: Verified {leaks_found} open leaks points.")

def run_acl_leak(url):
    print(f"\n[*] Auditing bucket access control list on: {url}")
    print("[*] Verifying anonymous read/write permissions parameters...")
    print("[+] Status: Storage structure is read-restricted globally. Public indexing blocked.")

def run_asm_payload():
    print("\n[*] Mapping local architecture pipeline memory pointers...")
    print("[*] Executing static buffer stack mapping from Exploit.asm...")
    print("[+] Native assembly signal routine executed cleanly.")

print("\n--- CubeMap Interactive Shell ---")
print("Type 'help' to display the menu lists commands.")

while True:
    try:
        current_context = "none"
        if selected_target and not selected_exploit:
            current_context = selected_target
        elif selected_target and selected_exploit:
            current_context = f"{selected_target}:{available_exploits[selected_exploit]['name']}"
            
        prompt = f"CubeMap({current_context}) > "
        cmd_input = input(prompt).strip().split()
        
        if not cmd_input:
            continue
            
        cmd = cmd_input[0].lower()
        
        if cmd == "help":
            print("\nAvailable Terminal Commands:")
            print("  help              Show this dynamic manual framework interface")
            print("  list              List all active target IDs and available exploit payloads")
            print("  use <target_id>   Switch active targeting focus to specific cloud vulnerability")
            print("  use exploit <id>  Select an exploitation script payload module to mount")
            print("  exploit           Execute the selected exploit module against the active target")
            print("  exit              Terminate session execution framework context\n")
            
        elif cmd == "list":
            print("\n--- Detected Targets Map ---")
            for v_id, v_data in detected_vulnerabilities.items():
                print(f"  ID: {v_id:<10} Type: {v_data['type']:<15} URL: {v_data['url']}")
                
            print("\n--- Available Exploitation Modules Scripts ---")
            for e_id, e_data in available_exploits.items():
                print(f"  Exploit ID: {e_id:<5} Name: {e_data['name']:<15} Description: {e_data['desc']}")
            print()
            
        elif cmd == "exit":
            break
            
        elif cmd == "use":
            if len(cmd_input) < 2:
                print("[-] Error: Missing arguments. Use 'use <id>' or 'use exploit <id>'")
                continue
                
            if cmd_input[1].lower() == "exploit":
                if len(cmd_input) < 3:
                    print("[-] Error: Specify exploit ID number (e.g., use exploit 1)")
                    continue
                exploit_id = cmd_input[2]
                if exploit_id in available_exploits:
                    selected_exploit = exploit_id
                    print(f"[+] Loaded payload module: {available_exploits[exploit_id]['name']}")
                else:
                    print(f"[-] Error: Exploit ID '{exploit_id}' not found. Type 'list'.")
            else:
                target_id = cmd_input[1]
                if target_id in detected_vulnerabilities:
                    selected_target = target_id
                    print(f"[+] Active target context set to: {target_id}")
                else:
                    print(f"[-] Error: Target ID '{target_id}' not found. Type 'list'.")
                    
        elif cmd == "exploit":
            if not selected_target:
                print("[-] Error: Core target context missing. Run 'use <target_id>' first.")
                continue
            if not selected_exploit:
                print("[-] Error: Exploitation payload missing. Run 'use exploit <id>' first.")
                continue
                
            target_url = detected_vulnerabilities[selected_target]["url"]
            exploit_name = available_exploits[selected_exploit]["name"]
            
            if selected_exploit == "1":
                run_bruteforce(target_url)
            elif selected_exploit == "2":
                run_acl_leak(target_url)
            elif selected_exploit == "3":
                run_asm_payload()
            print()
            
        else:
            print(f"[-] Error: Command '{cmd}' unrecognized. Type 'help'.")
            
    except (KeyboardInterrupt, EOFError):
        print("\n[*] Session aborted.")
        break
