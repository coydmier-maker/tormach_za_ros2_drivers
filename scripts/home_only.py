#!/usr/bin/env python3

import os
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
package_root = script_dir.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

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