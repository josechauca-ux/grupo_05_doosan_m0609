# Primer Parcial Práctico - Doosan M0609

## IMT-342 Robótica Chauca

Proyecto de ROS 2 para la visualización y estudio cinemático del robot
industrial **Doosan M0609**.

El proyecto incluye:

-   Modelo URDF del Doosan M0609 mediante `dsr_description2`.
-   Visualización en RViz2.
-   Transformaciones TF.
-   Cinemática directa (FK).
-   Cinemática inversa numérica (IK).
-   Publicación y lectura de `/joint_states`.
-   Objetivos cartesianos mediante `/target`.
-   Scripts para instalación, compilación y verificación.
-   Archivo `dependencias.repos` para recuperar la dependencia externa
    de Doosan.

------------------------------------------------------------------------

## 1. Requisitos

El proyecto fue desarrollado y probado con:

-   Ubuntu 24.04
-   ROS 2 Jazzy
-   Python 3
-   Git
-   NumPy
-   Colcon
-   RViz2
-   `vcstool`

No se requiere el robot físico para ejecutar las pruebas de
visualización, FK e IK.

> **Importante:** la instalación está pensada para una computadora con
> Ubuntu 24.04 y ROS 2 Jazzy.

------------------------------------------------------------------------

## 2. Descargar el proyecto

Abrir una terminal y ejecutar:

``` bash
cd ~
git clone https://github.com/josechauca-ux/grupo_05_doosan_m0609.git
```

Entrar al proyecto:

``` bash
cd ~/grupo_05_doosan_m0609
```

Para mantener el mismo nombre de workspace utilizado durante el
desarrollo:

``` bash
cd ~
mv grupo_05_doosan_m0609 grupo_05_doosan_m0609_ws
cd ~/grupo_05_doosan_m0609_ws
```

------------------------------------------------------------------------

## 3. Preparar las herramientas necesarias

Actualizar los paquetes:

``` bash
sudo apt update
```

Instalar Git, vcstool y las herramientas de compilación:

``` bash
sudo apt install git python3-vcstool python3-colcon-common-extensions python3-numpy -y
```

Cargar ROS 2 Jazzy:

``` bash
source /opt/ros/jazzy/setup.bash
```

------------------------------------------------------------------------

## 4. Descargar la dependencia de Doosan

El proyecto utiliza `dsr_description2` proveniente del repositorio
oficial de Doosan.

El archivo `dependencias.repos` contiene la versión utilizada durante el
desarrollo.

Desde la raíz del workspace:

``` bash
cd ~/grupo_05_doosan_m0609_ws
```

Importar las dependencias:

``` bash
vcs import src < dependencias.repos
```

Comprobar que exista:

``` text
src/doosan-robot2/
```

y dentro de él:

``` text
src/doosan-robot2/dsr_description2/
```

------------------------------------------------------------------------

## 5. Dar permisos a los scripts

Desde la raíz del workspace:

``` bash
cd ~/grupo_05_doosan_m0609_ws

chmod +x instalar.sh
chmod +x recompilar.sh
chmod +x verificar.sh
chmod +x entorno.sh
```

------------------------------------------------------------------------

## 6. Instalar y compilar el proyecto

Cargar ROS 2:

``` bash
source /opt/ros/jazzy/setup.bash
```

Ejecutar:

``` bash
./instalar.sh
```

El proyecto utiliza una compilación limitada a los paquetes necesarios
para la práctica:

``` bash
colcon build --packages-up-to grupo05_doosan_m0609_bringup m0609_kinematics --symlink-install
```

Si se desea realizar la compilación manualmente:

``` bash
rm -rf build install log

colcon build --packages-up-to grupo05_doosan_m0609_bringup m0609_kinematics --symlink-install
```

------------------------------------------------------------------------

## 7. Configurar el entorno

Después de compilar:

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash
```

También puede utilizarse:

``` bash
source ~/grupo_05_doosan_m0609_ws/entorno.sh
```

------------------------------------------------------------------------

## 8. Verificar la instalación

Desde la raíz del workspace:

``` bash
cd ~/grupo_05_doosan_m0609_ws
./verificar.sh
```

La verificación debe mostrar:

``` text
============================================
 VERIFICACION DEL PROYECTO M0609
============================================

[1] Paquetes propios:
grupo05_doosan_m0609_bringup
m0609_kinematics

[2] Ejecutables de m0609_kinematics:
m0609_kinematics fk_node
m0609_kinematics ik_node

[3] Dependencia Doosan:
dsr_description2

============================================
 VERIFICACION COMPLETADA
============================================
```

------------------------------------------------------------------------

## 9. Ejecutar la visualización del Doosan M0609

Primero cargar el entorno:

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash
```

Ejecutar:

``` bash
ros2 launch grupo05_doosan_m0609_bringup display.launch.py
```

Esto inicia:

-   `robot_state_publisher`
-   `joint_state_publisher_gui`
-   RViz2

El modelo del Doosan M0609 debe aparecer en RViz2.

------------------------------------------------------------------------

## 10. Ejecutar la cinemática directa (FK)

Abrir otra terminal.

Cargar el entorno:

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash
```

Ejecutar:

``` bash
ros2 run m0609_kinematics fk_node
```

El nodo queda esperando mensajes en:

``` text
/joint_states
```

Cuando recibe una configuración articular, calcula la matriz homogénea
`T06` y muestra la posición `X`, `Y` y `Z`.

------------------------------------------------------------------------

## 11. Ejecutar la cinemática inversa (IK)

Abrir otra terminal.

Cargar el entorno:

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash
```

Ejecutar:

``` bash
ros2 run m0609_kinematics ik_node
```

El nodo queda esperando objetivos en:

``` text
/target
```

------------------------------------------------------------------------

