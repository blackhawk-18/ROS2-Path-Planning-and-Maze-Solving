import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from scripts import GazeboRosPaths

def generate_launch_description():
    package_share_dir = get_package_share_directory("maze_bot")
    world_file = os.path.join(package_share_dir, "worlds", "maze_2_with_camera.world")
    urdf_file = os.path.join(package_share_dir, "urdf", "maze_bot.urdf")

    model_path, plugin_path, media_path = GazeboRosPaths.get_paths()
    env = {
        "GAZEBO_MODEL_PATH": model_path,
    }
    return LaunchDescription(
        [
            ExecuteProcess(
                cmd=["gazebo","--verbose",world_file,"-s","libgazebo_ros_factory.so",],
                output="screen",
                additional_env=env,
            ),
            Node(
                package="gazebo_ros",
                executable="spawn_entity.py",
                arguments=["-entity","maze_bot","-b","-file", urdf_file,"-Y","-1.57"
                ],
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                arguments=[urdf_file],
            ),
       
        ]
    )