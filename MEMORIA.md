# README - Proyecto Saimazoom

# 1. Introducción
Saimazoom es un sistema distribuido que simula la cadena logística de un marketplace utilizando RabbitMQ como middleware para la comunicación entre actores. Los actores del sistema son:

- **Cliente**: solicita pedidos, consulta su estado y puede cancelarlos.
- **Controlador**: gestiona los pedidos y coordina a los demás actores.
- **Robot**: simula la recogida del producto en el almacén.
- **Repartidor**: simula la entrega del producto al cliente.

# 2. Estructura del proyecto

```
.
├── controller/              # Código del controlador central
├── robot/                   # Código del robot
├── delivery/                # Código del repartidor
├── interfaces/              # Cliente interactivo desde terminal
├── messages/                # Protocolo de mensajes
├── scripts/                 # Scripts de prueba automatizados
├── clientes.pkl             # Persistencia de clientes
├── pedidos.pkl              # Persistencia de pedidos
├── run_sys.sh               # Script de arranque manual del sistema
```

# 3. Requisitos

- Python 3
- RabbitMQ en local o remoto (redes2.ii.uam.es)
- Terminal compatible con `gnome-terminal` 

# 4. Ejecución manual del sistema

Puedes lanzar los componentes básicos con el script:
```bash
./run_sys.sh
```
Este script abre terminales independientes para el controlador, robot, repartidor y cliente.

También puedes ejecutar cada componente por separado:
```bash
python3 controller/controller.py
python3 robot/robot.py
python3 delivery/delivery.py
python3 interfaces/commandline_client.py
```

# 5. Pruebas automatizadas

Dentro del directorio `scripts/`, se encuentran scripts Python para simular casos de uso completos:

- `simulate_case1_success.py`: Pedido completado con éxito.
- `simulate_case2_not_found.py`: Pedido fallido porque el robot no encuentra el producto.
- `simulate_case3_canceled.py`: Pedido cancelado antes de enviarse al repartidor.

Cada uno se lanza desde su respectivo script de bash:

```bash
./scripts/run_case1.sh  # Caso 1
./scripts/run_case2.sh  # Caso 2
./scripts/run_case3.sh  # Caso 3
```

Cada script lanza el controlador, robot, repartidor y un cliente que simula el comportamiento descrito.

# 6. Observaciones

- Todas las colas usan prefijos únicos para evitar colisiones: `2312-01_<tipo>`
- Las colas están configuradas con `durable=False` y `auto_delete=True` para facilitar el desarrollo.
- La persistencia de estado (clientes y pedidos) se realiza mediante ficheros `.pkl`

---

Este proyecto es parte de la asignatura Redes II. Para más detalles, consulta el documento de requisitos y el protocolo de mensajes (RFC-Saimazoom/1.0).
