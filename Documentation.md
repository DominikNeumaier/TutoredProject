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
  
