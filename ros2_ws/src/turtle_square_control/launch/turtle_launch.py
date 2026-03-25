import os
import datetime
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, RegisterEventHandler, EmitEvent
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown

def generate_launch_description():
    # 取得當下時間並格式化為字串 (例如: 20260322_153025)
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 組合出帶有時間戳記的資料夾名稱
    bag_folder_name = f'turtle1_status_bag_{current_time}'
    
    # 使用 os.path.expanduser 取得家目錄，並組合成你想要的完整路徑
    bag_path = os.path.join(
        os.path.expanduser('~'), 
        'ros_tutorial', 'ros2_ws', 'src', 'turtle_square_control', 'rosbag' , bag_folder_name
    )

    # 定義各個節點與執行程序
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='sim'
    )

    controller_node = Node(
        package='turtle_square_control', 
        executable='controller',
        name='turtle_controller',
        parameters=[{
            'start_x': 5.0,
            'start_y': 5.0,
            'square_length': 2.5
        }],
        output='screen'
    )

    rqt_plot_node = Node(
        package='rqt_plot',
        executable='rqt_plot',
        name='rqt_plot',
        arguments=['/turtle1/cmd_vel/linear/x', '/turtle1/cmd_vel/angular/z'],
        output='screen'
    )

    rosbag_record = ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-o', bag_path, '/turtle1/cmd_vel', '/turtle1/pose'],
        output='screen'
    )

    # 註冊事件處理器：當 controller_node 結束時，觸發 Shutdown 事件關閉整個 launch
    shutdown_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=controller_node,
            on_exit=[EmitEvent(event=Shutdown())]
        )
    )

    return LaunchDescription([
        turtlesim_node,
        controller_node,
        rqt_plot_node,
        rosbag_record,
        shutdown_handler # 加入事件處理器
    ])
