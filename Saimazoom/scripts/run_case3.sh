#!/bin/bash

echo "Lanzando entorno para CASO 3: Cancelación antes del reparto"

gnome-terminal --title="CONTROLADOR" -- bash -c "python3 controller/controller.py; exec bash"
gnome-terminal --title="ROBOT" -- bash -c "python3 robot/robot.py --p_almacen 1.0; exec bash"
gnome-terminal --title="REPARTIDOR" -- bash -c "python3 delivery/delivery.py --p_entrega 1.0; exec bash"

# Esperamos un poco para asegurar que las colas estén inicializadas
sleep 2

gnome-terminal --title="CLIENTE CASO 3" -- bash -c "python3 scripts/simulate_case3_canceled.py; exec bash"
