#!/usr/bin/env python3

import time
from pathlib import Path
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

        #
        # Give ROS time to initialize
        #
        robot.get_logger().info("Waiting for system to stabilize...")
        time.sleep(1.0)

        scene_path = Path(__file__).resolve().parent.parent / "python_api" / "config" / "scene.yaml"
        robot.scene.load_yaml(str(scene_path))
        
        time.sleep(2.0)

        robot.set_speed(0.025)

        robot.move_to_named_pose("preparing", cartesian=True)
        time.sleep(1.0)
        robot.move_to_named_pose("pickUp", cartesian=True)
        #
        # Wait for completion
        #
        time.sleep(2.0)

    finally:

        robot.shutdown()

        executor.shutdown()

        rclpy.shutdown()


if __name__ == "__main__":
    main()