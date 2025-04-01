#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include <vector>
#include <chrono>

using namespace std::chrono_literals;

class JointPublisher : public rclcpp::Node
{
public:
  JointPublisher()
  : Node("joint_publisher")
  {
    // Publisher for effort commands
    publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(
      "/diffbot_effort_controller/commands", 10);

    // Timer to periodically publish efforts
    timer_ = this->create_wall_timer(
      50ms, std::bind(&JointPublisher::publishEfforts, this));

    // Initialize constant effort values
    left_effort_ = 10.0;  // Set your desired constant left effort
    right_effort_ = 10.0; // Set your desired constant right effort
  }

private:
  // Publish the constant efforts on the effort controller command topic.
  void publishEfforts()
  {
    std_msgs::msg::Float64MultiArray msg;
    // Order: [right wheel, left wheel]
    // (Adjust the ordering if your URDF maps joints differently.)
    msg.data = {right_effort_, left_effort_};
    publisher_->publish(msg);
    RCLCPP_DEBUG(this->get_logger(), "Publishing efforts: right=%.2f, left=%.2f", right_effort_, left_effort_);
  }

  // Member variables
  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;

  double left_effort_;
  double right_effort_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<JointPublisher>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}