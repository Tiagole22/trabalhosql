import subprocess
import sys

processos = [
    subprocess.Popen([sys.executable, "ms_usuarios.py"]),
    subprocess.Popen([sys.executable, "ms_pedidos.py"]),
    subprocess.Popen([sys.executable, "frontend.py"])
]

try:
    for p in processos:
        p.wait()
except KeyboardInterrupt:
    for p in processos:
        p.terminate()