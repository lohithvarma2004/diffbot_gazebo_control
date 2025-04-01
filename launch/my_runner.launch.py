import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

def generate_launch_description():
    packagename = "diffbot_gazebo_control"
    robotname = "differential_drive_robot"
    modelrelativepath = 'urdf/robot.xacro'
    
    # Path to robot.xacro and process it to get the robot description
    xacro_file = os.path.join(get_package_share_directory(packagename), modelrelativepath)
    robotdescription = xacro.process_file(xacro_file).toxml()
    
    # Path to your custom world file (placed in the urdf folder)
    world_file = os.path.join(get_package_share_directory(packagename), "urdf", "empty_world.world")
    
    # Launch Gazebo with your custom world
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )
    
    # Spawn the robot into Gazebo using the processed robot description
    spawnnode = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=['-topic', 'robot_description', '-entity', robotname],
        output="screen"
    )
    
    # Launch robot_state_publisher to publish the robot description
    statenode = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robotdescription, "use_sim_time": True}],
        output="screen"
    )
    
    # Delay loading controllers to allow the controller manager to fully initialize
    load_joint_state_broadcaster = TimerAction(
        period=3.0,  # Wait for 3 seconds
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
                output="screen"
            )
        ]
    )
    
    load_joint_trajectory_controller = TimerAction(
        period=3.5,  # Wait a bit longer
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'diffbot_effort_controller'],
                output="screen"
            )
        ]
    )
    
    ld = LaunchDescription()
    ld.add_action(gazebo_launch)
    ld.add_action(spawnnode)
    ld.add_action(statenode)
    ld.add_action(load_joint_state_broadcaster)
    ld.add_action(load_joint_trajectory_controller)
    
    return ld
