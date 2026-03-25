import sys  # 新增 sys 模組以便呼叫 sys.exit()
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, TeleportAbsolute, SetPen


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        self.declare_parameter('start_x', 5.0)
        self.declare_parameter('start_y', 5.0)
        self.declare_parameter('square_length', 2.5)

        self.start_x = self.get_parameter('start_x').value
        self.start_y = self.get_parameter('start_y').value
        self.square_length = self.get_parameter('square_length').value

        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)

        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.teleport_client = self.create_client(
            TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')

        self.current_pose = None
        self.state = 'INIT_PEN_OFF'
        self.edges_completed = 0
        self.child_turtles = {}
        self.wait_ticks = 0

        self.waypoints = [
            (self.start_x + self.square_length, self.start_y),
            (self.start_x + self.square_length, self.start_y - self.square_length),
            (self.start_x, self.start_y - self.square_length),
            (self.start_x, self.start_y)
        ]
        self.target_headings = [0.0, -math.pi / 2, math.pi, math.pi / 2]

        self.angular_stop_thresh = 0.005
        self.linear_ramp_dist = 0.3
        self.high_linear_vel = 2.0
        self.low_linear_vel = 0.1

        self.timer = self.create_timer(0.05, self.control_loop)
        self.get_logger().info('Controller started.')

    # ------------------------------------------------------------------ #

    def pose_callback(self, msg):
        self.current_pose = msg

    def normalize_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    # ------------------------------------------------------------------ #
    #  Child turtle setup                                                  #
    # ------------------------------------------------------------------ #

    def setup_child_turtle(self, name, corner_x, corner_y):
        # --- Pen off ---
        pen_client = self.create_client(SetPen, f'/{name}/set_pen')
        if pen_client.wait_for_service(timeout_sec=1.0):
            pen_client.call_async(SetPen.Request(off=1))
        else:
            self.get_logger().warn(f'set_pen service not ready for {name}')

        # --- Publisher / subscriber ---
        pub = self.create_publisher(Twist, f'/{name}/cmd_vel', 10)
        sub = self.create_subscription(
            Pose, f'/{name}/pose',
            lambda msg, n=name: self.child_pose_callback(msg, n),
            10
        )

        # Register entry with movement LOCKED until teleport confirmed
        self.child_turtles[name] = {
            'pub': pub,
            'sub': sub,
            'pose': None,
            'corner_x': float(corner_x),
            'corner_y': float(corner_y),
            'teleported': False,        # ← LOCK
        }

        # --- Teleport to exact corner ---
        teleport_client = self.create_client(
            TeleportAbsolute, f'/{name}/teleport_absolute')
        if teleport_client.wait_for_service(timeout_sec=1.0):
            req = TeleportAbsolute.Request(
                x=float(corner_x),
                y=float(corner_y),
                theta=0.0
            )
            future = teleport_client.call_async(req)
            # UNLOCK only after the service confirms teleport is done
            future.add_done_callback(
                lambda f, n=name: self._on_teleport_done(f, n)
            )
            self.get_logger().info(
                f'{name} teleporting to exact corner '
                f'({corner_x:.3f}, {corner_y:.3f}) — movement locked.')
        else:
            # Fallback: unlock immediately to avoid permanent deadlock
            self.child_turtles[name]['teleported'] = True
            self.get_logger().warn(
                f'teleport_absolute not ready for {name}; '
                f'movement unlocked without positional correction.')

    def _on_teleport_done(self, future, name):
        """Teleport service responded — safe to start navigating."""
        if name in self.child_turtles:
            self.child_turtles[name]['teleported'] = True   # ← UNLOCK
            self.get_logger().info(
                f'{name} teleport confirmed — navigation unlocked.')

    def child_pose_callback(self, msg, name):
        if name in self.child_turtles:
            self.child_turtles[name]['pose'] = msg

    # ------------------------------------------------------------------ #
    #  Child turtle navigation                                             #
    # ------------------------------------------------------------------ #

    def control_children(self):
        for name, data in self.child_turtles.items():
            if name == 'turtle5':
                continue

            # KEY GUARD: skip until teleport is confirmed.
            if not data.get('teleported', False):
                continue

            pose = data['pose']
            if pose is None:
                continue

            dist = math.hypot(self.start_x - pose.x, self.start_y - pose.y)
            desired_h = math.atan2(
                self.start_y - pose.y, self.start_x - pose.x)
            h_err = self.normalize_angle(desired_h - pose.theta)

            cmd = Twist()
            if dist > 0.05:
                cmd.angular.z = 2.0 * h_err
                # Strict heading threshold (0.02 rad) keeps paths straight
                if abs(h_err) > 0.02:
                    cmd.linear.x = 0.0
                else:
                    cmd.linear.x = min(1.5, dist * 1.5)
            else:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0

            data['pub'].publish(cmd)

    # ------------------------------------------------------------------ #
    #  Main control loop                                                   #
    # ------------------------------------------------------------------ #

    def control_loop(self):
        if self.current_pose is None:
            return

        self.control_children()
        cmd = Twist()

        # --- Initialization Phase ---
        if self.state == 'INIT_PEN_OFF':
            if self.pen_client.wait_for_service(timeout_sec=0.1):
                self.pen_client.call_async(SetPen.Request(off=1))
                self.state = 'INIT_TELEPORT'

        elif self.state == 'INIT_TELEPORT':
            if self.teleport_client.wait_for_service(timeout_sec=0.1):
                self.teleport_client.call_async(
                    TeleportAbsolute.Request(
                        x=self.start_x, y=self.start_y, theta=0.0))
                self.state = 'INIT_WAIT'

        elif self.state == 'INIT_WAIT':
            if (abs(self.current_pose.x - self.start_x) < 0.05 and
                    abs(self.current_pose.y - self.start_y) < 0.05):
                self.state = 'INIT_PEN_ON'

        elif self.state == 'INIT_PEN_ON':
            self.pen_client.call_async(
                SetPen.Request(off=0, r=255, g=255, b=255, width=3))
            self.edges_completed = 0
            self.state = 'FORWARD'
            self.get_logger().info(
                'Teleported to start. Beginning square pattern.')

        # --- Linear Movement ---
        elif self.state == 'FORWARD':
            target_x, target_y = self.waypoints[self.edges_completed]

            if self.edges_completed == 0:
                dist_remaining = target_x - self.current_pose.x
            elif self.edges_completed == 1:
                dist_remaining = self.current_pose.y - target_y
            elif self.edges_completed == 2:
                dist_remaining = self.current_pose.x - target_x
            elif self.edges_completed == 3:
                dist_remaining = target_y - self.current_pose.y

            if dist_remaining > 0:
                dist_to_target = math.hypot(
                    target_x - self.current_pose.x,
                    target_y - self.current_pose.y)
                if dist_to_target > 0.05:
                    desired_heading = math.atan2(
                        target_y - self.current_pose.y,
                        target_x - self.current_pose.x)
                else:
                    desired_heading = self.target_headings[self.edges_completed]

                h_err = self.normalize_angle(
                    desired_heading - self.current_pose.theta)
                cmd.angular.z = 2.0 * h_err

                if dist_remaining > self.linear_ramp_dist:
                    cmd.linear.x = self.high_linear_vel
                else:
                    speed_ratio = dist_remaining / self.linear_ramp_dist
                    cmd.linear.x = max(
                        self.low_linear_vel +
                        (self.high_linear_vel - self.low_linear_vel) * speed_ratio,
                        self.low_linear_vel)
            else:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.wait_ticks = 0
                self.state = 'WAIT_STOP_LINEAR'

        # --- Linear Braking / Wait & Absolute Spawning ---
        elif self.state == 'WAIT_STOP_LINEAR':
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.wait_ticks += 1
            if self.wait_ticks >= 5:
                turtle_name = f'turtle{self.edges_completed + 2}'
                target_x, target_y = self.waypoints[self.edges_completed]

                if self.spawn_client.wait_for_service(timeout_sec=1.0):
                    req = Spawn.Request(
                        x=float(target_x),
                        y=float(target_y),
                        theta=float(self.current_pose.theta),
                        name=turtle_name
                    )
                    future = self.spawn_client.call_async(req)
                    future.add_done_callback(
                        lambda f, n=turtle_name, cx=target_x, cy=target_y:
                            self.spawn_done_callback(f, n, cx, cy)
                    )
                    self.state = 'WAITING_FOR_SPAWN'
                    self.get_logger().info(
                        f'Stationary. Spawning {turtle_name} at '
                        f'({target_x:.3f}, {target_y:.3f}).')
                else:
                    self.get_logger().error('Failed to call /spawn service.')

        elif self.state == 'WAITING_FOR_SPAWN':
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        # --- Turning Movement ---
        elif self.state == 'TURN':
            target_heading = self.target_headings[self.edges_completed]
            h_err = self.normalize_angle(
                target_heading - self.current_pose.theta)

            if abs(h_err) > self.angular_stop_thresh:
                cmd.angular.z = 2.5 * h_err
                if cmd.angular.z > 0:
                    cmd.angular.z = max(min(cmd.angular.z, 1.5), 0.1)
                else:
                    cmd.angular.z = min(max(cmd.angular.z, -1.5), -0.1)
            else:
                cmd.angular.z = 0.0
                self.wait_ticks = 0
                self.state = 'WAIT_STOP_ANGULAR'

        # --- Angular Braking / Wait ---
        elif self.state == 'WAIT_STOP_ANGULAR':
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.wait_ticks += 1
            if self.wait_ticks >= 5:
                self.state = 'FORWARD'
                self.get_logger().info(
                    'Rotation stabilized. Proceeding to next edge.')

        # --- Task Completed ---
        elif self.state == 'STOP':
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.cmd_vel_pub.publish(cmd)

    # ------------------------------------------------------------------ #
    #  Spawn callback                                                      #
    # ------------------------------------------------------------------ #

    def spawn_done_callback(self, future, name, corner_x, corner_y):
        self.edges_completed += 1

        if self.edges_completed >= 4:
            self.state = 'STOP'
            self.get_logger().info('Square closed. 5 turtles active. Auto-shutting down launch in 3 seconds...')
            # 設定 3 秒後觸發自我結束
            self.create_timer(3.0, self.shutdown_node)
        else:
            self.setup_child_turtle(name, corner_x, corner_y)
            self.state = 'TURN'
            self.get_logger().info('Spawn successful. Rotating...')

    # ------------------------------------------------------------------ #
    #  Shutdown Function                                                   #
    # ------------------------------------------------------------------ #
    def shutdown_node(self):
        """結束目前 Python 行程，以觸發 launch 的 OnProcessExit"""
        self.get_logger().info('Mission complete. Exiting controller node...')
        sys.exit(0)


# ---------------------------------------------------------------------- #

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except SystemExit:
        # 捕捉 sys.exit() 以確保優雅關閉
        pass
    finally:
        node.destroy_node()
        # 檢查 rclpy 是否已經 shutdown，避免重複 shutdown 產生錯誤
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
