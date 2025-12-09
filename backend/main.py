import subprocess
import time
import os
import signal
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = os.path.join(BASE_DIR, "..", "venv", "Scripts", "python.exe")

print("\n🚀 Starting PHISHGUARD Backend...\n")

p1 = subprocess.Popen([PYTHON, os.path.join(BASE_DIR, "api.py")])
time.sleep(1)
p2 = subprocess.Popen([PYTHON, os.path.join(BASE_DIR, "emailchk.py")])

print("✅ URL API     → http://127.0.0.1:8000")
print("✅ EMAIL API   → http://127.0.0.1:8001\n")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Stopping backend…")
    p1.terminate()
    p2.terminate()
    sys.exit(0)