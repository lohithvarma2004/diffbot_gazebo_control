cmake_minimum_required(VERSION 3.8)
project(mobile_dd_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED) 
find_package(gazebo_ros REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(nav2_msgs REQUIRED)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
install(
  DIRECTORY launch model config
  DESTINATION share/${PROJECT_NAME}
)
add_executable(diff_drive_controller src/diff_drive_controller.cpp)
ament_target_dependencies(diff_drive_controller rclcpp std_msgs geometry_msgs)
# Add your new plugin source file
add_library(rpm_diff_drive_plugin SHARED src/rpm_diff_drive_plugin.cpp)
ament_target_dependencies(rpm_diff_drive_plugin rclcpp gazebo_ros std_msgs nav_msgs)

# Install the plugin library to the 'lib' folder
install(TARGETS rpm_diff_drive_plugin
  LIBRARY DESTINATION lib)

install(TARGETS diff_drive_controller
  DESTINATION lib/${PROJECT_NAME})
install(PROGRAMS
  src/waypoint_navigation.py
  DESTINATION lib/${PROJECT_NAME}
)
install(PROGRAMS
  scripts/butler_manager_nav2.py # Ensure this path is correct
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
