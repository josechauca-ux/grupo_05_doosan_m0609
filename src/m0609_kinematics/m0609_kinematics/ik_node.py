import math
import numpy as np

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState


class IKNode(Node):

    def __init__(self):
        super().__init__('ik_node')

        # ==========================================================
        # PUBLICADOR
        # ==========================================================

        self.publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        # ==========================================================
        # SUSCRIPTOR AL OBJETIVO
        # ==========================================================

        self.subscription = self.create_subscription(
            Point,
            '/target',
            self.target_callback,
            10
        )

        # ==========================================================
        # CONFIGURACION INICIAL q0
        # ==========================================================

        self.q0 = np.array([
            0.0,
            0.7,
            0.7,
            0.0,
            0.0,
            0.0
        ], dtype=float)

        # ==========================================================
        # LIMITES ARTICULARES
        # ==========================================================

        self.lower_limits = np.array([
            -6.2832,
            -6.2832,
            -2.6180,
            -6.2832,
            -6.2832,
            -6.2832
        ])

        self.upper_limits = np.array([
             6.2832,
             6.2832,
             2.6180,
             6.2832,
             6.2832,
             6.2832
        ])

        # ==========================================================
        # PARAMETROS DEL ALGORITMO
        # ==========================================================

        self.alpha = 0.7
        self.epsilon = 0.001
        self.max_iterations = 300

        # Incremento para Jacobiano numerico
        self.delta = 1e-6

        self.joint_names = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]

        self.get_logger().info(
            '============================================\n'
            '       IK NODE - DOOSAN M0609\n'
            '============================================\n'
            'Esperando objetivos en /target...\n'
        )

    # ==============================================================
    # MATRIZ DH
    # ==============================================================

    def dh_matrix(self, a, d, alpha, theta):

        ct = math.cos(theta)
        st = math.sin(theta)

        ca = math.cos(alpha)
        sa = math.sin(alpha)

        return np.array([
            [ct, -st * ca,  st * sa, a * ct],
            [st,  ct * ca, -ct * sa, a * st],
            [0.0, sa,        ca,       d],
            [0.0, 0.0,       0.0,      1.0]
        ])

    # ==============================================================
    # CINEMATICA DIRECTA
    # ESTA ES LA MISMA FK QUE YA VALIDAMOS
    # ==============================================================

    def forward_kinematics(self, q):

        q1, q2, q3, q4, q5, q6 = q

        A1 = self.dh_matrix(
            0.0,
            0.1345,
            -math.pi / 2,
            q1
        )

        A2 = self.dh_matrix(
            0.411,
            0.0062,
            0.0,
            q2 - math.pi / 2
        )

        A3 = self.dh_matrix(
            0.0,
            0.0,
            math.pi / 2,
            q3 + math.pi / 2
        )

        A4 = self.dh_matrix(
            0.0,
            0.368,
            -math.pi / 2,
            q4
        )

        A5 = self.dh_matrix(
            0.0,
            0.0,
            math.pi / 2,
            q5
        )

        A6 = self.dh_matrix(
            0.0,
            0.121,
            0.0,
            q6
        )

        T01 = A1
        T02 = T01 @ A2
        T03 = T02 @ A3
        T04 = T03 @ A4
        T05 = T04 @ A5
        T06 = T05 @ A6

        return T01, T02, T03, T04, T05, T06

    # ==============================================================
    # POSICION DEL EFECTOR
    # ==============================================================

    def position(self, q):

        _, _, _, _, _, T06 = self.forward_kinematics(q)

        return T06[:3, 3]

    # ==============================================================
    # JACOBIANO POSICIONAL NUMERICO
    # ==============================================================

    def numerical_jacobian(self, q):

        J = np.zeros((3, 6))

        p0 = self.position(q)

        for i in range(6):

            q_delta = q.copy()

            q_delta[i] += self.delta

            p_delta = self.position(q_delta)

            J[:, i] = (p_delta - p0) / self.delta

        return J

    # ==============================================================
    # CINEMATICA INVERSA
    # ==============================================================

    def inverse_kinematics(self, target):

        # ----------------------------------------------------------
        # Empezamos siempre desde q0
        # ----------------------------------------------------------

        q = self.q0.copy()

        for iteration in range(1, self.max_iterations + 1):

            # Posicion actual
            current_position = self.position(q)

            # Error cartesiano
            error = target - current_position

            # Error euclidiano
            error_norm = np.linalg.norm(error)

            # ------------------------------------------------------
            # CRITERIO DE CONVERGENCIA
            # ------------------------------------------------------

            if error_norm < self.epsilon:

                return q, iteration, current_position, error_norm, True

            # ------------------------------------------------------
            # JACOBIANO
            # ------------------------------------------------------

            J = self.numerical_jacobian(q)

            # ------------------------------------------------------
            # PSEUDOINVERSA
            # ------------------------------------------------------

            J_pseudo = np.linalg.pinv(J)

            # ------------------------------------------------------
            # ACTUALIZACION
            #
            # q(k+1) = q(k) + alpha * J+ * e
            # ------------------------------------------------------

            dq = self.alpha * (J_pseudo @ error)

            q = q + dq

            # ------------------------------------------------------
            # APLICAR LIMITES ARTICULARES
            # ------------------------------------------------------

            q = np.clip(
                q,
                self.lower_limits,
                self.upper_limits
            )

        # ==========================================================
        # NO CONVERGIO
        # ==========================================================

        final_position = self.position(q)
        final_error = np.linalg.norm(target - final_position)

        return (
            q,
            self.max_iterations,
            final_position,
            final_error,
            False
        )

    # ==============================================================
    # CALLBACK DEL TARGET
    # ==============================================================

    def target_callback(self, msg):

        target = np.array([
            msg.x,
            msg.y,
            msg.z
        ], dtype=float)

        self.get_logger().info(
            '\n'
            '============================================\n'
            '          NUEVO OBJETIVO IK\n'
            '============================================\n'
            f'Objetivo:\n'
            f'X = {target[0]:.4f} m\n'
            f'Y = {target[1]:.4f} m\n'
            f'Z = {target[2]:.4f} m\n'
            '\n'
            'Configuracion inicial q0:\n'
            f'{np.array2string(self.q0, precision=4)}\n'
        )

        # ==========================================================
        # EJECUTAR IK
        # ==========================================================

        q_solution, iterations, final_position, final_error, converged = \
            self.inverse_kinematics(target)

        # ==========================================================
        # MOSTRAR RESULTADOS
        # ==========================================================

        self.get_logger().info(
            '============================================\n'
            '             RESULTADO IK\n'
            '============================================\n'
            f'Convergencia : {converged}\n'
            f'Iteraciones  : {iterations}\n'
            '\n'
            'Solucion articular:\n'
            f'q1 = {q_solution[0]: .6f} rad '
            f'({math.degrees(q_solution[0]): .2f} deg)\n'
            f'q2 = {q_solution[1]: .6f} rad '
            f'({math.degrees(q_solution[1]): .2f} deg)\n'
            f'q3 = {q_solution[2]: .6f} rad '
            f'({math.degrees(q_solution[2]): .2f} deg)\n'
            f'q4 = {q_solution[3]: .6f} rad '
            f'({math.degrees(q_solution[3]): .2f} deg)\n'
            f'q5 = {q_solution[4]: .6f} rad '
            f'({math.degrees(q_solution[4]): .2f} deg)\n'
            f'q6 = {q_solution[5]: .6f} rad '
            f'({math.degrees(q_solution[5]): .2f} deg)\n'
            '\n'
            'Posicion alcanzada:\n'
            f'X = {final_position[0]:.6f} m\n'
            f'Y = {final_position[1]:.6f} m\n'
            f'Z = {final_position[2]:.6f} m\n'
            '\n'
            f'Error final = {final_error:.8f} m\n'
            '============================================'
        )

        # ==========================================================
        # PUBLICAR SOLUCION
        # ==========================================================

        if converged:

            joint_msg = JointState()

            joint_msg.header.stamp = self.get_clock().now().to_msg()

            joint_msg.name = self.joint_names

            joint_msg.position = q_solution.tolist()

            self.publisher.publish(joint_msg)

            self.get_logger().info(
                'Solucion publicada en /joint_states.'
            )

        else:

            self.get_logger().warn(
                'IK NO CONVERGIO. '
                'No se publica la solucion.'
            )


def main(args=None):

    rclpy.init(args=args)

    node = IKNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
