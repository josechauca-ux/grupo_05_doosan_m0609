# Primer Parcial Práctico - Doosan M0609

## IMT-342 Robótica Chauca

Proyecto de ROS 2 para la visualización y estudio cinemático del robot industrial **Doosan M0609**.

El proyecto incluye:

- Modelo URDF del Doosan M0609 mediante `dsr_description2`.
- Visualización en RViz2.
- Transformaciones TF.
- Cinemática directa (FK).
- Cinemática inversa numérica (IK).
- Publicación y lectura de `/joint_states`.
- Objetivos cartesianos mediante `/target`.
- Scripts para instalación, compilación y verificación.
- Archivo `dependencias.repos` para recuperar la dependencia externa de Doosan.

---

# 1. Requisitos

El proyecto fue desarrollado y probado con:

- Ubuntu 24.04
- ROS 2 Jazzy
- Python 3
- Git
- NumPy
- Colcon
- RViz2
- `vcstool`

No se necesita el robot físico para realizar las pruebas de visualización, FK e IK.

> **Importante:** el proyecto está pensado para Ubuntu 24.04 con ROS 2 Jazzy.

---

# 2. Descargar el proyecto

Hay dos formas de obtenerlo. Se recomienda utilizar Git.

## Opción A: clonar desde GitHub

Abrir una terminal y ejecutar:

```bash
cd ~
git clone https://github.com/josechauca-ux/grupo_05_doosan_m0609.git
cd ~/grupo_05_doosan_m0609
```

A partir de este punto, esta carpeta será la raíz del proyecto.

## Opción B: descargar el ZIP

Si se descarga el proyecto desde GitHub como ZIP:

1. Descomprimir el archivo.
2. Entrar a la carpeta que se creó.
3. Comprobar la ubicación con:

```bash
pwd
```

Por ejemplo, si la carpeta quedó como:

```text
/home/danny/grupo_05_doosan_m0609-main
```

entonces se debe trabajar dentro de esa carpeta.

> **Importante:** no es necesario cambiar el nombre de la carpeta. En los pasos siguientes se recomienda utilizar `cd` hasta la carpeta del proyecto y después trabajar con rutas relativas como `source install/setup.bash`. De esta manera no importa si la carpeta se llama `grupo_05_doosan_m0609` o `grupo_05_doosan_m0609-main`.

---

# 3. Entrar siempre a la raíz del proyecto

Antes de ejecutar cualquiera de los scripts, comprobar que estamos en la carpeta que contiene:

```text
dependencias.repos
entorno.sh
instalar.sh
recompilar.sh
requirements.txt
src/
verificar.sh
```

Ejecutar:

```bash
cd ~/grupo_05_doosan_m0609
ls
```

Si se descargó como ZIP y la carpeta tiene otro nombre, utilizar la ruta correspondiente. Por ejemplo:

```bash
cd ~/grupo_05_doosan_m0609-main
ls
```

---

# 4. Preparar ROS 2 Jazzy

Antes de trabajar con el proyecto, cargar ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Comprobar que ROS 2 está disponible:

```bash
ros2 --version
```

Si el comando `source` aparece con caracteres extraños como:

```text
^[[200~
```

no copiar esos caracteres. Escribir manualmente:

```bash
source /opt/ros/jazzy/setup.bash
```

---

# 5. Instalar las herramientas necesarias

Desde la raíz del proyecto:

```bash
sudo apt update
```

Después:

```bash
sudo apt install git python3-vcstool python3-colcon-common-extensions python3-numpy -y
```

Cargar nuevamente ROS 2 si es necesario:

```bash
source /opt/ros/jazzy/setup.bash
```

---

# 6. Dar permisos a los scripts

Desde la raíz del proyecto:

```bash
chmod +x instalar.sh
chmod +x recompilar.sh
chmod +x verificar.sh
chmod +x entorno.sh
```

---

# 7. Instalar el proyecto

Desde la raíz del proyecto:

```bash
./instalar.sh
```

El script realiza automáticamente las principales tareas de instalación:

1. Instala las herramientas necesarias.
2. Recupera la dependencia externa de Doosan.
3. Instala las dependencias ROS que puede resolver.
4. Compila los paquetes necesarios para la práctica.
5. Prepara el entorno.

Al terminar correctamente debe aparecer:

```text
============================================
 INSTALACION COMPLETADA
============================================
```

---

# 8. Si aparece un error de Internet durante `rosdep`

Durante una instalación puede aparecer un mensaje parecido a:

```text
Temporary failure in name resolution
```

o:

```text
unable to process source
https://raw.githubusercontent.com/ros/rosdistro/...
```

