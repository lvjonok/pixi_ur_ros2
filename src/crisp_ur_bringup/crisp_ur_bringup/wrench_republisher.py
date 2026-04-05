#!/usr/bin/env python3
"""Republish F/T sensor wrench with bias removal, dead zone, and moving average.

Records the first N samples to compute a bias, then republishes
filtered, bias-subtracted wrench on /ft_sensor_unbiased.
"""

import numpy as np
import rclpy
from collections import deque
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, qos_profile_system_default
from geometry_msgs.msg import WrenchStamped

FORCE_DEAD_ZONE = 5.0   # N
TORQUE_DEAD_ZONE = 1.0  # Nm
MA_WINDOW_SIZE = 15     # moving average window


class WrenchRepublisher(Node):
    def __init__(self, n_bias_samples: int = 10):
        super().__init__("wrench_republisher")

        self._n_bias_samples = n_bias_samples
        self._bias_samples: list[np.ndarray] = []
        self._bias: np.ndarray | None = None
        self._ma_buffer: deque[np.ndarray] = deque(maxlen=MA_WINDOW_SIZE)

        self._sub = self.create_subscription(
            WrenchStamped,
            "/force_torque_sensor_broadcaster/wrench",
            self._callback,
            qos_profile_sensor_data,
        )
        self._pub = self.create_publisher(
            WrenchStamped,
            "/ft_sensor_unbiased",
            qos_profile_system_default,
        )
        self.get_logger().info(
            f"Collecting {n_bias_samples} samples for bias calibration..."
        )

    def _callback(self, msg: WrenchStamped):
        w = msg.wrench
        sample = np.array([w.force.x, w.force.y, w.force.z,
                           w.torque.x, w.torque.y, w.torque.z])

        # Collect bias samples
        if self._bias is None:
            self._bias_samples.append(sample)
            if len(self._bias_samples) >= self._n_bias_samples:
                self._bias = np.mean(self._bias_samples, axis=0)
                self.get_logger().info(
                    f"Bias computed: force=[{self._bias[0]:.2f}, {self._bias[1]:.2f}, {self._bias[2]:.2f}] "
                    f"torque=[{self._bias[3]:.2f}, {self._bias[4]:.2f}, {self._bias[5]:.2f}]"
                )
            return

        # Subtract bias
        unbiased = sample - self._bias

        # Moving average filter
        self._ma_buffer.append(unbiased)
        filtered = np.mean(self._ma_buffer, axis=0)

        # Dead zone (applied after filtering)
        for i in range(3):
            if abs(filtered[i]) < FORCE_DEAD_ZONE:
                filtered[i] = 0.0
        for i in range(3, 6):
            if abs(filtered[i]) < TORQUE_DEAD_ZONE:
                filtered[i] = 0.0

        out = WrenchStamped()
        out.header = msg.header
        out.wrench.force.x = filtered[0]
        out.wrench.force.y = filtered[1]
        out.wrench.force.z = filtered[2]
        out.wrench.torque.x = filtered[3]
        out.wrench.torque.y = filtered[4]
        out.wrench.torque.z = filtered[5]

        self._pub.publish(out)


def main():
    rclpy.init(signal_handler_options=rclpy.SignalHandlerOptions.NO)
    node = WrenchRepublisher(n_bias_samples=10)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
