#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run setup script as root (sudo ./setup.sh)"
  exit 1
fi

BASE_DIR=$(pwd)

echo "[*] Compiling C++ network engine..."
cd "$BASE_DIR/FUN/SCANNER" || exit 1
make clean && make

echo "[*] Installing CubeMap global launcher executable into /usr/local/bin..."
LAUNCHER_PATH="/usr/local/bin/CubeMap"

echo "#!/bin/bash" > "$LAUNCHER_PATH"
echo "python3 $BASE_DIR/MAIN/Main.py \"\$@\"" >> "$LAUNCHER_PATH"

chmod +x "$LAUNCHER_PATH"
chmod +x "$BASE_DIR/MAIN/Main.py"

echo "[+] Installation completed. You can now execute 'CubeMap' globally from any path."
