cmake_minimum_required(VERSION 3.8)
project(diffbot_gazebo_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(trajectory_msgs REQUIRED)

# Add the joint_publisher executable
add_executable(joint_publisher src/joint_publisher.cpp)
ament_target_dependencies(joint_publisher
  rclcpp
  std_msgs
  geometry_msgs
  trajectory_msgs
)

# Install the executable
install(TARGETS
  joint_publisher
  DESTINATION lib/${PROJECT_NAME}
)

# Install additional directories (launch, urdf, config)
install(DIRECTORY
  launch
  urdf
  config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # Skip cpplint for now (remove or modify as needed)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
