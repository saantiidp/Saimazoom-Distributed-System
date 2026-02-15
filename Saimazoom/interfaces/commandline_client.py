import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pika
import uuid
import time
from messages.protocol import Message, QueueName

class SaimazoomClient:
    def __init__(self, client_id, password):
        self.client_id = client_id
        self.password = password
        self.queue_controller = QueueName.CONTROLLER
        self.queue_client = QueueName.client_queue(client_id)

        # Conexión y canal de RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('redes2.ii.uam.es'))
        self.channel = self.connection.channel()

        # Declarar cola de cliente
        self.channel.queue_declare(queue=self.queue_client, durable=False, auto_delete=True)

    def send(self, message):
        """Envía un mensaje al controlador."""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_controller,
            body=message
        )
        print(f"[>] Enviado: {message}")

    def listen(self, expected_prefixes=None, timeout=5):
        """Escucha hasta encontrar un mensaje que empiece por alguno de los prefijos esperados."""
        if isinstance(expected_prefixes, str):
            expected_prefixes = [expected_prefixes]

        print("[~] Escuchando respuesta...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            method_frame, header_frame, body = self.channel.basic_get(queue=self.queue_client, auto_ack=True)
            if body:
                mensaje = body.decode()
                print(f"[~] Recibido: {mensaje}")
                if expected_prefixes is None or any(mensaje.startswith(p) for p in expected_prefixes):
                    if mensaje.startswith('ORDER_SUCCESS'):
                        self.last_order_id = mensaje.split()[1]
                    print(f"[<] Respuesta: {mensaje}")
                    return

            time.sleep(0.2)

        print("[!] No se recibió respuesta válida.")

    def register(self):
        message = f"{Message.REGISTER.value} {self.client_id} {self.password}"
        self.send(message)
        self.listen("REGISTERED")

    def login(self):
        message = f"{Message.LOGIN.value} {self.client_id} {self.password}"
        self.send(message)
        self.listen("LOGIN_SUCCESS")

    def order(self, n_products):
        message = f"{Message.ORDER.value} {self.client_id} {n_products}"
        self.send(message)

        # Escucha tanto la confirmación inicial como posibles fallos del robot
        self.listen(expected_prefixes=["ORDER_SUCCESS", "FAILURE"], timeout=8)


    def cancel(self, order_id):
        message = f"{Message.CANCEL.value} {order_id}"
        self.send(message)
        self.listen()

    def check(self, order_id):
        message = f"{Message.CHECK.value} {order_id}"
        self.send(message)
        self.listen("CHECK_SUCCESS")


    def close(self):
        self.connection.close()

def main():
    print("== Cliente Interactivo de Saimazoom ==")
    client_id = input("Introduce tu ID de cliente: ")
    password = input("Introduce tu contraseña: ")

    client = SaimazoomClient(client_id, password)

    print("\nComandos disponibles:")
    print("- register")
    print("- login")
    print("- order <n>")
    print("- cancel <order_id>")
    print("- check <order_id>")
    print("- exit\n")

    while True:
        try:
            entrada = input(">>> ").strip()
            if entrada == "exit":
                client.close()
                break
            elif entrada == "register":
                client.register()
            elif entrada == "login":
                client.login()
            elif entrada.startswith("order"):
                _, n = entrada.split()
                client.order(int(n))
            elif entrada.startswith("cancel"):
                _, oid = entrada.split()
                client.cancel(oid)
            elif entrada.startswith("check"):
                _, oid = entrada.split()
                client.check(oid)
            else:
                print("[!] Comando no reconocido.")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()