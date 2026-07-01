#!/usr/bin/env bash

set -euo pipefail

INPUT_FILE="sources-url"
OUTPUT_DIR="file-sources"

mkdir -p "$OUTPUT_DIR"

counter=1

while IFS= read -r url || [[ -n "$url" ]]; do
    # skip empty lines
    [[ -z "$url" ]] && continue

    filename=$(printf "source%02d.json" "$counter")

    echo "Downloading: $url"
    echo "Saving as: $OUTPUT_DIR/$filename"

    curl -L "$url" -o "$OUTPUT_DIR/$filename"

    ((counter++))
done < "$INPUT_FILE"

python3 ./colector.py

echo "Done."