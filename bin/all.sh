#!/bin/sh

./bin/docker_build.sh &&
./bin/docker_push.sh &&
./bin/create_instance_group.sh
