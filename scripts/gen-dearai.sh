#!/bin/bash

set -euo pipefail

rm -fR dearai
mkdir dearai
mkdir dearai/src
mkdir dearai/src/integrations

find src -type f ! -name "_*" -not -path "*/_*/*" -exec uvx jinja2 --strict {} -o dearai/{} \;

cp -r src/pyak dearai/pyak
cp -r src/samples dearai/samples
cp -r data/kittehub-main dearai/kittehub

# READMEs are long and boring.
find dearai/samples -name "README.md" -exec rm -f {} \;

# truncate all README.md files to the first 6 lines, which should be the metadata.
find dearai/kittehub -type f -name "README.md" -exec sh -c 'awk "/^---/{f=!f; next} f" "$1" > tmp && mv tmp "$1"' _ {} \;

mv dearai/src/* dearai
rm -fR dearai/src
