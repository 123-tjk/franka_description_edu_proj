# Dual-arm Franka FR3 visualization (based on visualize_franka.launch.py)
import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.actions import OpaqueFunction
from launch_ros.actions import Node


def robot_state_publisher_spawner(context: LaunchContext):
    xacro_file = os.path.join(
        get_package_share_directory('franka_description'),
        'robots', 'dual_fr3.urdf.xacro',
    )
    robot_description = xacro.process_file(xacro_file).toprettyxml(indent='  ')
    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        )
    ]


def generate_launch_description():
    rviz_file = os.path.join(
        get_package_share_directory('franka_description'),
        'rviz', 'visualize_franka.rviz',
    )
    return LaunchDescription([
        OpaqueFunction(function=robot_state_publisher_spawner, args=[]),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['--display-config', rviz_file],
        ),
    ])