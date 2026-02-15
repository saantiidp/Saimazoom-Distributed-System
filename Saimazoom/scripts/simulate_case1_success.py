import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'interfaces')))
from commandline_client import SaimazoomClient

client_id = "cliente_success"
password = "1234"

cliente = SaimazoomClient(client_id, password)

print("== Caso 1: Pedido exitoso ==")
cliente.register()
cliente.login()
cliente.order(2)

# Esperar a que se complete el proceso logístico
time.sleep(10)

# Consultar estado usando el ID guardado
order_id = cliente.last_order_id
if order_id:
    print(f"[>] Consultando estado del pedido {order_id}...")
    cliente.send(f"CHECK {order_id}")
    cliente.listen("CHECK_SUCCESS", timeout=5)
else:
    print("[!] No se pudo determinar el ID del pedido para el CHECK.")

cliente.close()