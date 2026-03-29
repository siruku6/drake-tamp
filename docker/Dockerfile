# 対応方針
# https://github.com/rvl-lab-utoronto/drake-tamp/compare/main...allenapplehead:drake-tamp:main

FROM python-ompl-base:ubuntu24.04
# FROM nvidia/cuda:11.1.1-runtime-ubuntu18.04

RUN DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y install --no-install-recommends \
    curl \
    unzip \
    git vim \
    \
    libgl1-mesa-dev libosmesa6-dev patchelf \
    libopenmpi-dev libglew-dev libglfw3 libglfw3-dev \
    \
    && rm -rf /var/lib/apt/lists/* \
    && apt -y autoremove


# for display through vnc
# ------------------------------------------------------------
# RUN dpkg --configure -a || true \
#     && apt --fix-broken install -y \
RUN apt-get -y update && apt-get -y install --no-install-recommends \
    xfce4 \
    tigervnc-standalone-server \
    tigervnc-tools \
    # To avoid Error: Unable to contact settings server Failed to execute child process "dbus-launch" (No such file orr directory)
    dbus-x11


# set python3.12 as default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# ----------------------------------------------------------------------
# Prepare uv
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# ----------------------------------------------------------------------
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# # Prepare packages from pyproject.toml
# COPY environments/experiment/pyproject.toml /${WORKING_DIRECTORY}/pyproject.toml
# https://www.reddit.com/r/learnpython/comments/1hspt62/comment/m5sak3o/?tl=ja
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
# RUN uv sync



# python venv setup with drake
RUN mkdir -p /python_venvs/tamp
WORKDIR /python_venvs/
RUN uv venv tamp --system-site-packages --python 3.12
WORKDIR /python_venvs/tamp


# utilities 
RUN apt -y install --no-install-recommends \
    gedit \
    trash-cli \
    ffmpeg \
    xdg-utils \
    tmux \
    openssh-server \
    sudo \
    xfce4-terminal \
    jq

# ・jq:    シェルスクリプトでの JSON ログ解析
#          (run.sh, collect-labels.sh 等の実験スクリプトで使用)

# NOTE: They are required to install python-fcl
RUN apt -y install --no-install-recommends liboctomap-dev libfcl-dev

# # bazel installation : it is required to install drake from source, with custom build.
# RUN apt-get -y install apt-transport-https gnupg
# RUN curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg
# RUN mv bazel.gpg /etc/apt/trusted.gpg.d/
# RUN echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
# RUN apt update && apt -y install bazel


# # pddlstream
#RUN git clone --recurse-submodules https://github.com/caelan/pddlstream.git pddlstream
#RUN cd pddlstream && ./FastDownward/build.py release64
#RUN cd pddlstream/FastDownward/builds && ln -s release64 release32
#ENV PYTHONPATH=${PYTHONPATH}:/python_venvs/tamp/pddlstream

# update terminal config
RUN printf "2\n" | update-alternatives --config x-terminal-emulator

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
# RUN groupadd -g $id $user
# RUN useradd -s /bin/bash -u $id -g $id -m $user && echo "$user:$password" | chpasswd && adduser $user sudo
RUN echo "$user:$password" | chpasswd && adduser $user sudo

# sudo 実行時にパスワード不要にする（entrypoint.sh での service 起動に必要）
RUN echo "$user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown -R $user /python_venvs
ENV PATH="/python_venvs/tamp/bin:$PATH"
USER $user



# NOTE: Not install mujoco as it is required only for furniture.
# -----------------------------------------------------------------------
# WORKDIR /home/$user/
# # mujoco
# RUN wget https://www.roboti.us/download/mujoco200_linux.zip -O mujoco.zip
# RUN unzip mujoco.zip -d .mujoco
# RUN mv .mujoco/mujoco200_linux .mujoco/mujoco200
# # add mujoco to LD_LIBRARY_PATH
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/$user/.mujoco/mujoco200/bin


# NOTE: Not install furniture specific dependencies here, since they may cause errors at pip install -r requirements.txt in furniture.
# -----------------------------------------------------------------------
# WORKDIR /home/$user/
# # start ikea specific stuff #
# RUN git clone https://github.com/BenAgro314/furniture.git
# WORKDIR /home/$user/furniture
# # NOTE: Problematic requirements.txt is here: https://github.com/BenAgro314/furniture/blob/aug2020_fixes/requirements.txt
# RUN git fetch origin aug2020_fixes:aug2020_fixes
# RUN git checkout aug2020_fixes
# RUN ln -s /home/$user/.mujoco/mujoco200 /home/$user/.mujoco/mujoco200_linux
# #RUN pip install --upgrade pip
# RUN uv pip install scikit-build
# RUN uv pip install glfw>=1.4.0 numpy>=1.19.5 Cython>=0.27.2 imageio>=2.1.2 cffi>=1.10 fasteners~=0.15 lockfile

# RUN uv pip install -r requirements.txt


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
ENV PYTHONPATH=${PYTHONPATH}:/home/$user/drake-tamp/:/home/$user/drake-tamp/pddlstream/:/home/$user/furniture/:/home/$user/drake-tamp/experiments/ikea_induction/

RUN echo "source /python_venvs/tamp/bin/activate" >> ~/.bashrc
RUN echo "export  USER=$user" >> ~/.bashrc
RUN echo "export  PYTHONPATH=${PYTHONPATH}:/home/$user/drake-tamp/:/home/$user/drake-tamp/pddlstream/:/home/$user/experiments/ikea_induction/:/home/$user/drake-tamp/pddlstream/examples/pybullet/utils/" >> ~/.bashrc
RUN echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/$user/.mujoco/mujoco200/bin" >> ~/.bashrc

ARG gitname
ARG gitemail

RUN git config --global user.name $gitname
RUN git config --global user.email $gitemail

WORKDIR /home/$user/drake-tamp
COPY .tmux.conf /home/$user/.tmux.conf
# COPY .vimrc /home/$user/.vimrc

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash","/entrypoint.sh"]

CMD ["bash"]
