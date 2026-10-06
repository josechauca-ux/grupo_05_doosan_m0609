#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

source /opt/ros/jazzy/setup.bash
source "$SCRIPT_DIR/entorno.sh"

cd "$SCRIPT_DIR"

colcon build --packages-up-to grupo05_doosan_m0609_bringup m0609_kinematics --symlink-install

source "$SCRIPT_DIR/install/setup.bash"

echo
echo "============================================"
echo " COMPILACION COMPLETADA"
echo "============================================"
echo "Workspace: $SCRIPT_DIR"
echo
