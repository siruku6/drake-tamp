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