## 12. Enviar un objetivo cartesiano

Abrir otra terminal.

Cargar el entorno:

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash
```

Publicar un punto de prueba:

``` bash
ros2 topic pub --once /target geometry_msgs/msg/Point "{x: 0.300, y: -0.250, z: 0.800}"
```

El nodo IK calcula una configuración articular que intenta alcanzar el
objetivo y publica el resultado en:

``` text
/joint_states
```

------------------------------------------------------------------------

## 13. Ejemplo de resultado IK obtenido durante las pruebas

Para:

``` text
X = 0.3000 m
Y = -0.2500 m
Z = 0.8000 m
```

se obtuvo:

``` text
q1 = -0.709824 rad (-40.67 deg)
q2 = -0.065335 rad (-3.74 deg)
q3 =  1.073826 rad ( 61.53 deg)
q4 = -0.042742 rad (-2.45 deg)
q5 =  0.054462 rad ( 3.12 deg)
q6 =  0.000000 rad ( 0.00 deg)
```

Posición alcanzada:

``` text
X = 0.299838 m
Y = -0.249825 m
Z = 0.799664 m
```

Error final:

``` text
0.00041183 m
```

------------------------------------------------------------------------

## 14. Ejemplo adicional de objetivo IK

Durante las pruebas también se utilizó:

``` bash
ros2 topic pub --once /target geometry_msgs/msg/Point "{x: 0.350, y: 0.200, z: 0.650}"
```

Resultado obtenido:

``` text
q1 =  0.501799 rad ( 28.75 deg)
q2 = -0.177244 rad (-10.16 deg)
q3 =  1.478046 rad ( 84.69 deg)
q4 =  0.031795 rad (  1.82 deg)
q5 =  0.169102 rad (  9.69 deg)
q6 =  0.000000 rad (  0.00 deg)
```

Posición alcanzada:

``` text
X = 0.349659 m
Y = 0.199647 m
Z = 0.649413 m
```

Error final:

``` text
0.00076473 m
```

------------------------------------------------------------------------

## 15. Comprobar `/joint_states`

Para conocer los nodos conectados:

``` bash
ros2 topic info /joint_states
```

Para obtener información detallada:

``` bash
ros2 topic info /joint_states -v
```

Para observar los mensajes:

``` bash
ros2 topic echo /joint_states
```

Durante las pruebas se verificó la comunicación entre:

-   `ik_node`
-   `joint_state_publisher_gui`
-   `robot_state_publisher`
-   `fk_node`

------------------------------------------------------------------------

## 16. Flujo completo de prueba

Para reproducir la práctica completa se pueden utilizar varias
terminales.

### Terminal 1 --- Visualización

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash

ros2 launch grupo05_doosan_m0609_bringup display.launch.py
```

### Terminal 2 --- Cinemática directa

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash

ros2 run m0609_kinematics fk_node
```

### Terminal 3 --- Cinemática inversa

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash

ros2 run m0609_kinematics ik_node
```

### Terminal 4 --- Enviar objetivo

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash

ros2 topic pub --once /target geometry_msgs/msg/Point "{x: 0.300, y: -0.250, z: 0.800}"
```

### Terminal 5 --- Observar `/joint_states`

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash

ros2 topic echo /joint_states
```

### Terminal 6 --- Información del tópico

``` bash
source /opt/ros/jazzy/setup.bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash

ros2 topic info /joint_states -v
```

No es obligatorio abrir las seis terminales para una prueba básica. Las
terminales adicionales sirven para observar y verificar la comunicación
entre nodos.

------------------------------------------------------------------------

## 17. Recompilar después de realizar cambios

Si se modifica algún archivo del proyecto:

``` bash
cd ~/grupo_05_doosan_m0609_ws

./recompilar.sh
```

O manualmente:

``` bash
source /opt/ros/jazzy/setup.bash

colcon build --packages-up-to grupo05_doosan_m0609_bringup m0609_kinematics --symlink-install
```

Después:

``` bash
source install/setup.bash
```

------------------------------------------------------------------------

## 18. Estructura principal del proyecto

``` text
grupo_05_doosan_m0609_ws/
├── .gitignore
├── dependencias.repos
├── entorno.sh
├── instalar.sh
├── recompilar.sh
├── requirements.txt
├── verificar.sh
└── src/
    ├── grupo05_doosan_m0609_bringup/
    │   ├── CMakeLists.txt
    │   ├── package.xml
    │   ├── launch/
    │   │   └── display.launch.py
    │   └── rviz/
    │       └── display.rviz
    │
    └── m0609_kinematics/
        ├── package.xml
        ├── setup.py
        ├── setup.cfg
        ├── resource/
        ├── test/
        └── m0609_kinematics/
            ├── __init__.py
            ├── fk_node.py
            └── ik_node.py
```

Las carpetas `build/`, `install/` y `log/` no se incluyen en GitHub
porque son archivos generados durante la compilación.

------------------------------------------------------------------------

## 19. Notas importantes

-   El proyecto utiliza **ROS 2 Jazzy**.
-   El workspace recomendado es `~/grupo_05_doosan_m0609_ws`.
-   No se necesita copiar las carpetas `build`, `install` ni `log` desde
    otra computadora.
-   Después de clonar el repositorio, estas carpetas se generan
    nuevamente mediante `colcon build`.
-   La dependencia de Doosan se recupera mediante `dependencias.repos`.
-   No se requiere el robot físico para realizar las pruebas de FK e IK.
-   Los ángulos articulares se manejan internamente en radianes.
-   Los objetivos cartesianos `X`, `Y` y `Z` se expresan en metros.

------------------------------------------------------------------------

## 20. Repositorio

Repositorio oficial del proyecto:

https://github.com/josechauca-ux/grupo_05_doosan_m0609
