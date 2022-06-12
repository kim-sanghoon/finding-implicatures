#!/bin/bash

source "$( poetry env info --path )/bin/activate"
python -m app.main
