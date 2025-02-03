#!/bin/bash

# Check if dataset argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <dataset_name>"
    exit 1
fi

# Store dataset name
DATASET=$1

# Run DAS query
OUTPUT=$(dasgoclient -query="summary dataset=${DATASET}" -json)

# Extract dataset information using awk
DATASET_NAME=$DATASET
DATASET_EVENTS=$(echo "$OUTPUT" | awk -F'[:,}]' '{for(i=1;i<=NF;i++) if ($i~/"nevents"/) print $(i+1)}')
DATASET_FILES=$(echo "$OUTPUT" | awk -F'[:,}]' '{for(i=1;i<=NF;i++) if ($i~/"nfiles"/) print $(i+1)}')
DATASET_SIZE=$(echo "$OUTPUT" | awk -F'[:,}]' '{for(i=1;i<=NF;i++) if ($i~/"file_size"/) print $(i+1)}')
DATASET_SIZE_GB=$(awk "BEGIN {printf \"%.2f\", $DATASET_SIZE/1e9}")

# Print results
echo ""
echo " Dataset Info"
echo "==============="
echo "Dataset: $DATASET_NAME"
echo "Events: $DATASET_EVENTS"
echo "Files: $DATASET_FILES"
echo "Size: $DATASET_SIZE_GB GB"
echo ""
