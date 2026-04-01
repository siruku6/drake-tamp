# Setup Instructions for Docker

This document provides instructions for setting up the Docker environment for this project.

## 1. Overview 🗺️

- The build process is divided into two stages: the base image and the main image.


### 1-1.What is the Base Image?

- The base image is built using the `docker-compose-base.yml` and `Dockerfile.base` file. This image only includes the necessary dependencies for installing [OMPL](https://ompl.kavrakilab.org/).


### 1-2. Why build the Base Image? 🤔

- The installation of OMPL takes a significant amount of time⏳, so this base image is created to perform the installation only once.
- Even if issues arise during the subsequent image build, there is no need to reinstall OMPL because you can use the base image as a starting point for the subsequent build ✌️



## 2. Building steps 🛠️

### 2-1. Building the Base Image

- Run the following command to build the base image:

   ```bash
   docker compose -f docker/docker-compose-base.yml build
   ```

- This command will create the base image `python-ompl-base:ubuntu24.04`. This will take a long time to complete because it includes the installation of OMPL 😣⏳.
- You will see the following output during the build process, which indicates that OMPL is being built:

    ```bash
    [137/530] Building CXX object src/ompl/CMakeFiles/ompl.dir/geometric/planne
    => => # rs/rlrt/src/RLRT.cpp.o
    ```


### 2-2. Building the Main Image

- After successfully building the base image, please follow the steps below.


#### 2-2-1. Create a `.env` file

- Before building the main image, you need to create a `.env` file in the `docker` directory. You can create it by copying the example file:

    ```bash
    cd docker
    cp .env.example .env
    ```


#### 2-2-2. Build the Main Image

- You can build the main image using the following command:

    ```bash
    # in docker/ directory
    docker compose build
    ```

- The main depends on the base image `python-ompl-base:ubuntu24.04`.


#### To compile FastDownward run:

```bash
git submodule update --init --recursive

cd docker
docker compose up -d
docker compose exec dtamp bash
cd pddlstream && ./FastDownward/build.py release64
cd pddlstream/FastDownward/builds && ln -s release64 release32
```


## 3. Remote Access via TigerVNC 🖥️

This section explains how to access the container's desktop environment from a remote machine via TigerVNC.

### 3-1. Port Mapping

The container exposes the following ports (configurable via `.env`):

| Port (Host) | Port (Container) | Protocol |
|-------------|-----------------|----------|
| `2300` (default) | `22` | SSH |
| `5901` (default) | `5901` | TigerVNC |

### 3-2. SSH Config (Local Machine)

Add the following entries to your local `~/.ssh/config`.  
Replace `<remote-server>` with the hostname or IP of the remote server where the container is running.

```ssh_config
Host <remote-server>
    Hostname <remote-server-ip>
    User ubuntu

Host tamp_workspace
    ProxyCommand ssh -q <remote-server> -W localhost:2300
    LocalForward 5901 localhost:5901
    User ubuntu
```

> ⚠️ **Common mistakes to avoid**
> - Do **not** use `-q0 localhost 5901` in `ProxyCommand` — `-q0` is not a valid SSH flag.
> - The `ProxyCommand` must forward to the **SSH port (2300)**, not the VNC port (5901).

### 3-3. Connecting

1. Open an SSH tunnel to the container:

    ```bash
    ssh tamp_workspace
    ```

2. Open your VNC client and connect to:

    ```
    localhost:5901
    ```

3. Enter the password set via `DOCKER_PASSWORD` in your `.env` file when prompted.

### 3-4. Connection Flow

```
Local PC
  │  ssh tamp_workspace
  ↓
Remote Server (ProxyCommand jump)
  │  -W localhost:2300  →  Docker container SSH (:22)
  ↓
Docker Container
  │  LocalForward 5901  →  TigerVNC server (:5901)
  ↓
XFCE Desktop
```
