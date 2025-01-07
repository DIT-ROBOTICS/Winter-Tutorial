FROM osrf/ros:noetic-desktop-full

# Install common tools
RUN apt-get update && apt-get install -y \
    curl \
    git \
    git-extras \
    htop \
    tree \
    net-tools \
    tmux \
    vim \
    wget \
    python3-pip \
    bash-completion

RUN apt-get update && apt-get install -y \
    ros-humble-dynamixel-sdk \
    ros-humble-turtlebot3-msgs \
    ros-humble-turtlebot3 \
    ros-humble-gazebo-ros-pkgs \

RUN apt-get update && apt-get dist-upgrade -y \
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && rm -rf /var/lib/apt/lists/*

ENV SHELL /bin/bash
ENV TERM=xterm-256color

CMD ["/bin/bash"]