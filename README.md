# TurtleBot3 Reinforcement Learning

This project documents the upgrade of the TurtleBot3 ecosystem from ROS 2 Humble (Ubuntu 22.04) to **ROS 2 Jazzy (Ubuntu 24.04)** and the implementation of a Deep Q-Network (DQN) for autonomous navigation. It includes the validation of the system in **Gazebo Harmonic** and the deployment of a trained agent on the physical **TurtleBot3 Burger** using custom environment nodes.

## Documentation

> **Note:** This README provides a technical overview of the repository structure and usage. For detailed step-by-step installation guides, hardware setup, and theoretical background, please refer to the full **Project Documentation PDF** (available upon request). 

## System Architecture

The project follows a phased upgrade approach:

* **Workstation:** Ubuntu 24.04 LTS | ROS 2 Jazzy | Gazebo Harmonic
* **TurtleBot3 (SBC):** Ubuntu Server 24.04 LTS | ROS 2 Jazzy
* **Methodology:** Training in Simulation → Transfer to Physical Robot

## Installation & Setup

### 1. Standard Dependencies

The system relies on the official ROBOTIS machine learning packages. Ensure you have the standard workspace set up as described in the official manual: https://emanual.robotis.com/docs/en/platform/turtlebot3/machine_learning/#machine-learning (adapted for Jazzy)

```bash
# Example setup (refer to documentation for full details)
cd ~/turtlebot3_ws/src/
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_machine_learning.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
# ... install dependencies ...
```

### 2. Custom Nodes for Training and Physical Deployment

To enable the Reinforcement Learning agent to run on the **physical robot**, this repository contains custom extensions to the standard package. We developed a fix to ensure a smooth training process in Gazebo and a "Real World" environment wrapper that bridges the gap between the simulation-based code and real hardware.

Files added/modified:

* **`dqn_agent_training.py`**: A modified version of the standard training agent. It includes critical bug fixes (handling random LiDAR shape mismatches) to ensure the training process in Gazebo does not crash.
    * *Note:* This file is intended **only for Phase 1 (Simulation Training)**. Do not use this for the physical robot deployment.
* **`dqn_environment_real.py`**: Handles sensor data processing (LiDAR downsampling) and reward calculation based on real-world telemetry.
* **`dqn_stage_real.py`**: Acts as a virtual referee, generating virtual goals relative to the robot's odometry since absolute world coordinates do not exist in the real room.


**Integration:**

To use these nodes, simply replace or extend the nodes in `turtlebot3_dqn` directory in your workspace with the one provided in this repository.

```bash
# Navigate to your workspace
cd ~/turtlebot3_ws/src/turtlebot3_machine_learning/

# Replace the inner turtlebot3_dqn folder with the one from this repo
cp -r /path/to/this/repo/turtlebot3_dqn/turtlebot3_dqn/ .
```

*This structure ensures that you can easily update the base package from ROBOTIS and simply re-apply our custom nodes for physical deployment.*

## Usage


### Phase 1: Training in Simulation

**This phase uses the standard ROBOTIS implementation with modification to the dqn_training.py .**

We used release **v1.0.1** from the official repository:
```bash
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_machine_learning/tree/main
```

For detailed training instructions, parameters, and potential updates to the training procedure, please refer to the official ROBOTIS e-Manual:

**[ROBOTIS TurtleBot3 Machine Learning Guide](https://emanual.robotis.com/docs/en/platform/turtlebot3/machine_learning/#machine-learning)**

**Note on Standard Implementation:**
While this phase generally uses the standard ROBOTIS implementation, we encountered issues with the original `dqn_agent.py` in the Jazzy/Harmonic release (specifically regarding library imports and LiDAR shape mismatches).

* **Recommendation:** Use the `dqn_agent.py` provided in this repository. It contains necessary fixes to prevent crashes during long training sessions in Gazebo.

> **Note:** Training procedures and hyperparameters may have changed since v1.0.1. Always consult the official documentation for the most up-to-date training workflow.

Example training workflow (verify with official docs):

```bash
# Terminal 1: Launch Simulation
ros2 launch turtlebot3_gazebo turtlebot3_dqn_stage1.launch.py

# Terminal 2: Run Environment
ros2 run turtlebot3_dqn dqn_environment 1

# Terminal 3: Run Agent (Training)
ros2 run turtlebot3_dqn dqn_agent 1 1000
```

### Phase 2: Physical Deployment (Real World) - **Custom Contribution**

After validating the model in simulation, deploy it to the physical robot. Ensure the PC and TurtleBot3 are in the same ROS Domain.

**This phase uses our custom nodes (`dqn_environment_real.py` and `dqn_stage_real.py`) to enable transfer from simulation to the physical robot.**

**1. On the TurtleBot3 (SSH):**

```bash
ros2 launch turtlebot3_bringup robot.launch.py
```

**2. On the PC (Workstation):**

```bash
# Start the Virtual Stage Manager (Referee)
python3 dqn_stage_real.py

# Start the Real-World Environment Bridge
python3 dqn_environment_real.py

# Run the Agent (Inference Mode)
# Loads the pre-trained model (e.g., Stage 1, Episode 600) from Phase 1
ros2 run turtlebot3_dqn dqn_test 1 600
```

## Repository Structure

```plaintext
.
├── README.md
├── docs/                        # Project Documentation & Reports
└── turtlebot3_dqn/              # Custom Source Code
    └── turtlebot3_dqn/
        ├── dqn_environment_real.py  # [NEW] Real-world logic
        ├── dqn_stage_real.py        # [NEW] Virtual goal manager
        ├── dqn_agent.py             # [NEW] Modified training agent (Simulation fixes)
        ├── dqn_agent.py             # Standard agent (refactored imports)
        ├── dqn_test.py              # Inference node
        └── ...
```

## Authors

* **Raoul Hartmann**
* **Dominik Neumaier**
* **Supervisors:** Dr. Loic Cuvillon (Télécom Physique Strasbourg)
