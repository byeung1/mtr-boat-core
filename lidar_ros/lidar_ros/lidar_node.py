import rclpy
from rclpy.node import Node

from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2

class LidarNode(Node):
	def __init__(self):
		super().__init__("lidar_node")

		self.subscription = self.create_subscription(
			PointCloud2,
			"/lidar/points",
			self.pointcloud_callback,
			qos_profile_sensor_data,
		)

		self.get_logger().info("LiDAR node started")
		self.get_logger().info("Waiting for PointCloud2 on /lidar/points...")

	def pointcloud_callback(self, msg): #turn the result into a list
		points = list(
			point_cloud2.read_points(
				msg,
				field_names=("x", "y", "z"),
				skip_nans=True,
			)
		)

		self.get_logger().info(f"Received point cloud with{len(points)}")

		#only print 5 poitns
		for i, point in enumerate(points[:5]):#only inspect 5 points
			x = float(point[0])
			y = float(point[1])
			z = float(point[2])

			self.get_logger().info(f"Point {i}: x={x:.3f} m, y={y:.3f} m, z={z:.3f} m" )

def main(args=None):
	rclpy.init(args=args)

	node = LidarNode()

	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	finally:
		node.destroy_node()
		rclpy.shutdown()

if __name__ == "__main__":
	main()

