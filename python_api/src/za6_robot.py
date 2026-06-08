#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from pymoveit2 import MoveIt2

from .scene_manager import SceneManager

import yaml

from pathlib import Path

from .gripper import Gripper

class ZA6Robot(Node):

    def __init__(self):

        super().__init__("za6_robot")

        # -------------------------
        # Robot configuration
        # -------------------------

        self.joint_names = [
            "joint_1",
            "joint_2",
            "joint_6",
            "joint_3",
            "joint_4",
            "joint_5",
        ]

        self.base_link_name = "base_link"
        self.end_effector_name = "tool0"
        self.group_name = "manipulator"

        self.gripper = Gripper(self)
        
        # Load poses.yaml from the package config directory

        poses_path = Path(__file__).parent.parent / "config" / "poses.yaml"

        with open(poses_path, "r") as f:
            self.poses = yaml.safe_load(f)["poses"]

        # -------------------------
        # MoveIt interface
        # -------------------------

        self.moveit2 = MoveIt2(
            node=self,
            joint_names=self.joint_names,
            base_link_name=self.base_link_name,
            end_effector_name=self.end_effector_name,
            group_name=self.group_name,
        )

        # -------------------------
        # Scene manager
        # -------------------------

        self.scene = SceneManager(
            node=self,
            base_frame=self.base_link_name,
        )

    # -------------------------
    # Joint-space motion
    # -------------------------

    def move_joints(self, joint_positions):

        self.get_logger().info(
            f"Moving to joints: {joint_positions}"
        )

        self.moveit2.move_to_configuration(joint_positions)

        self.moveit2.wait_until_executed()

    # -------------------------
    # Pose-space motion
    # -------------------------

    def move_pose(self, position, quat_xyzw, cartesian=False):

        self.get_logger().info(
            f"Moving to pose: {position}"
        )

        self.moveit2.move_to_pose(
            position=position,
            quat_xyzw=quat_xyzw,
            cartesian=cartesian,
        )

        self.moveit2.wait_until_executed()

    '''
    def move_pose_xyz_rpy(
        self,
        x,
        y,
        z,
        roll,
        pitch,
        yaw,
    ):

        quat = quaternion_from_euler(
            roll,
            pitch,
            yaw,
        )

        self.move_pose(
            position=[x, y, z],
            quat_xyzw=[
                quat[0],
                quat[1],
                quat[2],
                quat[3],
            ],
        )
    '''

    # -------------------------
    # Change speed
    # -------------------------

    def set_speed(self, scale):

        self.moveit2.max_velocity = scale
        self.moveit2.max_acceleration = scale

    # -------------------------
    # Convenience motions
    # -------------------------

    def home(self):

        joint_positions = [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]

        self.get_logger().info(
            f"HOME COMMAND: {joint_positions}"
        )

        self.move_joints(joint_positions)

    def move_to_named_pose(self, name, cartesian=False):

        if name not in self.poses:
            raise ValueError(f"Unknown pose: {name}")

        pose = self.poses[name]

        pose_type = pose["type"]

        if pose_type == "joints":

            self.get_logger().info(f"[POSE] Joint-space: {name}")

            self.move_joints(pose["values"])

        elif pose_type == "pose":

            self.get_logger().info(f"[POSE] Cartesian: {name}")

            self.move_pose(
                position=pose["position"],
                quat_xyzw=pose["orientation"],
                cartesian=cartesian
            )

        else:
            raise ValueError(f"Unknown pose type: {pose_type}")

    # -------------------------
    # Cleanup
    # -------------------------

    def shutdown(self):
        self.destroy_node()