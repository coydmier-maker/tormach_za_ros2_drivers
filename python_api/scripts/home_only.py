#!/usr/bin/env python3

import rclpy

from python_api.src.za6_robot import ZA6Robot

def main():
    rclpy.init()

    robot = ZA6Robot()

    robot.home()

    rclpy.spin(robot)

    robot.shutdown()

    rclpy.shutdown()


if __name__ == "__main__":
    main()