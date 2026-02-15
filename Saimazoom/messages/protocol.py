"""
Módulo que define los mensajes, colas y estados usados en el sistema distribuido Saimazoom.
Contiene enumeraciones para garantizar consistencia en los nombres y evitar errores tipográficos.
"""
from enum import Enum

class Message(Enum):
    """Enumeración de los tipos de mensajes válidos en el sistema."""
    REGISTER = "REGISTER"
    LOGIN = "LOGIN"
    ORDER = "ORDER"
    CHECK = "CHECK"
    CANCEL = "CANCEL"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    ORDER_SUCCESS = "ORDER_SUCCESS"
    CHECK_SUCCESS = "CHECK_SUCCESS"
    CANCEL_SUCCESS = "CANCEL_SUCCESS"
    FAILURE = "FAILURE"
    MOVE = "MOVE"
    MOVE_SUCCESS = "MOVE_SUCCESS"
    MOVE_FAILURE = "MOVE_FAILURE"
    DELIVERY = "DELIVERY"
    DELIVERY_SUCCESS = "DELIVERY_SUCCESS"
    DELIVERY_FAILURE = "DELIVERY_FAILURE"
    CLI = "CLI"
    INFO = "I"
    WARNING = "W"
    ERROR = "E"

class QueueName:
    """
    Clase con los nombres de las colas del sistema.
    Las colas se nombran usando el prefijo del grupo.
    """
    CONTROLLER = "2312-01_controller"
    ROBOTS = "2312-01_robots"
    DELIVERY = "2312-01_delivery"

    @staticmethod
    def client_queue(client_id):
        """
        Devuelve el nombre de la cola de respuesta para un cliente específico.
        """
        return f"2312-01_client_{client_id}"

class OrderState(Enum):
    """
    Posibles estados en los que puede estar un pedido a lo largo del proceso.
    """
    PENDING = "PENDING"         # Pedido creado pero no tramitado aún
    IN_STORE = "IN_STORE"       # El producto está siendo gestionado en almacén
    ON_CONVEYOR = "ON_CONVEYOR" # Producto en cinta transportadora
    IN_DELIVERY = "IN_DELIVERY" # En proceso de reparto
    DELIVERED = "DELIVERED"     # Pedido entregado
    CANCELED = "CANCELED"       # Cancelado antes del reparto
    FAILED = "FAILED"           # Fallo durante la entrega
    NOT_FOUND = "NOT_FOUND"     # Producto no encontrado por el robot

def parse_config(file_path="config.conf") -> dict:
    """
    Lee un archivo de configuración clave=valor y devuelve un diccionario.
    Útil para valores como probabilidades de fallo o parámetros de simulación.
    """
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split('=')
                config[key.strip()] = float(value.strip())
    return config
