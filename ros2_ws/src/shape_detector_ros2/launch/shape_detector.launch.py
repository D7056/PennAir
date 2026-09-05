from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='shape_detector_ros2', executable='video_publisher', name='video_publisher'),
        Node(package='shape_detector_ros2', executable='shape_detector', name='shape_detector'),
    ])
