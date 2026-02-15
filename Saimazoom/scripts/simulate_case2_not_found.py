# scripts/simulate_case2_not_found.py
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'interfaces')))
from commandline_client import SaimazoomClient


client_id = "cliente_fail_robot"
password = "1234"

cliente = SaimazoomClient(client_id, password)

print("== Caso 2: Producto no encontrado ==")
cliente.register()
cliente.login()
cliente.order(1)

# Esperar fallo del robot
time.sleep(8)
cliente.listen("FAILURE", timeout=10)

cliente.close()
