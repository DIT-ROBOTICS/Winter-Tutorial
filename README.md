# how to use
### build docker environment
- `cd Winter-Tutorial/docker`
- `docker build -t dit/tutourial-ws-noetic:latest .`
- `docker compose up -d --build`
- `docker start tutorial-ws-ros1`
### open work space
- Attach Visual Studio Code
- `cd tutorial_ws`
- `source /opt/ros/noetic/setup.bash`
- `catkin_make`