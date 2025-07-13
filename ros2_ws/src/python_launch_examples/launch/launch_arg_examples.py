from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 宣告兩個 launch arguments：
    #   use_py_talker: bool，決定是否啟動 py_talker
    #   prefix: 傳給 py_talker 的 message_prefix 參數
    use_py_talker_arg = DeclareLaunchArgument(
        'use_py_talker',
        default_value='true',
        description='Whether to launch py_talker node'
    )
    prefix_arg = DeclareLaunchArgument(
        'prefix',
        default_value='Hello from launch args!',
        description='Message prefix parameter for py_talker'
    )

    use_py_talker = LaunchConfiguration('use_py_talker')
    prefix = LaunchConfiguration('prefix')

    # 定義節點，但包在條件中，只有 use_py_talker 是 true 時才啟動
    py_talker_node = Node(
        package='py_pubsub',
        executable='talker',
        name='py_talker_arg',
        output='screen',
        parameters=[{'message_prefix': prefix}]
    )

    return LaunchDescription([
        use_py_talker_arg,
        prefix_arg,
        LogInfo(msg=['use_py_talker = ', use_py_talker]),
        LogInfo(msg=['prefix = ', prefix]),
        # 使用 Python 條件判斷來控制是否加入節點
        # LaunchDescription 不支援 if else 直接加入節點，所以用 Condition 或 Python API 動態控制
        py_talker_node if use_py_talker.perform({}) == 'true' else None
    ])