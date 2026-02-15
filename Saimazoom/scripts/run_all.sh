#!/bin/bash

echo "Lanzando el sistema Saimazoom..."

P_ALMACEN=1
P_ENTREGA=0.9

gnome-terminal --title="CONTROLADOR" -- bash -c "cd $(pwd); python3 controller/controller.py; exec bash"
gnome-terminal --title="ROBOT" -- bash -c "cd $(pwd); python3 robot/robot.py --p_almacen $P_ALMACEN; exec bash"
gnome-terminal --title="REPARTIDOR" -- bash -c "cd $(pwd); python3 delivery/delivery.py --p_entrega $P_ENTREGA; exec bash"
gnome-terminal --title="CLIENTE" -- bash -c "cd $(pwd); python3 interfaces/commandline_client.py; exec bash"
