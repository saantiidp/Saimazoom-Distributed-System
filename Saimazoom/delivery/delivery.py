import pika
import time
import random
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from messages.protocol import Message, QueueName

def intentar_entrega(channel, order_id, p_entrega):
    for intento in range(1, 4):  # hasta 3 intentos
        print(f"[DELIVERY] Intento {intento} de entrega para pedido {order_id}...")
        time.sleep(random.randint(10, 20))  # tiempo de intento

        if random.random() < p_entrega:
            print(f"[DELIVERY >] Entrega exitosa en intento {intento}")
            respuesta = f"{Message.DELIVERY_SUCCESS.value} {order_id}"
            break
    else:
        print(f"[DELIVERY >] Fallo tras 3 intentos. Pedido {order_id} no entregado.")
        respuesta = f"{Message.DELIVERY_FAILURE.value} {order_id}"

    channel.basic_publish(
        exchange='',
        routing_key=QueueName.CONTROLLER,
        body=respuesta
    )

def main():
    parser = argparse.ArgumentParser(description="Repartidor Saimazoom")
    parser.add_argument("--p_entrega", type=float, default=1.0, help="Probabilidad de éxito en cada intento (0.0–1.0)")
    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters('redes2.ii.uam.es'))
    channel = connection.channel()

    queue_name = QueueName.DELIVERY
    channel.queue_declare(queue=queue_name, durable=False, auto_delete=True)
    print(f"[DELIVERY] Escuchando en cola {queue_name}...")

    def callback(ch, method, properties, body):
        mensaje = body.decode()
        print(f"[DELIVERY <] Recibido: {mensaje}")
        partes = mensaje.strip().split()
        if len(partes) == 2 and partes[0] == Message.DELIVERY.value:
            order_id = partes[1]
            intentar_entrega(channel, order_id, args.p_entrega)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    main()
