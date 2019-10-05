#!/bin/sh

PROJECT_ID=$(gcloud config list project --format "value(core.project)")
IMAGE_NAME="trainer"

docker push "gcr.io/${PROJECT_ID}/${IMAGE_NAME}"
