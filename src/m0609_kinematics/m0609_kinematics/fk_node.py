import math
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class FKNode(Node):

    def __init__(self):
        super().__init__('fk_node')

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.get_logger().info('FK Node iniciado. Esperando /joint_states...')

        self.last_q = None

    def dh_matrix(self, a, d, alpha, theta):
        """
        Matriz DH estándar:

        A_i^(i-1) =
        Rz(theta) Tz(d) Tx(a) Rx(alpha)
        """

        ct = math.cos(theta)
        st = math.sin(theta)

        ca = math.cos(alpha)
        sa = math.sin(alpha)

        return np.array([
            [ct, -st * ca,  st * sa, a * ct],
            [st,  ct * ca, -ct * sa, a * st],
            [0.0, sa,        ca,       d],
            [0.0, 0.0,       0.0,       1.0]
        ])

    def forward_kinematics(self, q):

        q1, q2, q3, q4, q5, q6 = q

        # ==========================================
        # DH M0609
        # ==========================================

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

        # ==========================================
        # CINEMÁTICA DIRECTA
        # ==========================================

        T01 = A1
        T02 = T01 @ A2
        T03 = T02 @ A3
        T04 = T03 @ A4
        T05 = T04 @ A5
        T06 = T05 @ A6

        return T01, T02, T03, T04, T05, T06

    def joint_state_callback(self, msg):

        required_joints = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]

        positions = {}

        for name, position in zip(msg.name, msg.position):
            positions[name] = position

        if not all(joint in positions for joint in required_joints):
            return

        q = np.array([
            positions['joint_1'],
            positions['joint_2'],
            positions['joint_3'],
            positions['joint_4'],
            positions['joint_5'],
            positions['joint_6']
        ])

        # Evitar imprimir exactamente lo mismo continuamente
        if self.last_q is not None:
            if np.max(np.abs(q - self.last_q)) < 1e-5:
                return

        self.last_q = q.copy()

        _, _, _, _, _, T06 = self.forward_kinematics(q)

        x = T06[0, 3]
        y = T06[1, 3]
        z = T06[2, 3]

        self.get_logger().info(
            '\n'
            '============================================\n'
            '        CINEMATICA DIRECTA - M0609\n'
            '============================================\n'
            f'q1 = {q[0]: .4f} rad ({math.degrees(q[0]): .2f} deg)\n'
            f'q2 = {q[1]: .4f} rad ({math.degrees(q[1]): .2f} deg)\n'
            f'q3 = {q[2]: .4f} rad ({math.degrees(q[2]): .2f} deg)\n'
            f'q4 = {q[3]: .4f} rad ({math.degrees(q[3]): .2f} deg)\n'
            f'q5 = {q[4]: .4f} rad ({math.degrees(q[4]): .2f} deg)\n'
            f'q6 = {q[5]: .4f} rad ({math.degrees(q[5]): .2f} deg)\n'
            '\n'
            'T06 =\n'
            f'{np.array2string(T06, precision=4, suppress_small=True)}\n'
            '\n'
            f'Posición:\n'
            f'X = {x:.4f} m\n'
            f'Y = {y:.4f} m\n'
            f'Z = {z:.4f} m\n'
            '============================================'
        )


def main(args=None):

    rclpy.init(args=args)

    node = FKNode()

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
