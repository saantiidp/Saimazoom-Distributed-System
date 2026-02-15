"""
Script de cliente que se comunica con el controlador de Saimazoom a través de RabbitMQ.
Permite realizar acciones básicas como registrar, iniciar sesión y hacer pedidos.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pika
import argparse
import uuid
import time
from messages.protocol import Message, QueueName



def send_message(channel, queue, message):
    """Envía un mensaje a la cola especificada."""
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=message
    )
    print(f"[>] Enviado a {queue}: {message}")

def listen_response(channel, queue_name):
    """Escucha una única respuesta en la cola del cliente."""
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    if body:
        print(f"[<] Respuesta recibida: {body.decode()}")
    else:
        print("[!] No se recibió respuesta (¿mensaje no procesado aún?)")


def main():
    parser = argparse.ArgumentParser(description="Cliente de Saimazoom")
    parser.add_argument("--id", required=True, help="ID del cliente")
    parser.add_argument("--password", required=True, help="Contraseña del cliente")
    parser.add_argument("--action", required=True, choices=["register", "login", "order"], help="Acción a realizar")
    parser.add_argument("--n_products", type=int, help="Número de productos (solo para 'order')")

    args = parser.parse_args()
    client_id = args.id
    password = args.password
    action = args.action
    n_products = args.n_products

    # Conexión a RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

     # Declarar la cola del cliente y del controlador
    controller_queue = QueueName.CONTROLLER
    client_queue = QueueName.client_queue(client_id)
    channel.queue_declare(queue=client_queue, durable=False, auto_delete=True)

    # Construir el mensaje según la acción
    if action == "register":
        message = f"{Message.REGISTER.value} {client_id} {password}"
    elif action == "login":
        message = f"{Message.LOGIN.value} {client_id} {password}"
    elif action == "order":
        if n_products is None:
            print("[!] Debes indicar --n_products para hacer un pedido.")
            return
        message = f"{Message.ORDER.value} {client_id} {n_products}"

    # Enviar mensaje al controlador
    send_message(channel, controller_queue, message)

    # Esperar breve para que el controlador tenga tiempo de responder
    time.sleep(1)

    # Escuchar la respuesta en la cola del cliente
    listen_response(channel, client_queue)

    # Cerrar conexión
    connection.close()

if __name__ == "__main__":
    main()