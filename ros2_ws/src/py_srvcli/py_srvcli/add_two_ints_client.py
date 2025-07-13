import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        # 建立 Client 端，參數分別為：
        # (使用的interface(資料格式), Service名稱)
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        self.send_request()

    def send_request(self):
        req = AddTwoInts.Request()
        req.a = 3
        req.b = 5
        # 發送 request
        future = self.client.call_async(req)
        # 等待 Server 端回傳資料
        rclpy.spin_until_future_complete(self, future)
        if future.result():
            self.get_logger().info(f'Result: {future.result().sum}')

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClient()
    rclpy.shutdown()

if __name__ == '__main__':
    main()