Esto indica un problema temporal de conexión o resolución DNS, no necesariamente un problema del proyecto.

Primero comprobar la conexión:

```bash
ping -c 3 raw.githubusercontent.com
```

Si la conexión funciona, volver a ejecutar:

```bash
./instalar.sh
```

En una de las pruebas del proyecto, el primer intento mostró un error de resolución DNS y al volver a ejecutar la instalación las fuentes de `rosdep` se descargaron correctamente.

---

# 9. Si aparece `gazebo_ros` en rosdep

Durante la instalación también puede aparecer:

```text
Cannot locate rosdep definition for [gazebo_ros]
```

Esto puede aparecer porque el repositorio externo de Doosan contiene paquetes relacionados con Gazebo que no son necesarios para esta práctica.

El proyecto que desarrollamos utiliza los paquetes necesarios para:

- `dsr_description2`
- `grupo05_doosan_m0609_bringup`
- `m0609_kinematics`

Si el script continúa y termina con:

```text
[4/5] Compilando workspace...
```

y posteriormente:

```text
Summary: 3 packages finished
```

la instalación de nuestro proyecto se realizó correctamente.

No es necesario instalar Gazebo para realizar las pruebas de FK e IK del proyecto.

---

# 10. Verificar que la compilación terminó correctamente

Desde la raíz del proyecto:

```bash
ls
```

Después de una compilación correcta deben existir, entre otras:

```text
build/
install/
log/
src/
```

También se puede ejecutar:

```bash
./verificar.sh
```

La verificación debe mostrar:

```text
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

---

# 11. Configurar el entorno después de compilar

Este punto es importante.

**No asumir que el workspace se llama `grupo_05_doosan_m0609_ws`.**

El nombre depende de cómo se haya descargado el proyecto.

Por eso, estando dentro de la raíz del proyecto, utilizar:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

También se puede utilizar:

```bash
source ./entorno.sh
```

El archivo `entorno.sh` está preparado para cargar el workspace utilizado durante el desarrollo.

> **Importante:** si se descargó el proyecto como ZIP y la carpeta se llama `grupo_05_doosan_m0609-main`, NO ejecutar:
>
> ```bash
> source ~/grupo_05_doosan_m0609_ws/install/setup.bash
> ```
>
> a menos que realmente exista una carpeta con ese nombre.
>
> La forma recomendada es:
>
> ```bash
> cd ~/grupo_05_doosan_m0609-main
> source /opt/ros/jazzy/setup.bash
> source install/setup.bash
> ```

Este fue precisamente el problema que ocurrió al probar el proyecto en otra computadora: la compilación había terminado correctamente, pero se intentó cargar un `install/setup.bash` perteneciente a una ruta que no existía en esa computadora.

---

# 12. Ejecutar la visualización del Doosan M0609

Abrir una terminal.

Entrar a la raíz del proyecto:

```bash
cd ~/grupo_05_doosan_m0609
```

Si se descargó como ZIP:

```bash
cd ~/grupo_05_doosan_m0609-main
```

Cargar el entorno:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Ejecutar:

```bash
ros2 launch grupo05_doosan_m0609_bringup display.launch.py
```

Esto inicia:

- `robot_state_publisher`
- `joint_state_publisher_gui`
- RViz2

El modelo del Doosan M0609 debe aparecer en RViz2.

---

# 13. Ejecutar la Cinemática Directa (FK)

Abrir una segunda terminal.

Entrar a la carpeta del proyecto:

```bash
cd ~/grupo_05_doosan_m0609
```

o, si se descargó como ZIP:

```bash
cd ~/grupo_05_doosan_m0609-main
```

Cargar ROS 2 y el proyecto:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Ejecutar:

```bash
ros2 run m0609_kinematics fk_node
```

El nodo queda esperando mensajes en:

```text
/joint_states
```

Cuando recibe una configuración articular, calcula la transformación homogénea del robot y obtiene la posición del efector final.

---

# 14. Ejecutar la Cinemática Inversa (IK)

Abrir una tercera terminal.

Entrar al proyecto:

```bash
cd ~/grupo_05_doosan_m0609
```

o:

```bash
cd ~/grupo_05_doosan_m0609-main
```

Cargar el entorno:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Ejecutar:

```bash
ros2 run m0609_kinematics ik_node
```

El nodo queda esperando objetivos cartesianos en:

```text
/target
```

---

# 15. Enviar un objetivo cartesiano

Abrir una cuarta terminal.

Entrar al proyecto:

```bash
cd ~/grupo_05_doosan_m0609
```

o:

```bash
cd ~/grupo_05_doosan_m0609-main
```

Cargar el entorno:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Enviar un objetivo:

```bash
ros2 topic pub --once /target geometry_msgs/msg/Point "{x: 0.200, y: 0.150, z: 0.750}"
```

El nodo IK recibe el punto:

```text
X = 0.200 m
Y = 0.150 m
Z = 0.750 m
```

y busca una configuración articular que permita alcanzar ese objetivo.

El resultado se publica mediante:

```text
/joint_states
```

---

# 16. Comprobar `/joint_states`

Para observar los mensajes:

```bash
ros2 topic echo /joint_states
```

Para conocer información del tópico:

```bash
ros2 topic info /joint_states
```

Para obtener información detallada:

```bash
ros2 topic info /joint_states -v
```

---

# 17. Flujo completo de ejecución

Para reproducir la práctica de forma ordenada se pueden utilizar cuatro terminales.

### Terminal 1 — RViz y robot

```bash
cd ~/grupo_05_doosan_m0609
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch grupo05_doosan_m0609_bringup display.launch.py
```

### Terminal 2 — FK

```bash
cd ~/grupo_05_doosan_m0609
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 run m0609_kinematics fk_node
```

### Terminal 3 — IK

```bash
cd ~/grupo_05_doosan_m0609
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 run m0609_kinematics ik_node
```

### Terminal 4 — Objetivo

```bash
cd ~/grupo_05_doosan_m0609
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 topic pub --once /target geometry_msgs/msg/Point "{x: 0.200, y: 0.150, z: 0.750}"
```

Si la carpeta tiene otro nombre, simplemente cambiar el primer `cd`.

Por ejemplo:

```bash
cd ~/grupo_05_doosan_m0609-main
```

---

# 18. ¿Dónde está programado el proyecto?

La programación realizada para la práctica está principalmente dentro de `src/`.

Los archivos más importantes son:

```text
src/
├── m0609_kinematics/
│   ├── m0609_kinematics/
│   │   ├── fk_node.py
│   │   └── ik_node.py
│   ├── package.xml
│   ├── setup.py
│   └── setup.cfg
│
└── grupo05_doosan_m0609_bringup/
    ├── launch/
    │   └── display.launch.py
    ├── rviz/
    │   └── display.rviz
    ├── CMakeLists.txt
    └── package.xml
