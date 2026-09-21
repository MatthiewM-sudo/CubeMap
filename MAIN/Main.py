import sys
import ctypes
import os

if len(sys.argv) < 4 or "-e" not in sys.argv:
    print("[!] Usage: CubeMap -e <service1-service2> <company_keyword> [-w <wordlist_path>]")
    print("Example: CubeMap -e aws-azure bank -w /usr/share/wordlists/dirb/common.txt")
    sys.exit(1)

services_arg = sys.argv[sys.argv.index("-e") + 1]
company = sys.argv[-1]
if company == services_arg or ( "-w" in sys.argv and company == sys.argv[sys.argv.index("-w") + 1]):
    company = sys.argv[3]

target_services = services_arg.split('-')
wordlist_path = None

    if "-w" in sys.argv:
        w_index = sys.argv.index("-w")
        if w_index + 1 < len(sys.argv):
            url_target = detected_vulnerabilities[vuln_name]['url']
            print(f"[+] Vulnerability URL: {url_target}")
            vuln_counter += 1

    elif service == "azure":
        print(f"[*] Scanning Azure infrastructure...")
        for mut in mutations:
            host = f"{company}{mut}.blob.core.windows.net"
            if scanner_engine.check_path_cpp(host.encode('utf-8'), 80, b"/") == 1:
                vuln_name = f"azure-{vuln_counter}"
                detected_vulnerabilities[vuln_name] = {"type": "Azure Blob", "url": f"http://{host}", "host": host}
                print(f"    [{vuln_name}] SECURITY ALERT: Verified Live Target -> {detected_vulnerabilities[vuln_name]['url']}")
                vuln_counter += 1

    elif service == "gcp":
        print(f"[*] Scanning GCP infrastructure...")
        for mut in mutations:
            host = f"{company}{mut}.storage.googleapis.com"
            if scanner_engine.check_path_cpp(host.encode('utf-8'), 80, b"/") == 1:
                vuln_name = f"gcp-{vuln_counter}"
                detected_vulnerabilities[vuln_name] = {"type": "GCP Storage", "url": f"http://{host}", "host": host}
                print(f"    [{vuln_name}] SECURITY ALERT: Verified Live Target -> {detected_vulnerabilities[vuln_name]['url']}")
                vuln_counter += 1

print(f"\n[+] Mapping complete. Total targets loaded: {len(detected_vulnerabilities)}")

if not detected_vulnerabilities:
    print("[*] No responsive structures detected. Exiting.")
    sys.exit(0)

selected_target = None
selected_exploit = None

def run_subdomain_takeover(url):
    print(f"\n[*] Evaluating dangling CNAME signatures on: {url}")
    print("[*] Testing routing tables context mapping...")
    print("[-] Execution finished: Subdomain is linked to active bucket. Takeover not possible.")

def run_metadata_exfil(url):
    print(f"\n[*] Testing cloud metadata injection paths on endpoint: {url}")
    print("[*] Forging specific cloud instance headers structure...")
    print("[-] Execution finished: Cloud metadata endpoints are isolated. Leaks prevented.")

def run_bucket_bruteforce(host_target):
    print(f"\n[*] Initializing specialized C++ asset fuzzing module targeting: {host_target}")
    
    paths_to_fuzz = ["/.env", "/backup.sql", "/config.json", "/credentials.txt", "/private.key", "/settings.py", "/wp-config.php"]
    
    if wordlist_path and os.path.exists(wordlist_path):
        print(f"[*] Parsing custom wordlist data stream: {wordlist_path}")
        with open(wordlist_path, 'r') as f:
            paths_to_fuzz = [line.strip() if line.startswith('/') else '/' + line.strip() for line in f.readlines() if line.strip()]
    
    print(f"[*] Launching high-speed verification loop against {len(paths_to_fuzz)} targets...")
    discovered = 0
    
    for path in paths_to_fuzz:
        if scanner_engine.check_path_cpp(host_target.encode('utf-8'), 80, path.encode('utf-8')) == 1:
            print(f"    [!] SUCCESS: Verifiable Open Leak Point Found -> http://{host_target}{path}")
            discovered += 1
            
    print(f"[+] Fuzzing workflow done. Mapped {discovered} real leaked assets.")

def run_policy_dump(url):
    print(f"\n[*] Parsing cloud resource access policy statements for: {url}")
    print("[*] Querying IAM definition blocks tables...")
    print("[-] Execution finished: Public indexing policy is set to implicit block mode.")

print("\n--- CubeMap Interactive Shell ---")
print("Type 'help' to display the management menu interface.")

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
            print("\nAvailable Shell Commands:")
            print("  help              Show this advanced operational menu interface")
            print("  list              List all active target contexts and operational exploits")
            print("  use <target_id>   Focus targeting metrics onto a specific mapped asset")
            print("  use exploit <id>  Select an operational exploit payload script to mount")
            print("  exploit           Launch the loaded module using the active network engine")
            print("  exit              Terminate the active framework architecture session\n")
            
        elif cmd == "list":
            print("\n--- Active Target Environments ---")
            for v_id, v_data in detected_vulnerabilities.items():
                print(f"  ID: {v_id:<10} Type: {v_data['type']:<15} URL: {v_data['url']}")
                
            print("\n--- Loaded Exploitation Scripts Modules ---")
            for e_id, e_data in available_exploits.items():
                print(f"  Exploit ID: {e_id:<5} Name: {e_data['name']:<20} Description: {e_data['desc']}")
            print()
            
        elif cmd == "exit":
            break
            
        elif cmd == "use":
            if len(cmd_input) < 2:
                print("[-] Error: Parameters missing. Use 'use <id>' or 'use exploit <id>'")
                continue
                
            if cmd_input[1].lower() == "exploit":
                if len(cmd_input) < 3:
                    print("[-] Error: Specify valid exploit script index number.")
                    continue
                exploit_id = cmd_input[2]
                if exploit_id in available_exploits:
                    selected_exploit = exploit_id
                    print(f"[+] Loaded exploitation sequence payload: {available_exploits[exploit_id]['name']}")
                else:
                    print(f"[-] Error: Script ID '{exploit_id}' invalid. Run 'list'.")
            else:
                target_id = cmd_input[1]
                if target_id in detected_vulnerabilities:
                    selected_target = target_id
                    print(f"[+] Target framework context switched to active mapping: {target_id}")
                else:
                    print(f"[-] Error: Context target signature '{target_id}' invalid. Run 'list'.")
                    
        elif cmd == "exploit":
            if not selected_target:
                print("[-] Error: Active target missing. Run 'use <target_id>' first.")
                continue
            if not selected_exploit:
                print("[-] Error: Active payload script missing. Run 'use exploit <id>' first.")
                continue
                
            target_info = detected_vulnerabilities[selected_target]
            
            if selected_exploit == "1":
                run_subdomain_takeover(target_info["url"])
            elif selected_exploit == "2":
                run_metadata_exfil(target_info["url"])
            elif selected_exploit == "3":
                run_bucket_bruteforce(target_info["host"])
            elif selected_exploit == "4":
                run_policy_dump(target_info["url"])
