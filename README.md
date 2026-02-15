# Saimazoom — Sistema Distribuido de Pedidos (RabbitMQ)

Sistema distribuido que **simula la cadena logística de un marketplace** usando **RabbitMQ** y colas de mensajes. Incluye **cliente**, **controlador**, **robots** y **repartidores**, con un **flujo de estados de pedido** bien definido y un **protocolo de mensajes** tipo RFC.

> Proyecto académico (Redes II). La documentación completa de requisitos y mensajes está en `Plantilla_Requisitos.pdf` y `Documento_Especificación_de_mensajes_de_Saimazoom.pdf`.

---

## 🚀 Descripción

Saimazoom coordina pedidos desde su creación hasta su entrega mediante **publicación/suscripción** sobre RabbitMQ.  
El **controlador central** orquesta el proceso, asigna robots y repartidores, mantiene **persistencia** y notifica a los clientes.  
Los **robots** simulan la búsqueda de productos en almacén y los **repartidores** simulan la entrega con reintentos y posibles fallos.

Estados de un pedido (ver diagrama incluido):
- `PENDING` → `IN_STORE` → `ON_CONVEYOR` → `IN_DELIVERY` → `DELIVERED`
- Alternativas: `NOT_FOUND`, `FAILED`, `CANCELED`

---

## 🏗️ Arquitectura (alto nivel)

- **Cliente**: registra/login, crea pedidos (`ORDER`), consulta (`CHECK`) y cancela (`CANCEL`).
- **Controlador**: recibe peticiones, gestiona estados, asigna trabajo y persiste datos.
- **Robot**: procesa `MOVE <order_id>` y responde con `MOVE_SUCCESS` o `MOVE_FAILURE`.
- **Repartidor**: procesa `DELIVERY <order_id>` y responde con `DELIVERY_SUCCESS` o `DELIVERY_FAILURE`.
- **Mensajería**: RabbitMQ con colas separadas por actor; comunicación asíncrona y desacoplada.

---

## 🧾 Protocolo de mensajes (resumen)

Comandos principales (formato: `COMANDO arg1 arg2 ...`):
- Cliente → Controlador: `REGISTER`, `LOGIN`, `ORDER`, `CHECK`, `CANCEL`
- Controlador → Robot: `MOVE`
- Robot → Controlador: `MOVE_SUCCESS`, `MOVE_FAILURE`
- Controlador → Repartidor: `DELIVERY`
- Repartidor → Controlador: `DELIVERY_SUCCESS`, `DELIVERY_FAILURE`
- Respuestas al cliente: `LOGIN_SUCCESS`, `ORDER_SUCCESS`, `CHECK_SUCCESS`, `CANCEL_SUCCESS`, `FAILURE`

El detalle completo de sintaxis y semántica está en el documento RFC del proyecto.

---

## 📁 Estructura del proyecto (típica)

```
.
├── controller/              # Controlador central
├── robot/                   # Robot (trabajador de almacén)
├── delivery/                # Repartidor
├── interfaces/              # Cliente por terminal
├── messages/                # Definición del protocolo
├── scripts/                 # Scripts de simulación de casos de uso
├── clientes.pkl             # Persistencia de clientes
├── pedidos.pkl              # Persistencia de pedidos
├── run_sys.sh               # Arranque manual del sistema
└── README.md
```

---

## ▶️ Requisitos

- Python 3
- RabbitMQ (local o servidor de la asignatura)
- `pika` (cliente RabbitMQ para Python)

---

## ▶️ Cómo ejecutar

### Arranque completo (manual)
```bash
./run_sys.sh
```

Esto abre terminales para **controlador**, **robot**, **repartidor** y **cliente**.

### Arranque por componentes
```bash
python3 controller/controller.py
python3 robot/robot.py
python3 delivery/delivery.py
python3 interfaces/commandline_client.py
```

---

## 🧪 Pruebas / Simulaciones

En `scripts/` hay simulaciones de casos de uso:
- Pedido completado con éxito
- Pedido no encontrado por el robot
- Pedido cancelado antes del reparto

Cada caso se lanza con su script correspondiente (`run_case*.sh`).

---

## 🗺️ Diagramas incluidos

- **Diagrama de clases**: relaciones entre Cliente, Controlador, Robot, Repartidor y Pedido.
- **Diagrama de estados de pedido**: transiciones entre `PENDING`, `IN_STORE`, `ON_CONVEYOR`, `IN_DELIVERY`, `DELIVERED`, `FAILED`, `NOT_FOUND`, `CANCELED`.
- **Tabla y sintaxis de mensajes**: en el RFC del proyecto.

(Ver PDFs adjuntos en el repositorio.)

---

## 🛠️ Tecnologías

- Python 3
- RabbitMQ
- pika
- Persistencia en ficheros (`.pkl`)
- Bash para orquestación de pruebas

---

## 👤 Autor

Santiago de Prada Lorenzo  
Universidad Autónoma de Madrid — Redes II

---

## 📜 Licencia

MIT (o la licencia académica que prefieras)
