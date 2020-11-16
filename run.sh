#!/bin/bash

gunicorn implModule:app -w 1 -b 0.0.0.0:444 -t 60