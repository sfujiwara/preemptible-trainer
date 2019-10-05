#!/bin/sh

IMAGE_NAME="trainer"

docker run \
  -v ${HOME}/.config/gcloud:/root/.config/gcloud \
  -v $(pwd)/outputs:/app/outputs \
  --rm \
  -it \
  trainer --batch_size=64 --epochs=3 --output_dir=outputs
