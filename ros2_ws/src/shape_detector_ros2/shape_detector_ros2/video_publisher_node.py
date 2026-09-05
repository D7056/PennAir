import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class Publisher(Node):
    def __init__(self):
        super().__init__('video_publisher')
        self.publisher = self.create_publisher(Image, 'camera/image_raw', 10)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture('/workspace/imgs/hard_vid.mp4')
        fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.timer = self.create_timer(1.0 / fps, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return
        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()