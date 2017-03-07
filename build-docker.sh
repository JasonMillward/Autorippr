#!/bin/bash -e
#
# Createas a container with autorippr in 
#
# Run like
#
# docker run -ti -v /tmp:/tmp  --device=/dev/sr1 autorippr --all --debug
#


docker build -t buildmakemkv ./build_makemkv
docker run --rm buildmakemkv | tar xz
docker build -t autorippr .
