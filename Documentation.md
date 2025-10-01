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

# Installation of ROS2 Jazzy for Ubuntu 24.04

Since **ROS 2 Jazzy** is only supported on Ubuntu 24.04, the installation can now be executed.

---

# 1. Installation 

Installation of ROS2-jazzy according to the following tutorial was sucessfull on the "fresh" UBUNTU24 versions. 
https://automaticaddison.com/how-to-install-ros-2-jazzy/

Installing Gazobo according to the same tutorial. 

