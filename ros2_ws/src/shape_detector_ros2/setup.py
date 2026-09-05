from setuptools import find_packages, setup

package_name = 'shape_detector_ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/shape_detector.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='PennAir shape detection ROS2 package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'video_publisher = shape_detector_ros2.video_publisher_node:main',
            'shape_detector = shape_detector_ros2.shape_detector_node:main',
        ],
    },
)
