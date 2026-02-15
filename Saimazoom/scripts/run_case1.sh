#!/bin/bash

echo "Lanzando entorno para CASO 1: Pedido exitoso"

gnome-terminal --title="CONTROLADOR" -- bash -c "python3 controller/controller.py; exec bash"
gnome-terminal --title="ROBOT" -- bash -c "python3 robot/robot.py --p_almacen 1.0; exec bash"
gnome-terminal --title="REPARTIDOR" -- bash -c "python3 delivery/delivery.py --p_entrega 1.0; exec bash"
sleep 2
gnome-terminal --title="CLIENTE CASO 1" -- bash -c "python3 scripts/simulate_case1_success.py; exec bash"
