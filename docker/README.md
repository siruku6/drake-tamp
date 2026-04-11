# Setup Instructions for Docker

This document provides instructions for setting up the Docker environment for this project.

## 1. Overview 🗺️

- Recently, `ompl` has been updated to version 2.0.0, which can be installed through `pip install ompl`.
- Please also see the official documentation for more details: https://ompl.kavrakilab.org/installation.html
    - After accessing the link, click on the "Python" button to view the installation instructions for the Python bindings of OMPL.


## 2. Building steps 🛠️

<!-- ### 2-1. Building the Base Image

- Run the following command to build the base image:

   ```bash
   docker compose -f docker/docker-compose-base.yml build
   ```

- This command will create the base image `python-ompl-base:ubuntu24.04`. This will take a long time to complete because it includes the installation of OMPL 😣⏳.
- You will see the following output during the build process, which indicates that OMPL is being built:

    ```bash
    [137/530] Building CXX object src/ompl/CMakeFiles/ompl.dir/geometric/planne
    => => # rs/rlrt/src/RLRT.cpp.o
    ``` -->


### 2-1. Building the Main Image

- Please follow the steps below.


#### 2-1-1. Create a `.env` file

- Before building the main image, you need to create a `.env` file in the `docker` directory. You can create it by copying the example file:

    ```bash
    cd docker
    cp .env.example .env
    ```


#### 2-1-2. Build the Main Image

- You can build the main image using the following command:

    ```bash
    # in docker/ directory
    docker compose build
    ```


#### To compile FastDownward

- It may be better to fix the version of gc and g++ to 11 in advance.
- Run the following commands at first:
    ```bash
    git rm -rf experiments/ikea_induction
    rm -rf .git/modules/experiments/ikea_induction
    git submodule update --init --recursive

    cd docker
    docker compose up -d
    docker compose exec dtamp bash
    ```
- Then add the following line to `FastDownward/src/search/options/option_parser.h` before the line `#include <memory>` at line 9:
    ```cpp
    #include <limits>
    ```
- At last, run the following commands to compile FastDownward:
    ```bash
    cd pddlstream
    ./FastDownward/build.py release64

    cd ./FastDownward/builds && ln -s release64 release32
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

> [!WARNING]
> **Common mistakes to avoid**
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

## 4. Running Experiments 🧪

### Running an experiment in the container

```bash
# @ drake-tamp/ directory
python -O experiments/main.py \
    --domain blocks_world \
    --algorithm adaptive \
    --mode normal \
    --problem-file experiments/blocks_world/problems/default_problem.yaml \
    --logpath logs/smoke_default \
    --max-time 90 \
    --max_planner_time 30
```

```bash
# @ drake-tamp/ directory
python -O experiments/main.py \
  --domain blocks_world \
  --mode save \
  --algorithm adaptive \
  --problem-file experiments/blocks_world/problems/default_problem.yaml \
  --logpath ./logs/exp_output/ \
  --url tcp://127.0.0.1:6000
```

### Create a recording of the experiment

- This doesn't work:

```bash
# @ drake-tamp/ directory
python -m experiments.blocks_world.run -u dummy -p ./logs/test/
```

- This makes a recording:

```bash
# @ drake-tamp/ directory
python -m experiments.main \
    --domain blocks_world \
    --mode save \
    --algorithm adaptive \
    --problem-file experiments/blocks_world/problems/default_problem.yaml \
    --logpath ./logs/test/ \
    --simulate \
    --url tcp://127.0.0.1:6000
```
