#!/bin/bash

IMAGE=kilimo_data_science

# Running JupyterLab
docker run --rm --network="host" -p 8888:8888 -e GRANT_SUDO=yes -e JUPYTER_ENABLE_LAB=yes --user root -v $PWD/work:/home/jovyan/work $IMAGE 
