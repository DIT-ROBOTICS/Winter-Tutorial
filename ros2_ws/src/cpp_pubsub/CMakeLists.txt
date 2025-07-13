cmake_minimum_required(VERSION 3.8)
project(cpp_pubsub)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Add executables
add_executable(talker src/publisher_member_function.cpp) # 將"src/publisher_member_function.cpp"這個檔案命名為"talker"的可執行目標(executable target)，並加入編譯列表
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/subscriber_member_function.cpp) # 將"src/publisher_member_function.cpp"這個檔案命名為"listener"的可執行目標(executable target)，並加入編譯列表
ament_target_dependencies(listener rclcpp std_msgs)

# Install executables
install(TARGETS
  talker
  listener
  DESTINATION lib/${PROJECT_NAME})

ament_package()
