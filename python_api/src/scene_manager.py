#!/usr/bin/env python3

from geometry_msgs.msg import Pose

from moveit_msgs.msg import CollisionObject

from shape_msgs.msg import SolidPrimitive

from moveit_msgs.msg import PlanningScene

from moveit_msgs.srv import ApplyPlanningScene

from rclpy.callback_groups import ReentrantCallbackGroup

import yaml


class SceneManager:

    def __init__(self, node, base_frame="base_link"):

        self.node = node

        self.base_frame = base_frame

        #
        # Planning scene service client
        #

        self.callback_group = ReentrantCallbackGroup()

        self.planning_scene_client = node.create_client(
            ApplyPlanningScene,
            "/apply_planning_scene",
            callback_group=self.callback_group,
        )

        self.node.get_logger().info(
            "Waiting for planning scene service..."
        )

        self.planning_scene_client.wait_for_service()

        self.node.get_logger().info(
            "Planning scene service connected"
        )

    #
    # Add box collision object
    #

    def add_box(
        self,

        name,

        position,

        size,
    ):

        collision_object = CollisionObject()

        collision_object.id = name

        collision_object.header.frame_id = self.base_frame

        #
        # Box geometry
        #

        primitive = SolidPrimitive()

        primitive.type = SolidPrimitive.BOX

        primitive.dimensions = size

        #
        # Pose
        #

        pose = Pose()

        pose.position.x = position[0]
        pose.position.y = position[1]
        pose.position.z = position[2]

        pose.orientation.w = 1.0

        #
        # Add geometry
        #

        collision_object.primitives.append(primitive)

        collision_object.primitive_poses.append(pose)

        collision_object.operation = CollisionObject.ADD

        #
        # Planning scene message
        #

        planning_scene = PlanningScene()

        planning_scene.is_diff = True

        planning_scene.world.collision_objects.append(
            collision_object
        )

        #
        # Service request
        #

        request = ApplyPlanningScene.Request()

        request.scene = planning_scene

        future = self.planning_scene_client.call_async(
            request
        )

        self.node.get_logger().info(
            f"Adding box '{name}'"
        )

        return future

    #
    # Remove object
    #

    def remove_object(self, name):

        collision_object = CollisionObject()

        collision_object.id = name

        collision_object.header.frame_id = self.base_frame

        collision_object.operation = CollisionObject.REMOVE

        planning_scene = PlanningScene()

        planning_scene.is_diff = True

        planning_scene.world.collision_objects.append(
            collision_object
        )

        request = ApplyPlanningScene.Request()

        request.scene = planning_scene

        future = self.planning_scene_client.call_async(
            request
        )

        self.node.get_logger().info(
            f"Removing object '{name}'"
        )

        return future
    
    #
    # Load scene from YAML
    #

    def load_yaml(self, filepath):

        with open(filepath, "r") as f:

            data = yaml.safe_load(f)

        #
        # Boxes
        #

        for box in data.get("boxes", []):

            self.add_box(
                name=box["name"],

                position=[
                    box["position"]["x"],
                    box["position"]["y"],
                    box["position"]["z"],
                ],

                size=[
                    box["size"]["x"],
                    box["size"]["y"],
                    box["size"]["z"],
                ],
            )