```

### `fk_node.py`

Contiene el nodo de cinemática directa.

### `ik_node.py`

Contiene el nodo de cinemática inversa numérica.

### `setup.py`

Registra los ejecutables ROS 2:

```text
fk_node
ik_node
```

### `display.launch.py`

Inicia la visualización del robot, `robot_state_publisher`, `joint_state_publisher_gui` y RViz2.

---

# 19. Parámetros Denavit-Hartenberg utilizados

La cinemática directa utiliza la convención D-H estándar.

Los parámetros utilizados para el modelo son:

| i | Articulación | θᵢ | dᵢ (m) | aᵢ (m) | αᵢ |
|---:|---|---|---:|---:|---:|
| 1 | q₁ | q₁ | 0.1345 | 0 | −90° |
| 2 | q₂ | q₂ − 90° | 0.0062 | 0.411 | 0° |
| 3 | q₃ | q₃ + 90° | 0 | 0 | +90° |
| 4 | q₄ | q₄ | 0.368 | 0 | −90° |
| 5 | q₅ | q₅ | 0 | 0 | +90° |
| 6 | q₆ | q₆ | 0.121 | 0 | 0° |

En los cálculos realizados en Python, los ángulos se manejan en radianes:

| i | θᵢ | dᵢ (m) | aᵢ (m) | αᵢ |
|---:|---|---:|---:|---:|
| 1 | q₁ | 0.1345 | 0 | −π/2 |
| 2 | q₂ − π/2 | 0.0062 | 0.411 | 0 |
| 3 | q₃ + π/2 | 0 | 0 | +π/2 |
| 4 | q₄ | 0.368 | 0 | −π/2 |
| 5 | q₅ | 0 | 0 | +π/2 |
| 6 | q₆ | 0.121 | 0 | 0 |

La matriz D-H utilizada es:

```text
        | cosθ   -sinθ cosα    sinθ sinα    a cosθ |
Aᵢ =    | sinθ    cosθ cosα   -cosθ sinα    a sinθ |
        |   0        sinα          cosα          d   |
        |   0          0             0           1   |
