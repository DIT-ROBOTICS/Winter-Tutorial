from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cpp_pubsub',
            executable='talker',
            name='cpp_talker_param',
            parameters=['config/pub_params.yaml'], #參數採用config資料夾中的pub_params.yaml
            output='screen'
        ),
        Node(
            package='py_pubsub',
            executable='talker',
            name='py_talker_param',
            parameters=['config/pub_params.yaml'], #參數採用config資料夾中的pub_params.yaml
            output='screen'
        )
    ])