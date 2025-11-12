# Initial Situation and Approach

## Initial Situation

The project started with the following hardware and software configuration:

- PC workstations running Ubuntu 22.04, ROS2 Humble, and Gazebo 11 Classic
- Turtlebot 3 robot operating on Ubuntu 22.04 with ROS2 Humble

This configuration represented the existing infrastructure at Telecom Physique Strasbourg. However, with the release of newer versions of the core software components, an upgrade was necessary to take advantage of improved features, better performance, and long-term support.

## Project Approach

The upgrade strategy was designed as a phased implementation to minimize risks and validate each step before proceeding to the next phase. This methodical approach ensured system stability and allowed for troubleshooting at each stage.

The first phase involves upgrading the PC workstations to Ubuntu 24.04 and ROS2 Jazzy, including the transition from Gazebo 11 Classic to Gazebo Harmonic. This allows the development environment to be modernized while keeping the physical robot operational.

A critical question emerges at this point: can ROS2 Jazzy and ROS2 Humble communicate with each other? To answer this, the second phase conducts simulations while keeping the physical Turtlebot 3 on its original Ubuntu 22.04 and ROS2 Humble configuration. This validates cross-version compatibility through controlled testing.

Once cross-version compatibility is confirmed, the physical Turtlebot 3 is upgraded to Ubuntu 24.04 and ROS2 Jazzy to match the PC workstation configuration. Additional simulations are then performed with matching software versions across all components to ensure the system operates correctly.

With the upgraded infrastructure validated, machine learning experiments are conducted on the Turtlebot 3 system. The final validation step involves testing the trained machine learning model in real-world scenarios to assess its performance outside the simulation environment and verify that the entire system functions as intended in practical applications.

## Table of Contents

