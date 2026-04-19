from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    

    teleop = Node(
        package='rosbot_controller',
        executable='teleop_node', 
        name = 'teleop',
        output = 'screen'
    )

    motor_driver = Node(
        package='rosbot_controller',
        executable='motor_driver_node', 
        name = 'motor_driver'
    )
    return LaunchDescription([
        motor_driver,
        teleop   
    ])