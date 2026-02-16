from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ur_type_arg = DeclareLaunchArgument(
        "ur_type",
        default_value="ur16e",
        description="Type/series of used UR robot.",
        choices=[
            "ur3", "ur3e", "ur5", "ur5e",
            "ur10", "ur10e", "ur16e", "ur20", "ur30",
        ],
    )

    robot_ip_arg = DeclareLaunchArgument(
        "robot_ip",
        default_value="192.168.56.101",
        description="IP address by which the robot can be reached.",
    )

    use_fake_hardware_arg = DeclareLaunchArgument(
        "use_fake_hardware",
        default_value="false",
        description="Start robot with fake hardware mirroring command to its states.",
    )

    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="false",
        description="Start RViz for visualization.",
    )

    ur_type = LaunchConfiguration("ur_type")
    robot_ip = LaunchConfiguration("robot_ip")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    use_rviz = LaunchConfiguration("use_rviz")

    ur_robot_driver_path = FindPackageShare("ur_robot_driver")

    controllers_file = PathJoinSubstitution(
        [FindPackageShare("crisp_ur_bringup"), "config", "ur_controllers.yaml"]
    )

    ur_control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [ur_robot_driver_path, "launch", "ur_control.launch.py"]
            )
        ),
        launch_arguments={
            "ur_type": ur_type,
            "robot_ip": robot_ip,
            "use_mock_hardware": use_fake_hardware,
            "controllers_file": controllers_file,
            "launch_rviz": use_rviz,
            "initial_joint_controller": "scaled_joint_trajectory_controller",
            "headless_mode": "true",
        }.items(),
    )

    crisp_broadcasters_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "--controller-manager", "/controller_manager",
            "twist_broadcaster", "pose_broadcaster",
        ],
        output="screen",
    )

    crisp_controllers_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "--controller-manager", "/controller_manager",
            "--inactive",
            "gravity_compensation",
            "cartesian_impedance_controller",
            "joint_impedance_controller",
        ],
        output="screen",
    )

    return LaunchDescription([
        ur_type_arg,
        robot_ip_arg,
        use_fake_hardware_arg,
        use_rviz_arg,
        ur_control,
        crisp_broadcasters_spawner,
        crisp_controllers_spawner,
    ])
