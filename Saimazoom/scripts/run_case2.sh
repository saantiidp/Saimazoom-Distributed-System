#!/bin/bash

echo "Lanzando entorno para CASO 2: Producto no encontrado"

gnome-terminal --title="CONTROLADOR" -- bash -c "python3 controller/controller.py; exec bash"
gnome-terminal --title="ROBOT" -- bash -c "python3 robot/robot.py --p_almacen 0.0; exec bash"
gnome-terminal --title="REPARTIDOR" -- bash -c "python3 delivery/delivery.py --p_entrega 1.0; exec bash"
sleep 2
gnome-terminal --title="CLIENTE CASO 2" -- bash -c "python3 scripts/simulate_case2_not_found.py; exec bash"
