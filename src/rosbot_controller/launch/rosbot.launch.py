from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    

    teleop = Node(
        package='rosbot_controller',
        executable='teleop_node', 
        name = 'teleop',
        output = 'screen'
    )

    cmd_vel = Node(
        package='rosbot_controller',
        executable='cmd_vel_node',
        name = 'cmd_vel'
    )

    motor_driver = Node(
        package='rosbot_controller',
        executable='motor_driver_node', 
        name = 'motor_driver'
    )
    return LaunchDescription([
        motor_driver,
        teleop,
        cmd_vel    
    ])