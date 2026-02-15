import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'interfaces')))
from commandline_client import SaimazoomClient

client_id = "cliente_cancel"
password = "cancel123"

cliente = SaimazoomClient(client_id, password)

print("== Caso 3: Pedido cancelado antes del reparto ==")
cliente.register()
cliente.login()
cliente.order(1)

# Esperar un poco para asegurarse de que el robot empiece, pero no tanto como para que termine
time.sleep(3)

order_id = cliente.last_order_id
if order_id:
    print(f"[>] Cancelando pedido {order_id} antes del reparto...")
    cliente.send(f"CANCEL {order_id}")
    cliente.listen(["CANCEL_SUCCESS", "FAILURE"], timeout=5)

    print(f"[>] Consultando estado del pedido {order_id}...")
    cliente.send(f"CHECK {order_id}")
    cliente.listen("CHECK_SUCCESS", timeout=5)
else:
    print("[!] No se pudo obtener el ID del pedido para cancelar.")

cliente.close()