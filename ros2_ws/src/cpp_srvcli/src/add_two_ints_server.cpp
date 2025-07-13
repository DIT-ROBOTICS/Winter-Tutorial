#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using AddTwoInts = example_interfaces::srv::AddTwoInts;
using std::placeholders::_1;
using std::placeholders::_2;

class AddTwoIntsServer : public rclcpp::Node {
public:
		// 建構子, Node名稱叫做"add_two_ints_server"
    AddTwoIntsServer() : Node("add_two_ints_server") {
		    // 建立 Service 通訊
		    // 第一個參數是名稱（跟Topic一樣）, 第二個是bind函式，裡面放要運行的函式，後面照著打就好
        service_ = create_service<AddTwoInts>(
        "add_two_ints", std::bind(&AddTwoIntsServer::handle_add, this, _1, _2));
    }

private:
    // ()裡面就是固定格式
    // <>裡面放 Service 用的 interface，也就是定義通訊雙方的資料格式，可以看下方補充
    void handle_add(const std::shared_ptr<AddTwoInts::Request> request,
                    std::shared_ptr<AddTwoInts::Response> response) {
        response->sum = request->a + request->b;
        RCLCPP_INFO(this->get_logger(), "Received: %ld + %ld", request->a, request->b);
    }

    rclcpp::Service<AddTwoInts>::SharedPtr service_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<AddTwoIntsServer>());
    rclcpp::shutdown();
    return 0;
}