#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

source /opt/ros/jazzy/setup.bash
source "$SCRIPT_DIR/entorno.sh"

echo
echo "============================================"
echo " VERIFICACION DEL PROYECTO M0609"
echo "============================================"

echo
echo "[1] Paquetes propios:"
ros2 pkg list | grep -E '^grupo05_doosan_m0609_bringup$|^m0609_kinematics$'

echo
echo "[2] Ejecutables de m0609_kinematics:"
ros2 pkg executables m0609_kinematics

echo
echo "[3] Dependencia Doosan:"
ros2 pkg list | grep '^dsr_description2$'

echo
echo "============================================"
echo " VERIFICACION COMPLETADA"
echo "============================================"
