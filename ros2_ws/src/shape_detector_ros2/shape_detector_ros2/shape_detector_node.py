import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
from .tracker import tracker

class ShapeTrackerNode(Node):
    def __init__(self):
        super().__init__('shape_tracker_node')
        self.cv_bridge = CvBridge()
        self.image_sub = self.create_subscription(Image, 'camera/image_raw', self.on_image, 10)
        self.marker_pub = self.create_publisher(MarkerArray, 'shape_detections', 10)

    def on_image(self, image_msg):
        bgr_frame = self.cv_bridge.imgmsg_to_cv2(image_msg, desired_encoding='bgr8')
        found_shapes = tracker(bgr_frame)

        markers = MarkerArray()
        for idx, shape in enumerate(found_shapes):
            m = Marker()
            m.header = image_msg.header
            m.ns = 'shapes'
            m.id = idx
            m.type = Marker.LINE_STRIP
            m.action = Marker.ADD
            m.scale.x = 0.01
            m.color.g = 1.0
            m.color.a = 1.0
            m.pose.position = Point(x=shape['position'][0], y=shape['position'][1], z=shape['position'][2])
            m.points = [Point(x=float(px), y=float(py), z=0.0) for (px, py) in shape['outline']]
            markers.markers.append(m)

        self.marker_pub.publish(markers)

def main():
    rclpy.init()
    node = ShapeTrackerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()