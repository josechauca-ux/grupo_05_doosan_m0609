#!/usr/bin/env bash

# Directorio del workspace, independientemente de dónde se haya clonado
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# ROS 2 Jazzy
source /opt/ros/jazzy/setup.bash

# DDS utilizado durante las pruebas
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Workspace
if [ -f "$SCRIPT_DIR/install/setup.bash" ]; then
    source "$SCRIPT_DIR/install/setup.bash"
fi
