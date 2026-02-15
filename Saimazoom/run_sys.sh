#!/bin/bash

# Lanza controlador, robot, delivery y cliente en terminales nuevas (modo GNOME)
echo "Lanzando el sistema Saimazoom..."

# Puedes cambiar estas probabilidades fácilmente
P_ALMACEN=1
P_ENTREGA=0.1

# Lanza controlador
gnome-terminal --title="CONTROLADOR" -- bash -c "cd $(pwd); python3 controller/controller.py; exec bash"

# Lanza robot con p_almacen
gnome-terminal --title="ROBOT" -- bash -c "cd $(pwd); python3 robot/robot.py --p_almacen $P_ALMACEN; exec bash"

# Lanza delivery con p_entrega
gnome-terminal --title="REPARTIDOR" -- bash -c "cd $(pwd); python3 delivery/delivery.py --p_entrega $P_ENTREGA; exec bash"

# Lanza cliente
gnome-terminal -- bash -c "cd $(pwd); python3 interfaces/commandline_client.py; exec bash"
