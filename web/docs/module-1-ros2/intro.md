# Module 1: ROS 2

This module covers the fundamentals of ROS 2, including nodes, topics, services, and URDF.

## 1.1 Introduction to ROS 2

Robot Operating System 2 (ROS 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

### Key Concepts:

*   **Nodes**: Executable processes that perform computation.
*   **Topics**: Named buses over which nodes exchange messages.
*   **Services**: Request/reply communication mechanisms.
*   **Actions**: Long-running tasks with feedback and cancellability.

## 1.2 Understanding ROS 2 Nodes

Nodes are the fundamental building blocks of a ROS 2 system. Each node is designed to perform a specific task, such as controlling a motor, reading sensor data, or performing path planning.

### Creating a Simple Node:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 1.3 ROS 2 Topics and Communication

Topics are the most common way for nodes to communicate with each other. A node publishes messages to a topic, and other nodes can subscribe to that topic to receive those messages. This asynchronous communication model allows for flexible and decoupled systems.

## 1.4 URDF for Robot Description

Unified Robot Description Format (URDF) is an XML format for describing all aspects of a robot. It's used in ROS 2 for visualizing robots, simulating them, and even for controlling them.

### Example URDF Structure:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.6 0.4 0.2"/>
      </geometry>
    </visual>
  </link>
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <axis xyz="0 1 0"/>
  </joint>
  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </visual>
  </link>
</robot>
```