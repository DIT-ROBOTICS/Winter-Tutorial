import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsServer(Node):
		# 初始化
    def __init__(self):
        # 'add_two_ints_server' 為 Node名稱，其他照著打
        super().__init__('add_two_ints_server')
        # 建立 Service 端，參數分別為：
        # (使用的interface(資料格式), Service名稱, 要運行的函式)，可以看一下C++版本對照一下
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.handle_add)

    def handle_add(self, request, response):
        self.get_logger().info(f"Received request: {request.a} + {request.b}")
        response.sum = request.a + request.b
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()