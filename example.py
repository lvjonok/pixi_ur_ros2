from crisp_py.robot import make_robot
import numpy as np
import time

robot = make_robot("ur")
robot.wait_until_ready()

print(robot.end_effector_pose)
print(robot.joint_values)

# NOTE: carefully check your available home position and adjust per need
robot.home(np.deg2rad([0, -90, -90, -180, -90, 0]))

# Try move_to
robot.controller_switcher_client.switch_controller("cartesian_impedance_controller")

homing_pose = robot.end_effector_pose.copy()
# Let center be 10 cm above the current position
center_position = homing_pose.position.copy()
center_position[2] += 0.1

robot.move_to(center_position, speed=0.15)
# sleep and go back to home
time.sleep(2)
robot.move_to(homing_pose.position, speed=0.15)

# Try joint movements
robot.controller_switcher_client.switch_controller("joint_impedance_controller")
home_joints = robot.joint_values.copy()
# Make a small move in joint space
target_joints = home_joints.copy()
target_joints[0] += np.deg2rad(5)  # Move the first joint by 10 degrees
robot.set_target_joint(target_joints)
time.sleep(2)
# Go back to home
robot.set_target_joint(home_joints)
time.sleep(2)

robot.shutdown()
