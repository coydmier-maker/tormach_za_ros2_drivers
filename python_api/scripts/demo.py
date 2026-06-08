#!/usr/bin/env python3

import time
import rclpy
from rclpy.executors import SingleThreadedExecutor
from pathlib import Path

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

        #
        # Move robot to home
        #
        robot.home()

        #
        # Load collision scene
        #
        
        scene_path = Path(__file__).parent.parent / "config" / "scene.yaml"
        robot.scene.load_yaml(str(scene_path))
        
        #
        # Small pause so planning scene updates propagate
        #
        time.sleep(1.0)

        #
        # Example pose motion
        #

        robot.set_speed(0.025)
        robot.move_to_named_pose("tall")

        time.sleep(2.0)

        robot.set_speed(1.0)
        robot.move_to_named_pose("meltio")

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