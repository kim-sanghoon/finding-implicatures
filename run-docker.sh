#!/bin/bash
# If you need an interactive shell, remove '-d' option and attach '-it' option.

docker run --gpus all -it \
 -v $(pwd)/data:/data \
 -v $(pwd)/cache:/cache \
 -v $(pwd)/implModule.py:/implModule.py \
 -v $(pwd)/run.sh:/run.sh \
 -e TRANSFORMERS_CACHE=/cache/ \
 -p 0.0.0.0:444:444 \
 implicature