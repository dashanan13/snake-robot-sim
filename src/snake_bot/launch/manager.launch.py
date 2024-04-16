import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit



from launch_ros.actions import Node
import xacro


def generate_launch_description():


    # Configure the node


    robot_controller_spawner1 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints1_controllers", "-c", "/controller_manager"],
    )

    robot_controller_spawner2 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints2_controllers", "-c", "/controller_manager"],
    )

    robot_controller_spawner3 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints3_controllers", "-c", "/controller_manager"],
    )

    robot_controller_spawner4 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints4_controllers", "-c", "/controller_manager"],
    )

    robot_controller_spawner5 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints5_controllers", "-c", "/controller_manager"],
    )

    robot_controller_spawner6 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints6_controllers", "-c", "/controller_manager"],
    )

    robot_controller_spawner7 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints7_controllers", "-c", "/controller_manager"],
    )

    robot_controller_spawner8 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints8_controllers", "-c", "/controller_manager"],
    )

    robot_controller_spawner9 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joints9_controllers", "-c", "/controller_manager"],
    )


    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )
    
    


    # Run the node
    return LaunchDescription([
        RegisterEventHandler(
        event_handler= OnProcessExit(
        target_action=joint_state_broadcaster_spawner,
        on_exit = [robot_controller_spawner1,robot_controller_spawner2,robot_controller_spawner3,
                   robot_controller_spawner4,robot_controller_spawner5,robot_controller_spawner6,
                   robot_controller_spawner7,robot_controller_spawner8,robot_controller_spawner9]
        )),
        joint_state_broadcaster_spawner,
        
    ])