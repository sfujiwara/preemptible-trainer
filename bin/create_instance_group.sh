#!/bin/sh

BASE_NAME="trainer-$(date '+%Y%m%d%H%M%S')"
INSTANCE_TEMPLATE_NAME=${BASE_NAME}
INSTANCE_GROUP_NAME=${BASE_NAME}
PROJECT_ID=$(gcloud config list project --format "value(core.project)")
ZONE=us-central1-c

# Parameters
BATCH_SIZE=64
EPOCHS=2
OUTPUT_DIR="gs://${PROJECT_ID}/${BASE_NAME}"

# Create instance template for managed instance group
gcloud compute instance-templates create-with-container "${INSTANCE_TEMPLATE_NAME}" \
  --machine-type=n1-standard-1 \
  --metadata=google-logging-enabled=true \
  --preemptible \
  --scopes=cloud-platform \
  --boot-disk-size=200GB \
  --container-image="gcr.io/${PROJECT_ID}/trainer" \
  --container-arg="--batch_size=${BATCH_SIZE}" \
  --container-arg="--epochs=${EPOCHS}" \
  --container-arg="--output_dir=${OUTPUT_DIR}"

# Create managed instance group from the template
gcloud compute instance-groups managed create "${INSTANCE_GROUP_NAME}" \
  --base-instance-name=instance-group-1 \
  --template="${INSTANCE_TEMPLATE_NAME}" \
  --size=1 \
  --zone="${ZONE}"
