# ====================================================================
# Base Image
# ====================================================================
# The past resolution for dependency problems
# https://github.com/rvl-lab-utoronto/drake-tamp/compare/main...allenapplehead:drake-tamp:main

FROM ubuntu:24.04
# FROM moby21.jaist.ac.jp/s2530012/ompl-base-refined-260402:1
# FROM nvidia/cuda:11.1.1-runtime-ubuntu18.04

RUN DEBIAN_FRONTEND=noninteractive

# ====================================================================
# Core Build Tools & Dependencies
# ====================================================================
# gcc and g++: Required for ompl and Drake (must be version 11)
# cmake & build-essential: Required to build FastDownward
# Reference:
#   - Drake supported configurations: https://drake.mit.edu/installation.html#supported-configurations
#   - Drake v1.49.0+ requires gcc-13: https://drake.mit.edu/release_notes/v1.49.0.html
#   - We use drake==1.48.0 which supports gcc-11
# Additional tools: curl, python3, unzip, git, vim

RUN apt-get -y update && apt-get -y install --no-install-recommends \
    curl \
    \
    # * gcc and g++ are required for installing ompl and it has to be version 11.
    # Drake also requires them and the latest one requires version 13 for installing drake 1.51.0.
    # * As there is the conflict between ompl and drake, we will install gcc-11 and g++-11
    # and we decided to use drake==1.48.0 which is the latest version that supports gcc-11.
    # [Reference]
    # https://drake.mit.edu/installation.html#supported-configurations
    # Starting with the drake 1.49.0, support for gcc-13 is required.
    # https://drake.mit.edu/release_notes/v1.49.0.html
    gcc-11 g++-11 \
    \
    python3 \
    python3-dev \
    \
    # NOTE: cmake & build-essential (make) is required to build FastDownward.
    cmake build-essential \
    \
    unzip \
    git vim \
    # \
    # Maybe not required
    # libgl1-mesa-dev libosmesa6-dev patchelf \
    # libopenmpi-dev libglew-dev libglfw3 libglfw3-dev \
    \
    && rm -rf /var/lib/apt/lists/* \
    && apt -y autoremove \
    \
    # HACK: FastDownward requires a specific version of gcc and g++. We will install gcc-11 and g++-11 and set them as default.
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 200 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 200 \
    && update-alternatives --install /usr/bin/cc cc /usr/bin/gcc-11 200 \
    && update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++-11 200 \
    && update-alternatives --set gcc /usr/bin/gcc-11 \
    && update-alternatives --set g++ /usr/bin/g++-11 \
    && update-alternatives --set cc /usr/bin/gcc-11 \
    && update-alternatives --set c++ /usr/bin/g++-11

# ====================================================================
# Compiler Environment Variables
# ====================================================================
ENV CC=/usr/bin/gcc-11
ENV CXX=/usr/bin/g++-11
ENV CMAKE_C_COMPILER=/usr/bin/gcc-11
ENV CMAKE_CXX_COMPILER=/usr/bin/g++-11


# ====================================================================
# Desktop Environment (VNC)
# ====================================================================
# for display through vnc
# Installation packages: xfce4, tigervnc, dbus (to avoid settings server error)

RUN apt-get -y update && apt-get -y install --no-install-recommends \
    xfce4 \
    tigervnc-standalone-server \
    tigervnc-tools \
    # To avoid Error: Unable to contact settings server Failed to execute child process "dbus-launch" (No such file orr directory)
    dbus-x11


# ====================================================================
# Utilities
# ====================================================================
# gedit: Text editor
# trash-cli: Safe delete command
# ffmpeg: Media tools
# xdg-utils: Open files with default applications
# tmux: Terminal multiplexer
# firefox: Web browser
# openssh-server: Remote access
# sudo: Privilege escalation
# xfce4-terminal: Terminal emulator
# jq: JSON query tool for log parsing (used in run.sh, collect-labels.sh)

RUN apt -y install --no-install-recommends \
    gedit \
    trash-cli \
    ffmpeg \
    xdg-utils \
    tmux \
    firefox \
    openssh-server \
    sudo \
    xfce4-terminal \
    jq

# ・jq:    シェルスクリプトでの JSON ログ解析
#          (run.sh, collect-labels.sh 等の実験スクリプトで使用)

# NOTE: They are required to install python-fcl
# RUN apt -y install --no-install-recommends liboctomap-dev

# ====================================================================
# Terminal Configuration
# ====================================================================
# update terminal config
RUN printf "2\n" | update-alternatives --config x-terminal-emulator

# ====================================================================
# Python Environment Setup (uv & venv)
# ====================================================================
# Setup Python 3.12 as default and prepare uv package manager
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# uv is used for efficient package management (faster than pip)

# set python3.12 as default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Prepare uv
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# # Prepare packages from pyproject.toml
# COPY environments/experiment/pyproject.toml /${WORKING_DIRECTORY}/pyproject.toml
# https://www.reddit.com/r/learnpython/comments/1hspt62/comment/m5sak3o/?tl=ja
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Python venv setup with drake
RUN mkdir -p /python_venvs/tamp
ENV PATH="/python_venvs/tamp/bin:$PATH"
WORKDIR /python_venvs/
RUN uv venv tamp --system-site-packages --python 3.12

WORKDIR /home/$user/
# other requirements
RUN uv pip install --upgrade setuptools
COPY requirements.txt requirements.txt
RUN uv pip install -r requirements.txt
# torch==1.9.0 は Python 3.12 (cp312) に対応したホイールが存在しないため 2.2.2 を使用
# RUN pip3 install torch==1.9.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
# RUN pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://pytorch-geometric.com/whl/torch-1.9.0+cu111.html
RUN uv pip install torch==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu
RUN uv pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-2.2.2+cpu.html

# ====================================================================
# User Setup
# ====================================================================
# arguments when building image
# login password
ARG password
# $UID
ARG id
# $USER
ARG user
ENV PASS=$password

# In case that the user is "ubuntu", you can add neither group nor user, since it already exists in the base image.
# In that case, just set the password for the existing user and add it to sudo group.
# --- For not ubuntu user ---
# RUN groupadd -g $id $user
# RUN useradd -s /bin/bash -u $id -g $id -m $user && echo "$user:$password" | chpasswd && adduser $user sudo
# --- For ubuntu user ---
RUN echo "$user:$password" | chpasswd && adduser $user sudo

# sudo 実行時にパスワード不要にする（entrypoint.sh での service 起動に必要）
RUN echo "$user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown -R $user /python_venvs
USER $user

# ====================================================================
# Python Path Configuration
# ====================================================================
# Add Drake-TAMP and related paths to PYTHONPATH for development
ENV PYTHONPATH=${PYTHONPATH}:/home/$user/drake-tamp/:/home/$user/drake-tamp/pddlstream/:/home/$user/furniture/:/home/$user/drake-tamp/experiments/ikea_induction/

# ====================================================================
# Shell Configuration
# ====================================================================
# Configure bash to automatically activate the virtual environment and set environment variables
RUN echo "source /python_venvs/tamp/bin/activate" >> ~/.bashrc
RUN echo "export  USER=$user" >> ~/.bashrc
RUN echo "export  PYTHONPATH=${PYTHONPATH}:/home/$user/drake-tamp/:/home/$user/drake-tamp/pddlstream/:/home/$user/experiments/ikea_induction/:/home/$user/drake-tamp/pddlstream/examples/pybullet/utils/" >> ~/.bashrc

# ====================================================================
# Git Configuration
# ====================================================================
# Configure git with user information (passed as build arguments)

ARG gitname
ARG gitemail

RUN git config --global user.name $gitname
RUN git config --global user.email $gitemail

# ====================================================================
# Entrypoint & Final Configuration
# ====================================================================
# Copy configuration files and set up the working directory
WORKDIR /home/$user/drake-tamp
COPY .tmux.conf /home/$user/.tmux.conf
# COPY .vimrc /home/$user/.vimrc

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash","/entrypoint.sh"]

CMD ["bash"]
