import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pika
import uuid
import pickle
from messages.protocol import Message, QueueName, OrderState

# --- Almacenamiento en memoria ---
clientes = {}
pedidos = {}

# --- Persistencia ---
def guardar_datos():
    with open("clientes.pkl", "wb") as f:
        pickle.dump(clientes, f)
    with open("pedidos.pkl", "wb") as f:
        pickle.dump(pedidos, f)
    print(f"Guardado: {len(clientes)} clientes, {len(pedidos)} pedidos.")


def cargar_datos():
    global clientes, pedidos
    try:
        with open("clientes.pkl", "rb") as f:
            clientes = pickle.load(f)
    except FileNotFoundError:
        clientes = {}

    try:
        with open("pedidos.pkl", "rb") as f:
            pedidos = pickle.load(f)
    except FileNotFoundError:
        pedidos = {}

# --- Envío de respuestas ---
def send_response(channel, queue_name, message):
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message
    )
    print(f"[>] Enviado a {queue_name}: {message}")

# --- Manejo de mensajes entrantes ---
def handle_message(channel, method, properties, body):
    mensaje = body.decode()
    print(f"[<] Recibido: {mensaje}")
    partes = mensaje.strip().split()
    if not partes:
        return

    comando = partes[0]

    # --- Registro ---
    if comando == Message.REGISTER.value:
        client_id, password = partes[1], partes[2]
        if client_id in clientes:
            respuesta = Message.FAILURE.value + " Ya registrado"
        else:
            clientes[client_id] = password
            guardar_datos()
            print(f"Cliente registrado: {client_id}")
            respuesta = "REGISTERED " + client_id
        send_response(channel, QueueName.client_queue(client_id), respuesta)
    
    # --- Login ---
    elif comando == Message.LOGIN.value:
        client_id, password = partes[1], partes[2]
        if client_id in clientes and clientes[client_id] == password:
            respuesta = f"{Message.LOGIN_SUCCESS.value} {client_id}"
        else:
            respuesta = f"{Message.FAILURE.value} Login incorrecto"
        send_response(channel, QueueName.client_queue(client_id), respuesta)

    # --- Pedido nuevo ---
    elif comando == Message.ORDER.value:
        client_id, n_products = partes[1], int(partes[2])
        if client_id not in clientes:
            respuesta = Message.FAILURE.value + " Cliente no registrado"
            send_response(channel, QueueName.client_queue(client_id), respuesta)
            return

        order_id = str(uuid.uuid4())[:8]
        pedidos[order_id] = {
            "cliente": client_id,
            "productos": n_products,
            "estado": OrderState.PENDING.value
        }

        # Enviar a robot
        pedidos[order_id]["estado"] = OrderState.IN_STORE.value
        move_msg = f"{Message.MOVE.value} {order_id}"
        send_response(channel, QueueName.ROBOTS, move_msg)

        respuesta = f"{Message.ORDER_SUCCESS.value} {order_id}"
        send_response(channel, QueueName.client_queue(client_id), respuesta)
        guardar_datos()

    # --- Movimiento exitoso del robot ---
    elif comando == Message.MOVE_SUCCESS.value:
        order_id = partes[1]
        if order_id in pedidos:
            pedidos[order_id]["estado"] = OrderState.ON_CONVEYOR.value
            delivery_msg = f"{Message.DELIVERY.value} {order_id}"
            send_response(channel, QueueName.DELIVERY, delivery_msg)
            guardar_datos()

    # --- Fallo del robot ---
    elif comando == Message.MOVE_FAILURE.value:
        order_id = partes[1]
        if order_id in pedidos:
            pedidos[order_id]["estado"] = OrderState.NOT_FOUND.value
            client_id = pedidos[order_id]["cliente"]
            respuesta = f"{Message.FAILURE.value} Producto no encontrado"
            send_response(channel, QueueName.client_queue(client_id), respuesta)
            guardar_datos()

    # --- Entrega exitosa ---
    elif comando == Message.DELIVERY_SUCCESS.value:
        order_id = partes[1]
        if order_id in pedidos:
            pedidos[order_id]["estado"] = OrderState.DELIVERED.value
            client_id = pedidos[order_id]["cliente"]
            respuesta = f"{Message.DELIVERY_SUCCESS.value} {order_id}"
            send_response(channel, QueueName.client_queue(client_id), respuesta)
            guardar_datos()

    # --- Fallo en la entrega ---
    elif comando == Message.DELIVERY_FAILURE.value:
        order_id = partes[1]
        if order_id in pedidos:
            pedidos[order_id]["estado"] = OrderState.FAILED.value
            client_id = pedidos[order_id]["cliente"]
            respuesta = f"{Message.FAILURE.value} Fallo en la entrega"
            send_response(channel, QueueName.client_queue(client_id), respuesta)
            guardar_datos()

    # --- Cancelación de pedido ---
    elif comando == Message.CANCEL.value:
        order_id = partes[1]
        if order_id not in pedidos:
            respuesta = f"{Message.FAILURE.value} Pedido no encontrado"
        else:
            estado = pedidos[order_id]["estado"]
            if estado in [OrderState.DELIVERED.value, OrderState.IN_DELIVERY.value]:
                respuesta = f"{Message.FAILURE.value} Pedido ya en reparto o entregado"
            else:
                pedidos[order_id]["estado"] = OrderState.CANCELED.value
                respuesta = f"{Message.CANCEL_SUCCESS.value} {order_id}"
                guardar_datos()
            client_id = pedidos[order_id]["cliente"]
            send_response(channel, QueueName.client_queue(client_id), respuesta)

    # --- Consulta de estado ---
    elif comando == Message.CHECK.value:
        order_id = partes[1]
        if order_id not in pedidos:
            respuesta = f"{Message.FAILURE.value} Pedido no encontrado"
        else:
            estado = pedidos[order_id]["estado"]
            respuesta = f"{Message.CHECK_SUCCESS.value} {order_id} {estado}"
            client_id = pedidos[order_id]["cliente"]
            send_response(channel, QueueName.client_queue(client_id), respuesta)

# --- Main ---
def main():
    cargar_datos()
    print(f"[!] Clientes cargados: {len(clientes)}")
    print(f"[!] Pedidos cargados: {len(pedidos)}")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('redes2.ii.uam.es')  # Cambiar por 'redes2.ii.uam.es' para entrega
    )
    channel = connection.channel()

    queue_name = QueueName.CONTROLLER
    channel.queue_declare(queue=queue_name, durable=False, auto_delete=True)
    print(f"[!] Escuchando en cola {queue_name}...")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=handle_message,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    main()
