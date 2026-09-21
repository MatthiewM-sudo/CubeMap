# CubeMap - High Speed Cloud Attack Surface Enumerator

CubeMap is an offensive security tool designed to map, enumerate, and test misconfigured cloud resources across multiple infrastructure providers concurrently. Leveraging a hybrid architecture, it controls arguments and mutates corporate keywords in Python while offloading raw network sockets execution to an optimized low-level C++ engine.

## File Architecture
* **FUN/EXPLOIT/Exploit.asm**: Low-level assembly exploitation payloads and shellcodes.
* **FUN/SCANNER/Scanner.cpp**: C++ socket engine checking open endpoints via direct hardware layer integration.
* **MAIN/Main.py**: Main Python controller orchestrating user arguments and logic pipelines.
* **README/README.md**: Tool documentation.

## Prerequisites & Installation
Ensure you are running a Linux distribution (such as Kali Linux) with `g++` and Python 3 installed.

1. Navigate to the scanner directory:
   cd FUN/SCANNER
   
2. Compile the shared C++ engine:
   make
   

## Usage Instructions
Execute the core script from the `MAIN` directory. The syntax requires selecting multi-cloud platforms separated by hyphens and a corporate keyword to fuzz.

python3 Main.py -e aws-azure-gcp targetcompany

### Interactive Mode
If CubeMap flags an open bucket or exposed storage environment, an internal hook intercepts execution, alerts the operator of a vulnerability, and asks for explicit confirmation before triggering any automated memory post-exploitation payload written in assembly.
