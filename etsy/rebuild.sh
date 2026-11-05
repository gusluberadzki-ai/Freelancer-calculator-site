#!/bin/sh
# Rebuild the Etsy pack into $1 and zip it to /mnt/project-files/income/etsy/
set -e; OUT=$1; rm -rf "$OUT"; cd "$(dirname "$0")"
python3 build.py "$OUT" 2>&1 | grep -v Warning; node render.js "$OUT/jobs.json"
cd "$OUT"; rm -rf _tmp jobs.json; rm -f ../Etsy-upload-pack.zip; zip -qr ../Etsy-upload-pack.zip .
mkdir -p /mnt/project-files/income/etsy; cp ../Etsy-upload-pack.zip listings.csv /mnt/project-files/income/etsy/
