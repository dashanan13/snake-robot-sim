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

    pkg_name = 'snake_bot'
    file_subpath = 'rviz/snake.rviz'

    rviz_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)

    snake_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('snake_bot'), 'launch'), '/wave.launch.py']),
        )
    
    manager_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('snake_bot'), 'launch'), '/manager.launch.py']),
        )
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        arguments=['-d', rviz_file],  # Replace with your package name
        output='screen'
    )

    sensor_node_10sec = Node(
        package='snake_bot',
        executable='sensor10sec',
        name='sensor10sec',
        output='screen'
    )

    sensor_node_altime = Node(
        package='snake_bot',
        executable='sensoralltime',
        name='sensoralltime',
        output='screen'
    )

    sensor_node_contact = Node(
        package='snake_bot',
        executable='sensorcontact',
        name='sensorcontact',
        output='screen'
    )


    # Run the node
    return LaunchDescription([
        snake_launch,
        manager_launch,
        rviz_node,
        #sensor_node_10sec,
        #sensor_node_altime,
        #sensor_node_contact,
    ])