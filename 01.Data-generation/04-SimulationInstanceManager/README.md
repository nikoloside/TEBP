# FractureRB Docker Implementation

## Overview
This Docker implementation allows you to run FractureRB simulations with Google Drive integration for data storage and retrieval. The system is designed to work with Ubuntu and includes automated build processes for the FractureRB library.

## Prerequisites
- Ubuntu 20.04 or later
- Docker Engine
- Google Drive API credentials
- Vultr API credentials (for cloud deployment)

## Installation Steps

### 1. Install Docker

- Add Docker's official GPG key:
> sudo apt-get update
> sudo apt-get install ca-certificates curl
> sudo install -m 0755 -d /etc/apt/keyrings
> sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
> sudo chmod a+r /etc/apt/keyrings/docker.asc

- Add the repository to Apt sources:
> echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
> sudo apt-get update

- Install the Docker packages.

> sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

### 2. Pull FractureRB Docker Image

> docker pull nikoloside/fracturerb-ubuntu:shape-impulse-shapenet
> 

## How to use

> brew install az

> az login


> brew install yq