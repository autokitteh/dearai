#!/bin/bash

set -euox pipefail

rm -fR data
mkdir data

curl https://raw.githubusercontent.com/autokitteh/autokitteh/refs/heads/main/manifest.schema.yaml > data/manifest.schema.yaml

curl -L https://github.com/autokitteh/kittehub/archive/refs/heads/main.zip > data/kittehub.zip
unzip data/kittehub.zip -d data
rm -f data/kittehub.zip

find . -name autokitteh.yaml -exec grep integration: {} \; | cut -d:  -f 2 | sort -u > data/integrations.txt
