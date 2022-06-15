#!/bin/bash

source "$( poetry env info --path )/bin/activate"
ray start --head --dashboard-host 0.0.0.0
python -m app.main

# do an infinite loop to prevent the container from exiting
while true
do
    sleep 10000
done
