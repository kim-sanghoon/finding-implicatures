#!/bin/bash

docker run -it \
  -p 0.0.0.0:8000:8000 \
  --env-file .env \
  --shm-size 1gb \
  implicature \
  /bin/bash
