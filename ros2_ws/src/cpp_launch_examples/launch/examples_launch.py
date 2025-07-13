from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # C++ Pub-Sub
        Node(package='cpp_pubsub', executable='talker', name='cpp_talker', output='screen'),
        Node(package='cpp_pubsub', executable='listener', name='cpp_listener', output='screen'),

        # Python Pub-Sub
        Node(package='py_pubsub', executable='talker', name='py_talker', output='screen'),
        Node(package='py_pubsub', executable='listener', name='py_listener', output='screen'),

        # C++ Service
        Node(package='cpp_srvcli', executable='add_two_ints_server', name='cpp_srv_server', output='screen'),
        Node(package='cpp_srvcli', executable='add_two_ints_client', name='cpp_srv_client', output='screen'),

        # Python Service
        Node(package='py_srvcli', executable='add_two_ints_server', name='py_srv_server', output='screen'),
        Node(package='py_srvcli', executable='add_two_ints_client', name='py_srv_client', output='screen'),
    ])