# Update of the Windows PC (Ubuntu 22.04 → 24.04)

Since **ROS 2 Jazzy** is only supported on Ubuntu 24.04, the PC must first be upgraded from Ubuntu 22.04 (Jammy) to Ubuntu 24.04 (Noble).

---

## 1. Update package lists and installed packages
```bash
sudo apt update && sudo apt upgrade -y
```

- ```bash apt update``` fetches the latest package lists from repositories.

- ```bash apt upgrade ``` updates all installed packages to the newest available versions that do not require new dependencies.

- ```bash -y ``` automatically confirms all prompts.


## 2. Perform a distribution upgrade