```

Y la transformación total se obtiene mediante:

```text
T₀₆ = A₁ A₂ A₃ A₄ A₅ A₆
```

---

# 20. Recompilar después de modificar código

Si se modifica `fk_node.py`, `ik_node.py` o cualquier otro archivo del proyecto:

```bash
cd ~/grupo_05_doosan_m0609
source /opt/ros/jazzy/setup.bash
./recompilar.sh
```

Después de compilar:

```bash
source install/setup.bash
```

También se puede compilar manualmente:

```bash
colcon build --packages-up-to grupo05_doosan_m0609_bringup m0609_kinematics --symlink-install
```

---

# 21. Si algo falla, comprobar primero estas tres cosas

Antes de buscar un problema más complejo, ejecutar:

### 1. Estoy en la carpeta correcta

```bash
pwd
```

Debe mostrar la carpeta donde están:

```text
src/
instalar.sh
recompilar.sh
verificar.sh
```

### 2. ROS 2 está cargado

```bash
source /opt/ros/jazzy/setup.bash
```

### 3. El workspace está cargado

Desde la raíz del proyecto:

```bash
source install/setup.bash
```

Después comprobar:

```bash
ros2 pkg list | grep m0609
```

Debe aparecer:

```text
m0609_kinematics
```

Si aparece, ya se puede ejecutar:

```bash
ros2 run m0609_kinematics fk_node
```

o:

```bash
ros2 run m0609_kinematics ik_node
```

---

# 22. Error común: `Package 'm0609_kinematics' not found`

Si aparece:

```text
Package 'm0609_kinematics' not found
```

primero comprobar que ya se compiló el proyecto:

```bash
ls install
```

Después, desde la raíz del proyecto:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Comprobar:

```bash
ros2 pkg list | grep m0609
```

Si todavía no aparece, recompilar:

```bash
./recompilar.sh
source install/setup.bash
```

Un error frecuente es intentar cargar:

```bash
source ~/grupo_05_doosan_m0609_ws/install/setup.bash
```

cuando la carpeta real tiene otro nombre. Por eso en este README se utiliza:

```bash
source install/setup.bash
```

después de entrar a la raíz real del proyecto.

---

# 23. Error común: `No such file or directory` al cargar `install/setup.bash`

Si aparece:

```text
bash: .../install/setup.bash: No such file or directory
```

comprobar primero:

```bash
pwd
ls
```

Luego entrar a la carpeta correcta y ejecutar:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Si `install/` todavía no existe, ejecutar:

```bash
./instalar.sh
```

y esperar a que termine la compilación.

---

# 24. Carpetas generadas

Las siguientes carpetas se generan automáticamente:

```text
build/
install/
log/
```

No es necesario copiarlas desde otra computadora.

Después de clonar el repositorio se vuelven a generar mediante:

```bash
./instalar.sh
```

Por eso estas carpetas no forman parte del código fuente que se mantiene en GitHub.

---

# 25. Dependencia externa de Doosan

El proyecto no incluye manualmente todo el repositorio de Doosan.

La dependencia se especifica en:

```text
dependencias.repos
```

El archivo indica la versión utilizada durante el desarrollo:

```text
https://github.com/DoosanRobotics/doosan-robot2.git
```

De esta manera, otra computadora puede recuperar automáticamente la dependencia mediante:

```bash
vcs import src < dependencias.repos
```

El script `instalar.sh` realiza este proceso automáticamente.

---

# 26. Resumen rápido para una computadora nueva

Si Ubuntu 24.04 y ROS 2 Jazzy ya están instalados, el procedimiento básico es:

### 1. Clonar

```bash
cd ~
git clone https://github.com/josechauca-ux/grupo_05_doosan_m0609.git
cd ~/grupo_05_doosan_m0609
```

### 2. Cargar ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

### 3. Dar permisos

```bash
chmod +x instalar.sh recompilar.sh verificar.sh entorno.sh
```

### 4. Instalar y compilar

```bash
./instalar.sh
```

### 5. Cargar el proyecto

```bash
source install/setup.bash
```

### 6. Verificar

```bash
./verificar.sh
```

### 7. Abrir RViz

```bash
ros2 launch grupo05_doosan_m0609_bringup display.launch.py
```

### 8. En otra terminal, cargar el entorno

```bash
cd ~/grupo_05_doosan_m0609
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

### 9. Ejecutar FK

```bash
ros2 run m0609_kinematics fk_node
```

### 10. En otra terminal, cargar el entorno y ejecutar IK

```bash
cd ~/grupo_05_doosan_m0609
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run m0609_kinematics ik_node
```

### 11. Enviar un objetivo

```bash
ros2 topic pub --once /target geometry_msgs/msg/Point "{x: 0.200, y: 0.150, z: 0.750}"
```

Con esto se puede reproducir la parte principal de la práctica.

---

# 27. Repositorio

Repositorio del proyecto:

https://github.com/josechauca-ux/grupo_05_doosan_m0609

**IMT-342 Robótica Chauca — Grupo 05**
