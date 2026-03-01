# pixi_ur_ros2

ROS 2 Jazzy environment for Universal Robots using [pixi](https://prefix.dev/docs/pixi/overview).

Features:
- **UR16e default** - configurable for all UR models
- **CRISP Controllers** - cartesian/joint impedance controllers from [crisp_controllers](https://github.com/utiasDSL/crisp_controllers)
- **pixi package management** - reproducible environment with robostack-jazzy

## Prerequisites

Install pixi:
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

## Quick Start

```bash
git clone https://github.com/lvjonok/pixi_ur_ros2.git
cd pixi_ur_ros2

# Setup: clone CRISP controllers and build
pixi run -e jazzy setup

# Launch the robot
pixi run -e jazzy launch robot_ip:=192.168.56.101
```

## Available Commands

| Command | Description |
|---------|-------------|
| `pixi run -e jazzy setup` | Clone CRISP controllers and build all packages |
| `pixi run -e jazzy build` | Build packages with colcon |
| `pixi run -e jazzy launch` | Launch the UR robot |

## Launch Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `robot_ip` | `192.168.56.101` | IP address of the robot |
| `ur_type` | `ur16e` | Robot type (ur3, ur3e, ur5, ur5e, ur10, ur10e, ur16e, ur20, ur30) |
| `use_fake_hardware` | `false` | Use mock hardware for testing |
| `use_rviz` | `false` | Launch RViz for visualization |

## CRISP Controllers

Available controllers (spawned inactive by default):
- `cartesian_impedance_controller`
- `joint_impedance_controller`
- `gravity_compensation`

Active broadcasters:
- `twist_broadcaster`
- `pose_broadcaster`

Activate a controller:
```bash
ros2 control switch_controllers --activate cartesian_impedance_controller --deactivate scaled_joint_trajectory_controller
```
