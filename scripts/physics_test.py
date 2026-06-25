#!/usr/bin/env python3

import os
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
package_root = script_dir.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

import time
import rclpy
from rclpy.executors import SingleThreadedExecutor

from python_api.src.za6_robot import ZA6Robot


def main():

    rclpy.init()
    robot = ZA6Robot()
    executor = SingleThreadedExecutor()
    executor.add_node(robot)

    try:
        #
        # Run spin in background execution loop
        #
        import threading
        spin_thread = threading.Thread(
            target=executor.spin,
            daemon=True
        )
        spin_thread.start()

        robot.get_logger().info("Waiting for system to stabilize...")
        time.sleep(1.0)

        scene_path = Path(__file__).parent.parent / "python_api" / "config" / "scene.yaml"
        robot.scene.load_yaml(str(scene_path))
        robot.scene.add_gripper_collider()
        time.sleep(2.0)

        robot.set_speed(0.025)

        # -----------------------------------
        # Start movement
        # -----------------------------------

        # Ungrip
        robot.gripper.open()

        # Ready
        robot.move_joints(
            joint_positions=[0.044, 1.362, 0.504, 0.682, 0.048, -1.940]
        )

        # Apprach
        robot.move_joints(
            joint_positions=[0.0156, 1.3746, 0.482, 0.332, 0.016, -1.626]
        )

        # Grip
        robot.gripper.close()

        # Move up
        robot.move_joints(
            joint_positions=[0.015, 1.082, 0.480, 0.487, 0.017, -1.487]
        )

        # Move over
        robot.move_joints(
            joint_positions=[-0.410, 1.078, 0.528, 0.375, -0.415, -1.380]
        )

        # Go down
        robot.move_joints(
            joint_positions=[-0.407, 1.476, 0.473, 0.112, -0.404, -1.505]
        )

        # Push off
        robot.move_joints(
            joint_positions=[0.581, 1.500, 0.401, -0.070, 0.594, -1.372]
        )

        # Back to middle
        robot.move_joints(
            joint_positions=[-0.018, 1.243, 0.480, 0.342, -0.016, -1.502]
        )

        # Drop
        robot.gripper.open()

        # Return home
        robot.move_joints(
            joint_positions=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        )

        # -----------------------------------
        # End movement
        # -----------------------------------

        time.sleep(2.0)

    finally:

        robot.shutdown()

        executor.shutdown()

        rclpy.shutdown()


if __name__ == "__main__":
    main()