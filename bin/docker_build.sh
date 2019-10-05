#!/bin/sh

PROJECT_ID=$(gcloud config list project --format "value(core.project)")
IMAGE_NAME="trainer"

docker build -t ${IMAGE_NAME} .
docker tag ${IMAGE_NAME} "gcr.io/${PROJECT_ID}/${IMAGE_NAME}"
