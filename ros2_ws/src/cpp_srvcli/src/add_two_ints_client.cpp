#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using AddTwoInts = example_interfaces::srv::AddTwoInts;

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    // 創一個名叫 "add_two_ints_client" 的 Node
    auto node = rclcpp::Node::make_shared("add_two_ints_client");
    // 創建一個 "add_two_ints" 這個 Service 的 Client 端
    auto client = node->create_client<AddTwoInts>("add_two_ints");

    while (!client->wait_for_service(std::chrono::seconds(1))) {
        RCLCPP_INFO(node->get_logger(), "Waiting for service...");
    }

    auto request = std::make_shared<AddTwoInts::Request>();
    request->a = 3;
    request->b = 7;
		
		// 發送請求給 Server 端
    auto result = client->async_send_request(request);
    // 等待 Server 端回傳資料
    if (rclcpp::spin_until_future_complete(node, result) == rclcpp::FutureReturnCode::SUCCESS) {
        RCLCPP_INFO(node->get_logger(), "Result: %ld", result.get()->sum);
    } 
    else {
        RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call service add_three_doubles");    // CHANGE
    }
    rclcpp::shutdown();
    return 0;
}