1. [Phase 1: PC Workstation Upgrade](#phase-1-pc-workstation-upgrade)
2. [Phase 2: Cross-Version Compatibility Testing](#phase-2-cross-version-compatibility-testing)
3. [Phase 3: Turtlebot 3 Hardware Upgrade](#phase-3-turtlebot-3-hardware-upgrade)
4. [Phase 4: Full System Validation](#phase-4-full-system-validation)
5. [Phase 5: Machine Learning Implementation](#phase-5-machine-learning-implementation)
6. [Phase 6: Real-World Validation](#phase-6-real-world-validation)


# Initial situation

- PCs mit Ubuntu 22.04 und ROS2 Humble sowie Gazebo 11 (Classic)
- Turtlebot 3 mit Ubuntu 22.04 
- Ziel: Upgrade des Rechners auf 24.04 und ROS2 Jazzy
- Verwendung einer neuen Version von Gazebo (Harmonic)?
- Validierung der neuen Versionen mit der Simulation
- Updaten des Turtlebot3 auf neue ROS & Ubunut Version



# Update of the Linux PC (Ubuntu 22.04 → 24.04)

Since **ROS 2 Jazzy** is only supported on Ubuntu 24.04, the PC must first be upgraded from Ubuntu 22.04 (Jammy) to Ubuntu 24.04 (Noble).

---

## 0. Before You Start
- You can directly upgrade to Ubuntu 24.04 LTS ("Noble Numbat") from either Ubuntu 22.04 LTS ("Jammy Jellyfish") or Ubuntu 23.10 ("Mantic Minotaur").
- Upgrades will not be available immediately following the release of Ubuntu 24.04 LTS. Upgrades from Ubuntu 23.10 will be enabled shortly after the release, once any known upgrade issues are resolved. Upgrades from Ubuntu 22.04 LTS are not enabled until the release of Ubuntu 24.04.1 LTS. This is currently scheduled for August 2024.
- Be sure that you have all updates applied to your current version of Ubuntu before you upgrade.
- Before upgrading it is recommended that you read the release notes for Ubuntu 24.04 LTS, which document caveats and workarounds for known issues in this version.

If you have a version of Ubuntu other than 22.04 LTS or 23.10, please see UpgradeNotes for information on how to upgrade.

## 1. Update package lists and installed packages
```bash
sudo apt update && sudo apt upgrade -y
```

- ```bash apt update``` fetches the latest package lists from repositories.

- ```bash apt upgrade ``` updates all installed packages to the newest available versions that do not require new dependencies.

- ```bash -y ``` automatically confirms all prompts.


## 2. Perform a distribution upgrade

```bash sudo apt dist-upgrade -y```


- Executes a more complete upgrade that may add or remove packages if required by new dependencies.
- Ensures the system is fully up to date before the release upgrade.
- Not strictly required, but helps to minimize issues during the upgrade.

## 3. Remove unused packages
```bash sudo apt autoremove -y```

- Cleans up orphaned dependencies that are no longer needed.
- Helps to prevent conflicts during the release upgrade and frees disk space.
- Not mandatory, but improves system cleanliness before upgrading.

## 4. Update manual packages

An error occured:

```bash linux-generic-hwe-22.04 : Depends: linux-image-generic-hwe-22.04 (= 6.8.0-84.84~22.04.1) but 5.15.0.48.48 is to be installed Depends: linux-headers-generic-hwe-22.04 (= 6.8.0-84.84~22.04.1) but 5.15.0.48.48 is to be installed Recommends: ubuntu-kernel-accessories but it is not installable```

- Some packages needed to be manually updated before an update to Ubunutu 22.04 via UI or CLI is possible.
- Use the following command:
```bash sudo apt install <package>``` 

- Reboot is necessary after this

## 4b. Upgrading via CLI

```bash sudo do-release-upgrade```

- Now the new Ubunut version can be installed

## 4b. Alternative: Upgrading Ubuntu Deskop 22.04 LTS to 24.04 LTS

1. Run the update-manager application.
2. In Update Manager, click the Settings... button, and enter your password to start the Software Sources application.
3. Select the sub menu Updates from the Software Sources application.
4. Confirm the "Notify me of a new Ubuntu version:" option is set to "For any new version", and change it if otherwise.
5. Close the Software Sources application and return to Update Manager.
6. In Update Manager, click the Check button to check for new updates.
7. If there are any updates to install, use the Install Updates button to install them.
8. Run update-manager.
9. If you want to upgrade early, before upgrades are officially supported, you can pass the -d option when running update-manager. Do this at your own risk. It is advised to check the release notes for Ubuntu 24.04 LTS before doing so.
10. A message will appear informing you of the availability of the new release.
11. Click Upgrade.
12. Follow the on-screen instructions.

(Credits: https://help.ubuntu.com/community/NobleUpgrades#Upgrading_Ubuntu_Desktops_to_24.04_LTS)


## 5. Fresh installation for a PC

Since manual upgrading from 22 to 24 lead to some errors, a fresh installation of UBUNTU24 was done. The required ISO image was downloaded and flashed with balenaEtcher. Afterwards the PC was rebooted with that fresh destribution which was sucessfull. 

- ISO Image runtergeladen UBunutu Seite Link: 
- balenaEtcher für Flashing USB Stick
- Screenshot des Kopievorgangs

# Installation of ROS2 Jazzy & Gazebo Harmonic for Ubuntu 24.04

Since **ROS 2 Jazzy** is only supported on Ubuntu 24.04, the installation can now be executed.

---

# 1. Installation 

Installation of ROS2-jazzy according to the following tutorial was sucessfull on the "fresh" UBUNTU24 versions. 
https://automaticaddison.com/how-to-install-ros-2-jazzy/

Installing Gazobo according to the same tutorial. 
Installation was sucessfull. Demo are working. 
To start gazebo: gz sim

### State 01.10: Gazebo and ROS are up and running but not interconnected. Problems with installing ros-jazzy-gazebo-ros-pkgs


# Validating Installation by using Turtlebot 3 Simulation


- Zuerst PC Setup: https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/

- Vor Start der Simulation mit dem Burger Turtlebot noch source ~/.bashrc  
- Vor Start der Keyboard Kontrolle in das Verzeichnis wechseln mit cd und dann nochmal source ~/.bashrc  dann kann man starten
- https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/

- DRLNAV Demo not working due to dependencies (Screenshot) to old Gazebo Classic (11.0) version
- Using the documentation to try a new simulation to check whether ROS2 Jazzy and Gazebo Harmonic work together on Ubuntu 24.04
- Simulation is used for Turtlebot 3

- Screenshot von der Demo anhängen



# Simulation - Überprüfen ob der Turtlebot3 mit veralteter ROS und Ubuntu Version nun mit dem Rechner mit neuer Software als Node funktioniert

- Simulation funktioniert, daher weitermachen
- Verwendung der einfachen Navigation via Pfeiltasten (https://seafile.unistra.fr/lib/ea938cb8-ad06-43c2-928f-077ff7b1a944/file/turtlebot3_demos/turtlebot3_navigation_demo.md)

- Doku dazu ist auf der Webseite ausführlicher
    - https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/#run-slam-node
    - PC Setup wurde vorhin bereits durchgeführt
    - Hardware unverändert wie vor 2 Jahren (1x sudo apt update nach Start aufgrund WiFi Probleme)
    - Bringup konfiguriert: https://emanual.robotis.com/docs/en/platform/turtlebot3/bringup/#bringup auf dem Turtlebot

- Es funktioniert nicht (siehe Screenshot wo der Prozess abbricht)


# SD Card Backup of turtlebot3
- Backup der SD-Karte
    - MicroSD Karte aus dem Turlebot entnehmen und mit Adapter mit dem PC verbinden
    - nach Anleitung aber leicht andere Befehle: https://seafile.unistra.fr/lib/ea938cb8-ad06-43c2-928f-077ff7b1a944/file/turtlebot3_demos/BackupRestore_SDCard.md
        - lsblk | grep 'writable\|system-boot'
        - sudo umount /dev/sdb1  sudo umount /dev/sdb2
        - sudo dd if=/dev/sdb of=./rpi5_rpit_tir4street.img status=progress
        - sync
        - Restliche befehle identisch zur Anleitung durchgeführt bis zum Kapitel Restore the image, das wurde nicht durchgeführt
- Erneutes testen der Simulation mit dem Keyboard https://emanual.robotis.com/docs/en/platform/turtlebot3/basic_operation/#basic-operation


# Upgrading Turtlebot 3 to Ubunutu 24.04 and Gazebo Harmonic
- Following the Instructions: https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup



# Checking whether remote control via keyboard control



# Trying Machine Learning with 
- https://emanual.robotis.com/docs/en/platform/turtlebot3/machine_learning/#machine-learning
- Check how we get it to the robot at the end
- We only have to 
- How is the communication between the nodes working




# Trying Reinforcement Learning Demo on new Ubunutu and ROS2 installation with Gazebo

## 1. Installation 

- Following this: https://github.com/tomasvr/turtlebot3_drlnav?tab=readme-ov-file#installation

- Using manual installation (Not Docker)
- Removing nvidia-container-toolkit

- sudo apt python 3
- sudo apt install python3-pip

## 2. Installing Gazebo

- Connecting Gazebo to ROS2 Jazzy

-  ROS2-Gazebo Bridge installieren
sudo apt install ros-jazzy-ros-gz
- Demo-Pakete installieren
bashsudo apt install ros-jazzy-ros-core ros-jazzy-geometry2
- ROS2 Jazzy sourcen
source /opt/ros/jazzy/setup.bash
- Gazebo-ROS2 Verbindung testen
Option A: Mit dem neuen Gazebo Sim (empfohlen)
Starte eine einfache Welt:
gz sim shapes.sdf
In einem zweiten Terminal, teste die ROS2-Verbindung:
source /opt/ros/jazzy/setup.bash
ros2 topic list

- Ab hier starten mit installing Python3, Pytorch in der Dokumentation

- Python packages installiert um Konflikte zwischen apt und pip zu umgehen
    - Hinzufügen von --break-system-packages nach den Befehlen im Tutorial --> Versionen entfernen da veraltet (torch zB)
    
- Nvidida installation

- Downloading the code base and building
    - Use sudo apt-get install ros-jazzy-turtlebot3-description instead of foxxy
    - src Pfad angepast zu ros update wo jazzy nun liegt und jazzy ergänzt
 
# Trying to steer the pyshical TurtleBot
  
Validation that the following set up works: 

- Ubuntu PC: 24.04 and ROS Jazzy 
- Ubuntu version TurtleBot: 22.04 and ROS Humble
  
- Problem: TurtleBot has no IP adress, is not registered in the WLAN network.
- Therefore not reachable via SSH
- Robot is connected with Screen and keyboard, IP problem not resolvable

# Installing UBUNTU 24 on the Turtle-Bot

- saving the current image of the SD card
- Using the Raspberry Pi imager to follow this tutorial: https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/
- SD card hard to be unmounted to successfully follow the process
- UBUNTU SERVER 24.04.3 LTS (64-Bit) is written on the SD card

# Visualize the LIDAR SCAN

On the TurtleBot vis SSH:
1. ros2 launch turtlebot3_bringup robot.launch.py
2. (To see the values): ros2 topic echo /scan 

On the PC:
rviz2 
-> Global Options: BaseScan
-> LaserScan, Topic, Relicability Polica : BestEffort

# interim status (17.10)
-> PC and TurtleBot were successfully upgraded 
-> The TurtleBot can be steered via PC and SSH, Lidar and camera are wokring
-> next step: ML capabilities 

# Machine Learning 
Following this tutorial: https://emanual.robotis.com/docs/en/platform/turtlebot3/machine_learning/#software-setup
9.1: Problems with building the hls_lfcd_lds_driver for the turtlebot 
    -> node parameteres needed to be upgraded 
    -> rebuilt afterwards successfull 
    -> all 18 packages were installed 

# Model Training
Four terminals required. The following commands need to be executed (in the respective folder)

1. /turtlebot3_ws/install/turtlebot3_gazebo:
   ros2 launch turtlebot3_gazebo turtlebot3_dqn_stage1.launch.py
   
2. /turtlebot3_ws/install/:
   ros2 run turtlebot3_dqn dqn_environment 1
   
3. /turtlebot3_ws/install/turtlebot3_dqn:
   ros 2 run turtlebot3_dqn dqn_gazebo 1
   
4. /turtlebot3_ws/:
   ros2 run turtlebot3_dqn dqn_agent 1 1000 (stage + anzahl episoden)




# Training wieder zum Laufen gebracht

- Wie in der Anleitung
 $ cd ~/turtlebot3_ws/src/
 $ git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_machine_learning.git
 $ sudo rosdep update
 $ export PIP_BREAK_SYSTEM_PACKAGES=1


- Anlage venv in Ordner src und dort installieren der dependencies:
 $ cd ~/turtlebot3_ws && rosdep install --from-paths src --ignore-src

- Zudem noch folgende Versionen / Pakete installieren im venv:

(venv) ros@c138-pc12:~/turtlebot3_ws$ pip list
Package                              Version     Editable project location
------------------------------------ ----------- ---------------------------------------------
absl-py                              2.3.1
ackermann-msgs                       2.0.2
action-msgs                          2.0.3
action-tutorials-interfaces          0.33.7
action-tutorials-py                  0.33.7
actionlib-msgs                       5.3.6
actuator-msgs                        0.0.1
ament-cmake-test                     2.5.4
ament-copyright                      0.17.3
ament-cppcheck                       0.17.3
ament-cpplint                        0.17.3
ament-flake8                         0.17.3
ament-index-python                   1.8.1
ament-lint                           0.17.3
ament-lint-cmake                     0.17.3
ament-package                        0.16.4
ament-pep257                         0.17.3
ament-uncrustify                     0.17.3
ament-xmllint                        0.17.3
angles                               1.16.1
argcomplete                          3.6.3
astunparse                           1.6.3
bond                                 4.1.2
builtin-interfaces                   2.0.3
cartographer-ros-msgs                2.0.9003
catkin-pkg                           1.1.0
certifi                              2025.11.12
charset-normalizer                   3.4.4
colcon-argcomplete                   0.3.3
colcon-bash                          0.5.0
colcon-cd                            0.1.1
colcon-cmake                         0.2.29
colcon-common-extensions             0.3.0
colcon-core                          0.20.1
colcon-defaults                      0.2.9
colcon-devtools                      0.3.0
colcon-library-path                  0.2.1
colcon-metadata                      0.2.5
colcon-notification                  0.3.0
colcon-output                        0.2.13
colcon-package-information           0.4.0
colcon-package-selection             0.2.10
colcon-parallel-executor             0.4.0
colcon-pkg-config                    0.1.0
colcon-powershell                    0.4.0
colcon-python-setup-py               0.2.9
colcon-recursive-crawl               0.2.3
colcon-ros                           0.5.0
colcon-test-result                   0.3.8
colcon-zsh                           0.5.0
composition-interfaces               2.0.3
control-msgs                         5.5.0
controller-manager                   4.38.0
controller-manager-msgs              4.38.0
coverage                             7.11.3
cv-bridge                            4.1.0
demo-nodes-py                        0.33.7
diagnostic-msgs                      5.3.6
diagnostic-updater                   4.2.6
distlib                              0.4.0
docutils                             0.22.3
domain-coordinator                   0.12.0
dwb-msgs                             1.3.9
dynamixel-sdk                        3.8.4
empy                                 4.2
example-interfaces                   0.12.0
examples-rclpy-executors             0.19.6
examples-rclpy-minimal-action-client 0.19.6
examples-rclpy-minimal-action-server 0.19.6
examples-rclpy-minimal-client        0.19.6
examples-rclpy-minimal-publisher     0.19.6
examples-rclpy-minimal-service       0.19.6
examples-rclpy-minimal-subscriber    0.19.6
flatbuffers                          25.9.23
gast                                 0.6.0
generate-parameter-library-py        0.5.0
geographic-msgs                      1.0.6
geometry-msgs                        5.3.6
google-pasta                         0.2.0
gps-msgs                             2.1.1
grpcio                               1.76.0
h5py                                 3.15.1
idna                                 3.11
image-geometry                       4.1.0
iniconfig                            2.3.0
interactive-markers                  2.5.5
joint-state-publisher                2.4.0
keras                                3.9.2
laser-geometry                       2.7.2
launch                               3.4.7
launch-ros                           0.26.9
launch-testing                       3.4.7
launch-testing-ros                   0.26.9
launch-xml                           3.4.7
launch-yaml                          3.4.7
libclang                             18.1.1
lifecycle-msgs                       2.0.3
logging-demo                         0.33.7
map-msgs                             2.4.1
Markdown                             3.10
markdown-it-py                       4.0.0
MarkupSafe                           3.0.3
mdurl                                0.1.2
message-filters                      4.11.8
ml-dtypes                            0.4.1
my-test-package                      1.0         /home/ros/turtlebot3_ws/build/my-test-package
namex                                0.1.0
nav-2d-msgs                          1.3.9
nav-msgs                             5.3.6
nav2-common                          1.3.9
nav2-msgs                            1.3.9
nav2-simple-commander                1.0.0
notify2                              0.3.1
numpy                                1.26.4
opt_einsum                           3.4.0
optree                               0.17.0
osrf-pycommon                        2.1.7
packaging                            25.0
pal-statistics                       2.7.0
pal-statistics-msgs                  2.7.0
pcl-msgs                             1.0.0
pendulum-msgs                        0.33.7
pip                                  24.0
pluggy                               1.6.0
protobuf                             4.25.8
Pygments                             2.19.2
pyparsing                            3.2.5
pyqtgraph                            0.13.7
pytest                               9.0.0
pytest-cov                           7.0.0
pytest-repeat                        0.9.4
pytest-rerunfailures                 16.1
python-dateutil                      2.9.0.post0
python-qt-binding                    2.2.2
PyYAML                               6.0.3
qt-dotgraph                          2.7.5
qt-gui                               2.7.5
qt-gui-cpp                           2.7.5
qt-gui-py-common                     2.7.5
quality-of-service-demo-py           0.33.7
rcl-interfaces                       2.0.3
rclpy                                7.1.5
rcutils                              6.7.4
requests                             2.32.5
resource-retriever                   3.4.4
rich                                 14.2.0
rmw-dds-common                       3.1.0
robot-localization                   3.8.3
ros-gz-bridge                        1.0.16
ros-gz-interfaces                    1.0.16
ros-gz-sim                           1.0.16
ros2action                           0.32.6
ros2bag                              0.26.9
ros2bag-mcap-cli                     0.26.9
ros2bag-sqlite3-cli                  0.26.9
ros2cli                              0.32.6
ros2component                        0.32.6
ros2controlcli                       4.38.0
ros2doctor                           0.32.6
ros2interface                        0.32.6
ros2launch                           0.26.9
ros2lifecycle                        0.32.6
ros2multicast                        0.32.6
ros2node                             0.32.6
ros2param                            0.32.6
ros2pkg                              0.32.6
ros2run                              0.32.6
ros2service                          0.32.6
ros2topic                            0.32.6
rosbag2-interfaces                   0.26.9
rosbag2-py                           0.26.9
rosgraph-msgs                        2.0.3
rosidl-adapter                       4.6.6
rosidl-cli                           4.6.6
rosidl-cmake                         4.6.6
rosidl-generator-c                   4.6.6
rosidl-generator-cpp                 4.6.6
rosidl-generator-py                  0.22.2
rosidl-generator-type-description    4.6.6
rosidl-parser                        4.6.6
rosidl-pycommon                      4.6.6
rosidl-runtime-py                    0.13.1
rosidl-typesupport-c                 3.2.2
rosidl-typesupport-cpp               3.2.2
rosidl-typesupport-fastrtps-c        3.6.2
rosidl-typesupport-fastrtps-cpp      3.6.2
rosidl-typesupport-introspection-c   4.6.6
rosidl-typesupport-introspection-cpp 4.6.6
rpyutils                             0.4.2
rqt                                  1.6.1
rqt-action                           2.2.0
rqt-bag                              1.5.5
rqt-bag-plugins                      1.5.5
rqt-console                          2.2.1
rqt-graph                            1.5.5
rqt-gui                              1.6.1
rqt-gui-py                           1.6.1
rqt-msg                              1.5.1
rqt-plot                             1.4.4
rqt-publisher                        1.7.2
rqt-py-common                        1.6.1
rqt-py-console                       1.2.2
rqt-reconfigure                      1.6.2
rqt-service-caller                   1.2.1
rqt-shell                            1.2.2
rqt-srv                              1.2.2
rqt-topic                            1.7.3
scipy                                1.16.3
sensor-msgs                          5.3.6
sensor-msgs-py                       5.3.6
service-msgs                         2.0.3
setuptools                           79.0.1
shape-msgs                           5.3.6
six                                  1.17.0
slam-toolbox                         2.8.3
smclib                               4.1.2
sros2                                0.13.4
statistics-msgs                      2.0.3
std-msgs                             5.3.6
std-srvs                             5.3.6
stereo-msgs                          5.3.6
teleop-twist-keyboard                2.4.1
tensorboard                          2.17.1
tensorboard-data-server              0.7.2
tensorflow                           2.17.1      /home/ros/turtlebot3_ws/build/tensorflow
termcolor                            3.2.0
tf-transformations                   1.1.0
tf2-geometry-msgs                    0.36.14
tf2-kdl                              0.36.14
tf2-msgs                             0.36.14
tf2-py                               0.36.14
tf2-ros-py                           0.36.14
tf2-sensor-msgs                      0.36.14
tf2-tools                            0.36.14
theora-image-transport               4.0.6
topic-monitor                        0.33.7
trajectory-msgs                      5.3.6
turtlebot3_dqn                       1.0.1       /home/ros/turtlebot3_ws/build/turtlebot3_dqn
turtlebot3-example                   2.3.3
turtlebot3-msgs                      2.4.0
turtlebot3-teleop                    2.3.3
turtlesim                            1.8.3
type-description-interfaces          2.0.3
typing_extensions                    4.15.0
unique-identifier-msgs               2.5.0
urllib3                              2.5.0
vision-msgs                          4.1.1
visualization-msgs                   5.3.6
Werkzeug                             3.1.3
wheel                                0.45.1
wrapt                                2.0.1
xacro                                2.1.1



- Danach:

- colcon build --symlink-install

Quell-Setup-Skript ausführen:
Nach dem Build musst du das ROS2-Setup-Skript ausführen, um sicherzustellen, dass die Umgebungsvariablen richtig gesetzt sind:

source ~/turtlebot3_ws/install/setup.bash

Versuche erneut, das Paket auszuführen:

 -/turtlebot3_ws/   ros2 run turtlebot3_dqn dqn_agent 1 1000

    


  

 $ colcon build --symlink-install
