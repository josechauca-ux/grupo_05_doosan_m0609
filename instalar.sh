#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

echo
echo "============================================"
echo " INSTALACION - DOOSAN M0609 - GRUPO 05"
echo "============================================"

if [ ! -f /opt/ros/jazzy/setup.bash ]; then
    echo "ERROR: No se encontro ROS 2 Jazzy."
    echo "Instala ROS 2 Jazzy antes de continuar."
    exit 1
fi

source /opt/ros/jazzy/setup.bash

cd "$SCRIPT_DIR"

echo
echo "[1/5] Instalando herramientas necesarias..."
sudo apt update
sudo apt install -y python3-vcstool python3-rosdep python3-numpy

echo
echo "[2/5] Importando dependencias externas..."
vcs import src < dependencias.repos

echo
echo "[3/5] Instalando dependencias ROS..."
rosdep update
rosdep install --from-paths src --ignore-src -r -y

echo
echo "[4/5] Compilando workspace..."
colcon build --packages-up-to grupo05_doosan_m0609_bringup m0609_kinematics --symlink-install

echo
echo "[5/5] Preparando entorno..."
source "$SCRIPT_DIR/install/setup.bash"

echo
echo "============================================"
echo " INSTALACION COMPLETADA"
echo "============================================"
echo "Workspace: $SCRIPT_DIR"
echo
