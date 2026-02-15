import pika
import time
import random
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from messages.protocol import Message, QueueName

def procesar_pedido(channel, method, properties, body, p_almacen):
    mensaje = body.decode()
    print(f"[ROBOT <] Recibido: {mensaje}")

    partes = mensaje.split()
    if len(partes) != 2 or partes[0] != Message.MOVE.value:
        print("[ROBOT] Mensaje inválido")
        return

    order_id = partes[1]
    print(f"[ROBOT] Buscando producto del pedido {order_id}...")

    time.sleep(random.randint(5, 10))  # simula búsqueda

    if random.random() < p_almacen:
        print(f"[ROBOT >] Producto encontrado, enviando MOVE_SUCCESS {order_id}")
        respuesta = f"{Message.MOVE_SUCCESS.value} {order_id}"
    else:
        print(f"[ROBOT >] Producto NO encontrado, enviando MOVE_FAILURE {order_id}")
        respuesta = f"{Message.MOVE_FAILURE.value} {order_id}"

    channel.basic_publish(
        exchange='',
        routing_key=QueueName.CONTROLLER,
        body=respuesta
    )

def main():
    parser = argparse.ArgumentParser(description="Robot Saimazoom")
    parser.add_argument("--p_almacen", type=float, default=1.0, help="Probabilidad de encontrar el producto (0.0–1.0)")
    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters('redes2.ii.uam.es'))
    channel = connection.channel()

    queue_name = QueueName.ROBOTS
    channel.queue_declare(queue=queue_name, durable=False, auto_delete=True)
    print(f"[ROBOT] Escuchando en cola {queue_name}...")

    def callback(ch, method, properties, body):
        procesar_pedido(ch, method, properties, body, args.p_almacen)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    main()
